#!/usr/bin/env python3
"""
Build Aware - Multi-Tab Master Electrical Checklists Generator
Generates a formatted multi-tab Excel workbook containing standard electrical inspection checklists
based on NFPA 70E, NFPA 70B, and NEC (NFPA 70) standards.
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

os.makedirs("data/checklists", exist_ok=True)
os.makedirs("faq/checklists", exist_ok=True)

wb = openpyxl.Workbook()
wb.remove(wb.active) # Remove default blank sheet

# Styling definitions
header_fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid") # Dark Slate 800
header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
index_header_fill = PatternFill(start_color="312E81", end_color="312E81", fill_type="solid") # Indigo 900

row_font = Font(name="Calibri", size=10)
bold_font = Font(name="Calibri", size=10, bold=True)
code_font = Font(name="Consolas", size=10, bold=True, color="1E1B4B")

thin_border = Border(
    left=Side(style="thin", color="CBD5E1"),
    right=Side(style="thin", color="CBD5E1"),
    top=Side(style="thin", color="CBD5E1"),
    bottom=Side(style="thin", color="CBD5E1")
)

critical_fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid") # Red-100
major_fill = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid") # Amber-100
high_fill = PatternFill(start_color="FFEDD5", end_color="FFEDD5", fill_type="solid") # Orange-100

headers = [
    "Item_No",
    "Standard_Ref",
    "Inspection_Prompt",
    "Verification_Criteria",
    "Severity",
    "Standard_Frequency",
    "Guidance_Notes",
    "Checklist_ID",
    "Category",
    "Checklist_Title"
]

col_widths = {
    "A": 10, # Item_No
    "B": 18, # Standard_Ref
    "C": 48, # Inspection_Prompt
    "D": 48, # Verification_Criteria
    "E": 14, # Severity
    "F": 16, # Standard_Frequency
    "G": 48, # Guidance_Notes
    "H": 18, # Checklist_ID
    "I": 14, # Category
    "J": 35  # Checklist_Title
}

sheets_data = [
    {
        "tab_name": "NFPA 70E Safety",
        "chk_id": "CHK-SAFETY-70E",
        "category": "safety",
        "title": "NFPA 70E Pre-Work Hazard Analysis & Safety",
        "standard_basis": "NFPA 70E Standard for Electrical Safety in the Workplace",
        "items": [
            [
                1, "NFPA 70E 110.1", "Verify electrical safety program and site job safety briefing.",
                "Job safety plan documented and briefing conducted with all personnel before opening equipment.",
                "Critical", "Pre-Task", "Mandatory before opening any energized electrical enclosure."
            ],
            [
                2, "NFPA 70E 130.5", "Verify equipment has an updated Arc Flash risk assessment & label.",
                "Label displays nominal system voltage, arc flash boundary, and incident energy (cal/cm2) or PPE category.",
                "Critical", "Visual / Initial", "Labels must be updated whenever system modifications occur or at minimum every 5 years."
            ],
            [
                3, "NFPA 70E 130.4", "Establish shock protection boundaries (Limited and Restricted approach).",
                "Boundaries clearly identified based on system AC/DC voltage tables.",
                "Critical", "Pre-Task", "Only qualified persons with appropriate insulated tools permitted inside restricted boundary."
            ],
            [
                4, "NFPA 70E 130.7", "Inspect PPE condition and voltage ratings for task.",
                "Rubber insulating gloves air-tested and within test date; arc-rated face shield/suit clean and undamaged.",
                "Critical", "Pre-Task", "Rubber insulating gloves must be electrically re-tested every 6 months."
            ]
        ]
    },
    {
        "tab_name": "NEC 110 Clearances",
        "chk_id": "CHK-GEN-110",
        "category": "general",
        "title": "General Working Clearances & Enclosure Environment",
        "standard_basis": "NEC 2023 / NFPA 70 Article 110 (General Requirements)",
        "items": [
            [
                1, "NEC 110.26(A)(1)", "Verify minimum 36-inch (or depth by voltage condition) clear working space in front of equipment.",
                "Unobstructed depth (36 in. up to 150V, 42 in. 151-600V Condition 2) maintaining full 90-degree door swing.",
                "Critical", "Initial Survey", "Working space cannot be used for permanent or temporary storage."
            ],
            [
                2, "NEC 110.26(A)(2)", "Verify minimum width of working space is at least 30 inches or width of equipment.",
                "Width accommodates equipment footprint and allows unimpeded egress.",
                "Major", "Initial Survey", "Measure from outer edges of enclosure trim."
            ],
            [
                3, "NEC 110.26(A)(3)", "Verify minimum 6.5 ft (or equipment height) headroom in working space.",
                "Ceiling, piping, and ductwork clear above working area.",
                "Major", "Initial Survey", "Exceptions apply for existing residential service replacements."
            ],
            [
                4, "NEC 110.26(E)", "Verify dedicated electrical space above and below panelboard/switchboard.",
                "No foreign systems (plumbing, drainage, steam, HVAC ducts) within dedicated zone extending to structural ceiling.",
                "Critical", "Initial Survey", "Protection against leaks and condensation required if foreign systems pass outside zone."
            ],
            [
                5, "NEC 110.16(A)", "Verify presence of field or factory Arc Flash warning label.",
                "Clearly visible label on switchboards, switchgear, panelboards, and motor control centers.",
                "High", "Initial Survey", "Required on equipment likely to require examination, adjustment, or maintenance while energized."
            ],
            [
                6, "NEC 110.28", "Verify enclosure NEMA/IP rating is suitable for environmental conditions.",
                "NEMA 1 (indoor dry), NEMA 3R (outdoor rain), NEMA 4/4X (washdown/corrosive), NEMA 12 (industrial dust/oil).",
                "Major", "Initial Survey", "Inspect for moisture intrusion, corrosion, or compromised gaskets."
            ]
        ]
    },
    {
        "tab_name": "NEC 408 Panels & Gear",
        "chk_id": "CHK-PANEL-408",
        "category": "panel",
        "title": "Panelboards, Switchboards & Switchgear Audit",
        "standard_basis": "NEC Article 408 & NFPA 70B (Panelboards & Switchboards)",
        "items": [
            [
                1, "NEC 408.4(A)", "Verify circuit directory / panel schedule is complete, accurate, and legible.",
                "Every circuit breaker clearly identified with specific room/load served; no vague labels like 'Lights'.",
                "Major", "Annual / Survey", "Crucial for emergency isolation and single-line diagram validation."
            ],
            [
                2, "NEC 408.36", "Verify panelboard overcurrent protection rating does not exceed busbar rating.",
                "Main breaker or upstream feeder overcurrent device <= panel ampacity rating.",
                "Critical", "Initial Survey", "Check nameplate continuous current rating against supply device."
            ],
            [
                3, "NEC 408.41", "Verify grounded conductor (neutral) terminals have only one conductor per terminal.",
                "Each neutral wire connected to an individual terminal screw unless identified for multiple conductors.",
                "Major", "Initial Survey", "Do not double-lug neutrals on standard terminal bars."
            ],
            [
                4, "NEC 408.7", "Verify all unused breaker openings are closed with approved filler plates.",
                "No open knockouts or exposed busbar slots on dead-front cover.",
                "High", "Visual / Monthly", "Prevents accidental finger contact and containment of internal flash."
            ],
            [
                5, "NFPA 70B 13.2", "Inspect enclosure and busbar for thermal discoloration, arcing, or foreign contamination.",
                "No signs of heat damage, carbon deposits, rodent intrusion, metal shavings, or moisture.",
                "Critical", "Annual 70B", "Infrared thermography scan recommended under load."
            ]
        ]
    },
    {
        "tab_name": "NEC 450 Transformers",
        "chk_id": "CHK-XFRM-450",
        "category": "transformer",
        "title": "Dry-Type & Liquid Transformers Verification",
        "standard_basis": "NEC Article 450 & NFPA 70B (Transformers)",
        "items": [
            [
                1, "NEC 450.9", "Verify adequate ventilation clearances around transformer enclosure.",
                "Minimum manufacturer clearance (typically 6-12 inches) maintained from walls and obstructions.",
                "Critical", "Initial Survey", "Ventilation louvers must be clean and unblocked to prevent thermal degradation."
            ],
            [
                2, "NEC 450.3", "Verify primary and secondary overcurrent protection complies with sizing tables.",
                "Overcurrent device size <= maximum percentage in NEC Table 450.3(A)/(B) (e.g. 125% or next standard size).",
                "Critical", "Initial Survey", "Calculated based on primary/secondary full-load amperes (FLA)."
            ],
            [
                3, "NEC 250.30(A)", "Verify separately derived system grounding electrode conductor (GEC) & bonding jumper.",
                "System bonding jumper connects X0 neutral to transformer enclosure and grounding electrode conductor.",
                "Critical", "Initial Survey", "Sized according to NEC Table 250.102(C)(1) based on derived phase conductors."
            ],
            [
                4, "NFPA 70B 21.2", "Inspect core, coils, and terminal connections for loose lugs, dust buildup, or acoustic noise.",
                "Connections torqued to specification; no abnormal humming, vibration, or insulation varnish cracking.",
                "Major", "Annual 70B", "Clean coils with dry, low-pressure compressed air or vacuum."
            ]
        ]
    },
    {
        "tab_name": "NEC 240 Breakers & Fuses",
        "chk_id": "CHK-BKR-240",
        "category": "breaker",
        "title": "Circuit Breakers & Fuses Verification",
        "standard_basis": "NEC Article 240 & NFPA 70B (Overcurrent Protection)",
        "items": [
            [
                1, "NEC 240.4", "Verify conductor ampacity is properly protected by the upstream breaker or fuse rating.",
                "Conductor gauge (AWG/kcmil) ampacity (75°C column) >= overcurrent protective device rating (with standard size rules).",
                "Critical", "Initial Survey", "Check continuous load factors (125%) where applicable."
            ],
            [
                2, "NEC 240.86", "Verify series ratings or fully rated AIC exceeds available fault current (SCCR).",
                "Interrupting rating (kAIC) of breaker >= available short-circuit current from upstream utility/source.",
                "Critical", "Initial Survey", "Prevents catastrophic breaker explosion during dead short-circuit."
            ],
            [
                3, "NFPA 70B 17.2", "Exercise molded-case circuit breaker mechanisms and verify smooth handle operation.",
                "Breaker trips and resets crisply; handle not loose or binding.",
                "Major", "Annual 70B", "De-energized mechanical exercise prevents contact welding."
            ]
        ]
    },
    {
        "tab_name": "NEC 250 Grounding",
        "chk_id": "CHK-GND-250",
        "category": "grounding",
        "title": "Grounding Electrode System & Equipment Bonding",
        "standard_basis": "NEC Article 250 (Grounding & Bonding)",
        "items": [
            [
                1, "NEC 250.50", "Verify all available grounding electrodes (water pipe, steel frame, rod/pipe, concrete-encased) bonded together.",
                "Interconnected into a single Grounding Electrode System (GES).",
                "Critical", "Initial Survey", "25 ohms or supplemental electrode required for single rod/pipe/plate."
            ],
            [
                2, "NEC 250.64(E)", "Verify bonding of ferrous metal raceways containing Grounding Electrode Conductors (GEC).",
                "Both ends of conduit bonded to ensure low-impedance path and eliminate inductive choke effect.",
                "Critical", "Initial Survey", "Bonding bushings required at both service enclosure and electrode entry."
            ],
            [
                3, "NEC 250.122", "Verify equipment grounding conductor (EGC) size in raceway/cable matches upstream overcurrent device.",
                "Sized per Table 250.122 (e.g. 10 AWG Cu for 30A, 8 AWG for 40/50A, 6 AWG for 60A).",
                "Critical", "Initial Survey", "Must be increased proportionally if ungrounded conductors are upsized for voltage drop."
            ]
        ]
    },
    {
        "tab_name": "NEC 404 Switches & Motors",
        "chk_id": "CHK-SW-404",
        "category": "switch",
        "title": "Disconnect Switches & Motor Controls",
        "standard_basis": "NEC Article 404 & 430 (Switches & Motors)",
        "items": [
            [
                1, "NEC 430.102", "Verify disconnect switch is in sight from motor location (or lockable in open position).",
                "Within 50 ft and visible line of sight unless locked under safety protocol.",
                "Critical", "Initial Survey", "Disconnect must open all ungrounded supply conductors simultaneously."
            ],
            [
                2, "NEC 404.6(A)", "Verify knife switches / safety switches are installed so gravity will not close them.",
                "Up position = ON / Closed; Down position = OFF / Open.",
                "Critical", "Initial Survey", "Enclosure interlock prevents opening door with switch in ON position."
            ],
            [
                3, "NFPA 70B 16.2", "Inspect switch blade contacts for pitting, burning, alignment, and spring tension.",
                "Clean contact surface; adequate clip pressure and uniform blade engagement.",
                "Major", "Annual 70B", "Check fuse clip tension and apply dielectric lubricant if specified."
            ]
        ]
    }
]

# 1. Index & Summary Sheet
ws_index = wb.create_sheet(title="Index & Summary")
index_headers = ["Checklist_ID", "Tab_Name", "Domain / Category", "Checklist_Title", "Standard_Basis", "Items_Count", "Application_Notes"]
ws_index.append(index_headers)

for col_num, cell in enumerate(ws_index[1], 1):
    cell.fill = index_header_fill
    cell.font = header_font
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

total_items = 0
for idx, s in enumerate(sheets_data, 2):
    cnt = len(s["items"])
    total_items += cnt
    cat_name = s["category"]
    row_vals = [
        s["chk_id"],
        s["tab_name"],
        cat_name.upper(),
        s["title"],
        s["standard_basis"],
        cnt,
        f"Used for {cat_name} inspection and code verification."
    ]
    ws_index.append(row_vals)
    for col_idx in range(1, len(row_vals) + 1):
        cell = ws_index.cell(row=idx, column=col_idx)
        cell.font = row_font
        cell.border = thin_border
        cell.alignment = Alignment(vertical="center")
        if col_idx in (1, 2, 3, 6):
            cell.alignment = Alignment(horizontal="center", vertical="center")
            if col_idx == 1:
                cell.font = code_font

index_col_widths = {"A": 20, "B": 24, "C": 18, "D": 42, "E": 48, "F": 14, "G": 40}
for col_letter, width in index_col_widths.items():
    ws_index.column_dimensions[col_letter].width = width

ws_index.row_dimensions[1].height = 28
for r in range(2, len(sheets_data) + 2):
    ws_index.row_dimensions[r].height = 26

ws_index.freeze_panes = "A2"

# 2. Domain Sheets
for s in sheets_data:
    ws = wb.create_sheet(title=s["tab_name"])
    ws.append(headers)
    
    for col_num, cell in enumerate(ws[1], 1):
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    for r_idx, item in enumerate(s["items"], 2):
        row_data = [
            item[0], # Item_No
            item[1], # Standard_Ref
            item[2], # Inspection_Prompt
            item[3], # Verification_Criteria
            item[4], # Severity
            item[5], # Standard_Frequency
            item[6], # Guidance_Notes
            s["chk_id"],   # Checklist_ID
            s["category"], # Category
            s["title"]     # Checklist_Title
        ]
        ws.append(row_data)
        for col_idx in range(1, len(row_data) + 1):
            cell = ws.cell(row=r_idx, column=col_idx)
            cell.font = row_font
            cell.border = thin_border
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            
            if col_idx in (1, 2, 5, 6, 8, 9):
                cell.alignment = Alignment(horizontal="center", vertical="top")
            
            if col_idx == 2:
                cell.font = code_font
            
            # Severity color highlight
            if col_idx == 5:
                val = str(cell.value or "")
                if "Critical" in val:
                    cell.fill = critical_fill
                    cell.font = bold_font
                elif "Major" in val:
                    cell.fill = major_fill
                elif "High" in val:
                    cell.fill = high_fill

    for col_letter, width in col_widths.items():
        ws.column_dimensions[col_letter].width = width

    ws.row_dimensions[1].height = 28
    for r in range(2, len(s["items"]) + 2):
        ws.row_dimensions[r].height = 42

    ws.freeze_panes = "A2"

# Save workbook
xlsx_path = "data/checklists/build_aware_electrical_checklists.xlsx"
faq_xlsx_path = "faq/checklists/build_aware_electrical_checklists.xlsx"
wb.save(xlsx_path)
wb.save(faq_xlsx_path)

# Also remove old flat CSV to keep clean
if os.path.exists("data/checklists/build_aware_electrical_checklists.csv"):
    os.remove("data/checklists/build_aware_electrical_checklists.csv")
if os.path.exists("faq/checklists/build_aware_electrical_checklists.csv"):
    os.remove("faq/checklists/build_aware_electrical_checklists.csv")

print(f"✓ Generated multi-tab workbook with {len(sheets_data)} domain sheets and {total_items} items.")
