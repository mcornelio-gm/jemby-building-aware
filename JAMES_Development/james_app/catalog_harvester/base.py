"""
Base Harvester Abstraction for Multi-Vendor Equipment Catalog Ingestion.
Provides common export utilities for JSONL, JSON, and Master Catalog SQLite synchronization.
"""

import json
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional

from james_app.catalog_harvester.models import CatalogItem


class BaseVendorHarvester(ABC):
    """
    Abstract base class for all vendor-specific catalog harvesters.
    Subclasses implement vendor-specific parsing, product categorization,
    and specification extraction.
    """

    vendor_name: str = "Generic"
    vendor_key: str = "generic"
    source_url: str = ""

    def __init__(self, cache_dir: Optional[Path] = None):
        self.cache_dir = cache_dir or Path(__file__).resolve().parent.parent.parent / "data" / "catalog_jsonl"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def harvest(self) -> List[CatalogItem]:
        """
        Harvest equipment specifications for the target vendor.
        Returns a list of validated CatalogItem instances.
        """
        pass

    def export_jsonl(self, output_path: Optional[Any] = None) -> Path:
        """
        Export all harvested items to a streaming JSONL file (one JSON object per line).
        """
        items = self.harvest()
        target_path = Path(output_path) if output_path else (self.cache_dir / f"{self.vendor_key}.jsonl")
        target_path.parent.mkdir(parents=True, exist_ok=True)

        with open(target_path, "w", encoding="utf-8") as f:
            for item in items:
                f.write(item.to_jsonl_line() + "\n")

        return target_path

    def export_json(self, output_path: Optional[Any] = None) -> Path:
        """
        Export harvested items to a standard JAMES catalog JSON file ({manufacturer, items: [...]}).
        """
        items = self.harvest()
        target_path = Path(output_path) if output_path else (self.cache_dir.parent / "catalog" / f"{self.vendor_key}.json")
        target_path.parent.mkdir(parents=True, exist_ok=True)

        payload = {
            "manufacturer": self.vendor_name,
            "items": [item.to_dict() for item in items]
        }

        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

        return target_path

    def sync_to_db(self, manager: Optional[Any] = None) -> int:
        """
        Directly upsert all harvested items into the Master Catalog SQLite database.
        """
        from james_app.master_catalog import MasterCatalogManager
        mgr = manager or MasterCatalogManager()
        items = self.harvest()
        count = 0
        with mgr._get_connection() as conn:
            for item in items:
                raw_dict = item.to_dict()
                raw_dict["manufacturer"] = self.vendor_name
                mgr._upsert_item_row(conn, raw_dict)
                count += 1
            conn.commit()
        return count
