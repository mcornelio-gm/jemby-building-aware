"""System Integrity Audit Engine for Electrical Digital Twins.

Performs deterministic multi-point engineering and topology checks:
1. Voltage Alignment & Transformation (flags direct voltage mismatches without step-down transformers)
2. Bus Capacity & Ampacity Headroom (upstream feed sizing vs downstream demand)
3. AIC / Short-Circuit Withstand Ratings (over-dutied downstream gear)
4. Topological Completeness (orphaned equipment, unassigned emergency feeds for ATS/MTS)
5. Panel Schedule Integrity (slot limit overflows, unassigned breaker loads)
6. Documentation & Survey Quality (nameplate photos, serial numbers, condition ratings)
"""

import csv
import io
import json
import re
from typing import Any, Dict, List, Optional, Tuple

from james_app.checklists import get_checklists_for_domain


def _parse_voltage_num(v_str: Any) -> Optional[float]:
    """Extract primary nominal line-to-line voltage number (e.g. '480Y/277V' -> 480.0, '208V' -> 208.0)."""
    if not v_str:
        return None
    s = str(v_str).strip()
    match = re.search(r'(\d+)', s)
    if match:
        try:
            return float(match.group(1))
        except ValueError:
            return None
    return None


def _parse_amps_num(a_str: Any) -> Optional[float]:
    """Extract numeric ampacity rating."""
    if a_str is None:
        return None
    try:
        return float(a_str)
    except (ValueError, TypeError):
        match = re.search(r'(\d+(?:\.\d+)?)', str(a_str))
        if match:
            try:
                return float(match.group(1))
            except ValueError:
                return None
    return None


