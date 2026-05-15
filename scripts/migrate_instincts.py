#!/usr/bin/env python3
"""Create the lightweight instincts table for PKA_JCH."""

from __future__ import annotations

import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "TEAM" / "team.db"


def main() -> int:
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS instincts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                instinct_key TEXT NOT NULL UNIQUE,
                summary TEXT NOT NULL,
                trigger_pattern TEXT NOT NULL,
                observation TEXT NOT NULL,
                action TEXT NOT NULL,
                confidence REAL DEFAULT 0.6,
                scope TEXT DEFAULT 'global',
                project_key TEXT,
                source_kind TEXT DEFAULT 'learned',
                source_ref TEXT,
                observation_count INTEGER DEFAULT 1,
                last_observed DATE DEFAULT CURRENT_DATE,
                created_at DATE DEFAULT CURRENT_DATE,
                updated_at DATE DEFAULT CURRENT_DATE,
                model TEXT DEFAULT 'claude-sonnet-4-6',
                status TEXT DEFAULT 'active'
            )
            """
        )
        conn.commit()
    print("✅ Instincts migration complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
