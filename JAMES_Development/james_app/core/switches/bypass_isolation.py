"""Bypass-Isolation Automatic Transfer Switch Object Class."""

from typing import List, Optional
from pydantic import Field
from james_app.core.switches.automatic_transfer import (
    AutomaticTransferSwitchObject,
    ConnectedSource,
    TransferTransitionType,
)


class BypassIsolationSwitchObject(AutomaticTransferSwitchObject):
    """
    Bypass-Isolation Automatic Transfer Switch.
    High-reliability dual-mechanism transfer apparatus engineered for healthcare facilities (NFPA 99 / NEC 517),
    data centers, and mission-critical 7x24 infrastructures.
    Combines an automatic transfer switch with a dedicated manual bypass switch, enabling safe live racking,
    testing, and maintenance of the ATS unit without dropping power to downstream critical life-safety loads.
    """
    category: str = "Critical Power Transfer Switch"
    switch_type_name: str = "Bypass-Isolation Automatic Transfer Switch"
    is_drawout_ats: bool = Field(default=True, description="ATS mechanism is drawout-rackable for maintenance")
    bypass_source_active: Optional[ConnectedSource] = Field(default=None, description="Active manual bypass feed (if bypassed)")
    is_in_bypass_mode: bool = Field(default=False, description="True when manual bypass is actively carrying the load")
    has_zero_interruption_transfer: bool = Field(default=True, description="No-break overlapping bypass contacts")

    def validate_rules(self) -> List[str]:
        """Perform bypass-isolation code safety checks."""
        warnings = super().validate_rules()
        if self.rated_amps < 100:
            warnings.append(
                f"Bypass-Isolation ATS {self.tag}: Bypass-isolation switches are typically >= 100A for critical facilities (got {self.rated_amps}A)."
            )
        return warnings
