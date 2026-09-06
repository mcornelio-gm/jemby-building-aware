"""Main Distribution Panel (MDP) / Power Panel Object Class."""

from typing import List, Optional
from pydantic import Field
from james_app.core.panels.base_panel import PanelboardObject, SystemType
from james_app.core.breaker import BreakerStatus, CircuitBreakerObject


class MainDistributionPanelObject(PanelboardObject):
    """
    Main Distribution Panel (MDP) / Power Panel (e.g. I-Line).
    Primary facility power trunk where positions are predominantly 3-pole
    sub-feeder breakers (70A - 800A) routing power to downstream subpanels and major machinery.
    """
    category: str = "Main Power Distribution"
    system_type: SystemType = Field(default=SystemType.THREE_PHASE_480Y_277V)
    mains_rating_amps: int = Field(default=800, description="Main breaker rating in Amps")
    bus_amps: int = Field(default=800, description="Main busbar rating in Amps")
    total_spaces: int = Field(default=42, description="Total physical slots")

    def add_feeder_breaker(
        self,
        slot_start: int,
        amps: int,
        target_panel_name: str,
        target_panel_id: Optional[str] = None,
        poles: int = 3
    ) -> CircuitBreakerObject:
        """Helper to add a 3-pole sub-feeder breaker to a downstream panel."""
        description = f"Feeder to {target_panel_name}"
        return self.add_breaker(
            slot_start=slot_start,
            poles=poles,
            amps=amps,
            description=description,
            target_load_id=target_panel_id
        )

    def validate_rules(self) -> List[str]:
        """Perform Main Distribution specific checks."""
        warnings = super().validate_rules()
        for bkr in self.breakers.values():
            if bkr.status == BreakerStatus.ON and bkr.poles == 1 and bkr.amps < 30:
                warnings.append(
                    f"Main Panel {self.tag}: Branch circuit {bkr.tag} ({bkr.amps}A 1P) is unusual on an MDP. Main panels typically house 3-pole feeder breakers (>=50A)."
                )
        return warnings
