"""Unit tests for all specialized Electrical Panelboard Subclasses."""

import pytest
from james_app.core.panels import (
    CriticalPowerPanelObject,
    EmergencyPanelObject,
    LightingBranchPanelObject,
    MainDistributionPanelObject,
    MotorControlCenterObject,
    PanelboardObject,
    ResidentialLoadcenterObject,
    SubpanelObject,
    SystemType,
    MainsType,
)


def test_lighting_branch_panel():
    """Test Lighting & Branch panel creation and branch circuit additions."""
    lp = LightingBranchPanelObject.create_empty(
        panel_id="LP_1",
        tag="LP-1",
        name="Lighting Panel 1",
        total_spaces=42,
        mains_rating_amps=225,
        system_type=SystemType.THREE_PHASE_208Y_120V
    )
    assert isinstance(lp, PanelboardObject)
    assert isinstance(lp, LightingBranchPanelObject)
    
    bkr = lp.add_branch_circuit(slot_start=1, description="Hallway Lighting", amps=20, poles=1)
    assert bkr.amps == 20
    assert bkr.poles == 1
    assert "HALLWAY LIGHTING" in lp.compile_focused_dot().upper()


def test_emergency_panel_and_rules():
    """Test Emergency Panel rules and emergency circuit tagging."""
    ep = EmergencyPanelObject.create_empty(
        panel_id="EP_LIFE_SAFETY",
        tag="EP-1",
        name="Emergency Life Safety Panel",
        total_spaces=30,
        mains_rating_amps=225
    )
    bkr = ep.add_emergency_circuit(slot_start=1, description="Egress Stairwell Lighting", amps=20)
    assert "[EMERG]" in bkr.name
    
    # Check warning when not connected to ATS/source
    warnings = ep.validate_rules()
    assert any("ATS" in w for w in warnings)


def test_critical_power_panel():
    """Test Critical Power Panel with Isolated Ground and SPD."""
    cp = CriticalPowerPanelObject.create_empty(
        panel_id="CP_DATACENTER",
        tag="CP-1",
        name="Data Center Server Panel",
        total_spaces=42,
        mains_rating_amps=225
    )
    assert cp.has_isolated_ground is True
    assert cp.spd_rating_ka == 120.0
    
    bkr = cp.add_it_circuit(slot_start=1, description="Rack A Server Power", amps=30, poles=2)
    assert "[IG/CLEAN]" in bkr.name
    assert bkr.poles == 2


def test_motor_control_center():
    """Test Motor Control Center starter bucket additions."""
    mcc = MotorControlCenterObject.create_empty(
        panel_id="MCC_PUMP_STATION",
        tag="MCC-1",
        name="Pump Station MCC",
        total_spaces=42,
        mains_rating_amps=800,
        system_type=SystemType.THREE_PHASE_480Y_277V
    )
    assert mcc.sections_count == 3
    
    bkr = mcc.add_motor_starter_bucket(
        slot_start=1,
        motor_name="Chilled Water Pump 1",
        hp_rating=50.0,
        fl_amps=65.0,
        is_vfd=True
    )
    assert bkr.poles == 3
    assert bkr.amps == 162  # 65A * 2.5 ~ 162A
    assert "VFD" in bkr.name
    assert bkr.id in mcc.buckets


def test_subpanel_mlo():
    """Test Subpanel with MLO default."""
    sub = SubpanelObject.create_empty(
        panel_id="SUB_GARAGE",
        tag="PANEL-G",
        name="Garage Subpanel",
        total_spaces=24,
        mains_rating_amps=100
    )
    assert sub.mains_type == MainsType.MLO


def test_residential_loadcenter():
    """Test Residential Loadcenter with split-phase 120/240V and AFCI/GFCI."""
    res = ResidentialLoadcenterObject.create_empty(
        panel_id="HOME_PANEL",
        tag="LP-HOME",
        name="Main House Loadcenter",
        total_spaces=40,
        mains_rating_amps=200,
        system_type=SystemType.SINGLE_PHASE_120_240V
    )
    assert res.system_type == SystemType.SINGLE_PHASE_120_240V
    assert res.has_plug_on_neutral is True
    
    bkr = res.add_residential_circuit(slot_start=1, description="Master Bedroom Outlets", amps=15, is_afci_gfci=True)
    assert "[AFCI/GFCI]" in bkr.name
