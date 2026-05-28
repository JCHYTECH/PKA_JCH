# PKA System Improvement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a transversal PKA system-improvement audit, enrich the skills metadata model, and register a reusable skill for future PKA evolution requests.

**Architecture:** Keep the current PKA structure intact and extend it with one focused audit script, one backward-compatible [[SQLite]] migration, small updates to the existing skill read/write scripts, and one registered skill row in 

**Tech Stack:** [[Python]] 3, [[SQLite]], Markdown specs/plans, existing PKA scripts in 

---

### Task 1: Add regression tests for the skills metadata upgrade

**Files:**
- Create: `tests/test_skill_tools.py`
- Test: `tests/test_skill_tools.py`

- [ ] **Step 1: Write the failing tests**

```python
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import skill_search, skill_write


class SkillToolsTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.tmpdir.name) / "team.db"
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript(
                """
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
            )

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


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_skill_tools -v`
Expected: FAIL because `write_skill()` and `search_skills()` do not yet support the new metadata arguments and project-aware ordering.

- [ ] **Step 3: Write minimal implementation**

Add support in `scripts/skill_write.py` and `scripts/skill_search.py` for:
- metadata fields: `source_kind`, `confidence`, `scope`, `project_key`, `model`
- project-aware ranking that prefers matching project-scoped rows before global ones

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_skill_tools -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/test_skill_tools.py scripts/skill_write.py scripts/skill_search.py
git commit -m "feat: enrich pka skills metadata"
```

### Task 2: Add regression tests for the system-improvement audit

**Files:**
- Create: `tests/test_pka_system_improvement_audit.py`
- Test: `tests/test_pka_system_improvement_audit.py`

- [ ] **Step 1: Write the failing tests**

```python
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import pka_system_improvement_audit


class PkaSystemImprovementAuditTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        (self.root / "TEAM").mkdir()
        (self.root / "scripts").mkdir()
        (self.root / "CLAUDE.md").write_text("25 membres actifs", encoding="utf-8")
        (self.root / "AGENTS.md").write_text("25 membres actifs", encoding="utf-8")
        (self.root / "GEMINI.md").write_text("24 membres actifs", encoding="utf-8")
        (self.root / "ADAPTER-PROMPT.md").write_text("25 membres actifs", encoding="utf-8")

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_overlay_drift_is_reported(self):
        with mock.patch.object(pka_system_improvement_audit, "ROOT", self.root):
            findings = pka_system_improvement_audit.check_instruction_surface()

        self.assertTrue(any(item["check"] == "instruction-surface" for item in findings))

    def test_quick_wins_are_emitted(self):
        result = {
            "generated_at": "2026-05-14T12:00:00",
            "status": "orange",
            "findings": [
                {
                    "severity": "medium",
                    "check": "instruction-surface",
                    "path": "GEMINI.md",
                    "detail": "count drift",
                    "mitigation": "sync overlay",
                    "quick_win": True,
                }
            ],
        }
        markdown = pka_system_improvement_audit.markdown_report(result)
        self.assertIn("Quick Wins", markdown)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m unittest tests.test_pka_system_improvement_audit -v`
Expected: FAIL because `scripts/pka_system_improvement_audit.py` does not exist yet.

- [ ] **Step 3: Write minimal implementation**

Create `scripts/pka_system_improvement_audit.py` with:
- local instruction-surface checks
- script presence checks
- hook coverage checks
- skills metadata coverage checks
- markdown and JSON output

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m unittest tests.test_pka_system_improvement_audit -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add tests/test_pka_system_improvement_audit.py scripts/pka_system_improvement_audit.py
git commit -m "feat: add pka system improvement audit"
```

### Task 3: Apply the schema migration and register the skill

**Files:**
- Modify: `TEAM/team.db`
- Create: `scripts/migrate_skills_metadata.py`

- [ ] **Step 1: Write a migration script**

```python
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "TEAM" / "team.db"


def add_column(conn, sql):
    try:
        conn.execute(sql)
    except sqlite3.OperationalError as exc:
        if "duplicate column name" not in str(exc).lower():
            raise


with sqlite3.connect(DB_PATH) as conn:
    add_column(conn, "ALTER TABLE skills ADD COLUMN source_kind TEXT DEFAULT 'manual'")
    add_column(conn, "ALTER TABLE skills ADD COLUMN confidence REAL DEFAULT 0.7")
    add_column(conn, "ALTER TABLE skills ADD COLUMN scope TEXT DEFAULT 'global'")
    add_column(conn, "ALTER TABLE skills ADD COLUMN project_key TEXT")
    add_column(conn, "ALTER TABLE skills ADD COLUMN updated_at DATE DEFAULT CURRENT_DATE")
    conn.commit()
```

- [ ] **Step 2: Run migration**

Run: `python3 scripts/migrate_skills_metadata.py`
Expected: exit 0

- [ ] **Step 3: Register the skill in `TEAM/team.db`**

Insert a `skills` row for `pka-system-improvement` with:
- `trigger_pattern`: phrases around improving PKA, system evolution, and useful external adaptations
- `procedure`: the validated staged workflow from the design
- `source_kind`: `system`
- `confidence`: `0.9`
- `scope`: `global`
- `project_key`: `PKA`

- [ ] **Step 4: Verify schema and row**

Run: `sqlite3 TEAM/team.db "SELECT source_kind, confidence, scope, project_key FROM skills WHERE trigger_pattern LIKE '%pka-system-improvement%' OR title='pka-system-improvement';"`
Expected: one row with the expected metadata

- [ ] **Step 5: Commit**

```bash
git add scripts/migrate_skills_metadata.py TEAM/team.db
git commit -m "feat: register pka system improvement skill"
```

### Task 4: Run end-to-end verification

**Files:**
- Modify: `docs/superpowers/specs/2026-05-14-pka-system-improvement-design.md` (only if verification reveals a mismatch)

- [ ] **Step 1: Run the full unit test set**

Run: `python3 -m unittest tests.test_skill_tools tests.test_pka_system_improvement_audit -v`
Expected: PASS

- [ ] **Step 2: Run the new audit script**

Run: `python3 scripts/pka_system_improvement_audit.py`
Expected: Markdown report printed with status, findings, quick wins, and next steps

- [ ] **Step 3: Verify the skill retrieval path**

Run: `python3 scripts/skill_search.py "amélioration système PKA adaptation repo efficacité Dobby" --limit 5`
Expected: output includes `pka-system-improvement`

- [ ] **Step 4: Record any required documentation adjustments**

If the implementation deviates from the design, update:
- `docs/superpowers/specs/2026-05-14-pka-system-improvement-design.md`

- [ ] **Step 5: Commit**

```bash
git add tests/ scripts/ docs/superpowers/specs/2026-05-14-pka-system-improvement-design.md TEAM/team.db
git commit -m "test: verify pka system improvement workflow"
```
