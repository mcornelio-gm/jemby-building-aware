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


def test_cad_compiler_sheet_sizes():
    """Verify 36x24 (ANSI D) and 42x30 (ARCH E1) dimensions and title block annotations."""
    mock_nodes = [
        {"id": "UTIL_1", "tag": "UTIL-1", "domain": "sources"},
        {"id": "SWBD_1", "tag": "MSB-1", "domain": "distribution", "fed_from": "UTIL-1"}
    ]
    mock_edges = [{"source": "UTIL_1", "target": "SWBD_1"}]

    # 1. Test 36x24 ANSI D
    c_36 = SingleLineCadCompiler(nodes=mock_nodes, edges=mock_edges, sheet_size="36x24")
    assert c_36.sheet_width == 864.0
    assert c_36.sheet_height == 558.0
    assert "ANSI D" in c_36.sheet_size_label
    dxf_36 = c_36.compile_dxf_bytes().decode("utf-8")
    assert "ANSI D" in dxf_36

    # 2. Test 42x30 ARCH E1
    c_42 = SingleLineCadCompiler(nodes=mock_nodes, edges=mock_edges, sheet_size="42x30")
    assert c_42.sheet_width == 1066.8
    assert c_42.sheet_height == 762.0
    assert "ARCH E1" in c_42.sheet_size_label
    dxf_42 = c_42.compile_dxf_bytes().decode("utf-8")
    assert "ARCH E1" in dxf_42


def test_cad_compiler_themes():
    """Verify light architectural print and dark CAD blueprint SVG rendering."""
    mock_nodes = [
        {"id": "UTIL_1", "tag": "UTIL-1", "domain": "sources"},
        {"id": "SWBD_1", "tag": "MSB-1", "domain": "distribution", "fed_from": "UTIL-1"}
    ]
    mock_edges = [{"source": "UTIL_1", "target": "SWBD_1"}]

    compiler = SingleLineCadCompiler(nodes=mock_nodes, edges=mock_edges)

    # 1. Dark Theme
    svg_dark = compiler.compile_svg_string(theme="dark")
    assert 'fill="#070A12"' in svg_dark or 'fill="#070a12"' in svg_dark

    # 2. Light Theme
    compiler_light = SingleLineCadCompiler(nodes=mock_nodes, edges=mock_edges)
    svg_light = compiler_light.compile_svg_string(theme="light")
    assert 'fill="#FFFFFF"' in svg_light or 'fill="#ffffff"' in svg_light
    # Check light theme palette colors
    assert "#0284C7" in svg_light or "#0284c7" in svg_light  # Bus
    assert "#0F172A" in svg_light or "#0f172a" in svg_light  # Feed / TTLB


def test_cad_api_theme_and_size_parameters():
    """Test API query parameters for theme (light/dark) and sheet size (36x24/42x30)."""
    from fastapi.testclient import TestClient
    from james_app.main import app

    client = TestClient(app)

    # 1. Test SVG with light theme and 42x30 size
    resp_svg = client.get("/api/clients/zoetis/facilities/b4/cad/svg?theme=light&size=42x30")
    assert resp_svg.status_code == 200
    assert "image/svg+xml" in resp_svg.headers["content-type"]
    svg_text = resp_svg.text
    assert "<svg" in svg_text
    assert 'fill="#FFFFFF"' in svg_text or 'fill="#ffffff"' in svg_text
    assert '1066.8mm' in svg_text
    assert '762mm' in svg_text

    # 2. Test DXF download with 42x30 size
    resp_dxf = client.get("/api/clients/zoetis/facilities/b4/cad/dxf?size=42x30")
    assert resp_dxf.status_code == 200
    assert "application/dxf" in resp_dxf.headers["content-type"]
    assert "zoetis_b4_42x30_single_line.dxf" in resp_dxf.headers.get("content-disposition", "")
    dxf_content = resp_dxf.content.decode("utf-8")
    assert "ARCH E1" in dxf_content


