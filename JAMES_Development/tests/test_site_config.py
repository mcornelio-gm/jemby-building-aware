"""Unit and Integration Tests for Site Configuration and 208V Facilities (Task #49)."""

import json
import pytest
from pathlib import Path
from fastapi.testclient import TestClient

from james_app.main import app
from james_app import db
from james_app.cad_compiler import SingleLineCadCompiler

client = TestClient(app)


@pytest.fixture(autouse=True)
def cleanup_test_facilities():
    """Ensure clean test state before and after each test."""
    yield
    db.delete_client_facility("test_client", "test_fac")
    db.delete_client_facility("test_client", "test_208v_site")
    db.delete_client_facility("test_co", "site_208")


def test_default_zoetis_b4_site_config():
    """Verify default authoritative site configuration for Zoetis Building 4."""
    config = db.get_site_config("zoetis", "b4")
    assert config is not None
    assert config["client_id"] == "zoetis"
    assert config["facility_id"] == "b4"
    assert "Zoetis Building 4" in config["facility_name"]
    assert "100 Campus Drive" in config["street_address"]
    assert config["city"] == "Florham Park"
    assert config["state"] == "NJ"
    assert "Jersey Central Power & Light" in config["utility_name"]
    assert "480Y/277V" in config["service_voltage"]
    assert config["primary_contact_name"] == "Benjie Craig"
    assert "Senior Electrical Facilities Manager" in config["primary_contact_title"]
    assert "(973) 555-0142" in config["primary_contact_phone"]


def test_save_and_retrieve_site_config():
    """Verify persisting and reading site configuration from SQLite and companion JSON."""
    c = "test_client"
    f = "test_fac"
    db.delete_client_facility(c, f)

    payload = {
        "facility_name": "East Coast Distribution Hub",
        "street_address": "450 Industrial Parkway",
        "city": "Secaucus",
        "state": "NJ",
        "postal_code": "07094",
        "country": "USA",
        "service_voltage": "208Y/120V 3Ø 4W",
        "service_amperage": 1200.0,
        "service_phase": 3,
        "service_wires": 4,
        "utility_name": "Public Service Electric & Gas (PSE&G)",
        "utility_account_number": "PSEG-991240-01",
        "utility_meter_number": "MTR-1200-EAST",
        "utility_transformer_id": "XFMR-NET-08",
        "primary_contact_name": "Alex Mercer",
        "primary_contact_title": "Facility Engineering Lead",
        "primary_contact_email": "alex.mercer@testclient.com",
        "primary_contact_phone": "(201) 555-0188",
        "emergency_contact_name": "Secaucus Security Control",
        "emergency_contact_phone": "(201) 555-0911",
        "facility_operating_hours": "M-F 6am - 10pm",
        "nec_edition": "NEC 2023",
        "arc_flash_status": "Verified / Compliant",
        "notes": "Direct 208Y/120V secondary network entrance."
    }

    saved = db.save_site_config(c, f, payload)
    assert saved["facility_name"] == "East Coast Distribution Hub"
    assert saved["service_voltage"] == "208Y/120V 3Ø 4W"
    assert saved["utility_name"] == "Public Service Electric & Gas (PSE&G)"
    assert saved["primary_contact_name"] == "Alex Mercer"

    # Verify companion JSON on disk
    json_path = db.get_site_config_path(c, f)
    assert json_path.exists()
    with open(json_path, "r", encoding="utf-8") as jf:
        disk_data = json.load(jf)
        assert disk_data["primary_contact_name"] == "Alex Mercer"
        assert disk_data["utility_meter_number"] == "MTR-1200-EAST"

    # Query afresh from DB
    retrieved = db.get_site_config(c, f)
    assert retrieved["facility_name"] == "East Coast Distribution Hub"
    assert retrieved["primary_contact_name"] == "Alex Mercer"
    assert retrieved["service_amperage"] == 1200.0
    assert "Secaucus" in retrieved["full_address"]