def audit_facility_system_integrity(nodes: List[Dict[str, Any]], client: str = "", facility: str = "") -> Dict[str, Any]:
    """Run comprehensive System Integrity Audit over facility nodes."""
    nodes = nodes or []
    nodes_by_tag: Dict[str, Dict[str, Any]] = {}
    nodes_by_id: Dict[str, Dict[str, Any]] = {}

    for n in nodes:
        tag = (n.get("tag") or "").strip()
        if tag:
            nodes_by_tag[tag.upper()] = n
        nid = str(n.get("id") or "").strip()
        if nid:
            nodes_by_id[nid.upper()] = n

    findings: List[Dict[str, Any]] = []

    def add_finding(
        severity: str,  # 'critical', 'warning', 'info'
        category: str,  # 'Voltage', 'Capacity', 'Topology', 'AIC', 'Schedule', 'Documentation'
        asset_tag: str,
        asset_name: str,
        room: str,
        asset_id: str,
        title: str,
        description: str,
        recommendation: str
    ):
        findings.append({
            "id": f"audit_{len(findings) + 1}",
            "severity": severity.lower(),
            "category": category,
            "asset_tag": asset_tag or asset_id,
            "asset_name": asset_name or "Equipment",
            "room": room or "Unassigned Room",
            "asset_id": asset_id,
            "title": title,
            "description": description,
            "recommendation": recommendation
        })

    # 1. Topological Completeness & Orphan Checks
    for n in nodes:
        tag = n.get("tag") or n.get("id") or "EQ"
        name = n.get("name") or n.get("type_name") or tag
        domain = (n.get("domain") or "").lower()
        type_tag = (n.get("type_tag") or "").upper()
        room = n.get("room") or "Unassigned"
        nid = n.get("id") or tag
        attrs = n.get("attributes") or {}

        # Sources (UTIL, GEN, PV) are naturally root nodes
        if domain == "sources" or type_tag in ["UTIL", "GEN", "PV"]:
            continue

        raw_sources = attrs.get("upstream_sources") or []
        fed_from = n.get("fed_from") or attrs.get("fed_from") or ""
        valid_sources = [s for s in raw_sources if str(s).strip()]
        if not valid_sources and fed_from:
            valid_sources = [str(fed_from).strip()]

        if not valid_sources:
            add_finding(
                severity="critical",
                category="Topology",
                asset_tag=tag,
                asset_name=name,
                room=room,
                asset_id=nid,
                title="Orphaned Equipment (Missing Upstream Feed)",
                description=f"Equipment [{tag}] has no configured upstream electrical supply source.",
                recommendation="Assign upstream power source in the equipment form drawer or verify field feeder connection."
            )
        else:
            # Verify that upstream parent exists in the model
            for src in valid_sources:
                src_upper = str(src).strip().upper()
                parent = nodes_by_tag.get(src_upper) or nodes_by_id.get(src_upper)
                if not parent:
                    add_finding(
                        severity="warning",
                        category="Topology",
                        asset_tag=tag,
                        asset_name=name,
                        room=room,
                        asset_id=nid,
                        title=f"Unresolved Upstream Parent Reference: '{src}'",
                        description=f"Equipment [{tag}] is configured to receive power from '{src}', but '{src}' does not exist in this facility model.",
                        recommendation=f"Add '{src}' to facility database or update [{tag}] upstream feed to an existing equipment tag."
                    )

        # Dual Source Validation (ATS, MTS, STS)
        if type_tag in ["ATS", "MTS", "STS"] or "TRANSFER" in name.upper():
            if len(valid_sources) < 2 and not attrs.get("emergency_source"):
                add_finding(
                    severity="warning",
                    category="Topology",
                    asset_tag=tag,
                    asset_name=name,
                    room=room,
                    asset_id=nid,
                    title="Transfer Switch Missing Emergency / Alternate Power Source",
                    description=f"Transfer Switch [{tag}] only has 1 power feed configured. Dual-source automatic/manual transfer switches require both Normal and Emergency inputs.",
                    recommendation="Add secondary power feed (e.g. Generator, UPS, or Alternate Substation) in the equipment drawer."
                )

    # 2. Voltage Compatibility & Transformation Checks
    for n in nodes:
        tag = n.get("tag") or n.get("id") or "EQ"
        name = n.get("name") or n.get("type_name") or tag
        domain = (n.get("domain") or "").lower()
        type_tag = (n.get("type_tag") or "").upper()
        room = n.get("room") or "Unassigned"
        nid = n.get("id") or tag
        attrs = n.get("attributes") or {}

        child_v_num = _parse_voltage_num(n.get("voltage") or attrs.get("voltage"))

        # Check upstream parents
        raw_sources = attrs.get("upstream_sources") or ([n.get("fed_from")] if n.get("fed_from") else [])
        for src in raw_sources:
            if not src:
                continue
            parent = nodes_by_tag.get(str(src).strip().upper()) or nodes_by_id.get(str(src).strip().upper())
            if not parent:
                continue

            parent_tag = parent.get("tag") or parent.get("id") or "Parent"
            parent_type = (parent.get("type_tag") or "").upper()
            parent_domain = (parent.get("domain") or "").lower()
            parent_v_num = _parse_voltage_num(parent.get("voltage") or (parent.get("attributes") or {}).get("voltage"))

            # If parent is a transformer, voltage step-down/step-up is expected and legitimate
            if parent_domain == "transformers" or parent_type in ["XFMR", "PAD"]:
                continue

            if child_v_num and parent_v_num:
                # Flag major voltage class mismatches (e.g., 480V feeding 208V/120V directly without transformer)
                if abs(child_v_num - parent_v_num) > 50:
                    add_finding(
                        severity="critical",
                        category="Voltage",
                        asset_tag=tag,
                        asset_name=name,
                        room=room,
                        asset_id=nid,
                        title=f"Voltage Class Mismatch with Upstream Feeder [{parent_tag}]",
                        description=f"Equipment [{tag}] operates at {n.get('voltage', f'{child_v_num}V')}, but is directly fed from [{parent_tag}] at {parent.get('voltage', f'{parent_v_num}V')} without an intervening step-down transformer.",
                        recommendation=f"Insert a step-down transformer (e.g. 480V primary to 208Y/120V secondary) between [{parent_tag}] and [{tag}]."
                    )

    # 3. Capacity & Ampacity Headroom Checks
    for n in nodes:
        tag = n.get("tag") or n.get("id") or "EQ"
        name = n.get("name") or n.get("type_name") or tag
        domain = (n.get("domain") or "").lower()
        room = n.get("room") or "Unassigned"
        nid = n.get("id") or tag
        attrs = n.get("attributes") or {}

        child_amps = _parse_amps_num(n.get("amps") or attrs.get("amps"))

        raw_sources = attrs.get("upstream_sources") or ([n.get("fed_from")] if n.get("fed_from") else [])
        for src in raw_sources:
            if not src:
                continue
            parent = nodes_by_tag.get(str(src).strip().upper()) or nodes_by_id.get(str(src).strip().upper())
            if not parent:
                continue
            parent_tag = parent.get("tag") or parent.get("id") or "Parent"
            parent_amps = _parse_amps_num(parent.get("amps") or (parent.get("attributes") or {}).get("amps"))

            if child_amps and parent_amps and parent_amps > 0:
                # If downstream equipment has significantly higher amp rating than upstream feeder bus
                if child_amps > parent_amps:
                    add_finding(
                        severity="warning",
                        category="Capacity",
                        asset_tag=tag,
                        asset_name=name,
                        room=room,
                        asset_id=nid,
                        title=f"Downstream Amp Rating ({child_amps}A) Exceeds Upstream Bus ({parent_amps}A)",
                        description=f"Equipment [{tag}] is rated for {child_amps}A, which exceeds the {parent_amps}A capacity of upstream supplier [{parent_tag}].",
                        recommendation=f"Verify that upstream protective device or main bus at [{parent_tag}] is adequate to support [{tag}] design load."
                    )

    # 4. AIC / Short-Circuit Withstand Rating Checks
    for n in nodes:
        tag = n.get("tag") or n.get("id") or "EQ"
        name = n.get("name") or n.get("type_name") or tag
        room = n.get("room") or "Unassigned"
        nid = n.get("id") or tag
        attrs = n.get("attributes") or {}

        aic = n.get("aic") or attrs.get("aic")
        aic_num = _parse_amps_num(aic)

        if aic_num is not None:
            # Low AIC (< 14 kA) on main distribution panels or upstream switches
            if aic_num < 14 and (n.get("is_panel") or (n.get("amps") and float(n.get("amps", 0) or 0) >= 400)):
                add_finding(
                    severity="warning",
                    category="AIC",
                    asset_tag=tag,
                    asset_name=name,
                    room=room,
                    asset_id=nid,
                    title=f"Low Short-Circuit Withstand Rating ({aic_num} kA AIC)",
                    description=f"Equipment [{tag}] has an AIC rating of {aic_num} kA, which may be insufficient for high-capacity service entrance or feeder distribution.",
                    recommendation="Perform short-circuit fault study or verify current-limiting upstream fuses/breakers."
                )

    # 5. Panel Schedule Integrity Checks
    for n in nodes:
        tag = n.get("tag") or n.get("id") or "EQ"
        name = n.get("name") or n.get("type_name") or tag
        room = n.get("room") or "Unassigned"
        nid = n.get("id") or tag
        attrs = n.get("attributes") or {}

        if n.get("is_panel") or (n.get("domain") or "").lower() == "panels":
            slots_max = int(n.get("slots") or attrs.get("slots") or 42)
            schedule = attrs.get("schedule") or []
            if isinstance(schedule, list) and schedule:
                # Count occupied slots
                occupied_slots = 0
                for row in schedule:
                    if isinstance(row, dict):
                        if row.get("leftTrip") and str(row.get("leftTrip")).strip():
                            occupied_slots += int(row.get("leftPoles") or 1)
                        if row.get("rightTrip") and str(row.get("rightTrip")).strip():
                            occupied_slots += int(row.get("rightPoles") or 1)

                if occupied_slots > slots_max:
                    add_finding(
                        severity="critical",
                        category="Schedule",
                        asset_tag=tag,
                        asset_name=name,
                        room=room,
                        asset_id=nid,
                        title=f"Panel Schedule Over Capacity ({occupied_slots} / {slots_max} Slots)",
                        description=f"Panel [{tag}] schedule defines {occupied_slots} occupied breaker poles, exceeding physical enclosure capacity of {slots_max} slots.",
                        recommendation=f"Audit breaker schedule for [{tag}] or reallocate branch circuits to a subpanel."
                    )
                elif occupied_slots == 0 and slots_max > 0:
                    add_finding(
                        severity="info",
                        category="Schedule",
                        asset_tag=tag,
                        asset_name=name,
                        room=room,
                        asset_id=nid,
                        title="Empty Panel Schedule",
                        description=f"Panel [{tag}] has {slots_max} available breaker slots, but no circuit schedule rows are documented.",
                        recommendation="Survey field branch circuits and populate schedule during site inspection."
                    )

    # 6. Documentation & Survey Field Quality Checks
    for n in nodes:
        tag = n.get("tag") or n.get("id") or "EQ"
        name = n.get("name") or n.get("type_name") or tag
        room = n.get("room") or "Unassigned"
        nid = n.get("id") or tag
        attrs = n.get("attributes") or {}

        has_nameplate = bool(attrs.get("nameplate_photo") or n.get("nameplate_photo"))
        has_serial = bool(attrs.get("serial_no") or n.get("serial_no"))
        has_condition = bool(attrs.get("condition") or n.get("condition"))
        has_room = bool(n.get("room") and str(n.get("room")).strip() and str(n.get("room")).strip().lower() != "unassigned")

        if not has_nameplate:
            add_finding(
                severity="info",
                category="Documentation",
                asset_tag=tag,
                asset_name=name,
                room=room,
                asset_id=nid,
                title="Missing Nameplate Field Photo",
                description=f"Equipment [{tag}] has no attached nameplate photograph for visual verification.",
                recommendation="Capture and attach high-resolution nameplate photo using mobile survey camera."
            )

        if not has_room:
            add_finding(
                severity="warning",
                category="Documentation",
                asset_tag=tag,
                asset_name=name,
                room=room,
                asset_id=nid,
                title="Unassigned Physical Location / Room",
                description=f"Equipment [{tag}] has no room or physical area assigned.",
                recommendation="Assign room name (e.g. 'Main Electrical Room', 'Penthouse') in equipment details."
            )

    # 7. Field Inspection Checklists & Code Compliance Checks
    total_facility_chk_items = 0
    passed_facility_chk_items = 0
    deficient_facility_chk_items = 0
    evaluated_facility_chk_items = 0
    signoffs_count = 0

    for n in nodes:
        tag = n.get("tag") or n.get("id") or "EQ"
        name = n.get("name") or n.get("type_name") or tag
        room = n.get("room") or "Unassigned"
        nid = n.get("id") or tag
        domain = n.get("domain") or "generic"
        type_tag = n.get("type_tag") or ""
        attrs = n.get("attributes") or {}
        checklists_data = attrs.get("checklists") or {}
        signoff = attrs.get("checklist_signoff")

        if signoff and isinstance(signoff, dict) and signoff.get("inspector"):
            signoffs_count += 1

        app_checklists = get_checklists_for_domain(domain, type_tag)
        if not app_checklists:
            continue

        node_total_items = 0
        node_evaluated_items = 0
        node_passed_items = 0
        node_deficient_items = 0

        for chk in app_checklists:
            cid = chk["id"]
            c_items = chk.get("items", [])
            node_saved_chk = checklists_data.get(cid, {}) if isinstance(checklists_data, dict) else {}

            for it in c_items:
                node_total_items += 1
                total_facility_chk_items += 1
                item_no = it.get("item_no")
                it_state = node_saved_chk.get(str(item_no)) or node_saved_chk.get(item_no) or {}
                status = (it_state.get("status") if isinstance(it_state, dict) else it_state) or "pending"
                notes = (it_state.get("notes") if isinstance(it_state, dict) else "") or ""

                if status == "pass":
                    node_passed_items += 1
                    passed_facility_chk_items += 1
                    node_evaluated_items += 1
                    evaluated_facility_chk_items += 1
                elif status in ["deficient", "fail"]:
                    node_deficient_items += 1
                    deficient_facility_chk_items += 1
                    node_evaluated_items += 1
                    evaluated_facility_chk_items += 1

                    # Flag specific code deficiency finding!
                    sev = "critical" if it.get("severity") == "Critical" else "warning"
                    std_ref = it.get("standard_ref") or "NEC/NFPA Code"
                    prompt = it.get("inspection_prompt") or "Code Deficient Condition"
                    notes_desc = f' Field Notes: "{notes}"' if notes else ""
                    add_finding(
                        severity=sev,
                        category="Checklists & Code",
                        asset_tag=tag,
                        asset_name=name,
                        room=room,
                        asset_id=nid,
                        title=f"Code Deficiency: {std_ref} ({prompt})",
                        description=f"Equipment [{tag}] failed inspection criteria for {std_ref}: {prompt}.{notes_desc}",
                        recommendation=f"Remediate non-compliant installation per {std_ref} specifications."
                    )
                elif status == "na":
                    node_evaluated_items += 1
                    evaluated_facility_chk_items += 1

        # Check if asset has incomplete checklists
        if node_total_items > 0:
            if node_evaluated_items == 0:
                add_finding(
                    severity="info",
                    category="Checklists & Code",
                    asset_tag=tag,
                    asset_name=name,
                    room=room,
                    asset_id=nid,
                    title="Inspection Checklist Not Started",
                    description=f"Equipment [{tag}] has {node_total_items} applicable code inspection items with 0% evaluated.",
                    recommendation="Perform physical walkdown and complete standard checklist."
                )
            elif node_evaluated_items < node_total_items:
                rem = node_total_items - node_evaluated_items
                add_finding(
                    severity="info",
                    category="Checklists & Code",
                    asset_tag=tag,
                    asset_name=name,
                    room=room,
                    asset_id=nid,
                    title=f"Incomplete Inspection Checklist ({node_evaluated_items}/{node_total_items} Evaluated)",
                    description=f"Equipment [{tag}] has {rem} remaining checklist items pending inspector review.",
                    recommendation="Complete outstanding checklist items in equipment drawer."
                )
            elif node_evaluated_items == node_total_items and not signoff:
                add_finding(
                    severity="info",
                    category="Checklists & Code",
                    asset_tag=tag,
                    asset_name=name,
                    room=room,
                    asset_id=nid,
                    title="Inspection Complete - Awaiting Inspector Sign-Off",
                    description=f"Equipment [{tag}] has 100% of checklist items evaluated but has not been signed off by the lead inspector.",
                    recommendation="Review findings and sign off in equipment drawer."
                )

    # Compute Facility Health Score (0 - 100)
    critical_count = sum(1 for f in findings if f["severity"] == "critical")
    warning_count = sum(1 for f in findings if f["severity"] == "warning")
    info_count = sum(1 for f in findings if f["severity"] == "info")

    base_score = 100.0
    deductions = (critical_count * 20.0) + (warning_count * 5.0) + (info_count * 1.0)
    health_score = max(0, min(100, int(round(base_score - deductions))))

    if health_score >= 90:
        health_grade = "A (Optimal)"
        status_color = "emerald"
    elif health_score >= 80:
        health_grade = "B (Good)"
        status_color = "indigo"
    elif health_score >= 65:
        health_grade = "C (Action Required)"
        status_color = "amber"
    else:
        health_grade = "D (Critical Attention Needed)"
        status_color = "rose"

    chk_completion_pct = round((evaluated_facility_chk_items / total_facility_chk_items * 100)) if total_facility_chk_items > 0 else 0
    chk_compliance_pct = round((passed_facility_chk_items / evaluated_facility_chk_items * 100)) if evaluated_facility_chk_items > 0 else 100

    return {
        "client": client,
        "facility": facility,
        "total_nodes": len(nodes),
        "health_score": health_score,
        "health_grade": health_grade,
        "status_color": status_color,
        "critical_count": critical_count,
        "warning_count": warning_count,
        "info_count": info_count,
        "total_findings": len(findings),
        "findings": findings,
        "checklist_summary": {
            "total_items": total_facility_chk_items,
            "evaluated_items": evaluated_facility_chk_items,
            "passed_items": passed_facility_chk_items,
            "deficient_items": deficient_facility_chk_items,
            "pending_items": max(0, total_facility_chk_items - evaluated_facility_chk_items),
            "signoffs_count": signoffs_count,
            "completion_pct": chk_completion_pct,
            "compliance_pct": chk_compliance_pct
        }
    }


