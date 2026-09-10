import pytest
from fastapi.testclient import TestClient
from james_app.main import app
from james_app.checklists import (
    load_master_checklists,
    get_all_checklists,
    get_checklist_by_id,
    get_checklists_for_domain
)

client = TestClient(app)

def test_load_master_checklists():
    checklists = load_master_checklists()
    assert len(checklists) >= 7
    ids = [c["id"] for c in checklists]
    assert "CHK-SAFETY-70E" in ids
    assert "CHK-GEN-110" in ids
    assert "CHK-PANEL-408" in ids

def test_get_checklists_for_panels():
    panel_chks = get_checklists_for_domain("panels")
    ids = [c["id"] for c in panel_chks]
    assert "CHK-PANEL-408" in ids
    assert "CHK-SAFETY-70E" in ids
    assert "CHK-GEN-110" in ids
    assert "CHK-BKR-240" in ids

def test_get_checklists_for_transformers():
    xfmr_chks = get_checklists_for_domain("transformers")
    ids = [c["id"] for c in xfmr_chks]
    assert "CHK-XFRM-450" in ids
    assert "CHK-GND-250" in ids
    assert "CHK-SAFETY-70E" in ids

def test_api_checklists_endpoints():
    # 1. Get all checklists
    res = client.get("/api/checklists")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, list)
    assert len(data) >= 7

    # 2. Get single checklist
    res = client.get("/api/checklists/CHK-PANEL-408")
    assert res.status_code == 200
    item = res.json()
    assert item["id"] == "CHK-PANEL-408"
    assert len(item["items"]) > 0

    # 3. Get domain checklists
    res = client.get("/api/checklists/domain/panels?type_tag=MDP")
    assert res.status_code == 200
    domain_items = res.json()
    c_ids = [c["id"] for c in domain_items]
    assert "CHK-PANEL-408" in c_ids

    # 4. Reload endpoint
    res = client.post("/api/checklists/reload")
    assert res.status_code == 200
    reload_data = res.json()
    assert reload_data["status"] == "success"
    assert reload_data["reloaded_count"] >= 7
