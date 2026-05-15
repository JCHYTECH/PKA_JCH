import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import generate_tool_pointers


class GenerateToolPointersTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        (self.root / "TEAM").mkdir()
        (self.root / "JCH_Inbox" / "99_SYSTEM").mkdir(parents=True)
        (self.root / "JCH_Inbox" / "03_PROJECTS").mkdir(parents=True)
        (self.root / "JCH_Inbox" / "00_INBOX").mkdir(parents=True)
        (self.root / "JCH_Inbox" / "03_PROJECTS" / "01_AI_IT_TOOLS").mkdir()
        (self.root / "JCH_Inbox" / "03_PROJECTS" / "02_ARTEON").mkdir()
        (self.root / "JCH_Inbox" / "00_INBOX" / "a.txt").write_text("x", encoding="utf-8")
        with sqlite3.connect(self.root / "TEAM" / "team.db") as conn:
            conn.execute("CREATE TABLE members (status TEXT)")
            conn.executemany("INSERT INTO members (status) VALUES (?)", [("active",)] * 25)
            conn.commit()
        (self.root / "CLAUDE.md").write_text(
            "# CLAUDE\n\n<!-- PKA:CANONICAL-START -->\nold\n<!-- PKA:CANONICAL-END -->\n\nrest",
            encoding="utf-8",
        )
        config = {
            "identity_intro": [
                "You are Dobby.",
                "The {specialist_count} specialists are delegated."
            ],
            "source_of_truth": ["`MEMORY.md`"],
            "operating_protocol": "See `ADAPTER-PROMPT.md`.",
            "activation_lines": [
                "**TOOL :** {tool_label}",
                "**MODEL :** {model_hint}",
                "**TEAM :** {team_count} membres actifs — {specialist_count} spécialistes + Dobby"
            ],
            "tools": {
                "AGENTS.md": {
                    "title": "AGENTS.md — Pointer",
                    "tool_label": "Codex CLI",
                    "model_hint": "(model in use)"
                }
            }
        }
        (self.root / "JCH_Inbox" / "99_SYSTEM" / "tool_pointer_config.json").write_text(
            json.dumps(config), encoding="utf-8"
        )

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_generate_writes_pointer_with_live_counts(self):
        with (
            mock.patch.object(generate_tool_pointers, "ROOT", self.root),
            mock.patch.object(generate_tool_pointers, "DB_PATH", self.root / "TEAM" / "team.db"),
            mock.patch.object(generate_tool_pointers, "CONFIG_PATH", self.root / "JCH_Inbox" / "99_SYSTEM" / "tool_pointer_config.json"),
            mock.patch.object(generate_tool_pointers, "PROJECTS_DIR", self.root / "JCH_Inbox" / "03_PROJECTS"),
            mock.patch.object(generate_tool_pointers, "INBOX_DIR", self.root / "JCH_Inbox" / "00_INBOX"),
        ):
            rc = generate_tool_pointers.generate(check=False)

        self.assertEqual(rc, 0)
        text = (self.root / "AGENTS.md").read_text(encoding="utf-8")
        self.assertIn("25 membres actifs — 24 spécialistes + Dobby", text)
        self.assertIn("2 projets actifs", text)
        self.assertIn("1 éléments", text)
        claude_text = (self.root / "CLAUDE.md").read_text(encoding="utf-8")
        self.assertIn("## Canonical PKA Overlay", claude_text)
        self.assertIn("25 membres actifs — 24 spécialistes + Dobby", claude_text)
        self.assertIn("rest", claude_text)

    def test_check_reports_drift(self):
        (self.root / "AGENTS.md").write_text("old content", encoding="utf-8")
        with (
            mock.patch.object(generate_tool_pointers, "ROOT", self.root),
            mock.patch.object(generate_tool_pointers, "DB_PATH", self.root / "TEAM" / "team.db"),
            mock.patch.object(generate_tool_pointers, "CONFIG_PATH", self.root / "JCH_Inbox" / "99_SYSTEM" / "tool_pointer_config.json"),
            mock.patch.object(generate_tool_pointers, "PROJECTS_DIR", self.root / "JCH_Inbox" / "03_PROJECTS"),
            mock.patch.object(generate_tool_pointers, "INBOX_DIR", self.root / "JCH_Inbox" / "00_INBOX"),
        ):
            rc = generate_tool_pointers.generate(check=True)

        self.assertEqual(rc, 1)

    def test_check_reports_claude_managed_block_drift(self):
        with (
            mock.patch.object(generate_tool_pointers, "ROOT", self.root),
            mock.patch.object(generate_tool_pointers, "DB_PATH", self.root / "TEAM" / "team.db"),
            mock.patch.object(generate_tool_pointers, "CONFIG_PATH", self.root / "JCH_Inbox" / "99_SYSTEM" / "tool_pointer_config.json"),
            mock.patch.object(generate_tool_pointers, "PROJECTS_DIR", self.root / "JCH_Inbox" / "03_PROJECTS"),
            mock.patch.object(generate_tool_pointers, "INBOX_DIR", self.root / "JCH_Inbox" / "00_INBOX"),
        ):
            rc = generate_tool_pointers.generate(check=True)

        self.assertEqual(rc, 1)


if __name__ == "__main__":
    unittest.main()
