"""Graphviz DOT Compiler Engine for Electrical Single-Line Diagrams using Record & Port syntax."""

import html
import re
from typing import Any, Dict, List, Optional, Set
from james_app.models import Edge, Node, Project


def _clean_str(text: Any) -> str:
    """Clean string for Graphviz record labels without breaking syntax tokens."""
    if text is None:
        return ""
    # Remove/replace reserved record characters: { } < > | [ ] " \
    s = str(text).replace("{", "(").replace("}", ")").replace("<", "(").replace(">", ")")
    s = s.replace("|", "/").replace("[", "(").replace("]", ")").replace('"', "'").replace("\\", "/")
    return s.strip()


def _sanitize_id(identifier: str) -> str:
    """Sanitize identifier for valid Graphviz node ID."""
    clean = re.sub(r'[^a-zA-Z0-9_]', '_', str(identifier))
    if clean and clean[0].isdigit():
        clean = "n_" + clean
    return clean or "node"


def _make_silver_badge(
    text: str,
    font_size: int = 8,
    font_color: str = "#0F172A",
    bg_color: str = "#E2E8F0",
    border_color: str = "#94A3B8"
) -> str:
    """Wrap label text in an HTML-like table pill with a silver background for maximum readability over lines/borders."""
    if not text:
        return ""
    clean = html.escape(str(text).strip()).replace("\n", "<BR/>")
    return f'<<TABLE BGCOLOR="{bg_color}" BORDER="1" COLOR="{border_color}" CELLBORDER="0" CELLSPACING="0" CELLPADDING="3"><TR><TD><FONT POINT-SIZE="{font_size}" COLOR="{font_color}" FACE="Arial">{clean}</FONT></TD></TR></TABLE>>'



# Domain color definitions for Graphviz Single-Line Diagram
DOMAIN_CONFIG: Dict[str, Dict[str, str]] = {
    "sources": {
        "bg": "#FEF3C7",      # Pastel Amber
        "border": "#D97706",  # Amber 600
        "text": "#0F172A",    # Dark Slate 900
    },
    "transformers": {
        "bg": "#F3E8FF",      # Pastel Purple
        "border": "#9333EA",  # Purple 600
        "text": "#0F172A",
    },
    "switches": {
        "bg": "#DBEAFE",      # Pastel Blue
        "border": "#2563EB",  # Blue 600
        "text": "#0F172A",
    },
    "panels": {
        "bg": "#F1F5F9",      # Pastel Slate
        "border": "#475569",  # Slate 600
        "text": "#0F172A",
    },
    "power_quality": {
        "bg": "#D1FAE5",      # Pastel Emerald
        "border": "#059669",  # Emerald 600
        "text": "#0F172A",
    },
    "loads": {
        "bg": "#CCFBF1",      # Pastel Teal
        "border": "#0D9488",  # Teal 600
        "text": "#0F172A",
    },
    "cables": {
        "bg": "#FFEDD5",      # Pastel Orange
        "border": "#EA580C",  # Orange 600
        "text": "#0F172A",
    },
    "metering": {
        "bg": "#E0F2FE",      # Pastel Sky
        "border": "#0284C7",  # Sky 600
        "text": "#0F172A",
    },
    "renewables": {
        "bg": "#FEF9C3",      # Pastel Yellow
        "border": "#CA8A04",  # Yellow 600
        "text": "#0F172A",
    },
    "generic": {
        "bg": "#F8FAFC",      # Pastel Slate Light
        "border": "#64748B",  # Slate 500
        "text": "#0F172A",
    },
}

PORT_STYLE = 'fillcolor="#334155", fontcolor="#FFFFFF", color="#1E293B"'


def _get_equipment_unit(type_tag: str = "", is_mcc: bool = False) -> tuple[str, str]:
    """Return (singular, plural) physical unit names for electrical equipment."""
    tag = (type_tag or "").upper()
    if tag == "MCC" or is_mcc:
        return "Bucket", "Buckets"
    if tag in ["MDP", "SWBD", "SWGR", "MSB"]:
        return "Space", "Spaces"
    if tag in ["PDU", "RPP"]:
        return "Pole", "Poles"
    return "Slot", "Slots"


def _format_slot_range(slot_num: int, poles: int = 1, type_tag: str = "", is_mcc: bool = False) -> str:
    """Format slot, bucket, space, or pole string representing the full physical occupied range (e.g. 'Slots 1, 3, 5')."""
    sing, plur = _get_equipment_unit(type_tag=type_tag, is_mcc=is_mcc)
    if poles <= 1:
        return f"{sing} {slot_num}"
    
    slots = [str(slot_num + (p * 2)) for p in range(poles)]
    return f"{plur} {', '.join(slots)}"


