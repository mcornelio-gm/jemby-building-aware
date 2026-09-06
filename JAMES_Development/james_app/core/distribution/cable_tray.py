"""Cable Tray Raceway System Object Class (NEC 392)."""

from enum import Enum
from typing import List, Optional
from pydantic import Field
from james_app.core.base import BaseElectricalObject


class CableTrayType(str, Enum):
    LADDER = "Ladder Cable Tray (Maximum Ventilation)"
    VENTILATED_TROUGH = "Ventilated Trough"
    SOLID_BOTTOM = "Solid Bottom (EMI Shielding)"
    WIRE_MESH_BASKET = "Wire Mesh Basket (Data / Telecom)"


class CableTrayObject(BaseElectricalObject):
    """
    Cable Tray Support & Raceway System (NEC Article 392).
    Models continuous structural raceway supporting bulk power feeders, multi-conductor cables,
    and control wiring with cross-sectional fill calculations.
    """
    category: str = "Raceway System"
    tray_type: CableTrayType = Field(default=CableTrayType.LADDER)
    width_inches: float = Field(default=24.0, ge=6.0, le=48.0, description="Tray internal width in inches (6, 12, 18, 24, 30, 36, 42, 48)")
    depth_inches: float = Field(default=6.0, ge=3.0, le=8.0, description="Tray side rail loading depth in inches (4, 6)")
    length_ft: float = Field(default=80.0, ge=1.0, description="Total continuous run distance in feet")
    max_fill_area_sq_in: float = Field(default=144.0, description="Total usable cross-sectional area")
    current_fill_pct: float = Field(default=45.0, ge=0.0, le=100.0, description="Calculated cable fill percentage (NEC 392 max 50% for control, single-layer for large power)")

    def get_input_ports(self) -> List[str]:
        return ["tray_start"]

    def get_output_ports(self) -> List[str]:
        return ["tray_end"]

    def validate_rules(self) -> List[str]:
        warnings = []
        if self.current_fill_pct > 50.0:
            warnings.append(f"Cable Tray {self.tag}: Calculated cable fill ({self.current_fill_pct:.1f}%) exceeds NEC 392 recommended 50% limit.")
        return warnings

    def compile_focused_dot(self) -> str:
        return f'    Tray_{self.id} [shape=record, style="filled", fillcolor="#F3F4F6", color="#6B7280", label="TRAY: {self.name}|{self.width_inches:.0f}\\"W x {self.depth_inches:.0f}\\"D ({self.current_fill_pct:.0f}% Fill)"];\n'

    def render_html_view(self) -> str:
        return f'<div class="p-2 border border-slate-700 bg-slate-900 rounded text-xs text-slate-300"><strong>Tray {self.tag}</strong>: {self.width_inches:.0f}"W {self.tray_type.value.split()[0]} ({self.current_fill_pct:.0f}% Fill)</div>'

    def compile_plantuml_sld(self) -> str:
        return f'node "{self.name}\\nTray {self.width_inches}\\"W" as {self.id} <<tray>>\n'
