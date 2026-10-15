"""
Catalog Harvester Module for JAMES Building-Aware Master Catalog.
Provides multi-vendor scrapers and structured harvesters for industrial electrical equipment:
- Eaton (PowerEdge CA08100002E - CA08100016E)
- Square D / Schneider Electric (Digest 179)
- ABB Electrification (BuyLog Sections 1 - 24)
- Siemens (Speedfax Sections 1 - 19)
"""

from typing import Dict, Type
from james_app.catalog_harvester.models import CatalogItem
from james_app.catalog_harvester.base import BaseVendorHarvester
from james_app.catalog_harvester.eaton import EatonCatalogHarvester
from james_app.catalog_harvester.square_d import SquareDCatalogHarvester
from james_app.catalog_harvester.abb import ABBCatalogHarvester
from james_app.catalog_harvester.siemens import SiemensCatalogHarvester

HARVESTERS: Dict[str, Type[BaseVendorHarvester]] = {
    "eaton": EatonCatalogHarvester,
    "square_d": SquareDCatalogHarvester,
    "abb": ABBCatalogHarvester,
    "siemens": SiemensCatalogHarvester,
}


def get_harvester(vendor_name: str) -> BaseVendorHarvester:
    """Retrieve an initialized harvester instance for a vendor key."""
    key = vendor_name.lower().strip()
    if key not in HARVESTERS:
        raise ValueError(f"Unknown vendor harvester '{vendor_name}'. Available: {list(HARVESTERS.keys())}")
    return HARVESTERS[key]()


__all__ = [
    "CatalogItem",
    "BaseVendorHarvester",
    "EatonCatalogHarvester",
    "SquareDCatalogHarvester",
    "ABBCatalogHarvester",
    "SiemensCatalogHarvester",
    "HARVESTERS",
    "get_harvester",
]
