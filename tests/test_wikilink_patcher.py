import sqlite3
import tempfile
import unittest
from pathlib import Path

from scripts.modules import wikilink_patcher


class WikilinkPatcherTest(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        db_path = self.root / "TEAM" / "team.db"
        db_path.parent.mkdir(parents=True)
        with sqlite3.connect(db_path) as conn:
            conn.execute("CREATE TABLE members (name TEXT, status TEXT)")
            conn.execute("INSERT INTO members VALUES ('Forge', 'active')")
            conn.execute("INSERT INTO members VALUES ('Vasco', 'active')")
            conn.execute("INSERT INTO members VALUES ('Corbeau', 'inactive')")
        self.db_path = db_path

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_load_active_members(self):
        members = wikilink_patcher.load_active_members(self.db_path)
        self.assertIn("Forge", members)
        self.assertIn("Vasco", members)
        self.assertNotIn("Corbeau", members)

    def test_patch_member_mention(self):
        text = "J'ai demandé à Forge de vérifier le pipeline."
        result = wikilink_patcher.patch_text(text, members=["Forge", "Vasco"], known_files=[])
        self.assertIn("[[Forge]]", result)
        self.assertNotIn("[[Vasco]]", result)

    def test_no_double_wrap(self):
        text = "[[Forge]] a livré le rapport."
        result = wikilink_patcher.patch_text(text, members=["Forge"], known_files=[])
        self.assertEqual(result.count("[[Forge]]"), 1)

    def test_skip_code_block(self):
        text = "```\nForge est mentionné ici\n```"
        result = wikilink_patcher.patch_text(text, members=["Forge"], known_files=[])
        self.assertNotIn("[[Forge]]", result)

    def test_skip_url(self):
        text = "Voir https://example.com/Forge pour les détails."
        result = wikilink_patcher.patch_text(text, members=["Forge"], known_files=[])
        self.assertNotIn("[[Forge]]", result)

    def test_patch_known_file_reference(self):
        text = "Consulter pka_system_check pour l'audit."
        result = wikilink_patcher.patch_text(
            text, members=[], known_files=["pka_system_check"]
        )
        self.assertIn("[[pka_system_check]]", result)

    def test_patch_file_writes_to_disk(self):
        md_file = self.root / "note.md"
        md_file.write_text("Forge a livré.", encoding="utf-8")
        modified = wikilink_patcher.patch_file(
            md_file, members=["Forge"], known_files=[]
        )
        self.assertTrue(modified)
        self.assertIn("[[Forge]]", md_file.read_text(encoding="utf-8"))

    def test_excluded_files_not_touched(self):
        excluded = self.root / "CLAUDE.md"
        excluded.write_text("Forge travaille ici.", encoding="utf-8")
        modified = wikilink_patcher.patch_file(
            excluded, members=["Forge"], known_files=[]
        )
        self.assertFalse(modified)
        self.assertNotIn("[[Forge]]", excluded.read_text(encoding="utf-8"))
