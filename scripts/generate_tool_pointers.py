#!/usr/bin/env python3
"""Generate thin cross-tool pointer files from one canonical source."""

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
CLAUDE_PATH = ROOT / "CLAUDE.md"
CLAUDE_BLOCK_START = "<!-- PKA:CANONICAL-START -->"
CLAUDE_BLOCK_END = "<!-- PKA:CANONICAL-END -->"


def active_count() -> int:
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute("SELECT count(*) FROM members WHERE status='active'").fetchone()
    return int(row[0])


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def list_projects() -> list[str]:
    if not PROJECTS_DIR.is_dir():
        return []
    return sorted(item.name for item in PROJECTS_DIR.iterdir() if item.is_dir())


def inbox_count() -> int:
    if not INBOX_DIR.is_dir():
        return 0
    return sum(1 for item in INBOX_DIR.iterdir())


def render_pointer(filename: str, tool_cfg: dict, cfg: dict, team_count: int) -> str:
    specialist_count = team_count - 1
    projects = ", ".join(f"`{name}`" for name in list_projects())
    inbox_items = inbox_count()

    lines = [
        f"# {tool_cfg['title']}",
        "",
        "> Generated from `JCH_Inbox/99_SYSTEM/tool_pointer_config.json` by `scripts/generate_tool_pointers.py`.",
        "",
        "## Identity (MANDATORY — applies every session)",
        "",
    ]
    for line in cfg["identity_intro"]:
        lines.append(line.format(specialist_count=specialist_count))

    lines.extend([
        "",
        "## Source of truth",
        "",
    ])
    for item in cfg["source_of_truth"]:
        lines.append(f"- {item}")

    lines.extend([
        "",
        "Read these at session start. This file is a pointer, not a copy.",
        "",
        "## Operating protocol",
        "",
        cfg["operating_protocol"],
        "",
        "## Activation confirmation",
        "",
        "Reply to JCH as Dobby with:",
    ])
    for line in cfg["activation_lines"]:
        lines.append(
            f"- {line.format(tool_label=tool_cfg['tool_label'], model_hint=tool_cfg['model_hint'], team_count=team_count, specialist_count=specialist_count)}"
        )

    lines.extend([
        "",
        f"Current scan snapshot: {len(list_projects())} projets actifs ({projects}) ; {inbox_items} éléments dans `JCH_Inbox/00_INBOX/`.",
        "",
    ])
    return "\n".join(lines)


def render_claude_managed_block(cfg: dict, team_count: int) -> str:
    specialist_count = team_count - 1
    projects = ", ".join(f"`{name}`" for name in list_projects())
    inbox_items = inbox_count()
    lines = [
        CLAUDE_BLOCK_START,
        "## Canonical PKA Overlay",
        "",
        "This block is generated from `JCH_Inbox/99_SYSTEM/tool_pointer_config.json` by `scripts/generate_tool_pointers.py`.",
        "",
        f"- Identity check: `Je suis Dobby 🦉 — ton orchestrateur.`",
        f"- Team count: {team_count} membres actifs — {specialist_count} spécialistes + Dobby",
        "- Source of truth: `MEMORY.md`, `TEAM/team.db`, `TEAM/ROSTER.md`, `TEAM/dobby.md`, `wiki/index.md`",
        f"- Current scan snapshot: {len(list_projects())} projets actifs ({projects}) ; {inbox_items} éléments dans `JCH_Inbox/00_INBOX/`.",
        "",
        "Tool pointer files `AGENTS.md`, `GEMINI.md`, and `DEEPSEEK.md` are derived from the same canonical source.",
        CLAUDE_BLOCK_END,
    ]
    return "\n".join(lines)


def sync_claude_managed_block(root: Path, cfg: dict, team_count: int, check: bool) -> int:
    target = root / "CLAUDE.md"
    if not target.exists():
        if check:
            print("DRIFT CLAUDE.md")
            return 1
        return 0

    current = target.read_text(encoding="utf-8")
    managed = render_claude_managed_block(cfg, team_count)
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
        if current != updated:
            print("DRIFT CLAUDE.md")
            return 1
        return 0

    target.write_text(updated, encoding="utf-8")
    print("UPDATED CLAUDE.md")
    return 0


def generate(check: bool = False) -> int:
    cfg = load_config()
    team_count = active_count()
    exit_code = 0
    exit_code = max(exit_code, sync_claude_managed_block(ROOT, cfg, team_count, check))
    for filename, tool_cfg in cfg["tools"].items():
        rendered = render_pointer(filename, tool_cfg, cfg, team_count) + "\n"
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
    parser = argparse.ArgumentParser(description="Generate PKA tool pointer files")
    parser.add_argument("--check", action="store_true", help="Report drift without writing files")
    args = parser.parse_args()
    return generate(check=args.check)


if __name__ == "__main__":
    raise SystemExit(main())
