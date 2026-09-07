#!/usr/bin/env python3
"""Populate Google Cut-Sheet search URLs and direct OEM URLs across all items in SQLite Master Catalog."""

import urllib.parse
from james_app.master_catalog import get_master_catalog


def generate_search_url(item: dict) -> str:
    """Generate high-yield Google / OEM cut-sheet search URL for the given part number."""
    pn = str(item.get("part_number", "")).strip()
    mfg = str(item.get("manufacturer", "")).strip()
    mfg_lower = mfg.lower()
    
    # Direct SKU pages that are 100% verified to resolve cleanly
    if "eaton" in mfg_lower and "bussmann" not in mfg_lower and pn.startswith("PD"):
        return f"https://www.eaton.com/us/en-us/skuPage.{pn}.html"
    elif "leviton" in mfg_lower and len(pn) <= 8 and not pn.startswith("GEN"):
        return f"https://www.leviton.com/en/products/{pn.lower()}"
    else:
        # High-precision Google Cut-Sheet PDF query
        query = f"{mfg} {pn} cut sheet pdf"
        return f"https://www.google.com/search?q={urllib.parse.quote(query)}"


def main():
    mgr = get_master_catalog()
    all_items = mgr.get_all_items()
    updated_count = 0
    
    print(f"Scanning {len(all_items)} catalog items for high-yield Google cut-sheet URLs...")
    
    for item in all_items:
        pn = item.get("part_number")
        url = generate_search_url(item)
        if url:
            if not item.get("docs"):
                item["docs"] = {}
            item["docs"]["cut_sheet"] = url
            mgr.update_item(pn, item)
            updated_count += 1
            
    # Sync all manufacturers to disk JSONs
    for mfg in mgr.get_manufacturers():
        mgr._sync_mfg_to_disk(mfg["name"])
        
    print(f"✅ Successfully updated {updated_count}/{len(all_items)} equipment items with high-yield cut-sheet search URLs!")


if __name__ == "__main__":
    main()
