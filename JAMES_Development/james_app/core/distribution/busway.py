"""Electrical Busway / Busduct Feeder Object Class."""

from enum import Enum
from typing import List, Optional
from pydantic import Field
from james_app.core.base import BaseElectricalObject


class BuswayType(str, Enum):
    FEEDER = "Feeder Busway (No Tap-Off Openings)"
    PLUG_IN = "Plug-In Busway (Tap-Off Receptacle Outlets)"


class BuswayConductorMaterial(str, Enum):
    COPPER = "Copper (1000A/sq.in)"
    ALUMINUM = "Aluminum (Density Sized)"


class BuswayObject(BaseElectricalObject):
    """
    Electrical Busway / Busduct Trunk Distribution.
    Prefabs sandwich busbar trunking for vertical riser shafts and manufacturing plant floors.
    Carries high amperage (800A - 5000A) with integrated plug-in tap-off outlets.
    """
    category: str = "Busway Infrastructure"
    busway_type: BuswayType = Field(default=BuswayType.PLUG_IN)
    conductor_material: BuswayConductorMaterial = Field(default=BuswayConductorMaterial.COPPER)
    rated_amps: int = Field(default=1600, ge=800, description="Continuous busbar rating in Amps (800, 1000, 1200, 1600, 2000, 2500, 3000, 4000, 5000)")
    voltage: float = Field(default=480.0, description="Rated system voltage")
    phases: int = Field(default=3, description="3-phase 3W/4W")
    length_ft: float = Field(default=100.0, ge=1.0, description="Total physical busway run distance in feet")
    short_circuit_rating_ka: float = Field(default=65.0, description="Short circuit withstand rating in kA")
    plug_in_outlets_count: int = Field(default=10, description="Number of tap-off plug-in receptacles along the run")

    def get_input_ports(self) -> List[str]:
        return ["bus_in_L1", "bus_in_L2", "bus_in_L3", "bus_in_N", "bus_in_GND"]

    def get_output_ports(self) -> List[str]:
        return [f"tap_outlet_{i}" for i in range(1, self.plug_in_outlets_count + 1)]

    def validate_rules(self) -> List[str]:
        warnings = []
        if self.rated_amps < 800:
            warnings.append(f"Busway {self.tag}: Sandwich busways are typically rated >= 800A (got {self.rated_amps}A).")
        return warnings

    def compile_focused_dot(self) -> str:
        return f'    Busway_{self.id} [shape=box, style="filled", fillcolor="#FEF3C7", color="#D97706", label="BUSWAY: {self.name}\\n{self.rated_amps}A {int(self.voltage)}V ({self.length_ft:.0f}ft)"];\n'

    def render_html_view(self) -> str:
        return f'<div class="p-3 border border-amber-600 bg-slate-900 rounded text-xs text-amber-300"><strong>Busway {self.tag}</strong>: {self.rated_amps}A {self.conductor_material.value.split()[0]} ({self.length_ft:.0f}ft)</div>'

    def compile_plantuml_sld(self) -> str:
        return f'rectangle "{self.name}\\nBusway {self.rated_amps}A" as {self.id} <<busway>> #D97706\n'
