"""
Script to generate a comprehensive, highly realistic Tesla Gigafactory Digital Twin
(Substation, Megapack BESS, Solar Rooftop, Giga Press, 4680 Cells, Paint, Body, Robotics, Superchargers)
for client 'jemby', facility 'tesla_gigafactory'.
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


def generate_tesla_gigafactory():
    client_id = "jemby"
    facility_id = "tesla_gigafactory"
    facility_dir = get_facility_dir(client_id, facility_id)
    facility_dir.mkdir(parents=True, exist_ok=True)

    print(f"[*] Initializing Tesla Gigafactory for {client_id} / {facility_id} at {facility_dir}...")

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
        amps: float = 400.0,
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
    # 1. 138kV UTILITY TRANSMISSION INTERCONNECT & MAIN SUBSTATION
    # =========================================================================
    add_node(
        tag="UTIL-138KV-1",
        name="Austin Energy 138kV Grid Interconnect #1 (North Feeder)",
        object_class="UtilityServiceSource",
        domain="sources",
        type_tag="UTIL",
        type_name="High-Voltage Transmission Grid Interconnect",
        room="Outdoor Yard - High Voltage Substation Yard West",
        fed_from=None,
        voltage="138,000V 3Ø 3W",
        amps=1200.0,
        aic=40.0,
        attributes={
            "utility_provider": "Austin Energy / ERCOT",
            "interconnect_kv": 138.0,
            "short_circuit_mva": 3500.0,
            "substation_bay": "Bay 1 North Line",
            "meter_number": "AE-TX-GIGA-01"
        }
    )

    add_node(
        tag="UTIL-138KV-2",
        name="Austin Energy 138kV Grid Interconnect #2 (South Feeder)",
        object_class="UtilityServiceSource",
        domain="sources",
        type_tag="UTIL",
        type_name="High-Voltage Transmission Grid Interconnect",
        room="Outdoor Yard - High Voltage Substation Yard West",
        fed_from=None,
        voltage="138,000V 3Ø 3W",
        amps=1200.0,
        aic=40.0,
        attributes={
            "utility_provider": "Austin Energy / ERCOT",
            "interconnect_kv": 138.0,
            "short_circuit_mva": 3500.0,
            "substation_bay": "Bay 2 South Line",
            "meter_number": "AE-TX-GIGA-02"
        }
    )

    add_node(
        tag="XFMR-SUB-1",
        name="50 MVA Main Substation Transformer #1 (138kV / 13.8kV)",
        object_class="StepDownTransformerObject",
        domain="transformers",
        type_tag="XFMR",
        type_name="Substation Liquid-Filled Power Transformer",
        room="Outdoor Yard - Substation Transformer Bay #1",
        fed_from="UTIL-138KV-1",
        voltage="138kV : 13.8kV 3Ø 3W",
        amps=2092.0,
        aic=50.0,
        attributes={
            "mva": 50.0,
            "cooling_class": "ONAN / ONAF / ODAF",
            "impedance_pct": 8.5,
            "oil_type": "FR3 Natural Ester Dielectric Fluid",
            "temp_rise_c": 65.0
        }
    )
    add_edge("UTIL-138KV-1", "XFMR-SUB-1", spec={"type": "ACSR_BIRD", "conduit": "Overhead Bus"})

    add_node(
        tag="XFMR-SUB-2",
        name="50 MVA Main Substation Transformer #2 (138kV / 13.8kV)",
        object_class="StepDownTransformerObject",
        domain="transformers",
        type_tag="XFMR",
        type_name="Substation Liquid-Filled Power Transformer",
        room="Outdoor Yard - Substation Transformer Bay #2",
        fed_from="UTIL-138KV-2",
        voltage="138kV : 13.8kV 3Ø 3W",
        amps=2092.0,
        aic=50.0,
        attributes={
            "mva": 50.0,
            "cooling_class": "ONAN / ONAF / ODAF",
            "impedance_pct": 8.5,
            "oil_type": "FR3 Natural Ester Dielectric Fluid",
            "temp_rise_c": 65.0
        }
    )
    add_edge("UTIL-138KV-2", "XFMR-SUB-2", spec={"type": "ACSR_BIRD", "conduit": "Overhead Bus"})

    # =========================================================================
    # 2. 13.8kV MEDIUM VOLTAGE SWITCHGEAR & RENEWABLE MICROGRID
    # =========================================================================
    add_node(
        tag="SWGR-13KV-MAIN",
        name="13.8kV Medium Voltage Switchgear (Main-Tie-Main)",
        object_class="MediumVoltageSwitchgearObject",
        domain="switches",
        type_tag="SWGR",
        type_name="15kV Metal-Clad Arc-Resistant Switchgear",
        room="Building 1 - Main Substation Control House",
        fed_from="XFMR-SUB-1",
        voltage="13,800V 3Ø 3W",
        amps=3000.0,
        aic=50.0,
        is_panel=1,
        slots=12,
        attributes={
            "breakers": "Vacuum Circuit Breakers (VCB)",
            "bus_rating_a": 3000.0,
            "arc_flash_rating": "Type 2B Arc-Resistant",
            "scada_protocol": "IEC 61850 / DNP3"
        }
    )
    add_edge("XFMR-SUB-1", "SWGR-13KV-MAIN", spec={"type": "MV-105_CU_SHIELDED", "conduit": "Underground Ductbank"})

    # Tesla Megapack 2XL Utility-Scale Energy Storage Lineup
    add_node(
        tag="MEGAPACK-1",
        name="Tesla Megapack 2XL BESS Array (40 MWh / 10 MW)",
        object_class="BatteryEnergyStorageObject",
        domain="sources",
        type_tag="BESS",
        type_name="Grid-Scale Lithium Iron Phosphate (LFP) BESS",
        room="Outdoor Yard - Energy Storage Pad East",
        fed_from="SWGR-13KV-MAIN",
        voltage="13,800V 3Ø",
        amps=418.0,
        aic=50.0,
        attributes={
            "energy_capacity_mwh": 40.0,
            "power_mw": 10.0,
            "chemistry": "Lithium Iron Phosphate (LFP)",
            "thermal_management": "Liquid Cooled with Built-In Heat Pump",
            "inverter_topology": "Bidirectional 4-Quadrant Smart Inverter",
            "response_time_ms": 20.0
        }
    )
    add_edge("SWGR-13KV-MAIN", "MEGAPACK-1", spec={"type": "MV-105_CU_SHIELDED", "conduit": "Trench"})

    # Massive Rooftop Solar PV Generation Array
    add_node(
        tag="SOLAR-ROOF-1",
        name="15 MW Rooftop Solar Photovoltaic Generation Array",
        object_class="SolarPhotovoltaicObject",
        domain="sources",
        type_tag="SOLAR",
        type_name="Commercial High-Efficiency PV Microgrid Array",
        room="Building 1 - Main Factory Rooftop Structure",
        fed_from="SWGR-13KV-MAIN",
        voltage="13,800V 3Ø",
        amps=627.0,
        aic=50.0,
        attributes={
            "peak_kw": 15000.0,
            "module_count": 32600,
            "inverters": "Utility-Scale Central Inverter Stations (13.8kV Step-Up)",
            "annual_mwh_est": 24500.0
        }
    )
    add_edge("SWGR-13KV-MAIN", "SOLAR-ROOF-1", spec={"type": "MV-105_CU_SHIELDED", "conduit": "Cable Tray"})

    # Emergency Standby Generator Lineup
    add_node(
        tag="GEN-STANDBY-1",
        name="2500 kW Standby Diesel Generator Set (Life Safety & Critical Process)",
        object_class="DieselGeneratorObject",
        domain="sources",
        type_tag="GEN",
        type_name="Emergency Medium-Voltage Diesel Generator",
        room="Outdoor Yard - Emergency Generator Enclosure",
        fed_from=None,
        voltage="13,800V 3Ø",
        amps=104.0,
        aic=35.0,
        attributes={
            "kw": 2500.0,
            "fuel_tank_gal": 5000,
            "runtime_full_load_hrs": 36.0,
            "tier_rating": "EPA Tier 4 Final"
        }
    )

    add_node(
        tag="ATS-EMERG-1",
        name="13.8kV Medium Voltage Automatic Transfer Switch",
        object_class="AutomaticTransferSwitchObject",
        domain="switches",
        type_tag="ATS",
        type_name="15kV Metal-Enclosed Automatic Transfer Switch",
        room="Building 1 - Main Substation Control House",
        fed_from="SWGR-13KV-MAIN",
        voltage="13,800V 3Ø",
        amps=600.0,
        aic=50.0,
        attributes={
            "poles": 3,
            "transition": "Closed Transition Soft-Load",
            "normal_source": "SWGR-13KV-MAIN",
            "emergency_source": "GEN-STANDBY-1"
        }
    )
    add_edge("SWGR-13KV-MAIN", "ATS-EMERG-1")
    add_edge("GEN-STANDBY-1", "ATS-EMERG-1")

    # =========================================================================
    # 3. GIGA PRESS & HIGH-PRESSURE DIE CASTING AREA
    # =========================================================================
    add_node(
        tag="XFMR-CAST-1",
        name="5000 kVA Casting Unit Substation Transformer (13.8kV / 480V)",
        object_class="StepDownTransformerObject",
        domain="transformers",
        type_tag="XFMR",
        type_name="Cast Resin Dry-Type Unit Substation Transformer",
        room="Building 1 - Casting Mezzanine Vault",
        fed_from="SWGR-13KV-MAIN",
        voltage="13.8kV : 480Y/277V 3Ø 4W",
        amps=6014.0,
        aic=65.0,
        attributes={"kva": 5000.0, "impedance_pct": 5.75, "fan_cooling": "FA 6666kVA"}
    )
    add_edge("SWGR-13KV-MAIN", "XFMR-CAST-1", spec={"type": "MV-105_CU_SHIELDED", "conduit": "Cable Tray"})

    add_node(
        tag="SWGR-CAST-480V",
        name="6000A Giga Press Main Low-Voltage Switchgear",
        object_class="LowVoltageSwitchgearObject",
        domain="panels",
        type_tag="SWGR",
        type_name="UL 1558 Low-Voltage Drawout Switchgear",
        room="Building 1 - Die Casting Electrical Room C101",
        fed_from="XFMR-CAST-1",
        voltage="480Y/277V 3Ø 4W",
        amps=6000.0,
        aic=100.0,
        is_panel=1,
        slots=8,
        attributes={"main_breaker": "6000A 100% Rated Drawout Power Breaker", "bus_material": "Silver-Plated Copper"}
    )
    add_edge("XFMR-CAST-1", "SWGR-CAST-480V", spec={"type": "BUSWAY_CU", "conduit": "Busduct Riser"})

    add_node(
        tag="PRESS-IDRA-9000T-1",
        name="Giga Press #1 (IDRA 9,000-Ton Die Cast - Rear Underbody)",
        object_class="IndustrialMachineryObject",
        domain="loads",
        type_tag="MTR",
        type_name="High-Pressure Aluminum Injection Servo Hydraulic Press",
        room="Building 1 - High Bay Casting Pit 01",
        fed_from="SWGR-CAST-480V",
        voltage="480V 3Ø",
        amps=1850.0,
        aic=100.0,
        attributes={
            "clamping_force_tons": 9000.0,
            "pump_hp": 1200.0,
            "cycle_time_sec": 90.0,
            "shot_weight_kg": 85.0
        }
    )
    add_edge("SWGR-CAST-480V", "PRESS-IDRA-9000T-1", spec={"type": "500kcmil_CU_x6", "conduit": "Rigid Galvanized"})

    add_node(
        tag="PRESS-IDRA-9000T-2",
        name="Giga Press #2 (IDRA 9,000-Ton Die Cast - Front Underbody)",
        object_class="IndustrialMachineryObject",
        domain="loads",
        type_tag="MTR",
        type_name="High-Pressure Aluminum Injection Servo Hydraulic Press",
        room="Building 1 - High Bay Casting Pit 02",
        fed_from="SWGR-CAST-480V",
        voltage="480V 3Ø",
        amps=1850.0,
        aic=100.0,
        attributes={
            "clamping_force_tons": 9000.0,
            "pump_hp": 1200.0,
            "cycle_time_sec": 90.0,
            "shot_weight_kg": 75.0
        }
    )
    add_edge("SWGR-CAST-480V", "PRESS-IDRA-9000T-2", spec={"type": "500kcmil_CU_x6", "conduit": "Rigid Galvanized"})

    add_node(
        tag="FURNACE-ALUM-1",
        name="Continuous Aluminum Melting & Dosing Induction Furnace (1500 kW)",
        object_class="IndustrialHeaterObject",
        domain="loads",
        type_tag="HTR",
        type_name="High-Frequency Induction Melting Furnace",
        room="Building 1 - Casting Raw Material Melting Yard",
        fed_from="SWGR-CAST-480V",
        voltage="480V 3Ø",
        amps=1804.0,
        aic=100.0,
        attributes={"kw": 1500.0, "melt_rate_tons_hr": 4.5, "operating_temp_c": 720.0}
    )
    add_edge("SWGR-CAST-480V", "FURNACE-ALUM-1", spec={"type": "500kcmil_CU_x6", "conduit": "Rigid Steel"})

    # =========================================================================
    # 4. 4680 BATTERY CELL MANUFACTURING & DRY ELECTRODE FACILITY
    # =========================================================================
    add_node(
        tag="XFMR-CELL-1",
        name="3500 kVA Battery Cell Unit Substation Transformer",
        object_class="StepDownTransformerObject",
        domain="transformers",
        type_tag="XFMR",
        type_name="Harmonic-Mitigating K-Factor 13 Dry Transformer",
        room="Building 2 - 4680 Cell Electrical Substation B201",
        fed_from="SWGR-13KV-MAIN",
        voltage="13.8kV : 480Y/277V 3Ø 4W",
        amps=4210.0,
        aic=65.0,
        attributes={"kva": 3500.0, "k_factor": 13, "efficiency_pct": 99.1}
    )
    add_edge("SWGR-13KV-MAIN", "XFMR-CELL-1", spec={"type": "MV-105_CU_SHIELDED", "conduit": "Cable Tray"})

    add_node(
        tag="MSB-CELL-480V",
        name="4000A 4680 Battery Manufacturing Main Switchboard",
        object_class="MainSwitchboardObject",
        domain="panels",
        type_tag="MSB",
        type_name="UL 891 Front-Connected Distribution Switchboard",
        room="Building 2 - 4680 Cell Electrical Substation B201",
        fed_from="XFMR-CELL-1",
        voltage="480Y/277V 3Ø 4W",
        amps=4000.0,
        aic=65.0,
        is_panel=1,
        slots=10,
        attributes={"bus_amps": 4000.0, "mcb": "4000A Solid State Trip"}
    )
    add_edge("XFMR-CELL-1", "MSB-CELL-480V")

    add_node(
        tag="OVEN-DRY-ELECTRODE-1",
        name="4680 Dry Battery Electrode Calender & Coating Line",
        object_class="IndustrialMachineryObject",
        domain="loads",
        type_tag="IND",
        type_name="Dry Polymer Electrode Powder Processing Line",
        room="Building 2 - Dry Room Area Cleanroom ISO 7",
        fed_from="MSB-CELL-480V",
        voltage="480V 3Ø",
        amps=750.0,
        aic=65.0,
        attributes={"throughput_ppm": 1200, "solvent_free": True, "powder_feed_kw": 450.0}
    )
    add_edge("MSB-CELL-480V", "OVEN-DRY-ELECTRODE-1")

    add_node(
        tag="CELL-WIND-CAN-1",
        name="High-Speed 4680 Tabless Winding & Can Integration Line",
        object_class="IndustrialMachineryObject",
        domain="loads",
        type_tag="IND",
        type_name="Automated High-Speed Jellyroll Winder & Laser Welder",
        room="Building 2 - Assembly Bay 04",
        fed_from="MSB-CELL-480V",
        voltage="480V 3Ø",
        amps=450.0,
        aic=65.0,
        attributes={"tabless_laser_weld_kw": 25.0, "cells_per_minute": 300}
    )
    add_edge("MSB-CELL-480V", "CELL-WIND-CAN-1")

    add_node(
        tag="FORMATION-CYCLER-1",
        name="Battery Formation, Aging & Grading Regenerative DC Cyclers",
        object_class="IndustrialMachineryObject",
        domain="loads",
        type_tag="IND",
        type_name="High-Density Bi-Directional DC Formation System",
        room="Building 2 - Formation Tower Area",
        fed_from="MSB-CELL-480V",
        voltage="480V 3Ø",
        amps=1200.0,
        aic=65.0,
        attributes={"energy_recovery_pct": 92.0, "channels": 4096, "dc_bus_v": 800.0}
    )
    add_edge("MSB-CELL-480V", "FORMATION-CYCLER-1")

    add_node(
        tag="DRY-ROOM-DEHUM-1",
        name="Ultra-Low Dewpoint Desiccant Cleanroom Dehumidifier Plant",
        object_class="HvacEquipmentObject",
        domain="loads",
        type_tag="HVAC",
        type_name="Industrial Desiccant Wheel Dehumidification System",
        room="Building 2 - Rooftop HVAC Penthouse",
        fed_from="MSB-CELL-480V",
        voltage="480V 3Ø",
        amps=680.0,
        aic=65.0,
        attributes={"dew_point_c": -45.0, "airflow_cfm": 45000, "motor_hp": 400.0}
    )
    add_edge("MSB-CELL-480V", "DRY-ROOM-DEHUM-1")

    # =========================================================================
    # 5. BODY-IN-WHITE (ROBOTICS & AUTOMATED WELDING)
    # =========================================================================
    add_node(
        tag="XFMR-BODY-1",
        name="2500 kVA Body-In-White Unit Substation Transformer",
        object_class="StepDownTransformerObject",
        domain="transformers",
        type_tag="XFMR",
        type_name="Dry-Type Step-Down Transformer",
        room="Building 3 - Body Shop Substation Mezzanine",
        fed_from="SWGR-13KV-MAIN",
        voltage="13.8kV : 480Y/277V 3Ø 4W",
        amps=3007.0,
        aic=65.0,
        attributes={"kva": 2500.0, "impedance_pct": 5.75}
    )
    add_edge("SWGR-13KV-MAIN", "XFMR-BODY-1", spec={"type": "MV-105_CU_SHIELDED", "conduit": "Cable Tray"})

    add_node(
        tag="BUS-BODY-1",
        name="3000A Overhead Feeder Busway (Body Shop Production Spine)",
        object_class="BuswayObject",
        domain="cables",
        type_tag="BUSWAY",
        type_name="High-Ampacity Sandwich Feeder Busduct Riser",
        room="Building 3 - Body Shop Production Floor Ceiling",
        fed_from="XFMR-BODY-1",
        voltage="480Y/277V 3Ø 4W",
        amps=3000.0,
        aic=65.0,
        attributes={"length_ft": 450, "housing": "Extruded Aluminum Ground Housing"}
    )
    add_edge("XFMR-BODY-1", "BUS-BODY-1")

    add_node(
        tag="PP-WELD-ROBOTS-1",
        name="Robotic Laser & Resistance Welding Distribution Panel #1",
        object_class="PowerDistributionPanelObject",
        domain="panels",
        type_tag="PP",
        type_name="Industrial Power Distribution Panelboard",
        room="Building 3 - Robotic Framing Cell Bay 12",
        fed_from="BUS-BODY-1",
        voltage="480V 3Ø 3W",
        amps=800.0,
        aic=65.0,
        is_panel=1,
        slots=12,
        attributes={"connected_robots": 36, "welding_type": "Laser Braze & Medium-Freq DC Spot"}
    )
    add_edge("BUS-BODY-1", "PP-WELD-ROBOTS-1", spec={"type": "Bus Plug Drop Cable", "conduit": "Flexible Liquidtight"})

    add_node(
        tag="PP-FRAMING-LINE-1",
        name="Automated Structural Framing & Hemming Robotic Panel #2",
        object_class="PowerDistributionPanelObject",
        domain="panels",
        type_tag="PP",
        type_name="Industrial Power Distribution Panelboard",
        room="Building 3 - Framing Line Station 08",
        fed_from="BUS-BODY-1",
        voltage="480V 3Ø 3W",
        amps=800.0,
        aic=65.0,
        is_panel=1,
        slots=12,
        attributes={"line_speed_uph": 45, "safety_interlock": "ISO 13849-1 Cat 4 Ple"}
    )
    add_edge("BUS-BODY-1", "PP-FRAMING-LINE-1", spec={"type": "Bus Plug Drop Cable", "conduit": "Flexible Liquidtight"})

    # =========================================================================
    # 6. PAINT SHOP & HIGH-GLOSS CURING
    # =========================================================================
    add_node(
        tag="XFMR-PAINT-1",
        name="2500 kVA Paint Shop Substation Transformer",
        object_class="StepDownTransformerObject",
        domain="transformers",
        type_tag="XFMR",
        type_name="Dry-Type Step-Down Transformer",
        room="Building 4 - Paint Shop Electrical Room P101",
        fed_from="SWGR-13KV-MAIN",
        voltage="13.8kV : 480Y/277V 3Ø 4W",
        amps=3007.0,
        aic=65.0,
        attributes={"kva": 2500.0, "impedance_pct": 5.75}
    )
    add_edge("SWGR-13KV-MAIN", "XFMR-PAINT-1", spec={"type": "MV-105_CU_SHIELDED", "conduit": "Cable Tray"})

    add_node(
        tag="MSB-PAINT-480V",
        name="3000A Automated Paint Line Main Switchboard",
        object_class="MainSwitchboardObject",
        domain="panels",
        type_tag="MSB",
        type_name="UL 891 Main Distribution Switchboard",
        room="Building 4 - Paint Shop Electrical Room P101",
        fed_from="XFMR-PAINT-1",
        voltage="480Y/277V 3Ø 4W",
        amps=3000.0,
        aic=65.0,
        is_panel=1,
        slots=8
    )
    add_edge("XFMR-PAINT-1", "MSB-PAINT-480V")

    add_node(
        tag="BOOTH-E-COAT-1",
        name="Cathodic Electrodeposition (E-Coat) Dip Tank & Rectifier System",
        object_class="IndustrialMachineryObject",
        domain="loads",
        type_tag="IND",
        type_name="Continuous Immersion E-Coat Dip Rectifier Plant",
        room="Building 4 - Pretreatment Area Bay 01",
        fed_from="MSB-PAINT-480V",
        voltage="480V 3Ø",
        amps=850.0,
        aic=65.0,
        attributes={"rectifier_kw": 500.0, "tank_volume_gallons": 85000}
    )
    add_edge("MSB-PAINT-480V", "BOOTH-E-COAT-1")

    add_node(
        tag="ROBOT-SPRAY-BOOTH-1",
        name="Automated Cleanroom Paint Spray Booth (Bell Applicator Robots)",
        object_class="IndustrialMachineryObject",
        domain="loads",
        type_tag="IND",
        type_name="Air-Recirculating High-Transfer Efficiency Spray Booth",
        room="Building 4 - Topcoat Cleanroom Spray Booth 02",
        fed_from="MSB-PAINT-480V",
        voltage="480V 3Ø",
        amps=620.0,
        aic=65.0,
        attributes={"robots_count": 16, "downdraft_cfm": 65000, "overspray_recovery_pct": 98.0}
    )
    add_edge("MSB-PAINT-480V", "ROBOT-SPRAY-BOOTH-1")

    add_node(
        tag="OVEN-CURING-1",
        name="Infrared & Convection Clearcoat Curing Bake Tunnel (800 kW)",
        object_class="IndustrialHeaterObject",
        domain="loads",
        type_tag="HTR",
        type_name="Multi-Zone Convection & IR Thermal Bake Oven",
        room="Building 4 - Topcoat Curing Tunnel Exit",
        fed_from="MSB-PAINT-480V",
        voltage="480V 3Ø",
        amps=962.0,
        aic=65.0,
        attributes={"temp_f": 320.0, "zones": 4, "rto_exhaust_scfm": 12000}
    )
    add_edge("MSB-PAINT-480V", "OVEN-CURING-1")

    # =========================================================================
    # 7. DRIVE UNIT / POWERTRAIN & DYNO TEST FACILITY
    # =========================================================================
    add_node(
        tag="XFMR-DRIVE-1",
        name="2000 kVA Powertrain & Inverter Substation Transformer",
        object_class="StepDownTransformerObject",
        domain="transformers",
        type_tag="XFMR",
        type_name="High-Efficiency Dry-Type Transformer",
        room="Building 5 - Drive Unit Assembly Substation D101",
        fed_from="SWGR-13KV-MAIN",
        voltage="13.8kV : 480Y/277V 3Ø 4W",
        amps=2406.0,
        aic=65.0,
        attributes={"kva": 2000.0, "impedance_pct": 5.75}
    )
    add_edge("SWGR-13KV-MAIN", "XFMR-DRIVE-1", spec={"type": "MV-105_CU_SHIELDED", "conduit": "Cable Tray"})

    add_node(
        tag="MSB-DRIVE-480V",
        name="2500A Drive Unit Production Main Switchboard",
        object_class="MainSwitchboardObject",
        domain="panels",
        type_tag="MSB",
        type_name="Distribution Switchboard",
        room="Building 5 - Drive Unit Assembly Substation D101",
        fed_from="XFMR-DRIVE-1",
        voltage="480Y/277V 3Ø 4W",
        amps=2500.0,
        aic=65.0,
        is_panel=1,
        slots=8
    )
    add_edge("XFMR-DRIVE-1", "MSB-DRIVE-480V")

    add_node(
        tag="LINE-STATOR-1",
        name="Hairpin Stator Automated Continuous Winding Line",
        object_class="IndustrialMachineryObject",
        domain="loads",
        type_tag="IND",
        type_name="Precision Servo Hairpin Motor Stator Winding & Welding",
        room="Building 5 - Stator Line Bay 03",
        fed_from="MSB-DRIVE-480V",
        voltage="480V 3Ø",
        amps=450.0,
        aic=65.0,
        attributes={"laser_welding_heads": 8, "uph": 80}
    )
    add_edge("MSB-DRIVE-480V", "LINE-STATOR-1")

    add_node(
        tag="DYNO-TEST-CELL-1",
        name="High-Speed Powertrain Regenerative Dynamometer Test Cell (350 kW)",
        object_class="IndustrialMachineryObject",
        domain="loads",
        type_tag="MTR",
        type_name="4-Quadrant High-Speed Electric Motor Dynamometer",
        room="Building 5 - End of Line Testing Chamber 01",
        fed_from="MSB-DRIVE-480V",
        voltage="480V 3Ø",
        amps=520.0,
        aic=65.0,
        attributes={"max_rpm": 22000, "regen_power_kw": 350.0, "torque_nm": 650.0}
    )
    add_edge("MSB-DRIVE-480V", "DYNO-TEST-CELL-1")

    # =========================================================================
    # 8. GENERAL ASSEMBLY (GA) & END-OF-LINE SUPERCHARGER HUB
    # =========================================================================
    add_node(
        tag="XFMR-GA-1",
        name="2500 kVA General Assembly Substation Transformer",
        object_class="StepDownTransformerObject",
        domain="transformers",
        type_tag="XFMR",
        type_name="Dry-Type Step-Down Transformer",
        room="Building 6 - General Assembly Substation G101",
        fed_from="SWGR-13KV-MAIN",
        voltage="13.8kV : 480Y/277V 3Ø 4W",
        amps=3007.0,
        aic=65.0,
        attributes={"kva": 2500.0, "impedance_pct": 5.75}
    )
    add_edge("SWGR-13KV-MAIN", "XFMR-GA-1", spec={"type": "MV-105_CU_SHIELDED", "conduit": "Cable Tray"})

    add_node(
        tag="MSB-GA-480V",
        name="3000A General Assembly & Logistics Switchboard",
        object_class="MainSwitchboardObject",
        domain="panels",
        type_tag="MSB",
        type_name="Main Distribution Switchboard",
        room="Building 6 - General Assembly Substation G101",
        fed_from="XFMR-GA-1",
        voltage="480Y/277V 3Ø 4W",
        amps=3000.0,
        aic=65.0,
        is_panel=1,
        slots=8
    )
    add_edge("XFMR-GA-1", "MSB-GA-480V")

    add_node(
        tag="CONVEYOR-GA-1",
        name="Main Skillet Carrier Assembly Conveyor & Marriage Line",
        object_class="IndustrialMachineryObject",
        domain="loads",
        type_tag="MTR",
        type_name="Variable Frequency Skillet Carrier Conveyor Drive System",
        room="Building 6 - GA Line 1 Centerline",
        fed_from="MSB-GA-480V",
        voltage="480V 3Ø",
        amps=380.0,
        aic=65.0,
        attributes={"drive_stations": 14, "vfd_model": "PowerFlex 755TS", "uph": 60}
    )
    add_edge("MSB-GA-480V", "CONVEYOR-GA-1")

    # Tesla V4 Supercharger Industrial Testing & Fleet Hub
    add_node(
        tag="SUPERCHARGER-HUB-1",
        name="Tesla V4 Supercharger Factory End-of-Line Test Skid #1 (350 kW DC)",
        object_class="ElectricVehicleChargerObject",
        domain="loads",
        type_tag="EVSE",
        type_name="Ultra-High Power DC Fast Charger Cabinet",
        room="Building 6 - End of Line Quality Roll Test Station",
        fed_from="MSB-GA-480V",
        voltage="480V 3Ø",
        amps=450.0,
        aic=65.0,
        attributes={"output_kw": 350.0, "max_voltage_vdc": 1000.0, "connector": "NACS / SAE J3400"}
    )
    add_edge("MSB-GA-480V", "SUPERCHARGER-HUB-1")

    add_node(
        tag="SUPERCHARGER-HUB-2",
        name="Tesla V4 Supercharger Fleet Depot #2 (350 kW DC Logistics)",
        object_class="ElectricVehicleChargerObject",
        domain="loads",
        type_tag="EVSE",
        type_name="Ultra-High Power DC Fast Charger Cabinet",
        room="Outdoor Yard - Logistics Outbound Transport Staging",
        fed_from="MSB-GA-480V",
        voltage="480V 3Ø",
        amps=450.0,
        aic=65.0,
        attributes={"output_kw": 350.0, "max_voltage_vdc": 1000.0, "connector": "NACS / SAE J3400"}
    )
    add_edge("MSB-GA-480V", "SUPERCHARGER-HUB-2")

    # =========================================================================
    # 9. CENTRAL UTILITY PLANT (CUP) & CORTEX DOJO SCADA DATA CENTER
    # =========================================================================
    add_node(
        tag="XFMR-CUP-1",
        name="3500 kVA Central Utility Plant Unit Substation Transformer",
        object_class="StepDownTransformerObject",
        domain="transformers",
        type_tag="XFMR",
        type_name="Dry-Type Step-Down Transformer",
        room="Building 7 - Central Utility Plant Vault",
        fed_from="SWGR-13KV-MAIN",
        voltage="13.8kV : 480Y/277V 3Ø 4W",
        amps=4210.0,
        aic=65.0,
        attributes={"kva": 3500.0, "impedance_pct": 5.75}
    )
    add_edge("SWGR-13KV-MAIN", "XFMR-CUP-1", spec={"type": "MV-105_CU_SHIELDED", "conduit": "Cable Tray"})

    add_node(
        tag="SWGR-CUP-480V",
        name="4000A Central Utility Plant Main Switchgear",
        object_class="LowVoltageSwitchgearObject",
        domain="panels",
        type_tag="SWGR",
        type_name="Low-Voltage Drawout Switchgear",
        room="Building 7 - Central Utility Plant Electrical Room U101",
        fed_from="XFMR-CUP-1",
        voltage="480Y/277V 3Ø 4W",
        amps=4000.0,
        aic=100.0,
        is_panel=1,
        slots=8
    )
    add_edge("XFMR-CUP-1", "SWGR-CUP-480V")

    add_node(
        tag="CHLR-IND-1",
        name="2,500 Ton Process Centrifugal Chiller #1 (VFD Magnetic Bearing)",
        object_class="IndustrialChillerObject",
        domain="loads",
        type_tag="HVAC",
        type_name="High-Efficiency Water-Cooled Centrifugal Process Chiller",
        room="Building 7 - CUP Chiller Floor",
        fed_from="SWGR-CUP-480V",
        voltage="480V 3Ø",
        amps=1680.0,
        aic=100.0,
        attributes={"tonnage": 2500.0, "cop": 6.8, "refrigerant": "R-1233zd(E)"}
    )
    add_edge("SWGR-CUP-480V", "CHLR-IND-1", spec={"type": "500kcmil_CU_x5", "conduit": "Rigid Galvanized"})

    add_node(
        tag="CHLR-IND-2",
        name="2,500 Ton Process Centrifugal Chiller #2 (VFD Magnetic Bearing)",
        object_class="IndustrialChillerObject",
        domain="loads",
        type_tag="HVAC",
        type_name="High-Efficiency Water-Cooled Centrifugal Process Chiller",
        room="Building 7 - CUP Chiller Floor",
        fed_from="SWGR-CUP-480V",
        voltage="480V 3Ø",
        amps=1680.0,
        aic=100.0,
        attributes={"tonnage": 2500.0, "cop": 6.8, "refrigerant": "R-1233zd(E)"}
    )
    add_edge("SWGR-CUP-480V", "CHLR-IND-2", spec={"type": "500kcmil_CU_x5", "conduit": "Rigid Galvanized"})

    add_node(
        tag="COMP-AIR-1",
        name="Oil-Free Rotary Screw Air Compressor #1 (350 HP / 1650 CFM)",
        object_class="AirCompressorObject",
        domain="loads",
        type_tag="MTR",
        type_name="Two-Stage Oil-Free Rotary Screw Process Compressor",
        room="Building 7 - Pneumatics Compressor Hall",
        fed_from="SWGR-CUP-480V",
        voltage="480V 3Ø",
        amps=410.0,
        aic=100.0,
        attributes={"hp": 350.0, "cfm": 1650.0, "pressure_psi": 125.0}
    )
    add_edge("SWGR-CUP-480V", "COMP-AIR-1")

    # Critical Factory Automation & Dojo Compute Power Quality
    add_node(
        tag="UPS-DOJO-1",
        name="1000 kVA Cortex Dojo & Factory SCADA Online Double-Conversion UPS",
        object_class="UninterruptiblePowerSupplyObject",
        domain="power_quality",
        type_tag="UPS",
        type_name="Three-Phase Transformerless Industrial UPS",
        room="Building 1 - Factory IT Data Center Room D01",
        fed_from="ATS-EMERG-1",
        voltage="480Y/277V 3Ø 4W",
        amps=1203.0,
        aic=65.0,
        attributes={
            "kva": 1000.0,
            "kw": 1000.0,
            "topology": "Online Double-Conversion VFI-SS-111",
            "battery_backup_min": 15.0,
            "efficiency_pct": 97.2
        }
    )
    add_edge("ATS-EMERG-1", "UPS-DOJO-1")

    add_node(
        tag="PDU-DOJO-RACKS-1",
        name="Factory Neural Net & SCADA Automation Compute PDU (400A)",
        object_class="PowerDistributionPanelObject",
        domain="panels",
        type_tag="PDU",
        type_name="Data Center Power Distribution Unit",
        room="Building 1 - Factory IT Data Center Room D01",
        fed_from="UPS-DOJO-1",
        voltage="208Y/120V 3Ø 4W",
        amps=400.0,
        aic=22.0,
        is_panel=1,
        slots=42,
        attributes={"k_factor": 20, "isolated_ground": True}
    )
    add_edge("UPS-DOJO-1", "PDU-DOJO-RACKS-1")

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
    generate_tesla_gigafactory()
