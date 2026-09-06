"""Base Electrical Load Object Class."""

from enum import Enum
import html
import math
from typing import Any, Dict, List, Optional
from pydantic import Field
from james_app.core.base import BaseElectricalObject


class LoadType(str, Enum):
    """General load classification."""
    MOTOR = "Electric Motor / Rotating Machinery"
    VFD = "Variable Frequency Drive"
    HVAC = "HVAC Packaged Unit / Chiller"
    EV_CHARGER = "EV Charging Station"
    LIGHTING = "Lighting Circuit / Zone"
    RECEPTACLE = "General Receptacles / Appliances"
    IT_SERVER = "Data Center IT Rack / Server"
    PROCESS = "Industrial Process Equipment"
    CUSTOM = "Custom Load"


class LoadObject(BaseElectricalObject):
    """Base Electrical Load Digital Twin Representation Model."""
    category: str = "Electrical Load"
    load_type: LoadType = Field(default=LoadType.RECEPTACLE)
    voltage: float = Field(default=120.0, gt=0.0, description="Operating voltage in Volts")
    phases: int = Field(default=1, ge=1, le=3, description="Phase count (1 or 3)")
    power_kw: float = Field(default=1.8, ge=0.0, description="Real active power in kW")
    power_kva: float = Field(default=2.0, ge=0.0, description="Apparent power in kVA")
    power_factor: float = Field(default=0.90, ge=0.1, le=1.0, description="Operating power factor")
    is_continuous: bool = Field(default=True, description="Operates continuously for >=3 hours (NEC 125% factor)")
    upstream_panel_id: Optional[str] = Field(default=None, description="Feeding panelboard ID")
    upstream_breaker_tag: Optional[str] = Field(default=None, description="Feeding circuit breaker tag")

    # --- 1. Connectivity Terminals ---
    def get_input_ports(self) -> List[str]:
        """Load connection input terminals."""
        if self.phases == 1:
            return ["L1", "N", "GND"]
        return ["L1", "L2", "L3", "N", "GND"]

    def get_output_ports(self) -> List[str]:
        """Loads terminate the circuit path."""
        return []

    # --- 2. Deterministic Electrical Sizing ---
    @property
    def full_load_amps(self) -> float:
        """Calculate continuous operating current in Amps."""
        if self.phases == 3:
            return round((self.power_kva * 1000.0) / (math.sqrt(3) * self.voltage), 2)
        return round((self.power_kva * 1000.0) / self.voltage, 2)

    @property
    def minimum_circuit_ampacity(self) -> float:
        """Calculate conductor ampacity requirement (125% continuous per NEC 210.19)."""
        factor = 1.25 if self.is_continuous else 1.0
        return round(self.full_load_amps * factor, 2)

    def validate_rules(self) -> List[str]:
        warnings = []
        if self.power_kw > self.power_kva:
            warnings.append(f"Load {self.tag}: kW ({self.power_kw}) cannot exceed kVA ({self.power_kva}).")
        return warnings

    # --- 3. Multi-View Visual Projections ---
    def compile_focused_dot(self) -> str:
        """Render load node in Graphviz DOT format."""
        v_str = f"{int(self.voltage)}V {self.phases}Ø"
        return (
            f'    Load_{self.id} [\n'
            f'        id="node_load_{self.id}",\n'
            f'        shape=box, style="rounded,filled", fillcolor="#F1F5F9", color="#475569",\n'
            f'        label=<\n'
            f'            <font point-size="8" color="#475569"><b>[{self.load_type.value.split("/")[0].strip()}]</b></font><br/>\n'
            f'            <b>{html.escape(self.name)}</b><br/>\n'
            f'            <font point-size="8" color="#64748B">{v_str} &bull; {self.power_kw}kW ({self.full_load_amps}A)</font>\n'
            f'        >\n'
            f'    ];\n'
        )

    def render_html_view(self) -> str:
        """Render native HTML load card."""
        return (
            f'<div class="rounded-xl border border-slate-700 bg-slate-950 p-3 shadow text-xs space-y-2">'
            f'<div class="flex justify-between items-center">'
            f'<span class="bg-slate-800 text-slate-300 font-mono text-[10px] px-2 py-0.5 rounded">{self.load_type.value.split("/")[0].strip()}</span>'
            f'<span class="font-mono text-cyan-400 font-bold">{html.escape(self.tag)}</span>'
            f'</div>'
            f'<h4 class="font-bold text-white text-xs truncate">{html.escape(self.name)}</h4>'
            f'<div class="flex justify-between text-[11px] text-slate-400 font-mono">'
            f'<span>{int(self.voltage)}V {self.phases}Ø &bull; {self.power_kw}kW</span>'
            f'<span class="text-white font-semibold">{self.full_load_amps} FLA</span>'
            f'</div>'
            f'</div>'
        )

    def compile_plantuml_sld(self) -> str:
        """Render PlantUML load component."""
        return f"card \"{self.name}\\n{self.power_kw}kW {self.full_load_amps}A\" as {self.id} <<load>>\n"
