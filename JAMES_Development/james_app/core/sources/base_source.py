"""Base Power Source Object Class."""

from enum import Enum
import html
import math
from typing import Any, Dict, List, Optional
from pydantic import Field
from james_app.core.base import BaseElectricalObject


class SourceType(str, Enum):
    """Classification of power generation source."""
    UTILITY = "Utility Grid Service"
    GENERATOR = "Standby / Emergency Generator"
    SOLAR_PV = "Solar Photovoltaic"
    BATTERY_BESS = "Battery Energy Storage (BESS)"
    WIND = "Wind Turbine"
    COGEN_CHP = "Combined Heat & Power (CHP)"


class PowerSourceObject(BaseElectricalObject):
    """Base Power Generation & Grid Supply Digital Twin Entity."""
    category: str = "Power Source"
    source_type: SourceType = Field(default=SourceType.UTILITY)
    voltage: float = Field(default=480.0, gt=0.0, description="Nominal line-to-line output voltage in Volts")
    phases: int = Field(default=3, ge=1, le=3, description="Number of output phases (1 or 3)")
    frequency_hz: float = Field(default=60.0, description="Nominal frequency in Hz (50 or 60)")
    capacity_kva: float = Field(default=1000.0, gt=0.0, description="Rated apparent power capacity in kVA")
    capacity_kw: float = Field(default=800.0, gt=0.0, description="Rated real power capacity in kW")
    power_factor: float = Field(default=0.80, ge=0.1, le=1.0, description="Rated operating power factor")
    is_grid_forming: bool = Field(default=True, description="Can establish independent voltage & frequency reference")
    available_fault_current_ka: float = Field(default=40.0, ge=0.0, description="Available short-circuit fault current at source terminals in kA")

    # --- 1. Connectivity Terminals ---
    def get_input_ports(self) -> List[str]:
        """Sources typically have no upstream electrical input (unless charging/fuel)."""
        return []

    def get_output_ports(self) -> List[str]:
        """Source output bus terminals."""
        if self.phases == 1:
            return ["L1", "N", "GND"]
        return ["L1", "L2", "L3", "N", "GND"]

    # --- 2. Deterministic Physics Calculations ---
    @property
    def full_load_amps(self) -> float:
        """Calculate source rated continuous output current in Amps."""
        if self.phases == 3:
            return round((self.capacity_kva * 1000.0) / (math.sqrt(3) * self.voltage), 2)
        return round((self.capacity_kva * 1000.0) / self.voltage, 2)

    # --- 3. Deterministic Code Rules ---
    def validate_rules(self) -> List[str]:
        warnings = []
        if self.capacity_kw > self.capacity_kva:
            warnings.append(f"Source {self.tag}: Real power ({self.capacity_kw} kW) cannot exceed apparent capacity ({self.capacity_kva} kVA).")
        return warnings

    # --- 4. Multi-View Visual Projections ---
    def compile_focused_dot(self) -> str:
        """Render source node in Graphviz DOT format."""
        v_label = f"{int(self.voltage)}V {self.phases}Ø {self.frequency_hz:.0f}Hz"
        return (
            f'    Source_{self.id} [\n'
            f'        id="node_src_{self.id}",\n'
            f'        shape=none,\n'
            f'        label=<\n'
            f'        <TABLE BORDER="2" CELLBORDER="1" CELLSPACING="0" COLOR="#0284C7" BGCOLOR="#FFFFFF">\n'
            f'            <TR><TD BGCOLOR="#0369A1" PORT="out">\n'
            f'                <FONT COLOR="WHITE" POINT-SIZE="10"><B>{html.escape(self.name.upper())}</B></FONT><BR/>\n'
            f'                <FONT COLOR="#BAE6FD" POINT-SIZE="8">[{self.source_type.value} &bull; {self.capacity_kw} kW / {self.capacity_kva} kVA]</FONT>\n'
            f'            </TD></TR>\n'
            f'            <TR><TD BGCOLOR="#F0F9FF" ALIGN="CENTER">\n'
            f'                <FONT POINT-SIZE="8"><B>{v_label}</B> &bull; FLA: {self.full_load_amps}A &bull; I_sc: {self.available_fault_current_ka:.0f}kA</FONT>\n'
            f'            </TD></TR>\n'
            f'        </TABLE>>\n'
            f'    ];\n'
        )

    def render_html_view(self) -> str:
        """Render native HTML component card."""
        return (
            f'<div class="rounded-xl border border-sky-700 bg-slate-950 p-4 shadow-xl space-y-3">'
            f'<div class="flex justify-between items-start border-b border-sky-900 pb-2.5">'
            f'<div>'
            f'<span class="bg-sky-950 text-sky-300 font-mono text-[10px] px-2 py-0.5 rounded uppercase font-semibold">{self.source_type.value}</span>'
            f'<h3 class="font-bold text-white text-sm mt-1">{html.escape(self.name)}</h3>'
            f'</div>'
            f'<span class="bg-sky-600 text-white font-mono text-xs px-2.5 py-1 rounded shadow">{self.tag}</span>'
            f'</div>'
            f'<div class="grid grid-cols-2 gap-2 text-xs bg-slate-900/80 p-3 rounded-lg border border-slate-800">'
            f'<div>'
            f'<p class="text-slate-400 text-[11px]">Capacity</p>'
            f'<p class="font-mono text-cyan-400 font-bold">{self.capacity_kw} kW / {self.capacity_kva} kVA</p>'
            f'</div>'
            f'<div>'
            f'<p class="text-slate-400 text-[11px]">Voltage / Current</p>'
            f'<p class="font-mono text-white font-bold">{int(self.voltage)}V {self.phases}Ø &bull; {self.full_load_amps}A</p>'
            f'</div>'
            f'</div>'
            f'<div class="flex justify-between items-center text-[11px] text-slate-400 font-mono pt-1">'
            f'<span>PF: <strong class="text-white">{self.power_factor}</strong></span>'
            f'<span class="text-sky-400">Fault: {self.available_fault_current_ka:.0f}kA</span>'
            f'</div>'
            f'</div>'
        )

    def compile_plantuml_sld(self) -> str:
        """Render PlantUML SLD power source symbol."""
        return (
            f'circle "{self.name}\\n<size:10>{self.capacity_kw}kW {int(self.voltage)}V</size>" '
            f'as {self.id} <<source>> #0284C7;line:white;text:white\n'
        )
