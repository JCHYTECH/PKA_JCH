#!/usr/bin/env python3
"""Idempotent migration for the PKA skills metadata fields."""

from __future__ import annotations

import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "TEAM" / "team.db"


def add_column(conn: sqlite3.Connection, sql: str) -> None:
    try:
        conn.execute(sql)
    except sqlite3.OperationalError as exc:
        if "duplicate column name" not in str(exc).lower():
            raise


def main() -> int:
    with sqlite3.connect(DB_PATH) as conn:
        add_column(conn, "ALTER TABLE skills ADD COLUMN source_kind TEXT DEFAULT 'manual'")
        add_column(conn, "ALTER TABLE skills ADD COLUMN confidence REAL DEFAULT 0.7")
        add_column(conn, "ALTER TABLE skills ADD COLUMN scope TEXT DEFAULT 'global'")
        add_column(conn, "ALTER TABLE skills ADD COLUMN project_key TEXT")
        add_column(conn, "ALTER TABLE skills ADD COLUMN updated_at DATE")
        conn.execute("UPDATE skills SET updated_at = COALESCE(updated_at, created_at, CURRENT_DATE)")
        conn.execute("UPDATE skills SET source_kind = COALESCE(source_kind, 'manual')")
        conn.execute("UPDATE skills SET confidence = COALESCE(confidence, 0.7)")
        conn.execute("UPDATE skills SET scope = COALESCE(scope, 'global')")
        conn.commit()
    print("✅ Skills metadata migration complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
