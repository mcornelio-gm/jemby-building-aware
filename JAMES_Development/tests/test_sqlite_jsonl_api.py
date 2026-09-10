"""Unit tests for multi-tenant SQLite + JSONL layer and FastAPI cockpit endpoints."""

from pathlib import Path
import shutil
import pytest
from fastapi.testclient import TestClient

from james_app.main import app
from james_app import db

client = TestClient(app)

TEST_CLIENT_ID = "test_fixture_client"
TEST_FACILITY_ID = "test_fixture_b4"


@pytest.fixture(autouse=True)
def setup_and_teardown_test_facility():
    """Ensure tests run against an isolated test facility database and clean up after."""
    db.seed_demo_facility(TEST_CLIENT_ID, TEST_FACILITY_ID)
    yield
    p = Path("data/clients") / TEST_CLIENT_ID
    if p.exists():
        shutil.rmtree(p, ignore_errors=True)


def test_sqlite_db_and_jsonl_isolation():
    client_id = "test_isolation_client"
    facility_id = "facility_a"

    # Seed demo facility
    db.seed_demo_facility(client_id, facility_id)

    db_path = db.get_db_path(client_id, facility_id)
    jsonl_path = db.get_jsonl_path(client_id, facility_id)

    assert db_path.exists()
    assert jsonl_path.exists()

    with db.get_session(client_id, facility_id) as session:
        nodes = session.query(db.NodeRecord).all()
        assert len(nodes) >= 9
        ats = session.query(db.NodeRecord).filter_by(tag="ATS-1").first()
        assert ats is not None
        assert ats.domain == "switches"
        assert ats.amps == 400.0

    # Cleanup
    p = Path("data/clients") / client_id
    if p.exists():
        shutil.rmtree(p, ignore_errors=True)


def test_api_survey_view():
    res = client.get("/survey")
    assert res.status_code == 200
    assert "Building Aware" in res.text

    # Backwards compatibility alias
    res_legacy = client.get("/cockpit")
    assert res_legacy.status_code == 200


def test_api_get_nodes():
    res = client.get(f"/api/clients/{TEST_CLIENT_ID}/facilities/{TEST_FACILITY_ID}/nodes")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) >= 9
    tags = [item["tag"] for item in data]
    assert "UTIL-1" in tags
    assert "ATS-1" in tags
    assert "MDP-1" in tags


def test_api_upsert_and_delete_node():
    new_node = {
        "id": "test_pump_1",
        "tag": "PUMP-101",
        "name": "Chilled Water Circulation Pump",
        "domain": "loads",
        "object_class": "MotorEquipmentObject",
        "type_tag": "MOTOR",
        "type_name": "Three-Phase Induction Motor",
        "room": "Mechanical Basement",
        "fed_from": "MCC-1",
        "voltage": "480V 3Ø",
        "amps": 45.0,
        "aic": 65.0,
        "is_panel": False,
        "slots": 0,
        "attributes": {"hp": 40.0, "fla": 45.0}
    }

    # Upsert
    res = client.post(f"/api/clients/{TEST_CLIENT_ID}/facilities/{TEST_FACILITY_ID}/nodes", json=new_node)
    assert res.status_code == 200
    assert res.json()["status"] == "success"

    # Verify present
    res2 = client.get(f"/api/clients/{TEST_CLIENT_ID}/facilities/{TEST_FACILITY_ID}/nodes")
    tags = [item["tag"] for item in res2.json()]
    assert "PUMP-101" in tags

    # Verify JSONL export
    res_jsonl = client.get(f"/api/clients/{TEST_CLIENT_ID}/facilities/{TEST_FACILITY_ID}/export/jsonl")
    assert res_jsonl.status_code == 200
    assert "PUMP-101" in res_jsonl.text

    # Delete
    res_del = client.delete(f"/api/clients/{TEST_CLIENT_ID}/facilities/{TEST_FACILITY_ID}/nodes/test_pump_1")
    assert res_del.status_code == 200

    # Verify deleted
    res3 = client.get(f"/api/clients/{TEST_CLIENT_ID}/facilities/{TEST_FACILITY_ID}/nodes")
    tags_after = [item["tag"] for item in res3.json()]
    assert "PUMP-101" not in tags_after


