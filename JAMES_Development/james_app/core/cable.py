"""Cable / Conductor Run Object Class for electrical feeders and branch circuits."""

from enum import Enum
import html
import math
from typing import Any, Dict, List, Optional
from pydantic import Field
from james_app.core.base import BaseElectricalObject


class ConductorMaterial(str, Enum):
    COPPER = "Cu"
    ALUMINUM = "Al"


class InsulationType(str, Enum):
    THHN = "THHN"
    THWN_2 = "THWN-2"
    XHHW_2 = "XHHW-2"
    USE_2 = "USE-2"


class ConduitType(str, Enum):
    EMT = "EMT"
    PVC = "PVC"
    RMC = "RMC"
    MC_CABLE = "MC Cable"
    FREE_AIR = "Free Air"


# Standard 75°C Copper Ampacity (NEC Table 310.16)
NEC_COPPER_75C_AMPACITY = {
    "14 AWG": 20,
    "12 AWG": 25,
    "10 AWG": 35,
    "8 AWG": 50,
    "6 AWG": 65,
    "4 AWG": 85,
    "3 AWG": 100,
    "2 AWG": 115,
    "1 AWG": 130,
    "1/0 AWG": 150,
    "2/0 AWG": 175,
    "3/0 AWG": 200,
    "4/0 AWG": 230,
    "250 kcmil": 255,
    "300 kcmil": 285,
    "350 kcmil": 310,
    "400 kcmil": 335,
    "500 kcmil": 380,
    "600 kcmil": 420,
    "750 kcmil": 475,
}

# Approximate conductor resistance (Ohms per 1000 ft, Cu in steel conduit)
NEC_COPPER_OHMS_PER_1000FT = {
    "14 AWG": 3.1,
    "12 AWG": 2.0,
    "10 AWG": 1.2,
    "8 AWG": 0.78,
    "6 AWG": 0.49,
    "4 AWG": 0.31,
    "3 AWG": 0.25,
    "2 AWG": 0.19,
    "1 AWG": 0.15,
    "1/0 AWG": 0.12,
    "2/0 AWG": 0.10,
    "3/0 AWG": 0.077,
    "4/0 AWG": 0.062,
    "250 kcmil": 0.052,
    "350 kcmil": 0.038,
    "500 kcmil": 0.027,
}


