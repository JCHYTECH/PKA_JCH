#!/usr/bin/env python3
"""Search lightweight PKA instincts."""

from __future__ import annotations

import argparse
import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "TEAM" / "team.db"


def search_instincts(query: str, limit: int = 3, project_key: str | None = None) -> list[dict]:
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    tokens = [t.lower() for t in query.split() if len(t) > 2]
    if not tokens:
        return []
    conditions = " OR ".join(
        ["(LOWER(instinct_key) LIKE ? OR LOWER(summary) LIKE ? OR LOWER(trigger_pattern) LIKE ? OR LOWER(observation) LIKE ?)"]
        * len(tokens)
    )
    params = []
    for token in tokens:
        params += [f"%{token}%", f"%{token}%", f"%{token}%", f"%{token}%"]
    order_parts = []
    if project_key:
        order_parts.append(
            "CASE "
            "WHEN scope = 'project' AND project_key = ? THEN 0 "
            "WHEN scope = 'global' THEN 1 "
            "ELSE 2 END"
        )
        params.append(project_key)
    order_parts.append("confidence DESC")
    order_parts.append("observation_count DESC")
    rows = cur.execute(
        f"""
        SELECT instinct_key, summary, action, confidence, scope, project_key, observation_count
        FROM instincts
        WHERE status = 'active' AND ({conditions})
        ORDER BY {", ".join(order_parts)}
        LIMIT ?
        """,
        params + [limit],
    ).fetchall()
    con.close()
    return [dict(row) for row in rows]


def format_instincts(instincts: list[dict]) -> str:
    if not instincts:
        return ""
    lines = ["## Instincts pertinents chargés depuis la mémoire PKA\n"]
    for instinct in instincts:
        lines.append(f"### {instinct['instinct_key']}")
        lines.append(f"**Résumé :** {instinct['summary']}")
        lines.append(f"**Action :** {instinct['action']}")
        metadata = [
            f"scope={instinct['scope']}",
            f"confidence={instinct['confidence']}",
            f"observations={instinct['observation_count']}",
        ]
        if instinct.get("project_key"):
            metadata.append(f"project={instinct['project_key']}")
        lines.append(f"**Métadonnées :** {', '.join(metadata)}")
        lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Search PKA instincts")
    parser.add_argument("query")
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("--project-key", default=None)
    args = parser.parse_args()
    print(format_instincts(search_instincts(args.query, args.limit, args.project_key)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
