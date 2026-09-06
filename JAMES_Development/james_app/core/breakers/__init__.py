"""JEMBY Digital Twin - Specialized Circuit Breaker Classes Package."""

from typing import Type
from james_app.core.breakers.base_breaker import CircuitBreakerObject, BreakerStatus
from james_app.core.breakers.molded_case import MoldedCaseBreakerObject
from james_app.core.breakers.miniature_breaker import MiniatureBreakerObject
from james_app.core.breakers.afci_gfci import AfciGfciBreakerObject
from james_app.core.breakers.motor_protector import MotorCircuitProtectorObject
from james_app.core.breakers.drawout_power import DrawoutPowerBreakerObject
from james_app.core.breakers.tandem_breaker import TandemBreakerObject

__all__ = [
    "CircuitBreakerObject",
    "BreakerStatus",
    "MoldedCaseBreakerObject",
    "MiniatureBreakerObject",
    "AfciGfciBreakerObject",
    "MotorCircuitProtectorObject",
    "DrawoutPowerBreakerObject",
    "TandemBreakerObject",
    "get_recommended_breaker_class",
]

# Mapping Panel Categories to their engineered default breaker types
PANEL_TO_BREAKER_MAP = {
    "Main Power Distribution": MoldedCaseBreakerObject,
    "Branch Lighting & Receptacle Panel": MiniatureBreakerObject,
    "Emergency & Life Safety": MiniatureBreakerObject,
    "Critical IT & Isolated Ground": MiniatureBreakerObject,
    "Motor Control Center": MotorCircuitProtectorObject,
    "Sub-Distribution Panel": MiniatureBreakerObject,
    "Residential Loadcenter": AfciGfciBreakerObject,
    "Switchgear": DrawoutPowerBreakerObject,
}


def get_recommended_breaker_class(panel_category: str) -> Type[CircuitBreakerObject]:
    """Return the primary matched circuit breaker class for a given panel category."""
    return PANEL_TO_BREAKER_MAP.get(panel_category, MiniatureBreakerObject)
