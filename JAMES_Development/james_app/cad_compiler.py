"""
Build Aware CAD Single-Line Diagram (SLD) Compiler Engine
Generates IEEE 315 / ANSI Y32.2 compliant AutoCAD DXF files and vector SVG previews
strictly locked to standard ANSI D (24" x 36" / 864mm x 558mm) sheet framing.
"""

from typing import Any, Dict, List, Optional, Tuple, Set
from collections import defaultdict, deque
import io
import ezdxf
from ezdxf.document import Drawing
from ezdxf.enums import TextEntityAlignment
from ezdxf.addons.drawing import Frontend, RenderContext, layout
from ezdxf.addons.drawing.svg import SVGBackend

from james_app.cad_symbols import register_all_cad_symbols
from james_app.core.feeder_calculator import suggest_feeder_conductors

# Strict Industry Standard ANSI D Paper Dimensions (in millimeters)
ANSI_D_WIDTH = 864.0   # 36 inches
ANSI_D_HEIGHT = 558.0  # 24 inches


def _format_feeder_callout(trip_str: Any) -> str:
    """Format conductor and conduit callout text for CAD drawing."""
    clean_num = ''.join(c for c in str(trip_str) if c.isdigit() or c == '.')
    val = float(clean_num) if clean_num else 100.0
    try:
        rec = suggest_feeder_conductors(val)
        gauge = rec.get("gauge") or rec.get("conductor_size") or "3/0 AWG"
        egc = rec.get("egc") or rec.get("egc_recommended") or "#6"
        conduit = rec.get("conduit") or "2\""
        sets = rec.get("sets") or 1
        prefix = f"({sets}) " if sets > 1 else ""
        return f"{prefix}3#{gauge} CU, 1#{egc} GND, {conduit} C"
    except Exception:
        return "3#3/0 CU, 1#6 GND, 2\" C"


def _infer_symbol_name(type_tag: str, domain: str) -> str:
    """Map electrical equipment type tag or domain to standard IEEE CAD block name."""
    t = (type_tag or "").upper()
    d = (domain or "").lower()

    if "UTIL" in t or "GRID" in t or (d == "sources" and "UTIL" in t):
        return "SYM_UTILITY_SOURCE"
    if "GEN" in t or "EMERG" in t:
        return "SYM_GENERATOR"
    if "SOLAR" in t or "PV" in t:
        return "SYM_SOLAR_PV"
    if "BESS" in t or "BATT" in t:
        return "SYM_BESS"
    if "XFRM" in t or "XFMR" in t or d == "transformers":
        return "SYM_TRANSFORMER_2W"
    if "ATS" in t or "TRANSFER" in t:
        return "SYM_ATS"
    if "FUSED" in t or "DISC" in t or "SAFETY" in t:
        return "SYM_FUSED_DISCONNECT"
    if "DRAWOUT" in t or "PCB" in t or "SWG" in t:
        return "SYM_CB_DRAWOUT"
    if "CB" in t or "BREAKER" in t or "MCCB" in t:
        return "SYM_CB_MOLDED_CASE"
    if any(m in t for m in ["MOTOR", "PUMP", "CHILLER", "CHLR", "FAN", "AHU", "ELEV", "HVAC", "MTR", "FP"]):
        return "SYM_MOTOR_LOAD"
    if "METER" in t or d == "metering":
        return "SYM_POWER_METER"
    if "SPD" in t or "TVSS" in t or d == "power_quality":
        return "SYM_SPD"
    if d == "loads":
        return "SYM_MOTOR_LOAD"
    return "SYM_CB_MOLDED_CASE"


