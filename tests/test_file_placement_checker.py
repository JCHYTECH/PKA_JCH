import tempfile
import unittest
from pathlib import Path

from scripts.modules import file_placement_checker


class FilePlacementCheckerTest(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)

    def tearDown(self):
        self.tmpdir.cleanup()

    def _create(self, rel: str) -> Path:
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.touch()
        return p

    def test_daily_note_in_wrong_place(self):
        self._create("JCH_Inbox/03_PROJECTS/2026-05-28_daily.md")
        anomalies = file_placement_checker.check(self.root)
        paths = [a["path"] for a in anomalies]
        self.assertTrue(any("2026-05-28_daily.md" in p for p in paths))

    def test_daily_note_in_correct_place(self):
        self._create("JCH_Inbox/01_DASHBOARDS/2026-05-28_daily.md")
        anomalies = file_placement_checker.check(self.root)
        paths = [a["path"] for a in anomalies]
        self.assertFalse(any("2026-05-28_daily.md" in p for p in paths))

    def test_py_outside_scripts(self):
        self._create("JCH_Inbox/03_PROJECTS/helper.py")
        anomalies = file_placement_checker.check(self.root)
        paths = [a["path"] for a in anomalies]
        self.assertTrue(any("helper.py" in p for p in paths))

    def test_py_inside_scripts_ok(self):
        self._create("scripts/helper.py")
        anomalies = file_placement_checker.check(self.root)
        paths = [a["path"] for a in anomalies]
        self.assertFalse(any("helper.py" in p for p in paths))

    def test_plist_outside_launchd(self):
        self._create("scripts/com.test.plist")
        anomalies = file_placement_checker.check(self.root)
        paths = [a["path"] for a in anomalies]
        self.assertTrue(any("com.test.plist" in p for p in paths))

    def test_plist_inside_launchd_ok(self):
        self._create("scripts/launchd/com.test.plist")
        anomalies = file_placement_checker.check(self.root)
        paths = [a["path"] for a in anomalies]
        self.assertFalse(any("com.test.plist" in p for p in paths))

    def test_file_at_inbox_root(self):
        self._create("JCH_Inbox/orphan.md")
        anomalies = file_placement_checker.check(self.root)
        paths = [a["path"] for a in anomalies]
        self.assertTrue(any("orphan.md" in p for p in paths))

    def test_excluded_dirs_not_scanned(self):
        self._create("scripts/__pycache__/helper.py")
        anomalies = file_placement_checker.check(self.root)
        paths = [a["path"] for a in anomalies]
        self.assertFalse(any("helper.py" in p for p in paths))

    def test_anomaly_dict_structure(self):
        self._create("JCH_Inbox/orphan.md")
        anomalies = file_placement_checker.check(self.root)
        self.assertTrue(len(anomalies) > 0)
        a = anomalies[0]
        self.assertIn("path", a)
        self.assertIn("description", a)
        self.assertIn("expected", a)
