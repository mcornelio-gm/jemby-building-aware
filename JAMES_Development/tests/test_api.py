"""Integration tests for FastAPI endpoints."""

from fastapi.testclient import TestClient
from james_app.main import app

client = TestClient(app)


def test_root_redirect():
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 373 or response.status_code == 307
    assert response.headers["location"] == "/survey"


def test_get_project_workspace():
    response = client.get("/projects/zoetis_b4")
    assert response.status_code == 200
    assert "Zoetis Building 4 - Power Distribution" in response.text
    assert "d3-graphviz" in response.text


def test_api_get_catalog():
    response = client.get("/api/catalog")
    assert response.status_code == 200
    data = response.json()
    assert "SWBD" in data
    assert "XFMR" in data


def test_api_get_project_dot():
    response = client.get("/api/projects/zoetis_b4/dot")
    assert response.status_code == 200
    assert "digraph SLD {" in response.text
    assert "SWBD_MSA" in response.text


def test_get_node_form():
    response = client.get("/api/projects/zoetis_b4/nodes/SWBD_MSA/form")
    assert response.status_code == 200
    assert "SWBD-MSA" in response.text
    assert "bus_amps" in response.text


def test_update_node_attributes():
    response = client.post(
        "/api/projects/zoetis_b4/nodes/SWBD_MSA",
        data={"label": "SWBD-MSA-UPDATED", "field_bus_amps": "2500", "field_voltage": "480/277V"}
    )
    assert response.status_code == 200
    assert "refreshDiagram" in response.headers.get("HX-Trigger", "")
    assert "SWBD-MSA-UPDATED" in response.text

    # Re-fetch DOT to ensure DOT compilation reflects update
    dot_res = client.get("/api/projects/zoetis_b4/dot")
    assert "SWBD-MSA-UPDATED (2500A, 480/277V)" in dot_res.text


def test_create_and_delete_edge():
    # Create edge
    res_create = client.post(
        "/api/projects/zoetis_b4/edges",
        data={
            "from_node": "UTIL",
            "from_port": "out",
            "to_node": "ATS_1",
            "to_port": "emerg",
            "breaker": "CB-EMERG-600A"
        }
    )
    assert res_create.status_code == 200
    assert "refreshDiagram" in res_create.headers.get("HX-Trigger", "")

    # Check DOT for new edge
    dot_res = client.get("/api/projects/zoetis_b4/dot")
    assert "UTIL:out -> ATS_1:emerg" in dot_res.text
