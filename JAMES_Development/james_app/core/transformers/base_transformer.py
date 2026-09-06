"""Base Transformer Object Class for electrical voltage transformation."""

from enum import Enum
import html
import math
from typing import Any, Dict, List, Optional
from pydantic import Field
from james_app.core.base import BaseElectricalObject


class WindingConfiguration(str, Enum):
    """Transformer primary/secondary winding connection topologies."""
    DELTA_WYE = "Delta - Wye"
    DELTA_DELTA = "Delta - Delta"
    WYE_WYE = "Wye - Wye"
    WYE_DELTA = "Wye - Delta"
    SINGLE_PHASE = "Single Phase"


class CoolingType(str, Enum):
    """Transformer cooling classification."""
    ANN_AIR = "ANN (Dry Type Natural Air)"
    AF_FORCED_AIR = "AF (Forced Air)"
    ONAN_OIL = "ONAN (Mineral Oil Natural)"
    KNAN_LESS_FLAMMABLE = "KNAN (FR3 / Synthetic Fluid)"


STANDARD_KVA_RATINGS = [
    15.0, 30.0, 45.0, 75.0, 112.5, 150.0, 225.0, 300.0, 500.0, 750.0, 1000.0, 1500.0, 2000.0, 2500.0, 3750.0, 5000.0
]


