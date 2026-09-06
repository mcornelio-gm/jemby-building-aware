"""Base Circuit Breaker Object Class for embedded branch protection."""

from enum import Enum
import html
from typing import Any, List, Optional
from pydantic import Field
from james_app.core.base import BaseElectricalObject


class BreakerStatus(str, Enum):
    """Operational status of a circuit position."""
    ON = "ON"
    OFF = "OFF"
    TRIPPED = "TRIPPED"
    SPARE = "SPARE"
    SPACE = "SPACE"


class CircuitBreakerObject(BaseElectricalObject):
    """Base embedded circuit breaker object representing a branch protection unit."""
    category: str = "Protective Device"
    breaker_type_name: str = Field(default="Standard Circuit Breaker", description="Specific breaker technology name")
    slot_start: int = Field(..., description="Starting slot number")
    poles: int = Field(default=1, ge=1, le=3, description="Number of poles (1, 2, or 3)")
    occupied_slots: List[int] = Field(default_factory=list, description="All occupied slot IDs")
    amps: int = Field(default=20, ge=0, description="Continuous trip rating in Amps")
    frame_amps: int = Field(default=100, description="Breaker frame physical rating in Amps")
    aic_rating_ka: float = Field(default=10.0, description="Short-circuit interrupting capacity in kA")
    status: BreakerStatus = Field(default=BreakerStatus.ON, description="Breaker operational status")
    connected_phases: List[str] = Field(default_factory=list, description="Connected phase legs: ['A'], ['A', 'B'], etc.")
    target_load_id: Optional[str] = Field(default=None, description="Connected downstream load or asset ID")
    compatible_panel_categories: List[str] = Field(
        default_factory=lambda: ["Distribution Enclosure", "Main Power Distribution", "Branch Lighting & Receptacle Panel", "Sub-Distribution Panel", "Residential Loadcenter"],
        description="List of compatible panel categories"
    )

    def get_input_ports(self) -> List[str]:
        return [f"bus_stab_{s}" for s in self.occupied_slots]

    def get_output_ports(self) -> List[str]:
        slot_tag = "_".join(str(s) for s in self.occupied_slots)
        return [f"ckt_{slot_tag}"]

    def is_compatible_with(self, panel_category: str) -> bool:
        """Check if this breaker type is engineered for the specified panel category."""
        return panel_category in self.compatible_panel_categories

    def validate_rules(self) -> List[str]:
        errors = []
        if self.amps < 0:
            errors.append(f"Breaker {self.tag}: Trip rating cannot be negative ({self.amps}A).")
        if self.poles not in [1, 2, 3]:
            errors.append(f"Breaker {self.tag}: Invalid pole count ({self.poles}). Must be 1, 2, or 3.")
        if len(self.occupied_slots) != self.poles:
            errors.append(f"Breaker {self.tag}: Occupied slot count ({len(self.occupied_slots)}) does not match pole count ({self.poles}).")
        if self.status not in [BreakerStatus.SPARE, BreakerStatus.SPACE] and len(set(self.connected_phases)) != self.poles:
            errors.append(f"Breaker {self.tag}: Multi-pole breaker must span distinct phase stabs (got {self.connected_phases}).")
        return errors

    def compile_focused_dot(self) -> str:
        """Render a focused DOT box depiction of the breaker."""
        label_text = f"{self.tag}: {self.name} ({self.poles}P {self.amps}A)"
        status_color = "#16A34A" if self.status == BreakerStatus.ON else "#DC2626"
        return (
            f'    {self.id} [\n'
            f'        shape=record,\n'
            f'        style="rounded,filled", fillcolor="#F8FAFC", color="#334155",\n'
            f'        label="<in> Line ({self.poles}P)|<bkr> {html.escape(label_text)}\\n[{self.breaker_type_name}] |<out> Load ({status_color})"\n'
            f'    ];\n'
        )

    def render_html_view(self) -> str:
        """Render native HTML badge / slot row."""
        slot_tag = ",".join(str(s) for s in self.occupied_slots)
        if self.status == BreakerStatus.SPARE:
            return f'<div class="bg-amber-100 text-amber-900 border border-amber-300 rounded px-2 py-1 text-xs font-mono">[SPARE] {html.escape(self.name)} :{slot_tag}</div>'
        elif self.status == BreakerStatus.SPACE:
            return f'<div class="bg-slate-100 text-slate-400 border border-slate-200 rounded px-2 py-1 text-xs font-mono">[SPACE] Blank</div>'
        else:
            return (
                f'<div class="bg-slate-800 text-white border border-slate-700 rounded px-2.5 py-1.5 text-xs flex justify-between items-center shadow-sm">'
                f'<span class="font-bold text-cyan-400 font-mono">[{self.status.value}] {slot_tag}</span>'
                f'<span class="font-medium text-slate-200 truncate mx-2">{html.escape(self.name)}</span>'
                f'<span class="bg-indigo-900/80 text-indigo-300 px-1.5 py-0.5 rounded font-mono text-[10px]">{self.poles}P {self.amps}A</span>'
                f'</div>'
            )

    def compile_plantuml_sld(self) -> str:
        """Render PlantUML single-line schematic element."""
        return f"component [{self.tag}\\n{self.amps}A {self.poles}P\\n{self.breaker_type_name}] as {self.id}\n"
