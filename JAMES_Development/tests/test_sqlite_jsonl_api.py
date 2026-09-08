"""Unit tests for multi-tenant SQLite + JSONL layer and FastAPI cockpit endpoints."""

from pathlib import Path
import pytest
from fastapi.testclient import TestClient

from james_app.main import app
from james_app import db

client = TestClient(app)


def test_sqlite_db_and_jsonl_isolation(tmp_path):
    client_id = "test_client"
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


def test_api_survey_view():
    res = client.get("/survey")
    assert res.status_code == 200
    assert "Building Aware" in res.text

    # Backwards compatibility alias
    res_legacy = client.get("/cockpit")
    assert res_legacy.status_code == 200


def test_api_get_nodes():
    res = client.get("/api/clients/zoetis/facilities/b4/nodes")
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
    res = client.post("/api/clients/zoetis/facilities/b4/nodes", json=new_node)
    assert res.status_code == 200
    assert res.json()["status"] == "success"

    # Verify present
    res2 = client.get("/api/clients/zoetis/facilities/b4/nodes")
    tags = [item["tag"] for item in res2.json()]
    assert "PUMP-101" in tags

    # Verify JSONL export
    res_jsonl = client.get("/api/clients/zoetis/facilities/b4/export/jsonl")
    assert res_jsonl.status_code == 200
    assert "PUMP-101" in res_jsonl.text

    # Delete
    res_del = client.delete("/api/clients/zoetis/facilities/b4/nodes/test_pump_1")
    assert res_del.status_code == 200

    # Verify deleted
    res3 = client.get("/api/clients/zoetis/facilities/b4/nodes")
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
    res_dup = client.post("/api/clients/zoetis/facilities/b4/nodes", json=duplicate_node)
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
        "voltage": "480Y/277V 3Ø 4W",
        "amps": 1200.0,
        "aic": 65.0,
        "is_panel": True,
        "slots": 42
    }
    res_valid = client.post("/api/clients/zoetis/facilities/b4/nodes", json=update_s4)
    assert res_valid.status_code == 200
    assert res_valid.json()["status"] == "success"


def test_api_facility_dot_and_sld():
    # Test DOT endpoint
    res_dot = client.get("/api/clients/zoetis/facilities/b4/dot")
    assert res_dot.status_code == 200
    assert "subgraph cluster_" in res_dot.text
    assert "MDP-1" in res_dot.text

    # Test HTML SLD Viewer endpoint
    res_sld = client.get("/clients/zoetis/facilities/b4/sld")
    assert res_sld.status_code == 200
    assert "Building Aware" in res_sld.text
    assert "Single-Line Diagram" in res_sld.text
    assert "d3-graphviz" in res_sld.text



