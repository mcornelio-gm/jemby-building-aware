"""Unit tests for Workspace Finder API and client/facility database management."""

import pytest
import shutil
from fastapi.testclient import TestClient
from pathlib import Path

from james_app.main import app
from james_app import db

client = TestClient(app)


@pytest.fixture(autouse=True)
def cleanup_test_clients():
    """Clean up test client directories after each test."""
    yield
    test_dirs = ["merck_pharma", "pfizer_biotech", "test_client"]
    for d in test_dirs:
        p = Path("data/clients") / d
        if p.exists():
            shutil.rmtree(p, ignore_errors=True)


def test_list_all_client_facilities_db_helper():
    """Verify list_all_client_facilities discovers existing clients and counts SQLite equipment nodes."""
    clients = db.list_all_client_facilities()
    assert isinstance(clients, list)
    assert len(clients) > 0

    # Zoetis should exist
    zoetis = next((c for c in clients if c["client_id"] == "zoetis"), None)
    assert zoetis is not None
    assert zoetis["client_name"] == "Zoetis"
    assert zoetis["facility_count"] >= 1

    b4 = next((f for f in zoetis["facilities"] if f["facility_id"] == "b4"), None)
    assert b4 is not None
    assert b4["asset_count"] >= 9
    assert "model.db" in b4["db_path"]
    assert "KB" in b4["file_size_str"] or "B" in b4["file_size_str"]


def test_create_client_facility_db_helper(tmp_path):
    """Verify creating a new client and facility database with optional starter seeding."""
    test_client = "pfizer_biotech"
    test_facility = "lab_building_9"

    info = db.create_client_facility(test_client, test_facility, seed=True)
    assert info["client_id"] == "pfizer_biotech"
    assert info["facility_id"] == "lab_building_9"
    assert info["asset_count"] >= 4

    db_path = Path(info["db_path"])
    assert db_path.exists()
    assert db_path.name == "model.db"

    # Verify nodes in the new database
    with db.get_session(test_client, test_facility) as session:
        nodes = session.query(db.NodeRecord).all()
        assert len(nodes) >= 4
        tags = [n.tag for n in nodes]
        assert "MDP-1" in tags
        assert "ATS-1" in tags


def test_api_get_workspace_facilities():
    """Verify GET /api/workspace/facilities returns structured client/facility hierarchy."""
    res = client.get("/api/workspace/facilities")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) > 0

    for client_entry in data:
        assert "client_id" in client_entry
        assert "client_name" in client_entry
        assert "facilities" in client_entry
        assert isinstance(client_entry["facilities"], list)
        for fac in client_entry["facilities"]:
            assert "facility_id" in fac
            assert "db_path" in fac
            assert "asset_count" in fac
            assert "file_size_str" in fac
            assert "modified_at" in fac


def test_api_post_workspace_facilities_success():
    """Verify POST /api/workspace/facilities creates a new client and facility."""
    payload = {
        "client_id": "merck_pharma",
        "facility_id": "vial_packaging_line",
        "seed": True
    }
    res = client.post("/api/workspace/facilities", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["client_id"] == "merck_pharma"
    assert data["facility_id"] == "vial_packaging_line"
    assert data["asset_count"] >= 4
    assert "model.db" in data["db_path"]


def test_api_post_workspace_facilities_validation():
    """Verify POST /api/workspace/facilities enforces validation on empty parameters."""
    res = client.post("/api/workspace/facilities", json={"client_id": "", "facility_id": "b1"})
    assert res.status_code == 400

    res = client.post("/api/workspace/facilities", json={"client_id": "client_a", "facility_id": ""})
    assert res.status_code == 400


def test_survey_and_catalog_client_param_routing():
    """Verify ?client=...&facility=... query params are correctly parsed by survey and catalog routes."""
    res = client.get("/survey?client=pfizer_biotech&facility=lab_building_9")
    assert res.status_code == 200
    assert "PFIZER_BIOTECH" in res.text
    assert "LAB_BUILDING_9" in res.text

    res_cat = client.get("/catalog?client=pfizer_biotech&facility=lab_building_9")
    assert res_cat.status_code == 200
    assert "PFIZER_BIOTECH" in res_cat.text
    assert "LAB_BUILDING_9" in res_cat.text


def test_api_create_unseeded_workspace_facility():
    """Verify creating a facility without seeding produces an empty (0 assets) database."""
    res = client.post("/api/workspace/facilities", json={"client_id": "test_client", "facility_id": "empty_building"})
    assert res.status_code == 200
    data = res.json()
    assert data["asset_count"] == 0

    # Verify nodes API returns empty list
    res_nodes = client.get("/api/clients/test_client/facilities/empty_building/nodes")
    assert res_nodes.status_code == 200
    assert res_nodes.json() == []


def test_api_delete_workspace_facility():
    """Verify DELETE /api/workspace/facilities/{client_id}/{facility_id} removes the database and directory."""
    # Create a facility first
    create_res = client.post("/api/workspace/facilities", json={"client_id": "test_client", "facility_id": "to_delete"})
    assert create_res.status_code == 200

    # Verify it exists
    del_res = client.delete("/api/workspace/facilities/test_client/to_delete")
    assert del_res.status_code == 200
    assert del_res.json()["status"] == "success"

    # Verify protected default demo cannot be deleted
    demo_del = client.delete("/api/workspace/facilities/zoetis/b4")
    assert demo_del.status_code == 400