def _build_cluster_title(n: Dict[str, Any]) -> str:
    """Build rich, compact multi-line equipment cluster title for single-line diagram headers."""
    name = _clean_str(n.get("name", "Equipment"))
    tag = _clean_str(n.get("tag", "EQ"))
    domain = n.get("domain", "generic")
    type_tag = n.get("type_tag", "")
    volts = _clean_str(n.get("voltage", ""))
    amps = n.get("amps", "")
    amps_str = f"{amps}A" if amps else ""
    aic = n.get("aic") or (n.get("attributes") or {}).get("aic")
    aic_str = f"{aic}kA AIC" if aic else ""
    room = n.get("room")
    room_str = f"[{room}]" if room else ""

    line1 = f"{name} ({tag})"
    line2_parts: List[str] = []
    line3_parts: List[str] = []

    # Domain-specific physical attributes
    if n.get("is_panel") or domain == "panels" or type_tag in ["LP", "MDP", "MCC", "PP", "REC", "PDU"]:
        slots = n.get("slots") or (n.get("attributes") or {}).get("slots") or (n.get("attributes") or {}).get("defaultSlots") or 42
        main_type = (n.get("attributes") or {}).get("main_type", "Main Lugs")
        main_abbr = "MCB" if "breaker" in str(main_type).lower() or "mcb" in str(main_type).lower() else ("MLO" if "lug" in str(main_type).lower() or "mlo" in str(main_type).lower() else str(main_type))
        sing, _ = _get_equipment_unit(type_tag=type_tag)
        line2_parts.append(f"{slots}-{sing} ({main_abbr})")
        if amps_str or volts:
            line2_parts.append(f"{amps_str} {volts}".strip())
        if aic_str:
            line3_parts.append(aic_str)

    elif domain == "transformers" or type_tag in ["XFMR", "PAD"]:
        kva = n.get("kva") or (n.get("attributes") or {}).get("kva")
        if kva:
            line2_parts.append(f"{kva}kVA")
        if volts:
            line2_parts.append(volts)
        z_pct = (n.get("attributes") or {}).get("impedance_z") or (n.get("attributes") or {}).get("z_pct")
        if z_pct:
            line3_parts.append(f"{z_pct}% Z")

    elif domain == "switches" or type_tag in ["ATS", "MTS", "DISC"]:
        if amps_str or volts:
            line2_parts.append(f"{amps_str} {volts}".strip())
        trans = (n.get("attributes") or {}).get("transition_type")
        if trans:
            line2_parts.append(str(trans))
        if aic_str:
            line3_parts.append(aic_str)

    elif domain == "sources" or type_tag in ["UTIL", "GEN", "PV"]:
        if amps_str or volts:
            line2_parts.append(f"{amps_str} {volts}".strip())
        if aic_str:
            line3_parts.append(aic_str)

    elif domain == "power_quality" or type_tag in ["UPS", "PDU"]:
        kva = n.get("kva") or (n.get("attributes") or {}).get("kva")
        if kva:
            line2_parts.append(f"{kva}kVA")
        if amps_str or volts:
            line2_parts.append(f"{amps_str} {volts}".strip())
        batt = (n.get("attributes") or {}).get("runtime_min")
        if batt:
            line3_parts.append(f"{batt} min backup")

    elif domain == "loads" or type_tag in ["HVAC", "MOTOR", "EV", "PUMP"]:
        hp = (n.get("attributes") or {}).get("hp")
        if hp:
            line2_parts.append(f"{hp} HP")
        if amps_str or volts:
            line2_parts.append(f"{amps_str} {volts}".strip())

    else:
        if amps_str or volts:
            line2_parts.append(f"{amps_str} {volts}".strip())
        if aic_str:
            line3_parts.append(aic_str)

    # Location / Room on line 3 (or line 2 if line 2 is empty)
    if room_str:
        if not line2_parts and not line3_parts:
            line2_parts.append(room_str)
        else:
            line3_parts.append(room_str)

    lines = [line1]
    if line2_parts:
        lines.append(" • ".join(line2_parts))
    if line3_parts:
        lines.append(" • ".join(line3_parts))

    return "\\n".join(lines)


def _find_feeder_slot_in_parent(parent_node: Dict[str, Any], child_node: Dict[str, Any]):
    """Search the parent's panel schedule for a breaker targeting child_node."""
    schedule = (parent_node.get("attributes") or {}).get("schedule", [])
    if not schedule or not isinstance(schedule, list):
        return None, 1, "", None

    c_tag = (child_node.get("tag") or "").strip().upper()
    c_id = (child_node.get("id") or "").strip().upper()
    c_name = (child_node.get("name") or "").strip().upper()

    for row in schedule:
        if not isinstance(row, dict):
            continue
        # Check left side
        left_target = str(row.get("leftTargetLoad") or "").strip().upper()
        left_desc = str(row.get("leftDesc") or row.get("leftDescription") or "").strip().upper()
        left_trip = row.get("leftTrip") or row.get("leftAmps")
        if left_trip:
            matched = False
            if left_target and (left_target == c_tag or left_target == c_id):
                matched = True
            elif left_desc and (left_desc == c_name or (c_tag and c_tag in left_desc)):
                matched = True
            
            if matched:
                slot_num = int(row.get("leftParentSlot") or row.get("leftSlot") or 1)
                poles = int(row.get("leftPoles") or 1)
                amps = str(left_trip).strip()
                return slot_num, poles, amps, "left"

        # Check right side
        right_target = str(row.get("rightTargetLoad") or "").strip().upper()
        right_desc = str(row.get("rightDesc") or row.get("rightDescription") or "").strip().upper()
        right_trip = row.get("rightTrip") or row.get("rightAmps")
        if right_trip:
            matched = False
            if right_target and (right_target == c_tag or right_target == c_id):
                matched = True
            elif right_desc and (right_desc == c_name or (c_tag and c_tag in right_desc)):
                matched = True

            if matched:
                slot_num = int(row.get("rightParentSlot") or row.get("rightSlot") or 2)
                poles = int(row.get("rightPoles") or 1)
                amps = str(right_trip).strip()
                return slot_num, poles, amps, "right"

    return None, 1, "", None


