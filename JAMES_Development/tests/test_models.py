"""Unit tests for Pydantic Models and Catalog."""

from james_app.catalog import get_catalog, get_equipment_schema
from james_app.models import Edge, Node, Project


def test_catalog_retrieval():
    catalog = get_catalog()
    assert "SWBD" in catalog
    assert "XFMR" in catalog
    assert "UTIL" in catalog
    
    swbd_schema = get_equipment_schema("SWBD")
    assert swbd_schema is not None
    assert swbd_schema["symbol_code"] == "SWBD"
    assert "bus_amps" in swbd_schema["fields"]


def test_node_model():
    node = Node(
        type="SWBD",
        label="SWBD-MSA",
        data={"bus_amps": 2000, "voltage": "480/277V"}
    )
    assert node.type == "SWBD"
    assert node.label == "SWBD-MSA"
    assert node.data["bus_amps"] == 2000


def test_edge_model():
    edge = Edge(
        id="edge_1",
        from_node="UTIL",
        from_port="out",
        to_node="XFMR_PGE",
        to_port="in",
        data={"fuse": "50E Fuse"}
    )
    assert edge.id == "edge_1"
    assert edge.from_node == "UTIL"
    assert edge.to_node == "XFMR_PGE"


def test_project_model():
    project = Project(
        project_id="test_proj",
        name="Test Project",
        nodes={
            "UTIL": Node(type="UTIL", label="Utility Grid", data={"voltage": "12kV"}),
            "XFMR": Node(type="XFMR", label="Transformer", data={"kva": 750})
        },
        edges=[
            Edge(id="e1", from_node="UTIL", from_port="out", to_node="XFMR", to_port="in")
        ]
    )
    assert project.project_id == "test_proj"
    assert len(project.nodes) == 2
    assert len(project.edges) == 1
