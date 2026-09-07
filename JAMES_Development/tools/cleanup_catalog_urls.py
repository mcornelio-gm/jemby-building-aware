#!/usr/bin/env python3
"""Clean up all auto-generated google search URLs from the Master Catalog database and JSON files.

Only explicit direct manufacturer URLs (e.g. Eaton SKU pages, Leviton product pages)
or user-specified URLs will remain. Items without direct URLs will rely on on-the-fly
dynamic search in the UI.
"""

from james_app.master_catalog import get_master_catalog


def main():
    mgr = get_master_catalog()
    all_items = mgr.get_all_items()
    cleared_count = 0
    kept_count = 0
    
    print(f"Scanning {len(all_items)} catalog items to remove default Google search URLs...")
    
    for item in all_items:
        pn = item.get("part_number")
        docs = item.get("docs") or {}
        cut_sheet = docs.get("cut_sheet", "") or ""
        
        if cut_sheet.startswith("https://www.google.com/search") or cut_sheet.startswith("http://www.google.com/search"):
            docs["cut_sheet"] = None
            item["docs"] = docs
            mgr.update_item(pn, item)
            cleared_count += 1
        elif cut_sheet:
            kept_count += 1
            
    # Sync all manufacturers to disk JSONs
    for mfg in mgr.get_manufacturers():
        mgr._sync_mfg_to_disk(mfg["name"])
        
    print(f"✅ Finished! Cleared {cleared_count} Google search URLs. Kept {kept_count} direct OEM URLs.")


if __name__ == "__main__":
    main()
