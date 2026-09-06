"""Unit tests for all specialized Circuit Breaker Subclasses and Panel Matching Rules."""

import pytest
from james_app.core.breakers import (
    AfciGfciBreakerObject,
    BreakerStatus,
    CircuitBreakerObject,
    DrawoutPowerBreakerObject,
    MiniatureBreakerObject,
    MoldedCaseBreakerObject,
    MotorCircuitProtectorObject,
    TandemBreakerObject,
    get_recommended_breaker_class,
)
from james_app.core.panels import (
    CriticalPowerPanelObject,
    LightingBranchPanelObject,
    MainDistributionPanelObject,
    MotorControlCenterObject,
    ResidentialLoadcenterObject,
)


def test_breaker_to_panel_type_matching():
    """Verify panel category to breaker class matching helper."""
    assert get_recommended_breaker_class("Main Power Distribution") == MoldedCaseBreakerObject
    assert get_recommended_breaker_class("Branch Lighting & Receptacle Panel") == MiniatureBreakerObject
    assert get_recommended_breaker_class("Residential Loadcenter") == AfciGfciBreakerObject
    assert get_recommended_breaker_class("Motor Control Center") == MotorCircuitProtectorObject
    assert get_recommended_breaker_class("Switchgear") == DrawoutPowerBreakerObject


def test_molded_case_breaker():
    """Test industrial MCCB with frame sizing and high AIC ratings."""
    mccb = MoldedCaseBreakerObject(
        id="mccb_1",
        tag="CB-100",
        name="Chiller Feeder",
        slot_start=1,
        poles=3,
        occupied_slots=[1, 3, 5],
        amps=225,
        frame_amps=250,
        frame_name="J-Frame (250A)",
        aic_rating_ka=65.0,
        connected_phases=["A", "B", "C"]
    )
    assert mccb.is_compatible_with("Main Power Distribution") is True
    assert mccb.is_compatible_with("Residential Loadcenter") is False
    assert len(mccb.validate_rules()) == 0


def test_miniature_breaker():
    """Test standard branch MCB with 1P/2P ratings."""
    mcb = MiniatureBreakerObject(
        id="mcb_1",
        tag="CB-1",
        name="Office Receptacles",
        slot_start=1,
        poles=1,
        occupied_slots=[1],
        amps=20,
        connected_phases=["A"]
    )
    assert mcb.is_compatible_with("Branch Lighting & Receptacle Panel") is True
    assert len(mcb.validate_rules()) == 0


def test_afci_gfci_breaker():
    """Test dual-function AFCI/GFCI residential breaker."""
    afci = AfciGfciBreakerObject(
        id="afci_1",
        tag="CB-AFCI-1",
        name="Bedroom Circuit",
        slot_start=1,
        poles=1,
        occupied_slots=[1],
        amps=15,
        is_afci=True,
        is_gfci=True,
        connected_phases=["A"]
    )
    assert afci.is_compatible_with("Residential Loadcenter") is True
    assert len(afci.validate_rules()) == 0


def test_motor_circuit_protector():
    """Test instantaneous-only MCP for MCC motor starter buckets."""
    mcp = MotorCircuitProtectorObject(
        id="mcp_1",
        tag="MCP-1",
        name="Pump Motor Mag-Only",
        slot_start=1,
        poles=3,
        occupied_slots=[1, 3, 5],
        amps=50,
        magnetic_trip_setting_amps=450.0,
        connected_phases=["A", "B", "C"]
    )
    assert mcp.is_compatible_with("Motor Control Center") is True
    assert mcp.is_compatible_with("Branch Lighting & Receptacle Panel") is False
    assert len(mcp.validate_rules()) == 0


def test_drawout_power_breaker():
    """Test drawout air circuit breaker with LSIG protection for switchgear."""
    lvpcb = DrawoutPowerBreakerObject(
        id="main_drawout",
        tag="MAIN-SWGR",
        name="Main Service Air Breaker",
        slot_start=1,
        poles=3,
        occupied_slots=[1, 2, 3],
        amps=2000,
        frame_amps=2000,
        aic_rating_ka=100.0,
        is_drawout=True,
        connected_phases=["A", "B", "C"]
    )
    assert lvpcb.is_compatible_with("Switchgear") is True
    assert len(lvpcb.validate_rules()) == 0


def test_tandem_breaker():
    """Test residential tandem space-saver twin breaker."""
    tandem = TandemBreakerObject(
        id="tandem_1",
        tag="CB-1A/1B",
        name="Twin Circuit 1A",
        slot_start=1,
        poles=1,
        occupied_slots=[1],
        amps=15,
        secondary_amps=20,
        secondary_name="Twin Circuit 1B",
        connected_phases=["A"]
    )
    assert tandem.is_compatible_with("Residential Loadcenter") is True
    assert len(tandem.validate_rules()) == 0
