"""Miniature Circuit Breaker (MCB) Object Class."""

from typing import List, Optional
from pydantic import Field
from james_app.core.breakers.base_breaker import BreakerStatus, CircuitBreakerObject


class MiniatureBreakerObject(CircuitBreakerObject):
    """
    Standard Miniature Circuit Breaker (MCB).
    Engineered for Branch Lighting & Appliance Panels (LP / RP) and Subpanels
    for 120V/208V/277V branch circuits (15A - 60A).
    """
    breaker_type_name: str = "Miniature Breaker (MCB)"
    mounting_type: str = Field(default="Bolt-On", description="Bolt-On (QOB/BQ) or Plug-On (QO/Q)")
    aic_rating_ka: float = Field(default=10.0, description="Interrupting rating in kA (10kA, 22kA)")
    compatible_panel_categories: List[str] = Field(
        default_factory=lambda: ["Branch Lighting & Receptacle Panel", "Sub-Distribution Panel", "Emergency & Life Safety", "Critical IT & Isolated Ground", "Residential Loadcenter"],
        description="Matched panel categories"
    )

    def validate_rules(self) -> List[str]:
        """Perform MCB specific checks."""
        warnings = super().validate_rules()
        if self.amps > 100:
            warnings.append(
                f"MCB {self.tag}: Miniature breakers typically top out at 100A (got {self.amps}A). For >=125A, use a Molded Case Breaker (MCCB)."
            )
        return warnings
