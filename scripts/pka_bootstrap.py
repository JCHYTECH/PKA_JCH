#!/usr/bin/env python3
"""pka_bootstrap.py — Assembleur de bootstrap PKA (source canonique unique).

Construit un contexte de démarrage consolidé dans l'ordre canonique de
`docs/system/dobby-memory-bootstrap.md` :

    Config (identité/règles) → State (état vivant) → TTD → Log → scans.

Chaque runtime (deepseek-tui, qwen, codex, gemini) lit le MÊME contexte,
assemblé ici de façon déterministe au lieu de laisser le modèle juger quoi lire.

Usage :
    python3 scripts/pka_bootstrap.py              # écrit _local/bootstrap-context.md
    python3 scripts/pka_bootstrap.py --print      # stdout (embedding system prompt)
    python3 scripts/pka_bootstrap.py --write PATH # écrit un fichier arbitraire
    python3 scripts/pka_bootstrap.py --quick      # identité seulement (Config), sans State/scans

Notes :
    - Les fichiers Config et State sont lus EN ENTIER (jamais tronqués).
    - MEMORY.md (Log) est limité à sa queue récente : le passé n'est pas l'état.
    - Tout fichier manquant est signalé `[missing: path]`, jamais inventé.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

# ---- Séquence canonique ----------------------------------------------------

# Phase 1 — Identité & Personnalité (Config, immuable)
CONFIG_FILES: list[Path] = [
    ROOT_DIR / "ADAPTER-PROMPT.md",
    ROOT_DIR / "SOUL.md",
    ROOT_DIR / "USER.md",
    ROOT_DIR / "TEAM" / "dobby.md",
    ROOT_DIR / "TEAM" / "ROSTER.md",
    ROOT_DIR / "docs" / "system" / "dobby-memory-bootstrap.md",
    ROOT_DIR / "docs" / "system" / "procedure-traduction-jade.md",
]

# Contexte & outils (petits fichiers, lus en entier)
CONTEXT_FILES: list[Path] = [
    ROOT_DIR / "wiki" / "index.md",
    ROOT_DIR / "docs" / "system" / "outils-index.md",
    ROOT_DIR / "JCH_Inbox" / "99_SYSTEM" / "routing_rules.md",
]

# Phase 3 — État Vivant (State — lu en entier, jamais tronqué)
STATE_FILES: list[Path] = [
    ROOT_DIR / "JCH_Inbox" / "04_PILOTAGE_STRATEGIQUE" / "hardware-state.md",
    ROOT_DIR / "JCH_Inbox" / "04_PILOTAGE_STRATEGIQUE" / "etat-projets.md",
    ROOT_DIR / "JCH_Inbox" / "04_PILOTAGE_STRATEGIQUE" / "decisions-actives.md",
    ROOT_DIR / "JCH_Inbox" / "04_PILOTAGE_STRATEGIQUE" / "priorites-actives.md",
    ROOT_DIR / "JCH_Inbox" / "04_PILOTAGE_STRATEGIQUE" / "risques-et-frottements.md",
    ROOT_DIR / "JCH_Inbox" / "04_PILOTAGE_STRATEGIQUE" / "roadmap-90-jours.md",
    ROOT_DIR / "JCH_Inbox" / "04_PILOTAGE_STRATEGIQUE" / "photo-materiel.md",
    ROOT_DIR / "JCH_Inbox" / "04_PILOTAGE_STRATEGIQUE" / "lupo-materiel.md",
]

# Vue consolidée des choses à faire (dérivé, régénéré au /save)
TTD_FILE: Path = ROOT_DIR / "JCH_Inbox" / "03_PROJECTS" / "TTD.md"

# Phase 2 — Contexte & Historique (Log). MEMORY.md est un journal : on ne garde
# que la queue récente, car les faits datés ne sont pas l'état actuel.
LOG_FILE: Path = ROOT_DIR / "MEMORY.md"
LOG_TAIL_LINES: int = 300

DEFAULT_OUTPUT: Path = ROOT_DIR / "_local" / "bootstrap-context.md"


# ---- Helpers ---------------------------------------------------------------

def read_optional(path: Path) -> str:
    if not path.exists():
        return f"[missing: {path.relative_to(ROOT_DIR)}]"
    return path.read_text(encoding="utf-8")


def read_tail(path: Path, lines: int) -> str:
    if not path.exists():
        return f"[missing: {path.relative_to(ROOT_DIR)}]"
    content = path.read_text(encoding="utf-8").splitlines()
    if len(content) <= lines:
        return "\n".join(content)
    head = content[:1]
    return "\n".join(head + ["… (tronqué — journal complet disponible sur disque)"] + content[-lines:])


def render_loaded_file(path: Path, content: str, *, note: str | None = None) -> str:
    rel = path.relative_to(ROOT_DIR) if path.is_relative_to(ROOT_DIR) else path
    suffix = f"\n<!-- {note} -->" if note else ""
    return f"""Loaded file: {rel}{suffix}