def _get_node_upstream_sources(n: Dict[str, Any], all_nodes: List[Dict[str, Any]]) -> List[str]:
    """Gather all upstream source tags for a node, combining fed_from, upstream_sources, and panel schedule breaker links."""
    sources_list = []
    if n.get("fed_from"):
        sources_list.append(str(n.get("fed_from")).strip())
    raw_sources = (n.get("attributes") or {}).get("upstream_sources") or []
    for s in raw_sources:
        s_clean = str(s).strip()
        if s_clean and s_clean not in sources_list:
            sources_list.append(s_clean)
    if (n.get("attributes") or {}).get("emergency_source"):
        em_clean = str((n.get("attributes") or {}).get("emergency_source")).strip()
        if em_clean and em_clean not in sources_list:
            sources_list.append(em_clean)

    # Bidirectional discovery: scan all panels to check if any breaker explicitly targets this node
    child_tag = (n.get("tag") or "").strip().upper()
    child_id = (n.get("id") or "").strip().upper()
    for parent in all_nodes:
        if parent.get("id") == n.get("id"):
            continue
        p_tag = (parent.get("tag") or "").strip()
        if not p_tag:
            continue
        schedule = (parent.get("attributes") or {}).get("schedule", [])
        if schedule and isinstance(schedule, list):
            for row in schedule:
                if not isinstance(row, dict):
                    continue
                lt = str(row.get("leftTargetLoad") or "").strip().upper()
                rt = str(row.get("rightTargetLoad") or "").strip().upper()
                if (lt and (lt == child_tag or lt == child_id)) or (rt and (rt == child_tag or rt == child_id)):
                    if p_tag not in sources_list and (parent.get("id") not in sources_list):
                        sources_list.append(p_tag)
                    break

    return sources_list


