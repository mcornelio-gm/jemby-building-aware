"""Battery Energy Storage System (BESS) Object Class."""

from typing import List, Optional
from pydantic import Field
from james_app.core.sources.base_source import PowerSourceObject, SourceType


class BatteryEnergyStorageObject(PowerSourceObject):
    """
    Battery Energy Storage System (BESS).
    Electrochemical energy storage system (Lithium-Ion / LFP) coupled with a bidirectional 4-quadrant inverter.
    Provides peak shaving, frequency regulation, microgrid islanding, and backup energy buffering.
    """
    category: str = "Energy Storage"
    source_type: SourceType = SourceType.BATTERY_BESS
    battery_chemistry: str = Field(default="Lithium Iron Phosphate (LFP)", description="Battery cell chemistry")
    energy_capacity_kwh: float = Field(default=1000.0, gt=0.0, description="Nameplate total energy storage in kWh")
    usable_capacity_kwh: float = Field(default=900.0, description="Usable energy storage depth (e.g. 90% DoD)")
    power_rating_kw: float = Field(default=500.0, description="Maximum continuous charge / discharge power in kW")
    c_rate: float = Field(default=0.5, description="Continuous discharge C-Rate (e.g. 0.5C for 2-hour duration)")
    round_trip_efficiency_pct: float = Field(default=89.0, description="AC-to-AC round trip cycle efficiency percentage")
    state_of_charge_pct: float = Field(default=85.0, ge=0.0, le=100.0, description="Current real-time battery state of charge (SOC %)")
    has_microgrid_islanding: bool = Field(default=True, description="Capable of seamless grid disconnect and black start")

    @property
    def duration_hours(self) -> float:
        """Calculate continuous full-power discharge duration in hours."""
        if self.power_rating_kw > 0:
            return round(self.usable_capacity_kwh / self.power_rating_kw, 2)
        return 0.0

    def validate_rules(self) -> List[str]:
        """Perform BESS sizing validation."""
        warnings = super().validate_rules()
        if self.usable_capacity_kwh > self.energy_capacity_kwh:
            warnings.append(f"BESS {self.tag}: Usable capacity ({self.usable_capacity_kwh} kWh) cannot exceed nameplate capacity ({self.energy_capacity_kwh} kWh).")
        return warnings