class CableObject(BaseElectricalObject):
    """Physical conductor / cable run connecting equipment terminals."""
    category: str = "Conductor Run"
    gauge: str = Field(default="12 AWG", description="Wire gauge size (e.g. '12 AWG', '4/0 AWG', '500 kcmil')")
    material: ConductorMaterial = Field(default=ConductorMaterial.COPPER)
    insulation: InsulationType = Field(default=InsulationType.THHN)
    conduit: ConduitType = Field(default=ConduitType.EMT)
    length_ft: float = Field(default=50.0, ge=0.0, description="One-way conductor length in feet")
    sets: int = Field(default=1, ge=1, description="Number of parallel sets (e.g. 2x, 3x)")
    num_conductors: int = Field(default=3, ge=2, le=5, description="Active current-carrying conductors (2, 3, or 4)")
    from_node_id: str = Field(..., description="Source equipment ID")
    from_port_id: str = Field(default="out", description="Source terminal port ID")
    to_node_id: str = Field(..., description="Target equipment ID")
    to_port_id: str = Field(default="in", description="Target terminal port ID")
    load_amps: float = Field(default=16.0, ge=0.0, description="Operating design current in Amps")
    nominal_voltage: float = Field(default=120.0, ge=0.0, description="Operating line-to-neutral or line-to-line voltage")

    # --- 1. Connectivity Terminals ---
    def get_input_ports(self) -> List[str]:
        return [f"{self.from_node_id}:{self.from_port_id}"]

    def get_output_ports(self) -> List[str]:
        return [f"{self.to_node_id}:{self.to_port_id}"]

    # --- 2. Deterministic Sizing & Physics Calculations ---
    @property
    def base_ampacity(self) -> int:
        """Return base 75°C ampacity for the conductor size multiplied by parallel sets."""
        single_a = NEC_COPPER_75C_AMPACITY.get(self.gauge, 20)
        return single_a * self.sets

    def calculate_voltage_drop(self, is_three_phase: bool = False) -> Dict[str, float]:
        """
        Compute one-way estimated voltage drop based on Ohm's law and NEC resistance:
        Single-Phase: Vd = 2 * K * L * I / (sets * 1000)
        Three-Phase:  Vd = sqrt(3) * K * L * I / (sets * 1000)
        """
        r_per_1000 = NEC_COPPER_OHMS_PER_1000FT.get(self.gauge, 2.0) / self.sets
        multiplier = math.sqrt(3) if is_three_phase else 2.0
        
        # Vd = multiplier * (Length / 1000) * R * I
        v_drop = (multiplier * (self.length_ft / 1000.0) * r_per_1000 * self.load_amps)
        v_pct = (v_drop / self.nominal_voltage) * 100.0 if self.nominal_voltage > 0 else 0.0

        return {
            "drop_volts": round(v_drop, 2),
            "drop_pct": round(v_pct, 2),
            "max_recommended_pct": 3.0
        }

    def validate_rules(self) -> List[str]:
        """Verify NEC ampacity and branch voltage drop limits."""
        warnings = []
        if self.load_amps > self.base_ampacity:
            warnings.append(
                f"Cable {self.tag}: Design load ({self.load_amps}A) exceeds rated conductor ampacity ({self.base_ampacity}A for {self.sets}x {self.gauge})."
            )

        vd = self.calculate_voltage_drop(is_three_phase=(self.num_conductors >= 3 and self.nominal_voltage > 200))
        if vd["drop_pct"] > 3.0:
            warnings.append(
                f"Cable {self.tag}: Voltage drop ({vd['drop_pct']}%) exceeds NEC recommended 3.0% maximum for branch circuits ({vd['drop_volts']}V drop over {self.length_ft}ft)."
            )

        return warnings

    # --- 3. Multi-View Projections ---
    def compile_focused_dot(self) -> str:
        """Render cable connection edge in Graphviz DOT format."""
        sets_str = f"{self.sets}x " if self.sets > 1 else ""
        label = f"{sets_str}({self.num_conductors}-{self.gauge} {self.material.value}) | {self.length_ft:.0f} ft"
        from_spec = f"{self.from_node_id}:{self.from_port_id}" if self.from_port_id else self.from_node_id
        to_spec = f"{self.to_node_id}:{self.to_port_id}" if self.to_port_id else self.to_node_id
        
        return (
            f'    {from_spec} -> {to_spec} [\n'
            f'        id="{self.id}",\n'
            f'        label="{html.escape(label)}",\n'
            f'        fontsize=8,\n'
            f'        fontname="Helvetica",\n'
            f'        color="#334155"\n'
            f'    ];\n'
        )

    def render_html_view(self) -> str:
        """Render native HTML cable badge / specification card."""
        vd = self.calculate_voltage_drop()
        vd_color = "text-red-400" if vd["drop_pct"] > 3.0 else "text-emerald-400"
        sets_str = f"{self.sets}x " if self.sets > 1 else ""

        return (
            f'<div class="rounded-lg border border-slate-700 bg-slate-900 p-3 text-xs space-y-1.5 shadow">'
            f'<div class="flex justify-between items-center">'
            f'<span class="font-bold text-white">{html.escape(self.tag)}: {sets_str}{self.gauge} {self.material.value}</span>'
            f'<span class="px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 font-mono text-[10px]">{self.conduit.value}</span>'
            f'</div>'
            f'<div class="flex justify-between text-slate-400 text-[11px]">'
            f'<span>Length: {self.length_ft:.0f} ft &bull; Ampacity: {self.base_ampacity}A</span>'
            f'<span class="{vd_color} font-mono font-medium">Vd: {vd["drop_pct"]}% ({vd["drop_volts"]}V)</span>'
            f'</div>'
            f'<div class="text-slate-500 font-mono text-[10px] truncate">'
            f'{self.from_node_id}:{self.from_port_id} &rarr; {self.to_node_id}:{self.to_port_id}'
            f'</div>'
            f'</div>'
        )

    def compile_plantuml_sld(self) -> str:
        """Render PlantUML single-line connection edge."""
        sets_str = f"{self.sets}x " if self.sets > 1 else ""
        label = f"{sets_str}{self.gauge} ({self.length_ft:.0f}ft)"
        return f"{self.from_node_id} --> {self.to_node_id} : {label}\n"
