"""Emergency / Standby Diesel Generator Object Class."""

from enum import Enum
from typing import List, Optional
from pydantic import Field
from james_app.core.sources.base_source import PowerSourceObject, SourceType


class FuelType(str, Enum):
    DIESEL = "Diesel #2"
    NATURAL_GAS = "Natural Gas"
    LP_PROPANE = "Liquid Propane"
    DUAL_FUEL = "Dual Fuel (NG / Diesel)"


class DieselGeneratorObject(PowerSourceObject):
    """
    Emergency / Standby Diesel Generator Set.
    Engineered for backup life-safety and emergency power (NEC 700 / 701, NFPA 110 Type 10).
    Features quick 10-second start response, sub-base UL 142 fuel tank autonomy, and digital isochronous governor.
    """
    category: str = "Emergency Generation"
    source_type: SourceType = SourceType.GENERATOR
    fuel_type: FuelType = Field(default=FuelType.DIESEL)
    fuel_tank_capacity_gallons: float = Field(default=500.0, description="Sub-base belly tank capacity in Gallons")
    fuel_burn_rate_gph: float = Field(default=52.0, description="Full load fuel consumption in gallons/hour")
    starting_time_seconds: float = Field(default=10.0, description="Time to reach rated voltage & frequency (<=10s for NFPA 110 Class 10)")
    sound_attenuated_enclosure_level: str = Field(default="Level 2 (72 dBA @ 23 ft)", description="Acoustic weather housing rating")
    is_life_safety_rated: bool = Field(default=True, description="Designated for NEC 700 Emergency Life Safety power")

    @property
    def fuel_autonomy_hours(self) -> float:
        """Calculate continuous full-load runtime in hours based on on-site fuel storage."""
        if self.fuel_burn_rate_gph > 0:
            return round(self.fuel_tank_capacity_gallons / self.fuel_burn_rate_gph, 1)
        return 0.0

    def validate_rules(self) -> List[str]:
        """Perform NFPA 110 runtime and starting safety checks."""
        warnings = super().validate_rules()
        if self.is_life_safety_rated and self.starting_time_seconds > 10.0:
            warnings.append(
                f"Generator {self.tag}: NEC 700 / NFPA 110 Emergency life safety requires transfer power within 10 seconds (configured for {self.starting_time_seconds}s)."
            )
        if self.is_life_safety_rated and self.fuel_autonomy_hours < 2.0:
            warnings.append(
                f"Generator {self.tag}: On-site fuel autonomy ({self.fuel_autonomy_hours}h) is less than NFPA minimum 2.0 hours."
            )
        return warnings
