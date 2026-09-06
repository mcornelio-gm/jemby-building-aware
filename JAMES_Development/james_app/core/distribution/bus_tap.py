"""Busway Plug-In Tap-Off Disconnect/Breaker Unit Object Class."""

from typing import List, Optional
from pydantic import Field
from james_app.core.base import BaseElectricalObject


class BusTapOffUnitObject(BaseElectricalObject):
    """
    Busway Plug-In Tap-Off Unit (Bus Plug).
    Stab-connected disconnect switch or molded case circuit breaker tapped into the busway spine
    to feed a local industrial machine, subpanel, or crane rail.
    """
    category: str = "Busway Tap-Off"
    breaker_or_switch_amps: int = Field(default=100, ge=30, description="Tap-off OCPD trip rating in Amps (30A - 800A)")
    poles: int = Field(default=3, ge=1, le=3, description="Switching poles")
    is_fusible: bool = Field(default=False, description="True for fusible switch plug, False for circuit breaker plug")
    host_busway_id: Optional[str] = Field(default=None, description="Host parent busway ID")
    tap_outlet_index: int = Field(default=1, description="Physical plug outlet position index on the busway run")

    def get_input_ports(self) -> List[str]:
        return ["bus_stabs"]

    def get_output_ports(self) -> List[str]:
        return ["load_terminals"]

    def validate_rules(self) -> List[str]:
        return []

    def compile_focused_dot(self) -> str:
        return f'    BusTap_{self.id} [shape=ellipse, style="filled", fillcolor="#FEF3C7", color="#D97706", label="Tap: {self.tag}\\n{self.breaker_or_switch_amps}A {self.poles}P"];\n'

    def render_html_view(self) -> str:
        return f'<div class="p-2 border border-amber-500 bg-amber-950/40 rounded text-xs text-amber-200"><strong>Tap {self.tag}</strong>: {self.breaker_or_switch_amps}A {self.poles}P</div>'

    def compile_plantuml_sld(self) -> str:
        return f'card "Tap {self.tag}\\n{self.breaker_or_switch_amps}A" as {self.id} <<bustap>>\n'
