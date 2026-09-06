"""Unit tests for the Modular Master Catalog Engine and API."""

from james_app.master_catalog import get_master_catalog
from fastapi.testclient import TestClient
from james_app.main import app

client = TestClient(app)


def test_master_catalog_loaded():
    mgr = get_master_catalog()
    assert len(mgr.manufacturers) >= 8
    assert "Eaton" in mgr.manufacturers
    assert "Square D / Schneider Electric" in mgr.manufacturers
    assert "Siemens" in mgr.manufacturers
    
    all_items = mgr.get_all_items()
    assert len(all_items) >= 250


def test_master_catalog_domain_and_type_filtering():
    mgr = get_master_catalog()
    
    # Check transformers
    xfmr_items = mgr.filter_items(domain="transformers", type_tag="XFMR")
    assert len(xfmr_items) >= 11
    
    # Check manufacturers for transformers
    xfmr_mfgs = mgr.get_manufacturers(domain="transformers", type_tag="XFMR")
    mfg_names = [m["name"] for m in xfmr_mfgs]
    assert "Square D / Schneider Electric" in mfg_names
    assert "Eaton" in mfg_names
    assert "Siemens" in mfg_names
    
    # Check breaker filtering
    eaton_breakers = mgr.filter_items(manufacturer="Eaton", domain="breakers", type_tag="CB")
    assert len(eaton_breakers) >= 100
    
    # Check single item lookup
    item = mgr.get_item("PDF34GH400E2XN")
    assert item is not None
    assert item["specs"]["amps"] == 400.0
    assert item["specs"]["poles"] == 4


def test_master_catalog_api_endpoints():
    # 1. GET /api/catalog/manufacturers
    res_mfgs = client.get("/api/catalog/manufacturers?domain=transformers&type_tag=XFMR")
    assert res_mfgs.status_code == 200
    mfgs = res_mfgs.json()
    assert len(mfgs) >= 3
    
    # 2. GET /api/catalog/items
    res_items = client.get("/api/catalog/items?manufacturer=Square%20D%20%2F%20Schneider%20Electric&domain=transformers&type_tag=XFMR")
    assert res_items.status_code == 200
    items = res_items.json()
    assert len(items) == 5
    assert any(it["part_number"] == "EE75T3H" for it in items)
    
    # 3. GET /api/catalog/items/{part_number}
    res_single = client.get("/api/catalog/items/EE75T3H")
    assert res_single.status_code == 200
    single = res_single.json()
    assert single["part_number"] == "EE75T3H"
    assert single["specs"]["kva"] == 75.0
    assert single["specs"]["voltage"] == "480V : 208Y/120V"
