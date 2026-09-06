"""Emergency and Life Safety Panelboard Object Class."""

from typing import List, Optional
from pydantic import Field
from james_app.core.panels.base_panel import PanelboardObject, SystemType
from james_app.core.breaker import BreakerStatus, CircuitBreakerObject


class EmergencyPanelObject(PanelboardObject):
    """
    Emergency / Life Safety Distribution Panel (EP / LP-EM).
    Fed from an Automatic Transfer Switch (ATS), UPS, or Standby Generator.
    Powers egress lighting, exit signs, fire alarm, and life safety loads per NEC 700/701.
    """
    category: str = "Emergency & Life Safety"
    system_type: SystemType = Field(default=SystemType.THREE_PHASE_208Y_120V)
    mains_rating_amps: int = Field(default=225, description="Mains rating in Amps")
    bus_amps: int = Field(default=225, description="Busbar rating in Amps")
    total_spaces: int = Field(default=30, description="Total physical slots")
    ats_source_id: Optional[str] = Field(default=None, description="Connected ATS instance ID")

    def add_emergency_circuit(
        self,
        slot_start: int,
        description: str,
        amps: int = 20,
        poles: int = 1,
        target_load_id: Optional[str] = None
    ) -> CircuitBreakerObject:
        """Add dedicated emergency / life safety branch circuit."""
        return self.add_breaker(
            slot_start=slot_start,
            poles=poles,
            amps=amps,
            description=f"[EMERG] {description}",
            target_load_id=target_load_id
        )

    def validate_rules(self) -> List[str]:
        """Verify NEC 700/701 Emergency system segregation requirements."""
        warnings = super().validate_rules()
        if not self.upstream_feed and not self.ats_source_id:
            warnings.append(f"Emergency Panel {self.tag}: Must be connected to an upstream ATS or Standby Power Source.")
        return warnings