def compile_facility_to_dot(nodes: List[Dict[str, Any]], mode: str = "detailed") -> str:
    """Compile a list of facility equipment nodes into Graphviz DOT single-line diagram.
    
    Supports:
    - mode='detailed' (default): Cluster-based layout with discrete port rectangles and breaker slots.
    - mode='macro': Consolidated single-node boxes per equipment for high-level power flow hierarchy.
    """
    dot_lines = [
        "digraph ElectricalOneLine {",
        '    graph [rankdir=TB, splines=polyline, nodesep=0.75, ranksep=0.95, compound=true, fontname="Arial", bgcolor="#CBD5E1"];',
        '    node [fontname="Arial", fontsize=9, shape=box, style="filled,rounded", color="#1E293B", fillcolor="#334155", fontcolor="#FFFFFF", penwidth=1.0];',
        '    edge [fontname="Arial", fontsize=9, color="#0F172A", fontcolor="#0F172A", penwidth=2.0, arrowsize=0.85];',
        ""
    ]

    nodes_by_tag: Dict[str, Dict[str, Any]] = {}
    nodes_by_id: Dict[str, Dict[str, Any]] = {}
    for n in nodes:
        tag = n.get("tag")
        if tag:
            nodes_by_tag[tag] = n
        nodes_by_id[n.get("id", tag)] = n

    if mode == "macro":
        # 1. Render each equipment as a single consolidated node box
        for n in nodes:
            node_id = _sanitize_id(n.get("id", n.get("tag", "eq")))
            domain = n.get("domain", "generic")
            cluster_title = _build_cluster_title(n)
            palette = DOMAIN_CONFIG.get(domain, DOMAIN_CONFIG["generic"])
            
            dot_lines.append(
                f'    {node_id} [label="{cluster_title}", shape=box, style="filled,rounded", '
                f'color="{palette["border"]}", fillcolor="{palette["bg"]}", fontcolor="{palette["text"]}", '
                f'penwidth=2.0, margin="0.2,0.12"];'
            )
        
        dot_lines.append("")
        # 2. Render Direct Edges with Arrowtail & Arrowhead Labels (Parent -> Child)
        rendered_edges = set()
        for n in nodes:
            node_id = _sanitize_id(n.get("id", n.get("tag", "eq")))
            type_tag = n.get("type_tag", "")
            child_domain = n.get("domain", "")

            # Gather all configured upstream sources (including breaker targetLoad links)
            sources_list = _get_node_upstream_sources(n, nodes)

            for s_idx, fed_from in enumerate(sources_list):
                parent_node = nodes_by_tag.get(fed_from) or nodes_by_id.get(fed_from)
                if not parent_node:
                    continue
                parent_id = _sanitize_id(parent_node.get("id", parent_node.get("tag", "eq")))
                parent_domain = parent_node.get("domain", "")
                parent_type = parent_node.get("type_tag", "")

                edge_key = (parent_id, node_id)
                if edge_key in rendered_edges:
                    continue
                rendered_edges.add(edge_key)

                # 1. Determine Tail Label (Upstream Breaker / Output Port)
                tail_parts = []
                if parent_node.get("is_panel") or parent_domain == "panels":
                    slot_num, poles, amps, side = _find_feeder_slot_in_parent(parent_node, n)
                    if slot_num:
                        poles_str = f"/{poles}P" if poles > 1 else ""
                        slot_str = _format_slot_range(slot_num, poles, type_tag=parent_type)
                        tail_parts.append(f"{slot_str} • {amps}A{poles_str}" if amps else slot_str)
                    else:
                        tail_parts.append("Feeder Out")
                elif parent_domain == "transformers" or parent_type in ["XFMR", "PAD"]:
                    tail_parts.append("Secondary Out")
                elif parent_domain == "sources" or parent_type in ["UTIL", "GEN", "PV"]:
                    port_label = "Mtr / Main Out" if parent_type == "UTIL" else ("Gen Breaker" if parent_type == "GEN" else "Inverter Out")
                    tail_parts.append(port_label)
                elif parent_domain == "switches" or parent_type in ["ATS", "MTS", "DISC"]:
                    tail_parts.append("Load Out")
                elif parent_domain == "power_quality" or parent_type == "UPS":
                    tail_parts.append("Inverter Out")
                elif parent_domain == "cables" or parent_type in ["CABLE", "FEEDER"]:
                    tail_parts.append("Load Out")
                else:
                    tail_parts.append("Out")

                tail_label = _clean_str(" • ".join(tail_parts))

                # 2. Determine Head Label (Downstream Input Terminal)
                is_emergency = (s_idx == 1 and type_tag in ["ATS", "MTS", "STS"]) or (parent_type == "GEN" and type_tag in ["ATS", "MTS", "STS"])
                head_parts = []
                if type_tag in ["ATS", "MTS", "STS"]:
                    head_parts.append("Emerg In" if is_emergency else ("Normal In" if s_idx == 0 else f"Source {s_idx+1} In"))
                elif type_tag in ["XFMR", "PAD"]:
                    head_parts.append("Primary In" if s_idx == 0 else f"Feeder {s_idx+1} In")
                elif n.get("is_panel") or child_domain == "panels" or type_tag in ["LP", "MDP", "MCC", "PP", "REC", "PDU"]:
                    main_type = (n.get("attributes") or {}).get("main_type", "Main Lugs")
                    head_parts.append(main_type if s_idx == 0 else f"Feeder {s_idx+1}")
                elif child_domain == "power_quality" or type_tag == "UPS":
                    head_parts.append("UPS Input" if s_idx == 0 else "Bypass Input")
                elif child_domain == "loads" or type_tag in ["HVAC", "MOTOR", "EV", "PUMP"]:
                    head_parts.append("Disconnect / Lugs")
                elif child_domain == "metering" or type_tag in ["METER", "MTR"]:
                    head_parts.append("CT / Voltage Sense In")
                elif child_domain == "renewables" or type_tag in ["BESS", "SOLAR"]:
                    head_parts.append("Bi-Directional AC In/Out")
                elif child_domain == "cables" or type_tag in ["CABLE", "FEEDER"]:
                    head_parts.append("Line In")
                else:
                    head_parts.append(f"In {s_idx+1}" if s_idx > 0 else "In")

                head_label = _clean_str(" • ".join(head_parts))

                # 3. Conductor Wire Label (Center)
                conductor = (n.get("attributes") or {}).get("conductor") or n.get("conductor")
                cond_attr = f'label={_make_silver_badge(conductor, font_size=8, font_color="#1E293B", bg_color="#F1F5F9", border_color="#94A3B8")}, ' if conductor else ''

                edge_color = "#B45309" if is_emergency else "#0F172A"
                edge_penwidth = "2.2" if is_emergency else "2.0"
                tail_badge = _make_silver_badge(tail_label, font_size=8, font_color="#9A3412" if is_emergency else "#0F172A", bg_color="#FEF3C7" if is_emergency else "#E2E8F0", border_color="#D97706" if is_emergency else "#94A3B8")
                head_badge = _make_silver_badge(head_label, font_size=8, font_color="#9A3412" if is_emergency else "#0F172A", bg_color="#FEF3C7" if is_emergency else "#E2E8F0", border_color="#D97706" if is_emergency else "#94A3B8")

                dot_lines.append(
                    f'    {parent_id} -> {node_id} ['
                    f'color="{edge_color}", penwidth={edge_penwidth}, {cond_attr}'
                    f'taillabel={tail_badge}, headlabel={head_badge}, '
                    f'labeldistance=2.4, labelangle={"-25" if is_emergency else "25"}];'
                )

        # Fallback for standalone GEN to ATS if ATS has not been explicitly connected to an emergency source
        for n in nodes:
            if n.get("type_tag") == "GEN":
                gen_id = _sanitize_id(n.get("id", n.get("tag", "gen")))
                for candidate in nodes:
                    if candidate.get("type_tag") in ["ATS", "MTS", "STS"] or candidate.get("domain") == "switches":
                        ats_id = _sanitize_id(candidate.get("id", candidate.get("tag", "ats")))
                        edge_key = (gen_id, ats_id)
                        if edge_key not in rendered_edges:
                            rendered_edges.add(edge_key)
                            tail_badge = _make_silver_badge("Gen Breaker", font_size=8, font_color="#9A3412", bg_color="#FEF3C7", border_color="#D97706")
                            head_badge = _make_silver_badge("Emerg In", font_size=8, font_color="#9A3412", bg_color="#FEF3C7", border_color="#D97706")
                            dot_lines.append(
                                f'    {gen_id} -> {ats_id} ['
                                f'color="#B45309", penwidth=2.2, '
                                f'taillabel={tail_badge}, headlabel={head_badge}, '
                                f'labeldistance=2.4, labelangle=-25];'
                            )
                            break

        dot_lines.append("}")
        return "\n".join(dot_lines)

    # 1. Render Equipment Enclosures as Subgraph Clusters with Port Rectangles (Detailed Mode)
    for n in nodes:
        node_id = _sanitize_id(n.get("id", n.get("tag", "eq")))
        tag = _clean_str(n.get("tag", "EQ"))
        name = _clean_str(n.get("name", "Equipment"))
        domain = n.get("domain", "generic")
        type_tag = n.get("type_tag", "")

        cluster_title = _build_cluster_title(n)

        # Lookup domain palette
        palette = DOMAIN_CONFIG.get(domain, DOMAIN_CONFIG["generic"])

        # Cluster by Equipment Archetype with Pastel BG + Black text + Dark Gray Ports with White text
        if domain == "sources" or type_tag in ["UTIL", "GEN", "PV"]:
            palette = DOMAIN_CONFIG["sources"]
            port_label = "Mtr / Main Out" if type_tag == "UTIL" else ("Gen Breaker" if type_tag == "GEN" else "Inverter Out")
            dot_lines.extend([
                f'    subgraph cluster_{node_id} {{',
                f'        label = "{cluster_title}";',
                '        style = "filled,rounded";',
                f'        color = "{palette["border"]}";',
                f'        fillcolor = "{palette["bg"]}";',
                f'        fontcolor = "{palette["text"]}";',
                '        penwidth = 1.8;',
                f'        {node_id}_out [label="{port_label}", {PORT_STYLE}];',
                '    }',
                ''
            ])

        elif domain == "switches" or type_tag in ["ATS", "MTS", "DISC"]:
            palette = DOMAIN_CONFIG["switches"]
            if type_tag in ["ATS", "MTS"]:
                dot_lines.extend([
                    f'    subgraph cluster_{node_id} {{',
                    f'        label = "{cluster_title}";',
                    '        style = "filled,rounded";',
                    f'        color = "{palette["border"]}";',
                    f'        fillcolor = "{palette["bg"]}";',
                    f'        fontcolor = "{palette["text"]}";',
                    '        penwidth = 1.8;',
                    f'        {node_id}_norm  [label="Normal In", {PORT_STYLE}];',
                    f'        {node_id}_emerg [label="Emerg In", {PORT_STYLE}];',
                    f'        {node_id}_out   [label="Load Out", {PORT_STYLE}];',
                    f'        {{ rank=same; {node_id}_norm; {node_id}_emerg; }}',
                    f'        {node_id}_norm -> {node_id}_out [style=invis];',
                    '    }',
                    ''
                ])
            else:
                dot_lines.extend([
                    f'    subgraph cluster_{node_id} {{',
                    f'        label = "{cluster_title}";',
                    '        style = "filled,rounded";',
                    f'        color = "{palette["border"]}";',
                    f'        fillcolor = "{palette["bg"]}";',
                    f'        fontcolor = "{palette["text"]}";',
                    '        penwidth = 1.8;',
                    f'        {node_id}_in  [label="Line In", {PORT_STYLE}];',
                    f'        {node_id}_out [label="Load Out", {PORT_STYLE}];',
                    f'        {node_id}_in -> {node_id}_out [style=invis];',
                    '    }',
                    ''
                ])

        elif domain == "transformers" or type_tag in ["XFMR", "PAD"]:
            palette = DOMAIN_CONFIG["transformers"]
            dot_lines.extend([
                f'    subgraph cluster_{node_id} {{',
                f'        label = "{cluster_title}";',
                '        style = "filled,rounded";',
                f'        color = "{palette["border"]}";',
                f'        fillcolor = "{palette["bg"]}";',
                f'        fontcolor = "{palette["text"]}";',
                '        penwidth = 1.8;',
                f'        {node_id}_in  [label="Primary In", {PORT_STYLE}];',
                f'        {node_id}_out [label="Secondary Out", {PORT_STYLE}];',
                f'        {node_id}_in -> {node_id}_out [style=invis];',
                '    }',
                ''
            ])

        elif n.get("is_panel") or domain == "panels" or type_tag in ["LP", "MDP", "MCC", "PP", "REC", "PDU"]:
            palette = DOMAIN_CONFIG["panels"]
            main_device = (n.get("attributes") or {}).get("main_device") or (n.get("attributes") or {}).get("main_type") or "Main Lugs"
            if main_device == "MCB":
                main_type = "MCB (Main Breaker)"
            elif main_device == "MLO":
                main_type = "MLO (Main Lugs)"
            else:
                main_type = main_device

            schedule = (n.get("attributes") or {}).get("schedule", [])
            
            breaker_nodes = []
            breaker_ids = []
            if schedule and isinstance(schedule, list):
                for row in schedule:
                    left_trip = row.get("leftAmps") or row.get("leftTrip")
                    is_left_ganged = row.get("leftIsGanged") or bool(row.get("leftParentSlot"))
                    is_mcc_panel = (type_tag == "MCC" or "mcc" in str(n.get("type_name", "")).lower())
                    if left_trip is not None and str(left_trip).strip() and not is_left_ganged:
                        s_num = row.get("leftSlot")
                        desc = _clean_str(row.get("leftDescription") or row.get("leftDesc") or row.get("leftTargetLoad") or f"Circuit {s_num}")
                        trip = _clean_str(str(left_trip))
                        poles = row.get("leftPoles", 1)
                        try:
                            poles_int = int(poles)
                        except (ValueError, TypeError):
                            poles_int = 1
                        poles_str = f"/{poles_int}P" if poles_int > 1 else ""
                        slot_str = _format_slot_range(int(s_num), poles_int, type_tag=type_tag)
                        b_id = f"{node_id}_b{s_num}"
                        if b_id not in breaker_ids:
                            breaker_ids.append(b_id)
                            breaker_nodes.append(f'        {b_id} [label="[ {slot_str} ]\\n{desc}\\n{trip}A{poles_str}", {PORT_STYLE}];')

                    right_trip = row.get("rightAmps") or row.get("rightTrip")
                    is_right_ganged = row.get("rightIsGanged") or bool(row.get("rightParentSlot"))
                    if right_trip is not None and str(right_trip).strip() and not is_right_ganged:
                        s_num = row.get("rightSlot")
                        desc = _clean_str(row.get("rightDescription") or row.get("rightDesc") or row.get("rightTargetLoad") or f"Circuit {s_num}")
                        trip = _clean_str(str(right_trip))
                        poles = row.get("rightPoles", 1)
                        try:
                            poles_int = int(poles)
                        except (ValueError, TypeError):
                            poles_int = 1
                        poles_str = f"/{poles_int}P" if poles_int > 1 else ""
                        slot_str = _format_slot_range(int(s_num), poles_int, type_tag=type_tag)
                        b_id = f"{node_id}_b{s_num}"
                        if b_id not in breaker_ids:
                            breaker_ids.append(b_id)
                            breaker_nodes.append(f'        {b_id} [label="[ {slot_str} ]\\n{desc}\\n{trip}A{poles_str}", {PORT_STYLE}];')

            if breaker_ids:
                rank_same = " ".join(breaker_ids)
                dot_lines.extend([
                    f'    subgraph cluster_{node_id} {{',
                    f'        label = "{cluster_title}";',
                    '        style = "filled,rounded";',
                    f'        color = "{palette["border"]}";',
                    f'        fillcolor = "{palette["bg"]}";',
                    f'        fontcolor = "{palette["text"]}";',
                    '        penwidth = 1.8;',
                    f'        {node_id}_in  [label="{main_type}", {PORT_STYLE}];',
                    f'        {node_id}_out [label="Feeder / Aux Out", {PORT_STYLE}];',
                    *breaker_nodes,
                    f'        {{ rank=same; {rank_same}; }}',
                    f'        {node_id}_in -> {breaker_ids[0]} [style=invis];',
                    '    }',
                    ''
                ])
            else:
                dot_lines.extend([
                    f'    subgraph cluster_{node_id} {{',
                    f'        label = "{cluster_title}";',
                    '        style = "filled,rounded";',
                    f'        color = "{palette["border"]}";',
                    f'        fillcolor = "{palette["bg"]}";',
                    f'        fontcolor = "{palette["text"]}";',
                    '        penwidth = 1.8;',
                    f'        {node_id}_in  [label="{main_type}", {PORT_STYLE}];',
                    f'        {node_id}_out [label="Load Out", {PORT_STYLE}];',
                    f'        {node_id}_in -> {node_id}_out [style=invis];',
                    '    }',
                    ''
                ])

        elif domain == "power_quality" or type_tag == "UPS":
            palette = DOMAIN_CONFIG["power_quality"]
            dot_lines.extend([
                f'    subgraph cluster_{node_id} {{',
                f'        label = "{cluster_title}";',
                '        style = "filled,rounded";',
                f'        color = "{palette["border"]}";',
                f'        fillcolor = "{palette["bg"]}";',
                f'        fontcolor = "{palette["text"]}";',
                '        penwidth = 1.8;',
                f'        {node_id}_in     [label="UPS Input", {PORT_STYLE}];',
                f'        {node_id}_bypass [label="Bypass In", {PORT_STYLE}];',
                f'        {node_id}_out    [label="Inverter Out", {PORT_STYLE}];',
                f'        {{ rank=same; {node_id}_in; {node_id}_bypass; }}',
                f'        {node_id}_in -> {node_id}_out [style=invis];',
                '    }',
                ''
            ])

        elif domain == "loads" or type_tag in ["HVAC", "MOTOR", "EV", "PUMP"]:
            palette = DOMAIN_CONFIG["loads"]
            dot_lines.extend([
                f'    subgraph cluster_{node_id} {{',
                f'        label = "{cluster_title}";',
                '        style = "filled,rounded";',
                f'        color = "{palette["border"]}";',
                f'        fillcolor = "{palette["bg"]}";',
                f'        fontcolor = "{palette["text"]}";',
                '        penwidth = 1.8;',
                f'        {node_id}_in [label="Disconnect / Lugs", {PORT_STYLE}];',
                '    }',
                ''
            ])

        elif domain == "cables" or type_tag in ["CABLE", "FEEDER"]:
            palette = DOMAIN_CONFIG["cables"]
            dot_lines.extend([
                f'    subgraph cluster_{node_id} {{',
                f'        label = "{cluster_title}";',
                '        style = "filled,rounded";',
                f'        color = "{palette["border"]}";',
                f'        fillcolor = "{palette["bg"]}";',
                f'        fontcolor = "{palette["text"]}";',
                '        penwidth = 1.8;',
                f'        {node_id}_in  [label="Line In", {PORT_STYLE}];',
                f'        {node_id}_out [label="Load Out", {PORT_STYLE}];',
                f'        {node_id}_in -> {node_id}_out [style=invis];',
                '    }',
                ''
            ])

        elif domain == "metering" or type_tag in ["METER", "MTR"]:
            palette = DOMAIN_CONFIG["metering"]
            dot_lines.extend([
                f'    subgraph cluster_{node_id} {{',
                f'        label = "{cluster_title}";',
                '        style = "filled,rounded";',
                f'        color = "{palette["border"]}";',
                f'        fillcolor = "{palette["bg"]}";',
                f'        fontcolor = "{palette["text"]}";',
                '        penwidth = 1.8;',
                f'        {node_id}_in  [label="CT / Voltage Sense In", {PORT_STYLE}];',
                '    }',
                ''
            ])

        elif domain == "renewables" or type_tag in ["BESS", "SOLAR"]:
            palette = DOMAIN_CONFIG["renewables"]
            dot_lines.extend([
                f'    subgraph cluster_{node_id} {{',
                f'        label = "{cluster_title}";',
                '        style = "filled,rounded";',
                f'        color = "{palette["border"]}";',
                f'        fillcolor = "{palette["bg"]}";',
                f'        fontcolor = "{palette["text"]}";',
                '        penwidth = 1.8;',
                f'        {node_id}_in  [label="Bi-Directional AC In/Out", {PORT_STYLE}];',
                '    }',
                ''
            ])

        else:
            palette = DOMAIN_CONFIG.get(domain, DOMAIN_CONFIG["generic"])
            dot_lines.extend([
                f'    subgraph cluster_{node_id} {{',
                f'        label = "{cluster_title}";',
                '        style = "filled,rounded";',
                f'        color = "{palette["border"]}";',
                f'        fillcolor = "{palette["bg"]}";',
                f'        fontcolor = "{palette["text"]}";',
                '        penwidth = 1.8;',
                f'        {node_id}_in  [label="In", {PORT_STYLE}];',
                f'        {node_id}_out [label="Out", {PORT_STYLE}];',
                f'        {node_id}_in -> {node_id}_out [style=invis];',
                '    }',
                ''
            ])

    dot_lines.append("")

    # 2. Render Edges between Discrete Port Nodes (South -> North)
    detailed_rendered_edges = set()
    for n in nodes:
        node_id = _sanitize_id(n.get("id", n.get("tag", "eq")))
        type_tag = n.get("type_tag", "")
        child_domain = n.get("domain", "")
        attrs = n.get("attributes") or {}

        # Gather all configured upstream sources (including breaker targetLoad links)
        sources_list = _get_node_upstream_sources(n, nodes)

        for s_idx, fed_from in enumerate(sources_list):
            parent_node = nodes_by_tag.get(fed_from) or nodes_by_id.get(fed_from)
            if not parent_node:
                continue
            parent_id = _sanitize_id(parent_node.get("id", parent_node.get("tag", "eq")))
            parent_domain = parent_node.get("domain", "")
            parent_type = parent_node.get("type_tag", "")

            is_emergency = (s_idx == 1 and type_tag in ["ATS", "MTS", "STS"]) or (parent_type == "GEN" and type_tag in ["ATS", "MTS", "STS"])
            dest_port = f"{node_id}_emerg" if is_emergency else (f"{node_id}_norm" if type_tag in ["ATS", "MTS", "STS"] else f"{node_id}_in")
            edge_color = "#B45309" if is_emergency else "#0F172A"
            edge_penwidth = "2.2" if is_emergency else "2.0"

            edge_key = (parent_id, dest_port)
            if edge_key in detailed_rendered_edges:
                continue
            detailed_rendered_edges.add(edge_key)

            # If parent is panel, connect from the corresponding breaker if defined, else from Load Out
            if parent_node.get("is_panel") or parent_domain == "panels":
                slot_num, poles, amps, side = _find_feeder_slot_in_parent(parent_node, n)
                if slot_num:
                    dot_lines.append(f'    {parent_id}_b{slot_num}:s -> {dest_port}:n [color="{edge_color}", penwidth={edge_penwidth}];')
                else:
                    dot_lines.append(f'    {parent_id}_out:s -> {dest_port}:n [color="{edge_color}", penwidth={edge_penwidth}];')
            else:
                dot_lines.append(f'    {parent_id}_out:s -> {dest_port}:n [color="{edge_color}", penwidth={edge_penwidth}];')

        # Fallback for standalone GEN to ATS emergency port
        if type_tag == "GEN":
            for candidate in nodes:
                if candidate.get("type_tag") in ["ATS", "MTS", "STS"] or candidate.get("domain") == "switches":
                    ats_id = _sanitize_id(candidate.get("id", candidate.get("tag", "ats")))
                    dest_port = f"{ats_id}_emerg"
                    edge_key = (node_id, dest_port)
                    if edge_key not in detailed_rendered_edges:
                        detailed_rendered_edges.add(edge_key)
                        dot_lines.append(f'    {node_id}_out:s -> {dest_port}:n [color="#B45309", penwidth=2.2];')
                        break

    dot_lines.append("}\n")
    return "\n".join(dot_lines)


