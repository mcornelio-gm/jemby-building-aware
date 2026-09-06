"""Electric Utility Grid Service Entrance Source Object Class."""

from typing import List, Optional
from pydantic import Field
from james_app.core.sources.base_source import PowerSourceObject, SourceType


class UtilityServiceSource(PowerSourceObject):
    """
    Electric Utility Service Entrance Grid Connection.
    Represents the primary grid feed from the utility provider (e.g., ConEd, PG&E, ComEd),
    defining point of common coupling (PCC), available fault MVA / X/R ratio, and revenue metering.
    """
    category: str = "Utility Service"
    source_type: SourceType = SourceType.UTILITY
    utility_company_name: str = Field(default="Electric Utility", description="Operating utility provider name")
    account_number: Optional[str] = Field(default=None, description="Utility service account / meter identifier")
    service_entrance_type: str = Field(default="Underground Lateral", description="'Underground Lateral' or 'Overhead Service Drop'")
    utility_transformer_mva: float = Field(default=2.5, description="Utility substation / padmount transformer MVA")
    available_fault_mva_sc: float = Field(default=500.0, description="Utility primary available short-circuit MVA")
    xr_ratio: float = Field(default=15.0, description="Short-circuit X/R ratio at service point")
    has_revenue_metering_ct_pt: bool = Field(default=True, description="Dedicated utility revenue CT/PT metering compartment")

    def validate_rules(self) -> List[str]:
        """Perform utility connection validation."""
        warnings = super().validate_rules()
        if self.available_fault_current_ka <= 0:
            warnings.append(f"Utility Source {self.tag}: Available fault current must be greater than 0 kA for short-circuit study.")
        return warnings
