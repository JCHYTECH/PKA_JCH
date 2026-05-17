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

    def test_build_card_list_filters_by_project_status_owner_and_awaiting_jch(self):
        cards = [
            {
                "title": "Prepare ARTEON palette",
                "project": "02_ARTEON",
                "type": "task",
                "owner": "Dobby",
                "priority": "normale",
                "status": "En validation",
                "description": "Needs JCH sign-off",
                "labels": ["branding", "en-attente-jch"],
            },
            {
                "title": "Ship WildNexus field notes",
                "project": "03_WILDNEXUS",
                "type": "document",
                "owner": "Forge",
                "priority": "normale",
                "status": "En cours",
                "description": "Ongoing implementation",
                "labels": ["tech"],
            },
            {
                "title": "Review legal clause",
                "project": "08_VETALYX",
                "type": "decision",
                "owner": "Renard",
                "priority": "haute",
                "status": "En attente",
                "description": "Blocked by external answer",
                "labels": ["legal", "bloque-externe"],
            },
        ]

        filtered = pka_kanban_service.build_card_list(
            cards,
            project="02_ARTEON",
            status="En validation",
            owner="Dobby",
            awaiting_jch_only=True,
        )

        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["title"], "Prepare ARTEON palette")
        self.assertTrue(filtered[0]["awaiting_jch"])

    def test_build_card_list_sorts_by_status_then_title(self):
        cards = [
            {
                "title": "Zulu",
                "project": "02_ARTEON",
                "type": "task",
                "owner": "Dobby",
                "priority": "normale",
                "status": "En cours",
                "description": "Later alpha",
            },
            {
                "title": "Alpha",
                "project": "02_ARTEON",
                "type": "task",
                "owner": "Dobby",
                "priority": "normale",
                "status": "En cours",
                "description": "First alpha",
            },
        ]

        ordered = pka_kanban_service.build_card_list(cards)

        self.assertEqual([card["title"] for card in ordered], ["Alpha", "Zulu"])

    def test_available_card_filters_returns_projects_statuses_and_owners(self):
        cards = [
            {
                "title": "Prepare ARTEON palette",
                "project": "02_ARTEON",
                "type": "task",
                "owner": "Dobby",
                "priority": "normale",
                "status": "En validation",
                "description": "Needs JCH sign-off",
            },
            {
                "title": "Ship WildNexus field notes",
                "project": "03_WILDNEXUS",
                "type": "document",
                "owner": "Forge",
                "priority": "normale",
                "status": "En cours",
                "description": "Ongoing implementation",
            },
        ]

        filters = pka_kanban_service.available_card_filters(cards)

        self.assertEqual(filters["projects"], ["02_ARTEON", "03_WILDNEXUS"])
        self.assertIn("En validation", filters["statuses"])
        self.assertEqual(filters["owners"], ["Dobby", "Forge"])

    def test_build_card_list_ignores_invalid_cards_instead_of_failing_whole_list(self):
        cards = [
            {
                "title": "Valid card",
                "project": "03_WILDNEXUS",
                "type": "task",
                "owner": "Forge",
                "priority": "normale",
                "status": "En cours",
                "description": "Healthy card",
            },
            {
                "title": "Broken card",
                "project": "03_WILDNEXUS",
                "type": "task",
                "owner": "Forge",
                "priority": "normale",
                "status": "Doing",
                "description": "Invalid status",
            },
        ]

        filtered = pka_kanban_service.build_card_list(cards)

        self.assertEqual([card["title"] for card in filtered], ["Valid card"])

    def test_string_label_is_treated_as_single_label_for_awaiting_jch(self):
        cards = [
            {
                "title": "Decision review",
                "project": "02_ARTEON",
                "type": "task",
                "owner": "Dobby",
                "priority": "normale",
                "status": "En validation",
                "description": "Decision pending",
                "labels": "en-attente-jch",
            }
        ]

        filtered = pka_kanban_service.build_card_list(cards, awaiting_jch_only=True)

        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["labels"], ["en-attente-jch"])
        self.assertTrue(filtered[0]["awaiting_jch"])


if __name__ == "__main__":
    unittest.main()
