import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import instinct_search, instinct_write


INSTINCTS_SCHEMA = """
CREATE TABLE instincts (
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
);
"""


class InstinctToolsTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.tmpdir.name) / "team.db"
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript(INSTINCTS_SCHEMA)

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_write_instinct_upserts_and_increments_observation_count(self):
        with mock.patch.object(instinct_write, "DB_PATH", self.db_path):
            instinct_write.write_instinct(
                instinct_key="arteon-brand-scope",
                summary="ARTEON queries should prefer the ARTEON profile.",
                trigger_pattern="arteon brand",
                observation="Brand requests repeatedly map to ARTEON.",
                action="Load the ARTEON context profile first.",
                confidence=0.8,
                scope="project",
                project_key="02_ARTEON",
                source_ref="test",
                model="gpt-5",
            )
            instinct_write.write_instinct(
                instinct_key="arteon-brand-scope",
                summary="ARTEON queries should prefer the ARTEON profile.",
                trigger_pattern="arteon brand",
                observation="Brand requests repeatedly map to ARTEON.",
                action="Load the ARTEON context profile first.",
                confidence=0.85,
                scope="project",
                project_key="02_ARTEON",
                source_ref="test-2",
                model="gpt-5",
            )

        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT observation_count, confidence, project_key FROM instincts WHERE instinct_key = ?",
                ("arteon-brand-scope",),
            ).fetchone()

        self.assertEqual(row, (2, 0.85, "02_ARTEON"))

    def test_search_instincts_prefers_matching_project_scope(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO instincts
                (instinct_key, summary, trigger_pattern, observation, action, confidence, scope, project_key)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    "global-context",
                    "Use global context",
                    "photo nature",
                    "General photo requests",
                    "Load global context",
                    0.6,
                    "global",
                    None,
                ),
            )
            conn.execute(
                """
                INSERT INTO instincts
                (instinct_key, summary, trigger_pattern, observation, action, confidence, scope, project_key)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    "project-context",
                    "Use project context",
                    "photo nature",
                    "Photo nature requests",
                    "Load PHOTO_NATURE profile",
                    0.9,
                    "project",
                    "06_PHOTO_NATURE",
                ),
            )
            conn.commit()

        with mock.patch.object(instinct_search, "DB_PATH", self.db_path):
            rows = instinct_search.search_instincts("photo nature", project_key="06_PHOTO_NATURE")

        self.assertEqual(rows[0]["instinct_key"], "project-context")
        self.assertEqual(rows[1]["instinct_key"], "global-context")


if __name__ == "__main__":
    unittest.main()
