"""Motor Control Center (MCC) Object Class."""

from typing import Any, Dict, List, Optional
from pydantic import Field
from james_app.core.panels.base_panel import PanelboardObject, SystemType
from james_app.core.breaker import BreakerStatus, CircuitBreakerObject


class MotorControlCenterObject(PanelboardObject):
    """
    Motor Control Center (MCC).
    Modular multi-section vertical enclosure housing combination motor starters,
    Variable Frequency Drives (VFDs), overload protection, and contactor buckets.
    """
    category: str = "Motor Control Center"
    system_type: SystemType = Field(default=SystemType.THREE_PHASE_480Y_277V)
    mains_rating_amps: int = Field(default=800, description="MCC main bus continuous rating")
    bus_amps: int = Field(default=800, description="Horizontal busbar rating in Amps")
    sections_count: int = Field(default=3, ge=1, description="Number of vertical NEMA sections")
    buckets: Dict[str, Dict[str, Any]] = Field(default_factory=dict, description="Starter and VFD modular buckets")

    def add_motor_starter_bucket(
        self,
        slot_start: int,
        motor_name: str,
        hp_rating: float,
        fl_amps: float,
        nema_size: int = 1,
        is_vfd: bool = False,
        target_motor_id: Optional[str] = None
    ) -> CircuitBreakerObject:
        """Add a combination motor starter or VFD bucket to the MCC."""
        # Motor breaker sizing typically ~250% of FLA for standard inverse time breaker (NEC 430.52)
        bkr_amps = int(fl_amps * 2.5) if fl_amps > 0 else 30
        starter_type = "VFD" if is_vfd else f"NEMA Size {nema_size} Starter"
        desc = f"{motor_name} ({hp_rating}HP - {starter_type})"

        bkr = self.add_breaker(
            slot_start=slot_start,
            poles=3,
            amps=bkr_amps,
            description=desc,
            target_load_id=target_motor_id
        )

        self.buckets[bkr.id] = {
            "motor_name": motor_name,
            "hp": hp_rating,
            "fla": fl_amps,
            "starter_type": starter_type,
            "is_vfd": is_vfd
        }
        return bkr

    def validate_rules(self) -> List[str]:
        """Perform MCC motor protection checks."""
        warnings = super().validate_rules()
        for bkr in self.breakers.values():
            if bkr.status == BreakerStatus.ON and bkr.poles < 3:
                warnings.append(f"MCC {self.tag}: Single-phase bucket {bkr.tag} is unusual. MCCs predominantly house 3-phase motor starters.")
        return warnings
