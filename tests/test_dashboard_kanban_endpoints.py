import unittest
import os
from unittest import mock

from scripts import dashboard_server


class DashboardKanbanEndpointsTest(unittest.TestCase):
    def test_dashboard_health_includes_kanban_stub(self):
        with mock.patch.object(
            dashboard_server,
            "kanban_snapshot",
            return_value={"totals": {"En cours": 2}, "blocked": 1, "awaiting_jch": 1},
        ):
            health = dashboard_server.dashboard_health()

        self.assertEqual(health["kanban"]["blocked"], 1)
        self.assertEqual(health["kanban"]["awaitingJch"], 1)

    def test_kanban_snapshot_aggregates_live_plane_cards(self):
        config = {
            "projects": {
                "01_AI_IT_TOOLS": {"plane_project_id": "ai-tools"},
                "02_ARTEON": {"plane_project_id": "arteon"},
            }
        }
        cards_by_project = {
            "01_AI_IT_TOOLS": [
                {
                    "title": "Spec",
                    "project": "01_AI_IT_TOOLS",
                    "type": "task",
                    "owner": "Forge",
                    "priority": "normale",
                    "status": "En cours",
                    "description": "Build it",
                    "labels": ["ops"],
                }
            ],
            "02_ARTEON": [
                {
                    "title": "Review",
                    "project": "02_ARTEON",
                    "type": "task",
                    "owner": "Dobby",
                    "priority": "normale",
                    "status": "En validation",
                    "description": "Check it",
                    "labels": ["en-attente-jch"],
                }
            ],
        }

        with mock.patch.object(dashboard_server.pka_plane_adapter, "load_config", return_value=config):
            with mock.patch.object(
                dashboard_server.pka_plane_adapter,
                "fetch_project_issues",
                side_effect=lambda project_key: cards_by_project[project_key],
            ):
                summary = dashboard_server.kanban_snapshot()

        self.assertEqual(summary["totals"]["En cours"], 1)
        self.assertEqual(summary["totals"]["En validation"], 1)
        self.assertEqual(summary["awaiting_jch"], 1)
        self.assertEqual(summary["by_project"]["01_AI_IT_TOOLS"]["total"], 1)

    def test_kanban_snapshot_loads_plane_token_from_local_secret_file_fallback(self):
        config = {"projects": {"01_AI_IT_TOOLS": {"plane_project_id": "ai-tools"}}}
        cards = [
            {
                "title": "Spec",
                "project": "01_AI_IT_TOOLS",
                "type": "task",
                "owner": "Forge",
                "priority": "normale",
                "status": "En cours",
                "description": "Build it",
                "labels": ["ops"],
            }
        ]

        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("PKA_PLANE_API_TOKEN", None)
            with mock.patch.object(dashboard_server, "read_secret_value", return_value="plane-secret"):
                with mock.patch.object(dashboard_server.pka_plane_adapter, "load_config", return_value=config):
                    with mock.patch.object(
                        dashboard_server.pka_plane_adapter,
                        "fetch_project_issues",
                        return_value=cards,
                    ):
                        summary = dashboard_server.kanban_snapshot()
                        self.assertEqual(os.environ.get("PKA_PLANE_API_TOKEN"), "plane-secret")

        self.assertEqual(summary["totals"]["En cours"], 1)


if __name__ == "__main__":
    unittest.main()
