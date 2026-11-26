#!/usr/bin/env python3
"""Source kanban locale — lit la vue consolidée des thread files (TTD.md).

Décision JC 2026-11-26 : geler Plane comme source du kanban du Hub.
La source unique devient les thread files, consolidés dans TTD.md (régénéré au /save).
Ce module remplace pka_plane_adapter pour l'alimentation du kanban dashboard.

Format attendu des lignes TTD :
    - [ ] **P1 · — · (Dobby)** description
    - [x] **P2 · 2026-12-12 · (JC + Miel)** description
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TTD_PATH = ROOT / "JCH_Inbox" / "03_PROJECTS" / "TTD.md"

_LINE_RE = re.compile(r"^-\s*\[([ xX])\]\s+\*\*(.+?)\*\*\s*(.*)$")
_OWNER_RE = re.compile(r"^(.*?)\s*\(([^)]*)\)\s*$")
_PRIO_RE = re.compile(r"^(P\d+|.*?)\s*·")
_JC_RE = re.compile(r"\bjch?\b", re.IGNORECASE)

_BLOCKED_HINTS = (
    "bloqué", "bloquee", "reporté", "reporte",
    "gelé", "gelee", "en attente", "en pause", "en standby",
)

STATUS_DONE = "Termine"
STATUS_AWAITING = "En validation"
STATUS_BLOCKED = "En attente"
STATUS_IN_PROGRESS = "En cours"


def _parse_bold(bold: str) -> tuple[str, str]:
    """Extrait (priorité, owner) depuis le gras d'une ligne TTD."""
    m = _OWNER_RE.match(bold)
    if m:
        left, owner = m.group(1).strip(), m.group(2).strip()
    else:
        left, owner = bold.strip(), "Dobby"
    pm = _PRIO_RE.match(left)
    priority = (pm.group(1).strip() if pm else left) or "normale"
    return priority, owner or "Dobby"


def _status(done: bool, owner: str, description: str) -> str:
    if done:
        return STATUS_DONE
    low = description.lower()
    if any(h in low for h in _BLOCKED_HINTS):
        return STATUS_BLOCKED
    if _JC_RE.search(owner):
        return STATUS_AWAITING
    return STATUS_IN_PROGRESS


def _labels(done: bool, owner: str, description: str) -> list[str]:
    labels: list[str] = []
    if not done and _JC_RE.search(owner):
        labels.append("en-attente-jch")
    low = description.lower()
    if any(h in low for h in _BLOCKED_HINTS):
        labels.append("bloqué")
    return labels


def load_cards(ttd_path: Path | None = None) -> list[dict]:
    """Parse TTD.md et renvoie les cartes kanban (conformes pka_kanban_schema)."""
    path = ttd_path or TTD_PATH
    if not path.exists():
        return []

    cards: list[dict] = []
    project: str | None = None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line.startswith("## "):
            project = line[3:].strip()
            continue
        if project is None:
            continue
        m = _LINE_RE.match(line)
        if not m:
            continue
        done = m.group(1).lower() == "x"
        bold = m.group(2)
        description = m.group(3).strip()
        priority, owner = _parse_bold(bold)
        cards.append({
            "title": description or bold,
            "project": project,
            "type": "task",
            "owner": owner,
            "priority": priority,
            "status": _status(done, owner, description),
            "description": description,
            "labels": _labels(done, owner, description),
        })
    return cards


def main() -> int:
    parser = argparse.ArgumentParser(description="Liste les cartes kanban depuis TTD.md")
    parser.add_argument("--json", action="store_true", help="sortie JSON")
    args = parser.parse_args()
    cards = load_cards()
    if args.json:
        print(json.dumps(cards, ensure_ascii=False, indent=2))
    else:
        for c in cards:
            print(f"[{c['status']:12}] {c['project']:18} {c['priority']:9} ({c['owner']}) {c['title']}")
    print(f"\n{len(cards)} cartes", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
