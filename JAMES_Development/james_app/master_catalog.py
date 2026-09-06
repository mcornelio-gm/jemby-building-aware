"""Master Catalog Engine & Multi-Manufacturer Registry for JAMES Digital Twin."""

import json
import os
from typing import Any, Dict, List, Optional

CATALOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "catalog"))


class MasterCatalogManager:
    """Manages multi-manufacturer equipment catalogs with fast indexing."""

    def __init__(self, catalog_dir: str = CATALOG_DIR):
        self.catalog_dir = catalog_dir
        self.manufacturers: Dict[str, Dict[str, Any]] = {}
        self.items_by_pn: Dict[str, Dict[str, Any]] = {}
        self.items_by_domain_type: Dict[str, List[Dict[str, Any]]] = {}
        self.reload()

    def reload(self) -> None:
        """Scan data/catalog/*.json and rebuild lookup indexes."""
        self.manufacturers.clear()
        self.items_by_pn.clear()
        self.items_by_domain_type.clear()

        if not os.path.exists(self.catalog_dir):
            return

        for fname in os.listdir(self.catalog_dir):
            if fname.endswith(".json"):
                fpath = os.path.join(self.catalog_dir, fname)
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    mfg_name = data.get("manufacturer", os.path.splitext(fname)[0].capitalize())
                    items = data.get("items", [])
                    
                    self.manufacturers[mfg_name] = {
                        "key": os.path.splitext(fname)[0],
                        "name": mfg_name,
                        "item_count": len(items)
                    }

                    for item in items:
                        item_copy = dict(item)
                        item_copy["manufacturer"] = mfg_name
                        pn = item_copy.get("part_number")
                        if pn:
                            self.items_by_pn[pn.upper()] = item_copy

                        domain = item_copy.get("domain", "generic")
                        type_tag = item_copy.get("type_tag", "")
                        
                        # Index by domain and composite domain:type
                        key_domain = f"domain:{domain}"
                        key_combo = f"{domain}:{type_tag}"
                        
                        self.items_by_domain_type.setdefault(key_domain, []).append(item_copy)
                        self.items_by_domain_type.setdefault(key_combo, []).append(item_copy)
                        self.items_by_domain_type.setdefault("all", []).append(item_copy)

                except Exception as e:
                    print(f"[MasterCatalogManager] Error loading {fname}: {e}")

    def get_all_items(self) -> List[Dict[str, Any]]:
        """Return all catalog items."""
        return self.items_by_domain_type.get("all", [])

    def get_manufacturers(self, domain: Optional[str] = None, type_tag: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get distinct manufacturers supporting the given domain and/or type_tag."""
        if not domain and not type_tag:
            return list(self.manufacturers.values())

        matching_mfgs = set()
        items = self.filter_items(domain=domain, type_tag=type_tag)
        for item in items:
            matching_mfgs.add(item.get("manufacturer"))

        results = []
        for mfg_name in sorted(matching_mfgs):
            if mfg_name in self.manufacturers:
                results.append(self.manufacturers[mfg_name])
            else:
                results.append({"key": mfg_name.lower().replace(" ", "_"), "name": mfg_name, "item_count": 0})
        return results

    def filter_items(
        self,
        manufacturer: Optional[str] = None,
        domain: Optional[str] = None,
        type_tag: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Filter catalog items by manufacturer, domain, and type_tag."""
        if domain and type_tag:
            candidates = self.items_by_domain_type.get(f"{domain}:{type_tag}", [])
        elif domain:
            candidates = self.items_by_domain_type.get(f"domain:{domain}", [])
        else:
            candidates = self.items_by_domain_type.get("all", [])

        if not manufacturer:
            return candidates

        mfg_lower = manufacturer.lower()
        return [
            item for item in candidates
            if mfg_lower in item.get("manufacturer", "").lower()
        ]

    def get_item(self, part_number: str) -> Optional[Dict[str, Any]]:
        """Retrieve full item specs by part number."""
        return self.items_by_pn.get(part_number.upper().strip())

    def search(self, query: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Search items by part number, series, or description."""
        if not query:
            return self.get_all_items()[:limit]

        q = query.lower().strip()
        matches = []
        for item in self.get_all_items():
            if (
                q in item.get("part_number", "").lower() or
                q in item.get("description", "").lower() or
                q in item.get("series", "").lower() or
                q in item.get("manufacturer", "").lower()
            ):
                matches.append(item)
                if len(matches) >= limit:
                    break
        return matches


# Global singleton instance
catalog_manager = MasterCatalogManager()


def get_master_catalog() -> MasterCatalogManager:
    """Return the global MasterCatalogManager singleton."""
    return catalog_manager
