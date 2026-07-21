#!/usr/bin/env python3
"""
retro_digest.py — Digest des patterns récurrents pour injection en début de session.

Usage :
    python3 scripts/retro_digest.py              # top 15, seuil session_count >= 3
    python3 scripts/retro_digest.py --top 20     # top 20
    python3 scripts/retro_digest.py --min 2      # seuil session_count >= 2
    python3 scripts/retro_digest.py --raw        # sortie JSON brut
"""

import argparse
import json
import sqlite3
import sys
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "TEAM" / "team.db"

LABELS = {
    "failure": "Échec récurrent",
    "decision": "Décision fréquente",
    "question": "Question récurrente",
    "recurring_question": "Question récurrente",
    "llm_discovered_failure": "Échec (LLM)",
    "llm_discovered_decision": "Décision (LLM)",
}


def fetch_patterns(top: int = 15, min_count: int = 3) -> list[dict]:
    if not DB_PATH.exists():
        return []
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute(
            """SELECT pattern_type, content, session_count, date
               FROM retro_patterns
               WHERE resolved_at IS NULL
                 AND session_count >= ?
               ORDER BY session_count DESC
               LIMIT ?""",
            (min_count, top),
        )
        rows = c.fetchall()
        conn.close()
        return [
            {"type": r[0], "content": r[1], "count": r[2], "date": r[3]}
            for r in rows
        ]
    except sqlite3.DatabaseError:
        return []


def render_markdown(patterns: list[dict]) -> str:
    if not patterns:
        return ""
    lines = ["### Patterns récurrents (mémoire procédurale)\n"]
    for p in patterns:
        label = LABELS.get(p["type"], p["type"])
        lines.append(f"- [{label}] x{p['count']} — {p['content'][:100]}")
    lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Digest patterns récurrents PKA")
    parser.add_argument("--top", type=int, default=15)
    parser.add_argument("--min", dest="min_count", type=int, default=3)
    parser.add_argument("--raw", action="store_true")
    args = parser.parse_args()

    patterns = fetch_patterns(top=args.top, min_count=args.min_count)

    if args.raw:
        print(json.dumps(patterns, ensure_ascii=False, indent=2))
    else:
        print(render_markdown(patterns))


if __name__ == "__main__":
    main()
