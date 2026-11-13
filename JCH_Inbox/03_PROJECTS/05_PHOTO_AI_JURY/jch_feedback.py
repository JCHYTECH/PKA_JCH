#!/usr/bin/env python3
"""Migration et contrôle du retour de retouche explicite de JCH."""

import argparse
import json
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "argus_critique.db"
SCHEMA_VERSION = 1
FOUNDATION_TABLES = (
    "retouch_sessions",
    "retouch_proposals",
    "retouch_validations",
)

SCHEMA = (
    """
    CREATE TABLE argus_schema_migrations (
        version INTEGER PRIMARY KEY,
        applied_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
    ) STRICT
    """,
    """
    CREATE TABLE retouch_sessions (
        id TEXT PRIMARY KEY,
        image_hash TEXT NOT NULL CHECK (
            length(image_hash) = 64
            AND image_hash NOT GLOB '*[^0-9a-f]*'
        ),
        lightroom_photo_id TEXT NOT NULL CHECK (length(trim(lightroom_photo_id)) > 0),
        is_raw INTEGER NOT NULL CHECK (is_raw = 1),
        is_virtual_copy INTEGER NOT NULL CHECK (is_virtual_copy = 1),
        context TEXT NOT NULL CHECK (
            context IN ('naturaliste', 'macro', 'wildlife_artistique', 'paysage')
        ),
        baseline_settings_json TEXT NOT NULL CHECK (
            json_valid(baseline_settings_json)
            AND json_type(baseline_settings_json) = 'object'
        ),
        baseline_source TEXT NOT NULL CHECK (
            baseline_source IN ('lightroom_mcp', 'manual_jch')
        ),
        final_settings_json TEXT CHECK (
            final_settings_json IS NULL
            OR (json_valid(final_settings_json) AND json_type(final_settings_json) = 'object')
        ),
        final_source TEXT CHECK (
            final_source IS NULL OR final_source IN ('lightroom_mcp', 'manual_jch')
        ),
        status TEXT NOT NULL DEFAULT 'draft' CHECK (
            status IN ('draft', 'technical_tested', 'awaiting_jch', 'validated', 'rejected')
        ),
        mcp_test_status TEXT NOT NULL DEFAULT 'not_tested' CHECK (
            mcp_test_status IN ('not_tested', 'passed', 'failed')
        ),
        mcp_tested_at TEXT,
        tutorial_notes TEXT,
        created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
        validated_by TEXT CHECK (validated_by IS NULL OR validated_by = 'JCH'),
        validated_at TEXT,
        CHECK (
            (mcp_test_status = 'not_tested' AND mcp_tested_at IS NULL)
            OR (mcp_test_status IN ('passed', 'failed') AND mcp_tested_at IS NOT NULL)
        ),
        CHECK (
            (status = 'validated'
                AND validated_by = 'JCH'
                AND validated_at IS NOT NULL
                AND final_settings_json IS NOT NULL
                AND mcp_test_status = 'passed')
            OR (status != 'validated' AND validated_by IS NULL AND validated_at IS NULL)
        )
    ) STRICT
    """,
    """
    CREATE TABLE retouch_proposals (
        id TEXT PRIMARY KEY,
        session_id TEXT NOT NULL REFERENCES retouch_sessions(id) ON DELETE RESTRICT,
        proposal_number INTEGER NOT NULL CHECK (proposal_number > 0),
        settings_a_json TEXT NOT NULL CHECK (
            json_valid(settings_a_json) AND json_type(settings_a_json) = 'object'
        ),
        settings_b_json TEXT NOT NULL CHECK (
            json_valid(settings_b_json) AND json_type(settings_b_json) = 'object'
        ),
        tutorial_explanation TEXT NOT NULL CHECK (length(trim(tutorial_explanation)) > 0),
        decision TEXT NOT NULL DEFAULT 'pending' CHECK (
            decision IN ('pending', 'a', 'b', 'rejected')
        ),
        decision_comment TEXT,
        decided_by TEXT CHECK (decided_by IS NULL OR decided_by = 'JCH'),
        decided_at TEXT,
        created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
        UNIQUE (session_id, proposal_number),
        CHECK (
            (decision = 'pending' AND decided_by IS NULL AND decided_at IS NULL)
            OR (decision != 'pending' AND decided_by = 'JCH' AND decided_at IS NOT NULL)
        )
    ) STRICT
    """,
    """
    CREATE TABLE retouch_validations (
        id TEXT PRIMARY KEY,
        session_id TEXT NOT NULL REFERENCES retouch_sessions(id) ON DELETE RESTRICT,
        image_hash TEXT NOT NULL CHECK (
            length(image_hash) = 64
            AND image_hash NOT GLOB '*[^0-9a-f]*'
        ),
        unseen_for_jch INTEGER NOT NULL CHECK (unseen_for_jch = 1),
        outcome TEXT NOT NULL CHECK (outcome IN ('accepted', 'rejected')),
        comment TEXT,
        validated_by TEXT NOT NULL CHECK (validated_by = 'JCH'),
        validated_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
    ) STRICT
    """,
    "CREATE INDEX retouch_sessions_image_hash ON retouch_sessions(image_hash)",
    "CREATE INDEX retouch_proposals_session ON retouch_proposals(session_id)",
    "CREATE INDEX retouch_validations_session ON retouch_validations(session_id)",
)


