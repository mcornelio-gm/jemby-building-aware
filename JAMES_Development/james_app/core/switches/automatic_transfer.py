"""Automatic Transfer Switch (ATS) Object Class."""

from enum import Enum
import html
from typing import List, Optional
from pydantic import Field
from james_app.core.switches.base_switch import EnclosureNemaType, SwitchObject, SwitchState


class TransferTransitionType(str, Enum):
    """ATS electrical transition mechanics."""
    OPEN_TRANSITION = "Open Transition (Break-Before-Make)"
    CLOSED_TRANSITION = "Closed Transition (Make-Before-Break / Soft Load)"
    DELAYED_TRANSITION = "Delayed Transition (Programmed Center-Off Neutral Delay)"


class ConnectedSource(str, Enum):
    """Currently connected active power source."""
    NORMAL = "NORMAL (Utility)"
    EMERGENCY = "EMERGENCY (Generator / Alternate)"
    NEUTRAL_OFF = "OFF (Neutral Center Position)"


class AutomaticTransferSwitchObject(SwitchObject):
    """
    Automatic Transfer Switch (ATS).
    Critical power intelligence apparatus designed to automatically sense utility power loss,
    signal engine generator startup via dry contacts, and transfer critical building loads
    from the Normal (Utility) source to the Emergency (Generator) source per NEC 700 / 701 / 702.
    """
    category: str = "Transfer Switch"
    switch_type_name: str = "Automatic Transfer Switch (ATS)"
    normal_source_id: str = Field(..., description="Normal (Utility) source node identifier")
    emergency_source_id: str = Field(..., description="Emergency (Generator/UPS) source node identifier")
    active_source: ConnectedSource = Field(default=ConnectedSource.NORMAL, description="Currently connected power source")
    transition_type: TransferTransitionType = Field(default=TransferTransitionType.OPEN_TRANSITION)
    transfer_time_delay_sec: float = Field(default=3.0, description="Time delay before initiating transfer upon source failure")
    retransfer_time_delay_sec: float = Field(default=300.0, description="Time delay before returning to stable utility power (typically 5-30 min)")
    engine_cooldown_timer_sec: float = Field(default=300.0, description="Generator unloaded cool-down run time")
    has_in_phase_monitor: bool = Field(default=True, description="In-phase synchronism monitor for motor load transfers")
    is_service_entrance_rated: bool = Field(default=False, description="Includes integrated service entrance disconnect breaker")
    has_weekly_exerciser: bool = Field(default=True, description="Programmable weekly engine exerciser timer with/without load")

    # --- 1. Connectivity Terminals ---
    def get_input_ports(self) -> List[str]:
        """ATS has dual source inputs: Normal and Emergency."""
        normal_ports = [f"norm_L{i+1}" for i in range(self.poles)]
        emerg_ports = [f"emerg_L{i+1}" for i in range(self.poles)]
        return normal_ports + emerg_ports

    def get_output_ports(self) -> List[str]:
        """Single common load bus output."""
        return [f"load_T{i+1}" for i in range(self.poles)] + (["load_N"] if self.poles == 4 else [])

    # --- 2. Deterministic Code Rules ---
    def validate_rules(self) -> List[str]:
        """Perform ATS code compliance checks."""
        warnings = super().validate_rules()
        if not self.normal_source_id or not self.emergency_source_id:
            warnings.append(f"ATS {self.tag}: Both Normal and Emergency source feeds must be specified.")
        return warnings

    # --- 3. Multi-View Projections ---
    def compile_focused_dot(self) -> str:
        """Render ATS double-throw dual-source diagram in Graphviz DOT."""
        norm_color = "#16A34A" if self.active_source == ConnectedSource.NORMAL else "#64748B"
        emerg_color = "#DC2626" if self.active_source == ConnectedSource.EMERGENCY else "#64748B"

        return (
            f'    ATS_{self.id} [\n'
            f'        id="node_ats_{self.id}",\n'
            f'        shape=none,\n'
            f'        label=<\n'
            f'        <TABLE BORDER="2" CELLBORDER="1" CELLSPACING="0" COLOR="#B91C1C" BGCOLOR="#FFFFFF">\n'
            f'            <TR><TD COLSPAN="2" BGCOLOR="#991B1B">\n'
            f'                <FONT COLOR="WHITE" POINT-SIZE="10"><B>{html.escape(self.name.upper())}</B></FONT><BR/>\n'
            f'                <FONT COLOR="#FECACA" POINT-SIZE="8">[{self.rated_amps}A {self.poles}P &bull; {self.transition_type.value.split("(")[0]}]</FONT>\n'
            f'            </TD></TR>\n'
            f'            <TR>\n'
            f'                <TD BGCOLOR="#FEF2F2" PORT="norm" ALIGN="LEFT"><FONT POINT-SIZE="8" COLOR="{norm_color}"><B>[NORMAL SOURCE]</B></FONT></TD>\n'
            f'                <TD BGCOLOR="#FEF2F2" PORT="emerg" ALIGN="RIGHT"><FONT POINT-SIZE="8" COLOR="{emerg_color}"><B>[EMERGENCY SOURCE]</B></FONT></TD>\n'
            f'            </TR>\n'
            f'            <TR><TD COLSPAN="2" BGCOLOR="#FEE2E2" ALIGN="CENTER" PORT="load">\n'
            f'                <FONT POINT-SIZE="8" COLOR="#991B1B"><B>ACTIVE FEED: {self.active_source.value}</B></FONT>\n'
            f'            </TD></TR>\n'
            f'        </TABLE>>\n'
            f'    ];\n'
        )

    def render_html_view(self) -> str:
        """Render native HTML interactive ATS dashboard card."""
        return (
            f'<div class="rounded-xl border border-red-700 bg-slate-950 p-4 shadow-xl space-y-3">'
            f'<div class="flex justify-between items-start border-b border-red-900 pb-2.5">'
            f'<div>'
            f'<span class="bg-red-950 text-red-300 font-mono text-[10px] px-2 py-0.5 rounded uppercase font-semibold">Automatic Transfer Switch</span>'
            f'<h3 class="font-bold text-white text-sm mt-1">{html.escape(self.name)}</h3>'
            f'</div>'
            f'<span class="bg-red-600 text-white font-mono text-xs px-2.5 py-1 rounded shadow">{self.tag}</span>'
            f'</div>'
            f'<div class="grid grid-cols-2 gap-2 text-xs bg-slate-900/80 p-3 rounded-lg border border-slate-800">'
            f'<div class="p-2 rounded {"bg-emerald-950 border border-emerald-800 text-emerald-300" if self.active_source == ConnectedSource.NORMAL else "bg-slate-800 text-slate-400"}">'
            f'<p class="text-[10px] uppercase font-bold">Normal Feed</p>'
            f'<p class="font-semibold text-xs truncate">{self.normal_source_id}</p>'
            f'</div>'
            f'<div class="p-2 rounded {"bg-red-950 border border-red-800 text-red-300" if self.active_source == ConnectedSource.EMERGENCY else "bg-slate-800 text-slate-400"}">'
            f'<p class="text-[10px] uppercase font-bold">Emergency Feed</p>'
            f'<p class="font-semibold text-xs truncate">{self.emergency_source_id}</p>'
            f'</div>'
            f'</div>'
            f'<div class="flex justify-between items-center text-[11px] text-slate-400 font-mono pt-1">'
            f'<span>Transition: <strong class="text-slate-200">{self.transition_type.value.split()[0]}</strong></span>'
            f'<span class="text-red-400">Rating: {self.rated_amps}A {self.poles}P</span>'
            f'</div>'
            f'</div>'
        )

    def compile_plantuml_sld(self) -> str:
        """Render PlantUML ATS symbol."""
        return (
            f'rectangle "{self.name}\\n<size:10>ATS {self.rated_amps}A {self.poles}P\\n[{self.active_source.value}]</size>" '
            f'as {self.id} <<ats>> #991B1B;line:white;text:white\n'
        )