```markdown
{content}
```
"""


def scan_dir(path: Path, *, dirs_only: bool = False) -> list[str]:
    if not path.exists():
        return [f"[missing: {path.relative_to(ROOT_DIR)}]"]
    entries = []
    for item in sorted(path.iterdir(), key=lambda p: p.name.lower()):
        if dirs_only and not item.is_dir():
            continue
        if item.name.startswith("."):
            continue
        entries.append(str(item.relative_to(ROOT_DIR)))
    return entries


def latest_daily_files(limit: int = 2) -> list[Path]:
    daily_dir = ROOT_DIR / "wiki" / "Daily"
    if not daily_dir.exists():
        return []
    return sorted(daily_dir.glob("*.md"))[-limit:]


# ---- Assemblage ------------------------------------------------------------

def render_bootstrap_context(*, quick: bool = False) -> str:
    stamp = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M %Z")
    parts: list[str] = [f"# Bootstrap PKA — généré {stamp} par scripts/pka_bootstrap.py\n"]

    # Config (toujours, même en --quick)
    for path in CONFIG_FILES:
        parts.append(render_loaded_file(path, read_optional(path)))

    if quick:
        parts.append("<!-- mode --quick : Contexte, State, TTD et scans non chargés -->\n")
        return "\n".join(parts)

    # Contexte & outils
    for path in CONTEXT_FILES:
        parts.append(render_loaded_file(path, read_optional(path)))

    # State (en entier)
    for path in STATE_FILES:
        parts.append(render_loaded_file(path, read_optional(path)))

    # TTD
    parts.append(render_loaded_file(TTD_FILE, read_optional(TTD_FILE)))

    # Log (queue récente)
    parts.append(
        render_loaded_file(
            LOG_FILE,
            read_tail(LOG_FILE, LOG_TAIL_LINES),
            note=f"journal — dernières {LOG_TAIL_LINES} lignes",
        )
    )

    # Dernières daily
    for path in latest_daily_files():
        parts.append(render_loaded_file(path, read_optional(path)))

    # Scans (projets + inbox)
    projects = "\n".join(f"- {e}" for e in scan_dir(ROOT_DIR / "JCH_Inbox" / "03_PROJECTS", dirs_only=True))
    inbox = "\n".join(f"- {e}" for e in scan_dir(ROOT_DIR / "JCH_Inbox" / "00_INBOX"))
    parts.append(
        f"""Loaded scan: JCH_Inbox/03_PROJECTS/ (dossiers)
```text
{projects}
```

Loaded scan: JCH_Inbox/00_INBOX/ (entrées)
```text
{inbox}
```
"""
    )

    return "\n".join(parts)


# ---- CLI -------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Assemble le bootstrap PKA consolidé.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--print", action="store_true", help="Afficher sur stdout.")
    group.add_argument("--write", metavar="PATH", help="Écrire dans un fichier arbitraire.")
    parser.add_argument("--quick", action="store_true", help="Identité seulement (Config), sans State/scans.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    context = render_bootstrap_context(quick=args.quick)

    if args.print:
        sys.stdout.write(context)
        return 0

    out = Path(args.write) if args.write else DEFAULT_OUTPUT
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(context, encoding="utf-8")
    print(f"Bootstrap écrit : {out} ({len(context)} chars)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
