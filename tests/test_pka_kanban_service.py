import unittest

from scripts import pka_kanban_service


class PkaKanbanServiceTest(unittest.TestCase):
    def test_build_summary_counts_statuses_and_validation_queue(self):
        cards = [
            {
                "title": "Card 1",
                "project": "02_ARTEON",
                "type": "task",
                "owner": "Vega",
                "priority": "haute",
                "status": "En cours",
                "description": "First card",
                "labels": ["branding"],
                "lead_specialist": "Vega",
            },
            {
                "title": "Card 2",
                "project": "02_ARTEON",
                "type": "task",
                "owner": "Dobby",
                "priority": "haute",
                "status": "En validation",
                "description": "Second card",
                "labels": ["en-attente-jch"],
                "lead_specialist": "Dobby",
            },
            {
                "title": "Card 3",
                "project": "08_VETALYX",
                "type": "task",
                "owner": "Renard",
                "priority": "haute",
                "status": "En attente",
                "description": "Third card",
                "labels": ["bloque-externe"],
                "lead_specialist": "Renard",
            },
        ]

        summary = pka_kanban_service.build_summary(cards)

        self.assertEqual(summary["totals"]["En cours"], 1)
        self.assertEqual(summary["totals"]["En validation"], 1)
        self.assertEqual(summary["blocked"], 1)
        self.assertEqual(summary["awaiting_jch"], 1)
        self.assertEqual(summary["by_project"]["02_ARTEON"]["total"], 2)

    def test_validate_card_rejects_unknown_status(self):
        with self.assertRaises(ValueError):
            pka_kanban_service.validate_card(
                {
                    "title": "Bad card",
                    "project": "02_ARTEON",
                    "type": "task",
                    "owner": "Dobby",
                    "priority": "haute",
                    "status": "Doing",
                    "description": "wrong status",
                }
            )


if __name__ == "__main__":
    unittest.main()
