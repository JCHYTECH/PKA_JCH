import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import pka_plane_adapter


class PkaPlaneAdapterTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        (self.root / "JCH_Inbox" / "99_SYSTEM").mkdir(parents=True)
        (self.root / "JCH_Inbox" / "03_PROJECTS").mkdir(parents=True)
        for key in ("01_AI_IT_TOOLS", "02_ARTEON", "03_FAUNE_AUTOUR", "08_VETALYX"):
            (self.root / "JCH_Inbox" / "03_PROJECTS" / key).mkdir()
        self.write_config(
            {
                "01_AI_IT_TOOLS": {"plane_project_id": "ai-tools"},
                "02_ARTEON": {"plane_project_id": "arteon"},
                "08_VETALYX": {"plane_project_id": "vetalyx"},
            }
        )

    def tearDown(self):
        self.tmpdir.cleanup()

    def write_config(self, projects: dict) -> None:
        (self.root / "JCH_Inbox" / "99_SYSTEM" / "pka_plane_config.json").write_text(
            json.dumps(
                {
                    "workspace_slug": "pka-jch",
                    "api_base": "http://127.0.0.1:8088/api/v1",
                    "api_token_env": "PKA_PLANE_API_TOKEN",
                    "projects": projects,
                }
            ),
            encoding="utf-8",
        )

    def test_load_config_returns_known_project_mapping(self):
        with mock.patch.object(pka_plane_adapter, "ROOT", self.root):
            config = pka_plane_adapter.load_config()

        self.assertEqual(config["projects"]["02_ARTEON"]["plane_project_id"], "arteon")

    def test_plane_token_uses_configured_env_var(self):
        with mock.patch.object(pka_plane_adapter, "ROOT", self.root):
            with mock.patch.dict(
                "os.environ",
                {"PKA_PLANE_API_TOKEN": "plane-secret"},
                clear=True,
            ):
                self.assertEqual(pka_plane_adapter.plane_token(), "plane-secret")

    def test_validate_project_registry_detects_missing_mapping(self):
        with mock.patch.object(pka_plane_adapter, "ROOT", self.root):
            self.assertEqual(
                pka_plane_adapter.validate_project_registry(),
                ["03_PROJECTS project directory missing from Plane config: 03_FAUNE_AUTOUR"],
            )

    def test_validate_project_registry_reports_blank_and_malformed_mappings(self):
        self.write_config(
            {
                "01_AI_IT_TOOLS": {"plane_project_id": ""},
                "02_ARTEON": {"plane_project_id": "arteon"},
                "03_FAUNE_AUTOUR": "not-a-mapping",
                "08_VETALYX": {"plane_project_id": "vetalyx"},
            }
        )

        with mock.patch.object(pka_plane_adapter, "ROOT", self.root):
            findings = pka_plane_adapter.validate_project_registry()

        self.assertIn("03_PROJECTS project directory has unusable Plane mapping: 01_AI_IT_TOOLS", findings)
        self.assertIn("03_PROJECTS project directory has unusable Plane mapping: 03_FAUNE_AUTOUR", findings)

    def test_real_repo_config_has_non_empty_plane_ids_for_active_projects(self):
        config = pka_plane_adapter.load_config()
        projects_dir = pka_plane_adapter.ROOT / "JCH_Inbox" / "03_PROJECTS"

        self.assertIsInstance(config["workspace_slug"], str)
        self.assertNotEqual(config["workspace_slug"].strip(), "")
        self.assertNotEqual(config["api_base"].strip(), "https://plane.example/api/v1")
        self.assertEqual(config["api_base"].strip(), "http://127.0.0.1:8088/api/v1")

        for item in sorted(projects_dir.iterdir()):
            if not item.is_dir():
                continue
            self.assertIn(item.name, config["projects"])
            plane_project_id = config["projects"][item.name]["plane_project_id"]
            self.assertIsInstance(plane_project_id, str)
            self.assertNotEqual(plane_project_id.strip(), "", item.name)

    def test_load_config_rejects_placeholder_or_empty_connection_values(self):
        self.write_config(
            {
                "01_AI_IT_TOOLS": {"plane_project_id": "ai-tools"},
            }
        )
        (self.root / "JCH_Inbox" / "99_SYSTEM" / "pka_plane_config.json").write_text(
            json.dumps(
                {
                    "workspace_slug": "",
                    "api_base": "https://plane.example/api/v1",
                    "api_token_env": "PKA_PLANE_API_TOKEN",
                    "projects": {"01_AI_IT_TOOLS": {"plane_project_id": "ai-tools"}},
                }
            ),
            encoding="utf-8",
        )

        with mock.patch.object(pka_plane_adapter, "ROOT", self.root):
            with self.assertRaisesRegex(ValueError, "workspace_slug"):
                pka_plane_adapter.load_config()

    def test_normalize_issue_maps_plane_fields_to_pka_card(self):
        issue = {
            "name": "Ship Plane sync",
            "state": {"name": "En cours"},
            "assignee": {"display_name": "Vega"},
            "label_details": [{"name": "ops"}, {"name": "urgent"}],
            "description_html": "<p>Rich description</p>",
            "description_stripped": "Plain description",
        }

        card = pka_plane_adapter.normalize_issue("02_ARTEON", issue)

        self.assertEqual(
            card,
            {
                "title": "Ship Plane sync",
                "project": "02_ARTEON",
                "status": "En cours",
                "owner": "Vega",
                "labels": ["ops", "urgent"],
                "type": "task",
                "priority": "normale",
                "description": "<p>Rich description</p>",
            },
        )


if __name__ == "__main__":
    unittest.main()
