"""Non-Fused Safety Disconnect Switch Object Class."""

from typing import List, Optional
from pydantic import Field
from james_app.core.switches.base_switch import EnclosureNemaType, SwitchObject, SwitchState


class NonFusedDisconnectSwitchObject(SwitchObject):
    """
    Non-Fused Safety Disconnect Switch (Unfused Isolation Switch).
    Used as an OSHA/NEC compliant visible-blade or rotary physical isolation disconnect
    installed within sight of motors (NEC 430.102), air conditioning units (NEC 440.14),
    pumps, and industrial machinery.
    Relies on upstream panel circuit breakers or fuses for overcurrent protection.
    """
    category: str = "Safety Disconnect"
    switch_type_name: str = "Non-Fused Safety Disconnect Switch"
    short_circuit_rating_ka: float = Field(default=10.0, description="Base withstand rating (can be 100kA-200kA when series-rated with upstream OCPD)")
    horsepower_rating_hp: Optional[float] = Field(default=50.0, description="Motor isolation horsepower rating")
    is_rotary_style: bool = Field(default=False, description="Compact rotary DIN-rail or door-mount handle style")
    is_within_sight: bool = Field(default=True, description="Located within 50 feet and visible from the driven equipment per NEC 430.102")

    def validate_rules(self) -> List[str]:
        """Verify NEC 430/440 disconnect location and rules."""
        warnings = super().validate_rules()
        if not self.is_within_sight:
            warnings.append(
                f"Non-Fused Switch {self.tag}: Disconnect must be located within sight (<=50ft) of motor/equipment per NEC 430.102 unless lockable in the open position."
            )
        return warnings
