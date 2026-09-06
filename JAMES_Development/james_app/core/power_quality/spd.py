"""Surge Protective Device (SPD / TVSS) Object Class (NEC 242)."""

from enum import Enum
from typing import List, Optional
from pydantic import Field
from james_app.core.base import BaseElectricalObject


class SpdType(str, Enum):
    TYPE_1 = "Type 1 (Service Entrance Line/Load Side)"
    TYPE_2 = "Type 2 (Panelboard Load Side)"
    TYPE_3 = "Type 3 (Point of Utilization)"


class SurgeProtectiveDeviceObject(BaseElectricalObject):
    """
    Surge Protective Device (SPD / Transient Voltage Surge Suppressor - TVSS).
    Protects downstream sensitive electronics and panelboards against lightning surges
    and utility switching spikes per NEC Article 242 and UL 1449 4th Edition.
    """
    category: str = "Surge Protection"
    spd_type: SpdType = Field(default=SpdType.TYPE_2)
    surge_capacity_ka_per_phase: float = Field(default=120.0, ge=20.0, description="Surge current capacity per phase in kA (e.g. 50kA, 100kA, 200kA)")
    voltage_protection_rating_vpr: str = Field(default="L-N: 700V, L-G: 700V, N-G: 700V", description="UL 1449 clamping voltage protection rating (VPR)")
    short_circuit_current_rating_sccr_ka: float = Field(default=200.0, description="Short circuit withstand rating in kA")
    mrg_modes_protected: str = Field(default="All-Mode Protection (L-N, L-G, L-L, N-G)", description="Protected electrical transient modes")
    has_audible_alarm: bool = Field(default=True, description="Audible buzzer alarm upon MOV component degradation")
    has_surge_counter: bool = Field(default=True, description="Digital LCD surge event strike counter")
    connected_panel_id: Optional[str] = Field(default=None, description="Directly connected host panelboard tag or ID")

    def get_input_ports(self) -> List[str]:
        return ["phase_stabs", "neutral", "ground"]

    def get_output_ports(self) -> List[str]:
        return []

    def validate_rules(self) -> List[str]:
        warnings = []
        if self.surge_capacity_ka_per_phase < 50.0 and self.spd_type == SpdType.TYPE_1:
            warnings.append(f"SPD {self.tag}: Type 1 Service Entrance SPDs recommend >= 100kA per phase (got {self.surge_capacity_ka_per_phase}kA).")
        return warnings

    def compile_focused_dot(self) -> str:
        return f'    SPD_{self.id} [shape=diamond, style=filled, fillcolor="#EDE9FE", color="#7C3AED", label="SPD: {self.tag}\\n{self.surge_capacity_ka_per_phase:.0f}kA/Phase"];\n'

    def render_html_view(self) -> str:
        return f'<div class="p-2 border border-purple-800 bg-purple-950/40 rounded text-xs text-purple-300"><strong>{self.tag}</strong>: {self.spd_type.value.split()[0]} ({self.surge_capacity_ka_per_phase:.0f}kA/Phase)</div>'

    def compile_plantuml_sld(self) -> str:
        return f'component "{self.tag}\\n{self.surge_capacity_ka_per_phase:.0f}kA SPD" as {self.id} <<spd>>\n'
