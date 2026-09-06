"""Residential Loadcenter Object Class."""

from typing import List, Optional
from pydantic import Field
from james_app.core.panels.base_panel import PanelboardObject, SystemType
from james_app.core.breaker import BreakerStatus, CircuitBreakerObject


class ResidentialLoadcenterObject(PanelboardObject):
    """
    Residential Loadcenter Panel.
    Split-phase (120/240V 1Ø 3W) panelboard designed for single-family homes
    and multi-family residential units with plug-on neutral and AFCI/GFCI protection.
    """
    category: str = "Residential Loadcenter"
    system_type: SystemType = Field(default=SystemType.SINGLE_PHASE_120_240V)
    mains_rating_amps: int = Field(default=200, description="Main service breaker rating (e.g. 100A, 150A, 200A)")
    bus_amps: int = Field(default=200, description="Busbar rating in Amps")
    total_spaces: int = Field(default=40, description="Total physical slots (e.g. 24, 30, 40, 42)")
    has_plug_on_neutral: bool = Field(default=True, description="Plug-on Neutral (PoN) bus architecture")

    def add_residential_circuit(
        self,
        slot_start: int,
        description: str,
        amps: int = 20,
        poles: int = 1,
        is_afci_gfci: bool = True,
        target_load_id: Optional[str] = None
    ) -> CircuitBreakerObject:
        """Add residential branch circuit with AFCI/GFCI compliance."""
        prefix = "[AFCI/GFCI] " if is_afci_gfci else ""
        return self.add_breaker(
            slot_start=slot_start,
            poles=poles,
            amps=amps,
            description=f"{prefix}{description}",
            target_load_id=target_load_id
        )

    def validate_rules(self) -> List[str]:
        """Perform residential code safety checks."""
        warnings = super().validate_rules()
        if self.system_type != SystemType.SINGLE_PHASE_120_240V:
            warnings.append(f"Residential Loadcenter {self.tag}: Expected split-phase 120/240V 1Ø 3W, got {self.system_type.value}.")
        return warnings
