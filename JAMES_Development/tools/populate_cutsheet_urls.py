#!/usr/bin/env python3
"""Populate canonical manufacturer cut-sheet URLs across all items in SQLite Master Catalog."""

from james_app.master_catalog import get_master_catalog


def generate_canonical_url(item: dict) -> str:
    pn = item.get("part_number", "").strip()
    mfg = item.get("manufacturer", "").strip().lower()
    
    if "eaton" in mfg or "bussmann" in mfg:
        return f"https://www.eaton.com/us/en-us/skuPage.{pn}.html"
    elif "square d" in mfg or "schneider" in mfg:
        return f"https://www.se.com/us/en/product/{pn}/"
    elif "siemens" in mfg:
        return f"https://mall.industry.siemens.com/mall/en/us/Catalog/Product/{pn}"
    elif "leviton" in mfg:
        return f"https://www.leviton.com/en/products/{pn.lower()}"
    elif "generac" in mfg:
        return "https://www.generac.com/all-products/generators/home-standby-generators/guardian-series"
    elif "southwire" in mfg:
        return "https://www.southwire.com/wire-cable/building-wire/c/building-wire"
    elif "allied" in mfg or "atkore" in mfg:
        return "https://www.atkore.com/allied-tube-and-conduit"
    elif "cooper" in mfg or "metalux" in mfg or "acuity" in mfg:
        return "https://www.cooperlighting.com/global/brands/metalux"
    return ""


def main():
    mgr = get_master_catalog()
    all_items = mgr.get_all_items()
    updated_count = 0
    
    print(f"Scanning {len(all_items)} catalog items for canonical cut-sheet URLs...")
    
    for item in all_items:
        pn = item.get("part_number")
        url = generate_canonical_url(item)
        if url:
            if not item.get("docs"):
                item["docs"] = {}
            item["docs"]["cut_sheet"] = url
            mgr.update_item(pn, item)
            updated_count += 1
            
    # Trigger full file export to keep JSONs in sync
    for mfg in mgr.get_manufacturers():
        mgr._sync_mfg_to_disk(mfg["name"])
        
    print(f"✅ Successfully populated cut-sheet URLs for {updated_count}/{len(all_items)} equipment items!")


if __name__ == "__main__":
    main()
