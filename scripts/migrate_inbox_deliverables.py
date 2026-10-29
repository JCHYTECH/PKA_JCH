#!/usr/bin/env python3
"""Migrate inbox deliverable tracking fields.

Default mode is a dry-run on a temporary database copy. Use --apply to migrate
TEAM/team.db after creating a fresh backup.
"""

from __future__ import annotations

import argparse
import shutil
import sqlite3
import subprocess
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "TEAM" / "team.db"
TMP_DIR = ROOT / "tmp" / "inbox_migration"
BACKUP_SCRIPT = ROOT / "scripts" / "backup_team_db.py"

EXPECTED_COLUMNS = [
    "id",
    "direction",
    "from_name",
    "to_name",
    "subject",
    "body",
    "status",
    "created_at",
    "closed_at",
    "file_path",
]

NEW_COLUMNS = [
    "deliverable_path",
    "delivered_at",
    "validated_at",
    "validated_by",
    "rejection_reason",
]

ALLOWED_STATUS = (
    "'pending', 'in_progress', 'done', 'delivered', 'validated', 'rejected', 'cancelled'"
)


def connect(path: Path) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def table_columns(conn: sqlite3.Connection) -> list[str]:
    return [row["name"] for row in conn.execute("PRAGMA table_info(inbox)")]


def scalar(conn: sqlite3.Connection, sql: str) -> int | str:
    return conn.execute(sql).fetchone()[0]


def status_counts(conn: sqlite3.Connection) -> dict[str, int]:
    rows = conn.execute("SELECT status, COUNT(*) AS n FROM inbox GROUP BY status")
    return {row["status"]: row["n"] for row in rows}


def assert_ready(conn: sqlite3.Connection) -> None:
    columns = table_columns(conn)
    missing = [name for name in EXPECTED_COLUMNS if name not in columns]
    if missing:
        raise RuntimeError(f"inbox schema missing expected columns: {missing}")

    if any(name in columns for name in NEW_COLUMNS):
        existing = [name for name in NEW_COLUMNS if name in columns]
        raise RuntimeError(f"inbox already has deliverable columns: {existing}")

    unsupported = [
        row["status"]
        for row in conn.execute(
            """
            SELECT DISTINCT status
            FROM inbox
            WHERE status NOT IN ('pending', 'in_progress', 'done', 'cancelled')
            """
        )
    ]
    if unsupported:
        raise RuntimeError(f"inbox has unsupported pre-migration statuses: {unsupported}")


def migrate(conn: sqlite3.Connection) -> None:
    before_count = scalar(conn, "SELECT COUNT(*) FROM inbox")
    before_counts = status_counts(conn)

    conn.execute("BEGIN IMMEDIATE")
    try:
        conn.execute("DROP TABLE IF EXISTS inbox_new")
        conn.execute(
            f"""
            CREATE TABLE inbox_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                direction TEXT NOT NULL CHECK(direction IN ('JCH→TEAM', 'TEAM→JCH')),
                from_name TEXT NOT NULL,
                to_name TEXT NOT NULL,
                subject TEXT NOT NULL,
                body TEXT,
                status TEXT NOT NULL DEFAULT 'pending'
                    CHECK(status IN ({ALLOWED_STATUS})),
                created_at TEXT NOT NULL DEFAULT (datetime('now')),
                closed_at TEXT,
                file_path TEXT,
                deliverable_path TEXT,
                delivered_at TEXT,
                validated_at TEXT,
                validated_by TEXT DEFAULT 'JCH',
                rejection_reason TEXT
            )
            """
        )
        conn.execute(
            """
            INSERT INTO inbox_new (
                id, direction, from_name, to_name, subject, body, status,
                created_at, closed_at, file_path
            )
            SELECT
                id, direction, from_name, to_name, subject, body, status,
                created_at, closed_at, file_path
            FROM inbox
            ORDER BY id
            """
        )
        copied_count = scalar(conn, "SELECT COUNT(*) FROM inbox_new")
        if copied_count != before_count:
            raise RuntimeError(f"row count mismatch during copy: {copied_count} != {before_count}")

        conn.execute("DROP INDEX IF EXISTS idx_inbox_direction_status")
        conn.execute("ALTER TABLE inbox RENAME TO inbox_legacy_pre_deliverables")
        conn.execute("ALTER TABLE inbox_new RENAME TO inbox")
        conn.execute("CREATE INDEX idx_inbox_direction_status ON inbox(direction, status)")
        conn.execute("DROP TABLE inbox_legacy_pre_deliverables")

        after_count = scalar(conn, "SELECT COUNT(*) FROM inbox")
        after_counts = status_counts(conn)
        if after_count != before_count:
            raise RuntimeError(f"row count mismatch after migration: {after_count} != {before_count}")
        if after_counts != before_counts:
            raise RuntimeError(f"status counts changed: {after_counts} != {before_counts}")

        integrity = scalar(conn, "PRAGMA integrity_check")
        if integrity != "ok":
            raise RuntimeError(f"integrity check failed: {integrity}")

        conn.commit()
    except Exception:
        conn.rollback()
        raise


def run_backup() -> None:
    subprocess.run([sys.executable, str(BACKUP_SCRIPT)], cwd=ROOT, check=True)


def dry_run_path() -> Path:
    TMP_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    return TMP_DIR / f"team_inbox_migration_dry_run_{stamp}.db"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="migrate TEAM/team.db")
    args = parser.parse_args()

    target = DB_PATH
    if args.apply:
        print("Creating fresh backup before applying migration...")
        run_backup()
    else:
        target = dry_run_path()
        shutil.copy2(DB_PATH, target)
        target.chmod(0o600)
        print(f"Dry-run database copy: {target.relative_to(ROOT)}")

    with connect(target) as conn:
        assert_ready(conn)
        before_count = scalar(conn, "SELECT COUNT(*) FROM inbox")
        before_counts = status_counts(conn)
        migrate(conn)
        after_columns = table_columns(conn)
        print(f"Rows preserved: {before_count}")
        print(f"Status counts preserved: {before_counts}")
        print(f"New columns present: {[name for name in NEW_COLUMNS if name in after_columns]}")
        print(f"Integrity: {scalar(conn, 'PRAGMA integrity_check')}")

    if args.apply:
        DB_PATH.chmod(0o600)
        print("Applied migration to TEAM/team.db")
    else:
        print("Dry-run complete; source TEAM/team.db unchanged")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
