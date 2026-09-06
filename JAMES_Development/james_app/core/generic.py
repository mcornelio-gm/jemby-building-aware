"""Generic / Placeholder Electrical Object Class.

Used as a versatile placeholder for unknown, future, or custom equipment
before being promoted or converted to a concrete specialized class.
"""

from enum import Enum
import html
from typing import Any, Dict, List, Optional
from pydantic import Field
from james_app.core.base import BaseElectricalObject


class GenericKind(str, Enum):
    """Broad category of the placeholder object."""
    LOAD = "Generic Load"
    PANEL = "Future Sub-Panel"
    SWITCH = "Disconnect / Switch"
    SOURCE = "Power Source"
    TRANSFORMER = "Transformer"
    MOTOR = "Motor / Machinery"
    CUSTOM = "Custom Equipment"


class GenericElectricalObject(BaseElectricalObject):
    """Versatile placeholder electrical object with promotion capabilities."""
    category: str = "Placeholder / Generic"
    generic_kind: GenericKind = Field(default=GenericKind.LOAD, description="High-level archetype")
    voltage: Optional[str] = Field(default="120V", description="Nominal voltage (e.g. '120V', '208V 3Ø', '480V')")
    current_amps: float = Field(default=0.0, ge=0.0, description="Operating current in Amps")
    power_kva: float = Field(default=0.0, ge=0.0, description="Apparent power in kVA")
    power_kw: float = Field(default=0.0, ge=0.0, description="Real power in kW")
    power_factor: float = Field(default=0.90, ge=0.0, le=1.0, description="Power factor (0.0 to 1.0)")
    input_terminals: List[str] = Field(default_factory=lambda: ["in", "L1", "L2"], description="Custom input port tags")
    output_terminals: List[str] = Field(default_factory=lambda: ["out"], description="Custom output port tags")
    custom_attributes: Dict[str, Any] = Field(default_factory=dict, description="Arbitrary parameters")

    # --- 1. Connectivity Terminals ---
    def get_input_ports(self) -> List[str]:
        return self.input_terminals

    def get_output_ports(self) -> List[str]:
        return self.output_terminals

    # --- 2. Deterministic Rules ---
    def validate_rules(self) -> List[str]:
        warnings = []
        if self.current_amps < 0:
            warnings.append(f"Generic Object {self.tag}: Current cannot be negative ({self.current_amps}A).")
        if self.power_kva < 0:
            warnings.append(f"Generic Object {self.tag}: kVA cannot be negative ({self.power_kva} kVA).")
        return warnings

    # --- 3. Promotion / Class Conversion Helpers ---
    def promote_to_panel(self, total_spaces: int = 42, mains_amps: int = 400) -> "PanelboardObject":
        """Promote this placeholder into a full PanelboardObject."""
        from james_app.core.panel import PanelboardObject, SystemType, MainsType
        
        sys_type = SystemType.THREE_PHASE_208Y_120V if "208" in str(self.voltage) else SystemType.SINGLE_PHASE_120_240V
        return PanelboardObject.create_empty(
            panel_id=self.id,
            tag=self.tag,
            name=self.name,
            total_spaces=total_spaces,
            mains_rating_amps=int(self.current_amps) if self.current_amps > 0 else mains_amps,
            system_type=sys_type,
            mains_type=MainsType.MCB
        )

    def promote_to_breaker(self, slot_start: int = 1, poles: int = 1) -> "CircuitBreakerObject":
        """Promote this placeholder into a CircuitBreakerObject."""
        from james_app.core.breaker import CircuitBreakerObject, BreakerStatus
        
        occupied = [slot_start + (i * 2) for i in range(poles)]
        return CircuitBreakerObject(
            id=self.id,
            tag=self.tag,
            name=self.name,
            slot_start=slot_start,
            poles=poles,
            occupied_slots=occupied,
            amps=int(self.current_amps) if self.current_amps > 0 else 20,
            status=BreakerStatus.ON,
            connected_phases=["A" for _ in range(poles)]
        )

    # --- 4. Multi-View Projections ---
    def compile_focused_dot(self) -> str:
        """Render a placeholder box in Graphviz DOT format with dashed styling."""
        v_str = f" ({self.voltage})" if self.voltage else ""
        kva_str = f"<br/><font point-size='8' color='#64748B'>{self.power_kva} kVA | {self.current_amps}A</font>" if self.power_kva or self.current_amps else ""
        
        return (
            f'    {self.id} [\n'
            f'        shape=box,\n'
            f'        style="rounded,dashed,filled", fillcolor="#F8FAFC", color="#64748B", penwidth=1.5,\n'
            f'        label=<\n'
            f'            <font point-size="8" color="#6366F1"><b>[{self.generic_kind.value.upper()}]</b></font><br/>\n'
            f'            <b>{html.escape(self.name)}{html.escape(v_str)}</b>\n'
            f'            {kva_str}\n'
            f'        >\n'
            f'    ];\n'
        )

    def render_html_view(self) -> str:
        """Render native HTML placeholder card with promotion trigger."""
        return (
            f'<div class="rounded-xl border border-dashed border-indigo-700 bg-slate-900/90 p-4 text-xs space-y-2 shadow-lg">'
            f'<div class="flex justify-between items-center">'
            f'<span class="px-2 py-0.5 rounded bg-indigo-950 text-indigo-400 border border-indigo-800 text-[10px] font-semibold">{self.generic_kind.value}</span>'
            f'<span class="font-mono text-slate-400 text-[11px]">{html.escape(self.tag)}</span>'
            f'</div>'
            f'<h4 class="text-sm font-bold text-white">{html.escape(self.name)}</h4>'
            f'<div class="grid grid-cols-2 gap-2 text-slate-300 text-[11px]">'
            f'<div>Voltage: <span class="font-semibold text-white">{self.voltage}</span></div>'
            f'<div>Current: <span class="font-semibold text-white">{self.current_amps}A</span></div>'
            f'<div>Power: <span class="font-semibold text-white">{self.power_kva} kVA</span></div>'
            f'<div>Power Factor: <span class="font-semibold text-white">{self.power_factor}</span></div>'
            f'</div>'
            f'<div class="pt-2 border-t border-slate-800 flex justify-between items-center text-[10px] text-slate-400">'
            f'<span>Status: Ready for Class Promotion</span>'
            f'<span class="text-indigo-400 font-semibold cursor-pointer hover:underline">&rarr; Promote Class</span>'
            f'</div>'
            f'</div>'
        )

    def compile_plantuml_sld(self) -> str:
        """Render generic PlantUML component."""
        return f"node \"{self.name}\\n[{self.generic_kind.value}]\\n{self.voltage}\" as {self.id} <<placeholder>>\n"