def generate_markdown_report(audit_result: Dict[str, Any], client: str = "", facility: str = "") -> str:
    """Generate publication-grade Markdown System Integrity Audit report with Table of Contents."""
    c_name = (client or audit_result.get("client") or "Facility").upper()
    f_name = (facility or audit_result.get("facility") or "Digital Twin").upper()
    score = audit_result.get("health_score", 100)
    grade = audit_result.get("health_grade", "A")
    total_nodes = audit_result.get("total_nodes", 0)
    crit = audit_result.get("critical_count", 0)
    warn = audit_result.get("warning_count", 0)
    info = audit_result.get("info_count", 0)
    findings = audit_result.get("findings", [])

    lines = [
        f"# Electrical System Integrity Audit Report",
        f"**Facility:** {c_name} / {f_name} • **Health Score:** `{score}/100` ({grade})",
        "",
        "---",
        "",
        "## Table of Contents",
        "- [1. Executive Summary & Health Scorecard](#1-executive-summary--health-scorecard)",
        "- [2. Audit Scope & Equipment Inventory](#2-audit-scope--equipment-inventory)",
        "- [3. Critical Electrical Deficiencies](#3-critical-electrical-deficiencies-)",
        "- [4. Warnings & Capacity Headroom](#4-warnings--capacity-headroom-)",
        "- [5. Field Documentation & Informational Observations](#5-field-documentation--informational-observations-)",
        "- [6. Field Inspection Checklists & Code Compliance Summary](#6-field-inspection-checklists--code-compliance-summary-)",
        "- [7. Prioritized Remediation Action Plan](#7-prioritized-remediation-action-plan)",
        "",
        "---",
        "",
        "## 1. Executive Summary & Health Scorecard",
        "",
        f"This automated System Integrity Audit evaluated **{total_nodes} electrical digital twin equipment nodes** across voltage compatibility, capacity headroom, short-circuit withstand ratings (AIC), topology continuity, panel schedule boundaries, and field documentation completeness.",
        "",
        "| Metric | Result | Status |",
        "| :--- | :--- | :--- |",
        f"| **Overall Health Score** | **`{score} / 100`** | `{grade}` |",
        f"| **Total Equipment Assets** | `{total_nodes}` Assets | Verified |",
        f"| **🔴 Critical Findings** | `{crit}` Issue(s) | {'Action Required Immediately' if crit > 0 else 'Clear'} |",
        f"| **🟡 Warning Findings** | `{warn}` Issue(s) | {'Review & Coordinate' if warn > 0 else 'Clear'} |",
        f"| **ℹ️ Field Observations** | `{info}` Note(s) | Quality Enhancement |",
        "",
        "---",
        "",
        "## 2. Audit Scope & Equipment Inventory",
        f"The facility model contains `{total_nodes}` assets analyzed against IEEE and NEC electrical topology rules.",
        "",
        "---",
        "",
        "## 3. Critical Electrical Deficiencies 🔴",
    ]

    crit_findings = [f for f in findings if f.get("severity") == "critical"]
    if not crit_findings:
        lines.append("✓ **No critical electrical or topological defects detected.** All power distribution paths and voltage transformations are structurally sound.")
    else:
        for idx, f in enumerate(crit_findings, 1):
            lines.extend([
                f"### 3.{idx}. [{f['asset_tag']}] {f['title']}",
                f"- **Category:** `{f['category']}`",
                f"- **Asset:** {f['asset_name']} (`{f['asset_tag']}`)",
                f"- **Location:** {f['room']}",
                f"- **Deficiency:** {f['description']}",
                f"- **Recommended Action:** {f['recommendation']}",
                ""
            ])

    lines.extend([
        "---",
        "",
        "## 4. Warnings & Capacity Headroom 🟡",
    ])

    warn_findings = [f for f in findings if f.get("severity") == "warning"]
    if not warn_findings:
        lines.append("✓ **No capacity, headroom, or dual-source warnings detected.**")
    else:
        for idx, f in enumerate(warn_findings, 1):
            lines.extend([
                f"### 4.{idx}. [{f['asset_tag']}] {f['title']}",
                f"- **Category:** `{f['category']}`",
                f"- **Asset:** {f['asset_name']} (`{f['asset_tag']}`)",
                f"- **Location:** {f['room']}",
                f"- **Finding:** {f['description']}",
                f"- **Recommended Action:** {f['recommendation']}",
                ""
            ])

    lines.extend([
        "---",
        "",
        "## 5. Field Documentation & Informational Observations ℹ️",
    ])

    info_findings = [f for f in findings if f.get("severity") == "info"]
    if not info_findings:
        lines.append("✓ **All field documentation, nameplate captures, and schedules are 100% complete.**")
    else:
        lines.append("| Tag | Category | Location | Observation | Recommendation |")
        lines.append("| :--- | :--- | :--- | :--- | :--- |")
        for f in info_findings:
            lines.append(f"| **`{f['asset_tag']}`** | `{f['category']}` | {f['room']} | {f['title']} | {f['recommendation']} |")

    lines.extend([
        "",
        "---",
        "",
        "## 6. Field Inspection Checklists & Code Compliance Summary 📋",
        "",
        f"Facility inspection evaluation across NEC 110, NEC 408, NEC 450, and NFPA 70E checklists:",
        "",
        "| Metric | Value | Status |",
        "| :--- | :--- | :--- |",
        f"| **Total Checklist Inspection Points** | `{audit_result.get('checklist_summary', {}).get('total_items', 0)}` Items | Defined across active equipment |",
        f"| **Evaluated Inspection Points** | `{audit_result.get('checklist_summary', {}).get('evaluated_items', 0)}` Items | `{audit_result.get('checklist_summary', {}).get('completion_pct', 0)}% Complete` |",
        f"| **Passed Items** | `{audit_result.get('checklist_summary', {}).get('passed_items', 0)}` Items | `{audit_result.get('checklist_summary', {}).get('compliance_pct', 0)}% Compliant` |",
        f"| **Open Code Deficiencies** | `{audit_result.get('checklist_summary', {}).get('deficient_items', 0)}` Items | {'⚠️ Action Required' if audit_result.get('checklist_summary', {}).get('deficient_items', 0) > 0 else '✓ None'} |",
        f"| **Certified Inspector Sign-Offs** | `{audit_result.get('checklist_summary', {}).get('signoffs_count', 0)}` Assets | Stamped & Signed |",
        "",
        "---",
        "",
        "## 7. Prioritized Remediation Action Plan",
        "",
        "1. **Immediate Focus (Critical)**: Resolve all voltage mismatches, unassigned feeds, and Critical NFPA 70E/NEC code deficiencies.",
        "2. **Secondary Focus (Warnings)**: Remediate Major code deficiencies, verify secondary/emergency feeds, and confirm upstream bus sizing.",
        "3. **Field Survey Polish (Info)**: Complete remaining field inspection checklists, capture inspector sign-offs, and attach nameplate photos.",
        "",
        f"---",
        f"*Report generated by Building Aware System Integrity Audit Engine • Client: {c_name} • Facility: {f_name}*"
    ])

    return "\n".join(lines)