def test_site_config_rest_api_endpoints():
    """Verify GET and PUT /api/clients/{client_id}/facilities/{facility_id}/config endpoints."""
    # 1. GET default config
    resp = client.get("/api/clients/zoetis/facilities/b4/config")
    assert resp.status_code == 200
    b4_data = resp.json()
    assert b4_data["primary_contact_name"] == "Benjie Craig"
    assert "Jersey Central Power & Light" in b4_data["utility_name"]

    # 2. PUT custom site configuration
    c = "test_client"
    f = "test_fac"
    put_payload = {
        "facility_name": "Test Science Center",
        "street_address": "12 Research Boulevard",
        "city": "Cambridge",
        "state": "MA",
        "postal_code": "02142",
        "service_voltage": "208Y/120V 3Ø 4W",
        "service_amperage": 800.0,
        "utility_name": "Eversource Energy",
        "primary_contact_name": "Dr. Sarah Chen",
        "primary_contact_phone": "(617) 555-0391"
    }

    put_resp = client.put(f"/api/clients/{c}/facilities/{f}/config", json=put_payload)
    assert put_resp.status_code == 200
    put_data = put_resp.json()
    assert put_data["status"] == "success"
    assert put_data["config"]["facility_name"] == "Test Science Center"
    assert put_data["config"]["primary_contact_name"] == "Dr. Sarah Chen"

    # 3. GET back to verify persistence
    get_resp = client.get(f"/api/clients/{c}/facilities/{f}/config")
    assert get_resp.status_code == 200
    res_data = get_resp.json()
    assert res_data["facility_name"] == "Test Science Center"
    assert res_data["primary_contact_name"] == "Dr. Sarah Chen"
    assert res_data["utility_name"] == "Eversource Energy"
    assert res_data["service_voltage"] == "208Y/120V 3Ø 4W"


def test_208v_site_seed_creation():
    """Verify creating a 208Y/120V facility seeds realistic 208V equipment without 480V transformers."""
    c = "test_co"
    f = "site_208"
    db.delete_client_facility(c, f)

    create_res = db.create_client_facility(
        client_id=c,
        facility_id=f,
        seed=True,
        service_voltage="208Y/120V 3Ø 4W",
        site_config={
            "facility_name": "Downtown Commercial Tenant Unit",
            "utility_name": "ConEd",
            "primary_contact_name": "Marcus Vance"
        }
    )

    assert create_res["client_id"] == c
    assert create_res["facility_id"] == f
    assert create_res["seeded"] is True
    assert create_res["asset_count"] > 0

    # Query nodes in the 208V database
    with db.get_session(c, f) as session:
        nodes = session.query(db.NodeRecord).all()
        node_tags = [n.tag for n in nodes]
        node_voltages = [n.voltage for n in nodes]

        # Must have 208V equipment
        assert "UTIL-1" in node_tags
        assert "MSB-1" in node_tags
        assert "LP-1" in node_tags

        # Must NOT have 480V step-down transformer T-1 or 480V switchgear
        assert "T-1" not in node_tags
        for v in node_voltages:
            assert "480" not in v, f"Found unexpected 480V equipment in 208V-only facility: {v}"


def test_cad_compiler_title_block_dynamic_rendering():
    """Verify AutoCAD DXF and SVG title blocks dynamically display site configuration."""
    custom_cfg = {
        "facility_name": "BioTech Research Wing 3",
        "full_address": "88 Innovators Way, Boston, MA 02115",
        "service_voltage": "208Y/120V 3Ø 4W",
        "service_amperage": 1600.0,
        "utility_name": "National Grid",
        "primary_contact_name": "Benjie Craig",
        "primary_contact_phone": "(973) 555-0142",
        "nec_edition": "NEC 2023"
    }

    demo_nodes = db.get_208v_site_seed_assets()
    compiler = SingleLineCadCompiler(
        nodes=demo_nodes,
        edges=[],
        client_id="biotech",
        facility_id="wing3",
        sheet_size="36x24",
        site_config=custom_cfg
    )

    # Compile AutoCAD DXF bytes
    dxf_bytes = compiler.compile_dxf_bytes()
    assert dxf_bytes is not None
    assert b"BioTech Research Wing 3" in dxf_bytes
    assert b"88 Innovators Way" in dxf_bytes
    assert b"208Y/120V" in dxf_bytes
    assert b"National Grid" in dxf_bytes
    assert b"NEC 2023" in dxf_bytes

    # Compile SVG preview
    svg = compiler.compile_svg_string(theme="dark")
    assert svg is not None
    assert "<svg" in svg
    assert "</svg>" in svg

