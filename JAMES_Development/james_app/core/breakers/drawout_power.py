"""Drawout Low Voltage Power Circuit Breaker (LVPCB / Air Breaker) Object Class."""

from typing import List, Optional
from pydantic import Field
from james_app.core.breakers.base_breaker import BreakerStatus, CircuitBreakerObject


class DrawoutPowerBreakerObject(CircuitBreakerObject):
    """
    Drawout Low Voltage Power Circuit Breaker (LVPCB / Air Circuit Breaker).
    Heavy-duty switchgear main breaker (800A - 6000A) with drawout racking mechanism
    and advanced Electronic Trip Unit (LSIG: Long, Short, Instantaneous, Ground fault).
    Matched to Main Service Entrances, Switchgear, and heavy Substation Distribution.
    """
    breaker_type_name: str = "Drawout Power Air Breaker (LVPCB)"
    frame_amps: int = Field(default=2000, description="Switchgear frame size (e.g. 1600A, 2000A, 3200A, 5000A)")
    aic_rating_ka: float = Field(default=65.0, description="Withstand / interrupting rating in kA (65kA, 85kA, 100kA)")
    has_lsig_protection: bool = Field(default=True, description="Full LSIG electronic coordination protection")
    is_drawout: bool = Field(default=True, description="Racking drawout mechanism for live maintenance")
    compatible_panel_categories: List[str] = Field(
        default_factory=lambda: ["Main Power Distribution", "Switchgear", "Distribution Enclosure"],
        description="Matched panel categories"
    )

    def validate_rules(self) -> List[str]:
        """Perform LVPCB switchgear rules verification."""
        warnings = super().validate_rules()
        if self.amps < 400:
            warnings.append(f"Drawout Breaker {self.tag}: Drawout power breakers are designed for bulk mains (>=400A). For smaller loads, use an MCCB.")
        return warnings
