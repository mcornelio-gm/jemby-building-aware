"""
JAMES Electrical Digital Twin - Checklists Service
Loads and parses master inspection checklists from Excel workbook with automatic mtime caching.
"""

import os
import openpyxl
from typing import Dict, List, Any, Optional

CHECKLISTS_XLSX_PATH = "data/checklists/build_aware_electrical_checklists.xlsx"
FALLBACK_XLSX_PATH = "faq/checklists/build_aware_electrical_checklists.xlsx"

_CACHE: Dict[str, Any] = {
    "mtime": 0,
    "checklists": [],
    "by_id": {},
    "by_domain": {}
}

# Domain to Checklist_ID Mapping Rules
DOMAIN_CHECKLIST_MAP = {
    "panels": ["CHK-SAFETY-70E", "CHK-GEN-110", "CHK-PANEL-408", "CHK-BKR-240"],
    "transformers": ["CHK-SAFETY-70E", "CHK-GEN-110", "CHK-XFRM-450", "CHK-GND-250"],
    "switches": ["CHK-SAFETY-70E", "CHK-GEN-110", "CHK-SW-404", "CHK-BKR-240"],
    "sources": ["CHK-SAFETY-70E", "CHK-GEN-110", "CHK-GND-250", "CHK-SW-404"],
    "power_quality": ["CHK-SAFETY-70E", "CHK-GEN-110", "CHK-BKR-240", "CHK-GND-250"],
    "loads": ["CHK-SAFETY-70E", "CHK-GEN-110", "CHK-SW-404", "CHK-BKR-240"],
    "cables": ["CHK-SAFETY-70E", "CHK-GEN-110", "CHK-BKR-240", "CHK-GND-250"],
    "metering": ["CHK-SAFETY-70E", "CHK-GEN-110", "CHK-PANEL-408"],
    "renewables": ["CHK-SAFETY-70E", "CHK-GEN-110", "CHK-GND-250", "CHK-SW-404"],
    "generic": ["CHK-SAFETY-70E", "CHK-GEN-110"]
}


def _get_xlsx_path() -> str:
    if os.path.exists(CHECKLISTS_XLSX_PATH):
        return CHECKLISTS_XLSX_PATH
    if os.path.exists(FALLBACK_XLSX_PATH):
        return FALLBACK_XLSX_PATH
    return CHECKLISTS_XLSX_PATH


def load_master_checklists(force_reload: bool = False) -> List[Dict[str, Any]]:
    """Loads all checklist sheets from the master Excel workbook."""
    xlsx_path = _get_xlsx_path()
    if not os.path.exists(xlsx_path):
        return _CACHE.get("checklists", [])

    current_mtime = os.path.getmtime(xlsx_path)
    if not force_reload and _CACHE["mtime"] == current_mtime and _CACHE["checklists"]:
        return _CACHE["checklists"]

    try:
        wb = openpyxl.load_workbook(xlsx_path, data_only=True)
        checklists = []
        by_id = {}

        for sheetname in wb.sheetnames:
            if sheetname == "Index & Summary":
                continue
            
            ws = wb[sheetname]
            rows = list(ws.iter_rows(values_only=True))
            if not rows or len(rows) < 2:
                continue

            headers = [str(h or "").strip() for h in rows[0]]
            items = []
            
            chk_id = ""
            chk_title = sheetname
            category = "general"

            for r in rows[1:]:
                if not any(r):
                    continue
                row_dict = dict(zip(headers, r))
                item_no = row_dict.get("Item_No") or len(items) + 1
                std_ref = row_dict.get("Standard_Ref") or ""
                prompt = row_dict.get("Inspection_Prompt") or ""
                criteria = row_dict.get("Verification_Criteria") or ""
                severity = row_dict.get("Severity") or "Major"
                frequency = row_dict.get("Standard_Frequency") or "Initial Survey"
                guidance = row_dict.get("Guidance_Notes") or ""
                chk_id = row_dict.get("Checklist_ID") or chk_id
                category = row_dict.get("Category") or category
                chk_title = row_dict.get("Checklist_Title") or chk_title

                items.append({
                    "item_no": int(item_no) if str(item_no).isdigit() else item_no,
                    "standard_ref": str(std_ref).strip(),
                    "inspection_prompt": str(prompt).strip(),
                    "verification_criteria": str(criteria).strip(),
                    "severity": str(severity).strip(),
                    "standard_frequency": str(frequency).strip(),
                    "guidance_notes": str(guidance).strip()
                })

            if not chk_id:
                chk_id = "CHK-" + sheetname.replace(" ", "-").upper()

            chk_obj = {
                "id": chk_id,
                "tab_name": sheetname,
                "title": chk_title,
                "category": category,
                "total_items": len(items),
                "items": items
            }
            checklists.append(chk_obj)
            by_id[chk_id] = chk_obj

        _CACHE["mtime"] = current_mtime
        _CACHE["checklists"] = checklists
        _CACHE["by_id"] = by_id
        return checklists
    except Exception as e:
        print(f"[Checklists Service] Error reading {xlsx_path}: {e}")
        return _CACHE.get("checklists", [])


def get_all_checklists() -> List[Dict[str, Any]]:
    """Returns all parsed checklists."""
    return load_master_checklists()


def get_checklist_by_id(chk_id: str) -> Optional[Dict[str, Any]]:
    """Returns a specific checklist definition by ID."""
    load_master_checklists()
    return _CACHE["by_id"].get(chk_id)


def get_checklists_for_domain(domain_id: str, type_tag: str = "") -> List[Dict[str, Any]]:
    """
    Returns the mapped checklists for a given equipment domain and type tag.
    Always includes universal Safety and Clearances.
    """
    load_master_checklists()
    mapped_ids = DOMAIN_CHECKLIST_MAP.get(domain_id, ["CHK-SAFETY-70E", "CHK-GEN-110"])
    
    # Custom type overrides (e.g. ATS or Transformers)
    tag = (type_tag or "").upper()
    if tag in ["ATS", "MTS", "DISC", "SWITCH"] and "CHK-SW-404" not in mapped_ids:
        mapped_ids.append("CHK-SW-404")
    elif tag in ["XFMR", "PAD"] and "CHK-XFRM-450" not in mapped_ids:
        mapped_ids.append("CHK-XFRM-450")

    result = []
    for cid in mapped_ids:
        if cid in _CACHE["by_id"]:
            result.append(_CACHE["by_id"][cid])
    
    # Fallback to all if domain has no specific mapping
    if not result:
        result = _CACHE["checklists"]
        
    return result
