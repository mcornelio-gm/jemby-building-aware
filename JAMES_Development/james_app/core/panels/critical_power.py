"""Critical Power and Isolated Ground Panelboard Object Class."""

from typing import List, Optional
from pydantic import Field
from james_app.core.panels.base_panel import PanelboardObject, SystemType
from james_app.core.breaker import BreakerStatus, CircuitBreakerObject


class CriticalPowerPanelObject(PanelboardObject):
    """
    Critical Power / Electronic Data Processing Panel (CP / EDP).
    Equipped with an Isolated Ground (IG) bus and integrated Surge Protective Device (SPD).
    Used in data centers, server rooms, laboratories, and sensitive IT installations.
    """
    category: str = "Critical IT & Isolated Ground"
    system_type: SystemType = Field(default=SystemType.THREE_PHASE_208Y_120V)
    mains_rating_amps: int = Field(default=225, description="Mains rating in Amps")
    bus_amps: int = Field(default=225, description="Bus rating in Amps")
    has_isolated_ground: bool = Field(default=True, description="Equipped with dedicated Isolated Ground busbar")
    spd_rating_ka: float = Field(default=120.0, description="Integrated Surge Protective Device surge current rating per phase (kA)")

    def add_it_circuit(
        self,
        slot_start: int,
        description: str,
        amps: int = 20,
        poles: int = 1,
        target_load_id: Optional[str] = None
    ) -> CircuitBreakerObject:
        """Add clean computer / server power circuit."""
        return self.add_breaker(
            slot_start=slot_start,
            poles=poles,
            amps=amps,
            description=f"[IG/CLEAN] {description}",
            target_load_id=target_load_id
        )

    def validate_rules(self) -> List[str]:
        """Verify surge protection and clean power rules."""
        warnings = super().validate_rules()
        if self.spd_rating_ka < 50.0:
            warnings.append(f"Critical Panel {self.tag}: SPD rating ({self.spd_rating_ka}kA) is below recommended 50kA minimum for server environments.")
        return warnings
