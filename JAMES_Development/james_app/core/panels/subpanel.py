"""Subpanel / Remote Distribution Panelboard Object Class."""

from typing import List, Optional
from pydantic import Field
from james_app.core.panels.base_panel import MainsType, PanelboardObject, SystemType
from james_app.core.breaker import BreakerStatus, CircuitBreakerObject


class SubpanelObject(PanelboardObject):
    """
    Subpanel / Remote Distribution Board.
    Fed from an upstream Main Distribution Panel (MDP) or Switchboard.
    Frequently Main Lugs Only (MLO) or equipped with a secondary main disconnect.
    """
    category: str = "Sub-Distribution Panel"
    system_type: SystemType = Field(default=SystemType.THREE_PHASE_208Y_120V)
    mains_type: MainsType = Field(default=MainsType.MLO)
    mains_rating_amps: int = Field(default=225, description="Main lug or breaker rating")
    bus_amps: int = Field(default=225, description="Bus rating in Amps")
    upstream_panel_id: Optional[str] = Field(default=None, description="Feeding parent panel ID")

    @classmethod
    def create_empty(
        cls,
        panel_id: str,
        tag: str = "SUB-1",
        name: str = "SUBPANEL",
        total_spaces: int = 24,
        mains_rating_amps: int = 100,
        system_type: SystemType = SystemType.THREE_PHASE_208Y_120V,
        mains_type: MainsType = MainsType.MLO
    ) -> "SubpanelObject":
        """Instantiate empty subpanel defaulting to Main Lugs Only (MLO)."""
        return super().create_empty(
            panel_id=panel_id,
            tag=tag,
            name=name,
            total_spaces=total_spaces,
            mains_rating_amps=mains_rating_amps,
            system_type=system_type,
            mains_type=mains_type
        )

    def validate_rules(self) -> List[str]:
        """Perform subpanel distribution rules verification."""
        warnings = super().validate_rules()
        if not self.upstream_feed and not self.upstream_panel_id:
            warnings.append(f"Subpanel {self.tag}: Missing upstream feeder source assignment.")
        return warnings
