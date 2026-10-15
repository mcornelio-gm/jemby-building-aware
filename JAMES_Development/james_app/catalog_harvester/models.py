"""
Data Models for Vendor Equipment Catalog Harvesting in JAMES.
Defines normalized schemas conforming to the Master Catalog SQLite registry.
"""

import json
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class CatalogItem(BaseModel):
    """
    Standard equipment record representation for the JAMES Master Catalog.
    Compatible with SQLite catalog_items table and streaming JSONL exports.
    """
    part_number: str
    manufacturer: str
    series: str = ""
    domain: str
    type_tag: str
    type_name: str = ""
    description: str = ""
    voltage: str = ""
    amps: Optional[float] = None
    aic: Optional[float] = None
    kva: Optional[float] = None
    poles: str = ""
    phase: str = ""
    total_slots: Optional[int] = None
    nema_rating: str = ""
    impedance_z: Optional[float] = None
    upc: str = ""
    cut_sheet_url: str = ""
    specs: Dict[str, Any] = Field(default_factory=dict)
    docs: Dict[str, Any] = Field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert item to a dictionary matching JAMES catalog schema."""
        data = self.model_dump()
        # Ensure specs dictionary contains primary ratings if not explicitly set
        if self.voltage and "voltage" not in data["specs"]:
            data["specs"]["voltage"] = self.voltage
        if self.amps is not None and "amps" not in data["specs"]:
            data["specs"]["amps"] = self.amps
        if self.aic is not None and "aic" not in data["specs"]:
            data["specs"]["aic"] = self.aic
        if self.kva is not None and "kva" not in data["specs"]:
            data["specs"]["kva"] = self.kva
        if self.poles and "poles" not in data["specs"]:
            data["specs"]["poles"] = self.poles
        if self.phase and "phase" not in data["specs"]:
            data["specs"]["phase"] = self.phase
        if self.total_slots is not None and "total_slots" not in data["specs"]:
            data["specs"]["total_slots"] = self.total_slots
        if self.nema_rating and "nema_rating" not in data["specs"]:
            data["specs"]["nema_rating"] = self.nema_rating
        if self.impedance_z is not None and "impedance_z" not in data["specs"]:
            data["specs"]["impedance_z"] = self.impedance_z

        # Ensure docs dictionary contains standard URLs
        if self.cut_sheet_url and "cut_sheet" not in data["docs"]:
            data["docs"]["cut_sheet"] = self.cut_sheet_url
        if self.upc and "upc" not in data["docs"]:
            data["docs"]["upc"] = self.upc

        return data

    def to_jsonl_line(self) -> str:
        """Serialize item to a single compact JSON string line."""
        return json.dumps(self.to_dict(), ensure_ascii=False)
