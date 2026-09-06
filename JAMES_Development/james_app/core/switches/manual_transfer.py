"""Manual Transfer Switch (MTS) Object Class."""

from typing import List, Optional
from pydantic import Field
from james_app.core.switches.automatic_transfer import ConnectedSource
from james_app.core.switches.base_switch import EnclosureNemaType, SwitchObject, SwitchState


class ManualTransferSwitchObject(SwitchObject):
    """
    Manual Transfer Switch (MTS / Double-Throw Safety Switch).
    Mechanically interlocked double-throw switch engineered for manual load transfer between
    a utility feed and a portable generator, mobile transformer, or secondary utility service.
    Features center-OFF position and positive mechanical interlock preventing backfeeding.
    """
    category: str = "Transfer Switch"
    switch_type_name: str = "Manual Double-Throw Transfer Switch (MTS)"
    normal_source_id: str = Field(..., description="Utility source ID")
    emergency_source_id: str = Field(..., description="Portable/backup generator source ID")
    active_source: ConnectedSource = Field(default=ConnectedSource.NORMAL, description="Current mechanical position")
    has_cam_lock_inlet: bool = Field(default=False, description="Equipped with quick-connect Color-Coded Series 16 Cam-Lock inlets")
    has_center_off: bool = Field(default=True, description="Three-position switch (NORMAL - OFF - EMERGENCY)")

    # --- 1. Connectivity Terminals ---
    def get_input_ports(self) -> List[str]:
        """Dual source input ports: Normal and Emergency."""
        normal_ports = [f"norm_L{i+1}" for i in range(self.poles)]
        emerg_ports = [f"emerg_L{i+1}" for i in range(self.poles)]
        return normal_ports + emerg_ports

    def get_output_ports(self) -> List[str]:
        """Single common load bus output."""
        return [f"load_T{i+1}" for i in range(self.poles)] + (["load_N"] if self.poles == 4 else [])

    def validate_rules(self) -> List[str]:
        """Perform MTS validation checks."""
        warnings = super().validate_rules()
        if not self.normal_source_id or not self.emergency_source_id:
            warnings.append(f"MTS {self.tag}: Both Normal and Emergency source feeds must be specified.")
        return warnings
