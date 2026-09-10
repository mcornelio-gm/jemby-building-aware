"""Unit tests for Graphviz DOT Compiler Engine."""

from james_app.dot_compiler import compile_project_to_dot, compile_facility_to_dot
from james_app.storage import load_project


def test_compile_zoetis_project():
    project = load_project("zoetis_b4")
    assert project is not None
    
    dot_output = compile_project_to_dot(project)
    
    # Assert structural Graphviz headers
    assert "digraph SLD {" in dot_output
    assert "rankdir=TB" in dot_output
    
    # Assert nodes are present
    assert "XFMR_PGE [" in dot_output
    assert "SWBD_MSA [" in dot_output
    assert "ATS_1 [" in dot_output
    assert "SWBD_MSB2 [" in dot_output
    
    # Assert ports and edge formatting
    assert "SWBD_MSB2:p2 -> PNL_M1:in" in dot_output
    assert "CB-MAIN-MSA" in dot_output or "CB-SWBD-MSB-2" in dot_output


def test_compile_facility_to_dot():
    sample_nodes = [
        {"id": "s1", "tag": "UTIL-1", "name": "Utility Grid", "domain": "sources", "type_tag": "UTIL", "voltage": "480Y/277V", "amps": 2500},
        {"id": "s2", "tag": "GEN-1", "name": "Generator", "domain": "sources", "type_tag": "GEN", "voltage": "480V", "amps": 1000},
        {"id": "s3", "tag": "ATS-1", "name": "Transfer Switch", "domain": "switches", "type_tag": "ATS", "fed_from": "UTIL-1", "voltage": "480V", "amps": 400},
        {"id": "s4", "tag": "MDP-1", "name": "Main Panel", "domain": "panels", "type_tag": "MDP", "fed_from": "ATS-1", "is_panel": True, "voltage": "480V", "amps": 1200},
    ]
    # 1. Detailed Mode
    dot_detailed = compile_facility_to_dot(sample_nodes, mode="detailed")
    assert "digraph ElectricalOneLine {" in dot_detailed
    assert "subgraph cluster_s1 {" in dot_detailed
    assert "subgraph cluster_s4 {" in dot_detailed
    assert "s3_out:s -> s4_in:n" in dot_detailed
    assert "s2_out:s -> s3_emerg:n" in dot_detailed

    # 2. Macro Mode (Consolidated Single Nodes with Arrowtail & Arrowhead Labels)
    dot_macro = compile_facility_to_dot(sample_nodes, mode="macro")
    assert "digraph ElectricalOneLine {" in dot_macro
    assert "subgraph cluster_" not in dot_macro
    assert "s1 [label=" in dot_macro
    assert "s4 [label=" in dot_macro
    assert "s3 -> s4 [" in dot_macro
    assert 'taillabel=<' in dot_macro and 'Load Out' in dot_macro
    assert 'headlabel=<' in dot_macro and ('Main Lugs' in dot_macro or 'Line In' in dot_macro)
    assert "s2 -> s3 [" in dot_macro
    assert 'taillabel=<' in dot_macro and 'Gen Breaker' in dot_macro
    assert 'headlabel=<' in dot_macro and 'Emerg In' in dot_macro


def test_compile_multi_source_upstream_feeds():
    nodes = [
        {"id": "s1", "tag": "UTIL-1", "name": "Utility Grid", "domain": "sources", "type_tag": "UTIL", "voltage": "480Y/277V", "amps": 2500},
        {"id": "s2", "tag": "GEN-1", "name": "Generator", "domain": "sources", "type_tag": "GEN", "voltage": "480V", "amps": 1000},
        {"id": "s3", "tag": "GEN-2", "name": "Backup Generator", "domain": "sources", "type_tag": "GEN", "voltage": "480V", "amps": 800},
        {
            "id": "s4",
            "tag": "ATS-1",
            "name": "Transfer Switch",
            "domain": "switches",
            "type_tag": "ATS",
            "fed_from": "UTIL-1",
            "attributes": {
                "upstream_sources": ["UTIL-1", "GEN-1", "GEN-2"]
            },
            "voltage": "480V",
            "amps": 800
        },
    ]

    # Detailed Mode
    dot_detailed = compile_facility_to_dot(nodes, mode="detailed")
    assert "s1_out:s -> s4_norm:n" in dot_detailed
    assert "s2_out:s -> s4_emerg:n" in dot_detailed

    # Macro Mode
    dot_macro = compile_facility_to_dot(nodes, mode="macro")
    assert "s1 -> s4 [" in dot_macro
    assert "s2 -> s4 [" in dot_macro
    assert "s3 -> s4 [" in dot_macro
    assert "Emerg In" in dot_macro


