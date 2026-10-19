import pytest
from james_app.dot_compiler import compile_facility_to_dot
from james_app.db import get_session, NodeRecord

def test_dot_compiler_renewables_solar():
    nodes = [
        {
            "id": "pv_mod_1",
            "tag": "PV-MOD-1",
            "name": "Solar PV Array",
            "domain": "renewables",
            "type_tag": "PV-MOD",
            "fed_from": None,
            "voltage": "600V DC",
            "amps": 50.0,
            "aic": 10.0,
            "attributes": {}
        },
        {
            "id": "pv_inv_1",
            "tag": "PV-1",
            "name": "Solar PV Inverter",
            "domain": "renewables",
            "type_tag": "PV",
            "fed_from": "PV-MOD-1",
            "voltage": "480V 3Ø",
            "amps": 125.0,
            "aic": 22.0,
            "attributes": {"upstream_sources": ["PV-MOD-1"]}
        },
        {
            "id": "panel_mdp",
            "tag": "MDP-1",
            "name": "Main Distribution Panel",
            "domain": "panels",
            "type_tag": "MDP",
            "fed_from": "PV-1",
            "voltage": "480Y/277V",
            "amps": 800.0,
            "aic": 65.0,
            "is_panel": True,
            "attributes": {"upstream_sources": ["PV-1"]}
        }
    ]
    dot_str = compile_facility_to_dot(nodes, mode="detailed")
    assert "PV-MOD-1" in dot_str
    assert "PV-1" in dot_str
    assert "MDP-1" in dot_str
    assert "Inverter AC Out" in dot_str
    assert "DC Array Output" in dot_str
