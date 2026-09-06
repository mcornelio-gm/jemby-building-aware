"""Lighting & Appliance Branch Panelboard Object Class."""

from typing import List, Optional
from pydantic import Field
from james_app.core.panels.base_panel import PanelboardObject, SystemType
from james_app.core.breaker import BreakerStatus, CircuitBreakerObject


class LightingBranchPanelObject(PanelboardObject):
    """
    Branch Circuit Panelboard (LP / RP).
    Dense array of 1-Pole (15A, 20A) and 2-Pole branch circuits
    feeding lighting fixtures, receptacles, and tenant appliances.
    """
    category: str = "Branch Lighting & Receptacle Panel"
    system_type: SystemType = Field(default=SystemType.THREE_PHASE_208Y_120V)
    mains_rating_amps: int = Field(default=225, description="Mains rating in Amps")
    bus_amps: int = Field(default=225, description="Busbar continuous rating in Amps")
    total_spaces: int = Field(default=42, description="Total physical slots (30, 42, 54)")

    def add_branch_circuit(
        self,
        slot_start: int,
        description: str,
        amps: int = 20,
        poles: int = 1,
        target_load_id: Optional[str] = None
    ) -> CircuitBreakerObject:
        """Helper to quickly add a 1P/2P lighting or receptacle branch circuit."""
        return self.add_breaker(
            slot_start=slot_start,
            poles=poles,
            amps=amps,
            description=description,
            target_load_id=target_load_id
        )

    def validate_rules(self) -> List[str]:
        """Verify branch panel constraints."""
        warnings = super().validate_rules()
        for bkr in self.breakers.values():
            if bkr.status == BreakerStatus.ON and bkr.amps > 100:
                warnings.append(
                    f"Branch Panel {self.tag}: Large circuit {bkr.tag} ({bkr.amps}A) exceeds typical branch circuit limits (<=100A)."
                )
        return warnings
