from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _projects_dir() -> Path:
    return ROOT / "JCH_Inbox" / "03_PROJECTS"


def build_manifest() -> dict:
    projects = []
    for item in sorted(_projects_dir().iterdir(), key=lambda path: path.name):
        if item.is_dir():
            projects.append({"key": item.name, "name": item.name})
    return {"projects": projects}
