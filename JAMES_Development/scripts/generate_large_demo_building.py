"""
Script to generate a comprehensive, highly realistic 5-Story Commercial Building Electrical System
down to the room-level receptacles and appliances for client 'jemby', facility 'large_demo_bldg'.
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any

from james_app.db import (
    NodeRecord,
    EdgeRecord,
    PanelScheduleRecord,
    get_engine,
    get_session,
    export_to_jsonl,
    get_facility_dir
)


def generate_large_demo_building():
    client_id = "jemby"
    facility_id = "large_demo_bldg"
    facility_dir = get_facility_dir(client_id, facility_id)
    
    print(f"[*] Initializing large demo building for {client_id} / {facility_id} at {facility_dir}...")
    
    # Clean previous database if exists to ensure clean seed
    db_path = facility_dir / "model.db"
    jsonl_path = facility_dir / "model.jsonl"
    if db_path.exists():
        db_path.unlink()
    if jsonl_path.exists():
        jsonl_path.unlink()

    engine = get_engine(client_id, facility_id)
    session = get_session(client_id, facility_id)

    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []
    schedules: Dict[str, List[Dict[str, Any]]] = {}

    seq = 1

    def add_node(
        tag: str,
        name: str,
        object_class: str,
        domain: str,
        type_tag: str,
        type_name: str,
        room: str,
        fed_from: str = None,
        voltage: str = "480Y/277V 3Ø 4W",
        amps: float = 225.0,
        aic: float = 65.0,
        is_panel: int = 0,
        slots: int = 0,
        status: str = "VERIFIED",
        attributes: dict = None
    ):
        nonlocal seq
        node_id = f"node_{tag.lower().replace('-', '_')}"
        attr = attributes or {}
        nodes.append({
            "id": node_id,
            "tag": tag,
            "name": name,
            "object_class": object_class,
            "domain": domain,
            "type_tag": type_tag,
            "type_name": type_name,
            "room": room,
            "fed_from": fed_from,
            "voltage": voltage,
            "amps": amps,
            "aic": aic,
            "is_panel": is_panel,
            "slots": slots,
            "survey_sequence": seq,
            "status": status,
            "attributes": attr
        })
        seq += 1
        return tag

    def add_edge(from_tag: str, to_tag: str, from_port: str = "LOAD", to_port: str = "LINE", spec: dict = None):
        edge_id = f"edge_{from_tag.lower()}_{to_tag.lower()}".replace("-", "_")
        edges.append({
            "id": edge_id,
            "from_node_tag": from_tag,
            "from_port": from_port,
            "to_node_tag": to_tag,
            "to_port": to_port,
            "conductor_spec": spec or {"type": "THHN_CU", "conduit": "EMT"}
        })

    # =========================================================================
    # 1. SERVICE ENTRANCE & CENTRAL PLANT (BASEMENT)
    # =========================================================================
    add_node(
        tag="UTIL-1",
        name="Utility Grid Service Entrance (Consumers Energy)",
        object_class="UtilityServiceSource",
        domain="sources",
        type_tag="UTIL",
        type_name="Utility Grid Service Entrance",
        room="Basement - Utility Vault B01",
        fed_from=None,
        voltage="480Y/277V 3Ø 4W",
        amps=3000.0,
        aic=100.0,
        attributes={
            "utility_name": "Consumers Energy",
            "service_mva": 500.0,
            "transformer_type": "Outdoor Pad-Mounted Utility Transformer",
            "meter_number": "MTR-3000-HQ-01",
            "service_voltage": "480Y/277V 3Ø 4W"
        }
    )

    add_node(
        tag="GEN-1",
        name="1000 kW Emergency Standby Diesel Generator",
        object_class="DieselGeneratorObject",
        domain="sources",
        type_tag="GEN",
        type_name="Emergency Diesel Generator",
        room="Exterior - South Generator Enclosure",
        fed_from=None,
        voltage="480Y/277V 3Ø 4W",
        amps=1504.0,
        aic=35.0,
        attributes={
            "kw": 1000.0,
            "kva": 1250.0,
            "fuel_type": "Ultra-Low Sulfur Diesel #2",
            "fuel_tank_gal": 2500,
            "runtime_hours": 86.4,
            "main_breaker_a": 1600.0,
            "nfpa_class": "Class 48 / Type 10 / Level 1"
        }
    )

    add_node(
        tag="ATS-1",
        name="1200A 4-Pole Automatic Transfer Switch",
        object_class="AutomaticTransferSwitchObject",
        domain="switches",
        type_tag="ATS",
        type_name="Automatic Transfer Switch (ATS)",
        room="Basement - Main Electrical Room B101",
        fed_from="UTIL-1",
        voltage="480Y/277V 3Ø 4W",
        amps=1200.0,
        aic=65.0,
        attributes={
            "transition": "Closed Transition Dual-Bypass",
            "emergency_source": "GEN-1",
            "enclosure_rating": "NEMA 1 Gasketed",
            "timer_delay_sec": 10.0
        }
    )
    add_edge("UTIL-1", "ATS-1", from_port="NORMAL", to_port="NORMAL_LINE")
    add_edge("GEN-1", "ATS-1", from_port="EMERGENCY", to_port="EMERGENCY_LINE")

    add_node(
        tag="MSB-1",
        name="Main Switchboard (3000A Main-Tie-Main)",
        object_class="MainDistributionPanelObject",
        domain="panels",
        type_tag="MSB",
        type_name="Main Distribution Switchboard",
        room="Basement - Main Electrical Room B101",
        fed_from="ATS-1",
        voltage="480Y/277V 3Ø 4W",
        amps=3000.0,
        aic=65.0,
        is_panel=1,
        slots=42,
        attributes={
            "bus_rating_a": 3000.0,
            "main_device": "MCB",
            "main_type": "Drawout Air Circuit Breaker (Digitrip 1150+)",
            "spd_installed": True,
            "schedule": [
                {"leftSlot": 1, "leftDesc": "Feeder to Central Chiller CHLR-1", "leftTrip": "400", "leftPoles": 3, "leftType": "MCCB", "leftWire": "500 kcmil Cu", "leftTargetLoad": "CHLR-1", "leftParentSlot": None, "leftIsGanged": False, "phase": "A", "phaseColor": "text-red-500"},
                {"leftSlot": 3, "leftDesc": "↳ Ganged with Slot #1 (Phase B)", "leftTrip": "400", "leftPoles": 3, "leftType": "MCCB", "leftWire": "500 kcmil Cu", "leftTargetLoad": "CHLR-1", "leftParentSlot": 1, "leftIsGanged": True, "phase": "B", "phaseColor": "text-blue-500"},
                {"leftSlot": 5, "leftDesc": "↳ Ganged with Slot #1 (Phase C)", "leftTrip": "400", "leftPoles": 3, "leftType": "MCCB", "leftWire": "500 kcmil Cu", "leftTargetLoad": "CHLR-1", "leftParentSlot": 1, "leftIsGanged": True, "phase": "C", "phaseColor": "text-emerald-500"},
                {"leftSlot": 7, "leftDesc": "Feeder to Central Chiller CHLR-2", "leftTrip": "400", "leftPoles": 3, "leftType": "MCCB", "leftWire": "500 kcmil Cu", "leftTargetLoad": "CHLR-2", "leftParentSlot": None, "leftIsGanged": False, "phase": "A", "phaseColor": "text-red-500"},
                {"leftSlot": 9, "leftDesc": "↳ Ganged with Slot #7 (Phase B)", "leftTrip": "400", "leftPoles": 3, "leftType": "MCCB", "leftWire": "500 kcmil Cu", "leftTargetLoad": "CHLR-2", "leftParentSlot": 7, "leftIsGanged": True, "phase": "B", "phaseColor": "text-blue-500"},
                {"leftSlot": 11, "leftDesc": "↳ Ganged with Slot #7 (Phase C)", "leftTrip": "400", "leftPoles": 3, "leftType": "MCCB", "leftWire": "500 kcmil Cu", "leftTargetLoad": "CHLR-2", "leftParentSlot": 7, "leftIsGanged": True, "phase": "C", "phaseColor": "text-emerald-500"},
                {"leftSlot": 13, "leftDesc": "Feeder to Central UPS-1", "leftTrip": "350", "leftPoles": 3, "leftType": "MCCB", "leftWire": "350 kcmil Cu", "leftTargetLoad": "UPS-1", "leftParentSlot": None, "leftIsGanged": False, "phase": "A", "phaseColor": "text-red-500"},
                {"leftSlot": 15, "leftDesc": "↳ Ganged with Slot #13 (Phase B)", "leftTrip": "350", "leftPoles": 3, "leftType": "MCCB", "leftWire": "350 kcmil Cu", "leftTargetLoad": "UPS-1", "leftParentSlot": 13, "leftIsGanged": True, "phase": "B", "phaseColor": "text-blue-500"},
                {"leftSlot": 17, "leftDesc": "↳ Ganged with Slot #13 (Phase C)", "leftTrip": "350", "leftPoles": 3, "leftType": "MCCB", "leftWire": "350 kcmil Cu", "leftTargetLoad": "UPS-1", "leftParentSlot": 13, "leftIsGanged": True, "phase": "C", "phaseColor": "text-emerald-500"},
                {"leftSlot": 19, "leftDesc": "Feeder Riser Busway BUS-480-1 (Floors 1-5)", "leftTrip": "800", "leftPoles": 3, "leftType": "MCCB", "leftWire": "800A Busduct", "leftTargetLoad": "BUS-480-1", "leftParentSlot": None, "leftIsGanged": False, "phase": "A", "phaseColor": "text-red-500"},
                {"leftSlot": 21, "leftDesc": "↳ Ganged with Slot #19 (Phase B)", "leftTrip": "800", "leftPoles": 3, "leftType": "MCCB", "leftWire": "800A Busduct", "leftTargetLoad": "BUS-480-1", "leftParentSlot": 19, "leftIsGanged": True, "phase": "B", "phaseColor": "text-blue-500"},
                {"leftSlot": 23, "leftDesc": "↳ Ganged with Slot #19 (Phase C)", "leftTrip": "800", "leftPoles": 3, "leftType": "MCCB", "leftWire": "800A Busduct", "leftTargetLoad": "BUS-480-1", "leftParentSlot": 19, "leftIsGanged": True, "phase": "C", "phaseColor": "text-emerald-500"},
                {"leftSlot": 25, "leftDesc": "Feeder to Roof Penthouse DP-ROOF", "leftTrip": "600", "leftPoles": 3, "leftType": "MCCB", "leftWire": "2x(350 kcmil) Cu", "leftTargetLoad": "DP-ROOF", "leftParentSlot": None, "leftIsGanged": False, "phase": "A", "phaseColor": "text-red-500"},
                {"leftSlot": 27, "leftDesc": "↳ Ganged with Slot #25 (Phase B)", "leftTrip": "600", "leftPoles": 3, "leftType": "MCCB", "leftWire": "2x(350 kcmil) Cu", "leftTargetLoad": "DP-ROOF", "leftParentSlot": 25, "leftIsGanged": True, "phase": "B", "phaseColor": "text-blue-500"},
                {"leftSlot": 29, "leftDesc": "↳ Ganged with Slot #25 (Phase C)", "leftTrip": "600", "leftPoles": 3, "leftType": "MCCB", "leftWire": "2x(350 kcmil) Cu", "leftTargetLoad": "DP-ROOF", "leftParentSlot": 25, "leftIsGanged": True, "phase": "C", "phaseColor": "text-emerald-500"},
                {"leftSlot": 31, "leftDesc": "Feeder to Basement XFMR T-B1", "leftTrip": "70", "leftPoles": 3, "leftType": "MCCB", "leftWire": "4 AWG Cu", "leftTargetLoad": "T-B1", "leftParentSlot": None, "leftIsGanged": False, "phase": "A", "phaseColor": "text-red-500"},
                {"leftSlot": 33, "leftDesc": "↳ Ganged with Slot #31 (Phase B)", "leftTrip": "70", "leftPoles": 3, "leftType": "MCCB", "leftWire": "4 AWG Cu", "leftTargetLoad": "T-B1", "leftParentSlot": 31, "leftIsGanged": True, "phase": "B", "phaseColor": "text-blue-500"},
                {"leftSlot": 35, "leftDesc": "↳ Ganged with Slot #31 (Phase C)", "leftTrip": "70", "leftPoles": 3, "leftType": "MCCB", "leftWire": "4 AWG Cu", "leftTargetLoad": "T-B1", "leftParentSlot": 31, "leftIsGanged": True, "phase": "C", "phaseColor": "text-emerald-500"}
            ]
        }
    )
    add_edge("ATS-1", "MSB-1")

    # Central Chillers
    add_node("CHLR-1", "Central Plant Water-Cooled Chiller #1 (300 Ton)", "ElectricMotorObject", "loads", "MTR", "Centrifugal Chiller Compressor", "Basement - Mechanical Room B102", fed_from="MSB-1", voltage="480V 3Ø", amps=320.0, aic=65.0)
    add_node("CHLR-2", "Central Plant Water-Cooled Chiller #2 (300 Ton)", "ElectricMotorObject", "loads", "MTR", "Centrifugal Chiller Compressor", "Basement - Mechanical Room B102", fed_from="MSB-1", voltage="480V 3Ø", amps=320.0, aic=65.0)
    add_edge("MSB-1", "CHLR-1")
    add_edge("MSB-1", "CHLR-2")

    # Fire Pump
    add_node("FP-1", "100 HP Electric Fire Pump (NFPA 20)", "ElectricMotorObject", "loads", "MTR", "Electric Fire Pump", "Basement - Fire Pump Room B104", fed_from="UTIL-1", voltage="480V 3Ø", amps=124.0, aic=100.0)
    add_edge("UTIL-1", "FP-1")

    # Central UPS
    add_node(
        tag="UPS-1",
        name="250 kVA Online Double-Conversion Static UPS",
        object_class="UpsObject",
        domain="power_quality",
        type_tag="UPS",
        type_name="Double-Conversion Static UPS",
        room="Basement - UPS / Battery Room B103",
        fed_from="MSB-1",
        voltage="480V : 480V 3Ø 4W",
        amps=300.0,
        aic=65.0,
        attributes={"kva": 250.0, "efficiency_pct": 96.5, "battery_runtime_min": 30.0, "battery_type": "VRLA 12V High-Rate"}
    )
    add_edge("MSB-1", "UPS-1")

    add_node(
        tag="BESS-1",
        name="UPS VRLA Battery String (480VDC)",
        object_class="BatteryEnergyStorageObject",
        domain="sources",
        type_tag="BESS",
        type_name="Battery Energy Storage System (BESS)",
        room="Basement - UPS / Battery Room B103",
        fed_from="UPS-1",
        voltage="480V DC",
        amps=400.0,
        aic=25.0
    )
    add_edge("UPS-1", "BESS-1")

    # Basement Transformer & Panel
    add_node("T-B1", "45 kVA Basement Step-Down Transformer", "DryTypeStepDownTransformerObject", "transformers", "XFMR", "Dry-Type Step-Down Transformer", "Basement - Main Electrical Room B101", fed_from="MSB-1", voltage="480V : 208Y/120V 3Ø 4W", amps=125.0, aic=22.0, attributes={"kva": 45.0, "impedance_z": 4.5})
    add_edge("MSB-1", "T-B1")

    add_node("LP-B1", "Basement Mechanical & Workshop Lighting/Plugs", "LightingBranchPanelObject", "panels", "LP", "Lighting & Appliance Branch Panel", "Basement - Workshop B105", fed_from="T-B1", voltage="208Y/120V 3Ø 4W", amps=150.0, aic=22.0, is_panel=1, slots=42)
    add_edge("T-B1", "LP-B1")

    # Vertical Busway Riser
    add_node("BUS-480-1", "800A Vertical Feeder Busduct Riser", "BuswayObject", "cables", "BUS", "Feeder Busway (Floors 1-5)", "Shaft - Electrical Riser Closet", fed_from="MSB-1", voltage="480Y/277V 3Ø 4W", amps=800.0, aic=65.0)
    add_edge("MSB-1", "BUS-480-1")

    # =========================================================================
    # 2. FLOORS 1 TO 5 GENERATION LOOP
    # =========================================================================
    floor_configs = [
        {
            "floor": 1,
            "name_prefix": "Floor 1 (Lobby, Cafeteria & Conference)",
            "kva": 112.5,
            "lp_name": "LP-1A (Lobby Lighting & Public Zones)",
            "pp_name": "PP-1A (Commercial Cafeteria & Kitchen)",
            "rp_name": "RP-1B (Conference Center Floor Boxes & Reception)",
            "cp_name": "CP-1 (Telecom 105 & Security Access)",
            "rooms": [
                {"no": "101", "name": "Main Building Lobby & Atrium", "lights": "Lobby Architectural LED Troffers & Coves", "plugs": "Lobby Wall Plugs & Digital Directory Display"},
                {"no": "102", "name": "Security Command & Badge Desk", "lights": "Security Desk Task Lighting", "plugs": "Security Console Dual Monitors & CCTV Wall"},
                {"no": "103", "name": "Cafeteria Commercial Kitchen", "lights": "Vapor-Tight Kitchen Lighting", "plugs": "Walk-in Cooler / Reach-in Refrigeration (20A GFCI)"},
                {"no": "104", "name": "Cafeteria Dining Hall", "lights": "Pendant Downlights Zone A/B", "plugs": "Cafeteria Perimeter Cleaning Outlets"},
                {"no": "105", "name": "Main Conference Center Room A", "lights": "Dimmable 0-10V Conference Lighting", "plugs": "Table AV Pop-up Floor Boxes & Video Wall"},
                {"no": "106", "name": "Main Conference Center Room B", "lights": "Conference Room B Recessed LEDs", "plugs": "Presentation Podium & Microphones"},
                {"no": "107", "name": "Restroom Core 1st Floor", "lights": "Occupancy Sensor Restroom Lighting", "plugs": "Restroom Hand Dryers & GFCI Vanity Plugs"},
                {"no": "108", "name": "Building Management Office 108", "lights": "Office 108 LED Troffers", "plugs": "Facilities Desk Computer & Printer"}
            ]
        },
        {
            "floor": 2,
            "name_prefix": "Floor 2 (Operations & Accounting)",
            "kva": 75.0,
            "lp_name": "LP-2A (Office Lighting & Hallways)",
            "pp_name": "PP-2A (HVAC VAV Boxes & Utility)",
            "rp_name": "RP-2A (Workstation Plugs & Breakroom)",
            "cp_name": "CP-2 (IDF 208 Telecom Rack)",
            "rooms": [
                {"no": "201", "name": "Accounting Executive Office 201", "lights": "Office 201 Dimmable LED Troffers", "plugs": "Office 201 Desk Dual Monitor & Credenza Plugs"},
                {"no": "202", "name": "Operations Manager Office 202", "lights": "Office 202 LED Troffers", "plugs": "Office 202 Workstation & Shredder Receptacles"},
                {"no": "203", "name": "HR Department Suite 203", "lights": "HR Office Lighting Grid", "plugs": "HR Desk Perimeter Wall Outlets"},
                {"no": "204", "name": "Floor 2 Employee Breakroom", "lights": "Breakroom Recessed Downlights", "plugs": "Microwave & Coffee Maker Dedicated 20A GFCI"},
                {"no": "205", "name": "North Open Bullpen Cubicles", "lights": "Open Bullpen Continuous Linear Fixtures", "plugs": "Cubicle Power Poles Quads 1-6 (12 Desks)"},
                {"no": "206", "name": "South Open Bullpen Cubicles", "lights": "South Bullpen Ambient Lighting", "plugs": "Cubicle Power Poles Quads 7-12 (12 Desks)"},
                {"no": "207", "name": "Copy / Print / Mail Hub 207", "lights": "Copy Center Overhead Task Lighting", "plugs": "Heavy Duty Multifunction Copier Dedicated Circuit"},
                {"no": "208", "name": "Medium Team Conference Room 208", "lights": "Conference 208 Dimmable LED System", "plugs": "AV Conference Table Box & Display Screen"}
            ]
        },
        {
            "floor": 3,
            "name_prefix": "Floor 3 (Engineering & Prototyping Labs)",
            "kva": 112.5,
            "lp_name": "LP-3A (Engineering Lighting)",
            "pp_name": "PP-3A (Lab Equipment & 3D Printers)",
            "rp_name": "RP-3A (Engineering Desks & Clean Benches)",
            "cp_name": "CP-3 (IDF 305 Telecom)",
            "rooms": [
                {"no": "301", "name": "Hardware Engineering Lab 301", "lights": "High-CRI Lab Bench Overhead Illumination", "plugs": "Isolated Ground (IG) Test Bench Outlets (Oscilloscopes)"},
                {"no": "302", "name": "Rapid Prototyping & 3D Print Lab 302", "lights": "Lab 302 Lighting", "plugs": "3D Printer Array & Fume Hood (Dedicated 20A)"},
                {"no": "303", "name": "Firmware Development Bullpen 303", "lights": "Firmware Zone Glare-Free LED Panels", "plugs": "Developer Triple Monitor Workstations 1-8"},
                {"no": "304", "name": "QA Software Test Suite 304", "lights": "QA Testing Area Lighting", "plugs": "Test Rig Power Strips & Rack Shelves"},
                {"no": "305", "name": "Collaborative Huddle Room 305", "lights": "Huddle 305 Warm LED Downlights", "plugs": "Whiteboard Screen & Collaboration Table Plugs"},
                {"no": "306", "name": "Engineering Director Office 306", "lights": "Office 306 Recessed Lighting", "plugs": "Executive Desk & Laptop Docking Plugs"},
                {"no": "307", "name": "Floor 3 Kitchenette & Coffee Bar", "lights": "Kitchenette Task Lighting", "plugs": "Countertop GFCI Receptacles & Espresso Machine"},
                {"no": "308", "name": "Component Parts Stockroom 308", "lights": "Stockroom Motion-Activated LEDs", "plugs": "Barcode Scanner & Inventory Terminal Outlets"}
            ]
        },
        {
            "floor": 4,
            "name_prefix": "Floor 4 (Main Data Center / MDF & Cloud Ops)",
            "kva": 150.0,
            "lp_name": "LP-4A (Floor 4 Perimeter Lighting)",
            "pp_name": "DP-4 (In-Row CRAC Cooling Units 480V)",
            "rp_name": "RP-4A (Cloud Ops Center & Breakroom)",
            "cp_name": "PDU-4 (Data Center Server Racks A1-B8)",
            "rooms": [
                {"no": "401", "name": "Main Data Center / MDF Room 401", "lights": "Data Center High-Efficiency White LEDs", "plugs": "Server Rack PDU A-Feed (Racks A1-A4)"},
                {"no": "402", "name": "Server Hall Hot-Aisle Containment", "lights": "Aisle Waypoint Illumination", "plugs": "Server Rack PDU B-Feed (Racks B1-B4)"},
                {"no": "403", "name": "Network Operations Center (NOC) 403", "lights": "NOC Video Wall Ambient Backlights", "plugs": "NOC 24/7 Operator Consoles & Display Wall"},
                {"no": "404", "name": "Cloud Systems Architect Office 404", "lights": "Office 404 Recessed Panels", "plugs": "Architect Workstation & Whiteboard Display"},
                {"no": "405", "name": "Cybersecurity War Room 405", "lights": "War Room Dimmable Lighting", "plugs": "Secure Audio-Visual Conferencing Table Outlets"},
                {"no": "406", "name": "Floor 4 Data Center Breakroom 406", "lights": "Breakroom Lighting", "plugs": "Refrigerator & Dual Microwave GFCI Circuits"},
                {"no": "407", "name": "Telecom Carrier Demarcation Room", "lights": "Demarc Room Utility Strip", "plugs": "Fiber Optic Patch Panel & Telco Gateway Plugs"}
            ]
        },
        {
            "floor": 5,
            "name_prefix": "Floor 5 (Executive Suite & Boardroom)",
            "kva": 75.0,
            "lp_name": "LP-5A (Executive Architectural Lighting)",
            "pp_name": "PP-5A (Executive Lounge Kitchenette)",
            "rp_name": "RP-5A (Boardroom Table & Executive Plugs)",
            "cp_name": "CP-5 (IDF 504 Telecom & Comms)",
            "rooms": [
                {"no": "501", "name": "Executive Boardroom 501", "lights": "Lutron Architectural Dimming & Chandelier Coves", "plugs": "Custom Hardwood Boardroom Table Retractable AV Plugs"},
                {"no": "502", "name": "CEO Executive Suite 502", "lights": "CEO Office Architectural Recessed Downlights", "plugs": "Executive Desk, Credenza & Private Sitting Area Outlets"},
                {"no": "503", "name": "COO Executive Suite 503", "lights": "COO Office Dimmable LED System", "plugs": "COO Workstation & Conference Side Table Plugs"},
                {"no": "504", "name": "CFO & Legal Suite 504", "lights": "Legal Suite Glare-Free LED Panels", "plugs": "CFO Desk & Document Vault Power Circuits"},
                {"no": "505", "name": "Executive Lounge & Wet Bar 505", "lights": "Under-Cabinet & Accent LED Strips", "plugs": "Wine Cooler, Dishwasher & Espresso Bar GFCI"},
                {"no": "506", "name": "Boardroom Ante-Room & Cloakroom 506", "lights": "Ante-Room Ambient LEDs", "plugs": "Wall Receptacles & Coat Storage Power"},
                {"no": "507", "name": "Executive Restroom Suite 507", "lights": "Vanity Sconce & Ceiling Downlights", "plugs": "Vanity GFCI & Heated Towel Rack Circuit"}
            ]
        }
    ]

    for fc in floor_configs:
        fl = fc["floor"]
        ec_room = f"Level {fl} - Electrical Closet EC-{fl}"
        
        # 1. Floor Step-Down Transformer
        xfmr_tag = f"T-{fl}"
        add_node(
            tag=xfmr_tag,
            name=f"{fc['kva']} kVA Floor {fl} Step-Down Transformer",
            object_class="DryTypeStepDownTransformerObject",
            domain="transformers",
            type_tag="XFMR",
            type_name="Dry-Type Step-Down Transformer",
            room=ec_room,
            fed_from="BUS-480-1",
            voltage="480V : 208Y/120V 3Ø 4W",
            amps=round((fc["kva"] * 1000) / (1.732 * 208), 1),
            aic=22.0,
            attributes={"kva": fc["kva"], "impedance_z": 4.8, "winding": "Copper", "temp_rise_c": 115.0}
        )
        add_edge("BUS-480-1", xfmr_tag)

        # 2. Floor Lighting Panel (LP-x)
        lp_tag = f"LP-{fl}A"
        lp_sched = []
        # 3. Floor Receptacle Panel (RP-x)
        rp_tag = f"RP-{fl}A"
        rp_sched = []

        slot_idx = 1
        for rm in fc["rooms"]:
            rm_no = rm["no"]
            
            # --- Lighting circuit on LP-xA ---
            light_tag = f"LTG-{rm_no}"
            add_node(
                tag=light_tag,
                name=f"Room {rm_no} ({rm['name']}) - {rm['lights']}",
                object_class="LumpedLoadObject",
                domain="loads",
                type_tag="LOAD",
                type_name="Branch Lighting Zone",
                room=f"Level {fl} - Room {rm_no} ({rm['name']})",
                fed_from=lp_tag,
                voltage="120V 1Ø",
                amps=12.0,
                aic=10.0,
                attributes={"load_type": "LIGHTING", "continuous": True, "kw": 1.44}
            )
            add_edge(lp_tag, light_tag)

            if slot_idx <= 41:
                phase_char = "A" if (slot_idx % 6 in (1, 2)) else ("B" if (slot_idx % 6 in (3, 4)) else "C")
                phase_color = "text-red-500" if phase_char == "A" else ("text-blue-500" if phase_char == "B" else "text-emerald-500")
                lp_sched.append({
                    "leftSlot": slot_idx,
                    "leftDesc": f"Room {rm_no} ({rm['name'][:20]}) Lighting",
                    "leftTrip": "20",
                    "leftPoles": 1,
                    "leftType": "MCCB",
                    "leftWire": "12 AWG Cu",
                    "leftTargetLoad": light_tag,
                    "leftParentSlot": None,
                    "leftIsGanged": False,
                    "phase": phase_char,
                    "phaseColor": phase_color
                })

            # --- Receptacle plug circuit on RP-xA ---
            plug_tag = f"REC-{rm_no}"
            add_node(
                tag=plug_tag,
                name=f"Room {rm_no} ({rm['name']}) - {rm['plugs']}",
                object_class="LumpedLoadObject",
                domain="loads",
                type_tag="LOAD",
                type_name="Branch Receptacle Circuit",
                room=f"Level {fl} - Room {rm_no} ({rm['name']})",
                fed_from=rp_tag,
                voltage="120V 1Ø",
                amps=16.0,
                aic=10.0,
                attributes={"load_type": "RECEPTACLE", "continuous": False, "kw": 1.92}
            )
            add_edge(rp_tag, plug_tag)

            if slot_idx <= 41:
                phase_char = "A" if (slot_idx % 6 in (1, 2)) else ("B" if (slot_idx % 6 in (3, 4)) else "C")
                phase_color = "text-red-500" if phase_char == "A" else ("text-blue-500" if phase_char == "B" else "text-emerald-500")
                rp_sched.append({
                    "leftSlot": slot_idx,
                    "leftDesc": f"Room {rm_no} Plugs ({rm['plugs'][:25]})",
                    "leftTrip": "20",
                    "leftPoles": 1,
                    "leftType": "MCCB",
                    "leftWire": "12 AWG Cu",
                    "leftTargetLoad": plug_tag,
                    "leftParentSlot": None,
                    "leftIsGanged": False,
                    "phase": phase_char,
                    "phaseColor": phase_color
                })

            slot_idx += 2

        # Add Lighting Panel Node with Schedule
        add_node(
            tag=lp_tag,
            name=f"Floor {fl} Lighting Panel ({fc['lp_name']})",
            object_class="LightingBranchPanelObject",
            domain="panels",
            type_tag="LP",
            type_name="Lighting & Appliance Branch Panel",
            room=ec_room,
            fed_from=xfmr_tag,
            voltage="208Y/120V 3Ø 4W",
            amps=225.0,
            aic=22.0,
            is_panel=1,
            slots=42,
            attributes={"bus_rating_a": 225.0, "main_device": "MLO", "main_type": "MLO (Main Lugs)", "schedule": lp_sched}
        )
        add_edge(xfmr_tag, lp_tag)

        # Add Receptacle Panel Node with Schedule
        add_node(
            tag=rp_tag,
            name=f"Floor {fl} Receptacle & Power Panel ({fc['rp_name']})",
            object_class="LightingBranchPanelObject",
            domain="panels",
            type_tag="RP",
            type_name="Lighting & Appliance Branch Panel",
            room=ec_room,
            fed_from=xfmr_tag,
            voltage="208Y/120V 3Ø 4W",
            amps=225.0,
            aic=22.0,
            is_panel=1,
            slots=42,
            attributes={"bus_rating_a": 225.0, "main_device": "MLO", "main_type": "MLO (Main Lugs)", "schedule": rp_sched}
        )
        add_edge(xfmr_tag, rp_tag)

        # Clean IT / UPS-backed Panel
        cp_tag = f"CP-{fl}"
        add_node(
            tag=cp_tag,
            name=f"Floor {fl} Clean IT / Server Rack Panel ({fc['cp_name']})",
            object_class="LightingBranchPanelObject",
            domain="panels",
            type_tag="CP",
            type_name="Critical Power IT Panel",
            room=ec_room,
            fed_from="UPS-1",
            voltage="208Y/120V 3Ø 4W",
            amps=100.0,
            aic=22.0,
            is_panel=1,
            slots=42,
            attributes={"bus_rating_a": 100.0, "main_device": "MCB", "main_type": "MCB (Main Breaker)"}
        )
        add_edge("UPS-1", cp_tag)

    # =========================================================================
    # 3. ROOFTOP PENTHOUSE & HEAVY HVAC / ELEVATORS
    # =========================================================================
    add_node(
        tag="DP-ROOF",
        name="Rooftop Mechanical Distribution Panel",
        object_class="MainDistributionPanelObject",
        domain="panels",
        type_tag="DP",
        type_name="Distribution Panelboard",
        room="Roof - Penthouse Mechanical Room R01",
        fed_from="MSB-1",
        voltage="480Y/277V 3Ø 4W",
        amps=600.0,
        aic=65.0,
        is_panel=1,
        slots=42,
        attributes={"bus_rating_a": 600.0, "main_device": "MCB"}
    )
    add_edge("MSB-1", "DP-ROOF")

    # 5 Rooftop AHUs (Air Handling Units with VFDs)
    for fl in range(1, 6):
        ahu_tag = f"AHU-{fl}"
        add_node(
            tag=ahu_tag,
            name=f"Floor {fl} Rooftop Air Handling Unit (50 HP VFD)",
            object_class="HvacEquipmentObject",
            domain="loads",
            type_tag="HVAC",
            type_name="Packaged Rooftop AHU with VFD",
            room="Roof - Equipment Curbs",
            fed_from="DP-ROOF",
            voltage="480V 3Ø",
            amps=65.0,
            aic=65.0,
            attributes={"mca": 65.0, "mocp": 90.0, "cfm": 18500, "compressor_hp": 50.0}
        )
        add_edge("DP-ROOF", ahu_tag)

    # Traction Elevators
    add_node("ELEV-1", "Passenger Traction Elevator #1 (75 HP)", "ElectricMotorObject", "loads", "MTR", "Regenerative Gearless Traction Elevator", "Roof - Elevator Machine Room R02", fed_from="DP-ROOF", voltage="480V 3Ø", amps=96.0, aic=65.0)
    add_node("ELEV-2", "Passenger Traction Elevator #2 (75 HP)", "ElectricMotorObject", "loads", "MTR", "Regenerative Gearless Traction Elevator", "Roof - Elevator Machine Room R02", fed_from="DP-ROOF", voltage="480V 3Ø", amps=96.0, aic=65.0)
    add_edge("DP-ROOF", "ELEV-1")
    add_edge("DP-ROOF", "ELEV-2")

    # =========================================================================
    # INSERT ALL RECORDS INTO SQLITE
    # =========================================================================
    print(f"[*] Writing {len(nodes)} Equipment Nodes to SQLite...")
    for n in nodes:
        session.add(NodeRecord(
            id=n["id"],
            tag=n["tag"],
            name=n["name"],
            object_class=n["object_class"],
            domain=n["domain"],
            type_tag=n["type_tag"],
            type_name=n["type_name"],
            room=n["room"],
            fed_from=n["fed_from"],
            voltage=n["voltage"],
            amps=n["amps"],
            aic=n["aic"],
            is_panel=n["is_panel"],
            slots=n["slots"],
            survey_sequence=n["survey_sequence"],
            status=n["status"],
            attributes=n["attributes"]
        ))

    print(f"[*] Writing {len(edges)} Electrical Conductor Edges to SQLite...")
    for e in edges:
        session.add(EdgeRecord(
            id=e["id"],
            from_node_tag=e["from_node_tag"],
            from_port=e["from_port"],
            to_node_tag=e["to_node_tag"],
            to_port=e["to_port"],
            conductor_spec=e["conductor_spec"]
        ))

    session.commit()
    session.close()

    # Export companion JSONL
    jsonl_file = export_to_jsonl(client_id, facility_id)
    print(f"[+] Successfully generated {db_path} and {jsonl_file}!")
    print(f"[+] Total Equipment Nodes: {len(nodes)}")
    print(f"[+] Total Electrical Connections: {len(edges)}")


if __name__ == "__main__":
    generate_large_demo_building()