def test_api_unique_tag_enforcement():
    # Attempt to insert a new node with duplicate tag 'MDP-1'
    duplicate_node = {
        "id": "new_fake_mdp",
        "tag": "MDP-1",
        "name": "Another Main Distribution Panel",
        "domain": "panels",
        "object_class": "MainDistributionPanelObject",
        "type_tag": "MDP",
        "type_name": "Main Distribution Panel",
        "room": "Room 102",
        "voltage": "480Y/277V 3Ø 4W",
        "amps": 1200.0,
        "aic": 65.0,
        "is_panel": True,
        "slots": 42
    }
    res_dup = client.post(f"/api/clients/{TEST_CLIENT_ID}/facilities/{TEST_FACILITY_ID}/nodes", json=duplicate_node)
    assert res_dup.status_code == 400
    assert res_dup.json()["error"] == "DUPLICATE_TAG"

    # Updating existing node 's4' (which owns 'MDP-1') should succeed
    update_s4 = {
        "id": "s4",
        "tag": "MDP-1",
        "name": "Main Distribution Switchboard Updated",
        "domain": "panels",
        "object_class": "MainDistributionPanelObject",
        "type_tag": "MDP",
        "type_name": "Main Distribution Panel",
        "room": "Level 1 - Main Electric Room 101",
        "fed_from": "ATS-1",
        "voltage": "480Y/277V 3Ø 4W",
        "amps": 1200.0,
        "aic": 65.0,
        "is_panel": True,
        "slots": 42
    }
    res_valid = client.post(f"/api/clients/{TEST_CLIENT_ID}/facilities/{TEST_FACILITY_ID}/nodes", json=update_s4)
    assert res_valid.status_code == 200
    assert res_valid.json()["status"] == "success"


def test_api_facility_dot_and_sld():
    # Test DOT endpoint (defaults to macro view)
    res_dot = client.get(f"/api/clients/{TEST_CLIENT_ID}/facilities/{TEST_FACILITY_ID}/dot")
    assert res_dot.status_code == 200
    assert "MDP-1" in res_dot.text

    # Test DOT endpoint with detailed mode
    res_dot_detailed = client.get(f"/api/clients/{TEST_CLIENT_ID}/facilities/{TEST_FACILITY_ID}/dot?mode=detailed")
    assert res_dot_detailed.status_code == 200
    assert "subgraph cluster_" in res_dot_detailed.text
    assert "MDP-1" in res_dot_detailed.text

    # Test HTML SLD Viewer endpoint
    res_sld = client.get(f"/clients/{TEST_CLIENT_ID}/facilities/{TEST_FACILITY_ID}/sld")
    assert res_sld.status_code == 200
    assert "Building Aware" in res_sld.text
    assert "Single-Line Diagram" in res_sld.text
    assert "d3-graphviz" in res_sld.text


def test_api_update_node_multi_source_upstream():
    update_ats = {
        "id": "s3",
        "tag": "ATS-1",
        "name": "Automatic Transfer Switch",
        "domain": "switches",
        "object_class": "AutomaticTransferSwitchObject",
        "type_tag": "ATS",
        "type_name": "Automatic Transfer Switch (ATS)",
        "room": "Main Electrical Room 101",
        "fed_from": "UTIL-1",
        "voltage": "480Y/277V 3Ø 4W",
        "amps": 400.0,
        "aic": 65.0,
        "is_panel": False,
        "slots": 0,
        "attributes": {
            "fed_from": "UTIL-1",
            "upstream_sources": ["UTIL-1", "GEN-1"],
            "emergency_source": "GEN-1",
            "transition": "Open Transition"
        }
    }
    res = client.post(f"/api/clients/{TEST_CLIENT_ID}/facilities/{TEST_FACILITY_ID}/nodes", json=update_ats)
    assert res.status_code == 200
    assert res.json()["status"] == "success"

    # Fetch nodes and verify upstream_sources and emergency_source persisted
    res_get = client.get(f"/api/clients/{TEST_CLIENT_ID}/facilities/{TEST_FACILITY_ID}/nodes")
    assert res_get.status_code == 200
    ats_node = next((n for n in res_get.json() if n["id"] == "s3"), None)
    assert ats_node is not None
    assert ats_node["fed_from"] == "UTIL-1"
    assert ats_node["attributes"]["upstream_sources"] == ["UTIL-1", "GEN-1"]
    assert ats_node["attributes"]["emergency_source"] == "GEN-1"


