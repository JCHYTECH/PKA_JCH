import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import pka_context_profile


class PkaContextProfileTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        config = {
            "profiles": [
                {
                    "project_key": "02_ARTEON",
                    "label": "ARTEON",
                    "trigger_terms": ["arteon", "wildlens", "brand"],
                    "specialist_hint": "Vega",
                    "roots": ["JCH_Inbox/03_PROJECTS/02_ARTEON"],
                    "paired_skills": ["pka-system-improvement"]
                },
                {
                    "project_key": "PKA",
                    "label": "PKA Core",
                    "trigger_terms": ["pka", "dobby", "system"],
                    "specialist_hint": "Forge",
                    "roots": ["scripts", "TEAM", "JCH_Inbox/99_SYSTEM"],
                    "paired_skills": ["pka-system-improvement"]
                }
            ]
        }
        self.config_path = self.root / "context_profiles.json"
        self.config_path.write_text(json.dumps(config), encoding="utf-8")

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_infer_project_key_from_query(self):
        with mock.patch.object(pka_context_profile, "CONFIG_PATH", self.config_path):
            project_key = pka_context_profile.infer_project_key("arteon brand refresh")
        self.assertEqual(project_key, "02_ARTEON")

    def test_select_profile_by_explicit_project_key(self):
        with mock.patch.object(pka_context_profile, "CONFIG_PATH", self.config_path):
            profile = pka_context_profile.select_profile(project_key="PKA")
        self.assertEqual(profile["label"], "PKA Core")


if __name__ == "__main__":
    unittest.main()
