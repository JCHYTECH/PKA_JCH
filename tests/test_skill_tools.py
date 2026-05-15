import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import skill_search, skill_write


SKILLS_SCHEMA = """
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


class SkillToolsTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.tmpdir.name) / "team.db"
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript(SKILLS_SCHEMA)

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_write_skill_persists_new_metadata(self):
        with mock.patch.object(skill_write, "DB_PATH", self.db_path):
            skill_write.write_skill(
                title="PKA improvement",
                trigger_pattern="improve pka",
                procedure="Inspect local system first.",
                specialist="Forge",
                context="When improving PKA",
                source_kind="system",
                confidence=0.9,
                scope="tool",
                project_key="PKA",
                model="gpt-5",
            )

        with sqlite3.connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT source_kind, confidence, scope, project_key, model FROM skills WHERE trigger_pattern = ?",
                ("improve pka",),
            ).fetchone()

        self.assertEqual(row, ("system", 0.9, "tool", "PKA", "gpt-5"))

    def test_search_skills_orders_project_scope_before_global(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO skills
                (title, trigger_pattern, specialist, procedure, context, usage_count, scope, project_key)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                ("Global skill", "improve pka", "Forge", "Global procedure", "global", 1, "global", None),
            )
            conn.execute(
                """
                INSERT INTO skills
                (title, trigger_pattern, specialist, procedure, context, usage_count, scope, project_key)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                ("Project skill", "improve pka", "Forge", "Project procedure", "project", 1, "project", "PKA"),
            )
            conn.commit()

        with mock.patch.object(skill_search, "DB_PATH", self.db_path):
            rows = skill_search.search_skills("improve pka", limit=5, project_key="PKA")

        self.assertEqual(rows[0]["title"], "Project skill")
        self.assertEqual(rows[1]["title"], "Global skill")

    def test_search_skills_can_infer_project_key_from_context_profile(self):
        profile = {"project_key": "02_ARTEON", "label": "ARTEON"}
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO skills
                (title, trigger_pattern, specialist, procedure, context, usage_count, scope, project_key)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                ("ARTEON skill", "arteon brand", "Vega", "ARTEON procedure", "arteon", 1, "project", "02_ARTEON"),
            )
            conn.commit()

        with (
            mock.patch.object(skill_search, "DB_PATH", self.db_path),
            mock.patch.object(skill_search, "infer_project_key", return_value=profile["project_key"]),
        ):
            rows = skill_search.search_skills("arteon brand refresh", limit=5)

        self.assertEqual(rows[0]["project_key"], "02_ARTEON")


if __name__ == "__main__":
    unittest.main()