def test_api_custom_breakers_tracking():
    # Insert a panel with custom/uncataloged breakers in schedule
    custom_panel = {
        "id": "panel_custom_test",
        "tag": "LP-CUSTOM",
        "name": "Lighting Panel with Custom Breakers",
        "domain": "panels",
        "object_class": "LightingPanelboardObject",
        "type_tag": "LP",
        "type_name": "Lighting Panelboard",
        "room": "Electrical Room 102",
        "fed_from": "MDP-1",
        "voltage": "208Y/120V 3Ø 4W",
        "amps": 225.0,
        "aic": 10.0,
        "is_panel": True,
        "slots": 12,
        "attributes": {
            "schedule": [
                {
                    "leftSlot": 1,
                    "leftDesc": "Specialized Lab Oven",
                    "leftTrip": "30",
                    "leftPoles": 2,
                    "leftType": "MCCB",
                    "leftWire": "10 AWG Cu",
                    "leftPartNo": "CUST-EATON-30A-SPECIAL",
                    "leftMfr": "Eaton",
                    "leftIsCustom": True,
                    "leftCatalogStatus": "custom_pending",
                    "rightSlot": 2,
                    "rightDesc": "Standard Outlet",
                    "rightTrip": "20",
                    "rightPoles": 1,
                    "rightType": "MCCB",
                    "rightWire": "12 AWG Cu",
                    "rightPartNo": "QO120",
                    "rightMfr": "Square D / Schneider Electric",
                    "rightIsCustom": False,
                    "rightCatalogStatus": "verified"
                }
            ]
        }
    }
    res = client.post(f"/api/clients/{TEST_CLIENT_ID}/facilities/{TEST_FACILITY_ID}/nodes", json=custom_panel)
    assert res.status_code == 200

    # Test facility-scoped custom breakers endpoint
    res_cust = client.get(f"/api/clients/{TEST_CLIENT_ID}/facilities/{TEST_FACILITY_ID}/custom-breakers")
    assert res_cust.status_code == 200
    data = res_cust.json()
    assert isinstance(data, list)
    cust_item = next((b for b in data if b["part_number"] == "CUST-EATON-30A-SPECIAL"), None)
    assert cust_item is not None
    assert cust_item["manufacturer"] == "Eaton"
    assert cust_item["trip_amps"] == 30.0
    assert cust_item["poles"] == 2
    assert cust_item["is_custom"] is True
    assert cust_item["catalog_status"] == "custom_pending"
    assert cust_item["occurrences"] >= 1
    assert any(loc["panel_tag"] == "LP-CUSTOM" and loc["slot"] == 1 for loc in cust_item["discovered_locations"])

    # Test global catalog custom breakers endpoint
    res_global = client.get(f"/api/catalog/custom-breakers?client_id={TEST_CLIENT_ID}&facility_id={TEST_FACILITY_ID}")
    assert res_global.status_code == 200
    global_item = next((b for b in res_global.json() if b["part_number"] == "CUST-EATON-30A-SPECIAL"), None)
    assert global_item is not None
    assert global_item["is_custom"] is True

    # Cleanup
    client.delete(f"/api/clients/{TEST_CLIENT_ID}/facilities/{TEST_FACILITY_ID}/nodes/panel_custom_test")






