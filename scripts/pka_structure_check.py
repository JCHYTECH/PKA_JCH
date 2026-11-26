#!/usr/bin/env python3
"""Validate file placement against directory purpose — prevent structural drift."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Known directory rules: (relative path, expected_name_patterns, disallowed_extensions)
# Files that violate are reported as drift.
RULES: list[dict] = [
    # DASHBOARDS: only dashboards (.html) and the index
    {
        "path": "JCH_Inbox/01_DASHBOARDS",
        "description": "Tableaux de bord visuels",
        "allowed": [".html"],
        "index_files": ["INDEX.md"],
        "disallowed": [".md", ".command", ".sh", ".py", ".txt"],
        "exception_dirs": ["legacy", "assets"],
    },
    # BIN: only executables
    {
        "path": "bin",
        "description": "Exécutables et scripts lancés par l'utilisateur",
        "allowed": None,  # anything goes
        "index_files": None,
        "disallowed": [".md", ".txt", ".pyc", ".json"],
        "exception_dirs": [],
    },
    # SCRIPTS: code + logs + notes + systemd units
    {
        "path": "scripts",
        "description": "Scripts Python du système PKA",
        "allowed": None,
        "disallowed": [".jpg", ".png", ".gif", ".mp3", ".wav"],
        "index_files": [],
        "exception_dirs": ["modules", "launchd", "logs", "decouvertes-collector"],
    },
    # DOCS: only documentation
    {
        "path": "docs",
        "description": "Documentation et fiches d'usage",
        "allowed": None,
        "disallowed": [".command", ".sh", ".py", ".pptx", ".xlsx"],
        "index_files": [],
        "exception_dirs": [],
    },
]


def _check_rule(root: Path, rule: dict) -> list[str]:
    target = root / rule["path"]
    if not target.is_dir():
        return []

    _allowed = rule["allowed"]
    _disallowed = rule["disallowed"]
    _index_files = rule.get("index_files") or []
    _exception_dirs = rule.get("exception_dirs") or []
    violations: list[str] = []

    for item in sorted(target.iterdir()):
        if item.name.startswith("."):
            continue  # skip dotfiles
        if item.is_dir() and item.name in _exception_dirs:
            continue
        if item.is_dir():
            continue  # don't recurse (shallow only)

        ext = item.suffix.lower()
        name = item.name

        # Skip index files
        if name in _index_files:
            continue

        # Check disallowed
        if _disallowed and ext in _disallowed:
            violations.append(
                f"{rule['path']}/{name} — extension .{ext} interdite dans {rule['description']}"
            )
            continue

        # If allowed list exists, check membership
        if _allowed and ext not in _allowed:
            violations.append(
                f"{rule['path']}/{name} — extension .{ext} non attendue dans {rule['description']} (attendu: {', '.join(_allowed)})"
            )

    return violations


def run_structure_check() -> dict:
    findings: list[dict] = []
    for rule in RULES:
        violations = _check_rule(ROOT, rule)
        for v in violations:
            findings.append({
                "severity": "low",
                "check": "structure-drift",
                "path": v,
                "detail": "Fichier mal positionné — ne correspond pas à la vocation du dossier",
            })

    status = "green" if not findings else "orange"
    return {"status": status, "findings": findings}


def main() -> int:
    import json
    result = run_structure_check()
    if result["findings"]:
        print("STRUCTURE DRIFT DETECTED")
        for f in result["findings"]:
            print(f"  {f['path']}")
        print(f"Status: {result['status'].upper()}")
        return 1
    print("Structure clean.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
