"""
Vendor Equipment Catalog Harvester CLI.

Collects industrial equipment specifications across vendors in streaming JSONL format,
updates the Master Catalog SQLite database, and maintains bi-directional synchronization.

Usage:
    python -m scripts.harvest_vendor_catalogs --vendor eaton
    python -m scripts.harvest_vendor_catalogs --vendor eaton --sync-db
    python -m scripts.harvest_vendor_catalogs --vendor eaton --format jsonl
"""

import argparse
import sys
from collections import Counter
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from james_app.catalog_harvester import HARVESTERS, get_harvester
from james_app.master_catalog import MasterCatalogManager


def run_harvest(vendor: str, output_fmt: str, sync_db: bool, custom_output: str = "") -> None:
    """Execute harvesting for a given vendor."""
    vendors_to_process = list(HARVESTERS.keys()) if vendor == "all" else [vendor.lower()]

    print(f"\n=======================================================")
    print(f"🏭 JAMES Master Catalog Harvester")
    print(f"Target Vendor(s): {', '.join(vendors_to_process).upper()}")
    print(f"Output Format: {output_fmt.upper()}")
    print(f"Sync to SQLite DB: {sync_db}")
    print(f"=======================================================\n")

    mgr = MasterCatalogManager() if sync_db else None

    for v_key in vendors_to_process:
        if v_key not in HARVESTERS:
            print(f"⚠️  Unknown vendor '{v_key}'. Skipping.")
            continue

        harvester = get_harvester(v_key)
        print(f"▶ Harvesting gear specifications for: {harvester.vendor_name} ({harvester.source_url})...")
        items = harvester.harvest()
        print(f"  ✓ Extracted {len(items)} industrial equipment models across 17 categories.")

        # Breakdown summary
        type_counts = Counter(item.type_tag for item in items)
        print("\n  📊 Equipment Type Distribution:")
        for t_tag, cnt in sorted(type_counts.items(), key=lambda x: -x[1]):
            print(f"    • {t_tag:<12}: {cnt:>3} models")

        # 1. Export JSONL
        if output_fmt in ("jsonl", "both"):
            jsonl_path = Path(custom_output) if custom_output else (ROOT_DIR / "data" / "catalog_jsonl" / f"{v_key}.jsonl")
            exported_path = harvester.export_jsonl(jsonl_path)
            print(f"\n  💾 Exported JSONL to: {exported_path} ({exported_path.stat().st_size:,} bytes)")

        # 2. Export standard JSON
        if output_fmt in ("json", "both") or sync_db:
            json_path = ROOT_DIR / "data" / "catalog" / f"{v_key}.json"
            exported_json = harvester.export_json(json_path)
            print(f"  💾 Exported Master Catalog JSON to: {exported_json} ({exported_json.stat().st_size:,} bytes)")

        # 3. Direct SQLite Database Sync
        if sync_db and mgr:
            print(f"  🔄 Upserting into SQLite database ({mgr.db_path})...")
            synced_count = harvester.sync_to_db(mgr)
            print(f"  ✅ Successfully synced {synced_count} items into SQLite `catalog_items`.")

    print("\n✨ Done!\n")


def main():
    parser = argparse.ArgumentParser(description="Harvest vendor industrial equipment catalogs for JAMES.")
    parser.add_argument("--vendor", default="eaton", help="Vendor name or 'all' (default: eaton)")
    parser.add_argument("--format", choices=["jsonl", "json", "both"], default="jsonl", help="Export format (default: jsonl)")
    parser.add_argument("--sync-db", action="store_true", help="Synchronize harvested items directly into master_catalog.db")
    parser.add_argument("--output", default="", help="Custom output filepath")

    args = parser.parse_args()
    run_harvest(args.vendor, args.format, args.sync_db, args.output)


if __name__ == "__main__":
    main()