def get_available_facility_sheets(nodes: List[Dict[str, Any]], edges: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    """Determine drawing sheet partition structure based on facility electrical topology."""
    node_map = {str(n.get("tag") or n.get("id")): n for n in nodes}
    children = defaultdict(list)
    parents = defaultdict(list)

    for e in edges:
        s = str(e.get("source") or e.get("from_node_tag") or "")
        t = str(e.get("target") or e.get("to_node_tag") or "")
        if s in node_map and t in node_map and s != t:
            if t not in children[s]: children[s].append(t)
            if s not in parents[t]: parents[t].append(s)

    for n in nodes:
        tag = str(n.get("tag") or n.get("id") or "")
        ff = str(n.get("fed_from") or "")
        if ff and ff in node_map and ff != tag and ff not in ("-- None / Service Entrance --", "None", "null", ""):
            if tag not in children[ff]: children[ff].append(tag)
            if ff not in parents[tag]: parents[tag].append(ff)

    sheets = [
        {"sheet_id": "all", "sheet_no": "E-001", "title": "Overall Single-Line Diagram (Full Plant)"}
    ]

    sub_hubs = []
    for tag, ch_list in children.items():
        node = node_map.get(tag, {})
        dom = (node.get("domain") or "").lower()
        if len(ch_list) >= 3 or any(k in tag for k in ["BUS", "UPS", "DP", "MCC", "RISER"]):
            if dom not in ("sources",) and tag not in ("ATS-1",):
                sub_hubs.append(tag)

    if len(nodes) > 15 and sub_hubs:
        sheets.append({
            "sheet_id": "E-101",
            "sheet_no": "E-101",
            "title": "Primary Service & Main Distribution"
        })

        sheet_idx = 102
        for hub in sub_hubs:
            tag_u = hub.upper()
            if "BUS" in tag_u or "RISER" in tag_u:
                stitle = f"480V Riser & Floor Distribution ({hub})"
            elif "UPS" in tag_u or "BESS" in tag_u:
                stitle = f"Emergency, UPS & Critical Power ({hub})"
            elif "DP" in tag_u or "ROOF" in tag_u or "AHU" in tag_u or "MECH" in tag_u:
                stitle = f"Mechanical & Rooftop Distribution ({hub})"
            else:
                stitle = f"Sub-Distribution & Panelboards ({hub})"

            sheets.append({
                "sheet_id": f"E-{sheet_idx}",
                "sheet_no": f"E-{sheet_idx}",
                "title": stitle,
                "hub_tag": hub
            })
            sheet_idx += 1

    return sheets


class SingleLineCadCompiler:
    """
    Deterministic Hierarchical CAD Single-Line Diagram Compiler.
    Strictly standardizes all drawings to ANSI D (24" x 36" / 864mm x 558mm) sheet format.
    Automatically calculates proportional scaling and centering for clean, un-occluded plotting.
    """

    def __init__(
        self,
        nodes: Any,
        edges: Any,
        client_id: str = "Client",
        facility_id: str = "Facility",
        facility_title: Optional[str] = None,
        sheet_id: str = "all"
    ):
        self.client_id = client_id.upper()
        self.facility_id = facility_id.upper()
        self.facility_title = facility_title or f"{self.client_id} / {self.facility_id}"
        self.sheet_id = sheet_id or "all"

        # Normalize nodes input
        self.raw_nodes: List[Dict[str, Any]] = []
        if isinstance(nodes, dict):
            for k, v in nodes.items():
                if isinstance(v, dict):
                    node_copy = dict(v)
                    node_copy.setdefault("id", k)
                    node_copy.setdefault("tag", v.get("label") or k)
                    if "data" in v and isinstance(v["data"], dict):
                        for dk, dv in v["data"].items():
                            node_copy.setdefault(dk, dv)
                    self.raw_nodes.append(node_copy)
        elif isinstance(nodes, list):
            for item in nodes:
                if isinstance(item, dict):
                    node_copy = dict(item)
                    if "data" in item and isinstance(item["data"], dict):
                        for dk, dv in item["data"].items():
                            node_copy.setdefault(dk, dv)
                    self.raw_nodes.append(node_copy)

        # Normalize edges input
        self.raw_edges: List[Dict[str, Any]] = []
        if isinstance(edges, dict):
            for k, v in edges.items():
                if isinstance(v, dict):
                    self.raw_edges.append(dict(v))
        elif isinstance(edges, list):
            for item in edges:
                if isinstance(item, dict):
                    self.raw_edges.append(dict(item))

        # Partition graph for selected sheet
        self.sheet_title = "ELECTRICAL SINGLE-LINE DIAGRAM (SLD)"
        self.sheet_no = "E-001"
        self._partition_graph_for_sheet()

        # Initialize DXF Document (AutoCAD R2018 format)
        self.doc: Drawing = ezdxf.new("R2018")
        self.msp = self.doc.modelspace()
        
        # Setup Standard CAD Layers & Blocks
        self._setup_layers()
        register_all_cad_symbols(self.doc)

        self.rel_coords: Dict[str, Tuple[float, float]] = {}
        self.node_coords: Dict[str, Tuple[float, float]] = {}
        self.node_widths: Dict[str, float] = {}
        self.draw_scale = 1.0

    def _partition_graph_for_sheet(self) -> None:
        """Filter and prepare nodes and edges based on the requested sheet mode."""
        available_sheets = get_available_facility_sheets(self.raw_nodes, self.raw_edges)
        sheet_info = next((s for s in available_sheets if s["sheet_id"] == self.sheet_id), None)
        if sheet_info:
            self.sheet_no = sheet_info["sheet_no"]
            self.sheet_title = sheet_info["title"].upper()
        else:
            self.sheet_no = "E-001"
            self.sheet_title = "ELECTRICAL SINGLE-LINE DIAGRAM (SLD)"

        node_map = {str(n.get("tag") or n.get("id")): n for n in self.raw_nodes}
        children_map = defaultdict(list)
        parent_map = defaultdict(list)

        for e in self.raw_edges:
            s = str(e.get("source") or e.get("from_node_tag") or "")
            t = str(e.get("target") or e.get("to_node_tag") or "")
            if s in node_map and t in node_map and s != t:
                if t not in children_map[s]: children_map[s].append(t)
                if s not in parent_map[t]: parent_map[t].append(s)

        for n in self.raw_nodes:
            tag = str(n.get("tag") or n.get("id") or "")
            ff = str(n.get("fed_from") or "")
            if ff and ff in node_map and ff != tag and ff not in ("-- None / Service Entrance --", "None", "null", ""):
                if tag not in children_map[ff]: children_map[ff].append(tag)
                if ff not in parent_map[tag]: parent_map[tag].append(ff)

        hub_to_sheet = {s["hub_tag"]: s["sheet_no"] for s in available_sheets if "hub_tag" in s}

        if self.sheet_id == "all" or not available_sheets or len(available_sheets) <= 1:
            self.nodes = self.raw_nodes
            self.edges = self.raw_edges
            self.offpage_refs: Dict[str, str] = {}
            self.incoming_stub: Optional[str] = None
        elif self.sheet_id == "E-101":
            self.offpage_refs = {}
            self.incoming_stub = None
            active_tags = set()
            roots = [t for t in node_map if not parent_map[t]]
            q = deque(roots)
            while q:
                curr = q.popleft()
                active_tags.add(curr)
                for ch in children_map[curr]:
                    if ch in hub_to_sheet:
                        active_tags.add(ch)
                        self.offpage_refs[ch] = f"TO {ch} (SEE DWG {hub_to_sheet[ch]})"
                    elif curr not in hub_to_sheet:
                        active_tags.add(ch)
                        q.append(ch)

            self.nodes = [n for n in self.raw_nodes if str(n.get("tag") or n.get("id")) in active_tags]
            self.edges = [e for e in self.raw_edges if str(e.get("source") or e.get("from_node_tag")) in active_tags and str(e.get("target") or e.get("to_node_tag")) in active_tags]
        else:
            hub_tag = sheet_info.get("hub_tag") if sheet_info else None
            self.offpage_refs = {}
            active_tags = set()

            if hub_tag and hub_tag in node_map:
                parent_tag = parent_map[hub_tag][0] if parent_map[hub_tag] else "MAIN DISTRIBUTION"
                self.incoming_stub = f"FROM {parent_tag} (SEE DWG E-101)"
                q = deque([hub_tag])
                while q:
                    curr = q.popleft()
                    active_tags.add(curr)
                    for ch in children_map[curr]:
                        active_tags.add(ch)
                        q.append(ch)
            else:
                active_tags = {str(n.get("tag") or n.get("id")) for n in self.raw_nodes}

            self.nodes = [n for n in self.raw_nodes if str(n.get("tag") or n.get("id")) in active_tags]
            self.edges = [e for e in self.raw_edges if str(e.get("source") or e.get("from_node_tag")) in active_tags and str(e.get("target") or e.get("to_node_tag")) in active_tags]

        self.node_map = {str(n.get("tag") or n.get("id")): n for n in self.nodes}
        self.children = defaultdict(list)
        self.parents = defaultdict(list)
        self.edge_specs = {}

        for e in self.edges:
            s = str(e.get("source") or e.get("from_node_tag") or "")
            t = str(e.get("target") or e.get("to_node_tag") or "")
            if s in self.node_map and t in self.node_map and s != t:
                if s not in self.offpage_refs:
                    if t not in self.children[s]: self.children[s].append(t)
                    if s not in self.parents[t]: self.parents[t].append(s)
                    self.edge_specs[(s, t)] = e

        for n in self.nodes:
            tag = str(n.get("tag") or n.get("id") or "")
            ff = str(n.get("fed_from") or "")
            if ff and ff in self.node_map and ff != tag and ff not in ("-- None / Service Entrance --", "None", "null", ""):
                if ff not in self.offpage_refs:
                    if tag not in self.children[ff]: self.children[ff].append(tag)
                    if ff not in self.parents[tag]: self.parents[tag].append(ff)
                    if (ff, tag) not in self.edge_specs:
                        self.edge_specs[(ff, tag)] = {"source": ff, "target": tag}

    def _setup_layers(self) -> None:
        """Create standard AIA / NCS CAD layers with standardized colors and lineweights."""
        layer_defs = [
            ("E-ELEC-BUS", 4, 70, "Main Switchgear & Panel Power Buses"),         # Cyan (0.70mm)
            ("E-ELEC-FEED", 7, 35, "Feeder Conductors, Cable Runs & Drops"),      # White (0.35mm)
            ("E-ELEC-SYMB", 2, 35, "IEEE Standard Electrical Equipment Symbols"), # Yellow (0.35mm)
            ("E-ANNO-TEXT", 3, 25, "Equipment Ratings, Tags & kVA Annotation"),   # Green (0.25mm)
            ("E-ANNO-CABL", 1, 18, "Conductor & Conduit Size Schedules"),         # Red (0.18mm)
            ("E-TTLB", 7, 50, "Title Block & Border Framing")                     # White (0.50mm)
        ]
        for name, color, weight, desc in layer_defs:
            if name not in self.doc.layers:
                layer = self.doc.layers.add(name, color=color, lineweight=weight)
                layer.description = desc

    def _is_leaf_panel(self, tag: str) -> bool:
        """Check if node is a panelboard/switchboard whose children are all terminal branch loads."""
        ch_list = self.children.get(tag, [])
        return len(ch_list) >= 3 and all(len(self.children.get(c, [])) == 0 for c in ch_list)

    def _compute_widths(self, node_tag: str, visited: Set[str]) -> float:
        """Recursively calculate horizontal bounding width required for each equipment branch."""
        if node_tag in visited:
            return 32.0
        visited.add(node_tag)

        if node_tag in self.offpage_refs:
            self.node_widths[node_tag] = 36.0
            return 36.0

        ch_list = self.children.get(node_tag, [])
        if not ch_list:
            w = 32.0
            self.node_widths[node_tag] = w
            return w

        # 2-Tier Alternating Drops for Branch Panels: halve horizontal pitch while utilizing vertical space
        if self._is_leaf_panel(node_tag):
            pitch = 16.0
            w = max(40.0, (len(ch_list) - 1) * pitch + 28.0)
            self.node_widths[node_tag] = w
            return w

        total_ch_w = sum(self._compute_widths(c, visited) for c in ch_list) + (len(ch_list) - 1) * 12.0
        min_bus_w = max(40.0, len(ch_list) * 26.0)
        w = max(total_ch_w, min_bus_w)
        self.node_widths[node_tag] = w
        return w

    def _position_subtree_relative(self, tag: str, x: float, y: float, y_step: float, tier_offset: float, visited: Set[str]) -> None:
        """Position nodes relative to root (0, 0) downward using 2D adaptive staggering."""
        if tag in visited:
            return
        visited.add(tag)
        self.rel_coords[tag] = (x, y)

        if tag in self.offpage_refs:
            return

        ch_list = self.children.get(tag, [])
        if not ch_list:
            return

        # 2-Tier Alternating Drops for Branch Panels (Odd / Even Staggering)
        if self._is_leaf_panel(tag):
            pitch = 16.0
            total_w = (len(ch_list) - 1) * pitch
            start_x = x - (total_w / 2.0)
            for idx, c in enumerate(ch_list):
                cx = start_x + idx * pitch
                # Even indices at Tier 1, Odd indices at Tier 2
                is_staggered = (idx % 2 == 1)
                cy = y - (y_step + (tier_offset if is_staggered else 0.0))
                self.rel_coords[c] = (cx, cy)
                visited.add(c)
            return

        total_w = sum(self.node_widths.get(c, 32.0) for c in ch_list) + (len(ch_list) - 1) * 12.0
        ch_start_x = x - (total_w / 2.0)
        next_y = y - y_step

        for c in ch_list:
            cw = self.node_widths.get(c, 32.0)
            cx = ch_start_x + (cw / 2.0)
            self._position_subtree_relative(c, cx, next_y, y_step, tier_offset, visited)
            ch_start_x += cw + 12.0

    def build_cad_drawing(self) -> Drawing:
        """
        Executes 2D full-page auto-layout strictly formatted to ANSI D (24" x 36" / 864mm x 558mm).
        Calculates proportional scaling and vertical step expansion to guarantee full-page utilization.
        """
        roots = [
            str(n.get("tag") or n.get("id"))
            for n in self.nodes
            if not self.parents[str(n.get("tag") or n.get("id"))]
        ]
        if not roots and self.nodes:
            roots = [str(self.nodes[0].get("tag") or self.nodes[0].get("id"))]

        visited_w: Set[str] = set()
        for r in roots:
            self._compute_widths(r, visited_w)

        # Dynamic Tree Depth & Vertical Step Calculation to fill entire 24" sheet height
        def get_max_depth(t: str, seen: Set[str]) -> int:
            if t in seen: return 0
            seen.add(t)
            ch = self.children.get(t, [])
            if not ch: return 1
            return 1 + max(get_max_depth(c, set(seen)) for c in ch)

        max_depth = max((get_max_depth(r, set()) for r in roots), default=3)
        if max_depth <= 2:
            y_step = 130.0
            tier_offset = 45.0
        elif max_depth == 3:
            y_step = 100.0
            tier_offset = 40.0
        elif max_depth == 4:
            y_step = 85.0
            tier_offset = 38.0
        else:
            y_step = max(65.0, 360.0 / (max_depth + 1.2))
            tier_offset = min(36.0, y_step * 0.45)

        self.y_step = y_step
        self.tier_offset = tier_offset

        # Pass 1: Compute Relative Coordinates
        cur_x = 0.0
        visited_p: Set[str] = set()
        for r in roots:
            rw = self.node_widths.get(r, 40.0)
            rx = cur_x + (rw / 2.0)
            ry = 0.0
            self._position_subtree_relative(r, rx, ry, y_step, tier_offset, visited_p)
            cur_x += rw + 35.0

        for n in self.nodes:
            tag = str(n.get("tag") or n.get("id"))
            if tag not in self.rel_coords:
                self.rel_coords[tag] = (cur_x + 20.0, 0.0)
                cur_x += 40.0

        # Calculate Bounding Box of relative geometry
        min_x = min(c[0] for c in self.rel_coords.values()) if self.rel_coords else 0.0
        max_x = max(c[0] for c in self.rel_coords.values()) if self.rel_coords else 700.0
        min_y = min(c[1] for c in self.rel_coords.values()) if self.rel_coords else -350.0
        max_y = max(c[1] for c in self.rel_coords.values()) if self.rel_coords else 0.0

        for tag, ch_list in self.children.items():
            if ch_list and tag in self.rel_coords:
                ch_xs = [self.rel_coords[c][0] for c in ch_list if c in self.rel_coords]
                if ch_xs:
                    min_x = min(min_x, min(ch_xs) - 18.0)
                    max_x = max(max_x, max(ch_xs) + 18.0)

        if self.incoming_stub:
            max_y += 35.0

        content_w = max(10.0, max_x - min_x)
        content_h = max(10.0, max_y - min_y)

        # ANSI D Printable Area Bounds (in mm)
        margin_x = 40.0
        margin_top = 48.0
        margin_bottom = 80.0
        avail_w = ANSI_D_WIDTH - (margin_x * 2.0)         # 784.0 mm
        avail_h = ANSI_D_HEIGHT - margin_top - margin_bottom # 430.0 mm

        # Auto-fit scale factor to guarantee ANSI D sheet containment while maximizing full-page utilization
        if content_w > avail_w or content_h > avail_h:
            self.draw_scale = min(avail_w / content_w, avail_h / content_h) * 0.96
        else:
            self.draw_scale = 1.0

        # Center horizontally and vertically within ANSI D drawing canvas
        scaled_w = content_w * self.draw_scale
        scaled_h = content_h * self.draw_scale
        start_x = margin_x + (avail_w - scaled_w) / 2.0
        start_y = (ANSI_D_HEIGHT - margin_top) - ((avail_h - scaled_h) / 4.0)

        shift_x = start_x - (min_x * self.draw_scale)
        shift_y = start_y - (max_y * self.draw_scale)

        self.node_coords = {
            tag: (rx * self.draw_scale + shift_x, ry * self.draw_scale + shift_y)
            for tag, (rx, ry) in self.rel_coords.items()
        }

        # Render AutoCAD entities
        self._render_elements()

        # Draw Strict ANSI D Sheet Border & Engineering Title Block (24" x 36")
        self._draw_title_block(sheet_w=ANSI_D_WIDTH, sheet_h=ANSI_D_HEIGHT)

        return self.doc

    def _render_elements(self) -> None:
        """Render AutoCAD entities: buses, breaker drops, equipment blocks, and annotations."""
        s = self.draw_scale

        if self.incoming_stub and self.node_coords:
            roots = [t for t in self.node_coords if not self.parents[t]]
            if roots:
                rx, ry = self.node_coords[roots[0]]
                stub_len = 25.0 * s
                self.msp.add_line((rx, ry + stub_len), (rx, ry), dxfattribs={"layer": "E-ELEC-FEED"})
                self.msp.add_blockref("SYM_OFFPAGE_REF", (rx, ry + stub_len), dxfattribs={"layer": "E-ANNO-CABL", "rotation": 180, "xscale": s, "yscale": s})
                self.msp.add_text(
                    self.incoming_stub,
                    dxfattribs={"layer": "E-ANNO-TEXT", "height": max(2.2, 2.8 * s)}
                ).set_placement((rx + 8.0 * s, ry + 20.0 * s), align=TextEntityAlignment.LEFT)

        for tag, pos in self.node_coords.items():
            node = self.node_map.get(tag, {})
            nx, ny = pos
            dom = (node.get("domain") or "").lower()
            ttag = (node.get("type_tag") or "").upper()
            sym = _infer_symbol_name(ttag, dom)
            ch_list = self.children.get(tag, [])

            # -------------------------------------------------------------
            # Case 1: Off-Page Reference Continuation Stub
            # -------------------------------------------------------------
            if tag in self.offpage_refs:
                self.msp.add_blockref("SYM_OFFPAGE_REF", (nx, ny), dxfattribs={"layer": "E-ANNO-CABL", "xscale": s, "yscale": s})
                ref_txt = self.offpage_refs[tag]
                self.msp.add_text(
                    ref_txt,
                    dxfattribs={"layer": "E-ANNO-TEXT", "height": max(1.8, 2.4 * s)}
                ).set_placement((nx + 6.0 * s, ny - 3.0 * s), align=TextEntityAlignment.LEFT)
                continue

            # -------------------------------------------------------------
            # Case 2: Bus / Switchboard / Panelboard with Children
            # -------------------------------------------------------------
            if ch_list and (dom in ("panels", "sources", "cables", "switches") or any(
                k in tag for k in ["BUS", "SWG", "MSB", "MDP", "DP", "LP", "RP", "CP", "ATS", "UPS", "MCC"]
            )):
                ch_xs = [self.node_coords[c][0] for c in ch_list if c in self.node_coords]
                if ch_xs:
                    bus_left = min(ch_xs) - 8.0 * s
                    bus_right = max(ch_xs) + 8.0 * s
                else:
                    bus_left = nx - 16.0 * s
                    bus_right = nx + 16.0 * s

                self.msp.add_line((bus_left, ny), (bus_right, ny), dxfattribs={"layer": "E-ELEC-BUS"})
                self.msp.add_line((bus_left, ny - 0.5 * s), (bus_right, ny - 0.5 * s), dxfattribs={"layer": "E-ELEC-BUS"})

                amps = node.get("amps") or ""
                volts = node.get("voltage") or ""
                spec_str = f" • {amps}" if amps else ""
                if volts: spec_str += f" • {volts}"
                self.msp.add_text(
                    f"{tag}{spec_str}",
                    dxfattribs={"layer": "E-ANNO-TEXT", "height": max(2.2, 2.8 * s)}
                ).set_placement((bus_left, ny + 3.0 * s), align=TextEntityAlignment.BOTTOM_LEFT)

                is_leaf_panel = self._is_leaf_panel(tag)

                for idx, c in enumerate(ch_list):
                    if c not in self.node_coords:
                        continue
                    cx, cy = self.node_coords[c]
                    edge = self.edge_specs.get((tag, c), {})
                    trip_amps = edge.get("trip_amps") or "100A"

                    # 1. Bus Junction Dot
                    self.msp.add_blockref("SYM_JUNCTION_DOT", (cx, ny), dxfattribs={"layer": "E-ELEC-BUS", "xscale": s, "yscale": s})

                    # 2. Feeder Breaker on Drop (Staggered for 2-tier branch panels)
                    is_staggered = is_leaf_panel and (idx % 2 == 1)
                    if is_leaf_panel:
                        brk_y = cy + (22.0 * s)
                    else:
                        brk_y = ny - 9.0 * s

                    self.msp.add_line((cx, ny), (cx, brk_y + 3.0 * s), dxfattribs={"layer": "E-ELEC-FEED"})
                    self.msp.add_blockref("SYM_CB_MOLDED_CASE", (cx, brk_y), dxfattribs={"layer": "E-ELEC-SYMB", "xscale": s, "yscale": s})
                    self.msp.add_text(
                        f"{trip_amps}/3P",
                        dxfattribs={"layer": "E-ANNO-TEXT", "height": max(1.5, 1.8 * s)}
                    ).set_placement((cx + 2.5 * s, brk_y), align=TextEntityAlignment.LEFT)

                    # 3. Drop Line down to child incomer
                    target_node = self.node_map.get(c, {})
                    target_dom = (target_node.get("domain") or "").lower()
                    target_ttag = (target_node.get("type_tag") or "").upper()

                    if c in self.offpage_refs:
                        child_top_y = cy + 4.0 * s
                    elif target_dom == "transformers" or "XFMR" in target_ttag:
                        child_top_y = cy + 10.0 * s
                    elif self.children.get(c):
                        child_top_y = cy
                    else:
                        child_top_y = cy + 6.0 * s

                    self.msp.add_line((cx, brk_y - 3.0 * s), (cx, child_top_y), dxfattribs={"layer": "E-ELEC-FEED"})

                    # Feeder Cable Callout
                    cabl_callout = edge.get("conductor_size") or _format_feeder_callout(trip_amps)
                    self.msp.add_text(
                        cabl_callout,
                        dxfattribs={"layer": "E-ANNO-CABL", "height": max(1.3, 1.5 * s), "rotation": 90}
                    ).set_placement((cx + 1.8 * s, (brk_y + child_top_y) / 2.0), align=TextEntityAlignment.LEFT)

            # -------------------------------------------------------------
            # Case 3: Equipment Symbol (Transformer, Motor, Generator, etc.)
            # -------------------------------------------------------------
            else:
                self.msp.add_blockref(sym, (nx, ny), dxfattribs={"layer": "E-ELEC-SYMB", "xscale": s, "yscale": s})
                lbl = tag
                if dom == "transformers" or "XFMR" in ttag:
                    kva = node.get("kva") or ""
                    lbl = f"{tag} {kva}".strip()
                elif dom == "loads" or "MOTOR" in sym:
                    hp = node.get("hp") or node.get("amps") or ""
                    lbl = f"{tag} {hp}".strip()

                self.msp.add_text(
                    lbl,
                    dxfattribs={"layer": "E-ANNO-TEXT", "height": max(1.8, 2.2 * s)}
                ).set_placement((nx, ny - 8.0 * s), align=TextEntityAlignment.TOP_CENTER)

                # Transformer Secondary Feeder Distribution
                if (dom == "transformers" or "XFMR" in ttag) and ch_list:
                    valid_ch = [c for c in ch_list if c in self.node_coords]
                    if len(valid_ch) == 1:
                        cx, cy = self.node_coords[valid_ch[0]]
                        self.msp.add_line((nx, ny - 10.0 * s), (cx, cy), dxfattribs={"layer": "E-ELEC-FEED"})
                    elif len(valid_ch) > 1:
                        c_xs = [self.node_coords[c][0] for c in valid_ch]
                        c_ys = [self.node_coords[c][1] for c in valid_ch]
                        mid_y = (ny - 10.0 * s + max(c_ys)) / 2.0
                        # Vertical drop from transformer
                        self.msp.add_line((nx, ny - 10.0 * s), (nx, mid_y), dxfattribs={"layer": "E-ELEC-FEED"})
                        # Horizontal distribution manifold
                        self.msp.add_line((min(c_xs), mid_y), (max(c_xs), mid_y), dxfattribs={"layer": "E-ELEC-FEED"})
                        # Vertical taps down to each panel
                        for c in valid_ch:
                            cx, cy = self.node_coords[c]
                            self.msp.add_blockref("SYM_JUNCTION_DOT", (cx, mid_y), dxfattribs={"layer": "E-ELEC-FEED", "xscale": s, "yscale": s})
                            self.msp.add_line((cx, mid_y), (cx, cy), dxfattribs={"layer": "E-ELEC-FEED"})

    def _draw_title_block(self, sheet_w: float = ANSI_D_WIDTH, sheet_h: float = ANSI_D_HEIGHT) -> None:
        """Draws standard IEEE / ANSI D sheet border (24" x 36") and engineering title block."""
        margin = 15.0
        # Outer Border
        self.msp.add_lwpolyline(
            [(margin, margin), (sheet_w - margin, margin), (sheet_w - margin, sheet_h - margin), (margin, sheet_h - margin)],
            close=True,
            dxfattribs={"layer": "E-TTLB"}
        )
        # Inner Drawing Margin
        inner_m = margin + 5.0
        self.msp.add_lwpolyline(
            [(inner_m, inner_m), (sheet_w - inner_m, inner_m), (sheet_w - inner_m, sheet_h - inner_m), (inner_m, sheet_h - inner_m)],
            close=True,
            dxfattribs={"layer": "E-TTLB"}
        )

        # Title Block Box (Bottom Right Corner: 220mm x 60mm)
        tb_w = 220.0
        tb_h = 60.0
        tb_x = sheet_w - inner_m - tb_w
        tb_y = inner_m

        self.msp.add_lwpolyline(
            [(tb_x, tb_y), (tb_x + tb_w, tb_y), (tb_x + tb_w, tb_y + tb_h), (tb_x, tb_y + tb_h)],
            close=True,
            dxfattribs={"layer": "E-TTLB"}
        )
        self.msp.add_line((tb_x, tb_y + 40), (tb_x + tb_w, tb_y + 40), dxfattribs={"layer": "E-TTLB"})
        self.msp.add_line((tb_x, tb_y + 20), (tb_x + tb_w, tb_y + 20), dxfattribs={"layer": "E-TTLB"})
        self.msp.add_line((tb_x + 140, tb_y), (tb_x + 140, tb_y + 20), dxfattribs={"layer": "E-TTLB"})

        self.msp.add_text("BUILDING AWARE • ELECTRICAL DIGITAL TWIN", dxfattribs={"layer": "E-TTLB", "height": 3.0}).set_placement((tb_x + 5, tb_y + 48))
        self.msp.add_text(self.sheet_title, dxfattribs={"layer": "E-TTLB", "height": 3.4}).set_placement((tb_x + 5, tb_y + 42))

        self.msp.add_text(f"CLIENT: {self.client_id}", dxfattribs={"layer": "E-TTLB", "height": 2.8}).set_placement((tb_x + 5, tb_y + 30))
        self.msp.add_text(f"FACILITY: {self.facility_id}", dxfattribs={"layer": "E-TTLB", "height": 2.8}).set_placement((tb_x + 5, tb_y + 24))

        self.msp.add_text("SIZE: ANSI D (24\" × 36\") • N.T.S.", dxfattribs={"layer": "E-TTLB", "height": 2.2}).set_placement((tb_x + 5, tb_y + 10))
        self.msp.add_text(f"DWG: {self.sheet_no}", dxfattribs={"layer": "E-TTLB", "height": 4.0}).set_placement((tb_x + 145, tb_y + 10))

    def compile_dxf_bytes(self) -> bytes:
        """Compile the SLD into AutoCAD DXF ASCII/binary data stream locked to ANSI D."""
        self.build_cad_drawing()
        stream = io.StringIO()
        self.doc.write(stream)
        return stream.getvalue().encode("utf-8")

    def compile_svg_string(self) -> str:
        """Compile the SLD into high-fidelity vector SVG preview locked to ANSI D (864mm x 558mm)."""
        self.build_cad_drawing()
        backend = SVGBackend()
        ctx = RenderContext(self.doc)
        frontend = Frontend(ctx, backend)
        frontend.draw_layout(self.msp)
        page = layout.Page(ANSI_D_WIDTH, ANSI_D_HEIGHT, layout.Units.mm, layout.Margins.all(0))
        return backend.get_string(page)


def export_facility_dxf(project_data: Dict[str, Any], client: str, facility: str, sheet_id: str = "all") -> bytes:
    """Convenience helper to export a facility's project data as ANSI D DXF."""
    nodes = project_data.get("nodes") or project_data.get("stack") or []
    edges = project_data.get("edges") or []
    compiler = SingleLineCadCompiler(nodes=nodes, edges=edges, client_id=client, facility_id=facility, sheet_id=sheet_id)
    return compiler.compile_dxf_bytes()


def export_facility_svg(project_data: Dict[str, Any], client: str, facility: str, sheet_id: str = "all") -> str:
    """Convenience helper to export a facility's project data as ANSI D SVG."""
    nodes = project_data.get("nodes") or project_data.get("stack") or []
    edges = project_data.get("edges") or []
    compiler = SingleLineCadCompiler(nodes=nodes, edges=edges, client_id=client, facility_id=facility, sheet_id=sheet_id)
    return compiler.compile_svg_string()
