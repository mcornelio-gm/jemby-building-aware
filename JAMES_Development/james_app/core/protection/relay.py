"""Microprocessor Numerical Protective Relay Object Class."""

from typing import List, Optional
from pydantic import Field
from james_app.core.base import BaseElectricalObject


class ProtectiveRelayObject(BaseElectricalObject):
    """
    Microprocessor Numerical Protective Relay.
    Performs real-time power system protection, selective tripping, fault recording, and automation.
    Supports standard IEEE/ANSI device functions (50/51, 87, 27/59, 81, 32, 67).
    """
    category: str = "Protective Relaying"
    relay_model: str = Field(default="SEL-751 / GE Multilin", description="Relay manufacturer & model series")
    ansi_functions: List[str] = Field(
        default_factory=lambda: ["50/51 (Instantaneous/Time Overcurrent)", "50N/51N (Ground Overcurrent)", "27/59 (Under/Over Voltage)", "81O/U (Frequency)"],
        description="Active IEEE / ANSI protection elements"
    )
    trip_curve_type: str = Field(default="IEEE Very Inverse (U3)", description="TCC Time-Current Characteristic curve shape")
    pickup_current_amps: float = Field(default=5.0, description="Secondary CT pickup current threshold")
    time_dial_setting: float = Field(default=2.5, description="Time dial multiplier / time multiplier setting (TMS)")
    controls_breaker_id: Optional[str] = Field(default=None, description="Controlled drawout power breaker ID to trip")
    has_arc_flash_sensor: bool = Field(default=True, description="Optical fiber arc-flash point/loop sensor input (<2ms trip)")

    def get_input_ports(self) -> List[str]:
        return ["ct_input_Ia", "ct_input_Ib", "ct_input_Ic", "pt_input_Va", "pt_input_Vb", "pt_input_Vc"]

    def get_output_ports(self) -> List[str]:
        return ["trip_contact_out", "alarm_contact_out"]

    def validate_rules(self) -> List[str]:
        return []

    def compile_focused_dot(self) -> str:
        funcs = "\\n".join(f.split()[0] for f in self.ansi_functions[:3])
        return f'    Relay_{self.id} [shape=hexagon, style="filled", fillcolor="#FEF2F2", color="#EF4444", label="RELAY: {self.tag}\\n{funcs}"];\n'

    def render_html_view(self) -> str:
        return f'<div class="p-2 border border-red-800 bg-red-950/40 rounded text-xs text-red-300"><strong>Relay {self.tag}</strong>: {self.relay_model} ({len(self.ansi_functions)} ANSI Functions)</div>'

    def compile_plantuml_sld(self) -> str:
        return f'card "{self.tag}\\n{self.relay_model}" as {self.id} <<relay>>\n'
