"""Motor Circuit Protector (MCP) Object Class."""

from typing import List, Optional
from pydantic import Field
from james_app.core.breakers.base_breaker import BreakerStatus, CircuitBreakerObject


class MotorCircuitProtectorObject(CircuitBreakerObject):
    """
    Motor Circuit Protector (MCP / Instantaneous-Only Breaker).
    Engineered exclusively for combination motor starters inside Motor Control Centers (MCCs)
    providing instantaneous magnetic short-circuit protection without thermal overloads (NEC 430.52).
    """
    breaker_type_name: str = "Motor Circuit Protector (MCP)"
    magnetic_trip_setting_amps: float = Field(default=300.0, description="Adjustable instantaneous magnetic trip threshold")
    compatible_panel_categories: List[str] = Field(
        default_factory=lambda: ["Motor Control Center"],
        description="Matched panel categories"
    )

    def validate_rules(self) -> List[str]:
        """Perform MCP specific NEC 430 rules checks."""
        warnings = super().validate_rules()
        if self.poles != 3:
            warnings.append(f"MCP {self.tag}: Motor circuit protectors in industrial MCCs must be 3-Pole units.")
        return warnings
