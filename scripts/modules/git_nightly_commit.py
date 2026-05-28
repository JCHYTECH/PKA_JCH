"""git_nightly_commit — staging et commit automatique du vault PKA.

Fonctions publiques :
    build_commit_message(date_str) -> str
    build_add_args() -> list[str]
    run(date_str, root, dry_run) -> dict
"""

from __future__ import annotations

import subprocess
from datetime import date
from pathlib import Path

ADD_PATHS = ["JCH_Inbox/", "TEAM/", "TEAM_Inbox/", "docs/", "scripts/"]

# Exclusions absolues — ne jamais commiter
_EXCLUDED = [
    "JCH_Inbox/99_SYSTEM/security/",
]


def build_commit_message(date_str: str) -> str:
    """Retourne 'chore(vault): nightly maintenance YYYY-MM-DD'."""
    return f"chore(vault): nightly maintenance {date_str}"


def build_add_args() -> list[str]:
    """Retourne la liste des chemins pour git add (sans security/)."""
    return [p for p in ADD_PATHS if p not in _EXCLUDED]


def _git_status_empty(root: Path) -> bool:
    """Retourne True si git status --porcelain ne retourne rien."""
    result = subprocess.run(
        ["git", "status", "--porcelain"],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip() == ""


def run(
    date_str: str | None = None,
    root: Path | None = None,
    dry_run: bool = False,
) -> dict:
    """Exécute git add + git commit.

    Retourne {"committed": bool, "reason"?: str, "date"?: str, "error"?: str}
    """
    if date_str is None:
        date_str = date.today().isoformat()

    if root is None:
        root = Path(__file__).resolve().parents[2]

    if _git_status_empty(root):
        return {"committed": False, "reason": "nothing_to_commit"}

    if dry_run:
        return {"committed": False, "reason": "dry_run", "would_commit": date_str}

    try:
        add_cmd = ["git", "add", "--"] + build_add_args() + [":(exclude)JCH_Inbox/99_SYSTEM/security/"]
        subprocess.run(
            add_cmd,
            cwd=root,
            check=True,
        )
        subprocess.run(
            ["git", "commit", "-m", build_commit_message(date_str)],
            cwd=root,
            check=True,
        )
    except subprocess.CalledProcessError as exc:
        return {"committed": False, "error": str(exc)}

    return {"committed": True, "date": date_str}
