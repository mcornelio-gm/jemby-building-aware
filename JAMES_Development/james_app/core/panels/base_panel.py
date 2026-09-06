"""Base Panelboard Object Class for electrical distribution enclosures."""

from enum import Enum
import html
from typing import Any, Dict, List, Optional, Set
from pydantic import Field
from james_app.core.base import BaseElectricalObject
from james_app.core.breaker import BreakerStatus, CircuitBreakerObject


class SystemType(str, Enum):
    """Electrical distribution system phase & voltage configuration."""
    THREE_PHASE_208Y_120V = "120/208V 3Ø 4W"
    THREE_PHASE_480Y_277V = "277/480V 3Ø 4W"
    SINGLE_PHASE_120_240V = "120/240V 1Ø 3W"


class MainsType(str, Enum):
    """Main overcurrent protection or lug configuration."""
    MCB = "MAIN BREAKER"
    MLO = "MAIN LUGS ONLY"


STANDARD_SPACES = [18, 30, 42, 54, 72, 84]


class PanelboardObject(BaseElectricalObject):
    """Base Electrical Panelboard Digital Twin Representation Model."""
    category: str = "Distribution Enclosure"
    system_type: SystemType = Field(default=SystemType.THREE_PHASE_208Y_120V)
    mains_type: MainsType = Field(default=MainsType.MCB)
    mains_rating_amps: int = Field(default=400, description="Main breaker or lug rating in Amps")
    bus_amps: int = Field(default=400, description="Main busbar continuous rating in Amps")
    total_spaces: int = Field(default=42, description="Total physical slots (18, 30, 42, 54, 72, 84)")
    breakers: Dict[int, CircuitBreakerObject] = Field(default_factory=dict, description="Map of slot_start -> CircuitBreakerObject")
    upstream_feed: Optional[Dict[str, str]] = Field(default=None, description="Upstream source metadata")
    downstream_loads: Dict[str, Dict[str, Any]] = Field(default_factory=dict, description="Downstream load models")

    # --- 1. Connectivity Terminals ---
    def get_input_ports(self) -> List[str]:
        return ["main"]

    def get_output_ports(self) -> List[str]:
        return [f"ckt_{s}" for s in range(1, self.total_spaces + 1)]

    # --- 2. Deterministic Domain & Phase Rules ---
    def compute_slot_phase(self, slot: int) -> str:
        """Compute bus phase stab (A, B, C) for a given slot."""
        row = (slot - 1) // 2  # 0-indexed row
        if self.system_type == SystemType.SINGLE_PHASE_120_240V:
            return "A" if (row % 2 == 0) else "B"
        else:
            phases = ["A", "B", "C"]
            return phases[row % 3]

    @staticmethod
    def auto_size(poles_used: int, buffer_pct: float = 0.20) -> int:
        """Find the smallest standard panel space count >= poles_used * (1 + buffer_pct)."""
        target = int(poles_used * (1.0 + buffer_pct))
        for count in STANDARD_SPACES:
            if count >= target and count >= poles_used:
                return count
        return STANDARD_SPACES[-1]

    def add_breaker(
        self,
        slot_start: int,
        poles: int,
        amps: int,
        description: str,
        status: BreakerStatus = BreakerStatus.ON,
        target_load_id: Optional[str] = None
    ) -> CircuitBreakerObject:
        """Add or update an embedded breaker object with slot and phase validation."""
        if slot_start < 1 or slot_start > self.total_spaces:
            raise ValueError(f"Slot {slot_start} exceeds panel capacity (1..{self.total_spaces})")

        occupied = [slot_start + (i * 2) for i in range(poles)]
        for s in occupied:
            if s > self.total_spaces:
                raise ValueError(f"Breaker pole {s} exceeds panel capacity ({self.total_spaces})")

        phases = [self.compute_slot_phase(s) for s in occupied]

        # Clear existing breakers on these slots
        for existing_slot in list(self.breakers.keys()):
            bkr = self.breakers[existing_slot]
            if any(s in occupied for s in bkr.occupied_slots):
                del self.breakers[existing_slot]

        new_bkr = CircuitBreakerObject(
            id=f"bkr_{self.id}_{slot_start}",
            tag=f"CB-{slot_start}" if poles == 1 else f"CB-{slot_start}/{occupied[-1]}",
            name=description,
            slot_start=slot_start,
            poles=poles,
            occupied_slots=occupied,
            amps=amps,
            status=status,
            connected_phases=phases,
            target_load_id=target_load_id
        )
        self.breakers[slot_start] = new_bkr
        return new_bkr

    @classmethod
    def create_empty(
        cls,
        panel_id: str,
        tag: str = "MDP-1",
        name: str = "MAIN DISTRIBUTION PANEL",
        total_spaces: int = 42,
        mains_rating_amps: int = 400,
        system_type: SystemType = SystemType.THREE_PHASE_208Y_120V,
        mains_type: MainsType = MainsType.MCB
    ) -> "PanelboardObject":
        """Instantiate a new panelboard with all slots initialized as [SPARE]."""
        panel = cls(
            id=panel_id,
            tag=tag,
            name=name,
            total_spaces=total_spaces,
            mains_rating_amps=mains_rating_amps,
            bus_amps=mains_rating_amps,
            system_type=system_type,
            mains_type=mains_type,
            breakers={}
        )

        for slot in range(1, total_spaces + 1):
            phase = panel.compute_slot_phase(slot)
            panel.breakers[slot] = CircuitBreakerObject(
                id=f"bkr_{panel_id}_{slot}",
                tag=f"CB-{slot}",
                name=f"Unused :{slot}",
                slot_start=slot,
                poles=1,
                occupied_slots=[slot],
                amps=0,
                status=BreakerStatus.SPARE,
                connected_phases=[phase]
            )

        return panel

    def validate_rules(self) -> List[str]:
        """Perform physics, phase load balance, and capacity verification."""
        warnings = []
        if self.total_spaces % 2 != 0:
            warnings.append(f"Panel {self.tag}: Total spaces ({self.total_spaces}) must be an even number.")
        
        if self.bus_amps < self.mains_rating_amps:
            warnings.append(f"Panel {self.tag}: Bus rating ({self.bus_amps}A) is less than mains rating ({self.mains_rating_amps}A).")

        # Phase Load Summation
        phase_amps = {"A": 0.0, "B": 0.0, "C": 0.0}
        for bkr in self.breakers.values():
            if bkr.status == BreakerStatus.ON:
                per_pole_amps = bkr.amps / bkr.poles
                for p in bkr.connected_phases:
                    if p in phase_amps:
                        phase_amps[p] += per_pole_amps

        if self.system_type != SystemType.SINGLE_PHASE_120_240V:
            vals = [phase_amps["A"], phase_amps["B"], phase_amps["C"]]
            avg = sum(vals) / 3.0 if sum(vals) > 0 else 0.0
            if avg > 0:
                max_dev = max(abs(v - avg) for v in vals)
                unbalance_pct = (max_dev / avg) * 100.0
                if unbalance_pct > 15.0:
                    warnings.append(f"Panel {self.tag}: High phase unbalance detected ({unbalance_pct:.1f}%). Rebalance loads across phases A, B, C.")

        return warnings

    # --- 3. View Projection: Graphviz DOT HTML Table ---
    def compile_focused_dot(self) -> str:
        """Generate focused Graphviz DOT depiction with 4-column HTML table."""
        dot_lines = [
            "digraph FocusedPanel {",
            '    graph [rankdir=TB, splines=polyline, nodesep=0.8, ranksep=0.8, fontname="Helvetica", bgcolor="transparent"];',
            '    node [shape=none, fontname="Helvetica", fontsize=9];',
            '    edge [dir=forward, arrowhead=vee, arrowsize=0.7, penwidth=1.2, color="#1E293B", fontname="Helvetica", fontsize=8];',
            ""
        ]

        total_rows = self.total_spaces // 2
        slot_to_bkr: Dict[int, CircuitBreakerObject] = {}
        for bkr in self.breakers.values():
            for s in bkr.occupied_slots:
                slot_to_bkr[s] = bkr

        spanned_left: Set[int] = set()
        spanned_right: Set[int] = set()
        table_rows = []

        # Headers
        table_rows.append(
            f'            <TR><TD COLSPAN="4" BGCOLOR="#1A365D" PORT="main">'
            f'<FONT COLOR="WHITE" POINT-SIZE="11"><B>{html.escape(self.name.upper())} ({self.total_spaces} SPACES)</B></FONT>'
            f'</TD></TR>'
        )
        sub_title = f"[ {self.mains_rating_amps}A {self.mains_type.value} - {self.system_type.value} ]"
        table_rows.append(
            f'            <TR><TD COLSPAN="4" BGCOLOR="#2A4365">'
            f'<FONT COLOR="WHITE" POINT-SIZE="9"><B>{html.escape(sub_title)}</B></FONT>'
            f'</TD></TR>'
        )

        for row_idx in range(total_rows):
            left_s = 2 * row_idx + 1
            right_s = 2 * row_idx + 2
            left_bkr = slot_to_bkr.get(left_s)
            right_bkr = slot_to_bkr.get(right_s)

            row_tds = []

            # Left Cell
            if left_s not in spanned_left:
                if left_bkr and left_bkr.slot_start == left_s:
                    rowspan = f' ROWSPAN="{left_bkr.poles}"' if left_bkr.poles > 1 else ""
                    port = f"ckt_{'_'.join(str(s) for s in left_bkr.occupied_slots)}"
                    if left_bkr.status == BreakerStatus.SPARE:
                        row_tds.append(f'<TD ALIGN="LEFT"{rowspan} BGCOLOR="#FEFCBF" PORT="{port}"><FONT COLOR="#744210">[SPARE] {html.escape(left_bkr.name)}</FONT></TD>')
                    else:
                        poles_str = f" ({left_bkr.poles}P {left_bkr.amps}A)" if left_bkr.poles > 1 else f" ({left_bkr.amps}A)"
                        slot_str = ",".join(str(s) for s in left_bkr.occupied_slots)
                        row_tds.append(f'<TD ALIGN="LEFT"{rowspan} PORT="{port}"><B>[{left_bkr.status.value}] {slot_str}: {html.escape(left_bkr.name)}{poles_str}</B></TD>')
                    for s in left_bkr.occupied_slots[1:]:
                        spanned_left.add(s)
                else:
                    row_tds.append(f'<TD ALIGN="LEFT" BGCOLOR="#FEFCBF" PORT="ckt_{left_s}"><FONT COLOR="#744210">[SPARE] Unused :{left_s}</FONT></TD>')

            row_tds.append(f'<TD BGCOLOR="#E2E8F0"><B>{left_s}</B></TD>')
            row_tds.append(f'<TD BGCOLOR="#E2E8F0"><B>{right_s}</B></TD>')

            # Right Cell
            if right_s not in spanned_right:
                if right_bkr and right_bkr.slot_start == right_s:
                    rowspan = f' ROWSPAN="{right_bkr.poles}"' if right_bkr.poles > 1 else ""
                    port = f"ckt_{'_'.join(str(s) for s in right_bkr.occupied_slots)}"
                    if right_bkr.status == BreakerStatus.SPARE:
                        row_tds.append(f'<TD ALIGN="RIGHT"{rowspan} BGCOLOR="#FEFCBF" PORT="{port}"><FONT COLOR="#744210">[SPARE] {html.escape(right_bkr.name)}</FONT></TD>')
                    else:
                        poles_str = f" ({right_bkr.poles}P {right_bkr.amps}A)" if right_bkr.poles > 1 else f" ({right_bkr.amps}A)"
                        slot_str = ",".join(str(s) for s in right_bkr.occupied_slots)
                        row_tds.append(f'<TD ALIGN="RIGHT"{rowspan} PORT="{port}"><B>{html.escape(right_bkr.name)}{poles_str} :{slot_str} [{right_bkr.status.value}]</B></TD>')
                    for s in right_bkr.occupied_slots[1:]:
                        spanned_right.add(s)
                else:
                    row_tds.append(f'<TD ALIGN="RIGHT" BGCOLOR="#FEFCBF" PORT="ckt_{right_s}"><FONT COLOR="#744210">[SPARE] Unused :{right_s}</FONT></TD>')

            table_rows.append(f"            <TR>{''.join(row_tds)}</TR>")

        table_html = "\n".join(table_rows)
        dot_lines.append(f'    Panel_{self.id} [')
        dot_lines.append(f'        id="node_panel_{self.id}",')
        dot_lines.append('        label=<')
        dot_lines.append('        <TABLE BORDER="2" CELLBORDER="1" CELLSPACING="0" COLOR="#1A365D" BGCOLOR="#FFFFFF">')
        dot_lines.append(f'{table_html}')
        dot_lines.append('        </TABLE>>')
        dot_lines.append('    ];\n')

        # Upstream Service Feed Edge
        if self.upstream_feed:
            src_id = self.upstream_feed.get("id", "Utility_Grid")
            src_name = self.upstream_feed.get("name", "Utility Grid")
            src_v = self.upstream_feed.get("voltage", "120/208V Main")
            dot_lines.append(f'    {src_id} [shape=box, style="rounded,filled", fillcolor="#E2E8F0", color="#475569", label=<<b>{html.escape(src_name)}</b><br/><font point-size="8" color="#64748B">({html.escape(src_v)})</font>>];\n')
            dot_lines.append(f'    {src_id} -> Panel_{self.id}:main [label=" Service Feed "];\n')

        # Downstream Load Edges
        for bkr in self.breakers.values():
            if bkr.target_load_id and bkr.target_load_id in self.downstream_loads:
                load = self.downstream_loads[bkr.target_load_id]
                load_id = f"Load_{bkr.target_load_id}"
                port = f"ckt_{'_'.join(str(s) for s in bkr.occupied_slots)}"
                dot_lines.append(f'    {load_id} [shape=box, style="rounded,filled", fillcolor="#E2E8F0", color="#475569", label=<<b>{html.escape(load.get("name", "Load"))}</b><br/><font point-size="8" color="#64748B">({html.escape(load.get("rating_label", ""))})</font>>];\n')
                dot_lines.append(f'    Panel_{self.id}:{port} -> {load_id} [label=" {bkr.amps}A Cir {bkr.slot_start} "];\n')

        dot_lines.append("}\n")
        return "\n".join(dot_lines)

    # --- 4. View Projection: Native HTML/Tailwind Schedule ---
    def render_html_view(self) -> str:
        """Render a native HTML/Tailwind interactive schedule component."""
        total_rows = self.total_spaces // 2
        slot_to_bkr = {s: bkr for bkr in self.breakers.values() for s in bkr.occupied_slots}
        spanned_l, spanned_r = set(), set()

        rows_html = []
        for r in range(total_rows):
            ls, rs = 2 * r + 1, 2 * r + 2
            lb, rb = slot_to_bkr.get(ls), slot_to_bkr.get(rs)

            l_cell = ""
            if ls not in spanned_l:
                if lb and lb.slot_start == ls:
                    l_cell = f'<td class="p-2 border border-slate-700 bg-slate-800/80 text-left" rowspan="{lb.poles}">{lb.render_html_view()}</td>'
                    for s in lb.occupied_slots[1:]:
                        spanned_l.add(s)
                else:
                    l_cell = f'<td class="p-2 border border-slate-700 bg-amber-950/30 text-amber-400 text-xs text-left">[SPARE] Unused :{ls}</td>'

            r_cell = ""
            if rs not in spanned_r:
                if rb and rb.slot_start == rs:
                    r_cell = f'<td class="p-2 border border-slate-700 bg-slate-800/80 text-right" rowspan="{rb.poles}">{rb.render_html_view()}</td>'
                    for s in rb.occupied_slots[1:]:
                        spanned_r.add(s)
                else:
                    r_cell = f'<td class="p-2 border border-slate-700 bg-amber-950/30 text-amber-400 text-xs text-right">[SPARE] Unused :{rs}</td>'

            rows_html.append(
                f'<tr class="hover:bg-slate-800/50 transition">'
                f'{l_cell}'
                f'<td class="px-2.5 py-1.5 border border-slate-700 bg-slate-900 font-mono font-bold text-cyan-400 text-center text-xs">{ls}</td>'
                f'<td class="px-2.5 py-1.5 border border-slate-700 bg-slate-900 font-mono font-bold text-cyan-400 text-center text-xs">{rs}</td>'
                f'{r_cell}'
                f'</tr>'
            )

        return (
            f'<div class="rounded-xl border border-slate-700 bg-slate-950 overflow-hidden shadow-2xl">'
            f'<div class="bg-indigo-950 px-4 py-3 border-b border-indigo-800 flex justify-between items-center">'
            f'<div><h3 class="font-bold text-white text-sm">{html.escape(self.name)} ({self.total_spaces} SPACES)</h3>'
            f'<p class="text-xs text-indigo-300 font-mono">{self.mains_rating_amps}A {self.mains_type.value} &bull; {self.system_type.value}</p></div>'
            f'<span class="bg-indigo-600 text-white font-mono text-xs px-2 py-0.5 rounded shadow">{self.tag}</span>'
            f'</div>'
            f'<table class="w-full text-xs border-collapse">'
            f'<tbody>{"".join(rows_html)}</tbody>'
            f'</table>'
            f'</div>'
        )

    # --- 5. View Projection: PlantUML Single-Line Schematic ---
    def compile_plantuml_sld(self) -> str:
        """Render PlantUML Single-Line Diagram with horizontal busbar."""
        puml = [
            "@startuml",
            "!theme plain",
            "skinparam shadowing false",
            "skinparam defaultFontName Helvetica",
            f"rectangle \"== {self.name}\\n<size:10>{self.mains_rating_amps}A {self.system_type.value}</size>\" as {self.id} <<busbar>> #1A365D;line:white;text:white {{",
            "}"
        ]

        if self.upstream_feed:
            src_id = self.upstream_feed.get("id", "Utility")
            src_name = self.upstream_feed.get("name", "Utility Grid")
            puml.append(f"circle \"{src_name}\" as {src_id}")
            puml.append(f"{src_id} --> {self.id} : Service Feed")

        for bkr in self.breakers.values():
            if bkr.status == BreakerStatus.ON:
                bkr_tag = f"CB_{bkr.slot_start}"
                puml.append(f"card \"{bkr.name}\\n{bkr.poles}P {bkr.amps}A\" as {bkr_tag}")
                puml.append(f"{self.id} --> {bkr_tag} : Cir {bkr.slot_start}")

        puml.append("@enduml\n")
        return "\n".join(puml)
