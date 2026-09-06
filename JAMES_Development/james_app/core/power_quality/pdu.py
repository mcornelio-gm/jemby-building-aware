"""Data Center Power Distribution Unit (PDU) Object Class."""

from typing import List, Optional
from pydantic import Field
from james_app.core.base import BaseElectricalObject


class PowerDistributionUnitObject(BaseElectricalObject):
    """
    Data Center Floor Power Distribution Unit (PDU).
    Raised-floor power transformation and high-density distribution cabinet.
    Houses a clean-power K-13 isolation transformer, TVSS surge protection, subfeed breakers,
    and two to four 42-pole output panelboards with Branch Circuit Power Monitoring (BCM).
    """
    category: str = "Data Center Power"
    kva_rating: float = Field(default=150.0, description="Internal isolation transformer kVA (e.g. 75, 100, 150, 225, 300)")
    primary_voltage: float = Field(default=480.0, description="Primary feed voltage")
    secondary_voltage: float = Field(default=208.0, description="Secondary branch voltage (208Y/120V)")
    k_factor: int = Field(default=13, description="Harmonic K-Factor rating (K-13 / K-20)")
    total_branch_poles: int = Field(default=84, description="Total physical branch circuit positions (e.g. dual 42-pole panelboards)")
    has_branch_circuit_monitoring: bool = Field(default=True, description="Per-circuit real-time kW/kVA/Current telemetry")
    has_dual_input_source: bool = Field(default=False, description="Includes integrated Static Transfer Switch (STS)")

    def get_input_ports(self) -> List[str]:
        return ["pri_H1", "pri_H2", "pri_H3", "pri_GND"]

    def get_output_ports(self) -> List[str]:
        return [f"branch_ckt_{i}" for i in range(1, self.total_branch_poles + 1)]

    def validate_rules(self) -> List[str]:
        warnings = []
        if self.total_branch_poles % 42 != 0:
            warnings.append(f"PDU {self.tag}: Output panelboards typically consist of 42-pole column increments.")
        return warnings

    def compile_focused_dot(self) -> str:
        return f'    PDU_{self.id} [shape=box, style="rounded,filled", fillcolor="#EDE9FE", color="#7C3AED", label="PDU: {self.name}\\n{self.kva_rating}kVA ({self.total_branch_poles} Circuits)"];\n'

    def render_html_view(self) -> str:
        return f'<div class="p-3 border border-purple-800 bg-slate-900 rounded text-xs text-white"><strong>PDU {self.tag}</strong>: {self.kva_rating} kVA ({self.total_branch_poles} Branch Circuits)</div>'

    def compile_plantuml_sld(self) -> str:
        return f'rectangle "{self.name}\\nPDU {self.kva_rating}kVA" as {self.id} <<pdu>>\n'
