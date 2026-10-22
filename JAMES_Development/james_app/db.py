"""Database Layer: Client-Isolated SQLite + JSONL Multi-Tenant Architecture with SQLAlchemy ORM."""

import os
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional
from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    JSON,
    String,
    Text,
    create_engine,
)
from sqlalchemy.orm import declarative_base, sessionmaker, Session

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = Path(os.getenv("JAMES_DATA_DIR", str(BASE_DIR / "data")))
CLIENTS_DATA_DIR = DATA_DIR / "clients"

DEFAULT_CLIENT = "zoetis"
DEFAULT_FACILITY = "b4"

Base = declarative_base()


class NodeRecord(Base):
    """SQLAlchemy model for equipment node in SQLite."""
    __tablename__ = "equipment_nodes"

    id = Column(String(64), primary_key=True)
    tag = Column(String(64), index=True, nullable=False)
    name = Column(String(128), nullable=False)
    object_class = Column(String(64), nullable=False)  # e.g. "AutomaticTransferSwitchObject"
    domain = Column(String(32), index=True, nullable=False)
    type_tag = Column(String(32), nullable=False)
    type_name = Column(String(128), nullable=False)
    room = Column(String(128), index=True, default="Main Electrical Room 101")
    fed_from = Column(String(64), nullable=True)  # Tag of upstream source
    voltage = Column(String(32), default="480Y/277V 3Ø 4W")
    amps = Column(Float, default=225.0)
    aic = Column(Float, default=65.0)
    is_panel = Column(Integer, default=0)
    slots = Column(Integer, default=42)
    survey_sequence = Column(Integer, default=0)
    status = Column(String(32), default="STAGED")
    attributes = Column(JSON, nullable=False)  # Pydantic JSON payload
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class EdgeRecord(Base):
    """SQLAlchemy model for electrical conductor connections."""
    __tablename__ = "equipment_edges"

    id = Column(String(64), primary_key=True)
    from_node_tag = Column(String(64), index=True, nullable=False)
    from_port = Column(String(32), default="LOAD")
    to_node_tag = Column(String(64), index=True, nullable=False)
    to_port = Column(String(32), default="LINE")
    conductor_spec = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class PanelScheduleRecord(Base):
    """SQLAlchemy model storing the 42-slot circuit matrix for a panelboard."""
    __tablename__ = "panel_schedules"

    panel_tag = Column(String(64), primary_key=True)
    slots_count = Column(Integer, default=42)
    circuits_data = Column(JSON, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SiteConfigRecord(Base):
    """SQLAlchemy model storing site profile and electrical service configuration."""
    __tablename__ = "site_config"

    id = Column(Integer, primary_key=True, default=1)
    client_id = Column(String(64), index=True, nullable=False)
    facility_id = Column(String(64), index=True, nullable=False)

    # Facility Identity & Location
    facility_name = Column(String(128), nullable=False)
    street_address = Column(String(256), nullable=True, default="")
    city = Column(String(64), nullable=True, default="")
    state = Column(String(32), nullable=True, default="")
    postal_code = Column(String(32), nullable=True, default="")
    country = Column(String(64), default="USA")

    # Electrical Service Configuration
    service_voltage = Column(String(64), default="480Y/277V 3Ø 4W")
    service_amperage = Column(Float, default=3000.0)
    service_phase = Column(Integer, default=3)
    service_wires = Column(Integer, default=4)
    service_frequency = Column(String(16), default="60 Hz")
    service_type = Column(String(64), default="Underground Pad-Mounted")
    main_disconnect_type = Column(String(64), default="Main Circuit Breaker (MCB)")
    available_fault_current_ka = Column(Float, default=65.0)

    # Utility Provider
    utility_name = Column(String(128), nullable=True, default="")
    utility_account_number = Column(String(64), nullable=True, default="")
    utility_meter_number = Column(String(64), nullable=True, default="")
    utility_transformer_id = Column(String(64), nullable=True, default="")

    # Key Contacts
    primary_contact_name = Column(String(128), nullable=True, default="")
    primary_contact_title = Column(String(128), nullable=True, default="")
    primary_contact_email = Column(String(128), nullable=True, default="")
    primary_contact_phone = Column(String(64), nullable=True, default="")
    emergency_contact_name = Column(String(128), nullable=True, default="")
    emergency_contact_phone = Column(String(64), nullable=True, default="")
    facility_operating_hours = Column(String(64), default="24/7 Operations")

    # Compliance & Safety
    nec_edition = Column(String(32), default="NEC 2023")
    arc_flash_study_date = Column(String(32), nullable=True, default="")
    arc_flash_status = Column(String(64), default="Verified / Compliant")
    notes = Column(Text, nullable=True, default="")

    # Raw JSON payload for extended dynamic fields
    attributes = Column(JSON, default=dict)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


def sanitize_identifier(val: str, default: str = "default") -> str:
    """Sanitize client or facility identifier into a safe filesystem slug, rejecting phantom template expressions."""
    if not val:
        return default
    clean = str(val).strip().lower()
    if "${" in clean or clean.startswith("$"):
        clean = re.sub(r'[\$\{\}\(\)]', '', clean)
    clean = re.sub(r'[^a-zA-Z0-9_\-]', '_', clean).strip('_')
    return clean or default


def get_facility_dir(client_id: str, facility_id: str) -> Path:
    """Return and ensure directory path for a client facility."""
    clean_c = sanitize_identifier(client_id, "default_client")
    clean_f = sanitize_identifier(facility_id, "main_facility")
    path = CLIENTS_DATA_DIR / clean_c / clean_f
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_db_path(client_id: str, facility_id: str) -> Path:
    """Return path to client facility SQLite DB."""
    return get_facility_dir(client_id, facility_id) / "model.db"


def get_jsonl_path(client_id: str, facility_id: str) -> Path:
    """Return path to client facility companion JSONL file."""
    return get_facility_dir(client_id, facility_id) / "model.jsonl"


def get_site_config_path(client_id: str, facility_id: str) -> Path:
    """Return path to client facility companion site_config.json file."""
    return get_facility_dir(client_id, facility_id) / "site_config.json"



def get_engine(client_id: str, facility_id: str):
    """Create or return SQLAlchemy engine for client SQLite database."""
    db_file = get_db_path(client_id, facility_id)
    engine = create_engine(f"sqlite:///{db_file}", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    return engine


def get_session(client_id: str, facility_id: str) -> Session:
    """Return a new SQLAlchemy Session bound to client SQLite database."""
    engine = get_engine(client_id, facility_id)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()


def export_to_jsonl(client_id: str, facility_id: str) -> Path:
    """Export all equipment records from SQLite to a clean 1-line-per-asset JSONL file."""
    jsonl_file = get_jsonl_path(client_id, facility_id)
    with get_session(client_id, facility_id) as session:
        records = session.query(NodeRecord).order_by(NodeRecord.survey_sequence.asc()).all()
        lines = []
        for r in records:
            item_dict = {
                "id": r.id,
                "tag": r.tag,
                "name": r.name,
                "object_class": r.object_class,
                "domain": r.domain,
                "type_tag": r.type_tag,
                "type_name": r.type_name,
                "room": r.room,
                "fed_from": r.fed_from,
                "voltage": r.voltage,
                "amps": r.amps,
                "aic": r.aic,
                "is_panel": bool(r.is_panel),
                "slots": r.slots,
                "survey_sequence": r.survey_sequence,
                "status": r.status,
                "attributes": r.attributes,
            }
            lines.append(json.dumps(item_dict))

        jsonl_file.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")

    try:
        from james_app.gcs_sync import sync_client_facility_to_gcs
        sync_client_facility_to_gcs(client_id, facility_id)
    except Exception:
        pass

    return jsonl_file


def get_verified_demo_assets() -> List[Dict[str, Any]]:
    """Return the authoritative, physically verified digital twin asset model for demo facilities."""
    return [
        {
            "id": "s1", "tag": "UTIL-1", "name": "Utility Grid Service Entrance",
            "object_class": "UtilityServiceSource", "domain": "sources", "type_tag": "UTIL",
            "type_name": "Utility Grid Service Entrance", "room": "Level 1 - Main Electric Room 101",
            "fed_from": None, "voltage": "480Y/277V 3Ø 4W", "amps": 2500.0, "aic": 100.0,
            "is_panel": 0, "slots": 0, "survey_sequence": 1, "status": "VERIFIED",
            "attributes": {
                "service_mva": 250.0,
                "transformer_type": "Pad-Mounted Utility Transformer",
                "utility_name": "Consumers Energy",
                "service_voltage": "480Y/277V",
                "meter_number": "MTR-2500-01"
            }
        },
        {
            "id": "s2", "tag": "GEN-1", "name": "750 kW Standby Diesel Generator",
            "object_class": "DieselGeneratorObject", "domain": "sources", "type_tag": "GEN",
            "type_name": "Emergency Diesel Generator", "room": "Yard - Generator Pad",
            "fed_from": None, "voltage": "480Y/277V 3Ø 4W", "amps": 1128.0, "aic": 35.0,
            "is_panel": 0, "slots": 0, "survey_sequence": 2, "status": "VERIFIED",
            "attributes": {
                "kw": 750.0,
                "kva": 937.5,
                "fuel_type": "Diesel",
                "fuel_tank_gal": 1500,
                "runtime_hours": 124.5,
                "main_breaker_a": 1200.0
            }
        },
        {
            "id": "s3", "tag": "ATS-1", "name": "400A Life Safety Transfer Switch",
            "object_class": "AutomaticTransferSwitchObject", "domain": "switches", "type_tag": "ATS",
            "type_name": "Automatic Transfer Switch (ATS)", "room": "Level 1 - Main Electric Room 101",
            "fed_from": "UTIL-1", "voltage": "480Y/277V 3Ø 4W", "amps": 400.0, "aic": 65.0,
            "is_panel": 0, "slots": 0, "survey_sequence": 3, "status": "VERIFIED",
            "attributes": {
                "transition": "Open Transition",
                "emergency_source": "GEN-1",
                "enclosure_rating": "NEMA 1",
                "notes": [
                    {"id": "n1", "text": "Inspected 400A Class J fast-acting fuses. Arc flash label verified (2024).", "date": "09/06 09:30", "author": "Field Survey"},
                    {"id": "n2", "text": "Auxiliary microswitch contacts wired for SCADA generator start signal.", "date": "09/06 09:45", "author": "Field Survey"}
                ]
            }
        },
        {
            "id": "s4", "tag": "MDP-1", "name": "Main Distribution Switchboard",
            "object_class": "MainDistributionPanelObject", "domain": "panels", "type_tag": "MDP",
            "type_name": "Main Distribution Switchboard", "room": "Level 1 - Main Electric Room 101",
            "fed_from": "ATS-1", "voltage": "480Y/277V 3Ø 4W", "amps": 1200.0, "aic": 65.0,
            "is_panel": 1, "slots": 42, "survey_sequence": 4, "status": "VERIFIED",
            "attributes": {
                "bus_rating_a": 1200.0,
                "main_device": "MCB",
                "main_type": "MCB (Main Breaker)",
                "schedule": [
                    {
                        "leftSlot": 1, "leftDesc": "Feeder to Transformer T-1", "leftTrip": "100", "leftPoles": 3,
                        "leftType": "MCCB", "leftWire": "1/0 AWG Cu", "leftTargetLoad": "T-1", "leftParentSlot": None, "leftIsGanged": False,
                        "phase": "A", "phaseColor": "text-red-500"
                    },
                    {
                        "leftSlot": 3, "leftDesc": "↳ Ganged with Slot #1 (Phase B)", "leftTrip": "100", "leftPoles": 3,
                        "leftType": "MCCB", "leftWire": "1/0 AWG Cu", "leftTargetLoad": "T-1", "leftParentSlot": 1, "leftIsGanged": True,
                        "phase": "B", "phaseColor": "text-blue-500"
                    },
                    {
                        "leftSlot": 5, "leftDesc": "↳ Ganged with Slot #1 (Phase C)", "leftTrip": "100", "leftPoles": 3,
                        "leftType": "MCCB", "leftWire": "1/0 AWG Cu", "leftTargetLoad": "T-1", "leftParentSlot": 1, "leftIsGanged": True,
                        "phase": "C", "phaseColor": "text-emerald-500"
                    },
                    {
                        "leftSlot": 7, "leftDesc": "Feeder to Motor Control Center MCC-1", "leftTrip": "400", "leftPoles": 3,
                        "leftType": "MCCB", "leftWire": "500 kcmil Cu", "leftTargetLoad": "MCC-1", "leftParentSlot": None, "leftIsGanged": False,
                        "phase": "A", "phaseColor": "text-red-500"
                    },
                    {
                        "leftSlot": 9, "leftDesc": "↳ Ganged with Slot #7 (Phase B)", "leftTrip": "400", "leftPoles": 3,
                        "leftType": "MCCB", "leftWire": "500 kcmil Cu", "leftTargetLoad": "MCC-1", "leftParentSlot": 7, "leftIsGanged": True,
                        "phase": "B", "phaseColor": "text-blue-500"
                    },
                    {
                        "leftSlot": 11, "leftDesc": "↳ Ganged with Slot #7 (Phase C)", "leftTrip": "400", "leftPoles": 3,
                        "leftType": "MCCB", "leftWire": "500 kcmil Cu", "leftTargetLoad": "MCC-1", "leftParentSlot": 7, "leftIsGanged": True,
                        "phase": "C", "phaseColor": "text-emerald-500"
                    },
                    {
                        "leftSlot": 13, "leftDesc": "Feeder to Data Center UPS-1", "leftTrip": "350", "leftPoles": 3,
                        "leftType": "MCCB", "leftWire": "350 kcmil Cu", "leftTargetLoad": "UPS-1", "leftParentSlot": None, "leftIsGanged": False,
                        "phase": "A", "phaseColor": "text-red-500"
                    },
                    {
                        "leftSlot": 15, "leftDesc": "↳ Ganged with Slot #13 (Phase B)", "leftTrip": "350", "leftPoles": 3,
                        "leftType": "MCCB", "leftWire": "350 kcmil Cu", "leftTargetLoad": "UPS-1", "leftParentSlot": 13, "leftIsGanged": True,
                        "phase": "B", "phaseColor": "text-blue-500"
                    },
                    {
                        "leftSlot": 17, "leftDesc": "↳ Ganged with Slot #13 (Phase C)", "leftTrip": "350", "leftPoles": 3,
                        "leftType": "MCCB", "leftWire": "350 kcmil Cu", "leftTargetLoad": "UPS-1", "leftParentSlot": 13, "leftIsGanged": True,
                        "phase": "C", "phaseColor": "text-emerald-500"
                    }
                ],
                "notes": [
                    {"id": "n3", "text": "Main breaker is 1200A Frame / 1200A Sensor with LSIG electronic trip unit.", "date": "09/06 10:15", "author": "Field Survey"}
                ]
            }
        },
        {
            "id": "s5", "tag": "T-1", "name": "75 kVA Step-Down Transformer",
            "object_class": "DryTypeStepDownTransformerObject", "domain": "transformers", "type_tag": "XFMR",
            "type_name": "Dry-Type Step-Down Transformer", "room": "Level 1 - Main Electric Room 101",
            "fed_from": "MDP-1", "voltage": "480V : 208Y/120V 3Ø 4W", "amps": 208.0, "aic": 22.0,
            "is_panel": 0, "slots": 0, "survey_sequence": 5, "status": "VERIFIED",
            "attributes": {
                "kva": 75.0,
                "prim_v": 480.0,
                "sec_v": 208.0,
                "impedance_z": 4.8,
                "winding": "Copper",
                "temp_rise_c": 115.0
            }
        },
        {
            "id": "s6", "tag": "LP-1A", "name": "Floor 1 Lighting & Receptacle Panel",
            "object_class": "LightingBranchPanelObject", "domain": "panels", "type_tag": "LP",
            "type_name": "Lighting & Appliance Branch Panel", "room": "Level 1 - Electrical Closet 102",
            "fed_from": "T-1", "voltage": "208Y/120V 3Ø 4W", "amps": 225.0, "aic": 22.0,
            "is_panel": 1, "slots": 42, "survey_sequence": 6, "status": "VERIFIED",
            "attributes": {
                "bus_rating_a": 225.0,
                "main_device": "MLO",
                "main_type": "MLO (Main Lugs)",
                "schedule": [
                    {
                        "leftSlot": 1, "leftDesc": "Water Heater WH-1", "leftTrip": "30", "leftPoles": 2, "leftType": "MCCB", "leftWire": "10 AWG Cu", "leftTargetLoad": "", "leftParentSlot": None, "leftIsGanged": False,
                        "phase": "A", "phaseColor": "text-red-500",
                        "rightSlot": 2, "rightDesc": "Office 101-105 Lighting", "rightTrip": "20", "rightPoles": 1, "rightType": "MCCB", "rightWire": "12 AWG Cu", "rightTargetLoad": "", "rightParentSlot": None, "rightIsGanged": False
                    },
                    {
                        "leftSlot": 3, "leftDesc": "↳ Ganged with Slot #1 (Phase B)", "leftTrip": "30", "leftPoles": 2, "leftType": "MCCB", "leftWire": "10 AWG Cu", "leftTargetLoad": "", "leftParentSlot": 1, "leftIsGanged": True,
                        "phase": "B", "phaseColor": "text-blue-500",
                        "rightSlot": 4, "rightDesc": "Corridor & Restroom Lighting", "rightTrip": "20", "rightPoles": 1, "rightType": "MCCB", "rightWire": "12 AWG Cu", "rightTargetLoad": "", "rightParentSlot": None, "rightIsGanged": False
                    },
                    {
                        "leftSlot": 5, "leftDesc": "", "leftTrip": "", "leftPoles": 1, "leftType": "MCCB", "leftWire": "12 AWG Cu", "leftTargetLoad": "", "leftParentSlot": None, "leftIsGanged": False,
                        "phase": "C", "phaseColor": "text-emerald-500",
                        "rightSlot": 6, "rightDesc": "Emergency Egress Lighting", "rightTrip": "20", "rightPoles": 1, "rightType": "MCCB", "rightWire": "12 AWG Cu", "rightTargetLoad": "", "rightParentSlot": None, "rightIsGanged": False
                    },
                    {
                        "leftSlot": 7, "leftDesc": "Breakroom Kitchenette Receptacles", "leftTrip": "20", "leftPoles": 2, "leftType": "MCCB", "leftWire": "12 AWG Cu", "leftTargetLoad": "", "leftParentSlot": None, "leftIsGanged": False,
                        "phase": "A", "phaseColor": "text-red-500",
                        "rightSlot": 8, "rightDesc": "Air Handler AHU-1", "rightTrip": "50", "rightPoles": 3, "rightType": "MCCB", "rightWire": "8 AWG Cu", "rightTargetLoad": "", "rightParentSlot": None, "rightIsGanged": False
                    },
                    {
                        "leftSlot": 9, "leftDesc": "↳ Ganged with Slot #7 (Phase B)", "leftTrip": "20", "leftPoles": 2, "leftType": "MCCB", "leftWire": "12 AWG Cu", "leftTargetLoad": "", "leftParentSlot": 7, "leftIsGanged": True,
                        "phase": "B", "phaseColor": "text-blue-500",
                        "rightSlot": 10, "rightDesc": "↳ Ganged with Slot #8 (Phase B)", "rightTrip": "50", "rightPoles": 3, "rightType": "MCCB", "rightWire": "8 AWG Cu", "rightTargetLoad": "", "rightParentSlot": 8, "rightIsGanged": True
                    },
                    {
                        "leftSlot": 11, "leftDesc": "", "leftTrip": "", "leftPoles": 1, "leftType": "MCCB", "leftWire": "12 AWG Cu", "leftTargetLoad": "", "leftParentSlot": None, "leftIsGanged": False,
                        "phase": "C", "phaseColor": "text-emerald-500",
                        "rightSlot": 12, "rightDesc": "↳ Ganged with Slot #8 (Phase C)", "rightTrip": "50", "rightPoles": 3, "rightType": "MCCB", "rightWire": "8 AWG Cu", "rightTargetLoad": "", "rightParentSlot": 8, "rightIsGanged": True
                    }
                ]
            }
        },
        {
            "id": "s7", "tag": "MCC-1", "name": "Process Motor Control Center",
            "object_class": "MotorControlCenterObject", "domain": "panels", "type_tag": "MCC",
            "type_name": "Motor Control Center (MCC)", "room": "Penthouse - Mechanical Room",
            "fed_from": "MDP-1", "voltage": "480V 3Ø 3W", "amps": 800.0, "aic": 65.0,
            "is_panel": 1, "slots": 24, "survey_sequence": 7, "status": "VERIFIED",
            "attributes": {
                "bus_rating_a": 800.0,
                "main_device": "MCB",
                "main_type": "MCB (Main Breaker)",
                "schedule": [
                    {
                        "leftSlot": 1, "leftDesc": "Central Plant Chiller CH-1", "leftTrip": "400", "leftPoles": 3,
                        "leftType": "MCCB", "leftWire": "500 kcmil Cu", "leftTargetLoad": "CH-1", "leftParentSlot": None, "leftIsGanged": False,
                        "phase": "A", "phaseColor": "text-red-500"
                    },
                    {
                        "leftSlot": 3, "leftDesc": "↳ Ganged with Bucket #1 (Phase B)", "leftTrip": "400", "leftPoles": 3,
                        "leftType": "MCCB", "leftWire": "500 kcmil Cu", "leftTargetLoad": "CH-1", "leftParentSlot": 1, "leftIsGanged": True,
                        "phase": "B", "phaseColor": "text-blue-500"
                    },
                    {
                        "leftSlot": 5, "leftDesc": "↳ Ganged with Bucket #1 (Phase C)", "leftTrip": "400", "leftPoles": 3,
                        "leftType": "MCCB", "leftWire": "500 kcmil Cu", "leftTargetLoad": "CH-1", "leftParentSlot": 1, "leftIsGanged": True,
                        "phase": "C", "phaseColor": "text-emerald-500"
                    },
                    {
                        "leftSlot": 7, "leftDesc": "Chilled Water Pump P-1", "leftTrip": "100", "leftPoles": 3,
                        "leftType": "FVNR", "leftWire": "1/0 AWG Cu", "leftTargetLoad": "P-1", "leftParentSlot": None, "leftIsGanged": False,
                        "phase": "A", "phaseColor": "text-red-500"
                    },
                    {
                        "leftSlot": 9, "leftDesc": "↳ Ganged with Bucket #7 (Phase B)", "leftTrip": "100", "leftPoles": 3,
                        "leftType": "FVNR", "leftWire": "1/0 AWG Cu", "leftTargetLoad": "P-1", "leftParentSlot": 7, "leftIsGanged": True,
                        "phase": "B", "phaseColor": "text-blue-500"
                    },
                    {
                        "leftSlot": 11, "leftDesc": "↳ Ganged with Bucket #7 (Phase C)", "leftTrip": "100", "leftPoles": 3,
                        "leftType": "FVNR", "leftWire": "1/0 AWG Cu", "leftTargetLoad": "P-1", "leftParentSlot": 7, "leftIsGanged": True,
                        "phase": "C", "phaseColor": "text-emerald-500"
                    }
                ]
            }
        },
        {
            "id": "s8", "tag": "CH-1", "name": "Central Plant Water Chiller",
            "object_class": "HvacEquipmentObject", "domain": "loads", "type_tag": "HVAC",
            "type_name": "Centrifugal Water-Cooled Chiller", "room": "Penthouse - Mechanical Room",
            "fed_from": "MCC-1", "voltage": "480V 3Ø", "amps": 285.0, "aic": 65.0,
            "is_panel": 0, "slots": 0, "survey_sequence": 8, "status": "VERIFIED",
            "attributes": {
                "mca": 285.0,
                "mocp": 400.0,
                "tonnage": 250.0,
                "refrigerant": "R-134a",
                "compressor_type": "Centrifugal"
            }
        },
        {
            "id": "s9", "tag": "P-1", "name": "Chilled Water Primary Pump",
            "object_class": "HvacEquipmentObject", "domain": "loads", "type_tag": "PUMP",
            "type_name": "Centrifugal Water Pump", "room": "Penthouse - Mechanical Room",
            "fed_from": "MCC-1", "voltage": "480V 3Ø", "amps": 65.0, "aic": 65.0,
            "is_panel": 0, "slots": 0, "survey_sequence": 9, "status": "VERIFIED",
            "attributes": {
                "hp": 50.0,
                "fla": 65.0,
                "rpm": 1750,
                "impeller_dia_in": 8.5
            }
        },
        {
            "id": "s10", "tag": "UPS-1", "name": "250 kVA Data Center UPS",
            "object_class": "UpsObject", "domain": "power_quality", "type_tag": "UPS",
            "type_name": "Double-Conversion Static UPS", "room": "Level 1 - Main Electric Room 101",
            "fed_from": "MDP-1", "voltage": "480V 3Ø", "amps": 300.0, "aic": 65.0,
            "is_panel": 0, "slots": 0, "survey_sequence": 10, "status": "VERIFIED",
            "attributes": {
                "kva": 250.0,
                "kw": 250.0,
                "efficiency_pct": 96.5,
                "battery_v": 480.0,
                "runtime_min": 15.0
            }
        },
    ]


def get_208v_site_seed_assets() -> List[Dict[str, Any]]:
    """Return realistic 208Y/120V 3Ø 4W electrical digital twin equipment stack with no 480V step-down transformer."""
    return [
        {
            "id": "s1", "tag": "UTIL-1", "name": "Utility Grid Service Entrance (208Y/120V)",
            "object_class": "UtilityServiceSource", "domain": "sources", "type_tag": "UTIL",
            "type_name": "Utility Grid Service Entrance", "room": "Main Electrical Service Room",
            "fed_from": None, "voltage": "208Y/120V 3Ø 4W", "amps": 800.0, "aic": 65.0,
            "is_panel": 0, "slots": 0, "survey_sequence": 1, "status": "VERIFIED",
            "attributes": {
                "service_mva": 100.0,
                "transformer_type": "Utility Network Transformer",
                "utility_name": "Local Electric Utility",
                "service_voltage": "208Y/120V",
                "meter_number": "MTR-208-800A"
            }
        },
        {
            "id": "s2", "tag": "MSB-1", "name": "Main Service Switchboard (208Y/120V)",
            "object_class": "MainDistributionPanelObject", "domain": "panels", "type_tag": "MDP",
            "type_name": "Main Service Switchboard", "room": "Main Electrical Service Room",
            "fed_from": "UTIL-1", "voltage": "208Y/120V 3Ø 4W", "amps": 800.0, "aic": 42.0,
            "is_panel": 1, "slots": 42, "survey_sequence": 2, "status": "VERIFIED",
            "attributes": {
                "bus_rating_a": 800.0,
                "main_device": "MCB",
                "main_type": "MCB (Main Breaker)",
                "schedule": [
                    {
                        "leftSlot": 1, "leftDesc": "Feeder to Lighting Panel LP-1", "leftTrip": "225", "leftPoles": 3,
                        "leftType": "MCCB", "leftWire": "4/0 AWG Cu", "leftTargetLoad": "LP-1", "leftParentSlot": None, "leftIsGanged": False,
                        "phase": "A", "phaseColor": "text-red-500"
                    },
                    {
                        "leftSlot": 3, "leftDesc": "↳ Ganged with Slot #1 (Phase B)", "leftTrip": "225", "leftPoles": 3,
                        "leftType": "MCCB", "leftWire": "4/0 AWG Cu", "leftTargetLoad": "LP-1", "leftParentSlot": 1, "leftIsGanged": True,
                        "phase": "B", "phaseColor": "text-blue-500"
                    },
                    {
                        "leftSlot": 5, "leftDesc": "↳ Ganged with Slot #1 (Phase C)", "leftTrip": "225", "leftPoles": 3,
                        "leftType": "MCCB", "leftWire": "4/0 AWG Cu", "leftTargetLoad": "LP-1", "leftParentSlot": 1, "leftIsGanged": True,
                        "phase": "C", "phaseColor": "text-emerald-500"
                    },
                    {
                        "leftSlot": 7, "leftDesc": "Feeder to Power Panel PP-1", "leftTrip": "225", "leftPoles": 3,
                        "leftType": "MCCB", "leftWire": "4/0 AWG Cu", "leftTargetLoad": "PP-1", "leftParentSlot": None, "leftIsGanged": False,
                        "phase": "A", "phaseColor": "text-red-500"
                    },
                    {
                        "leftSlot": 9, "leftDesc": "↳ Ganged with Slot #7 (Phase B)", "leftTrip": "225", "leftPoles": 3,
                        "leftType": "MCCB", "leftWire": "4/0 AWG Cu", "leftTargetLoad": "PP-1", "leftParentSlot": 7, "leftIsGanged": True,
                        "phase": "B", "phaseColor": "text-blue-500"
                    },
                    {
                        "leftSlot": 11, "leftDesc": "↳ Ganged with Slot #7 (Phase C)", "leftTrip": "225", "leftPoles": 3,
                        "leftType": "MCCB", "leftWire": "4/0 AWG Cu", "leftTargetLoad": "PP-1", "leftParentSlot": 7, "leftIsGanged": True,
                        "phase": "C", "phaseColor": "text-emerald-500"
                    },
                    {
                        "leftSlot": 13, "leftDesc": "Feeder to Rooftop HVAC RTU-1", "leftTrip": "60", "leftPoles": 3,
                        "leftType": "MCCB", "leftWire": "6 AWG Cu", "leftTargetLoad": "RTU-1", "leftParentSlot": None, "leftIsGanged": False,
                        "phase": "A", "phaseColor": "text-red-500"
                    },
                    {
                        "leftSlot": 15, "leftDesc": "↳ Ganged with Slot #13 (Phase B)", "leftTrip": "60", "leftPoles": 3,
                        "leftType": "MCCB", "leftWire": "6 AWG Cu", "leftTargetLoad": "RTU-1", "leftParentSlot": 13, "leftIsGanged": True,
                        "phase": "B", "phaseColor": "text-blue-500"
                    },
                    {
                        "leftSlot": 17, "leftDesc": "↳ Ganged with Slot #13 (Phase C)", "leftTrip": "60", "leftPoles": 3,
                        "leftType": "MCCB", "leftWire": "6 AWG Cu", "leftTargetLoad": "RTU-1", "leftParentSlot": 13, "leftIsGanged": True,
                        "phase": "C", "phaseColor": "text-emerald-500"
                    },
                    {
                        "leftSlot": 19, "leftDesc": "Domestic Water Heater WH-1", "leftTrip": "30", "leftPoles": 2,
                        "leftType": "MCCB", "leftWire": "10 AWG Cu", "leftTargetLoad": "WH-1", "leftParentSlot": None, "leftIsGanged": False,
                        "phase": "A", "phaseColor": "text-red-500"
                    },
                    {
                        "leftSlot": 21, "leftDesc": "↳ Ganged with Slot #19 (Phase B)", "leftTrip": "30", "leftPoles": 2,
                        "leftType": "MCCB", "leftWire": "10 AWG Cu", "leftTargetLoad": "WH-1", "leftParentSlot": 19, "leftIsGanged": True,
                        "phase": "B", "phaseColor": "text-blue-500"
                    }
                ],
                "notes": [
                    {"id": "n1", "text": "Direct 208Y/120V service entrance switchboard - No 480V step-down transformer required.", "date": "10/21 10:00", "author": "Site Profile"}
                ]
            }
        },
        {
            "id": "s3", "tag": "LP-1", "name": "Lighting & Branch Panel",
            "object_class": "LightingBranchPanelObject", "domain": "panels", "type_tag": "LP",
            "type_name": "Lighting & Appliance Branch Panel", "room": "Electrical Closet A",
            "fed_from": "MSB-1", "voltage": "208Y/120V 3Ø 4W", "amps": 225.0, "aic": 22.0,
            "is_panel": 1, "slots": 42, "survey_sequence": 3, "status": "VERIFIED",
            "attributes": {
                "bus_rating_a": 225.0,
                "main_device": "MLO",
                "main_type": "MLO (Main Lugs)",
                "schedule": [
                    {
                        "leftSlot": 1, "leftDesc": "Office Lighting - West Wing", "leftTrip": "20", "leftPoles": 1, "leftType": "MCCB", "leftWire": "12 AWG Cu", "leftTargetLoad": "", "leftParentSlot": None, "leftIsGanged": False,
                        "phase": "A", "phaseColor": "text-red-500",
                        "rightSlot": 2, "rightDesc": "Office Lighting - East Wing", "rightTrip": "20", "rightPoles": 1, "rightType": "MCCB", "rightWire": "12 AWG Cu", "rightTargetLoad": "", "rightParentSlot": None, "rightIsGanged": False
                    },
                    {
                        "leftSlot": 3, "leftDesc": "Corridor & Restroom Lighting", "leftTrip": "20", "leftPoles": 1, "leftType": "MCCB", "leftWire": "12 AWG Cu", "leftTargetLoad": "", "leftParentSlot": None, "leftIsGanged": False,
                        "phase": "B", "phaseColor": "text-blue-500",
                        "rightSlot": 4, "rightDesc": "Exterior & Canopy Lighting", "rightTrip": "20", "rightPoles": 1, "rightType": "MCCB", "rightWire": "12 AWG Cu", "rightTargetLoad": "", "rightParentSlot": None, "rightIsGanged": False
                    },
                    {
                        "leftSlot": 5, "leftDesc": "Emergency Exit Signage & Egress", "leftTrip": "20", "leftPoles": 1, "leftType": "MCCB", "leftWire": "12 AWG Cu", "leftTargetLoad": "", "leftParentSlot": None, "leftIsGanged": False,
                        "phase": "C", "phaseColor": "text-emerald-500",
                        "rightSlot": 6, "rightDesc": "Conference Room Lighting & Controls", "rightTrip": "20", "rightPoles": 1, "rightType": "MCCB", "rightWire": "12 AWG Cu", "rightTargetLoad": "", "rightParentSlot": None, "rightIsGanged": False
                    }
                ]
            }
        },
        {
            "id": "s4", "tag": "PP-1", "name": "Receptacle & Equipment Power Panel",
            "object_class": "LightingBranchPanelObject", "domain": "panels", "type_tag": "LP",
            "type_name": "Power Panelboard", "room": "Electrical Closet B",
            "fed_from": "MSB-1", "voltage": "208Y/120V 3Ø 4W", "amps": 225.0, "aic": 22.0,
            "is_panel": 1, "slots": 42, "survey_sequence": 4, "status": "VERIFIED",
            "attributes": {
                "bus_rating_a": 225.0,
                "main_device": "MLO",
                "main_type": "MLO (Main Lugs)",
                "schedule": [
                    {
                        "leftSlot": 1, "leftDesc": "General Receptacles West", "leftTrip": "20", "leftPoles": 1, "leftType": "MCCB", "leftWire": "12 AWG Cu", "leftTargetLoad": "", "leftParentSlot": None, "leftIsGanged": False,
                        "phase": "A", "phaseColor": "text-red-500",
                        "rightSlot": 2, "rightDesc": "General Receptacles East", "rightTrip": "20", "rightPoles": 1, "rightType": "MCCB", "rightWire": "12 AWG Cu", "rightTargetLoad": "", "rightParentSlot": None, "rightIsGanged": False
                    },
                    {
                        "leftSlot": 3, "leftDesc": "Server & IT Network Rack (Dedicated)", "leftTrip": "20", "leftPoles": 1, "leftType": "MCCB", "leftWire": "12 AWG Cu", "leftTargetLoad": "", "leftParentSlot": None, "leftIsGanged": False,
                        "phase": "B", "phaseColor": "text-blue-500",
                        "rightSlot": 4, "rightDesc": "Breakroom Microwave & Coffee", "rightTrip": "20", "rightPoles": 1, "rightType": "MCCB", "rightWire": "12 AWG Cu", "rightTargetLoad": "", "rightParentSlot": None, "rightIsGanged": False
                    }
                ]
            }
        },
        {
            "id": "s5", "tag": "RTU-1", "name": "Packaged Rooftop HVAC Unit RTU-1",
            "object_class": "HvacEquipmentObject", "domain": "loads", "type_tag": "HVAC",
            "type_name": "Packaged Rooftop Unit", "room": "Roof Level",
            "fed_from": "MSB-1", "voltage": "208V 3Ø", "amps": 48.0, "aic": 22.0,
            "is_panel": 0, "slots": 0, "survey_sequence": 5, "status": "VERIFIED",
            "attributes": {
                "mca": 48.0,
                "mocp": 60.0,
                "tonnage": 10.0,
                "refrigerant": "R-410A"
            }
        },
        {
            "id": "s6", "tag": "WH-1", "name": "Commercial Water Heater WH-1",
            "object_class": "GenericEquipmentObject", "domain": "loads", "type_tag": "HEATER",
            "type_name": "Electric Storage Water Heater", "room": "Mechanical / Janitor Room",
            "fed_from": "MSB-1", "voltage": "208V 1Ø", "amps": 24.0, "aic": 22.0,
            "is_panel": 0, "slots": 0, "survey_sequence": 6, "status": "VERIFIED",
            "attributes": {
                "kw": 5.0,
                "tank_gal": 80.0,
                "element_type": "Dual Incoloy Elements"
            }
        }
    ]


DEFAULT_ZOETIS_B4_CONFIG: Dict[str, Any] = {
    "client_id": "zoetis",
    "facility_id": "b4",
    "facility_name": "Zoetis Building 4 (Manufacturing & Lab Facility)",
    "street_address": "100 Campus Drive",
    "city": "Florham Park",
    "state": "NJ",
    "postal_code": "07932",
    "country": "USA",
    "full_address": "100 Campus Drive, Florham Park, NJ 07932",
    "service_voltage": "480Y/277V 3Ø 4W",
    "service_amperage": 3000.0,
    "service_phase": 3,
    "service_wires": 4,
    "service_frequency": "60 Hz",
    "service_type": "Underground Pad-Mounted",
    "main_disconnect_type": "Main Circuit Breaker (MCB)",
    "available_fault_current_ka": 65.0,
    "utility_name": "Jersey Central Power & Light (JCP&L)",
    "utility_account_number": "JCP-994820-04",
    "utility_meter_number": "MTR-3000-B4",
    "utility_transformer_id": "TX-PAD-B4-01",
    "primary_contact_name": "Benjie Craig",
    "primary_contact_title": "Senior Electrical Facilities Manager",
    "primary_contact_email": "benjie.craig@zoetis.com",
    "primary_contact_phone": "(973) 555-0142",
    "emergency_contact_name": "Facilities Emergency Response Desk",
    "emergency_contact_phone": "(973) 555-0911",
    "facility_operating_hours": "24/7 Operations",
    "nec_edition": "NEC 2023",
    "arc_flash_study_date": "2024-06-15",
    "arc_flash_status": "Verified / Compliant",
    "notes": "Primary pharmaceutical R&D and critical pilot manufacturing facility.",
    "attributes": {}
}


def _site_config_record_to_dict(rec: SiteConfigRecord) -> Dict[str, Any]:
    """Serialize SiteConfigRecord SQLAlchemy model into JSON dictionary."""
    address_parts = [p for p in [rec.street_address, rec.city, f"{rec.state} {rec.postal_code}".strip()] if p]
    address_str = ", ".join(address_parts) if address_parts else ""
    return {
        "client_id": rec.client_id,
        "facility_id": rec.facility_id,
        "facility_name": rec.facility_name or f"{rec.client_id} - {rec.facility_id}".upper(),
        "street_address": rec.street_address or "",
        "city": rec.city or "",
        "state": rec.state or "",
        "postal_code": rec.postal_code or "",
        "country": rec.country or "USA",
        "full_address": address_str,
        "service_voltage": rec.service_voltage or "480Y/277V 3Ø 4W",
        "service_amperage": float(rec.service_amperage or 2000.0),
        "service_phase": int(rec.service_phase or 3),
        "service_wires": int(rec.service_wires or 4),
        "service_frequency": rec.service_frequency or "60 Hz",
        "service_type": rec.service_type or "Underground Pad-Mounted",
        "main_disconnect_type": rec.main_disconnect_type or "Main Circuit Breaker (MCB)",
        "available_fault_current_ka": float(rec.available_fault_current_ka or 65.0),
        "utility_name": rec.utility_name or "",
        "utility_account_number": rec.utility_account_number or "",
        "utility_meter_number": rec.utility_meter_number or "",
        "utility_transformer_id": rec.utility_transformer_id or "",
        "primary_contact_name": rec.primary_contact_name or "",
        "primary_contact_title": rec.primary_contact_title or "",
        "primary_contact_email": rec.primary_contact_email or "",
        "primary_contact_phone": rec.primary_contact_phone or "",
        "emergency_contact_name": rec.emergency_contact_name or "",
        "emergency_contact_phone": rec.emergency_contact_phone or "",
        "facility_operating_hours": rec.facility_operating_hours or "24/7 Operations",
        "nec_edition": rec.nec_edition or "NEC 2023",
        "arc_flash_study_date": rec.arc_flash_study_date or "",
        "arc_flash_status": rec.arc_flash_status or "Verified / Compliant",
        "notes": rec.notes or "",
        "attributes": rec.attributes if isinstance(rec.attributes, dict) else {},
        "updated_at": rec.updated_at.isoformat() if rec.updated_at else datetime.utcnow().isoformat()
    }


def get_site_config(client_id: str, facility_id: str) -> Dict[str, Any]:
    """Retrieve site configuration from SQLite model.db (falling back to JSON or defaults)."""
    clean_c = sanitize_identifier(client_id, "default_client")
    clean_f = sanitize_identifier(facility_id, "main_facility")

    get_facility_dir(clean_c, clean_f)
    get_engine(clean_c, clean_f)

    # 1. Try querying SQLite
    try:
        with get_session(clean_c, clean_f) as session:
            rec = session.query(SiteConfigRecord).filter_by(id=1).first()
            if rec:
                return _site_config_record_to_dict(rec)
    except Exception:
        pass

    # 2. Try loading companion site_config.json
    cfg_file = get_site_config_path(clean_c, clean_f)
    if cfg_file.exists():
        try:
            with open(cfg_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    # Persist into DB for subsequent fast queries
                    save_site_config(clean_c, clean_f, data)
                    return data
        except Exception:
            pass

    # 3. Default fallback
    if clean_c == "zoetis" and clean_f == "b4":
        default_data = dict(DEFAULT_ZOETIS_B4_CONFIG)
    else:
        default_data = {
            "client_id": clean_c,
            "facility_id": clean_f,
            "facility_name": f"{clean_c.replace('_', ' ').title()} - {clean_f.upper()}",
            "street_address": "",
            "city": "",
            "state": "",
            "postal_code": "",
            "country": "USA",
            "full_address": "",
            "service_voltage": "480Y/277V 3Ø 4W",
            "service_amperage": 2000.0,
            "service_phase": 3,
            "service_wires": 4,
            "service_frequency": "60 Hz",
            "service_type": "Underground Pad-Mounted",
            "main_disconnect_type": "Main Circuit Breaker (MCB)",
            "available_fault_current_ka": 65.0,
            "utility_name": "Local Electric Utility",
            "utility_account_number": "",
            "utility_meter_number": "",
            "utility_transformer_id": "",
            "primary_contact_name": "",
            "primary_contact_title": "Facility Electrical Lead",
            "primary_contact_email": "",
            "primary_contact_phone": "",
            "emergency_contact_name": "",
            "emergency_contact_phone": "",
            "facility_operating_hours": "Standard Commercial (7am - 6pm)",
            "nec_edition": "NEC 2023",
            "arc_flash_study_date": "",
            "arc_flash_status": "Survey Pending",
            "notes": "",
            "attributes": {}
        }

    # Auto-save defaults to initialize DB and file
    try:
        save_site_config(clean_c, clean_f, default_data)
    except Exception:
        pass
    return default_data


def save_site_config(client_id: str, facility_id: str, config_data: Dict[str, Any]) -> Dict[str, Any]:
    """Upsert site configuration into SQLite model.db and mirror to site_config.json."""
    clean_c = sanitize_identifier(client_id, "default_client")
    clean_f = sanitize_identifier(facility_id, "main_facility")

    get_facility_dir(clean_c, clean_f)
    get_engine(clean_c, clean_f)

    # Sanitize and extract fields
    fac_name = str(config_data.get("facility_name") or f"{clean_c.replace('_', ' ').title()} - {clean_f.upper()}").strip()
    street = str(config_data.get("street_address") or "").strip()
    city = str(config_data.get("city") or "").strip()
    state = str(config_data.get("state") or "").strip()
    postal = str(config_data.get("postal_code") or "").strip()
    country = str(config_data.get("country") or "USA").strip()

    voltage = str(config_data.get("service_voltage") or "480Y/277V 3Ø 4W").strip()
    try:
        amps = float(config_data.get("service_amperage") or 2000.0)
    except (ValueError, TypeError):
        amps = 2000.0

    try:
        phase = int(config_data.get("service_phase") or 3)
    except (ValueError, TypeError):
        phase = 3

    try:
        wires = int(config_data.get("service_wires") or 4)
    except (ValueError, TypeError):
        wires = 4

    freq = str(config_data.get("service_frequency") or "60 Hz").strip()
    svc_type = str(config_data.get("service_type") or "Underground Pad-Mounted").strip()
    disconnect = str(config_data.get("main_disconnect_type") or "Main Circuit Breaker (MCB)").strip()

    try:
        ka = float(config_data.get("available_fault_current_ka") or 65.0)
    except (ValueError, TypeError):
        ka = 65.0

    util_name = str(config_data.get("utility_name") or "").strip()
    util_acct = str(config_data.get("utility_account_number") or "").strip()
    util_mtr = str(config_data.get("utility_meter_number") or "").strip()
    util_xfmr = str(config_data.get("utility_transformer_id") or "").strip()

    c_name = str(config_data.get("primary_contact_name") or "").strip()
    c_title = str(config_data.get("primary_contact_title") or "").strip()
    c_email = str(config_data.get("primary_contact_email") or "").strip()
    c_phone = str(config_data.get("primary_contact_phone") or "").strip()

    e_name = str(config_data.get("emergency_contact_name") or "").strip()
    e_phone = str(config_data.get("emergency_contact_phone") or "").strip()
    hours = str(config_data.get("facility_operating_hours") or "24/7 Operations").strip()

    nec = str(config_data.get("nec_edition") or "NEC 2023").strip()
    af_date = str(config_data.get("arc_flash_study_date") or "").strip()
    af_status = str(config_data.get("arc_flash_status") or "Verified / Compliant").strip()
    notes = str(config_data.get("notes") or "").strip()
    attrs = config_data.get("attributes") if isinstance(config_data.get("attributes"), dict) else {}

    result_dict: Dict[str, Any] = {}
    with get_session(clean_c, clean_f) as session:
        rec = session.query(SiteConfigRecord).filter_by(id=1).first()
        if not rec:
            rec = SiteConfigRecord(
                id=1,
                client_id=clean_c,
                facility_id=clean_f,
                facility_name=fac_name,
                street_address=street,
                city=city,
                state=state,
                postal_code=postal,
                country=country,
                service_voltage=voltage,
                service_amperage=amps,
                service_phase=phase,
                service_wires=wires,
                service_frequency=freq,
                service_type=svc_type,
                main_disconnect_type=disconnect,
                available_fault_current_ka=ka,
                utility_name=util_name,
                utility_account_number=util_acct,
                utility_meter_number=util_mtr,
                utility_transformer_id=util_xfmr,
                primary_contact_name=c_name,
                primary_contact_title=c_title,
                primary_contact_email=c_email,
                primary_contact_phone=c_phone,
                emergency_contact_name=e_name,
                emergency_contact_phone=e_phone,
                facility_operating_hours=hours,
                nec_edition=nec,
                arc_flash_study_date=af_date,
                arc_flash_status=af_status,
                notes=notes,
                attributes=attrs,
                updated_at=datetime.utcnow()
            )
            session.add(rec)
        else:
            rec.facility_name = fac_name
            rec.street_address = street
            rec.city = city
            rec.state = state
            rec.postal_code = postal
            rec.country = country
            rec.service_voltage = voltage
            rec.service_amperage = amps
            rec.service_phase = phase
            rec.service_wires = wires
            rec.service_frequency = freq
            rec.service_type = svc_type
            rec.main_disconnect_type = disconnect
            rec.available_fault_current_ka = ka
            rec.utility_name = util_name
            rec.utility_account_number = util_acct
            rec.utility_meter_number = util_mtr
            rec.utility_transformer_id = util_xfmr
            rec.primary_contact_name = c_name
            rec.primary_contact_title = c_title
            rec.primary_contact_email = c_email
            rec.primary_contact_phone = c_phone
            rec.emergency_contact_name = e_name
            rec.emergency_contact_phone = e_phone
            rec.facility_operating_hours = hours
            rec.nec_edition = nec
            rec.arc_flash_study_date = af_date
            rec.arc_flash_status = af_status
            rec.notes = notes
            rec.attributes = attrs
            rec.updated_at = datetime.utcnow()

        session.commit()
        result_dict = _site_config_record_to_dict(rec)

    # Mirror to site_config.json
    cfg_file = get_site_config_path(clean_c, clean_f)
    try:
        with open(cfg_file, "w", encoding="utf-8") as f:
            json.dump(result_dict, f, indent=2, default=str)
    except Exception:
        pass

    return result_dict


def seed_demo_facility(client_id: str = "zoetis", facility_id: str = "b4") -> None:
    """Seed sample facility with realistic equipment stack if empty."""
    clean_c = client_id.strip().lower()
    clean_f = facility_id.strip().lower()
    get_facility_dir(clean_c, clean_f)
    get_engine(clean_c, clean_f)

    # Ensure site configuration exists
    get_site_config(clean_c, clean_f)

    with get_session(clean_c, clean_f) as session:
        if session.query(NodeRecord).count() > 0:
            return  # Already seeded

        for item in get_verified_demo_assets():
            session.add(NodeRecord(**item))
        session.commit()

    export_to_jsonl(clean_c, clean_f)


def reset_demo_facility(client_id: str = "zoetis", facility_id: str = "b4") -> None:
    """Clear and rebuild the authoritative, verified facility digital twin model."""
    with get_session(client_id, facility_id) as session:
        session.query(NodeRecord).delete()
        for item in get_verified_demo_assets():
            session.add(NodeRecord(**item))
        session.commit()

    export_to_jsonl(client_id, facility_id)


def list_all_client_facilities() -> List[Dict[str, Any]]:
    """Scan data/clients directory and return all discovered clients and their facility databases."""
    clients_map: Dict[str, Dict[str, Any]] = {}
    
    if not CLIENTS_DATA_DIR.exists():
        CLIENTS_DATA_DIR.mkdir(parents=True, exist_ok=True)

    for client_dir in sorted(CLIENTS_DATA_DIR.iterdir()):
        if not client_dir.is_dir() or client_dir.name.startswith("."):
            continue
        
        # Skip phantom or invalid template directories (e.g. '${c}' or containing '${')
        if "${" in client_dir.name or client_dir.name.startswith("$") or not re.match(r'^[a-zA-Z0-9_\-]+$', client_dir.name):
            continue
        
        client_id = client_dir.name
        facilities = []
        for fac_dir in sorted(client_dir.iterdir()):
            if not fac_dir.is_dir() or fac_dir.name.startswith("."):
                continue
            
            # Skip phantom or invalid facility directories
            if "${" in fac_dir.name or fac_dir.name.startswith("$") or not re.match(r'^[a-zA-Z0-9_\-]+$', fac_dir.name):
                continue
            
            facility_id = fac_dir.name
            db_file = fac_dir / "model.db"
            if not db_file.exists():
                continue
            
            # Count assets from SQLite
            asset_count = 0
            try:
                with get_session(client_id, facility_id) as session:
                    asset_count = session.query(NodeRecord).count()
            except Exception:
                pass

            # Fast site config extraction
            site_cfg = None
            cfg_file = fac_dir / "site_config.json"
            if cfg_file.exists():
                try:
                    with open(cfg_file, "r", encoding="utf-8") as f:
                        site_cfg = json.load(f)
                except Exception:
                    pass
            if not site_cfg and client_id == "zoetis" and facility_id == "b4":
                site_cfg = DEFAULT_ZOETIS_B4_CONFIG
            
            facility_display_name = (site_cfg.get("facility_name") if site_cfg else None) or facility_id.replace("_", " ").title()
            service_voltage = (site_cfg.get("service_voltage") if site_cfg else "480Y/277V 3Ø 4W")
            utility_name = (site_cfg.get("utility_name") if site_cfg else "")
            address_str = (site_cfg.get("full_address") if site_cfg else "") or (site_cfg.get("street_address") if site_cfg else "")

            stat = db_file.stat()
            size_kb = max(1, round(stat.st_size / 1024))
            size_str = f"{size_kb} KB" if size_kb < 1024 else f"{round(size_kb / 1024, 1)} MB"
            mod_time = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")

            facilities.append({
                "facility_id": facility_id,
                "facility_name": facility_display_name,
                "service_voltage": service_voltage,
                "utility_name": utility_name,
                "address": address_str,
                "db_path": f"data/clients/{client_id}/{facility_id}/model.db",
                "asset_count": asset_count,
                "file_size_bytes": stat.st_size,
                "file_size_str": size_str,
                "modified_at": mod_time,
            })

        if facilities:
            clients_map[client_id] = {
                "client_id": client_id,
                "client_name": client_id.replace("_", " ").title(),
                "facilities": facilities,
                "facility_count": len(facilities),
            }

    return list(clients_map.values())


def create_client_facility(
    client_id: str, 
    facility_id: str, 
    seed: bool = False,
    site_config: Optional[Dict[str, Any]] = None,
    service_voltage: Optional[str] = None
) -> Dict[str, Any]:
    """Create a new client/facility directory, save initial site profile, and initialize its SQLite database."""
    clean_client = sanitize_identifier(client_id, "default_client")
    clean_facility = sanitize_identifier(facility_id, "main_facility")

    get_facility_dir(clean_client, clean_facility)
    get_engine(clean_client, clean_facility)

    # Initialize site config
    cfg_to_save = dict(site_config or {})
    if service_voltage:
        cfg_to_save["service_voltage"] = service_voltage
    saved_config = save_site_config(clean_client, clean_facility, cfg_to_save)
    
    asset_count = 0
    with get_session(clean_client, clean_facility) as session:
        if seed and session.query(NodeRecord).count() == 0:
            volts = (saved_config.get("service_voltage") or "").strip()
            # If 208V/120V service is chosen, seed realistic 208V equipment (NO 480V step-down transformer)
            if "208" in volts or "120/208" in volts:
                assets = get_208v_site_seed_assets()
            else:
                assets = get_verified_demo_assets()

            for item in assets:
                session.add(NodeRecord(**item))
            session.commit()
        asset_count = session.query(NodeRecord).count()
    
    export_to_jsonl(clean_client, clean_facility)

    return {
        "client_id": clean_client,
        "facility_id": clean_facility,
        "db_path": f"data/clients/{clean_client}/{clean_facility}/model.db",
        "asset_count": asset_count,
        "seeded": seed,
        "site_config": saved_config
    }



def delete_client_facility(client_id: str, facility_id: str) -> bool:
    """Delete a facility directory and its databases."""
    import shutil
    # Try exact match first (allows removing phantom paths if needed)
    target_dir = CLIENTS_DATA_DIR / client_id / facility_id
    if not target_dir.exists():
        clean_client = sanitize_identifier(client_id, "")
        clean_facility = sanitize_identifier(facility_id, "")
        if clean_client and clean_facility:
            target_dir = CLIENTS_DATA_DIR / clean_client / clean_facility

    if target_dir.exists() and target_dir.is_dir():
        shutil.rmtree(target_dir, ignore_errors=True)
        parent = target_dir.parent
        if parent.exists() and parent != CLIENTS_DATA_DIR and not any(parent.iterdir()):
            shutil.rmtree(parent, ignore_errors=True)
        return True
    return False


def get_custom_breakers(client_id: Optional[str] = None, facility_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """Scan facility SQLite databases and aggregate all custom / uncataloged breakers across panel schedules."""
    discovered = {}
    
    if client_id and facility_id:
        targets = [(client_id, facility_id)]
    else:
        # Scan all client facilities
        targets = []
        if CLIENTS_DATA_DIR.exists():
            for c_dir in sorted(CLIENTS_DATA_DIR.iterdir()):
                if c_dir.is_dir() and not c_dir.name.startswith("."):
                    for f_dir in sorted(c_dir.iterdir()):
                        if f_dir.is_dir() and not f_dir.name.startswith("."):
                            if (f_dir / "model.db").exists():
                                targets.append((c_dir.name, f_dir.name))

    for c, f in targets:
        with get_session(c, f) as session:
            nodes = session.query(NodeRecord).all()
            for node in nodes:
                attrs = node.attributes if isinstance(node.attributes, dict) else {}
                sched = attrs.get("schedule", [])
                if not sched or not isinstance(sched, list):
                    continue
                for row in sched:
                    if not isinstance(row, dict):
                        continue
                    # Check left side
                    if row.get("leftTrip") and (row.get("leftPartNo") or row.get("leftPartNumber")):
                        part_no = (row.get("leftPartNo") or row.get("leftPartNumber") or "").strip()
                        is_custom = row.get("leftIsCustom") or row.get("leftCatalogStatus") == "custom_pending"
                        if part_no:
                            key = (part_no.upper(), (row.get("leftMfr") or "").strip().upper())
                            if key not in discovered:
                                discovered[key] = {
                                    "part_number": part_no,
                                    "manufacturer": (row.get("leftMfr") or "").strip() or "Custom / Generic",
                                    "poles": int(row.get("leftPoles") or 1),
                                    "trip_amps": float(row.get("leftTrip") or 20.0),
                                    "trip_type": row.get("leftType") or "MCCB",
                                    "wire": row.get("leftWire") or "",
                                    "is_custom": bool(is_custom),
                                    "catalog_status": row.get("leftCatalogStatus") or ("custom_pending" if is_custom else "verified"),
                                    "occurrences": 0,
                                    "discovered_locations": []
                                }
                            discovered[key]["occurrences"] += 1
                            discovered[key]["discovered_locations"].append({
                                "client": c,
                                "facility": f,
                                "panel_tag": node.tag,
                                "panel_name": node.name,
                                "slot": row.get("leftSlot")
                            })

                    # Check right side
                    if row.get("rightTrip") and (row.get("rightPartNo") or row.get("rightPartNumber")):
                        part_no = (row.get("rightPartNo") or row.get("rightPartNumber") or "").strip()
                        is_custom = row.get("rightIsCustom") or row.get("rightCatalogStatus") == "custom_pending"
                        if part_no:
                            key = (part_no.upper(), (row.get("rightMfr") or "").strip().upper())
                            if key not in discovered:
                                discovered[key] = {
                                    "part_number": part_no,
                                    "manufacturer": (row.get("rightMfr") or "").strip() or "Custom / Generic",
                                    "poles": int(row.get("rightPoles") or 1),
                                    "trip_amps": float(row.get("rightTrip") or 20.0),
                                    "trip_type": row.get("rightType") or "MCCB",
                                    "wire": row.get("rightWire") or "",
                                    "is_custom": bool(is_custom),
                                    "catalog_status": row.get("rightCatalogStatus") or ("custom_pending" if is_custom else "verified"),
                                    "occurrences": 0,
                                    "discovered_locations": []
                                }
                            discovered[key]["occurrences"] += 1
                            discovered[key]["discovered_locations"].append({
                                "client": c,
                                "facility": f,
                                "panel_tag": node.tag,
                                "panel_name": node.name,
                                "slot": row.get("rightSlot")
                            })

    return sorted(list(discovered.values()), key=lambda x: (-x["occurrences"], x["part_number"]))




