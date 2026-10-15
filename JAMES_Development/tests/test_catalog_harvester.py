"""
Unit Tests for the Multi-Vendor Industrial Equipment Catalog Harvester Engine.
Verifies Eaton, Square D, ABB, and Siemens catalog harvesting across all 17 industrial equipment categories,
streaming JSONL serialization, and Master Catalog SQLite synchronization.
"""

import json
from pathlib import Path
import pytest

from james_app.catalog_harvester import (
    CatalogItem,
    BaseVendorHarvester,
    EatonCatalogHarvester,
    SquareDCatalogHarvester,
    ABBCatalogHarvester,
    SiemensCatalogHarvester,
    get_harvester,
    HARVESTERS
)
from james_app.master_catalog import MasterCatalogManager


ALL_17_CATEGORIES = [
    "BUSWAY",
    "CB",
    "LOAD_CENTER",
    "MCC",
    "PANEL",
    "SOFTSTART",
    "SWBD",
    "DISC",
    "SWGR",
    "XFMR",
    "ATS",
    "PSG",
    "POWER_COND",
    "PDS",
    "STS",
    "SPD",
    "UPS"
]

ALL_VENDORS = ["eaton", "square_d", "abb", "siemens"]


def test_harvester_registry():
    """Verify all 4 vendor harvesters are properly registered and discoverable."""
    for v in ALL_VENDORS:
        assert v in HARVESTERS
        harvester = get_harvester(v)
        assert isinstance(harvester, BaseVendorHarvester)

    with pytest.raises(ValueError, match="Unknown vendor harvester"):
        get_harvester("non_existent_vendor")


@pytest.mark.parametrize("vendor_key", ALL_VENDORS)
def test_vendor_harvest_all_17_industrial_categories(vendor_key: str):
    """Verify each vendor harvest extracts models for every one of the 17 industrial categories."""
    harvester = get_harvester(vendor_key)
    items = harvester.harvest()
    assert len(items) >= 150, f"Vendor {vendor_key} harvested {len(items)} items, expected >= 150"

    type_tags = {item.type_tag for item in items}
    for expected_tag in ALL_17_CATEGORIES:
        assert expected_tag in type_tags, f"Vendor {vendor_key} missing expected industrial category: {expected_tag}"


@pytest.mark.parametrize("vendor_key", ALL_VENDORS)
def test_vendor_jsonl_export(tmp_path: Path, vendor_key: str):
    """Verify streaming JSONL export creates valid line-delimited JSON with required fields."""
    harvester = get_harvester(vendor_key)
    harvester.cache_dir = tmp_path
    jsonl_file = tmp_path / f"test_{vendor_key}.jsonl"
    exported_path = harvester.export_jsonl(jsonl_file)

    assert exported_path.exists()
    assert exported_path.stat().st_size > 50000

    line_count = 0
    with open(exported_path, "r", encoding="utf-8") as f:
        for line in f:
            line_str = line.strip()
            if not line_str:
                continue
            data = json.loads(line_str)
            line_count += 1

            assert data["manufacturer"] == harvester.vendor_name
            assert data["part_number"]
            assert data["domain"]
            assert data["type_tag"] in ALL_17_CATEGORIES
            assert "specs" in data
            assert isinstance(data["specs"], dict)
            assert "docs" in data

    assert line_count >= 150


def test_vendor_json_export(tmp_path: Path):
    """Verify standard catalog JSON export matches JAMES multi-item format."""
    harvester = get_harvester("square_d")
    harvester.cache_dir = tmp_path
    json_file = tmp_path / "test_square_d.json"
    exported_path = harvester.export_json(json_file)

    assert exported_path.exists()
    with open(exported_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data["manufacturer"] == "Square D"
    assert isinstance(data["items"], list)
    assert len(data["items"]) >= 150


def test_harvester_sqlite_sync_all_vendors(tmp_path: Path):
    """Verify all harvested vendor items can be upserted into an isolated SQLite database."""
    test_db = tmp_path / "test_catalog.db"
    test_cat_dir = tmp_path / "catalog"
    mgr = MasterCatalogManager(db_path=str(test_db), catalog_dir=str(test_cat_dir))

    total_synced = 0
    for v_key in ALL_VENDORS:
        harvester = get_harvester(v_key)
        synced = harvester.sync_to_db(mgr)
        assert synced >= 150
        total_synced += synced

    with mgr._get_connection() as conn:
        count = conn.execute("SELECT COUNT(*) as count FROM catalog_items").fetchone()["count"]
        assert count == total_synced
        assert count >= 600

        # Test specific queries across multiple vendors
        for expected_mfr in ["Eaton", "Square D", "ABB", "Siemens"]:
            mfr_count = conn.execute("SELECT COUNT(*) as count FROM catalog_items WHERE manufacturer = ?", (expected_mfr,)).fetchone()["count"]
            assert mfr_count >= 150

        # Test specific query on newly synced industrial gear
        busway_rows = conn.execute("SELECT DISTINCT manufacturer FROM catalog_items WHERE type_tag = 'BUSWAY'").fetchall()
        busway_mfrs = {r["manufacturer"] for r in busway_rows}
        assert busway_mfrs == {"Eaton", "Square D", "ABB", "Siemens"}
