"""Master Catalog of Electrical Equipment Types & Schemas."""

from typing import Any, Dict, Optional

MASTER_CATALOG: Dict[str, Dict[str, Any]] = {
    "UTIL": {
        "category": "Utility Source",
        "name": "Utility Grid Connection",
        "symbol_code": "UTIL",
        "fields": {
            "voltage": {"type": "select", "label": "Grid Voltage", "options": ["12kV", "4.16kV", "480V"], "required": True, "default": "12kV"},
            "duty_ka": {"type": "number", "label": "Short Circuit Duty (kA)", "default": 3.32}
        }
    },
    "SWBD": {
        "category": "Switchgear & Enclosures",
        "name": "Main / Distribution Switchboard",
        "symbol_code": "SWBD",
        "fields": {
            "bus_amps": {"type": "number", "label": "Bus Rating (A)", "default": 1200, "required": True},
            "voltage": {"type": "select", "label": "Nominal Voltage", "options": ["480/277V", "208/120V", "240/120V", "480V"], "required": True},
            "sccr_ka": {"type": "number", "label": "Short Circuit Rating (kA)", "default": 65.0},
            "neutral_rating_pct": {"type": "number", "label": "Neutral Rating (%)", "default": 100}
        }
    },
    "XFMR": {
        "category": "Transformation",
        "name": "Distribution Transformer",
        "symbol_code": "PT",
        "fields": {
            "kva": {"type": "number", "label": "kVA Rating", "default": 750, "required": True},
            "primary_v": {"type": "number", "label": "Primary Voltage (V)", "default": 12000, "required": True},
            "secondary_v": {"type": "number", "label": "Secondary Voltage (V)", "default": 480, "required": True},
            "impedance_pct": {"type": "number", "label": "Impedance (%Z)", "default": 5.75},
            "config": {"type": "select", "label": "Winding", "options": ["Delta-Wye Grounded", "Delta-Delta", "Wye-Wye"], "default": "Delta-Wye Grounded"}
        }
    },
    "ATS": {
        "category": "Switchgear & Enclosures",
        "name": "Automatic Transfer Switch",
        "symbol_code": "ATS",
        "fields": {
            "ampacity": {"type": "number", "label": "Rated Amps (A)", "default": 600, "required": True},
            "voltage": {"type": "select", "label": "Voltage", "options": ["480V", "208V", "240V"]},
            "poles": {"type": "select", "label": "Poles", "options": [3, 4], "default": 3}
        }
    },
    "PNL": {
        "category": "Distribution",
        "name": "Branch Circuit Panelboard",
        "symbol_code": "PNL",
        "fields": {
            "bus_amps": {"type": "number", "label": "Mains Rating (A)", "default": 225, "required": True},
            "voltage": {"type": "select", "label": "Voltage", "options": ["480/277V", "208/120V", "480V"], "required": True},
            "sccr_ka": {"type": "number", "label": "SCCR Rating (kA)", "default": 35.0},
            "mcb_or_mlo": {"type": "select", "label": "Main Type", "options": ["MCB", "MLO"], "default": "MCB"}
        }
    },
    "FEEDER_BREAKER": {
        "category": "Protection & Switching",
        "name": "Feeder Breaker / Disconnect",
        "symbol_code": "CB",
        "fields": {
            "frame_a": {"type": "number", "label": "Frame Rating (AF)", "default": 250},
            "trip_a": {"type": "number", "label": "Trip Setting (AT)", "default": 200, "required": True},
            "cable_size": {"type": "text", "label": "Conductor Size", "default": "4/0 Cu"},
            "conductors_per_phase": {"type": "number", "label": "Qty / Phase", "default": 1},
            "length_ft": {"type": "number", "label": "Run Length (ft)", "default": 50}
        }
    }
}


def get_catalog() -> Dict[str, Dict[str, Any]]:
    """Return the entire master catalog schema dictionary."""
    return MASTER_CATALOG


def get_equipment_schema(type_code: str) -> Optional[Dict[str, Any]]:
    """Retrieve schema definition for a given equipment type code."""
    return MASTER_CATALOG.get(type_code)
