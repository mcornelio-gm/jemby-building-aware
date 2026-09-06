"""Electric Motor & Rotating Machinery Object Class."""

from enum import Enum
import math
from typing import List, Optional
from pydantic import Field
from james_app.core.loads.base_load import LoadObject, LoadType


class NemaMotorDesign(str, Enum):
    DESIGN_B = "Design B (Standard Torque)"
    DESIGN_C = "Design C (High Starting Torque)"
    DESIGN_D = "Design D (High Slip / Crane)"


# Standard 460V 3-Phase Induction Motor FLA (NEC Table 430.250)
NEC_460V_MOTOR_FLA = {
    1.0: 1.8,
    2.0: 3.4,
    3.0: 4.8,
    5.0: 7.6,
    7.5: 11.0,
    10.0: 14.0,
    15.0: 21.0,
    20.0: 27.0,
    25.0: 34.0,
    30.0: 40.0,
    40.0: 52.0,
    50.0: 65.0,
    60.0: 77.0,
    75.0: 96.0,
    100.0: 124.0,
    125.0: 156.0,
    150.0: 180.0,
    200.0: 240.0,
}


class ElectricMotorObject(LoadObject):
    """
    3-Phase / 1-Phase Induction Electric Motor.
    Models motor nameplate horsepower (HP), NEC Table 430.250 full-load current (FLA),
    locked-rotor inrush (LRA per NEMA Code Letter), overload relay sizing (NEC 430.32),
    and branch short-circuit protection (NEC 430.52).
    """
    category: str = "Rotating Machinery"
    load_type: LoadType = LoadType.MOTOR
    horsepower_hp: float = Field(default=25.0, gt=0.0, description="Nameplate shaft mechanical rating in HP")
    voltage: float = Field(default=480.0, description="Rated motor terminal voltage")
    phases: int = Field(default=3, description="3-phase or 1-phase")
    rpm: int = Field(default=1750, description="Nominal synchronous operating speed in RPM")
    nema_design: NemaMotorDesign = Field(default=NemaMotorDesign.DESIGN_B)
    nema_code_letter: str = Field(default="G", description="NEMA Locked-Rotor Inrush Code Letter (e.g. G = 5.6-6.3 kVA/HP)")
    efficiency_pct: float = Field(default=93.6, description="NEMA Premium efficiency percentage")
    service_factor: float = Field(default=1.15, description="Motor continuous overload Service Factor (SF 1.0 or 1.15)")

    # --- Deterministic NEC 430 Sizing ---
    @property
    def nec_table_fla(self) -> float:
        """Lookup or compute standard NEC Table 430.250 full load current in Amps."""
        if self.voltage == 480.0 and self.horsepower_hp in NEC_460V_MOTOR_FLA:
            return NEC_460V_MOTOR_FLA[self.horsepower_hp]
        # Mathematical approximation: (HP * 746) / (sqrt(3) * V * Eff * PF)
        return round((self.horsepower_hp * 746.0) / (math.sqrt(3) * self.voltage * (self.efficiency_pct / 100.0) * self.power_factor), 2)

    @property
    def locked_rotor_amps(self) -> float:
        """Estimate locked-rotor starting current (LRA ~ 6x FLA for NEMA Code G)."""
        return round(self.nec_table_fla * 6.0, 1)

    @property
    def branch_conductor_ampacity(self) -> float:
        """NEC 430.22 branch conductor sizing: 125% of NEC Table FLA."""
        return round(self.nec_table_fla * 1.25, 2)

    @property
    def max_breaker_inverse_time_amps(self) -> float:
        """NEC 430.52 inverse-time breaker max rating: 250% of NEC Table FLA."""
        return round(self.nec_table_fla * 2.50, 1)

    def validate_rules(self) -> List[str]:
        warnings = super().validate_rules()
        if self.service_factor < 1.0 or self.service_factor > 1.25:
            warnings.append(f"Motor {self.tag}: Unusual Service Factor ({self.service_factor}). Typical is 1.0 or 1.15.")
        return warnings
