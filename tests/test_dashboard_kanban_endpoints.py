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
        dashboard_server.clear_kanban_cache()
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

    def test_all_kanban_cards_reuses_short_lived_cache(self):
        dashboard_server.clear_kanban_cache()
        config = {"projects": {"03_WILDNEXUS": {"plane_project_id": "wildnexus"}}}
        cards = [
            {
                "title": "Cached task",
                "project": "03_WILDNEXUS",
                "type": "task",
                "owner": "Forge",
                "priority": "normale",
                "status": "A qualifier",
                "description": "",
                "labels": [],
            }
        ]

        with mock.patch.object(dashboard_server.pka_plane_adapter, "load_config", return_value=config):
            with mock.patch.object(
                dashboard_server.pka_plane_adapter,
                "fetch_project_issues",
                return_value=cards,
            ) as fetch_mock:
                first = dashboard_server._all_kanban_cards()
                second = dashboard_server._all_kanban_cards()

        self.assertEqual(first, cards)
        self.assertEqual(second, cards)
        fetch_mock.assert_called_once_with("03_WILDNEXUS")
        dashboard_server.clear_kanban_cache()

    def test_kanban_cards_endpoint_returns_filtered_card_list(self):
        handler = object.__new__(dashboard_server.DashboardHandler)
        handler.path = "/api/kanban/cards?project=03_WILDNEXUS&status=En%20cours&owner=Forge&awaiting_jch=0"
        handler.command = "GET"
        handler.request_version = "HTTP/1.1"
        handler.headers = {}
        handler.wfile = mock.Mock()
        handler.send_response = mock.Mock()
        handler.send_header = mock.Mock()
        handler.end_headers = mock.Mock()
        handler.is_authorized_request = mock.Mock(return_value=True)
        handler.is_local_request = mock.Mock(return_value=True)
        payloads = []
        handler.send_json = lambda payload, status=200: payloads.append((status, payload))

        with mock.patch.object(
            dashboard_server,
            "kanban_cards_payload",
            return_value={"ok": True, "cards": [{"title": "Ship WildNexus field notes"}]},
        ) as payload_mock:
            dashboard_server.DashboardHandler.do_GET(handler)

        payload_mock.assert_called_once_with("03_WILDNEXUS", "En cours", "Forge", False)
        self.assertEqual(payloads[0][0], 200)
        self.assertEqual(payloads[0][1]["cards"][0]["title"], "Ship WildNexus field notes")

    def test_kanban_cards_endpoint_strips_filters_and_accepts_truthy_awaiting_flag(self):
        handler = object.__new__(dashboard_server.DashboardHandler)
        handler.path = "/api/kanban/cards?project=%2003_WILDNEXUS%20&status=%20En%20cours%20&owner=%20Forge%20&awaiting_jch=true"
        handler.command = "GET"
        handler.request_version = "HTTP/1.1"
        handler.headers = {}
        handler.wfile = mock.Mock()
        handler.send_response = mock.Mock()
        handler.send_header = mock.Mock()
        handler.end_headers = mock.Mock()
        handler.is_authorized_request = mock.Mock(return_value=True)
        handler.is_local_request = mock.Mock(return_value=True)
        payloads = []
        handler.send_json = lambda payload, status=200: payloads.append((status, payload))

        with mock.patch.object(
            dashboard_server,
            "kanban_cards_payload",
            return_value={"ok": True, "cards": []},
        ) as payload_mock:
            dashboard_server.DashboardHandler.do_GET(handler)

        payload_mock.assert_called_once_with("03_WILDNEXUS", "En cours", "Forge", True)
        self.assertEqual(payloads[0][0], 200)

    def test_kanban_cards_endpoint_returns_503_when_payload_is_unavailable(self):
        handler = object.__new__(dashboard_server.DashboardHandler)
        handler.path = "/api/kanban/cards?awaiting_jch=1"
        handler.command = "GET"
        handler.request_version = "HTTP/1.1"
        handler.headers = {}
        handler.wfile = mock.Mock()
        handler.send_response = mock.Mock()
        handler.send_header = mock.Mock()
        handler.end_headers = mock.Mock()
        handler.is_authorized_request = mock.Mock(return_value=True)
        handler.is_local_request = mock.Mock(return_value=True)
        payloads = []
        handler.send_json = lambda payload, status=200: payloads.append((status, payload))

        with mock.patch.object(
            dashboard_server,
            "kanban_cards_payload",
            return_value={"ok": False, "error": "Plane indisponible", "cards": []},
        ):
            dashboard_server.DashboardHandler.do_GET(handler)

        self.assertEqual(payloads[0][0], 503)
        self.assertFalse(payloads[0][1]["ok"])

    def test_kanban_filters_endpoint_returns_available_filters(self):
        handler = object.__new__(dashboard_server.DashboardHandler)
        handler.path = "/api/kanban/filters"
        handler.command = "GET"
        handler.request_version = "HTTP/1.1"
        handler.headers = {}
        handler.wfile = mock.Mock()
        handler.send_response = mock.Mock()
        handler.send_header = mock.Mock()
        handler.end_headers = mock.Mock()
        handler.is_authorized_request = mock.Mock(return_value=True)
        handler.is_local_request = mock.Mock(return_value=True)
        payloads = []
        handler.send_json = lambda payload, status=200: payloads.append((status, payload))

        with mock.patch.object(
            dashboard_server,
            "kanban_filters_payload",
            return_value={"ok": True, "projects": ["02_ARTEON"], "statuses": ["En validation"], "owners": ["Dobby"]},
        ):
            dashboard_server.DashboardHandler.do_GET(handler)

        self.assertEqual(payloads[0][0], 200)
        self.assertTrue(payloads[0][1]["ok"])
        self.assertEqual(payloads[0][1]["owners"], ["Dobby"])

    def test_kanban_cards_payload_returns_cards_from_service(self):
        with mock.patch.object(dashboard_server, "_all_kanban_cards", return_value=[{"title": "Raw card"}]):
            with mock.patch.object(
                dashboard_server.pka_kanban_service,
                "build_card_list",
                return_value=[{"title": "Rendered card"}],
            ) as build_mock:
                payload = dashboard_server.kanban_cards_payload("03_WILDNEXUS", "En cours", "Forge", True)

        build_mock.assert_called_once_with(
            [{"title": "Raw card"}],
            project="03_WILDNEXUS",
            status="En cours",
            owner="Forge",
            awaiting_jch_only=True,
        )
        self.assertEqual(payload, {"ok": True, "cards": [{"title": "Rendered card"}]})

    def test_kanban_cards_payload_returns_error_payload_when_fetch_fails(self):
        with mock.patch.object(dashboard_server, "_all_kanban_cards", side_effect=RuntimeError("Plane indisponible")):
            payload = dashboard_server.kanban_cards_payload(None, None, None, False)

        self.assertFalse(payload["ok"])
        self.assertEqual(payload["cards"], [])
        self.assertIn("Plane indisponible", payload["error"])

    def test_kanban_filters_endpoint_returns_503_when_payload_is_unavailable(self):
        handler = object.__new__(dashboard_server.DashboardHandler)
        handler.path = "/api/kanban/filters"
        handler.command = "GET"
        handler.request_version = "HTTP/1.1"
        handler.headers = {}
        handler.wfile = mock.Mock()
        handler.send_response = mock.Mock()
        handler.send_header = mock.Mock()
        handler.end_headers = mock.Mock()
        handler.is_authorized_request = mock.Mock(return_value=True)
        handler.is_local_request = mock.Mock(return_value=True)
        payloads = []
        handler.send_json = lambda payload, status=200: payloads.append((status, payload))

        with mock.patch.object(
            dashboard_server,
            "kanban_filters_payload",
            return_value={"ok": False, "error": "Plane indisponible", "projects": [], "statuses": [], "owners": []},
        ):
            dashboard_server.DashboardHandler.do_GET(handler)

        self.assertEqual(payloads[0][0], 503)
        self.assertFalse(payloads[0][1]["ok"])

    def test_kanban_filters_payload_returns_service_filters(self):
        with mock.patch.object(dashboard_server, "_all_kanban_cards", return_value=[{"title": "Raw card"}]):
            with mock.patch.object(
                dashboard_server.pka_kanban_service,
                "available_card_filters",
                return_value={"projects": ["02_ARTEON"], "statuses": ["En validation"], "owners": ["Dobby"]},
            ) as filters_mock:
                payload = dashboard_server.kanban_filters_payload()

        filters_mock.assert_called_once_with([{"title": "Raw card"}])
        self.assertEqual(
            payload,
            {"ok": True, "projects": ["02_ARTEON"], "statuses": ["En validation"], "owners": ["Dobby"]},
        )

    def test_kanban_filters_payload_returns_error_payload_when_fetch_fails(self):
        with mock.patch.object(dashboard_server, "_all_kanban_cards", side_effect=RuntimeError("Plane indisponible")):
            payload = dashboard_server.kanban_filters_payload()

        self.assertFalse(payload["ok"])
        self.assertEqual(payload["projects"], [])
        self.assertEqual(payload["statuses"], [])
        self.assertEqual(payload["owners"], [])
        self.assertIn("Plane indisponible", payload["error"])

    def test_file_index_search_endpoint_uses_backend_search(self):
        handler = object.__new__(dashboard_server.DashboardHandler)
        handler.path = "/api/file-index/search?q=wild&project_key=03_WILDNEXUS&component=03.01%20BIOACOUSTIC&limit=7"
        handler.command = "GET"
        handler.request_version = "HTTP/1.1"
        handler.headers = {}
        handler.wfile = mock.Mock()
        handler.send_response = mock.Mock()
        handler.send_header = mock.Mock()
        handler.end_headers = mock.Mock()
        handler.is_authorized_request = mock.Mock(return_value=True)
        handler.is_local_request = mock.Mock(return_value=True)
        payloads = []
        handler.send_json = lambda payload, status=200: payloads.append((status, payload))

        with mock.patch.object(
            dashboard_server.rebuild_file_index,
            "search_index",
            return_value=[
                {
                    "filename": "WildNexus_MASTER_ARCHITECTURE.md",
                    "file_path": "JCH_Inbox/03_PROJECTS/03_WILDNEXUS/WildNexus_MASTER_ARCHITECTURE.md",
                }
            ],
        ) as search_mock:
            dashboard_server.DashboardHandler.do_GET(handler)

        search_mock.assert_called_once_with(
            dashboard_server.TEAM_DB,
            "wild",
            project_key="03_WILDNEXUS",
            component="03.01 BIOACOUSTIC",
            limit=7,
        )
        self.assertEqual(payloads[0][0], 200)
        self.assertTrue(payloads[0][1]["ok"])
        self.assertEqual(payloads[0][1]["results"][0]["filename"], "WildNexus_MASTER_ARCHITECTURE.md")

    def test_file_index_search_endpoint_short_query_returns_empty_results(self):
        handler = object.__new__(dashboard_server.DashboardHandler)
        handler.path = "/api/file-index/search?q=w"
        handler.command = "GET"
        handler.request_version = "HTTP/1.1"
        handler.headers = {}
        handler.wfile = mock.Mock()
        handler.send_response = mock.Mock()
        handler.send_header = mock.Mock()
        handler.end_headers = mock.Mock()
        handler.is_authorized_request = mock.Mock(return_value=True)
        handler.is_local_request = mock.Mock(return_value=True)
        payloads = []
        handler.send_json = lambda payload, status=200: payloads.append((status, payload))

        with mock.patch.object(dashboard_server.rebuild_file_index, "search_index") as search_mock:
            dashboard_server.DashboardHandler.do_GET(handler)

        search_mock.assert_not_called()
        self.assertEqual(payloads[0][0], 200)
        self.assertEqual(payloads[0][1], {"ok": True, "results": []})

    def test_file_index_filters_endpoint_returns_projects_and_components(self):
        handler = object.__new__(dashboard_server.DashboardHandler)
        handler.path = "/api/file-index/filters"
        handler.command = "GET"
        handler.request_version = "HTTP/1.1"
        handler.headers = {}
        handler.wfile = mock.Mock()
        handler.send_response = mock.Mock()
        handler.send_header = mock.Mock()
        handler.end_headers = mock.Mock()
        handler.is_authorized_request = mock.Mock(return_value=True)
        handler.is_local_request = mock.Mock(return_value=True)
        payloads = []
        handler.send_json = lambda payload, status=200: payloads.append((status, payload))

        with mock.patch.object(
            dashboard_server.rebuild_file_index,
            "available_filters",
            return_value={
                "projects": ["03_WILDNEXUS", "06_PHOTO_NATURE"],
                "components": {
                    "03_WILDNEXUS": ["03.01 BIOACOUSTIC", "03.02 FAUNE_AUTOUR_APP"],
                    "06_PHOTO_NATURE": [],
                },
            },
        ):
            dashboard_server.DashboardHandler.do_GET(handler)

        self.assertEqual(payloads[0][0], 200)
        self.assertTrue(payloads[0][1]["ok"])
        self.assertIn("03_WILDNEXUS", payloads[0][1]["projects"])
        self.assertIn("03.01 BIOACOUSTIC", payloads[0][1]["components"]["03_WILDNEXUS"])


if __name__ == "__main__":
    unittest.main()
