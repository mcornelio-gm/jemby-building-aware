"""Unit tests for CableObject (conductors) and GenericElectricalObject (placeholders)."""

import pytest
from james_app.core.base import BaseElectricalObject
from james_app.core.cable import CableObject, ConductorMaterial, ConduitType
from james_app.core.generic import GenericElectricalObject, GenericKind
from james_app.core.panel import PanelboardObject
from james_app.core.breaker import CircuitBreakerObject


def test_cable_object_calculations_and_rules():
    """Test cable ampacity, voltage drop calculations, and validation rules."""
    # 1. Standard 12 AWG branch circuit: 50ft, 16A on 120V
    cable = CableObject(
        id="cable_1",
        tag="C-1",
        name="Branch Run 1",
        gauge="12 AWG",
        material=ConductorMaterial.COPPER,
        length_ft=50.0,
        from_node_id="MDP_1",
        from_port_id="ckt_1",
        to_node_id="Load_1",
        to_port_id="in",
        load_amps=16.0,
        nominal_voltage=120.0
    )

    assert isinstance(cable, BaseElectricalObject)
    assert cable.base_ampacity == 25  # 12 AWG 75°C Cu is 25A
    vd = cable.calculate_voltage_drop()
    assert vd["drop_pct"] < 3.0  # Should be well under 3% for 50ft
    assert len(cable.validate_rules()) == 0

    # 2. Test Parallel Feeders (2x 4/0 AWG Cu)
    feeder = CableObject(
        id="feeder_main",
        tag="F-MAIN",
        name="Main Service Feeder",
        gauge="4/0 AWG",
        sets=2,
        length_ft=150.0,
        from_node_id="Utility",
        from_port_id="out",
        to_node_id="MDP_1",
        to_port_id="main",
        load_amps=350.0,
        nominal_voltage=480.0
    )
    assert feeder.base_ampacity == 460  # 230A * 2 = 460A

    # 3. Test Voltage Drop Exceedance Warning
    long_cable = CableObject(
        id="long_cable",
        tag="C-LONG",
        name="Long Parking Lot Run",
        gauge="12 AWG",
        length_ft=400.0,  # 400ft will cause significant drop
        from_node_id="MDP_1",
        from_port_id="ckt_2",
        to_node_id="Light_Pole",
        to_port_id="in",
        load_amps=18.0,
        nominal_voltage=120.0
    )
    warnings = long_cable.validate_rules()
    assert any("Voltage drop" in w for w in warnings)

    # 4. Test Visual Projections
    dot = cable.compile_focused_dot()
    assert "MDP_1:ckt_1 -> Load_1:in" in dot
    assert "12 AWG Cu" in dot

    puml = cable.compile_plantuml_sld()
    assert "MDP_1 --> Load_1" in puml


def test_generic_electrical_object_and_promotion():
    """Test generic placeholder object, multi-views, and class promotion helpers."""
    gen = GenericElectricalObject(
        id="load_pump_future",
        tag="PUMP-X",
        name="Future Booster Pump",
        generic_kind=GenericKind.MOTOR,
        voltage="208V 3Ø",
        current_amps=30.0,
        power_kva=10.8
    )

    assert isinstance(gen, BaseElectricalObject)
    assert gen.get_input_ports() == ["in", "L1", "L2"]
    assert len(gen.validate_rules()) == 0

    # 1. Test Visual Projections
    dot = gen.compile_focused_dot()
    assert "Future Booster Pump" in dot
    assert "MOTOR / MACHINERY" in dot
    assert "dashed" in dot

    html_out = gen.render_html_view()
    assert "Future Booster Pump" in html_out
    assert "Promote Class" in html_out

    # 2. Test Promotion to PanelboardObject
    panel = gen.promote_to_panel(total_spaces=30, mains_amps=100)
    assert isinstance(panel, PanelboardObject)
    assert panel.id == "load_pump_future"
    assert panel.total_spaces == 30

    # 3. Test Promotion to CircuitBreakerObject
    bkr = gen.promote_to_breaker(slot_start=5, poles=2)
    assert isinstance(bkr, CircuitBreakerObject)
    assert bkr.id == "load_pump_future"
    assert bkr.poles == 2
    assert bkr.occupied_slots == [5, 7]
    assert bkr.amps == 30
