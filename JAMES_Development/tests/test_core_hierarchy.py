"""Unit tests for the Core Electrical Object Hierarchy, Multi-View Projections, and Validation."""

import pytest
from james_app.core.base import BaseElectricalObject
from james_app.core.breaker import BreakerStatus, CircuitBreakerObject
from james_app.core.panel import MainsType, PanelboardObject, SystemType


def test_circuit_breaker_object_rules():
    """Test breaker validation rules."""
    bkr = CircuitBreakerObject(
        id="bkr_1",
        tag="CB-1",
        name="Lighting",
        slot_start=1,
        poles=1,
        occupied_slots=[1],
        amps=20,
        connected_phases=["A"]
    )
    assert isinstance(bkr, BaseElectricalObject)
    assert bkr.get_input_ports() == ["bus_stab_1"]
    assert bkr.get_output_ports() == ["ckt_1"]
    assert len(bkr.validate_rules()) == 0


def test_panelboard_object_multi_projections():
    """Test Panelboard creation, breaker placement, and all 3 visual projections."""
    panel = PanelboardObject.create_empty(
        panel_id="MDP_DEMO",
        tag="MDP-1",
        name="Main Distribution Panel",
        total_spaces=30,
        mains_rating_amps=400,
        system_type=SystemType.THREE_PHASE_208Y_120V
    )

    assert panel.total_spaces == 30
    assert len(panel.breakers) == 30

    # Add 1P and 3P Breakers
    panel.add_breaker(slot_start=1, poles=1, amps=20, description="Lighting Cir 1")
    panel.add_breaker(slot_start=3, poles=3, amps=50, description="RTU-1 Rooftop Unit", target_load_id="rtu_1")
    panel.downstream_loads["rtu_1"] = {"name": "RTU-1", "rating_label": "50A 3Ø"}

    # Add Upstream Feed
    panel.upstream_feed = {"id": "Utility_PGE", "name": "PG&E Service Grid", "voltage": "120/208V"}

    # 1. Test Focused Graphviz DOT Projection
    dot = panel.compile_focused_dot()
    assert "MAIN DISTRIBUTION PANEL (30 SPACES)" in dot
    assert 'ROWSPAN="3"' in dot
    assert "Utility_PGE -> Panel_MDP_DEMO:main" in dot
    assert "Panel_MDP_DEMO:ckt_3_5_7 -> Load_rtu_1" in dot

    # 2. Test Native HTML View Projection
    html_out = panel.render_html_view()
    assert '<table class="w-full text-xs border-collapse">' in html_out
    assert "MDP-1" in html_out
    assert 'rowspan="3"' in html_out

    # 3. Test PlantUML Single-Line Projection
    puml = panel.compile_plantuml_sld()
    assert "@startuml" in puml
    assert "Utility_PGE --> MDP_DEMO : Service Feed" in puml
    assert "MDP_DEMO --> CB_3 : Cir 3" in puml
    assert "@enduml" in puml

    # 4. Test Gemini AI Context Export
    ctx = panel.to_gemini_context()
    assert ctx["id"] == "MDP_DEMO"
    assert ctx["total_spaces"] == 30
    assert 3 in ctx["breakers"]
    assert ctx["breakers"][3]["poles"] == 3


def test_main_distribution_panel_subclass():
    """Test MainDistributionPanelObject subclass functionality and 3-pole distribution rules."""
    from james_app.core.panel import MainDistributionPanelObject

    mdp = MainDistributionPanelObject.create_empty(
        panel_id="MDP_MAIN_800A",
        tag="MDP-1",
        name="Main Power Distribution Panel",
        total_spaces=42,
        mains_rating_amps=800,
        system_type=SystemType.THREE_PHASE_480Y_277V
    )

    # Add 3-pole feeder breakers to subpanels
    mdp.add_feeder_breaker(slot_start=1, amps=225, target_panel_name="Panelboard LP-1", target_panel_id="LP_1")
    mdp.add_feeder_breaker(slot_start=7, amps=400, target_panel_name="Chiller Plant CH-1", target_panel_id="CH_1")

    assert isinstance(mdp, MainDistributionPanelObject)
    assert mdp.breakers[1].poles == 3
    assert mdp.breakers[1].amps == 225
    assert mdp.breakers[1].occupied_slots == [1, 3, 5]
    assert mdp.breakers[7].poles == 3
    assert mdp.breakers[7].occupied_slots == [7, 9, 11]

    dot = mdp.compile_focused_dot()
    assert "MAIN POWER DISTRIBUTION PANEL" in dot
    assert "800A" in dot
    assert 'ROWSPAN="3"' in dot

