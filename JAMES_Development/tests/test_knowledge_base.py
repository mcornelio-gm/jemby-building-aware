"""Tests for Build Aware SQLite FTS5 Knowledge Base & Ingestion Pipeline."""

import os
import tempfile
import pytest
from fastapi.testclient import TestClient

from james_app.main import app
from james_app.knowledge_base import KnowledgeBaseManager


@pytest.fixture
def temp_kb():
    """Create an isolated temporary Knowledge Base for tests."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
        db_path = tmp.name
    
    kb = KnowledgeBaseManager(db_path=db_path)
    yield kb
    
    if os.path.exists(db_path):
        os.remove(db_path)


def test_markdown_chunking_and_search(temp_kb):
    md_content = """# NEC Rules & Clearances

## Section 110.26 Working Space
Working space for equipment operating at 600 volts, nominal, or less to ground and likely to require examination, adjustment, servicing, or maintenance while energized shall comply with the dimensions of 110.26(A)(1). Minimum clear depth for 480V is 3.5 feet.

## Section 215.2 Feeder Sizing
Feeder conductors shall have an ampacity not less than the noncontinuous load plus 125 percent of the continuous load.
"""
    with tempfile.NamedTemporaryFile(suffix=".md", delete=False, mode="w", encoding="utf-8") as f:
        f.write(md_content)
        f_path = f.name

    try:
        count = temp_kb.ingest_file(f_path, category="nec_code")
        assert count == 2

        # 1. Search for working space clearance
        results = temp_kb.search("working space clearance 480V")
        assert len(results) >= 1
        top = results[0]
        assert "Working" in top["snippet"] and "110.26" in top["section_heading"]

        # 2. Search for feeder 125%
        feeder_results = temp_kb.search("feeder 125 percent continuous load")
        assert len(feeder_results) >= 1
        assert "215.2" in feeder_results[0]["section_heading"]

    finally:
        if os.path.exists(f_path):
            os.remove(f_path)


def test_html_parsing_and_search(temp_kb):
    html_content = """<!DOCTYPE html>
<html>
<head><title>Transformer Maintenance Guide</title></head>
<body>
  <h1>Transformer Field Survey</h1>
  <h2>Nameplate Data & kVA Calculation</h2>
  <p>To determine primary FLA on a 3-phase 480V transformer, divide kVA by (480 * 1.732).</p>
</body>
</html>"""
    with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w", encoding="utf-8") as f:
        f.write(html_content)
        f_path = f.name

    try:
        count = temp_kb.ingest_file(f_path, category="manuals")
        assert count >= 1

        results = temp_kb.search("transformer primary FLA 480V")
        assert len(results) >= 1
        assert "Transformer" in results[0]["title"]
    finally:
        if os.path.exists(f_path):
            os.remove(f_path)


def test_kb_api_endpoints():
    client = TestClient(app)

    # 1. Ingest ad-hoc text chunk via API
    ingest_payload = {
        "title": "Breaker AIC Selection Guide",
        "section_heading": "Interrupting Capacity Rules",
        "body_text": "Always verify available fault current at the bus before selecting 10kA, 22kA, or 65kA interrupting capacity breakers.",
        "category": "specs",
        "tags": "aic, breaker, fault_current"
    }
    res = client.post("/api/kb/ingest/text", json=ingest_payload)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"

    # 2. Query search API
    search_res = client.get("/api/kb/search?q=fault+current+aic+breaker")
    assert search_res.status_code == 200
    search_data = search_res.json()
    assert search_data["count"] >= 1
    assert any("AIC" in r["title"] or "Interrupting" in r["section_heading"] for r in search_data["results"])

    # 3. Check stats API
    stats_res = client.get("/api/kb/stats")
    assert stats_res.status_code == 200
    stats_data = stats_res.json()
    assert stats_data["total_chunks"] >= 1


def test_kb_view_file_inline():
    client = TestClient(app)

    # 1. Test viewing Arc Flash PDF
    pdf_res = client.get("/api/kb/view/QSG-Arc%20Flash%20Labeling.pdf")
    assert pdf_res.status_code == 200
    assert "application/pdf" in pdf_res.headers.get("content-type", "")
    assert 'inline; filename="QSG-Arc Flash Labeling.pdf"' in pdf_res.headers.get("content-disposition", "")
    assert len(pdf_res.content) > 1000

    # 2. Test 404 for non-existent file
    not_found_res = client.get("/api/kb/view/non_existent_document_12345.pdf")
    assert not_found_res.status_code == 404


def test_kb_web_viewer_html():
    client = TestClient(app)
    # 1. Test PDF viewer
    res = client.get("/kb/viewer/QSG-Arc%20Flash%20Labeling.pdf?page=4&title=Arc%20Flash%20Labeling")
    assert res.status_code == 200
    assert "text/html" in res.headers.get("content-type", "")
    assert "BUILD AWARE" in res.text
    assert "pdfjsLib" in res.text
    assert 'value="4"' in res.text

    # 2. Test Markdown document viewer
    md_res = client.get("/kb/viewer/main_distribution.md")
    assert md_res.status_code == 200
    assert "text/html" in md_res.headers.get("content-type", "")
    assert "marked.min.js" in md_res.text
    assert "Table of Contents" in md_res.text
    assert "Main Distribution Panel" in md_res.text

    # 3. Test /api/kb/view redirect to rich viewer for markdown
    view_res = client.get("/api/kb/view/main_distribution.md", follow_redirects=False)
    assert view_res.status_code == 303
    assert view_res.headers["location"] == "/kb/viewer/main_distribution.md"

    # 4. Test raw markdown retrieval with ?raw=1
    raw_res = client.get("/api/kb/view/main_distribution.md?raw=1")
    assert raw_res.status_code == 200
    assert "text/plain" in raw_res.headers.get("content-type", "")
    assert "# Object Specification: Main Distribution Panel" in raw_res.text



