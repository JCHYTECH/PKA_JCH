#!/usr/bin/env python3
"""Write or refresh lightweight PKA instincts."""

from __future__ import annotations

import argparse
import sqlite3
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "TEAM" / "team.db"


def write_instinct(
    instinct_key: str,
    summary: str,
    trigger_pattern: str,
    observation: str,
    action: str,
    confidence: float = 0.6,
    scope: str = "global",
    project_key: str | None = None,
    source_kind: str = "learned",
    source_ref: str | None = None,
    model: str | None = None,
) -> int:
    today = date.today().isoformat()
    with sqlite3.connect(DB_PATH) as conn:
        row = conn.execute(
            "SELECT id, observation_count FROM instincts WHERE instinct_key = ?",
            (instinct_key,),
        ).fetchone()
        if row:
            instinct_id, observation_count = row
            conn.execute(
                """
                UPDATE instincts
                SET summary=?, trigger_pattern=?, observation=?, action=?, confidence=?,
                    scope=?, project_key=?, source_kind=?, source_ref=?, model=?,
                    observation_count=?, last_observed=?, updated_at=?, status='active'
                WHERE id=?
                """,
                (
                    summary, trigger_pattern, observation, action, confidence,
                    scope, project_key, source_kind, source_ref, model,
                    observation_count + 1, today, today, instinct_id,
                ),
            )
            print(f"✅ Instinct updated (id={instinct_id}) : {instinct_key}")
            return instinct_id
        cursor = conn.execute(
            """
            INSERT INTO instincts
            (instinct_key, summary, trigger_pattern, observation, action, confidence,
             scope, project_key, source_kind, source_ref, model, last_observed, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                instinct_key, summary, trigger_pattern, observation, action, confidence,
                scope, project_key, source_kind, source_ref, model, today, today,
            ),
        )
        instinct_id = cursor.lastrowid
        print(f"✅ New instinct created (id={instinct_id}) : {instinct_key}")
        return instinct_id


def main() -> int:
    parser = argparse.ArgumentParser(description="Write or refresh a PKA instinct")
    parser.add_argument("--instinct-key", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--trigger", required=True, dest="trigger_pattern")
    parser.add_argument("--observation", required=True)
    parser.add_argument("--action", required=True)
    parser.add_argument("--confidence", type=float, default=0.6)
    parser.add_argument("--scope", default="global")
    parser.add_argument("--project-key", default=None)
    parser.add_argument("--source-kind", default="learned")
    parser.add_argument("--source-ref", default=None)
    parser.add_argument("--model", default=None)
    args = parser.parse_args()
    write_instinct(
        instinct_key=args.instinct_key,
        summary=args.summary,
        trigger_pattern=args.trigger_pattern,
        observation=args.observation,
        action=args.action,
        confidence=args.confidence,
        scope=args.scope,
        project_key=args.project_key,
        source_kind=args.source_kind,
        source_ref=args.source_ref,
        model=args.model,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
