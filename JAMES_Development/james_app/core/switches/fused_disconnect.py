"""Fused Safety Disconnect Switch Object Class."""

from enum import Enum
from typing import List, Optional
from pydantic import Field
from james_app.core.switches.base_switch import EnclosureNemaType, SwitchObject, SwitchState


class FuseClass(str, Enum):
    """UL standard fuse classifications and rejection clip designs."""
    CLASS_R = "Class R (RK1 / RK5)"
    CLASS_J = "Class J (Time-Delay / High Speed)"
    CLASS_T = "Class T (Compact High Interrupting)"
    CLASS_L = "Class L (Heavy Feeder >= 601A)"
    CLASS_CC = "Class CC (Midget Control/Branch)"


class FusedDisconnectSwitchObject(SwitchObject):
    """
    Heavy Duty Fused Safety Disconnect Switch.
    Combines a visible-blade mechanical loadbreak disconnect with UL Class R/J/T rejection fuse clips
    providing up to 200kA RMS symmetrical short-circuit current ratings (SCCR).
    Used for service entrance disconnects, heavy motor feeds (NEC 430), and HVAC equipment.
    """
    category: str = "Safety Disconnect"
    switch_type_name: str = "Heavy Duty Fused Disconnect Switch"
    fuse_class: FuseClass = Field(default=FuseClass.CLASS_R, description="Installed fuse class and rejection clip type")
    fuse_amps: int = Field(default=100, ge=1, description="Installed current-limiting fuse rating in Amps")
    short_circuit_rating_ka: float = Field(default=200.0, description="Tested short-circuit rating with installed fuses (up to 200kA)")
    horsepower_rating_hp: Optional[float] = Field(default=60.0, description="Maximum standard motor horsepower rating at operating voltage")
    is_service_entrance_rated: bool = Field(default=False, description="Suitable for use as service entrance equipment (SUSE)")
    has_blown_fuse_indicators: bool = Field(default=True, description="Equipped with neon / LED blown fuse indicator lamps")

    def validate_rules(self) -> List[str]:
        """Perform fused switch code validation."""
        warnings = super().validate_rules()
        if self.fuse_amps > self.rated_amps:
            warnings.append(
                f"Fused Switch {self.tag}: Installed fuse rating ({self.fuse_amps}A) exceeds continuous switch switchblade rating ({self.rated_amps}A)."
            )
        return warnings
