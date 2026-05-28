"""file_placement_checker — détection de fichiers mal placés dans le vault PKA_JCH."""

import re
from pathlib import Path

_EXCLUDED_DIRS = {".obsidian", "__pycache__", "node_modules", ".git"}

_DAILY_NOTE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}_")


def _is_excluded(path: Path, root: Path) -> bool:
    """Return True if any component of the path relative to root is in the excluded set."""
    try:
        rel = path.relative_to(root)
    except ValueError:
        return False
    return any(part in _EXCLUDED_DIRS for part in rel.parts)


def check(root: Path) -> list[dict]:
    """Retourne la liste des anomalies de placement.

    Chaque anomalie : {"path": str, "description": str, "expected": str}
    """
    anomalies: list[dict] = []

    for file in root.rglob("*"):
        if not file.is_file():
            continue
        if _is_excluded(file, root):
            continue

        rel = file.relative_to(root)
        parts = rel.parts  # tuple of path components

        # Rule 1 — daily note (.md with YYYY-MM-DD_ prefix) must be in JCH_Inbox/01_DASHBOARDS/
        if file.suffix == ".md" and _DAILY_NOTE_PATTERN.match(file.name):
            # Correct location: parts[0] == "JCH_Inbox", parts[1] == "01_DASHBOARDS"
            if not (len(parts) >= 3 and parts[0] == "JCH_Inbox" and parts[1] == "01_DASHBOARDS"):
                anomalies.append({
                    "path": str(rel),
                    "description": "Daily notes hors 01_DASHBOARDS",
                    "expected": "JCH_Inbox/01_DASHBOARDS/",
                })
                continue

        # Rule 2 — .py files must be under scripts/
        elif file.suffix == ".py":
            if parts[0] != "scripts":
                anomalies.append({
                    "path": str(rel),
                    "description": "Fichier .py hors scripts/",
                    "expected": "scripts/",
                })
                continue

        # Rule 3 — .plist files must be under scripts/launchd/
        elif file.suffix == ".plist":
            if not (len(parts) >= 3 and parts[0] == "scripts" and parts[1] == "launchd"):
                anomalies.append({
                    "path": str(rel),
                    "description": "Fichier .plist hors scripts/launchd/",
                    "expected": "scripts/launchd/",
                })
                continue

        # Rule 4 — no file directly at the root of JCH_Inbox/ (depth must be > 1 inside inbox)
        if len(parts) == 2 and parts[0] == "JCH_Inbox":
            anomalies.append({
                "path": str(rel),
                "description": "Fichier directement à la racine de JCH_Inbox/",
                "expected": "Sous-dossier de JCH_Inbox/",
            })

    return anomalies
