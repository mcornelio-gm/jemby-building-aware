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
    dot = compile_facility_to_dot(sample_nodes)
    assert "digraph ElectricalOneLine {" in dot
    assert "subgraph cluster_s1 {" in dot
    assert "subgraph cluster_s4 {" in dot
    assert "s3_out:s -> s4_in:n" in dot
    assert "s2_out:s -> s3_emerg:n" in dot
