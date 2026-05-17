import contextlib
import io
import os
import sqlite3
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest import mock

from scripts import rebuild_file_index


class RebuildFileIndexTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        self.db_path = self.root / "TEAM" / "team.db"
        (self.root / "TEAM").mkdir()
        (self.root / "TEAM_Inbox").mkdir()
        (self.root / "wiki").mkdir()
        (self.root / "docs").mkdir()
        (self.root / "scripts").mkdir()
        (self.root / "JCH_Inbox" / "03_PROJECTS" / "03_WILDNEXUS" / "03.01 BIOACOUSTIC").mkdir(parents=True)
        (self.root / "JCH_Inbox" / "03_PROJECTS" / "03_WILDNEXUS" / "03.02 FAUNE_AUTOUR_APP" / "source").mkdir(parents=True)
        (self.root / "node_modules").mkdir()
        (self.root / ".git").mkdir()

        (self.root / "JCH_Inbox" / "03_PROJECTS" / "03_WILDNEXUS" / "03.01 BIOACOUSTIC" / "brief.md").write_text(
            "bioacoustic brief",
            encoding="utf-8",
        )
        (self.root / "JCH_Inbox" / "03_PROJECTS" / "03_WILDNEXUS" / "03.02 FAUNE_AUTOUR_APP" / "source" / "faune-autour_13.html").write_text(
            "<html></html>",
            encoding="utf-8",
        )
        (self.root / "TEAM_Inbox" / "2026-05-16_castor_audit.md").write_text("audit", encoding="utf-8")
        (self.root / "scripts" / "tool.py").write_text("print('ok')\n", encoding="utf-8")
        (self.root / "wiki" / "note.md").write_text("knowledge", encoding="utf-8")
        (self.root / "wiki" / ".DS_Store").write_text("junk", encoding="utf-8")
        (self.root / "node_modules" / "ignored.js").write_text("ignored", encoding="utf-8")
        (self.root / "docs" / "~$draft.docx").write_text("tmp", encoding="utf-8")

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                """
                CREATE TABLE file_index (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    file_path TEXT NOT NULL UNIQUE,
                    file_type TEXT,
                    size_bytes INTEGER,
                    description TEXT,
                    tags TEXT,
                    owner TEXT,
                    linked_member TEXT,
                    inbox_direction TEXT,
                    indexed_on TEXT NOT NULL DEFAULT (datetime('now')),
                    last_modified TEXT
                )
                """
            )
            conn.execute(
                """
                INSERT INTO file_index (filename, file_path, file_type, size_bytes, description, tags, owner, linked_member, inbox_direction, last_modified)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    "legacy.md",
                    "/old/path/legacy.md",
                    "markdown",
                    123,
                    "legacy row",
                    "legacy",
                    "",
                    "",
                    "JCH_Inbox",
                    "2026-05-01 00:00:00",
                ),
            )
            conn.execute("CREATE INDEX idx_file_index_inbox_dir ON file_index(inbox_direction)")
            conn.commit()

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_rebuild_archives_legacy_table_and_indexes_live_files(self):
        report = rebuild_file_index.rebuild_index(self.root, self.db_path, "2026_05_16")

        self.assertEqual(report["legacy_rows"], 1)
        self.assertEqual(report["indexed_rows"], 5)
        self.assertIn("file_index_legacy_2026_05_16", report["archived_table"])

        with sqlite3.connect(self.db_path) as conn:
            tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            self.assertIn("file_index", tables)
            self.assertIn("file_index_legacy_2026_05_16", tables)
            paths = {
                row[0]
                for row in conn.execute("SELECT file_path FROM file_index ORDER BY file_path")
            }

        self.assertEqual(
            paths,
            {
                "JCH_Inbox/03_PROJECTS/03_WILDNEXUS/03.01 BIOACOUSTIC/brief.md",
                "JCH_Inbox/03_PROJECTS/03_WILDNEXUS/03.02 FAUNE_AUTOUR_APP/source/faune-autour_13.html",
                "TEAM/team.db",
                "TEAM_Inbox/2026-05-16_castor_audit.md",
                "wiki/note.md",
            },
        )

    def test_rebuild_derives_project_metadata_and_excludes_ignored_files(self):
        rebuild_file_index.rebuild_index(self.root, self.db_path, "2026_05_16")

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            app_row = conn.execute(
                "SELECT file_type, category, project_key, component, inbox_direction, exists_on_disk, status FROM file_index WHERE filename = ?",
                ("faune-autour_13.html",),
            ).fetchone()
            ignored = conn.execute(
                "SELECT COUNT(*) FROM file_index WHERE filename IN ('.DS_Store', '~$draft.docx', 'ignored.js', 'tool.py')"
            ).fetchone()[0]

        self.assertEqual(app_row["file_type"], "html")
        self.assertEqual(app_row["category"], "app_source")
        self.assertEqual(app_row["project_key"], "03_WILDNEXUS")
        self.assertEqual(app_row["component"], "03.02 FAUNE_AUTOUR_APP")
        self.assertEqual(app_row["inbox_direction"], "JCH_Inbox")
        self.assertEqual(app_row["exists_on_disk"], 1)
        self.assertEqual(app_row["status"], "active")
        self.assertEqual(ignored, 0)

    def test_rebuild_does_not_overwrite_existing_archive_table(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("CREATE TABLE file_index_legacy_2026_05_16 (value TEXT)")
            conn.execute("INSERT INTO file_index_legacy_2026_05_16 (value) VALUES ('keep-me')")
            conn.commit()

        report = rebuild_file_index.rebuild_index(self.root, self.db_path, "2026_05_16")

        self.assertEqual(report["archived_table"], "file_index_legacy_2026_05_16_1")
        with sqlite3.connect(self.db_path) as conn:
            original = conn.execute("SELECT value FROM file_index_legacy_2026_05_16").fetchone()[0]
            tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")}

        self.assertEqual(original, "keep-me")
        self.assertIn("file_index_legacy_2026_05_16_1", tables)

    def test_rebuild_enriches_management_roots_with_pka_project_metadata(self):
        rebuild_file_index.rebuild_index(self.root, self.db_path, "2026_05_16")

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            team_row = conn.execute(
                "SELECT project_key, component, category FROM file_index WHERE file_path = 'TEAM/team.db'"
            ).fetchone()
            wiki_row = conn.execute(
                "SELECT project_key, component, category FROM file_index WHERE file_path = 'wiki/note.md'"
            ).fetchone()
            inbox_row = conn.execute(
                "SELECT project_key, component, category FROM file_index WHERE file_path = 'TEAM_Inbox/2026-05-16_castor_audit.md'"
            ).fetchone()

        self.assertEqual(team_row["project_key"], "PKA")
        self.assertEqual(team_row["component"], "TEAM")
        self.assertEqual(team_row["category"], "team_system")
        self.assertEqual(wiki_row["project_key"], "PKA")
        self.assertEqual(wiki_row["component"], "wiki")
        self.assertEqual(wiki_row["category"], "wiki")
        self.assertEqual(inbox_row["project_key"], "PKA")
        self.assertEqual(inbox_row["component"], "TEAM_Inbox")
        self.assertEqual(inbox_row["category"], "team_deliverable")

    def test_incremental_rescan_adds_updates_and_marks_deleted_files(self):
        rebuild_file_index.rebuild_index(self.root, self.db_path, "2026_05_16")

        target = self.root / "JCH_Inbox" / "03_PROJECTS" / "03_WILDNEXUS" / "03.01 BIOACOUSTIC" / "brief.md"
        target.write_text("bioacoustic brief updated", encoding="utf-8")
        future = datetime.now() + timedelta(minutes=5)
        timestamp = future.timestamp()
        os.utime(target, (timestamp, timestamp))

        new_file = self.root / "JCH_Inbox" / "03_PROJECTS" / "03_WILDNEXUS" / "03.01 BIOACOUSTIC" / "new-note.md"
        new_file.write_text("new", encoding="utf-8")
        deleted = self.root / "wiki" / "note.md"
        deleted.unlink()

        report = rebuild_file_index.rescan_index(self.root, self.db_path)

        self.assertEqual(report["inserted"], 1)
        self.assertEqual(report["marked_missing"], 1)

        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            updated = conn.execute(
                "SELECT size_bytes, exists_on_disk FROM file_index WHERE file_path = ?",
                ("JCH_Inbox/03_PROJECTS/03_WILDNEXUS/03.01 BIOACOUSTIC/brief.md",),
            ).fetchone()
            inserted = conn.execute(
                "SELECT exists_on_disk FROM file_index WHERE file_path = ?",
                ("JCH_Inbox/03_PROJECTS/03_WILDNEXUS/03.01 BIOACOUSTIC/new-note.md",),
            ).fetchone()
            missing = conn.execute(
                "SELECT exists_on_disk, status FROM file_index WHERE file_path = ?",
                ("wiki/note.md",),
            ).fetchone()

        self.assertEqual(updated["size_bytes"], len("bioacoustic brief updated"))
        self.assertEqual(updated["exists_on_disk"], 1)
        self.assertEqual(inserted["exists_on_disk"], 1)
        self.assertEqual(missing["exists_on_disk"], 0)
        self.assertEqual(missing["status"], "reference")

    def test_search_returns_ranked_matches_and_supports_project_filter(self):
        rebuild_file_index.rebuild_index(self.root, self.db_path, "2026_05_16")

        results = rebuild_file_index.search_index(self.db_path, "faune")
        filtered = rebuild_file_index.search_index(self.db_path, "brief", project_key="03_WILDNEXUS")

        self.assertEqual(results[0]["filename"], "faune-autour_13.html")
        self.assertEqual(filtered[0]["project_key"], "03_WILDNEXUS")
        self.assertEqual(filtered[0]["filename"], "brief.md")

    def test_search_supports_component_filter(self):
        rebuild_file_index.rebuild_index(self.root, self.db_path, "2026_05_16")

        results = rebuild_file_index.search_index(
            self.db_path,
            "faune",
            project_key="03_WILDNEXUS",
            component="03.02 FAUNE_AUTOUR_APP",
        )

        self.assertEqual(results[0]["component"], "03.02 FAUNE_AUTOUR_APP")

    def test_search_escapes_like_wildcards_in_query(self):
        rebuild_file_index.rebuild_index(self.root, self.db_path, "2026_05_16")

        results = rebuild_file_index.search_index(self.db_path, "%_")

        self.assertEqual(results, [])

    def test_search_excludes_archived_rows_even_if_they_exist_on_disk(self):
        rebuild_file_index.rebuild_index(self.root, self.db_path, "2026_05_16")

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "UPDATE file_index SET status = 'archived' WHERE file_path = ?",
                ("JCH_Inbox/03_PROJECTS/03_WILDNEXUS/03.02 FAUNE_AUTOUR_APP/source/faune-autour_13.html",),
            )
            conn.commit()

        results = rebuild_file_index.search_index(self.db_path, "faune")

        self.assertEqual(results, [])

    def test_available_filters_lists_projects_and_components(self):
        rebuild_file_index.rebuild_index(self.root, self.db_path, "2026_05_16")

        filters = rebuild_file_index.available_filters(self.db_path)

        self.assertIn("03_WILDNEXUS", filters["projects"])
        self.assertIn("03.01 BIOACOUSTIC", filters["components"]["03_WILDNEXUS"])

    def test_available_filters_excludes_archived_content(self):
        rebuild_file_index.rebuild_index(self.root, self.db_path, "2026_05_16")

        with sqlite3.connect(self.db_path) as conn:
            conn.execute("UPDATE file_index SET status = 'archived' WHERE component = ?", ("03.01 BIOACOUSTIC",))
            conn.commit()

        filters = rebuild_file_index.available_filters(self.db_path)

        self.assertIn("03_WILDNEXUS", filters["projects"])
        self.assertNotIn("03.01 BIOACOUSTIC", filters["components"]["03_WILDNEXUS"])
        self.assertIn("03.02 FAUNE_AUTOUR_APP", filters["components"]["03_WILDNEXUS"])

    def test_search_cli_accepts_component_filter(self):
        rebuild_file_index.rebuild_index(self.root, self.db_path, "2026_05_16")

        stdout = io.StringIO()
        argv = [
            "rebuild_file_index.py",
            "search",
            "faune",
            "--db",
            str(self.db_path),
            "--project-key",
            "03_WILDNEXUS",
            "--component",
            "03.02 FAUNE_AUTOUR_APP",
        ]
        with mock.patch.object(sys, "argv", argv):
            with contextlib.redirect_stdout(stdout):
                exit_code = rebuild_file_index.main()

        self.assertEqual(exit_code, 0)
        self.assertIn("03.02 FAUNE_AUTOUR_APP", stdout.getvalue())
        self.assertNotIn("brief.md", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
