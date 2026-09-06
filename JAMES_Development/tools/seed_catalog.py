#!/usr/bin/env python3
"""Seed Master Catalog from Tables for Building Aware.docx into data/catalog/{manufacturer}.json."""

import json
import os
import re
import xml.etree.ElementTree as ET
import zipfile

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "catalog")
os.makedirs(DATA_DIR, exist_ok=True)

DOCX_PATH = "/Users/michaelcornelio/jemby/jemby_solutions/jemby_gcp/Tables for Building Aware.docx"

with zipfile.ZipFile(DOCX_PATH) as z:
    xml_content = z.read("word/document.xml")
    root = ET.fromstring(xml_content)
    
    paragraphs = []
    for p in root.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p"):
        texts = [node.text for node in p.iter("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t") if node.text]
        if texts:
            paragraphs.append("".join(texts).strip())

catalogs = {
    "eaton": {"manufacturer": "Eaton", "items": []},
    "squared": {"manufacturer": "Square D / Schneider Electric", "items": []},
    "siemens": {"manufacturer": "Siemens", "items": []},
    "bussmann": {"manufacturer": "Bussmann (Eaton)", "items": []},
    "generac": {"manufacturer": "Generac Power Systems", "items": []},
    "leviton": {"manufacturer": "Leviton", "items": []},
    "southwire": {"manufacturer": "Southwire / Encore", "items": []},
    "allied_tube": {"manufacturer": "Allied Tube & Conduit / Atkore", "items": []},
    "cooper_lighting": {"manufacturer": "Cooper Lighting / Acuity Brands", "items": []}
}

# 1. Eaton Breakers (PDF / PDG / PDD / PDC / PDO / PDP)
for p in paragraphs:
    m_pd = re.search(r"\b(PD[A-Z0-9]{10,16})\b(?:\s*\((.*?)\))?", p)
    if m_pd:
        pn = m_pd.group(1)
        desc = m_pd.group(2) or ""
        
        frame = "Frame 2"
        poles = 3
        amps = 100.0
        aic = 65.0
        
        m_frame = re.search(r"Frame\s*(\d)", desc)
        if m_frame:
            frame = f"Frame {m_frame.group(1)}"
        elif pn.startswith("PDG1") or pn.startswith("PDF1"):
            frame = "Frame 1"
        elif pn.startswith("PDG2") or pn.startswith("PDF2") or pn.startswith("PDD2") or pn.startswith("PDO2") or pn.startswith("PDP2"):
            frame = "Frame 2"
        elif pn.startswith("PDG3") or pn.startswith("PDF3") or pn.startswith("PDO3") or pn.startswith("PDP3"):
            frame = "Frame 3"
        elif pn.startswith("PDG4") or pn.startswith("PDF4") or pn.startswith("PDO4") or pn.startswith("PDP4"):
            frame = "Frame 4"
        elif pn.startswith("PDG5") or pn.startswith("PDF5") or pn.startswith("PDC5"):
            frame = "Frame 5"
        elif pn.startswith("PDG6") or pn.startswith("PDF6"):
            frame = "Frame 6"

        m_poles = re.search(r"(Single|Two|Three|Four|\d)\s*Pole", desc, re.I)
        if m_poles:
            p_str = m_poles.group(1).lower()
            if p_str in ["single", "1"]: poles = 1
            elif p_str in ["two", "2"]: poles = 2
            elif p_str in ["three", "3"]: poles = 3
            elif p_str in ["four", "4"]: poles = 4
        else:
            if len(pn) > 4 and pn[3].isdigit():
                poles = int(pn[3])

        m_amps = re.search(r"(\d+(?:\.\d+)?)\s*A", desc, re.I)
        if m_amps:
            amps = float(m_amps.group(1))
        else:
            m_a_code = re.search(r"[A-Z](\d{4})[A-Z]", pn)
            if m_a_code:
                amps = float(int(m_a_code.group(1)))

        if "65" in desc or frame in ["Frame 3", "Frame 4"]:
            aic = 65.0
        elif frame in ["Frame 5", "Frame 6"]:
            aic = 100.0
        elif frame == "Frame 1":
            aic = 25.0
        else:
            aic = 35.0

        item_desc = desc if desc else f"Eaton Power Defense {frame} {poles}-Pole {amps:.0f}A Circuit Breaker"

        catalogs["eaton"]["items"].append({
            "part_number": pn,
            "series": f"Power Defense {frame}",
            "domain": "breakers",
            "type_tag": "CB",
            "type_name": "Molded Case Circuit Breaker",
            "description": item_desc,
            "specs": {
                "voltage": "480Y/277V" if amps > 60 else "240/120V",
                "amps": amps,
                "poles": poles,
                "aic": aic,
                "frame": frame,
                "interrupt_rating": f"{aic}kA @ 480V",
                "trip_type": "Electronic / Thermal Magnetic",
                "nema_rating": "NEMA 1"
            },
            "docs": {"cut_sheet": "", "upc": None}
        })

