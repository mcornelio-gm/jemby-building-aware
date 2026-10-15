"""
Catalog JSONL Ingestion CLI for JAMES Master Catalog.

Ingests streaming line-delimited JSONL equipment catalog files directly into
the Master Catalog SQLite database with full validation and ACID transactions.

Usage:
    python -m scripts.import_catalog_jsonl --file data/catalog_jsonl/eaton.jsonl
    python -m scripts.import_catalog_jsonl --all
    python -m scripts.import_catalog_jsonl --all --no-overwrite
"""

import argparse
import sys
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from james_app.master_catalog import MasterCatalogManager


def import_jsonl_file(mgr: MasterCatalogManager, file_path: Path, overwrite: bool = True) -> dict:
    """Import a single JSONL file into SQLite."""
    print(f"▶ Ingesting JSONL: {file_path.name}...")
    res = mgr.import_from_jsonl(file_path, overwrite=overwrite)
    print(f"  ✓ Imported: {res['imported']} items | Skipped: {res['skipped']} | Errors: {len(res['errors'])}")
    if res["errors"]:
        for err in res["errors"][:5]:
            print(f"    ⚠️  {err}")
    return res


def main():
    parser = argparse.ArgumentParser(description="Ingest JSONL catalog files into JAMES Master Catalog.")
    parser.add_argument("--file", help="Path to a specific .jsonl file to ingest")
    parser.add_argument("--all", action="store_true", help="Ingest all .jsonl files in data/catalog_jsonl/")
    parser.add_argument("--no-overwrite", action="store_true", help="Do not overwrite existing part numbers")

    args = parser.parse_args()
    mgr = MasterCatalogManager()
    overwrite = not args.no_overwrite
    jsonl_dir = ROOT_DIR / "data" / "catalog_jsonl"

    print("\n=======================================================")
    print("📦 JAMES Master Catalog JSONL Importer")
    print(f"Target Database: {mgr.db_path}")
    print(f"Overwrite Mode: {overwrite}")
    print("=======================================================\n")

    files_to_import = []
    if args.file:
        files_to_import.append(Path(args.file))
    elif args.all:
        files_to_import = sorted(list(jsonl_dir.glob("*.jsonl")))
    else:
        # Default to all if neither specified
        files_to_import = sorted(list(jsonl_dir.glob("*.jsonl")))

    if not files_to_import:
        print(f"⚠️  No .jsonl files found in {jsonl_dir}")
        sys.exit(1)

    total_imported = 0
    total_skipped = 0
    for f in files_to_import:
        if not f.exists():
            print(f"⚠️  File not found: {f}")
            continue
        res = import_jsonl_file(mgr, f, overwrite=overwrite)
        total_imported += res["imported"]
        total_skipped += res["skipped"]

    print("\n-------------------------------------------------------")
    print(f"✨ Import Complete!")
    print(f"Total Processed Across Files: {total_imported} imported, {total_skipped} skipped.")
    stats = mgr.get_catalog_stats()
    print(f"Total Master Catalog Count: {stats['total_items']} items across {stats['total_manufacturers']} manufacturers.")
    print("-------------------------------------------------------\n")


if __name__ == "__main__":
    main()
