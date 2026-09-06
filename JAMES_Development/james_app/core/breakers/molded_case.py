"""Molded Case Circuit Breaker (MCCB) Object Class."""

from typing import List, Optional
from pydantic import Field
from james_app.core.breakers.base_breaker import BreakerStatus, CircuitBreakerObject


class MoldedCaseBreakerObject(CircuitBreakerObject):
    """
    Industrial / Commercial Molded Case Circuit Breaker (MCCB).
    Engineered for Main Distribution Panels (MDP / I-Line), Switchboards,
    and heavy feeder loads (70A - 800A+) with high AIC interrupting ratings.
    """
    breaker_type_name: str = "Molded Case Breaker (MCCB)"
    frame_name: str = Field(default="J-Frame (250A)", description="Industrial frame type (e.g. H-Frame 150A, J-Frame 250A, L-Frame 400A, P-Frame 800A)")
    aic_rating_ka: float = Field(default=35.0, description="Short-circuit interrupting rating in kA (22kA, 35kA, 65kA, 100kA)")
    has_electronic_trip: bool = Field(default=False, description="Equipped with Micrologic / Electronic Trip Unit (ETU)")
    compatible_panel_categories: List[str] = Field(
        default_factory=lambda: ["Main Power Distribution", "Distribution Enclosure", "Motor Control Center"],
        description="Matched panel categories"
    )

    def validate_rules(self) -> List[str]:
        """Perform MCCB specific rating and frame checks."""
        warnings = super().validate_rules()
        if self.amps > self.frame_amps:
            warnings.append(
                f"MCCB {self.tag}: Trip rating ({self.amps}A) exceeds physical frame rating ({self.frame_amps}A for {self.frame_name})."
            )
        return warnings
