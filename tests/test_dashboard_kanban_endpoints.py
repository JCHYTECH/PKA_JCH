import unittest
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


if __name__ == "__main__":
    unittest.main()
