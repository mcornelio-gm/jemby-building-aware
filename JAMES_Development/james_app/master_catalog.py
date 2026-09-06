"""Master Catalog Engine & Multi-Manufacturer Registry for JAMES Digital Twin.

Supports fast in-memory indexing, domain/archetype queries, fuzzy searching,
and full CRUD + Clone + Import/Export persistence to data/catalog/{manufacturer}.json.
"""

import csv
import io
import json
import os
import re
from typing import Any, Dict, List, Optional

CATALOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "catalog"))


def sanitize_filename(name: str) -> str:
    """Generate a clean snake_case filename key for a manufacturer."""
    clean = re.sub(r"[^a-zA-Z0-9]+", "_", name.lower()).strip("_")
    return clean or "custom_manufacturer"


class MasterCatalogManager:
    """Manages multi-manufacturer equipment catalogs with fast indexing and JSON persistence."""

    def __init__(self, catalog_dir: str = CATALOG_DIR):
        self.catalog_dir = catalog_dir
        self.manufacturers: Dict[str, Dict[str, Any]] = {}
        self.items_by_pn: Dict[str, Dict[str, Any]] = {}
        self.items_by_domain_type: Dict[str, List[Dict[str, Any]]] = {}
        self.mfg_file_map: Dict[str, str] = {}  # mfg_name -> filename
        self.reload()

    def reload(self) -> None:
        """Scan data/catalog/*.json and rebuild lookup indexes."""
        self.manufacturers.clear()
        self.items_by_pn.clear()
        self.items_by_domain_type.clear()
        self.mfg_file_map.clear()

        if not os.path.exists(self.catalog_dir):
            os.makedirs(self.catalog_dir, exist_ok=True)
            return

        for fname in sorted(os.listdir(self.catalog_dir)):
            if fname.endswith(".json"):
                fpath = os.path.join(self.catalog_dir, fname)
                try:
                    with open(fpath, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    mfg_name = data.get("manufacturer", os.path.splitext(fname)[0].capitalize())
                    items = data.get("items", [])
                    
                    self.mfg_file_map[mfg_name] = fname

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
                            self.items_by_pn[pn.upper().strip()] = item_copy

                        domain = item_copy.get("domain", "generic")
                        type_tag = item_copy.get("type_tag", "")
                        
                        # Index by domain, composite domain:type, and all
                        key_domain = f"domain:{domain}"
                        key_combo = f"{domain}:{type_tag}"
                        
                        self.items_by_domain_type.setdefault(key_domain, []).append(item_copy)
                        self.items_by_domain_type.setdefault(key_combo, []).append(item_copy)
                        self.items_by_domain_type.setdefault("all", []).append(item_copy)

                except Exception as e:
                    print(f"[MasterCatalogManager] Error loading {fname}: {e}")

    def _get_filename_for_mfg(self, mfg_name: str) -> str:
        """Find or create filename for manufacturer."""
        if mfg_name in self.mfg_file_map:
            return self.mfg_file_map[mfg_name]
        
        # Check case-insensitive match
        for existing_name, fname in self.mfg_file_map.items():
            if existing_name.lower() == mfg_name.lower():
                return fname

        fname = f"{sanitize_filename(mfg_name)}.json"
        self.mfg_file_map[mfg_name] = fname
        return fname

    def _sync_mfg_to_disk(self, mfg_name: str) -> None:
        """Write all items for a given manufacturer to data/catalog/{filename}."""
        os.makedirs(self.catalog_dir, exist_ok=True)
        fname = self._get_filename_for_mfg(mfg_name)
        fpath = os.path.join(self.catalog_dir, fname)

        # Collect items for this manufacturer from items_by_pn registry
        mfg_items = []
        for item in self.items_by_pn.values():
            if item.get("manufacturer", "").strip().lower() == mfg_name.strip().lower():
                disk_item = {
                    "part_number": item.get("part_number", ""),
                    "series": item.get("series", ""),
                    "domain": item.get("domain", "power_distribution"),
                    "type_tag": item.get("type_tag", ""),
                    "type_name": item.get("type_name", ""),
                    "description": item.get("description", ""),
                    "specs": item.get("specs", {}),
                    "docs": item.get("docs", {"cut_sheet": "", "upc": item.get("docs", {}).get("upc", None)})
                }
                mfg_items.append(disk_item)

        if not mfg_items and os.path.exists(fpath):
            try:
                os.remove(fpath)
                if mfg_name in self.mfg_file_map:
                    del self.mfg_file_map[mfg_name]
            except Exception:
                pass
        else:
            data = {
                "manufacturer": mfg_name,
                "items": mfg_items
            }
            with open(fpath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

    def get_all_items(self) -> List[Dict[str, Any]]:
        """Return all catalog items."""
        return self.items_by_domain_type.get("all", [])

    def get_manufacturers(self, domain: Optional[str] = None, type_tag: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get distinct manufacturers supporting the given domain and/or type_tag."""
        if not domain and not type_tag:
            return sorted(list(self.manufacturers.values()), key=lambda x: x["name"])

        matching_mfgs = set()
        items = self.filter_items(domain=domain, type_tag=type_tag)
        for item in items:
            matching_mfgs.add(item.get("manufacturer"))

        results = []
        for mfg_name in sorted(matching_mfgs):
            if mfg_name in self.manufacturers:
                results.append(self.manufacturers[mfg_name])
            else:
                results.append({"key": sanitize_filename(mfg_name), "name": mfg_name, "item_count": 0})
        return results

    def filter_items(
        self,
        manufacturer: Optional[str] = None,
        domain: Optional[str] = None,
        type_tag: Optional[str] = None,
        query: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Filter catalog items by manufacturer, domain, type_tag, and keyword query."""
        if domain and type_tag:
            candidates = self.items_by_domain_type.get(f"{domain}:{type_tag}", [])
        elif domain:
            candidates = self.items_by_domain_type.get(f"domain:{domain}", [])
        else:
            candidates = self.items_by_domain_type.get("all", [])

        results = candidates
        if manufacturer:
            mfg_lower = manufacturer.lower()
            results = [item for item in results if mfg_lower in item.get("manufacturer", "").lower()]

        if query:
            q = query.lower().strip()
            results = [
                item for item in results
                if (
                    q in item.get("part_number", "").lower()
                    or q in item.get("description", "").lower()
                    or q in item.get("series", "").lower()
                    or q in item.get("manufacturer", "").lower()
                    or q in str(item.get("docs", {}).get("upc", "")).lower()
                )
            ]

        return results

    def get_item(self, part_number: str) -> Optional[Dict[str, Any]]:
        """Retrieve full item specs by part number."""
        if not part_number:
            return None
        return self.items_by_pn.get(part_number.upper().strip())

    def search(self, query: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Search items by part number, series, manufacturer, or description."""
        if not query:
            return self.get_all_items()[:limit]
        return self.filter_items(query=query)[:limit]

    def add_item(self, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new catalog item, index it, and persist to JSON."""
        pn = str(item_data.get("part_number", "")).strip().upper()
        if not pn:
            raise ValueError("Part number is required.")

        mfg = str(item_data.get("manufacturer", "")).strip() or "Generic"
        domain = str(item_data.get("domain", "power_distribution")).strip()
        type_tag = str(item_data.get("type_tag", "")).strip().upper()

        # Build clean item model
        new_item = {
            "part_number": pn,
            "manufacturer": mfg,
            "series": str(item_data.get("series", "")).strip(),
            "domain": domain,
            "type_tag": type_tag,
            "type_name": str(item_data.get("type_name", "")).strip(),
            "description": str(item_data.get("description", "")).strip(),
            "specs": dict(item_data.get("specs", {})),
            "docs": dict(item_data.get("docs", {"cut_sheet": "", "upc": None}))
        }

        # Update in-memory registry
        self.items_by_pn[pn] = new_item
        self._sync_mfg_to_disk(mfg)
        self.reload()
        return self.get_item(pn) or new_item

    def update_item(self, original_pn: str, item_data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing catalog item and sync to disk."""
        orig_pn_upper = original_pn.strip().upper()
        existing = self.items_by_pn.get(orig_pn_upper)
        if not existing:
            raise KeyError(f"Item with part number '{original_pn}' not found.")

        old_mfg = existing.get("manufacturer", "Generic")
        new_pn = str(item_data.get("part_number", original_pn)).strip().upper()
        new_mfg = str(item_data.get("manufacturer", old_mfg)).strip() or old_mfg

        updated_item = {
            "part_number": new_pn,
            "manufacturer": new_mfg,
            "series": str(item_data.get("series", existing.get("series", ""))).strip(),
            "domain": str(item_data.get("domain", existing.get("domain", "power_distribution"))).strip(),
            "type_tag": str(item_data.get("type_tag", existing.get("type_tag", ""))).strip().upper(),
            "type_name": str(item_data.get("type_name", existing.get("type_name", ""))).strip(),
            "description": str(item_data.get("description", existing.get("description", ""))).strip(),
            "specs": dict(item_data.get("specs", existing.get("specs", {}))),
            "docs": dict(item_data.get("docs", existing.get("docs", {"cut_sheet": "", "upc": None})))
        }

        # Remove old part number if changed
        if orig_pn_upper != new_pn and orig_pn_upper in self.items_by_pn:
            del self.items_by_pn[orig_pn_upper]

        self.items_by_pn[new_pn] = updated_item

        # Persist old mfg file if mfg changed
        if old_mfg.lower() != new_mfg.lower():
            self._sync_mfg_to_disk(old_mfg)

        self._sync_mfg_to_disk(new_mfg)
        self.reload()
        return self.get_item(new_pn) or updated_item

    def delete_item(self, part_number: str) -> bool:
        """Delete an item by part number and update JSON file."""
        pn_upper = part_number.strip().upper()
        existing = self.items_by_pn.get(pn_upper)
        if not existing:
            return False

        mfg = existing.get("manufacturer", "Generic")
        del self.items_by_pn[pn_upper]
        self._sync_mfg_to_disk(mfg)
        self.reload()
        return True

    def clone_item(
        self,
        source_part_number: str,
        new_part_number: str,
        overrides: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Clone an existing catalog item with a new part number and optional overrides."""
        source = self.get_item(source_part_number)
        if not source:
            raise KeyError(f"Source part '{source_part_number}' not found.")

        cloned = json.loads(json.dumps(source))  # Deep copy
        cloned["part_number"] = new_part_number.strip().upper()
        if overrides:
            for k, v in overrides.items():
                if k == "specs" and isinstance(v, dict):
                    cloned.setdefault("specs", {}).update(v)
                elif k == "docs" and isinstance(v, dict):
                    cloned.setdefault("docs", {}).update(v)
                else:
                    cloned[k] = v

        return self.add_item(cloned)

    def import_items(self, items: List[Dict[str, Any]], overwrite: bool = True) -> Dict[str, Any]:
        """Bulk import a list of items from JSON/CSV structures."""
        imported = 0
        skipped = 0
        errors = []

        affected_mfgs = set()

        for idx, raw in enumerate(items):
            pn = str(raw.get("part_number", "")).strip().upper()
            if not pn:
                errors.append(f"Row {idx + 1}: Missing part number.")
                skipped += 1
                continue

            if pn in self.items_by_pn and not overwrite:
                skipped += 1
                continue

            mfg = str(raw.get("manufacturer", "Generic")).strip()
            affected_mfgs.add(mfg)

            item_obj = {
                "part_number": pn,
                "manufacturer": mfg,
                "series": str(raw.get("series", "")).strip(),
                "domain": str(raw.get("domain", "power_distribution")).strip(),
                "type_tag": str(raw.get("type_tag", "")).strip().upper(),
                "type_name": str(raw.get("type_name", "")).strip(),
                "description": str(raw.get("description", "")).strip(),
                "specs": dict(raw.get("specs", {})),
                "docs": dict(raw.get("docs", {"cut_sheet": "", "upc": raw.get("upc", None)}))
            }
            self.items_by_pn[pn] = item_obj
            imported += 1

        for mfg in affected_mfgs:
            self._sync_mfg_to_disk(mfg)

        self.reload()
        return {
            "imported": imported,
            "skipped": skipped,
            "errors": errors,
            "total_catalog_count": len(self.get_all_items())
        }

    def export_items(
        self,
        domain: Optional[str] = None,
        manufacturer: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Export catalog items filtered by domain and manufacturer."""
        return self.filter_items(manufacturer=manufacturer, domain=domain)

    def get_catalog_stats(self) -> Dict[str, Any]:
        """Return summary metrics and distribution across manufacturers and domains."""
        all_items = self.get_all_items()
        mfg_counts = {}
        domain_counts = {}
        type_counts = {}

        for item in all_items:
            mfg = item.get("manufacturer", "Other")
            mfg_counts[mfg] = mfg_counts.get(mfg, 0) + 1

            dom = item.get("domain", "generic")
            domain_counts[dom] = domain_counts.get(dom, 0) + 1

            tt = item.get("type_tag", "UNKNOWN")
            type_counts[tt] = type_counts.get(tt, 0) + 1

        return {
            "total_items": len(all_items),
            "total_manufacturers": len(self.manufacturers),
            "by_manufacturer": mfg_counts,
            "by_domain": domain_counts,
            "by_type": type_counts
        }


# Global singleton instance
catalog_manager = MasterCatalogManager()


def get_master_catalog() -> MasterCatalogManager:
    """Return the global MasterCatalogManager singleton."""
    return catalog_manager
