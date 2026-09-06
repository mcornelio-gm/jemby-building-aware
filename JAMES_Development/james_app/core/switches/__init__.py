"""JEMBY Digital Twin - Switches & Disconnects Package."""

from james_app.core.switches.base_switch import (
    EnclosureNemaType,
    SwitchObject,
    SwitchState,
)
from james_app.core.switches.fused_disconnect import (
    FuseClass,
    FusedDisconnectSwitchObject,
)
from james_app.core.switches.non_fused_disconnect import (
    NonFusedDisconnectSwitchObject,
)
from james_app.core.switches.automatic_transfer import (
    AutomaticTransferSwitchObject,
    ConnectedSource,
    TransferTransitionType,
)
from james_app.core.switches.manual_transfer import (
    ManualTransferSwitchObject,
)
from james_app.core.switches.bypass_isolation import (
    BypassIsolationSwitchObject,
)

__all__ = [
    "SwitchObject",
    "SwitchState",
    "EnclosureNemaType",
    "FusedDisconnectSwitchObject",
    "FuseClass",
    "NonFusedDisconnectSwitchObject",
    "AutomaticTransferSwitchObject",
    "ConnectedSource",
    "TransferTransitionType",
    "ManualTransferSwitchObject",
    "BypassIsolationSwitchObject",
]