def test_cad_high_contrast_mode():
    """Verify high contrast monochrome rendering (white on black and black on white)."""
    mock_nodes = [
        {"id": "UTIL_1", "tag": "UTIL-1", "domain": "sources"},
        {"id": "SWBD_1", "tag": "MSB-1", "domain": "distribution", "fed_from": "UTIL-1", "rating": "2000A", "voltage": "480V"}
    ]
    mock_edges = [{"source": "UTIL_1", "target": "SWBD_1"}]

    # 1. High Contrast Dark: #000000 bg with #FFFFFF linework
    compiler_hc_dark = SingleLineCadCompiler(nodes=mock_nodes, edges=mock_edges, high_contrast=True)
    svg_hc_dark = compiler_hc_dark.compile_svg_string(theme="dark", high_contrast=True)
    assert 'fill="#000000"' in svg_hc_dark or 'fill="#000"' in svg_hc_dark
    assert '#FFFFFF' in svg_hc_dark or '#ffffff' in svg_hc_dark

    # 2. High Contrast Light: #FFFFFF bg with #000000 linework
    compiler_hc_light = SingleLineCadCompiler(nodes=mock_nodes, edges=mock_edges, high_contrast=True)
    svg_hc_light = compiler_hc_light.compile_svg_string(theme="light", high_contrast=True)
    assert 'fill="#FFFFFF"' in svg_hc_light or 'fill="#ffffff"' in svg_hc_light
    assert '#000000' in svg_hc_light or '#000' in svg_hc_light

    # 3. DXF monochrome layer ACI 7
    dxf_hc = compiler_hc_dark.compile_dxf_bytes().decode("utf-8")
    assert "E-ELEC-BUS" in dxf_hc


def test_cad_label_formatting():
    """Verify linear and stacked equipment and bus label formatting."""
    mock_nodes = [
        {
            "id": "UTIL_1",
            "tag": "UTIL-1",
            "domain": "sources",
            "voltage": "13.8kV",
            "source_type": "utility"
        },
        {
            "id": "SWBD_1",
            "tag": "MSB-1",
            "domain": "distribution",
            "fed_from": "UTIL-1",
            "rating": "3000A",
            "voltage": "480Y/277V",
            "aic_rating": "65kAIC"
        },
        {
            "id": "XFMR_1",
            "tag": "T-1",
            "domain": "distribution",
            "fed_from": "SWBD_1",
            "type": "transformer",
            "rating": "1500kVA",
            "primary_voltage": "13.8kV",
            "secondary_voltage": "480V"
        }
    ]
    mock_edges = [
        {"source": "UTIL_1", "target": "SWBD_1"},
        {"source": "SWBD_1", "target": "XFMR_1"}
    ]

    # 1. Linear format
    compiler_linear = SingleLineCadCompiler(nodes=mock_nodes, edges=mock_edges, label_format="linear")
    dxf_linear = compiler_linear.compile_dxf_bytes().decode("utf-8")
    assert "MSB-1" in dxf_linear
    assert "T-1" in dxf_linear

    # 2. Stacked format
    compiler_stacked = SingleLineCadCompiler(nodes=mock_nodes, edges=mock_edges, label_format="stacked")
    dxf_stacked = compiler_stacked.compile_dxf_bytes().decode("utf-8")
    assert "MSB-1" in dxf_stacked
    assert "3000A" in dxf_stacked
    assert "T-1" in dxf_stacked
    assert "1500kVA" in dxf_stacked


def test_cad_api_contrast_and_label_parameters():
    """Test API query parameters for contrast and label formatting."""
    from fastapi.testclient import TestClient
    from james_app.main import app

    client = TestClient(app)

    # 1. Test SVG with high contrast and stacked labels
    resp_svg = client.get("/api/clients/zoetis/facilities/b4/cad/svg?contrast=high&labels=stacked&theme=dark")
    assert resp_svg.status_code == 200
    assert "image/svg+xml" in resp_svg.headers["content-type"]
    svg_text = resp_svg.text
    assert "<svg" in svg_text
    assert 'fill="#000000"' in svg_text or 'fill="#000"' in svg_text

    # 2. Test DXF download with high contrast (appends _mono to filename)
    resp_dxf = client.get("/api/clients/zoetis/facilities/b4/cad/dxf?contrast=high&labels=stacked")
    assert resp_dxf.status_code == 200
    assert "application/dxf" in resp_dxf.headers["content-type"]
    assert "zoetis_b4_mono_single_line.dxf" in resp_dxf.headers.get("content-disposition", "")



