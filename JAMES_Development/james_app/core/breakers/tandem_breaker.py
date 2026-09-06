"""Tandem / Quad Space-Saver Circuit Breaker Object Class."""

from typing import List, Optional
from pydantic import Field
from james_app.core.breakers.base_breaker import BreakerStatus, CircuitBreakerObject


class TandemBreakerObject(CircuitBreakerObject):
    """
    Tandem / Twin / Quad Space-Saver Circuit Breaker.
    Houses two independent 1-pole circuits in a single 1-inch physical slot position
    (e.g. Circuit 1A and 1B on Slot 1) for residential loadcenter circuit expansion.
    """
    breaker_type_name: str = "Tandem Space-Saver (Twin 1P)"
    sub_circuits_count: int = Field(default=2, ge=2, le=4, description="Number of independent circuits (2 for Twin, 4 for Quad)")
    secondary_amps: int = Field(default=20, ge=15, description="Amps for the secondary circuit in the twin slot")
    secondary_name: str = Field(default="Secondary Circuit", description="Description for the secondary circuit")
    compatible_panel_categories: List[str] = Field(
        default_factory=lambda: ["Residential Loadcenter"],
        description="Matched panel categories"
    )

    def validate_rules(self) -> List[str]:
        """Perform tandem slot compatibility checks."""
        warnings = super().validate_rules()
        if self.poles != 1:
            warnings.append(f"Tandem Breaker {self.tag}: Twin breakers occupy 1 physical slot sharing a single phase stab.")
        return warnings
