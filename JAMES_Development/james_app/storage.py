"""Local JSON File Storage Manager for Projects."""

import json
from pathlib import Path
from typing import List, Optional

from james_app.models import Project

# Base directory for storing projects
BASE_DIR = Path(__file__).resolve().parent.parent
PROJECTS_DIR = BASE_DIR / "data" / "projects"


def ensure_storage_dir() -> None:
    """Ensure the projects data directory exists."""
    PROJECTS_DIR.mkdir(parents=True, exist_ok=True)


def get_project_path(project_id: str) -> Path:
    """Return file path for a given project ID."""
    return PROJECTS_DIR / f"{project_id}.json"


def save_project(project: Project) -> Path:
    """Save a Project object as a JSON file."""
    ensure_storage_dir()
    file_path = get_project_path(project.project_id)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(project.model_dump_json(indent=2))
    return file_path


def load_project(project_id: str) -> Optional[Project]:
    """Load a Project object by project_id."""
    file_path = get_project_path(project_id)
    if not file_path.exists():
        return None
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return Project.model_validate(data)


def list_projects() -> List[str]:
    """List all available project IDs."""
    ensure_storage_dir()
    return [p.stem for p in PROJECTS_DIR.glob("*.json")]
