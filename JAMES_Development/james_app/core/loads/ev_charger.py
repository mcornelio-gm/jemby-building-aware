"""Electric Vehicle Supply Equipment (EVSE) Charging Station Object Class."""

from enum import Enum
from typing import List, Optional
from pydantic import Field
from james_app.core.loads.base_load import LoadObject, LoadType


class EvChargerLevel(str, Enum):
    LEVEL_2_AC = "Level 2 AC (208V/240V, 32A-80A)"
    DC_FAST_CHARGER = "DC Fast Charger Level 3 (480V 3Ø, 50kW-350kW)"


class EvChargingStationObject(LoadObject):
    """
    Electric Vehicle Supply Equipment (EVSE) Charging Station (NEC 625).
    Continuous commercial or residential EV charging station with smart energy management,
    load-shedding controls, and ground-fault protection.
    """
    category: str = "EV Infrastructure"
    load_type: LoadType = LoadType.EV_CHARGER
    charger_level: EvChargerLevel = Field(default=EvChargerLevel.LEVEL_2_AC)
    charging_ports_count: int = Field(default=2, ge=1, description="Simultaneous charging vehicle plug count")
    output_power_kw: float = Field(default=19.2, gt=0.0, description="Maximum total continuous charging power in kW")
    rated_current_amps: float = Field(default=40.0, ge=16.0, description="Continuous current per port in Amps")
    is_continuous: bool = True  # EV chargers are 100% continuous duty per NEC 625.41 (125% breaker sizing)
    has_smart_load_management: bool = Field(default=True, description="Dynamically throttles charging power during building peak demand")

    @property
    def required_breaker_amps(self) -> int:
        """NEC 625.41 Overcurrent Protection: 125% of maximum continuous rating."""
        amps_125 = self.rated_current_amps * 1.25
        for std in [20, 30, 40, 50, 60, 70, 80, 100, 125, 150, 200, 250, 400]:
            if std >= amps_125:
                return std
        return int(amps_125)

    def validate_rules(self) -> List[str]:
        warnings = super().validate_rules()
        if self.charger_level == EvChargerLevel.DC_FAST_CHARGER and self.voltage < 400.0:
            warnings.append(f"EV Charger {self.tag}: DC Fast Chargers require 480V 3-Phase power (configured for {self.voltage}V).")
        return warnings