# 2. Eaton Modular Metering (MPS / MPN / SPN series)
for p in paragraphs:
    m_meter = re.search(r"\b(MP[A-Z0-9]{10,14}|SP[A-Z0-9]{10,14})\b", p)
    if m_meter:
        pn = m_meter.group(1)
        catalogs["eaton"]["items"].append({
            "part_number": pn,
            "series": "1MP / 3MM Commercial & Residential Modular Metering",
            "domain": "panels",
            "type_tag": "REC",
            "type_name": "Meter Center / Modular Meter Stack",
            "description": f"Eaton Modular Meter Stack / Tenant Main ({pn})",
            "specs": {
                "voltage": "208Y/120V 3Ø 4W" if "3" in pn[:4] or "MPN" in pn else "120/240V 1Ø 3W",
                "amps": 200.0,
                "aic": 65.0,
                "slots": 12,
                "nema_rating": "NEMA 3R" if "SW" in pn else "NEMA 1"
            },
            "docs": {"cut_sheet": "", "upc": None}
        })

# 3. Eaton Safety Switches (DG & DH Series)
for p in paragraphs:
    m_dg = re.search(r"\b(DG[0-9]{3}[A-Z0-9\-]+)\b", p)
    if m_dg:
        pn = m_dg.group(1)
        poles = 3 if pn.startswith("DG3") else 2
        a_map = {"1": 30, "2": 60, "3": 100, "4": 200, "5": 400, "6": 600}
        digit = pn[3] if len(pn) > 3 else "2"
        amps = float(a_map.get(digit, 60))
        is_fusible = "F" in pn[4:6] or "FR" in pn or "FG" in pn
        is_rainproof = "R" in pn[4:7] or "RB" in pn or "RK" in pn
        f_label = "Fusible" if is_fusible else "Non-Fusible"
        
        catalogs["eaton"]["items"].append({
            "part_number": pn,
            "series": "DG Series General Duty Safety Switch",
            "domain": "switches",
            "type_tag": "DISC",
            "type_name": "Safety Switch / Disconnect",
            "description": f"Eaton General Duty Safety Switch {poles}P {amps:.0f}A ({f_label})",
            "specs": {
                "voltage": "240V" if poles == 2 else "240V / 480V",
                "amps": amps,
                "poles": poles,
                "aic": 100.0 if is_fusible else 10.0,
                "fuse_style": "Class R / Class H" if is_fusible else "Non-Fused",
                "nema_rating": "NEMA 3R (Rainproof)" if is_rainproof else "NEMA 1 (Indoor)"
            },
            "docs": {"cut_sheet": "", "upc": None}
        })

    m_dh = re.search(r"\b(DH[0-9]{3}[A-Z0-9\-]+)\b", p)
    if m_dh:
        pn = m_dh.group(1)
        poles = 3 if pn.startswith("DH3") else (4 if pn.startswith("DH4") else 2)
        digit = pn[3] if len(pn) > 3 else "2"
        a_map = {"1": 30, "2": 60, "3": 100, "4": 200, "5": 400, "6": 600, "7": 800, "8": 1200}
        amps = float(a_map.get(digit, 100))
        is_fusible = "F" in pn[4:6]
        is_ss = "W" in pn or "K" in pn
        f_label = "Fusible" if is_fusible else "Non-Fusible"
        
        catalogs["eaton"]["items"].append({
            "part_number": pn,
            "series": "DH Series Heavy Duty Safety Switch",
            "domain": "switches",
            "type_tag": "DISC",
            "type_name": "Heavy Duty Safety Switch",
            "description": f"Eaton Heavy Duty Safety Switch {poles}P {amps:.0f}A ({f_label})",
            "specs": {
                "voltage": "600V AC/DC",
                "amps": amps,
                "poles": poles,
                "aic": 200.0 if is_fusible else 10.0,
                "fuse_style": "Class J / Class R" if is_fusible else "Non-Fused",
                "nema_rating": "NEMA 4X (Stainless)" if is_ss else "NEMA 12 / 3R"
            },
            "docs": {"cut_sheet": "", "upc": None}
        })

