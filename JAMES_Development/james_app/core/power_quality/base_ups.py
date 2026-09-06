"""Base Uninterruptible Power Supply (UPS) Object Class."""

from enum import Enum
import html
import math
from typing import Any, Dict, List, Optional
from pydantic import Field
from james_app.core.base import BaseElectricalObject


class UpsTopology(str, Enum):
    DOUBLE_CONVERSION = "Online Double-Conversion"
    LINE_INTERACTIVE = "Line-Interactive"
    ROTARY_FLYWHEEL = "Rotary Dynamic (Flywheel/Diesel)"


class UpsObject(BaseElectricalObject):
    """Base Uninterruptible Power Supply (UPS) Digital Twin Entity."""
    category: str = "Uninterruptible Power Supply"
    topology: UpsTopology = Field(default=UpsTopology.DOUBLE_CONVERSION)
    capacity_kva: float = Field(default=250.0, gt=0.0, description="Rated apparent power capacity in kVA")
    capacity_kw: float = Field(default=250.0, gt=0.0, description="Rated real power capacity in kW (Unity PF = 1.0)")
    input_voltage: float = Field(default=480.0, description="Rectifier input nominal voltage")
    output_voltage: float = Field(default=480.0, description="Inverter output nominal voltage")
    phases: int = Field(default=3, description="3-phase 3W/4W")
    battery_runtime_minutes_at_100pct: float = Field(default=15.0, description="Battery autonomy backup duration at 100% full load in minutes")
    efficiency_pct: float = Field(default=96.5, description="Full load AC-to-AC double conversion efficiency")
    has_static_bypass: bool = Field(default=True, description="Solid-state static bypass switch for instantaneous fault clearing")
    has_maintenance_bypass: bool = Field(default=True, description="External mechanical wrap-around maintenance bypass cabinet (MBC)")

    # --- 1. Connectivity Terminals ---
    def get_input_ports(self) -> List[str]:
        return ["rectifier_in", "bypass_in", "gnd"]

    def get_output_ports(self) -> List[str]:
        return ["inverter_out", "neutral", "gnd"]

    # --- 2. Deterministic Sizing Calculations ---
    @property
    def input_full_load_amps(self) -> float:
        """Calculate maximum AC rectifier input current (including battery recharge)."""
        recharge_margin = 1.15
        total_kw = (self.capacity_kw / (self.efficiency_pct / 100.0)) * recharge_margin
        return round((total_kw * 1000.0) / (math.sqrt(3) * self.input_voltage), 2)

    @property
    def output_full_load_amps(self) -> float:
        """Calculate continuous AC output current to critical loads."""
        return round((self.capacity_kva * 1000.0) / (math.sqrt(3) * self.output_voltage), 2)

    def validate_rules(self) -> List[str]:
        warnings = []
        if self.capacity_kw > self.capacity_kva:
            warnings.append(f"UPS {self.tag}: kW ({self.capacity_kw}) cannot exceed kVA ({self.capacity_kva}).")
        return warnings

    # --- 3. Multi-View Visual Projections ---
    def compile_focused_dot(self) -> str:
        """Render UPS node with rectifier/inverter styling."""
        return (
            f'    UPS_{self.id} [\n'
            f'        id="node_ups_{self.id}",\n'
            f'        shape=none,\n'
            f'        label=<\n'
            f'        <TABLE BORDER="2" CELLBORDER="1" CELLSPACING="0" COLOR="#7C3AED" BGCOLOR="#FFFFFF">\n'
            f'            <TR><TD COLSPAN="2" BGCOLOR="#6D28D9" PORT="in">\n'
            f'                <FONT COLOR="WHITE" POINT-SIZE="10"><B>{html.escape(self.name.upper())}</B></FONT><BR/>\n'
            f'                <FONT COLOR="#DDD6FE" POINT-SIZE="8">[{self.topology.value} &bull; {self.capacity_kw} kW / {self.capacity_kva} kVA]</FONT>\n'
            f'            </TD></TR>\n'
            f'            <TR>\n'
            f'                <TD BGCOLOR="#F5F3FF" ALIGN="LEFT"><FONT POINT-SIZE="8"><B>INPUT:</B> {int(self.input_voltage)}V ({self.input_full_load_amps}A)</FONT></TD>\n'
            f'                <TD BGCOLOR="#F5F3FF" ALIGN="RIGHT" PORT="out"><FONT POINT-SIZE="8"><B>OUTPUT:</B> {int(self.output_voltage)}V ({self.output_full_load_amps}A)</FONT></TD>\n'
            f'            </TR>\n'
            f'            <TR><TD COLSPAN="2" BGCOLOR="#EDE9FE" ALIGN="CENTER">\n'
            f'                <FONT POINT-SIZE="7" COLOR="#5B21B6">Runtime: {self.battery_runtime_minutes_at_100pct} min @ 100% &bull; Eff: {self.efficiency_pct}%</FONT>\n'
            f'            </TD></TR>\n'
            f'        </TABLE>>\n'
            f'    ];\n'
        )

    def render_html_view(self) -> str:
        """Render native HTML UPS dashboard component."""
        return (
            f'<div class="rounded-xl border border-purple-700 bg-slate-950 p-4 shadow-xl space-y-3">'
            f'<div class="flex justify-between items-start border-b border-purple-900 pb-2.5">'
            f'<div>'
            f'<span class="bg-purple-950 text-purple-300 font-mono text-[10px] px-2 py-0.5 rounded uppercase font-semibold">{self.topology.value}</span>'
            f'<h3 class="font-bold text-white text-sm mt-1">{html.escape(self.name)}</h3>'
            f'</div>'
            f'<span class="bg-purple-600 text-white font-mono text-xs px-2.5 py-1 rounded shadow">{self.tag}</span>'
            f'</div>'
            f'<div class="grid grid-cols-2 gap-2 text-xs bg-slate-900/80 p-3 rounded-lg border border-slate-800">'
            f'<div>'
            f'<p class="text-slate-400 text-[11px]">Output Capacity</p>'
            f'<p class="font-mono text-cyan-400 font-bold">{self.capacity_kw} kW / {self.capacity_kva} kVA</p>'
            f'</div>'
            f'<div>'
            f'<p class="text-slate-400 text-[11px]">Battery Autonomy</p>'
            f'<p class="font-mono text-white font-bold">{self.battery_runtime_minutes_at_100pct} min @ Full Load</p>'
            f'</div>'
            f'</div>'
            f'<div class="flex justify-between items-center text-[11px] text-slate-400 font-mono pt-1">'
            f'<span>Output: <strong class="text-white">{self.output_full_load_amps} FLA</strong></span>'
            f'<span class="text-purple-400">Eff: {self.efficiency_pct}%</span>'
            f'</div>'
            f'</div>'
        )

    def compile_plantuml_sld(self) -> str:
        """Render PlantUML UPS symbol."""
        return (
            f'rectangle "{self.name}\\n<size:10>UPS {self.capacity_kw}kW ({self.battery_runtime_minutes_at_100pct}min)</size>" '
            f'as {self.id} <<ups>> #6D28D9;line:white;text:white\n'
        )
