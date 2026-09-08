"""Database Layer: Client-Isolated SQLite + JSONL Multi-Tenant Architecture with SQLAlchemy ORM."""

import json
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
CLIENTS_DATA_DIR = BASE_DIR / "data" / "clients"

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


def get_facility_dir(client_id: str, facility_id: str) -> Path:
    """Return and ensure directory path for a client facility."""
    path = CLIENTS_DATA_DIR / client_id / facility_id
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_db_path(client_id: str, facility_id: str) -> Path:
    """Return path to client facility SQLite DB."""
    return get_facility_dir(client_id, facility_id) / "model.db"


def get_jsonl_path(client_id: str, facility_id: str) -> Path:
    """Return path to client facility companion JSONL file."""
    return get_facility_dir(client_id, facility_id) / "model.jsonl"


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
                        "leftType": "MCCB", "leftWire": "1/0 AWG Cu", "leftTargetLoad": "T-1", "leftParentSlot": None, "leftIsGanged": False
                    },
                    {
                        "leftSlot": 3, "leftDesc": "↳ Ganged with Slot #1 (Phase B)", "leftTrip": "100", "leftPoles": 3,
                        "leftType": "MCCB", "leftWire": "1/0 AWG Cu", "leftTargetLoad": "T-1", "leftParentSlot": 1, "leftIsGanged": True
                    },
                    {
                        "leftSlot": 5, "leftDesc": "↳ Ganged with Slot #1 (Phase C)", "leftTrip": "100", "leftPoles": 3,
                        "leftType": "MCCB", "leftWire": "1/0 AWG Cu", "leftTargetLoad": "T-1", "leftParentSlot": 1, "leftIsGanged": True
                    },
                    {
                        "leftSlot": 7, "leftDesc": "Feeder to Motor Control Center MCC-1", "leftTrip": "400", "leftPoles": 3,
                        "leftType": "MCCB", "leftWire": "500 kcmil Cu", "leftTargetLoad": "MCC-1", "leftParentSlot": None, "leftIsGanged": False
                    },
                    {
                        "leftSlot": 9, "leftDesc": "↳ Ganged with Slot #7 (Phase B)", "leftTrip": "400", "leftPoles": 3,
                        "leftType": "MCCB", "leftWire": "500 kcmil Cu", "leftTargetLoad": "MCC-1", "leftParentSlot": 7, "leftIsGanged": True
                    },
                    {
                        "leftSlot": 11, "leftDesc": "↳ Ganged with Slot #7 (Phase C)", "leftTrip": "400", "leftPoles": 3,
                        "leftType": "MCCB", "leftWire": "500 kcmil Cu", "leftTargetLoad": "MCC-1", "leftParentSlot": 7, "leftIsGanged": True
                    },
                    {
                        "leftSlot": 13, "leftDesc": "Feeder to Data Center UPS-1", "leftTrip": "350", "leftPoles": 3,
                        "leftType": "MCCB", "leftWire": "350 kcmil Cu", "leftTargetLoad": "UPS-1", "leftParentSlot": None, "leftIsGanged": False
                    },
                    {
                        "leftSlot": 15, "leftDesc": "↳ Ganged with Slot #13 (Phase B)", "leftTrip": "350", "leftPoles": 3,
                        "leftType": "MCCB", "leftWire": "350 kcmil Cu", "leftTargetLoad": "UPS-1", "leftParentSlot": 13, "leftIsGanged": True
                    },
                    {
                        "leftSlot": 17, "leftDesc": "↳ Ganged with Slot #13 (Phase C)", "leftTrip": "350", "leftPoles": 3,
                        "leftType": "MCCB", "leftWire": "350 kcmil Cu", "leftTargetLoad": "UPS-1", "leftParentSlot": 13, "leftIsGanged": True
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
                        "rightSlot": 2, "rightDesc": "Office 101-105 Lighting", "rightTrip": "20", "rightPoles": 1, "rightType": "MCCB", "rightWire": "12 AWG Cu", "rightTargetLoad": "", "rightParentSlot": None, "rightIsGanged": False
                    },
                    {
                        "leftSlot": 3, "leftDesc": "↳ Ganged with Slot #1 (Phase B)", "leftTrip": "30", "leftPoles": 2, "leftType": "MCCB", "leftWire": "10 AWG Cu", "leftTargetLoad": "", "leftParentSlot": 1, "leftIsGanged": True,
                        "rightSlot": 4, "rightDesc": "Corridor & Restroom Lighting", "rightTrip": "20", "rightPoles": 1, "rightType": "MCCB", "rightWire": "12 AWG Cu", "rightTargetLoad": "", "rightParentSlot": None, "rightIsGanged": False
                    },
                    {
                        "leftSlot": 5, "leftDesc": "", "leftTrip": "", "leftPoles": 1, "leftType": "MCCB", "leftWire": "12 AWG Cu", "leftTargetLoad": "", "leftParentSlot": None, "leftIsGanged": False,
                        "rightSlot": 6, "rightDesc": "Emergency Egress Lighting", "rightTrip": "20", "rightPoles": 1, "rightType": "MCCB", "rightWire": "12 AWG Cu", "rightTargetLoad": "", "rightParentSlot": None, "rightIsGanged": False
                    },
                    {
                        "leftSlot": 7, "leftDesc": "Breakroom Kitchenette Receptacles", "leftTrip": "20", "leftPoles": 2, "leftType": "MCCB", "leftWire": "12 AWG Cu", "leftTargetLoad": "", "leftParentSlot": None, "leftIsGanged": False,
                        "rightSlot": 8, "rightDesc": "Air Handler AHU-1", "rightTrip": "50", "rightPoles": 3, "rightType": "MCCB", "rightWire": "8 AWG Cu", "rightTargetLoad": "", "rightParentSlot": None, "rightIsGanged": False
                    },
                    {
                        "leftSlot": 9, "leftDesc": "↳ Ganged with Slot #7 (Phase B)", "leftTrip": "20", "leftPoles": 2, "leftType": "MCCB", "leftWire": "12 AWG Cu", "leftTargetLoad": "", "leftParentSlot": 7, "leftIsGanged": True,
                        "rightSlot": 10, "rightDesc": "↳ Ganged with Slot #8 (Phase B)", "rightTrip": "50", "rightPoles": 3, "rightType": "MCCB", "rightWire": "8 AWG Cu", "rightTargetLoad": "", "rightParentSlot": 8, "rightIsGanged": True
                    },
                    {
                        "leftSlot": 11, "leftDesc": "", "leftTrip": "", "leftPoles": 1, "leftType": "MCCB", "leftWire": "12 AWG Cu", "leftTargetLoad": "", "leftParentSlot": None, "leftIsGanged": False,
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
                        "leftType": "MCCB", "leftWire": "500 kcmil Cu", "leftTargetLoad": "CH-1", "leftParentSlot": None, "leftIsGanged": False
                    },
                    {
                        "leftSlot": 3, "leftDesc": "↳ Ganged with Bucket #1 (Phase B)", "leftTrip": "400", "leftPoles": 3,
                        "leftType": "MCCB", "leftWire": "500 kcmil Cu", "leftTargetLoad": "CH-1", "leftParentSlot": 1, "leftIsGanged": True
                    },
                    {
                        "leftSlot": 5, "leftDesc": "↳ Ganged with Bucket #1 (Phase C)", "leftTrip": "400", "leftPoles": 3,
                        "leftType": "MCCB", "leftWire": "500 kcmil Cu", "leftTargetLoad": "CH-1", "leftParentSlot": 1, "leftIsGanged": True
                    },
                    {
                        "leftSlot": 7, "leftDesc": "Chilled Water Pump P-1", "leftTrip": "100", "leftPoles": 3,
                        "leftType": "FVNR", "leftWire": "1/0 AWG Cu", "leftTargetLoad": "P-1", "leftParentSlot": None, "leftIsGanged": False
                    },
                    {
                        "leftSlot": 9, "leftDesc": "↳ Ganged with Bucket #7 (Phase B)", "leftTrip": "100", "leftPoles": 3,
                        "leftType": "FVNR", "leftWire": "1/0 AWG Cu", "leftTargetLoad": "P-1", "leftParentSlot": 7, "leftIsGanged": True
                    },
                    {
                        "leftSlot": 11, "leftDesc": "↳ Ganged with Bucket #7 (Phase C)", "leftTrip": "100", "leftPoles": 3,
                        "leftType": "FVNR", "leftWire": "1/0 AWG Cu", "leftTargetLoad": "P-1", "leftParentSlot": 7, "leftIsGanged": True
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


def seed_demo_facility(client_id: str = "zoetis", facility_id: str = "b4") -> None:
    """Seed sample facility with realistic equipment stack if empty."""
    with get_session(client_id, facility_id) as session:
        if session.query(NodeRecord).count() > 0:
            return  # Already seeded

        for item in get_verified_demo_assets():
            session.add(NodeRecord(**item))
        session.commit()

    export_to_jsonl(client_id, facility_id)


def reset_demo_facility(client_id: str = "zoetis", facility_id: str = "b4") -> None:
    """Clear and rebuild the authoritative, verified facility digital twin model."""
    with get_session(client_id, facility_id) as session:
        session.query(NodeRecord).delete()
        for item in get_verified_demo_assets():
            session.add(NodeRecord(**item))
        session.commit()

    export_to_jsonl(client_id, facility_id)