def test_compile_breaker_to_downstream_object_link():
    nodes = [
        {
            "id": "mdp_node",
            "tag": "MDP-1",
            "name": "Main Distribution Panel",
            "domain": "panels",
            "type_tag": "MDP",
            "is_panel": True,
            "slots": 42,
            "attributes": {
                "schedule": [
                    {
                        "leftSlot": 1,
                        "leftDesc": "Feeder to LP-1",
                        "leftTrip": "100",
                        "leftPoles": 3,
                        "leftType": "MCCB",
                        "leftTargetLoad": "LP-1"
                    },
                    {
                        "leftSlot": 7,
                        "leftDesc": "Feeder to T-1",
                        "leftTrip": "100",
                        "leftPoles": 3,
                        "leftType": "MCCB",
                        "leftTargetLoad": "T-1"
                    }
                ]
            }
        },
        {
            "id": "lp_node",
            "tag": "LP-1",
            "name": "Lighting Panel",
            "domain": "panels",
            "type_tag": "LP",
            "is_panel": True,
            "slots": 42,
            "fed_from": "MDP-1",
            "attributes": {}
        },
        {
            "id": "xfmr_node",
            "tag": "T-1",
            "name": "Step Down Transformer",
            "domain": "transformers",
            "type_tag": "XFMR",
            "fed_from": "",  # Unset fed_from, but discovered from MDP-1 schedule breaker
            "attributes": {}
        }
    ]

    # Test Detailed SLD (Direct breaker port connections)
    dot_detailed = compile_facility_to_dot(nodes, mode="detailed")
    assert "mdp_node_b1:s -> lp_node_in:n" in dot_detailed
    assert "mdp_node_b7:s -> xfmr_node_in:n" in dot_detailed

    # Test Macro SLD (Tail labels with slot ranges and trip ratings)
    dot_macro = compile_facility_to_dot(nodes, mode="macro")
    assert "mdp_node -> lp_node [" in dot_macro
    assert "Spaces 1, 3, 5 • 100A/3P" in dot_macro
    assert "mdp_node -> xfmr_node [" in dot_macro
    assert "Spaces 7, 9, 11 • 100A/3P" in dot_macro


def test_compile_device_clean_title_no_pencil_indicator():
    sample_nodes = [
        {"id": "pnl_1", "tag": "PANEL-A", "name": "Lighting Panel A", "domain": "panels", "type_tag": "LP", "is_panel": True, "voltage": "208Y/120V", "amps": 225},
        {"id": "xfmr_1", "tag": "XFMR-1", "name": "480-208V Transformer", "domain": "transformers", "type_tag": "XFMR", "voltage": "480V-208V", "amps": 150},
    ]
    # In Detailed mode, device cluster header has clean title without [ ✎ ]
    dot_detailed = compile_facility_to_dot(sample_nodes, mode="detailed")
    assert "[ ✎ ]" not in dot_detailed
    assert "PANEL-A" in dot_detailed

    # In Macro mode, node label has clean title without [ ✎ ]
    dot_macro = compile_facility_to_dot(sample_nodes, mode="macro")
    assert "[ ✎ ]" not in dot_macro
    assert "PANEL-A" in dot_macro


def test_compile_feeder_edge_attributes_and_badge():
    nodes = [
        {"id": "s1", "tag": "MDP-1", "name": "Main Switchboard", "domain": "panels", "type_tag": "MDP", "is_panel": True, "voltage": "480Y/277V", "amps": 1200},
        {
            "id": "s2",
            "tag": "LP-1",
            "name": "Lighting Panel 1",
            "domain": "panels",
            "type_tag": "LP",
            "is_panel": True,
            "fed_from": "MDP-1",
            "voltage": "208Y/120V",
            "amps": 225,
            "attributes": {
                "conductor": "4/0",
                "conductor_material": "Cu",
                "sets": 1,
                "length_ft": 120,
                "voltage_drop_pct": 1.45
            }
        }
    ]
    # 1. Detailed Mode
    dot_detailed = compile_facility_to_dot(nodes, mode="detailed")
    assert 'class="feeder-edge"' in dot_detailed
    assert 'id="edge_s1_s2"' in dot_detailed
    assert "(4/0 Cu)" in dot_detailed
    assert "120ft" in dot_detailed
    assert "1.5% ΔV" in dot_detailed or "1.4% ΔV" in dot_detailed

    # 2. Macro Mode
    dot_macro = compile_facility_to_dot(nodes, mode="macro")
    assert 'class="feeder-edge"' in dot_macro
    assert 'id="edge_s1_s2"' in dot_macro
    assert "(4/0 Cu)" in dot_macro
    assert "120ft" in dot_macro
    assert "1.5% ΔV" in dot_macro or "1.4% ΔV" in dot_macro

