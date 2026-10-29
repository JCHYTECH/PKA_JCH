#!/usr/bin/env python3
"""Generate thin cross-tool stub files pointing to AGENTS.md (single canonical source).

After migration to unified AGENTS.md (2026-07-02):
- AGENTS.md = canonical source with all rules
- CLAUDE.md, DEEPSEEK.md, GEMINI.md, QWEN.md, KIMI.md = stubs
- CLAUDE.md preserves its Claude-specific content after the managed block
"""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "TEAM" / "team.db"
CONFIG_PATH = ROOT / "JCH_Inbox" / "99_SYSTEM" / "tool_pointer_config.json"
PROJECTS_DIR = ROOT / "JCH_Inbox" / "03_PROJECTS"
INBOX_DIR = ROOT / "JCH_Inbox" / "00_INBOX"
AGENTS_PATH = ROOT / "AGENTS.md"
CLAUDE_PATH = ROOT / "CLAUDE.md"
CLAUDE_BLOCK_START = "<!-- PKA:CANONICAL-START -->"
CLAUDE_BLOCK_END = "<!-- PKA:CANONICAL-END -->"

# Snapshot marker in AGENTS.md — we update the line after this
SNAPSHOT_MARKER = "Current scan snapshot:"


def active_count() -> int:
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute("SELECT count(*) FROM members WHERE status='active'").fetchone()
    return int(row[0])


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def list_projects() -> list[str]:
    if not PROJECTS_DIR.is_dir():
        return []
    return sorted(item.name for item in PROJECTS_DIR.iterdir()
                  if item.is_dir() and item.name != "archive")


def inbox_count() -> int:
    if not INBOX_DIR.is_dir():
        return 0
    return sum(1 for item in INBOX_DIR.iterdir() if item.is_file() and not item.name.startswith("."))


def render_stub(filename: str, tool_cfg: dict, team_count: int) -> str:
    """Generate a stub that points to AGENTS.md."""
    specialist_count = team_count - 1 if team_count > 0 else 0
    return (
        f"# {tool_cfg['title']}\n"
        f"\n"
        f"**TOOL :** {tool_cfg['tool_label']}\n"
        f"**MODEL :** {tool_cfg['model_hint']}\n"
        f"\n"
        f"> **Lire `AGENTS.md` pour les instructions complètes** — identité, règles de comportement, sources, protocole opérationnel, graphify, moteur de recherche.\n"
        f"> Ce fichier est un stub. `AGENTS.md` est la source canonique unique.\n"
        f"> **TEAM :** {team_count} membres actifs — {specialist_count} spécialistes + Dobby\n"
    )


def render_claude_managed_block(tool_cfg: dict) -> str:
    """Generate the managed block for CLAUDE.md."""
    return (
        f"{CLAUDE_BLOCK_START}\n"
        f"## AGENTS.md — Source canonique\n"
        f"\n"
        f"**TOOL :** {tool_cfg['tool_label']}\n"
        f"**MODEL :** {tool_cfg['model_hint']}\n"
        f"\n"
        f"> **Lire `AGENTS.md` pour les instructions complètes** — identité, règles de comportement, sources, protocole opérationnel, graphify, moteur de recherche.\n"
        f"> Ce fichier est un stub. `AGENTS.md` est la source canonique unique pour tous les outils.\n"
        f"{CLAUDE_BLOCK_END}"
    )


def update_agents_snapshot(team_count: int, projects: list[str], inbox_items: int, check: bool) -> int:
    """Update the Current scan snapshot line in AGENTS.md."""
    if not AGENTS_PATH.exists():
        return 0

    current = AGENTS_PATH.read_text(encoding="utf-8")
    new_snapshot = (
        f"Current scan snapshot: {len(projects)} projets actifs "
        f"({', '.join(f'`{name}`' for name in projects)}) ; "
        f"{inbox_items} éléments dans `JCH_Inbox/00_INBOX/`."
    )

    lines = current.split("\n")
    updated_lines = []
    changed = False
    for line in lines:
        if line.startswith(SNAPSHOT_MARKER):
            if line != new_snapshot:
                updated_lines.append(new_snapshot)
                changed = True
            else:
                updated_lines.append(line)
        else:
            updated_lines.append(line)

    updated = "\n".join(updated_lines)

    if check:
        if changed:
            print("DRIFT AGENTS.md (snapshot)")
            return 1
        return 0

    if changed:
        AGENTS_PATH.write_text(updated, encoding="utf-8")
        print("UPDATED AGENTS.md (snapshot)")
    return 0


def sync_claude_managed_block(tool_cfg: dict, check: bool) -> int:
    """Update the managed block in CLAUDE.md, preserving content after it."""
    if not CLAUDE_PATH.exists():
        return 0

    current = CLAUDE_PATH.read_text(encoding="utf-8")
    managed = render_claude_managed_block(tool_cfg)

    start = current.find(CLAUDE_BLOCK_START)
    end = current.find(CLAUDE_BLOCK_END)

    if start == -1 or end == -1 or end < start:
        updated = managed + "\n\n" + current
    else:
        end += len(CLAUDE_BLOCK_END)
        updated = current[:start] + managed + current[end:]

    if not updated.endswith("\n"):
        updated += "\n"

    if check:
        if CLAUDE_PATH.read_text(encoding="utf-8") != updated:
            print("DRIFT CLAUDE.md")
            return 1
        return 0

    CLAUDE_PATH.write_text(updated, encoding="utf-8")
    print("UPDATED CLAUDE.md")
    return 0


def generate(check: bool = False) -> int:
    cfg = load_config()
    team_count = active_count()
    projects = list_projects()
    inbox_items = inbox_count()
    exit_code = 0

    # Update AGENTS.md snapshot
    exit_code = max(exit_code, update_agents_snapshot(team_count, projects, inbox_items, check))

    # Get Claude tool config
    claude_cfg = cfg["tools"].get("CLAUDE.md")
    if claude_cfg:
        exit_code = max(exit_code, sync_claude_managed_block(claude_cfg, check))

    # Generate stubs for all tool files except AGENTS.md and CLAUDE.md (handled separately)
    for filename, tool_cfg in cfg["tools"].items():
        if filename == "AGENTS.md":
            continue  # AGENTS.md is the canonical source, not a stub
        if filename == "CLAUDE.md":
            continue  # Handled by sync_claude_managed_block

        rendered = render_stub(filename, tool_cfg, team_count) + "\n"
        target = ROOT / filename
        current = target.read_text(encoding="utf-8") if target.exists() else None

        if check:
            if current != rendered:
                print(f"DRIFT {filename}")
                exit_code = 1
            continue

        target.write_text(rendered, encoding="utf-8")
        print(f"UPDATED {filename}")

    return exit_code


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate PKA tool pointer stubs")
    parser.add_argument("--check", action="store_true", help="Report drift without writing files")
    args = parser.parse_args()
    return generate(check=args.check)


if __name__ == "__main__":
    raise SystemExit(main())