# 4. Transformers
sqd_xfmrs = [
    {"pn": "EE75T3H", "kva": 75.0, "notes": "150°C rise, 20 taps, 480V Delta - 208Y/120V"},
    {"pn": "75T3HNV", "kva": 75.0, "notes": "Ventilated dry-type, 480V Delta - 208Y/120V"},
    {"pn": "EE112T3HFISNLP", "kva": 112.5, "notes": "NEMA 1, isolated, 480V Delta - 208Y/120V"},
    {"pn": "EE150T3HFISNLP", "kva": 150.0, "notes": "NEMA 1, 480V Delta - 208Y/120V"},
    {"pn": "EE225T3H", "kva": 225.0, "notes": "Standard Ventilated Dry-Type 480V Delta - 208Y/120V"}
]
for x in sqd_xfmrs:
    kva_val = x["kva"]
    notes_val = x["notes"]
    catalogs["squared"]["items"].append({
        "part_number": x["pn"],
        "series": "EE Series Low Voltage Dry-Type",
        "domain": "transformers",
        "type_tag": "XFMR",
        "type_name": "Dry-Type Step-Down Transformer",
        "description": f"Square D {kva_val:.0f} kVA Dry-Type Distribution Transformer ({notes_val})",
        "specs": {
            "kva": kva_val,
            "primary_voltage": "480V Delta",
            "secondary_voltage": "208Y/120V",
            "voltage": "480V : 208Y/120V",
            "phase": "3Ø",
            "impedance_z": 4.5,
            "winding": "Aluminum",
            "temp_rise": "150°C",
            "nema_rating": "NEMA 1 (Indoor Ventilated)"
        },
        "docs": {"cut_sheet": "", "upc": None}
    })

eaton_xfmrs = [
    {"pn": "V48M28T75EE", "kva": 75.0, "notes": "NEMA 1, Energy Star, aluminum windings"},
    {"pn": "V48M28T7516", "kva": 75.0, "notes": "NEMA 3R (outdoor enclosure)"},
    {"pn": "V48M28T112516", "kva": 112.5, "notes": "NEMA 3R (FR943 frame)"}
]
for x in eaton_xfmrs:
    kva_val = x["kva"]
    notes_val = x["notes"]
    catalogs["eaton"]["items"].append({
        "part_number": x["pn"],
        "series": "V48M Ventilated Transformer Series",
        "domain": "transformers",
        "type_tag": "XFMR",
        "type_name": "Dry-Type Step-Down Transformer",
        "description": f"Eaton {kva_val:.0f} kVA Ventilated Transformer ({notes_val})",
        "specs": {
            "kva": kva_val,
            "primary_voltage": "480V Delta",
            "secondary_voltage": "208Y/120V",
            "voltage": "480V : 208Y/120V",
            "phase": "3Ø",
            "impedance_z": 4.8,
            "winding": "Aluminum",
            "nema_rating": "NEMA 3R" if "3R" in notes_val else "NEMA 1"
        },
        "docs": {"cut_sheet": "", "upc": None}
    })

siemens_xfmrs = [
    {"pn": "T1F10075A5RXXM", "kva": 75.0, "notes": "Aluminum windings, catalog format"},
    {"pn": "T1F10150A5RXXM", "kva": 150.0, "notes": "Ventilated dry-type"},
    {"pn": "T1F10200A5RXXM", "kva": 200.0, "notes": "Standard ventilated size"}
]
for x in siemens_xfmrs:
    kva_val = x["kva"]
    notes_val = x["notes"]
    catalogs["siemens"]["items"].append({
        "part_number": x["pn"],
        "series": "Standard Ventilated Dry-Type",
        "domain": "transformers",
        "type_tag": "XFMR",
        "type_name": "Dry-Type Step-Down Transformer",
        "description": f"Siemens {kva_val:.0f} kVA Distribution Transformer ({notes_val})",
        "specs": {
            "kva": kva_val,
            "primary_voltage": "480V Delta",
            "secondary_voltage": "208Y/120V",
            "voltage": "480V : 208Y/120V",
            "phase": "3Ø",
            "impedance_z": 5.0,
            "winding": "Aluminum",
            "nema_rating": "NEMA 1 (Indoor)"
        },
        "docs": {"cut_sheet": "", "upc": None}
    })

