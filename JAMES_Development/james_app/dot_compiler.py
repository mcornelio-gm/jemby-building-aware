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
        line2_parts.append(f"{slots}-Slot ({main_abbr})")
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
        for n in nodes:
            node_id = _sanitize_id(n.get("id", n.get("tag", "eq")))
            fed_from = n.get("fed_from")
            type_tag = n.get("type_tag", "")
            child_domain = n.get("domain", "")

            if fed_from:
                parent_node = nodes_by_tag.get(fed_from)
                if parent_node:
                    parent_id = _sanitize_id(parent_node.get("id", parent_node.get("tag", "eq")))
                    parent_domain = parent_node.get("domain", "")
                    parent_type = parent_node.get("type_tag", "")

                    # 1. Determine Tail Label (Upstream Breaker / Output Port)
                    tail_parts = []
                    if parent_node.get("is_panel") or parent_domain == "panels":
                        schedule = (parent_node.get("attributes") or {}).get("schedule", [])
                        matched_slot = None
                        if schedule and isinstance(schedule, list):
                            for row in schedule:
                                if row.get("leftTargetLoad") == n.get("tag"):
                                    slot_num = int(row.get("leftSlot", 1))
                                    poles = int(row.get("leftPoles", 1))
                                    amps = row.get("leftAmps", "")
                                    poles_str = f"/{poles}P" if poles > 1 else ""
                                    if parent_type == "MCC":
                                        slot_str = f"Bucket {slot_num}A"
                                    elif poles == 1:
                                        slot_str = f"Slot {slot_num}"
                                    elif poles == 2:
                                        slot_str = f"Slots {slot_num},{slot_num + 2}"
                                    else:
                                        slot_str = f"Slots {slot_num}-{slot_num + 4}"
                                    matched_slot = f"[{slot_str}] {amps}A{poles_str}" if amps else f"[{slot_str}]"
                                    break
                                elif row.get("rightTargetLoad") == n.get("tag"):
                                    slot_num = int(row.get("rightSlot", 2))
                                    poles = int(row.get("rightPoles", 1))
                                    amps = row.get("rightAmps", "")
                                    poles_str = f"/{poles}P" if poles > 1 else ""
                                    if parent_type == "MCC":
                                        slot_str = f"Bucket {slot_num}B"
                                    elif poles == 1:
                                        slot_str = f"Slot {slot_num}"
                                    elif poles == 2:
                                        slot_str = f"Slots {slot_num},{slot_num + 2}"
                                    else:
                                        slot_str = f"Slots {slot_num}-{slot_num + 4}"
                                    matched_slot = f"[{slot_str}] {amps}A{poles_str}" if amps else f"[{slot_str}]"
                                    break
                        tail_parts.append(matched_slot if matched_slot else "Feeder Out")
                    elif parent_domain == "transformers" or parent_type in ["XFMR", "PAD"]:
                        tail_parts.append("Sec Out")
                    elif parent_domain == "sources" or parent_type in ["UTIL", "GEN", "PV"]:
                        tail_parts.append("Main Out")
                    elif parent_domain == "switches" or parent_type in ["ATS", "MTS", "DISC"]:
                        tail_parts.append("Load Out")
                    else:
                        tail_parts.append("Out")

                    tail_label = _clean_str(" • ".join(tail_parts))

                    # 2. Determine Head Label (Downstream Input Terminal)
                    head_parts = []
                    if type_tag in ["ATS", "MTS"]:
                        head_parts.append("Norm In")
                    elif type_tag in ["XFMR", "PAD"]:
                        head_parts.append("Pri In")
                    elif n.get("is_panel") or child_domain == "panels":
                        main_type = (n.get("attributes") or {}).get("main_type", "")
                        head_parts.append(f"Mains ({main_type})" if main_type else "Line In")
                    elif child_domain == "loads":
                        head_parts.append("Load In")
                    else:
                        head_parts.append("Line In")

                    head_label = _clean_str(" • ".join(head_parts))

                    # 3. Conductor Wire Label (Center)
                    conductor = (n.get("attributes") or {}).get("conductor") or n.get("conductor")
                    cond_attr = f'label="{_clean_str(conductor)}", ' if conductor else ''

                    dot_lines.append(
                        f'    {parent_id} -> {node_id} ['
                        f'color="#0F172A", penwidth=2.0, {cond_attr}'
                        f'taillabel="{tail_label}", headlabel="{head_label}", '
                        f'labeldistance=2.4, labelangle=25, fontsize=8, fontname="Arial", fontcolor="#334155"];'
                    )

            # Special connection: Emergency Generator to ATS
            if type_tag == "GEN":
                for candidate in nodes:
                    if candidate.get("type_tag") == "ATS" or candidate.get("domain") == "switches":
                        ats_id = _sanitize_id(candidate.get("id", candidate.get("tag", "ats")))
                        dot_lines.append(
                            f'    {node_id} -> {ats_id} ['
                            f'color="#B45309", penwidth=2.2, '
                            f'taillabel="Gen Out", headlabel="Emerg In", '
                            f'labeldistance=2.4, labelangle=-25, fontsize=8, fontname="Arial", fontcolor="#9A3412"];'
                        )

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
            main_type = (n.get("attributes") or {}).get("main_type", "Main Lugs")
            schedule = (n.get("attributes") or {}).get("schedule", [])
            
            breaker_nodes = []
            breaker_ids = []
            if schedule and isinstance(schedule, list):
                for row in schedule:
                    if row.get("leftTrip") and str(row.get("leftTrip")).strip():
                        s_num = row.get("leftSlot")
                        desc = _clean_str(row.get("leftDesc") or row.get("leftTargetLoad") or f"Circuit {s_num}")
                        trip = _clean_str(row.get("leftTrip"))
                        b_id = f"{node_id}_b{s_num}"
                        breaker_ids.append(b_id)
                        breaker_nodes.append(f'        {b_id} [label="[ Slot {s_num} ]\\n{desc}\\n{trip}A", {PORT_STYLE}];')
                    if row.get("rightTrip") and str(row.get("rightTrip")).strip():
                        s_num = row.get("rightSlot")
                        desc = _clean_str(row.get("rightDesc") or row.get("rightTargetLoad") or f"Circuit {s_num}")
                        trip = _clean_str(row.get("rightTrip"))
                        b_id = f"{node_id}_b{s_num}"
                        breaker_ids.append(b_id)
                        breaker_nodes.append(f'        {b_id} [label="[ Slot {s_num} ]\\n{desc}\\n{trip}A", {PORT_STYLE}];')

            if not breaker_ids:
                for idx in [1, 2, 3, 4]:
                    b_id = f"{node_id}_b{idx}"
                    breaker_ids.append(b_id)
                    breaker_nodes.append(f'        {b_id} [label="[ Slot {idx} ]\\nCircuit {idx}\\n20A", {PORT_STYLE}];')

            rank_same = " ".join(breaker_ids[:8])

            dot_lines.extend([
                f'    subgraph cluster_{node_id} {{',
                f'        label = "{cluster_title}";',
                '        style = "filled,rounded";',
                f'        color = "{palette["border"]}";',
                f'        fillcolor = "{palette["bg"]}";',
                f'        fontcolor = "{palette["text"]}";',
                '        penwidth = 1.8;',
                f'        {node_id}_in [label="{main_type}", {PORT_STYLE}];',
                *breaker_nodes[:10],
                f'        {{ rank=same; {rank_same}; }}',
                f'        {node_id}_in -> {breaker_ids[0]} [style=invis];',
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
    for n in nodes:
        node_id = _sanitize_id(n.get("id", n.get("tag", "eq")))
        fed_from = n.get("fed_from")
        type_tag = n.get("type_tag", "")

        if fed_from:
            parent_node = nodes_by_tag.get(fed_from)
            if parent_node:
                parent_id = _sanitize_id(parent_node.get("id", parent_node.get("tag", "eq")))
                parent_domain = parent_node.get("domain", "")
                parent_type = parent_node.get("type_tag", "")
                dest_port = f"{node_id}_norm" if type_tag in ["ATS", "MTS"] else f"{node_id}_in"

                # If parent is panel, connect from the corresponding breaker
                if parent_node.get("is_panel") or parent_domain == "panels":
                    schedule = (parent_node.get("attributes") or {}).get("schedule", [])
                    slot_port = "1"
                    if schedule and isinstance(schedule, list):
                        for row in schedule:
                            if row.get("leftTargetLoad") == n.get("tag"):
                                slot_port = str(row.get("leftSlot", "1"))
                                break
                            elif row.get("rightTargetLoad") == n.get("tag"):
                                slot_port = str(row.get("rightSlot", "2"))
                                break
                    dot_lines.append(f'    {parent_id}_b{slot_port}:s -> {dest_port}:n [color="#0F172A", penwidth=2.0];')
                else:
                    dot_lines.append(f'    {parent_id}_out:s -> {dest_port}:n [color="#0F172A", penwidth=2.0];')

        # Special connection: Emergency Generator to ATS emergency port
        if type_tag == "GEN":
            for candidate in nodes:
                if candidate.get("type_tag") == "ATS" or candidate.get("domain") == "switches":
                    ats_id = _sanitize_id(candidate.get("id", candidate.get("tag", "ats")))
                    dot_lines.append(f'    {node_id}_out:s -> {ats_id}_emerg:n [color="#B45309", penwidth=2.2];')
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
            label_str = " | ".join(edge_label_parts)
            label_attr = f' [label="{_clean_str(label_str)}"]'

        dot_lines.append(f"    {from_spec} -> {to_spec}{label_attr};")

    dot_lines.append("}\n")
    return "\n".join(dot_lines)
