import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import pka_kanban_bootstrap


class PkaKanbanBootstrapTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        (self.root / "JCH_Inbox" / "03_PROJECTS").mkdir(parents=True)
        for name in ("08_VETALYX", "01_AI_IT_TOOLS", "02_ARTEON"):
            (self.root / "JCH_Inbox" / "03_PROJECTS" / name).mkdir()
        (self.root / "JCH_Inbox" / "03_PROJECTS" / "README.txt").write_text("ignore me", encoding="utf-8")

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_build_manifest_lists_all_project_boards_sorted_by_name(self):
        with mock.patch.object(pka_kanban_bootstrap, "ROOT", self.root):
            manifest = pka_kanban_bootstrap.build_manifest()

        self.assertEqual(
            manifest,
            {
                "projects": [
                    {"key": "01_AI_IT_TOOLS", "name": "01_AI_IT_TOOLS"},
                    {"key": "02_ARTEON", "name": "02_ARTEON"},
                    {"key": "08_VETALYX", "name": "08_VETALYX"},
                ]
            },
        )


if __name__ == "__main__":
    unittest.main()
