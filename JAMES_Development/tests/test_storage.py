"""Unit tests for JSON Storage Manager."""

import tempfile
from pathlib import Path
from james_app.models import Node, Project
from james_app import storage


def test_storage_load_sample_project():
    project = storage.load_project("zoetis_b4")
    assert project is not None
    assert project.project_id == "zoetis_b4"
    assert "SWBD_MSA" in project.nodes
    assert len(project.edges) >= 3


def test_storage_save_and_load(monkeypatch):
    with tempfile.TemporaryDirectory() as tmp_dir:
        monkeypatch.setattr(storage, "PROJECTS_DIR", Path(tmp_dir))
        
        proj = Project(
            project_id="temp_proj",
            name="Temporary Project",
            nodes={"N1": Node(type="UTIL", label="Util Node", data={})},
            edges=[]
        )
        
        file_path = storage.save_project(proj)
        assert file_path.exists()
        
        loaded = storage.load_project("temp_proj")
        assert loaded is not None
        assert loaded.name == "Temporary Project"
        assert "N1" in loaded.nodes
        
        project_ids = storage.list_projects()
        assert "temp_proj" in project_ids
