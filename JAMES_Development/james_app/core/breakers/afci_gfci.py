"""AFCI / GFCI Dual-Function Safety Circuit Breaker Object Class."""

from typing import List, Optional
from pydantic import Field
from james_app.core.breakers.base_breaker import BreakerStatus, CircuitBreakerObject


class AfciGfciBreakerObject(CircuitBreakerObject):
    """
    Dual-Function AFCI / GFCI Safety Circuit Breaker.
    Combines Arc-Fault protection (NEC 210.12) and Class A 5mA Ground-Fault
    personnel protection (NEC 210.8) for bedrooms, kitchens, bathrooms, and living spaces.
    Matched primarily to Residential Loadcenters and branch lighting/receptacle panels.
    """
    breaker_type_name: str = "Dual-Function AFCI/GFCI"
    is_afci: bool = Field(default=True, description="Arc-Fault Circuit Interrupter active")
    is_gfci: bool = Field(default=True, description="Ground-Fault Circuit Interrupter active (Class A 5mA)")
    self_test_enabled: bool = Field(default=True, description="Continuous automatic self-testing")
    compatible_panel_categories: List[str] = Field(
        default_factory=lambda: ["Residential Loadcenter", "Branch Lighting & Receptacle Panel"],
        description="Matched panel categories"
    )

    def validate_rules(self) -> List[str]:
        """Perform AFCI/GFCI specific code compliance checks."""
        warnings = super().validate_rules()
        if self.poles > 2:
            warnings.append(f"AFCI/GFCI Breaker {self.tag}: Dual-function breakers are only manufactured in 1-Pole (120V) or 2-Pole (240V).")
        return warnings
