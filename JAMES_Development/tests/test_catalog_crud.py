"""Automated tests for Master Catalog CRUD, Clone, Import/Export, and JSON file synchronization."""

import pytest
from fastapi.testclient import TestClient

from james_app.main import app
from james_app.master_catalog import get_master_catalog

client = TestClient(app)


def test_catalog_studio_page_renders():
    """Verify GET /catalog returns the full Master Catalog Studio UI."""
    response = client.get("/catalog")
    assert response.status_code == 200
    assert "Master Catalog Studio" in response.text
    assert "Add Part" in response.text
    assert "Import" in response.text


def test_catalog_stats_endpoint():
    """Verify GET /api/catalog/stats returns valid breakdown metrics."""
    response = client.get("/api/catalog/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_items" in data
    assert data["total_items"] >= 280
    assert "total_manufacturers" in data
    assert data["total_manufacturers"] >= 9
    assert "by_manufacturer" in data
    assert "Eaton" in data["by_manufacturer"]


def test_catalog_crud_lifecycle():
    """Test Create -> Read -> Update -> Delete lifecycle for a new catalog item."""
    mgr = get_master_catalog()
    test_pn = "TEST-MCCB-999X"

    # 1. Ensure clean initial state
    mgr.delete_item(test_pn)

    # 2. CREATE (POST /api/catalog/items)
    create_payload = {
        "part_number": test_pn,
        "manufacturer": "Test Dynamics",
        "series": "TD-X Series",
        "domain": "power_distribution",
        "type_tag": "MCCB",
        "type_name": "Test Circuit Breaker",
        "description": "250A 480V 3P Test Breaker",
        "specs": {
            "voltage": "480V",
            "amps": 250.0,
            "aic": 65.0,
            "poles": "3P"
        },
        "docs": {
            "cut_sheet": "https://example.com/td-x.pdf",
            "upc": "999888777666"
        }
    }
    create_res = client.post("/api/catalog/items", json=create_payload)
    assert create_res.status_code == 200
    assert create_res.json()["status"] == "success"

    # 3. READ (GET /api/catalog/items/{pn})
    get_res = client.get(f"/api/catalog/items/{test_pn}")
    assert get_res.status_code == 200
    item = get_res.json()
    assert item["part_number"] == test_pn
    assert item["manufacturer"] == "Test Dynamics"
    assert item["specs"]["amps"] == 250.0
    assert item["docs"]["upc"] == "999888777666"

    # 4. UPDATE (PUT /api/catalog/items/{pn})
    update_payload = dict(create_payload)
    update_payload["specs"]["amps"] = 300.0
    update_payload["description"] = "Updated 300A 480V 3P Test Breaker"
    put_res = client.put(f"/api/catalog/items/{test_pn}", json=update_payload)
    assert put_res.status_code == 200
    updated_item = put_res.json()["item"]
    assert updated_item["specs"]["amps"] == 300.0
    assert "Updated" in updated_item["description"]

    # 5. CLONE (POST /api/catalog/clone/{pn})
    clone_pn = "TEST-MCCB-999X-CLONE"
    mgr.delete_item(clone_pn)
    clone_res = client.post(f"/api/catalog/clone/{test_pn}", json={
        "new_part_number": clone_pn,
        "overrides": {"specs": {"amps": 400.0}}
    })
    assert clone_res.status_code == 200
    cloned_item = clone_res.json()["item"]
    assert cloned_item["part_number"] == clone_pn
    assert cloned_item["specs"]["amps"] == 400.0

    # 6. DELETE (DELETE /api/catalog/items/{pn})
    del_res1 = client.delete(f"/api/catalog/items/{test_pn}")
    assert del_res1.status_code == 200
    del_res2 = client.delete(f"/api/catalog/clone/{clone_pn}")  # via delete_item
    client.delete(f"/api/catalog/items/{clone_pn}")

    # Verify both deleted
    check_res = client.get(f"/api/catalog/items/{test_pn}")
    assert check_res.status_code == 404


def test_catalog_import_and_export():
    """Verify bulk import and export endpoints."""
    mgr = get_master_catalog()
    import_pn = "BULK-TEST-001"
    mgr.delete_item(import_pn)

    # Test Bulk Import
    import_payload = {
        "items": [
            {
                "part_number": import_pn,
                "manufacturer": "BulkMfg",
                "domain": "transformers",
                "type_tag": "XFMR",
                "type_name": "Dry-Type Transformer",
                "description": "Bulk Imported 75kVA Transformer",
                "specs": {"kva": 75.0, "voltage": "480:208Y/120V"},
                "upc": "111222333444"
            }
        ],
        "overwrite": True
    }
    import_res = client.post("/api/catalog/import", json=import_payload)
    assert import_res.status_code == 200
    assert import_res.json()["result"]["imported"] >= 1

    # Verify item exists
    get_res = client.get(f"/api/catalog/items/{import_pn}")
    assert get_res.status_code == 200
    assert get_res.json()["manufacturer"] == "BulkMfg"

    # Test CSV Export
    export_csv = client.get("/api/catalog/export?format=csv")
    assert export_csv.status_code == 200
    assert "text/csv" in export_csv.headers["content-type"]
    assert "Part Number,Manufacturer" in export_csv.text
    assert import_pn in export_csv.text

    # Test JSON Export
    export_json = client.get("/api/catalog/export?format=json")
    assert export_json.status_code == 200
    json_data = export_json.json()
    assert "items" in json_data
    assert len(json_data["items"]) >= 280

    # Clean up test item
    client.delete(f"/api/catalog/items/{import_pn}")
