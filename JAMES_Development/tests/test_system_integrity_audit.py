"""Unit and integration tests for System Integrity Audit Engine and Export Generators."""

import pytest
from fastapi.testclient import TestClient

from james_app.integrity_audit import (
    audit_facility_system_integrity,
    generate_markdown_report,
    generate_csv_report,
    generate_txt_report
)
from james_app.main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_voltage_mismatch_detection():
    nodes = [
        {"id": "swbd_1", "tag": "MSB-1", "name": "Main Switchboard", "domain": "switches", "type_tag": "SWBD", "voltage": "480Y/277V", "amps": 2000},
        {"id": "pnl_1", "tag": "LP-1", "name": "Lighting Panel", "domain": "panels", "type_tag": "LP", "voltage": "208Y/120V", "amps": 225, "fed_from": "MSB-1"},
    ]
    audit = audit_facility_system_integrity(nodes)
    crit_findings = [f for f in audit["findings"] if f["severity"] == "critical" and f["category"] == "Voltage"]
    assert len(crit_findings) >= 1
    assert "Voltage Class Mismatch" in crit_findings[0]["title"]
    assert crit_findings[0]["asset_tag"] == "LP-1"


def test_transformer_step_down_is_valid():
    nodes = [
        {"id": "swbd_1", "tag": "MSB-1", "name": "Main Switchboard", "domain": "switches", "type_tag": "SWBD", "voltage": "480Y/277V", "amps": 2000},
        {"id": "xfmr_1", "tag": "XFMR-1", "name": "Step Down Transformer", "domain": "transformers", "type_tag": "XFMR", "voltage": "480V-208V", "amps": 150, "fed_from": "MSB-1"},
        {"id": "pnl_1", "tag": "LP-1", "name": "Lighting Panel", "domain": "panels", "type_tag": "LP", "voltage": "208Y/120V", "amps": 225, "fed_from": "XFMR-1"},
    ]
    audit = audit_facility_system_integrity(nodes)
    voltage_mismatches = [f for f in audit["findings"] if f["category"] == "Voltage"]
    assert len(voltage_mismatches) == 0


def test_orphaned_node_detection():
    nodes = [
        {"id": "util_1", "tag": "UTIL-1", "name": "Utility Grid", "domain": "sources", "type_tag": "UTIL", "voltage": "480V", "amps": 2000},
        {"id": "pnl_1", "tag": "LP-1", "name": "Isolated Panel", "domain": "panels", "type_tag": "LP", "voltage": "208V", "amps": 225, "fed_from": ""},
    ]
    audit = audit_facility_system_integrity(nodes)
    orphan_findings = [f for f in audit["findings"] if "Orphaned" in f["title"]]
    assert len(orphan_findings) >= 1
    assert orphan_findings[0]["asset_tag"] == "LP-1"


def test_transfer_switch_dual_source_warning():
    nodes = [
        {"id": "util_1", "tag": "UTIL-1", "name": "Utility Grid", "domain": "sources", "type_tag": "UTIL", "voltage": "480V", "amps": 2000},
        {"id": "ats_1", "tag": "ATS-1", "name": "Automatic Transfer Switch", "domain": "switches", "type_tag": "ATS", "voltage": "480V", "amps": 800, "fed_from": "UTIL-1"},
    ]
    audit = audit_facility_system_integrity(nodes)
    ats_warnings = [f for f in audit["findings"] if "Transfer Switch Missing Emergency" in f["title"]]
    assert len(ats_warnings) >= 1
    assert ats_warnings[0]["asset_tag"] == "ATS-1"


def test_panel_schedule_overcapacity():
    # Schedule with 44 occupied poles in a 42-slot panel
    schedule = [{"leftTrip": 20, "leftPoles": 1, "rightTrip": 20, "rightPoles": 1} for _ in range(22)]
    nodes = [
        {"id": "pnl_1", "tag": "LP-1", "name": "Lighting Panel", "domain": "panels", "type_tag": "LP", "is_panel": True, "slots": 42, "attributes": {"schedule": schedule}},
    ]
    audit = audit_facility_system_integrity(nodes)
    sched_crit = [f for f in audit["findings"] if f["category"] == "Schedule" and f["severity"] == "critical"]
    assert len(sched_crit) >= 1
    assert "Panel Schedule Over Capacity" in sched_crit[0]["title"]


def test_markdown_report_generation():
    nodes = [
        {"id": "util_1", "tag": "UTIL-1", "name": "Utility Grid", "domain": "sources", "type_tag": "UTIL", "voltage": "480V", "amps": 2000, "room": "Main Substation"},
        {"id": "pnl_1", "tag": "LP-1", "name": "Lighting Panel", "domain": "panels", "type_tag": "LP", "voltage": "208V", "amps": 225, "fed_from": "UTIL-1", "room": "Electrical Room 101"},
    ]
    audit = audit_facility_system_integrity(nodes, client="zoetis", facility="b4")
    md = generate_markdown_report(audit, client="zoetis", facility="b4")

    # Verify Table of Contents is present and formatted
    assert "## Table of Contents" in md
    assert "[1. Executive Summary & Health Scorecard]" in md
    assert "[2. Audit Scope & Equipment Inventory]" in md
    assert "[3. Critical Electrical Deficiencies" in md
    assert "[4. Warnings & Capacity Headroom" in md
    assert "[5. Field Documentation & Informational Observations" in md
    assert "[6. Prioritized Remediation Action Plan]" in md
    assert "ZOETIS" in md
    assert "B4" in md


def test_csv_and_txt_report_generation():
    nodes = [
        {"id": "pnl_1", "tag": "LP-1", "name": "Lighting Panel", "domain": "panels", "type_tag": "LP", "voltage": "208V", "amps": 225, "fed_from": ""},
    ]
    audit = audit_facility_system_integrity(nodes, client="zoetis", facility="b4")
    
    # CSV
    csv_out = generate_csv_report(audit)
    assert "Finding ID,Severity,Category,Asset Tag" in csv_out
    assert "LP-1" in csv_out

    # TXT
    txt_out = generate_txt_report(audit, client="zoetis", facility="b4")
    assert "BUILDING AWARE • SYSTEM INTEGRITY AUDIT REPORT" in txt_out
    assert "LP-1" in txt_out


def test_api_audit_endpoints(client):
    # 1. JSON API
    res = client.get("/api/clients/zoetis/facilities/b4/audit")
    assert res.status_code == 200
    data = res.json()
    assert "health_score" in data
    assert "health_grade" in data
    assert "findings" in data
    assert isinstance(data["findings"], list)

    # 2. Export Markdown (.md with TOC)
    res_md = client.get("/api/clients/zoetis/facilities/b4/audit/export?format=md")
    assert res_md.status_code == 200
    assert "## Table of Contents" in res_md.text
    assert "attachment; filename=" in res_md.headers.get("content-disposition", "")

    # 3. Export CSV
    res_csv = client.get("/api/clients/zoetis/facilities/b4/audit/export?format=csv")
    assert res_csv.status_code == 200
    assert "Finding ID,Severity,Category" in res_csv.text

    # 4. Export JSON
    res_json = client.get("/api/clients/zoetis/facilities/b4/audit/export?format=json")
    assert res_json.status_code == 200
    assert "health_score" in res_json.json()

    # 5. Export TXT
    res_txt = client.get("/api/clients/zoetis/facilities/b4/audit/export?format=txt")
    assert res_txt.status_code == 200
    assert "SYSTEM INTEGRITY AUDIT REPORT" in res_txt.text