class TransformerObject(BaseElectricalObject):
    """Base Electrical Transformer Digital Twin Representation Model."""
    category: str = "Transformer"
    transformer_type_name: str = Field(default="Distribution Transformer", description="Specific transformer technology name")
    kva_rating: float = Field(default=75.0, gt=0.0, description="Apparent power capacity in kVA")
    primary_voltage: float = Field(default=480.0, gt=0.0, description="Nominal primary line-to-line voltage in Volts")
    secondary_voltage: float = Field(default=208.0, gt=0.0, description="Nominal secondary line-to-line voltage in Volts")
    secondary_neutral_voltage: Optional[float] = Field(default=120.0, description="Secondary line-to-neutral voltage in Volts")
    primary_phases: int = Field(default=3, ge=1, le=3, description="Number of primary phases (1 or 3)")
    secondary_phases: int = Field(default=3, ge=1, le=3, description="Number of secondary phases (1 or 3)")
    winding_config: WindingConfiguration = Field(default=WindingConfiguration.DELTA_WYE)
    cooling_type: CoolingType = Field(default=CoolingType.ANN_AIR)
    impedance_pct_z: float = Field(default=5.75, ge=1.0, le=15.0, description="Nameplate percent impedance (%Z)")
    temperature_rise_c: int = Field(default=150, description="Winding temperature rise in °C (80, 115, 150)")
    tap_setting_pct: float = Field(default=0.0, description="Primary voltage tap adjustment (e.g. +2.5%, -2.5%, -5.0%)")
    k_factor: int = Field(default=1, ge=1, le=20, description="Harmonic K-Factor rating (K-1, K-4, K-13, K-20)")
    efficiency_pct: float = Field(default=98.5, ge=80.0, le=99.9, description="DOE 2016 full load efficiency percentage")
    upstream_feed_id: Optional[str] = Field(default=None, description="Upstream feeding equipment ID")
    downstream_panel_id: Optional[str] = Field(default=None, description="Direct downstream panelboard or switchboard ID")

    # --- 1. Connectivity Terminals ---
    def get_input_ports(self) -> List[str]:
        """Primary line connection terminals."""
        if self.primary_phases == 1:
            return ["H1", "H2"]
        return ["H1", "H2", "H3", "GND"]

    def get_output_ports(self) -> List[str]:
        """Secondary load connection terminals."""
        if self.secondary_phases == 1:
            return ["X1", "X2", "X0"]
        if self.winding_config in [WindingConfiguration.DELTA_WYE, WindingConfiguration.WYE_WYE]:
            return ["X1", "X2", "X3", "X0", "GND"]
        return ["X1", "X2", "X3", "GND"]

    # --- 2. Deterministic Electrical Sizing & Physics Calculations ---
    @property
    def primary_full_load_amps(self) -> float:
        """Calculate primary full load current (FLA) in Amps."""
        if self.primary_phases == 3:
            return round((self.kva_rating * 1000.0) / (math.sqrt(3) * self.primary_voltage), 2)
        return round((self.kva_rating * 1000.0) / self.primary_voltage, 2)

    @property
    def secondary_full_load_amps(self) -> float:
        """Calculate secondary full load current (FLA) in Amps."""
        if self.secondary_phases == 3:
            return round((self.kva_rating * 1000.0) / (math.sqrt(3) * self.secondary_voltage), 2)
        return round((self.kva_rating * 1000.0) / self.secondary_voltage, 2)

    @property
    def max_secondary_short_circuit_amps(self) -> float:
        """
        Calculate secondary bolted short-circuit fault current:
        I_sc = Secondary_FLA / (%Z / 100)
        """
        sec_fla = (self.kva_rating * 1000.0) / (math.sqrt(3) * self.secondary_voltage if self.secondary_phases == 3 else self.secondary_voltage)
        return round(sec_fla / (self.impedance_pct_z / 100.0), 1)

    def calculate_nec_450_max_primary_protection(self, has_secondary_protection: bool = True) -> Dict[str, float]:
        """
        Calculate maximum primary overcurrent protective device (OCPD) sizing per NEC Table 450.3(B):
        - With secondary protection (<=125%): Primary OCPD max = 250% of Primary FLA.
        - Without secondary protection: Primary OCPD max = 125% of Primary FLA (or next standard size).
        """
        multiplier = 2.50 if has_secondary_protection else 1.25
        max_amps = round(self.primary_full_load_amps * multiplier, 1)
        return {
            "primary_fla": self.primary_full_load_amps,
            "multiplier": multiplier,
            "max_primary_ocpd_amps": max_amps,
            "secondary_fla": self.secondary_full_load_amps,
            "max_secondary_ocpd_amps": round(self.secondary_full_load_amps * 1.25, 1)
        }

    # --- 3. Deterministic Domain & Code Rules ---
    def validate_rules(self) -> List[str]:
        """Verify NEC 450 transformer rules and physical consistency."""
        warnings = []
        if self.primary_voltage <= self.secondary_voltage:
            warnings.append(
                f"Transformer {self.tag}: Primary voltage ({self.primary_voltage}V) is less than or equal to secondary voltage ({self.secondary_voltage}V) on a step-down unit."
            )
        if self.impedance_pct_z < 1.5 or self.impedance_pct_z > 10.0:
            warnings.append(
                f"Transformer {self.tag}: Unusual impedance %Z ({self.impedance_pct_z}%). Standard distribution transformers range between 2.0% and 7.5%."
            )
        return warnings

    # --- 4. Multi-View Visual Projections ---
    def compile_focused_dot(self) -> str:
        """Render a focused Graphviz DOT node depicting the transformer with primary/secondary terminals."""
        pri_label = f"{int(self.primary_voltage)}V {self.primary_phases}Ø"
        sec_v = f"{int(self.secondary_voltage)}/{int(self.secondary_neutral_voltage)}V" if self.secondary_neutral_voltage else f"{int(self.secondary_voltage)}V"
        sec_label = f"{sec_v} {self.secondary_phases}Ø"
        
        return (
            f'    Transformer_{self.id} [\n'
            f'        id="node_xfmr_{self.id}",\n'
            f'        shape=none,\n'
            f'        label=<\n'
            f'        <TABLE BORDER="2" CELLBORDER="1" CELLSPACING="0" COLOR="#4338CA" BGCOLOR="#FFFFFF">\n'
            f'            <TR><TD COLSPAN="2" BGCOLOR="#3730A3" PORT="pri">\n'
            f'                <FONT COLOR="WHITE" POINT-SIZE="10"><B>{html.escape(self.name.upper())}</B></FONT><BR/>\n'
            f'                <FONT COLOR="#C7D2FE" POINT-SIZE="8">[{self.kva_rating} kVA &bull; %Z={self.impedance_pct_z}%]</FONT>\n'
            f'            </TD></TR>\n'
            f'            <TR>\n'
            f'                <TD BGCOLOR="#EEF2FF" ALIGN="LEFT"><FONT POINT-SIZE="8"><B>PRI: {pri_label}</B><BR/>FLA: {self.primary_full_load_amps}A</FONT></TD>\n'
            f'                <TD BGCOLOR="#EEF2FF" ALIGN="RIGHT" PORT="sec"><FONT POINT-SIZE="8"><B>SEC: {sec_label}</B><BR/>FLA: {self.secondary_full_load_amps}A</FONT></TD>\n'
            f'            </TR>\n'
            f'            <TR><TD COLSPAN="2" BGCOLOR="#E0E7FF" ALIGN="CENTER">\n'
            f'                <FONT POINT-SIZE="7" COLOR="#3730A3">I_sc Available: {self.max_secondary_short_circuit_amps:,.0f}A &bull; {self.winding_config.value}</FONT>\n'
            f'            </TD></TR>\n'
            f'        </TABLE>>\n'
            f'    ];\n'
        )

    def render_html_view(self) -> str:
        """Render native HTML interactive component card."""
        pri_label = f"{int(self.primary_voltage)}V {self.primary_phases}Ø"
        sec_v = f"{int(self.secondary_voltage)}/{int(self.secondary_neutral_voltage)}V" if self.secondary_neutral_voltage else f"{int(self.secondary_voltage)}V"
        sec_label = f"{sec_v} {self.secondary_phases}Ø"

        return (
            f'<div class="rounded-xl border border-indigo-700 bg-slate-950 p-4 shadow-xl space-y-3">'
            f'<div class="flex justify-between items-start border-b border-indigo-900 pb-2.5">'
            f'<div>'
            f'<span class="bg-indigo-900 text-indigo-200 font-mono text-[10px] px-2 py-0.5 rounded uppercase font-semibold">{self.transformer_type_name}</span>'
            f'<h3 class="font-bold text-white text-sm mt-1">{html.escape(self.name)}</h3>'
            f'</div>'
            f'<span class="bg-indigo-600 text-white font-mono text-xs px-2.5 py-1 rounded shadow">{self.tag}</span>'
            f'</div>'
            f'<div class="grid grid-cols-2 gap-3 bg-slate-900/80 p-3 rounded-lg border border-slate-800 text-xs">'
            f'<div>'
            f'<p class="text-slate-400 font-semibold text-[11px]">Primary ({pri_label})</p>'
            f'<p class="font-mono text-cyan-400 font-bold">{self.primary_full_load_amps} FLA</p>'
            f'</div>'
            f'<div>'
            f'<p class="text-slate-400 font-semibold text-[11px]">Secondary ({sec_label})</p>'
            f'<p class="font-mono text-cyan-400 font-bold">{self.secondary_full_load_amps} FLA</p>'
            f'</div>'
            f'</div>'
            f'<div class="flex justify-between items-center text-[11px] text-slate-400 font-mono pt-1">'
            f'<span>Rating: <strong class="text-white">{self.kva_rating} kVA</strong> (%Z: {self.impedance_pct_z}%)</span>'
            f'<span class="text-indigo-300">I_sc: {self.max_secondary_short_circuit_amps:,.0f}A</span>'
            f'</div>'
            f'</div>'
        )

    def compile_plantuml_sld(self) -> str:
        """Render standard Single-Line Diagram transformer symbol (two intersecting circles)."""
        return (
            f'rectangle "{self.name}\\n<size:10>{self.kva_rating} kVA | {int(self.primary_voltage)}V:{int(self.secondary_voltage)}V</size>" '
            f'as {self.id} <<transformer>> #4338CA;line:white;text:white\n'
        )
