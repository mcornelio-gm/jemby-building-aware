"""Power Factor Correction Capacitor Bank Object Class."""

from typing import List, Optional
from pydantic import Field
from james_app.core.base import BaseElectricalObject


class PowerFactorCapacitorBankObject(BaseElectricalObject):
    """
    Power Factor Correction (PFC) Capacitor Bank.
    Injects leading reactive power (kVAR) to offset inductive motor lagging current,
    raising the facility total power factor to >=0.95 and eliminating utility low-PF penalties.
    """
    category: str = "Power Quality"
    rated_kvar: float = Field(default=150.0, gt=0.0, description="Total reactive power injection capacity in kVAR")
    voltage: float = Field(default=480.0, description="Rated system voltage")
    is_automatic_stepped: bool = Field(default=True, description="Multi-stage automatic stepping controller based on real-time PF")
    steps_count: int = Field(default=6, description="Number of independent switching capacitor stages (e.g. 6x 25kVAR)")
    has_detuning_reactors: bool = Field(default=True, description="Harmonic detuning reactors preventing 5th/7th harmonic resonance")
    detuning_tuning_frequency_hz: float = Field(default=252.0, description="Tuning frequency (e.g. 252 Hz = 4.2nd harmonic)")

    def get_input_ports(self) -> List[str]:
        return ["cap_L1", "cap_L2", "cap_L3"]

    def get_output_ports(self) -> List[str]:
        return []

    def validate_rules(self) -> List[str]:
        warnings = []
        if not self.has_detuning_reactors:
            warnings.append(f"Capacitor Bank {self.tag}: Un-detuned capacitor banks on systems with VFDs may cause severe harmonic resonance.")
        return warnings

    def compile_focused_dot(self) -> str:
        return f'    CAP_{self.id} [shape=box, style="rounded,filled", fillcolor="#EDE9FE", color="#7C3AED", label="PFC: {self.name}\\n{self.rated_kvar:.0f} kVAR ({self.steps_count} Steps)"];\n'

    def render_html_view(self) -> str:
        return f'<div class="p-3 border border-purple-800 bg-slate-900 rounded text-xs text-white"><strong>PFC {self.tag}</strong>: {self.rated_kvar} kVAR ({self.steps_count} Steps)</div>'

    def compile_plantuml_sld(self) -> str:
        return f'card "{self.name}\\n{self.rated_kvar} kVAR Capacitor Bank" as {self.id} <<capacitor>>\n'
