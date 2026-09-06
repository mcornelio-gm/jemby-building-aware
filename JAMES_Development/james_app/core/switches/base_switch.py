"""Base Switch & Disconnect Object Class."""

from enum import Enum
import html
from typing import Any, Dict, List, Optional
from pydantic import Field
from james_app.core.base import BaseElectricalObject


class SwitchState(str, Enum):
    """Mechanical contact operational state."""
    CLOSED = "CLOSED"
    OPEN = "OPEN"
    TRIPPED = "TRIPPED"


class EnclosureNemaType(str, Enum):
    """NEMA Environmental Enclosure Classification."""
    NEMA_1 = "NEMA 1 (General Indoor)"
    NEMA_3R = "NEMA 3R (Outdoor Rainproof)"
    NEMA_4X = "NEMA 4X (Stainless Corrosion / Watertight)"
    NEMA_12 = "NEMA 12 (Industrial Dust-Tight)"


class SwitchObject(BaseElectricalObject):
    """Base Electrical Switch & Disconnect Digital Twin Representation Model."""
    category: str = "Switch & Disconnect"
    switch_type_name: str = Field(default="Safety Switch", description="Specific switch classification")
    poles: int = Field(default=3, ge=1, le=4, description="Number of switching poles (1, 2, 3, or 4)")
    rated_amps: int = Field(default=100, ge=15, description="Continuous thermal current rating in Amps")
    voltage: float = Field(default=480.0, description="Rated system voltage in Volts")
    is_three_phase: bool = Field(default=True, description="True for 3-phase systems, False for 1-phase")
    state: SwitchState = Field(default=SwitchState.CLOSED, description="Operating contact state")
    enclosure_type: EnclosureNemaType = Field(default=EnclosureNemaType.NEMA_1, description="NEMA environmental rating")
    has_lockout_tagout: bool = Field(default=True, description="Equipped with OSHA Lockout/Tagout (LOTO) padlock provisions")
    short_circuit_rating_ka: float = Field(default=10.0, description="Short-circuit current withstand/interrupting rating in kA")
    upstream_source_id: Optional[str] = Field(default=None, description="Upstream feeding source or breaker ID")
    downstream_load_id: Optional[str] = Field(default=None, description="Direct downstream equipment or motor ID")

    # --- 1. Connectivity Terminals ---
    def get_input_ports(self) -> List[str]:
        """Line-side input terminals."""
        return [f"line_L{i+1}" for i in range(self.poles)] + (["line_N"] if self.poles == 4 else [])

    def get_output_ports(self) -> List[str]:
        """Load-side output terminals."""
        return [f"load_T{i+1}" for i in range(self.poles)] + (["load_N"] if self.poles == 4 else [])

    # --- 2. Deterministic Domain & Code Rules ---
    def validate_rules(self) -> List[str]:
        """Perform basic switch code and capacity checks."""
        warnings = []
        if self.rated_amps < 15:
            warnings.append(f"Switch {self.tag}: Rated current ({self.rated_amps}A) is below standard minimum of 15A.")
        if self.is_three_phase and self.poles < 3:
            warnings.append(f"Switch {self.tag}: 3-phase switch must have at least 3 poles (got {self.poles}P).")
        return warnings

    # --- 3. Multi-View Visual Projections ---
    def compile_focused_dot(self) -> str:
        """Render focused Graphviz DOT node depicting switch contacts and status."""
        state_color = "#16A34A" if self.state == SwitchState.CLOSED else "#DC2626"
        status_label = f"[{self.state.value}]"
        
        return (
            f'    Switch_{self.id} [\n'
            f'        id="node_sw_{self.id}",\n'
            f'        shape=none,\n'
            f'        label=<\n'
            f'        <TABLE BORDER="2" CELLBORDER="1" CELLSPACING="0" COLOR="#047857" BGCOLOR="#FFFFFF">\n'
            f'            <TR><TD COLSPAN="2" BGCOLOR="#065F46" PORT="line">\n'
            f'                <FONT COLOR="WHITE" POINT-SIZE="10"><B>{html.escape(self.name.upper())}</B></FONT><BR/>\n'
            f'                <FONT COLOR="#A7F3D0" POINT-SIZE="8">[{self.switch_type_name} &bull; {self.rated_amps}A {self.poles}P]</FONT>\n'
            f'            </TD></TR>\n'
            f'            <TR>\n'
            f'                <TD BGCOLOR="#ECFDF5" ALIGN="LEFT"><FONT POINT-SIZE="8"><B>NEMA:</B> {self.enclosure_type.value.split()[0]}</FONT></TD>\n'
            f'                <TD BGCOLOR="#ECFDF5" ALIGN="RIGHT" PORT="load"><FONT POINT-SIZE="8" COLOR="{state_color}"><B>{status_label}</B></FONT></TD>\n'
            f'            </TR>\n'
            f'            <TR><TD COLSPAN="2" BGCOLOR="#D1FAE5" ALIGN="CENTER">\n'
            f'                <FONT POINT-SIZE="7" COLOR="#065F46">SCCR: {self.short_circuit_rating_ka:.0f}kA &bull; {int(self.voltage)}V</FONT>\n'
            f'            </TD></TR>\n'
            f'        </TABLE>>\n'
            f'    ];\n'
        )

    def render_html_view(self) -> str:
        """Render native HTML switch badge / card."""
        state_bg = "bg-emerald-950 text-emerald-400 border-emerald-800" if self.state == SwitchState.CLOSED else "bg-red-950 text-red-400 border-red-800"

        return (
            f'<div class="rounded-xl border border-emerald-700 bg-slate-950 p-4 shadow-xl space-y-3">'
            f'<div class="flex justify-between items-start border-b border-emerald-900 pb-2.5">'
            f'<div>'
            f'<span class="bg-emerald-950 text-emerald-300 font-mono text-[10px] px-2 py-0.5 rounded uppercase font-semibold">{self.switch_type_name}</span>'
            f'<h3 class="font-bold text-white text-sm mt-1">{html.escape(self.name)}</h3>'
            f'</div>'
            f'<span class="bg-emerald-600 text-white font-mono text-xs px-2.5 py-1 rounded shadow">{self.tag}</span>'
            f'</div>'
            f'<div class="flex justify-between items-center bg-slate-900/80 p-3 rounded-lg border border-slate-800 text-xs">'
            f'<div>'
            f'<p class="text-slate-400 text-[11px]">Rating / Poles</p>'
            f'<p class="font-mono text-white font-bold">{self.rated_amps}A &bull; {self.poles}P ({int(self.voltage)}V)</p>'
            f'</div>'
            f'<div class="text-right">'
            f'<span class="px-2.5 py-1 rounded border font-mono text-xs font-bold {state_bg}">{self.state.value}</span>'
            f'</div>'
            f'</div>'
            f'<div class="flex justify-between items-center text-[11px] text-slate-400 font-mono pt-1">'
            f'<span>Enclosure: <strong class="text-slate-200">{self.enclosure_type.value.split()[0]}</strong></span>'
            f'<span class="text-emerald-400">SCCR: {self.short_circuit_rating_ka:.0f}kA</span>'
            f'</div>'
            f'</div>'
        )

    def compile_plantuml_sld(self) -> str:
        """Render single-line diagram symbol for switch / disconnect."""
        return (
            f'rectangle "{self.name}\\n<size:10>{self.rated_amps}A {self.poles}P [{self.state.value}]</size>" '
            f'as {self.id} <<switch>> #047857;line:white;text:white\n'
        )
