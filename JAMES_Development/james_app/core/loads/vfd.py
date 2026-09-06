"""Variable Frequency Drive (VFD) Object Class."""

from typing import List, Optional
from pydantic import Field
from james_app.core.loads.base_load import LoadObject, LoadType


class VariableFrequencyDriveObject(LoadObject):
    """
    Variable Frequency Drive (VFD / Inverter Speed Controller).
    Controls motor speed, torque, and acceleration ramp profiles.
    Models continuous rated output current, input line harmonics (THD), carrier frequency,
    and optional 3-contactor maintenance bypass.
    """
    category: str = "Motor Control"
    load_type: LoadType = LoadType.VFD
    motor_hp: float = Field(default=25.0, description="Matched motor horsepower")
    rated_input_amps: float = Field(default=38.0, description="Rated continuous input current at 480V")
    rated_output_amps: float = Field(default=34.0, description="Continuous variable frequency output current in Amps")
    carrier_frequency_khz: float = Field(default=4.0, description="PWM carrier frequency in kHz (2, 4, 8, 12)")
    has_input_line_reactor: bool = Field(default=True, description="Includes 3% or 5% input line reactor for harmonic mitigation")
    has_bypass_contactor: bool = Field(default=False, description="Equipped with 3-contactor manual/auto across-the-line bypass")
    efficiency_pct: float = Field(default=97.5, description="Inverter electrical conversion efficiency")

    def validate_rules(self) -> List[str]:
        warnings = super().validate_rules()
        if self.rated_output_amps <= 0:
            warnings.append(f"VFD {self.tag}: Rated output current must be positive.")
        return warnings
