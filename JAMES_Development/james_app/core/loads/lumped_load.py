"""Lumped / Aggregate Building Electrical Load Object Class."""

from typing import List, Optional
from pydantic import Field
from james_app.core.loads.base_load import LoadObject, LoadType


class LumpedLoadObject(LoadObject):
    """
    Lumped / Aggregate Electrical Branch Load.
    Used for lighting circuit zones, general convenience receptacle banks,
    office workstation clusters, server rack rows, and kitchen appliance groupings.
    """
    category: str = "General Branch Load"
    load_type: LoadType = Field(default=LoadType.RECEPTACLE)
    area_served_sqft: Optional[float] = Field(default=None, description="Physical square footage served for W/sqft energy metrics")
    watts_per_sqft: Optional[float] = Field(default=None, description="Lighting/power density metric")
    demand_factor_pct: float = Field(default=100.0, ge=10.0, le=100.0, description="NEC Article 220 demand factor percentage")

    @property
    def diversified_power_kva(self) -> float:
        """Calculate calculated demand apparent power applying NEC demand factor."""
        return round(self.power_kva * (self.demand_factor_pct / 100.0), 2)
