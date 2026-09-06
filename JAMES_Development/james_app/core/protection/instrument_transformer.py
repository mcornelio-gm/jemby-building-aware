"""Current Transformer (CT) and Potential Transformer (PT) Instrument Classes."""

from typing import List, Optional
from pydantic import Field
from james_app.core.base import BaseElectricalObject


class CurrentTransformerObject(BaseElectricalObject):
    """
    Current Transformer (CT).
    Steps down high primary feeder current to standard 5A (or 1A) secondary current
    for protective relays, power quality meters, and revenue billing.
    """
    category: str = "Instrument Transformer"
    primary_ratio_amps: int = Field(default=1200, description="Primary rated current (e.g. 200, 400, 800, 1200, 2000, 4000)")
    secondary_ratio_amps: int = Field(default=5, description="Secondary output rating (5A standard in US, 1A in IEC)")
    accuracy_class: str = Field(default="0.3 B-0.5 (Metering) / C400 (Relaying)", description="IEEE C57.13 accuracy & relaying classification")
    window_diameter_inches: float = Field(default=4.5, description="Internal donut window diameter for busbar/cables")

    @property
    def ratio_str(self) -> str:
        return f"{self.primary_ratio_amps}:{self.secondary_ratio_amps}A"

    def get_input_ports(self) -> List[str]:
        return ["H1_line", "H2_load"]

    def get_output_ports(self) -> List[str]:
        return ["X1_sec", "X2_sec"]

    def validate_rules(self) -> List[str]:
        return []

    def compile_focused_dot(self) -> str:
        return f'    CT_{self.id} [shape=circle, style="filled", fillcolor="#FEF2F2", color="#EF4444", label="CT {self.ratio_str}"];\n'

    def render_html_view(self) -> str:
        return f'<div class="p-1 border border-red-800 bg-red-950/30 rounded text-[11px] text-red-300"><strong>CT {self.tag}</strong>: {self.ratio_str}</div>'

    def compile_plantuml_sld(self) -> str:
        return f'circle "CT {self.ratio_str}" as {self.id} <<ct>>\n'


class PotentialTransformerObject(BaseElectricalObject):
    """
    Potential / Voltage Transformer (PT / VT).
    Steps down high primary distribution voltage (e.g. 480V, 13.8kV) to standard 120V secondary
    for voltage sensing, synchrocheck, and energy metering.
    """
    category: str = "Instrument Transformer"
    primary_voltage: float = Field(default=480.0, description="Primary nominal voltage")
    secondary_voltage: float = Field(default=120.0, description="Secondary metering voltage (120V standard)")
    accuracy_class: str = Field(default="0.3 W, X, M, Y, Z (0.3% revenue accuracy)", description="IEEE metering accuracy class")

    @property
    def ratio_str(self) -> str:
        return f"{int(self.primary_voltage)}V:{int(self.secondary_voltage)}V"

    def get_input_ports(self) -> List[str]:
        return ["H1_pri", "H2_pri"]

    def get_output_ports(self) -> List[str]:
        return ["X1_sec", "X2_sec"]

    def validate_rules(self) -> List[str]:
        return []

    def compile_focused_dot(self) -> str:
        return f'    PT_{self.id} [shape=circle, style="filled", fillcolor="#FEF2F2", color="#EF4444", label="PT {self.ratio_str}"];\n'

    def render_html_view(self) -> str:
        return f'<div class="p-1 border border-red-800 bg-red-950/30 rounded text-[11px] text-red-300"><strong>PT {self.tag}</strong>: {self.ratio_str}</div>'

    def compile_plantuml_sld(self) -> str:
        return f'circle "PT {self.ratio_str}" as {self.id} <<pt>>\n'