# 5. Bussmann Fuses
bussmann_fuses = [
    {"upc": "051712204446", "pn": "LPJ-200SPI", "amps": 200.0, "desc": "Bussmann Low-Peak Class J Time-Delay Indicating Fuse 200A 600V"},
    {"upc": "051712101851", "pn": "LP-CC-30", "amps": 30.0, "desc": "Bussmann Low-Peak Class CC Time-Delay Current-Limiting Fuse 30A 600V"},
    {"upc": "051712204606", "pn": "LPJ-400SP", "amps": 400.0, "desc": "Bussmann Low-Peak Class J Time-Delay Fuse 400A 600V"},
    {"upc": "051712508483", "pn": "FRN-R-100", "amps": 100.0, "desc": "Bussmann Fusetron Class RK5 Dual-Element Time-Delay Fuse 100A 250V"},
    {"upc": "051712522007", "pn": "FRS-R-200", "amps": 200.0, "desc": "Bussmann Fusetron Class RK5 Dual-Element Time-Delay Fuse 200A 600V"}
]
for f in bussmann_fuses:
    catalogs["bussmann"]["items"].append({
        "part_number": f["pn"],
        "series": "Low-Peak & Fusetron Industrial Fuses",
        "domain": "switches",
        "type_tag": "FUSE",
        "type_name": "Industrial Fuse",
        "description": f["desc"],
        "specs": {
            "voltage": "600V",
            "amps": f["amps"],
            "aic": 200.0,
            "fuse_type": "Class J / RK5",
            "time_delay": True,
            "current_limiting": True
        },
        "docs": {"cut_sheet": "", "upc": f["upc"]}
    })

# 6. Generac Generators & ATS
generac_items = [
    {"upc": "696471074352", "pn": "G0070432", "domain": "sources", "type_tag": "GEN", "desc": "Generac 22kW Guardian Series Standby Generator (240V 1-Phase Aluminum Enclosure)"},
    {"upc": "696471615180", "pn": "RXSW200A3", "domain": "switches", "type_tag": "ATS", "desc": "Generac 200A Service Rated Automatic Transfer Switch (NEMA 3R Aluminum Enclosure)"},
    {"upc": "696471617122", "pn": "G0071720", "domain": "sources", "type_tag": "GEN", "desc": "Generac 24kW Guardian Series Standby Generator (240V 1-Phase)"},
    {"upc": "696471618280", "pn": "G0071890", "domain": "sources", "type_tag": "GEN", "desc": "Generac 26kW Guardian Standby Generator with Wi-Fi"}
]
for g in generac_items:
    catalogs["generac"]["items"].append({
        "part_number": g["pn"],
        "series": "Guardian Standby Power Systems",
        "domain": g["domain"],
        "type_tag": g["type_tag"],
        "type_name": "Standby Generator" if g["type_tag"] == "GEN" else "Automatic Transfer Switch",
        "description": g["desc"],
        "specs": {
            "voltage": "120/240V 1Ø",
            "amps": 200.0 if g["type_tag"] == "ATS" else 100.0,
            "kw": 24.0 if g["type_tag"] == "GEN" else None,
            "nema_rating": "NEMA 3R (Outdoor Weatherproof)"
        },
        "docs": {"cut_sheet": "", "upc": g["upc"]}
    })

# 7. Leviton Wiring Devices
leviton_items = [
    {"upc": "078477819814", "pn": "5362-W", "type_tag": "REC", "desc": "Leviton 20A 125V Commercial Specification Grade Duplex Receptacle (White)"},
    {"upc": "078477809495", "pn": "5262-W", "type_tag": "REC", "desc": "Leviton 15A 125V Extra Heavy-Duty Industrial Spec Grade Duplex Receptacle"},
    {"upc": "078477901908", "pn": "8300-W", "type_tag": "REC", "desc": "Leviton Hospital Grade 20A 125V Extra Heavy-Duty Duplex Receptacle"},
    {"upc": "078477901717", "pn": "5266-C", "type_tag": "PLUG", "desc": "Leviton 15A 125V Industrial Grade Straight Blade Plug (Black & White)"},
    {"upc": "078477808450", "pn": "5366-C", "type_tag": "PLUG", "desc": "Leviton 20A 125V Industrial Grade Straight Blade Plug"},
    {"upc": "078477795200", "pn": "L520-P", "type_tag": "PLUG", "desc": "Leviton 20A 125V NEMA L5-20P Industrial Locking Plug"}
]
for l in leviton_items:
    catalogs["leviton"]["items"].append({
        "part_number": l["pn"],
        "series": "Industrial & Commercial Specification Grade",
        "domain": "loads" if l["type_tag"] == "REC" else "wiring",
        "type_tag": l["type_tag"],
        "type_name": "Commercial Receptacle" if l["type_tag"] == "REC" else "Industrial Plug",
        "description": l["desc"],
        "specs": {
            "voltage": "125V 1Ø",
            "amps": 20.0 if "20A" in l["desc"] else 15.0,
            "nema_rating": "NEMA 5-20R / NEMA 5-15R"
        },
        "docs": {"cut_sheet": "", "upc": l["upc"]}
    })

