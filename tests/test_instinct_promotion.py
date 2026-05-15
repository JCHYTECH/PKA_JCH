import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest import mock
import json

from scripts import instinct_promote


SCHEMA = """
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

CREATE TABLE skills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    trigger_pattern TEXT NOT NULL,
    specialist TEXT,
    procedure TEXT NOT NULL,
    context TEXT,
    usage_count INTEGER DEFAULT 0,
    last_used DATE,
    created_at DATE DEFAULT CURRENT_DATE,
    model TEXT DEFAULT 'claude-sonnet-4-6',
    source_kind TEXT DEFAULT 'manual',
    confidence REAL DEFAULT 0.7,
    scope TEXT DEFAULT 'global',
    project_key TEXT,
    updated_at DATE DEFAULT CURRENT_DATE
);
"""


class InstinctPromotionTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.tmpdir.name) / "team.db"
        self.report_dir = Path(self.tmpdir.name) / "reports"
        self.report_dir.mkdir()
        self.config_path = Path(self.tmpdir.name) / "instinct_promotion_config.json"
        self.config_path.write_text(
            json.dumps(
                {
                    "min_confidence": 0.8,
                    "min_observations": 2,
                    "allow_scopes": ["global", "project"],
                    "allow_source_kinds": ["learned", "system"],
                    "report_dir": str(self.report_dir),
                }
            ),
            encoding="utf-8",
        )
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript(SCHEMA)

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_promote_instinct_creates_skill_and_marks_instinct(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO instincts
                (instinct_key, summary, trigger_pattern, observation, action, confidence, scope, project_key, observation_count, model)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    "arteon-context-first",
                    "ARTEON requests should load ARTEON context first.",
                    "arteon brand wildlens",
                    "Brand and Wildlens requests repeatedly map to ARTEON.",
                    "Resolve project_key=02_ARTEON before searching skills.",
                    0.9,
                    "project",
                    "02_ARTEON",
                    3,
                    "gpt-5",
                ),
            )
            conn.commit()

        with mock.patch.object(instinct_promote, "DB_PATH", self.db_path):
            promoted = instinct_promote.promote_instincts(min_confidence=0.8, min_observations=2)

        self.assertEqual(promoted["promoted"], ["arteon-context-first"])
        with sqlite3.connect(self.db_path) as conn:
            skill = conn.execute(
                "SELECT title, source_kind, confidence, scope, project_key FROM skills WHERE trigger_pattern = ?",
                ("arteon brand wildlens",),
            ).fetchone()
            instinct = conn.execute(
                "SELECT status, source_ref FROM instincts WHERE instinct_key = ?",
                ("arteon-context-first",),
            ).fetchone()

        self.assertEqual(skill, ("ARTEON requests should load ARTEON context first.", "promoted-instinct", 0.9, "project", "02_ARTEON"))
        self.assertEqual(instinct, ("promoted", "skill:arteon brand wildlens"))

    def test_promotion_updates_existing_skill_instead_of_duplicating(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO instincts
                (instinct_key, summary, trigger_pattern, observation, action, confidence, scope, project_key, observation_count, model)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    "pka-canonical-first",
                    "Canonical sources should be changed before overlays.",
                    "pka overlay canonical generate drift",
                    "Overlay fixes should begin from the canonical config.",
                    "Edit canonical sources first, then regenerate pointers.",
                    0.92,
                    "project",
                    "PKA",
                    4,
                    "gpt-5",
                ),
            )
            conn.execute(
                """
                INSERT INTO skills
                (title, trigger_pattern, specialist, procedure, context, source_kind, confidence, scope, project_key)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    "Old title",
                    "pka overlay canonical generate drift",
                    "Forge",
                    "Old procedure",
                    "Old context",
                    "manual",
                    0.7,
                    "project",
                    "PKA",
                ),
            )
            conn.commit()

        with mock.patch.object(instinct_promote, "DB_PATH", self.db_path):
            promoted = instinct_promote.promote_instincts(min_confidence=0.8, min_observations=2)

        self.assertEqual(promoted["promoted"], ["pka-canonical-first"])
        with sqlite3.connect(self.db_path) as conn:
            count = conn.execute("SELECT COUNT(*) FROM skills WHERE trigger_pattern = ?", ("pka overlay canonical generate drift",)).fetchone()[0]
            skill = conn.execute(
                "SELECT title, source_kind, confidence FROM skills WHERE trigger_pattern = ?",
                ("pka overlay canonical generate drift",),
            ).fetchone()

        self.assertEqual(count, 1)
        self.assertEqual(skill, ("Canonical sources should be changed before overlays.", "promoted-instinct", 0.92))

    def test_promotion_respects_thresholds(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO instincts
                (instinct_key, summary, trigger_pattern, observation, action, confidence, scope, project_key, observation_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    "weak-instinct",
                    "Weak instinct",
                    "weak trigger",
                    "Single observation",
                    "Do something",
                    0.7,
                    "global",
                    None,
                    1,
                ),
            )
            conn.commit()

        with mock.patch.object(instinct_promote, "DB_PATH", self.db_path):
            promoted = instinct_promote.promote_instincts(min_confidence=0.8, min_observations=2)

        self.assertEqual(promoted["promoted"], [])
        with sqlite3.connect(self.db_path) as conn:
            skill_count = conn.execute("SELECT COUNT(*) FROM skills").fetchone()[0]
            status = conn.execute("SELECT status FROM instincts WHERE instinct_key = ?", ("weak-instinct",)).fetchone()[0]

        self.assertEqual(skill_count, 0)
        self.assertEqual(status, "active")

    def test_config_driven_run_writes_report(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO instincts
                (instinct_key, summary, trigger_pattern, observation, action, confidence, scope, project_key, observation_count, source_kind)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    "pka-canonical-first",
                    "Canonical first",
                    "pka overlay canonical",
                    "Observed repeatedly",
                    "Edit canonical first",
                    0.91,
                    "project",
                    "PKA",
                    3,
                    "system",
                ),
            )
            conn.commit()

        with (
            mock.patch.object(instinct_promote, "DB_PATH", self.db_path),
            mock.patch.object(instinct_promote, "CONFIG_PATH", self.config_path),
        ):
            result = instinct_promote.run_promotion_from_config(write_report=True)

        self.assertEqual(result["promoted"], ["pka-canonical-first"])
        reports = list(self.report_dir.glob("*_instinct_promotion.md"))
        self.assertEqual(len(reports), 1)
        text = reports[0].read_text(encoding="utf-8")
        self.assertIn("pka-canonical-first", text)
        self.assertIn("Promoted Instincts", text)


if __name__ == "__main__":
    unittest.main()
