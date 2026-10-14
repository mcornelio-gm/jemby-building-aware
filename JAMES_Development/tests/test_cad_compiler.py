"""
Unit Tests for the IEEE CAD Single-Line Diagram Compiler & Symbol Library.
Verifies DXF generation, layer definitions, block registrations, and vector SVG exports.
"""

import pytest
import ezdxf
from james_app.cad_symbols import register_all_cad_symbols
from james_app.cad_compiler import SingleLineCadCompiler, export_facility_dxf, export_facility_svg


def test_cad_symbol_registration():
    """Verify all standard IEEE 315 blocks are registered in the drawing."""
    doc = ezdxf.new("R2018")
    register_all_cad_symbols(doc)

    expected_blocks = [
        "SYM_JUNCTION_DOT",
        "SYM_UTILITY_SOURCE",
        "SYM_GENERATOR",
        "SYM_SOLAR_PV",
        "SYM_BESS",
        "SYM_TRANSFORMER_2W",
        "SYM_CB_MOLDED_CASE",
        "SYM_CB_DRAWOUT",
        "SYM_FUSED_DISCONNECT",
        "SYM_ATS",
        "SYM_MOTOR_LOAD",
        "SYM_POWER_METER",
        "SYM_SPD"
    ]

    for block_name in expected_blocks:
        assert block_name in doc.blocks, f"Missing expected CAD block: {block_name}"


def test_cad_compiler_layers():
    """Verify AIA standard electrical CAD layers are created with correct lineweights and colors."""
    compiler = SingleLineCadCompiler(nodes=[], edges=[], client_id="TEST", facility_id="FAC1")
    doc = compiler.doc

    expected_layers = {
        "E-ELEC-BUS": 4,   # Cyan
        "E-ELEC-FEED": 7,  # White
        "E-ELEC-SYMB": 2,  # Yellow
        "E-ANNO-TEXT": 3,  # Green
        "E-ANNO-CABL": 1,  # Red
        "E-TTLB": 7        # White
    }

    for layer_name, expected_color in expected_layers.items():
        assert layer_name in doc.layers, f"Missing layer {layer_name}"
        layer = doc.layers.get(layer_name)
        assert layer.color == expected_color, f"Layer {layer_name} expected color {expected_color}, got {layer.color}"


def test_cad_compiler_dxf_and_svg_export():
    """Verify full DXF and SVG generation from mock facility data."""
    mock_nodes = [
        {"id": "UTIL_1", "tag": "UTIL-PGE", "domain": "sources", "voltage": "13.2 kV"},
        {"id": "XFRM_1", "tag": "T-1", "domain": "transformers", "kva": "1500 kVA", "voltage_primary": "13.2 kV", "voltage_secondary": "480Y/277V"},
        {"id": "SWBD_1", "tag": "MAIN-SWBD", "domain": "panels", "amps": "2000A", "voltage": "480Y/277V", "aic_rating": "65 kAIC"},
        {"id": "MTR_1", "tag": "PUMP-CHW-1", "domain": "loads", "type_tag": "MOTOR", "amps": "75A"}
    ]
    mock_edges = [
        {"source": "UTIL_1", "target": "XFRM_1"},
        {"source": "XFRM_1", "target": "SWBD_1"},
        {"source": "SWBD_1", "target": "MTR_1", "trip_amps": "100A", "conductor_size": "3#3 CU, 1#8 GND, 1-1/4\" C"}
    ]

    compiler = SingleLineCadCompiler(
        nodes=mock_nodes,
        edges=mock_edges,
        client_id="ZOETIS",
        facility_id="B4"
    )

    # 1. Test DXF export
    dxf_bytes = compiler.compile_dxf_bytes()
    assert isinstance(dxf_bytes, bytes)
    assert len(dxf_bytes) > 5000
    dxf_text = dxf_bytes.decode("utf-8")
    assert "SECTION" in dxf_text
    assert "BLOCKS" in dxf_text
    assert "E-ELEC-BUS" in dxf_text
    assert "MAIN-SWBD" in dxf_text
    assert "EOF" in dxf_text

    # 2. Test SVG export
    svg_str = compiler.compile_svg_string()
    assert isinstance(svg_str, str)
    assert svg_str.startswith("<?xml") or "<svg" in svg_str
    assert "</svg>" in svg_str
    assert len(svg_str) > 1000


def test_cad_compiler_dictionary_format():
    """Verify compiler gracefully handles dictionary-formatted nodes from JSON project files."""
    dict_project = {
        "nodes": {
            "GEN_1": {"type": "GEN", "label": "GEN-EMERG", "data": {"voltage": "480V", "kw": 750}},
            "ATS_1": {"type": "ATS", "label": "ATS-MAIN", "data": {"ampacity": 1200}}
        },
        "edges": {
            "E1": {"source": "GEN_1", "target": "ATS_1", "amps": "1200A"}
        }
    }

    dxf_bytes = export_facility_dxf(dict_project, "ABBOTT", "CENTRAL")
    assert len(dxf_bytes) > 5000

    svg_str = export_facility_svg(dict_project, "ABBOTT", "CENTRAL")
    assert "<svg" in svg_str


def test_cad_export_api_endpoints():
    """Test FastAPI REST endpoints for DXF and SVG download."""
    from fastapi.testclient import TestClient
    from james_app.main import app

    client = TestClient(app)

    # 1. Test DXF download endpoint
    resp_dxf = client.get("/api/clients/zoetis/facilities/b4/cad/dxf")
    assert resp_dxf.status_code == 200
    assert resp_dxf.headers["content-type"].startswith("application/dxf")
    assert "zoetis_b4_single_line.dxf" in resp_dxf.headers.get("content-disposition", "")
    assert len(resp_dxf.content) > 5000

    # 2. Test SVG preview endpoint
    resp_svg = client.get("/api/clients/zoetis/facilities/b4/cad/svg")
    assert resp_svg.status_code == 200
    assert resp_svg.headers["content-type"].startswith("image/svg+xml")
    assert "<svg" in resp_svg.text
    assert "</svg>" in resp_svg.text

    # 3. Test Sheets listing endpoint
    resp_sheets = client.get("/api/clients/zoetis/facilities/b4/cad/sheets")
    assert resp_sheets.status_code == 200
    sheets_data = resp_sheets.json()
    assert isinstance(sheets_data, list)
    assert any(s.get("sheet_id") == "all" for s in sheets_data)

    # 4. Test Large Facility Multi-Sheet Export
    resp_large_sheets = client.get("/api/clients/jemby/facilities/large_demo_bldg/cad/sheets")
    assert resp_large_sheets.status_code == 200
    large_sheets = resp_large_sheets.json()
    assert len(large_sheets) >= 2

    # 5. Test specific sheet SVG rendering
    resp_sheet_svg = client.get("/api/clients/jemby/facilities/large_demo_bldg/cad/svg?sheet=E-101")
    assert resp_sheet_svg.status_code == 200
    assert "<svg" in resp_sheet_svg.text