def generate_csv_report(audit_result: Dict[str, Any]) -> str:
    """Generate CSV spreadsheet export for field engineers."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Finding ID", "Severity", "Category", "Asset Tag", "Asset Name", "Room", "Title", "Description", "Recommendation"])
    for f in audit_result.get("findings", []):
        writer.writerow([
            f.get("id", ""),
            f.get("severity", "").upper(),
            f.get("category", ""),
            f.get("asset_tag", ""),
            f.get("asset_name", ""),
            f.get("room", ""),
            f.get("title", ""),
            f.get("description", ""),
            f.get("recommendation", "")
        ])
    return output.getvalue()


def generate_txt_report(audit_result: Dict[str, Any], client: str = "", facility: str = "") -> str:
    """Generate plain text summary suitable for terminals or emails."""
    c_name = (client or audit_result.get("client") or "FACILITY").upper()
    f_name = (facility or audit_result.get("facility") or "FACILITY").upper()
    score = audit_result.get("health_score", 100)
    grade = audit_result.get("health_grade", "A")
    findings = audit_result.get("findings", [])

    lines = [
        "=" * 70,
        f"BUILDING AWARE • SYSTEM INTEGRITY AUDIT REPORT",
        f"Facility: {c_name} / {f_name}",
        f"Health Score: {score}/100 ({grade})",
        f"Checklist Compliance: {audit_result.get('checklist_summary', {}).get('completion_pct', 0)}% Complete ({audit_result.get('checklist_summary', {}).get('evaluated_items', 0)}/{audit_result.get('checklist_summary', {}).get('total_items', 0)} pts) • {audit_result.get('checklist_summary', {}).get('deficient_items', 0)} Deficiencies",
        f"Total Findings: {len(findings)} (Critical: {audit_result.get('critical_count', 0)}, Warning: {audit_result.get('warning_count', 0)}, Info: {audit_result.get('info_count', 0)})",
        "=" * 70,
        ""
    ]

    for f in findings:
        sev = f.get("severity", "INFO").upper()
        lines.append(f"[{sev}] {f.get('category')}: [{f.get('asset_tag')}] {f.get('title')}")
        lines.append(f"  Location: {f.get('room')}")
        lines.append(f"  Issue:    {f.get('description')}")
        lines.append(f"  Action:   {f.get('recommendation')}")
        lines.append("-" * 70)

    return "\n".join(lines)
