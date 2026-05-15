import tempfile
import unittest
from pathlib import Path
from unittest import mock
import sqlite3
import json

from scripts import pka_system_improvement_audit


class PkaSystemImprovementAuditTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        (self.root / "TEAM").mkdir()
        (self.root / "scripts").mkdir()
        with sqlite3.connect(self.root / "TEAM" / "team.db") as conn:
            conn.execute("CREATE TABLE members (status TEXT)")
            conn.executemany("INSERT INTO members (status) VALUES (?)", [("active",)] * 25)
            conn.execute("CREATE TABLE skills (id INTEGER PRIMARY KEY, title TEXT)")
            conn.commit()
        (self.root / "CLAUDE.md").write_text("25 membres actifs", encoding="utf-8")
        (self.root / "AGENTS.md").write_text("25 membres actifs", encoding="utf-8")
        (self.root / "GEMINI.md").write_text("24 membres actifs", encoding="utf-8")
        (self.root / "DEEPSEEK.md").write_text("25 membres actifs", encoding="utf-8")
        (self.root / "ADAPTER-PROMPT.md").write_text("25 membres actifs", encoding="utf-8")
        (self.root / ".claude").mkdir()
        (self.root / ".claude" / "settings.local.json").write_text('{"hooks": {}}', encoding="utf-8")
        (self.root / "JCH_Inbox" / "99_SYSTEM").mkdir(parents=True)
        (self.root / "JCH_Inbox" / "03_PROJECTS").mkdir(parents=True)
        (self.root / "JCH_Inbox" / "00_INBOX").mkdir(parents=True)
        config = {
            "identity_intro": ["You are Dobby.", "The {specialist_count} specialists are delegated."],
            "source_of_truth": ["`MEMORY.md`"],
            "operating_protocol": "See `ADAPTER-PROMPT.md`.",
            "activation_lines": [
                "**TOOL :** {tool_label}",
                "**MODEL :** {model_hint}",
                "**TEAM :** {team_count} membres actifs — {specialist_count} spécialistes + Dobby"
            ],
            "tools": {
                "AGENTS.md": {"title": "AGENTS.md — Pointer", "tool_label": "Codex CLI", "model_hint": "(model)"},
                "GEMINI.md": {"title": "GEMINI.md — Pointer", "tool_label": "Gemini CLI", "model_hint": "(model)"},
                "DEEPSEEK.md": {"title": "DEEPSEEK.md — Pointer", "tool_label": "DeepSeek API", "model_hint": "(model)"}
            }
        }
        (self.root / "JCH_Inbox" / "99_SYSTEM" / "tool_pointer_config.json").write_text(json.dumps(config), encoding="utf-8")

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

    def test_pointer_generation_drift_is_reported(self):
        with mock.patch.object(pka_system_improvement_audit, "ROOT", self.root):
            findings = pka_system_improvement_audit.check_pointer_generation_drift()

        self.assertTrue(any(item["check"] == "pointer-generation" for item in findings))


if __name__ == "__main__":
    unittest.main()
