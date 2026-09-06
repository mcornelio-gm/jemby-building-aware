"""HVAC Equipment & Packaged Chiller Object Class (NEC 440)."""

from typing import List, Optional
from pydantic import Field
from james_app.core.loads.base_load import LoadObject, LoadType


class HvacEquipmentObject(LoadObject):
    """
    HVAC Packaged Unit / Chiller / Rooftop Unit (NEC Article 440).
    Incorporates hermetic refrigerant motor-compressors, condenser fans, and electric reheat.
    Models manufacturer nameplate Minimum Circuit Ampacity (MCA) for conductor sizing
    and Maximum Overcurrent Protective Device (MOCP) for circuit breaker selection.
    """
    category: str = "Mechanical / HVAC"
    load_type: LoadType = LoadType.HVAC
    tonnage: float = Field(default=50.0, description="Cooling refrigeration capacity in Tons (12,000 BTU/hr per Ton)")
    mca_amps: float = Field(default=84.5, gt=0.0, description="Nameplate Minimum Circuit Ampacity (conductor sizing per NEC 440.32)")
    mocp_amps: int = Field(default=125, ge=15, description="Nameplate Maximum Overcurrent Protective Device rating in Amps")
    compressor_rla: float = Field(default=58.0, description="Hermetic compressor Rated Load Amps (RLA)")
    compressor_lra: float = Field(default=290.0, description="Compressor Locked Rotor Amps (LRA)")
    fan_motor_fla: float = Field(default=12.0, description="Condenser fan motor total Full Load Amps")
    voltage: float = Field(default=480.0, description="Operating line voltage")
    phases: int = Field(default=3, description="Phase configuration (3-phase)")

    def validate_rules(self) -> List[str]:
        """Perform NEC 440 HVAC rules checks."""
        warnings = super().validate_rules()
        if self.mca_amps >= self.mocp_amps:
            warnings.append(
                f"HVAC Unit {self.tag}: Minimum Circuit Ampacity ({self.mca_amps}A) must be less than Maximum OCPD ({self.mocp_amps}A)."
            )
        return warnings