def compile_project_to_dot(project: Project) -> str:
    """Compile a Project topology graph into Graphviz DOT syntax using record & port representation."""
    dot_lines = [
        "digraph SLD {",
        '    graph [rankdir=TB, splines=polyline, nodesep=0.75, ranksep=0.9, fontname="Arial", bgcolor="#CBD5E1"];',
        '    node [shape=record, fontname="Arial", fontsize=10, style="filled", penwidth=1.8];',
        '    edge [fontname="Arial", fontsize=9, color="#0F172A", fontcolor="#0F172A", penwidth=2.0, arrowsize=0.85];',
        ""
    ]

    # Map node_id -> set of ports referenced by edges
    node_ports: Dict[str, Set[str]] = {node_id: set() for node_id in project.nodes}
    for edge in project.edges:
        if edge.from_node in node_ports and edge.from_port:
            node_ports[edge.from_node].add(edge.from_port)
        if edge.to_node in node_ports and edge.to_port:
            node_ports[edge.to_node].add(edge.to_port)

    # Render Nodes
    for node_id, node in project.nodes.items():
        clean_id = _sanitize_id(node_id)
        d = node.data or {}

        # Subtitle specs
        parts = []
        if "bus_amps" in d:
            parts.append(f"{d['bus_amps']}A")
        elif "ampacity" in d:
            parts.append(f"{d['ampacity']}A")
        elif "kva" in d:
            parts.append(f"{d['kva']}kVA")

        if "primary_v" in d and "secondary_v" in d:
            parts.append(f"{d['primary_v']}V → {d['secondary_v']}V")
        elif "voltage" in d:
            parts.append(f"{d['voltage']}")
        specs = _clean_str(", ".join(parts))

        header_text = f"{node.label} ({specs})" if specs else (node.label or node_id)
        header_text = _clean_str(header_text)

        ports = sorted(list(node_ports[node_id]))
        port_parts = [f"<{p}> {p.upper()}" for p in ports] if ports else ["<in> In", "<out> Out"]
        ports_str = " | ".join(port_parts)

        # Determine domain palette for record node
        nid_lower = node_id.lower()
        if "util" in nid_lower or "gen" in nid_lower or "pv" in nid_lower:
            pal = DOMAIN_CONFIG["sources"]
        elif "xfmr" in nid_lower or "trans" in nid_lower or "pad" in nid_lower:
            pal = DOMAIN_CONFIG["transformers"]
        elif "ats" in nid_lower or "mts" in nid_lower or "disc" in nid_lower or "switch" in nid_lower:
            pal = DOMAIN_CONFIG["switches"]
        elif "ups" in nid_lower:
            pal = DOMAIN_CONFIG["power_quality"]
        elif "load" in nid_lower or "chiller" in nid_lower or "pump" in nid_lower or "motor" in nid_lower or "hvac" in nid_lower:
            pal = DOMAIN_CONFIG["loads"]
        elif "cable" in nid_lower or "feeder" in nid_lower:
            pal = DOMAIN_CONFIG["cables"]
        elif "meter" in nid_lower or "mtr" in nid_lower:
            pal = DOMAIN_CONFIG["metering"]
        elif "bess" in nid_lower or "solar" in nid_lower:
            pal = DOMAIN_CONFIG["renewables"]
        elif "swbd" in nid_lower or "msa" in nid_lower or "msb" in nid_lower or "pnl" in nid_lower or "panel" in nid_lower or "mcc" in nid_lower:
            pal = DOMAIN_CONFIG["panels"]
        else:
            pal = DOMAIN_CONFIG["generic"]

        color_attrs = f' fillcolor="{pal["bg"]}", color="{pal["border"]}", fontcolor="{pal["text"]}"'
        label = f"{{ {header_text} | {{ {ports_str} }} }}"
        dot_lines.append(f'    {clean_id} [label="{label}",{color_attrs}];')

    dot_lines.append("")

    # Render Edges
    for edge in project.edges:
        from_id = _sanitize_id(edge.from_node)
        to_id = _sanitize_id(edge.to_node)
        from_spec = f"{from_id}:{_sanitize_id(edge.from_port)}" if edge.from_port else from_id
        to_spec = f"{to_id}:{_sanitize_id(edge.to_port)}" if edge.to_port else to_id

        edge_label_parts = []
        if "breaker" in edge.data:
            edge_label_parts.append(str(edge.data["breaker"]))
        if "fuse" in edge.data:
            edge_label_parts.append(str(edge.data["fuse"]))
        if "cable" in edge.data:
            edge_label_parts.append(str(edge.data["cable"]))
        if "length_ft" in edge.data:
            edge_label_parts.append(f"{edge.data['length_ft']} ft")

        label_attr = ""
        if edge_label_parts:
            label_str = " • ".join(edge_label_parts)
            badge = _make_silver_badge(label_str, font_size=8, font_color="#0F172A", bg_color="#E2E8F0", border_color="#94A3B8")
            label_attr = f' [label={badge}]'

        dot_lines.append(f"    {from_spec} -> {to_spec}{label_attr};")

    dot_lines.append("}\n")
    return "\n".join(dot_lines)
