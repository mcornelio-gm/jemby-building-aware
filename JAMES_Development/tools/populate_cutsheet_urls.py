#!/usr/bin/env python3
"""Populate resilient manufacturer cut-sheet and search URLs across all items in SQLite Master Catalog."""

import urllib.parse
from james_app.master_catalog import get_master_catalog


def generate_search_url(item: dict) -> str:
    """Generate official manufacturer search URL for the given part number."""
    pn = str(item.get("part_number", "")).strip()
    mfg = str(item.get("manufacturer", "")).strip().lower()
    pn_encoded = urllib.parse.quote(pn)
    
    if "eaton" in mfg or "bussmann" in mfg:
        return f"https://www.eaton.com/us/en-us/skuPage.{pn}.html"
    elif "square d" in mfg or "schneider" in mfg:
        return f"https://www.se.com/us/en/search/?q={pn_encoded}"
    elif "siemens" in mfg:
        return f"https://sieportal.siemens.com/en-us/search?searchTerm={pn_encoded}"
    elif "leviton" in mfg:
        return f"https://www.leviton.com/en/products/{pn.lower()}"
    elif "generac" in mfg:
        return f"https://www.generac.com/search?q={pn_encoded}"
    elif "southwire" in mfg or "encore" in mfg:
        return f"https://www.southwire.com/search?text={pn_encoded}"
    elif "allied" in mfg or "atkore" in mfg:
        return f"https://www.atkore.com/search-results?query={pn_encoded}"
    elif "cooper" in mfg or "metalux" in mfg or "acuity" in mfg:
        return f"https://www.cooperlighting.com/global/search#q={pn_encoded}"
    else:
        # Fallback to direct Google search for manufacturer + part number datasheet
        mfg_name = item.get("manufacturer", "Electrical")
        return f"https://www.google.com/search?q={urllib.parse.quote(f'{mfg_name} {pn} cut sheet pdf spec')}"


def main():
    mgr = get_master_catalog()
    all_items = mgr.get_all_items()
    updated_count = 0
    
    print(f"Scanning {len(all_items)} catalog items for resilient search URLs...")
    
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
        
    print(f"✅ Successfully updated {updated_count}/{len(all_items)} equipment items with active manufacturer search URLs!")


if __name__ == "__main__":
    main()