def readonly_connection(db_path: Path) -> sqlite3.Connection:
    return sqlite3.connect(f"{db_path.resolve().as_uri()}?mode=ro", uri=True)


def status(db_path: Path = DB_PATH) -> dict:
    with readonly_connection(db_path) as connection:
        tables = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }
        counts = {}
        for table in ("analyses", "analysis_evaluations", *FOUNDATION_TABLES):
            if table in tables:
                counts[table] = connection.execute(
                    f"SELECT count(*) FROM {table}"
                ).fetchone()[0]
        return {
            "database": str(db_path),
            "schema_version": connection.execute("PRAGMA user_version").fetchone()[0],
            "integrity_check": connection.execute("PRAGMA integrity_check").fetchone()[0],
            "foreign_key_violations": connection.execute(
                "SELECT count(*) FROM pragma_foreign_key_check"
            ).fetchone()[0],
            "counts": counts,
        }


def migrate(db_path: Path = DB_PATH) -> None:
    with sqlite3.connect(db_path) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        existing = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }
        version = connection.execute("PRAGMA user_version").fetchone()[0]
        applied = connection.execute(
            "SELECT count(*) FROM argus_schema_migrations WHERE version = ?",
            (SCHEMA_VERSION,),
        ).fetchone()[0] if "argus_schema_migrations" in existing else 0

        if version > SCHEMA_VERSION:
            raise RuntimeError(f"Version SQLite inattendue : {version}")
        if applied:
            if version != SCHEMA_VERSION or set(FOUNDATION_TABLES) - existing:
                raise RuntimeError("Migration déclarée mais schéma de retour incohérent")
            print(json.dumps(status(db_path), ensure_ascii=False, indent=2))
            return
        if version != 0:
            raise RuntimeError(f"Version SQLite inattendue : {version}")
        if set(FOUNDATION_TABLES) & existing or "argus_schema_migrations" in existing:
            raise RuntimeError("Tables de migration préexistantes : inspection nécessaire")

        connection.execute("BEGIN IMMEDIATE")
        try:
            old_counts = {
                table: connection.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
                for table in ("analyses", "analysis_evaluations", "moderation_queue")
            }
            for statement in SCHEMA:
                connection.execute(statement)
            connection.execute(
                "INSERT INTO argus_schema_migrations(version) VALUES (?)",
                (SCHEMA_VERSION,),
            )
            connection.execute(f"PRAGMA user_version = {SCHEMA_VERSION}")
            for table, expected in old_counts.items():
                actual = connection.execute(f"SELECT count(*) FROM {table}").fetchone()[0]
                if actual != expected:
                    raise RuntimeError(f"Comptage historique modifié dans {table}")
            if connection.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
                raise RuntimeError("Contrôle d'intégrité SQLite en échec")
            violations = connection.execute("PRAGMA foreign_key_check").fetchall()
            if violations:
                raise RuntimeError(f"Violations de clés étrangères : {violations}")
        except Exception:
            connection.rollback()
            raise
        connection.commit()

    print(json.dumps(status(db_path), ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("migrate", "status"))
    args = parser.parse_args()
    if args.command == "migrate":
        migrate()
    else:
        print(json.dumps(status(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
