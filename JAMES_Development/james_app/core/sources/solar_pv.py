"""Solar Photovoltaic (PV) Generation & Inverter System Object Class."""

from typing import List, Optional
from pydantic import Field
from james_app.core.sources.base_source import PowerSourceObject, SourceType


class SolarPvSystemObject(PowerSourceObject):
    """
    Solar Photovoltaic (PV) Array & Inverter System.
    Grid-tied or hybrid commercial solar generation system conforming to NEC 690 & NEC 705.
    Models DC string array capacity, inverter AC export capacity, and rapid shutdown capabilities.
    """
    category: str = "Renewable Generation"
    source_type: SourceType = SourceType.SOLAR_PV
    is_grid_forming: bool = False
    dc_system_capacity_kw: float = Field(default=250.0, description="Total DC solar module nameplate capacity in kW-DC")
    inverter_ac_capacity_kw: float = Field(default=200.0, description="Max AC continuous export capacity in kW-AC")
    inverter_efficiency_pct: float = Field(default=98.5, description="CEC weighted inverter efficiency percentage")
    mppt_voltage_range: str = Field(default="450V - 850V DC", description="Maximum Power Point Tracker DC operating window")
    has_rapid_shutdown: bool = Field(default=True, description="NEC 690.12 Module-Level Rapid Shutdown Initiator (RSD)")
    anti_islanding_protection: bool = Field(default=True, description="IEEE 1547 / UL 1741 utility loss disconnection")

    def validate_rules(self) -> List[str]:
        """Perform NEC 690 / 705 solar rules checks."""
        warnings = super().validate_rules()
        if not self.has_rapid_shutdown:
            warnings.append(f"Solar PV {self.tag}: NEC 690.12 requires rapid shutdown initiation for building-mounted solar arrays.")
        return warnings
