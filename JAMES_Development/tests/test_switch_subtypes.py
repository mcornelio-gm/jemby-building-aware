"""Unit tests for Switch & Disconnect Object Hierarchy."""

import pytest
from james_app.core.switches import (
    SwitchObject,
    SwitchState,
    EnclosureNemaType,
    FusedDisconnectSwitchObject,
    FuseClass,
    NonFusedDisconnectSwitchObject,
    AutomaticTransferSwitchObject,
    ConnectedSource,
    TransferTransitionType,
    ManualTransferSwitchObject,
    BypassIsolationSwitchObject,
)


def test_base_switch_object():
    """Test base switch object attributes, ports, rules, and visual projections."""
    sw = SwitchObject(
        id="sw_main_1",
        tag="SW-1",
        name="Main Service Disconnect",
        poles=3,
        rated_amps=200,
        voltage=480.0,
        state=SwitchState.CLOSED,
        enclosure_type=EnclosureNemaType.NEMA_3R
    )
    assert len(sw.get_input_ports()) == 3
    assert len(sw.get_output_ports()) == 3
    assert len(sw.validate_rules()) == 0

    dot = sw.compile_focused_dot()
    assert "Switch_sw_main_1" in dot
    assert "200A 3P" in dot

    html_view = sw.render_html_view()
    assert "SW-1" in html_view
    assert "CLOSED" in html_view

    puml = sw.compile_plantuml_sld()
    assert "SW-1" in puml or "Main Service Disconnect" in puml


def test_fused_and_non_fused_disconnects():
    """Test safety disconnect switch subclasses."""
    fused = FusedDisconnectSwitchObject(
        id="disc_chiller_1",
        tag="DS-CH1",
        name="Chiller #1 Fused Disconnect",
        poles=3,
        rated_amps=200,
        fuse_amps=175,
        fuse_class=FuseClass.CLASS_J,
        short_circuit_rating_ka=200.0,
        enclosure_type=EnclosureNemaType.NEMA_3R
    )
    assert fused.fuse_amps == 175
    assert fused.short_circuit_rating_ka == 200.0
    assert len(fused.validate_rules()) == 0

    # Rule check: fuse amps > switch amps
    fused_bad = FusedDisconnectSwitchObject(
        id="disc_bad",
        tag="DS-BAD",
        name="Bad Disconnect",
        rated_amps=100,
        fuse_amps=150
    )
    warnings = fused_bad.validate_rules()
    assert any("exceeds continuous switch" in w for w in warnings)

    non_fused = NonFusedDisconnectSwitchObject(
        id="disc_ahu_1",
        tag="DS-AHU1",
        name="AHU-1 Local Disconnect",
        poles=3,
        rated_amps=60,
        is_within_sight=True
    )
    assert len(non_fused.validate_rules()) == 0


def test_automatic_and_manual_transfer_switches():
    """Test ATS and MTS transfer switches."""
    ats = AutomaticTransferSwitchObject(
        id="ats_em_1",
        tag="ATS-1",
        name="Life Safety ATS",
        poles=4,
        rated_amps=400,
        voltage=480.0,
        normal_source_id="MDP-1",
        emergency_source_id="GEN-1",
        active_source=ConnectedSource.NORMAL,
        transition_type=TransferTransitionType.OPEN_TRANSITION
    )
    assert len(ats.get_input_ports()) == 8  # 4 normal + 4 emergency
    assert len(ats.get_output_ports()) == 5  # 4 load + neutral
    assert len(ats.validate_rules()) == 0

    dot = ats.compile_focused_dot()
    assert "ATS_ats_em_1" in dot
    assert "NORMAL SOURCE" in dot

    mts = ManualTransferSwitchObject(
        id="mts_dock",
        tag="MTS-1",
        name="Loading Dock Portable Generator MTS",
        poles=3,
        rated_amps=200,
        normal_source_id="MDP-2",
        emergency_source_id="PORTABLE_GEN",
        has_cam_lock_inlet=True
    )
    assert mts.has_cam_lock_inlet is True
    assert len(mts.validate_rules()) == 0

    bypass = BypassIsolationSwitchObject(
        id="ats_bypass_1",
        tag="ATS-BYP-1",
        name="Operating Suite Critical Power ATS",
        poles=4,
        rated_amps=800,
        normal_source_id="MDP-EM",
        emergency_source_id="GEN-EM",
        is_drawout_ats=True,
        has_zero_interruption_transfer=True
    )
    assert bypass.is_drawout_ats is True
    assert len(bypass.validate_rules()) == 0