# 8. Southwire
southwire_items = [
    {"upc": "048243234479", "pn": "THHN-12-SOL-500", "desc": "Southwire 12 AWG Solid Copper THHN/THWN-2 Building Wire (500 ft Spool)"},
    {"upc": "980100229108", "pn": "THHN-10-STR-500", "desc": "Southwire 10 AWG Stranded Copper THHN/THWN-2 600V Building Wire"},
    {"upc": "980100234010", "pn": "XHHW-4/0-STR-1000", "desc": "Southwire 4/0 AWG Stranded Copper XHHW-2 600V Feeder Conductor"}
]
for w in southwire_items:
    catalogs["southwire"]["items"].append({
        "part_number": w["pn"],
        "series": "Simpull Copper Building Wire",
        "domain": "wiring",
        "type_tag": "CABLE",
        "type_name": "Building Wire Conductor",
        "description": w["desc"],
        "specs": {
            "voltage": "600V",
            "conductor": "Copper",
            "insulation": "THHN / THWN-2 / XHHW-2",
            "temp_rating": "90°C"
        },
        "docs": {"cut_sheet": "", "upc": w["upc"]}
    })

# 9. Allied Tube
allied_items = [
    {"upc": "980010020024", "pn": "EMT-075-10", "desc": "Allied Tube 3/4-inch Electrical Metallic Tubing (EMT) Steel Conduit 10ft"},
    {"upc": "980010001061", "pn": "EMT-100-10", "desc": "Allied Tube 1-inch Electrical Metallic Tubing (EMT) Steel Conduit 10ft"},
    {"upc": "980060060063", "pn": "RMC-200-10", "desc": "Allied Tube 2-inch Rigid Metal Conduit (RMC) Galvanized Steel 10ft"}
]
for c in allied_items:
    catalogs["allied_tube"]["items"].append({
        "part_number": c["pn"],
        "series": "E-Z Pull EMT & True Color Rigid Steel Conduit",
        "domain": "conduit",
        "type_tag": "CONDUIT",
        "type_name": "Electrical Conduit Raceway",
        "description": c["desc"],
        "specs": {
            "material": "Galvanized Steel",
            "trade_size": "3/4 in" if "075" in c["pn"] else ("1 in" if "100" in c["pn"] else "2 in"),
            "standard": "UL 797 / ANSI C80.3"
        },
        "docs": {"cut_sheet": "", "upc": c["upc"]}
    })

# 10. Cooper / Acuity Lighting
lighting_items = [
    {"upc": "080083838196", "pn": "IBH-18L-MVOLT", "desc": "Lithonia Lighting I-BEAM LED High Bay 18,000 Lumens 120-277V"},
    {"upc": "193048671889", "pn": "2VTL4-40L-ADP", "desc": "Lithonia Lighting Volumetric LED Troffer 2x4 4000 Lumens 120-277V"},
    {"upc": "844006091194", "pn": "GTL-4000L-40K", "desc": "Lithonia Lighting Recessed LED Troffer 2x4 Direct/Indirect"},
    {"upc": "807154905201", "pn": "CPX-2X4-4000LM", "desc": "Lithonia Lighting LED Flat Panel 2x4 Edge-Lit 4000LM"},
    {"upc": "190887529739", "pn": "OVR-LED-4FT", "desc": "Cooper Lighting Metalux 4ft LED Commercial Strip Luminaire"}
]
for li in lighting_items:
    catalogs["cooper_lighting"]["items"].append({
        "part_number": li["pn"],
        "series": "Commercial & Industrial LED Luminaires",
        "domain": "lighting",
        "type_tag": "LIGHT",
        "type_name": "Commercial LED Luminaire",
        "description": li["desc"],
        "specs": {
            "voltage": "120-277V MVOLT",
            "amps": 1.2,
            "watts": 135.0 if "18L" in li["pn"] else 40.0,
            "nema_rating": "NEMA 1 (Damp Location)"
        },
        "docs": {"cut_sheet": "", "upc": li["upc"]}
    })

# Write JSON files to data/catalog/
total_items = 0
for key, cat_data in catalogs.items():
    filepath = os.path.join(DATA_DIR, f"{key}.json")
    with open(filepath, "w") as f:
        json.dump(cat_data, f, indent=2)
    cnt = len(cat_data["items"])
    total_items += cnt
    print(f"Wrote {filepath}: {cnt} items")

print(f"Done! Seeded {total_items} total catalog items across {len(catalogs)} manufacturers.")
