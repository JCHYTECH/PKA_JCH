import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from scripts import pka_kanban_schema


class PkaKanbanSchemaTest(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tmpdir.name)
        (self.root / "JCH_Inbox" / "99_SYSTEM").mkdir(parents=True)
        (self.root / "JCH_Inbox" / "99_SYSTEM" / "pka_kanban_schema.json").write_text(
            json.dumps(
                {
                    "statuses": [
                        "A qualifier",
                        "Pret",
                        "En cours",
                        "En attente",
                        "En validation",
                        "Termine",
                        "Archive",
                    ],
                    "types": [
                        "task",
                        "decision",
                        "document",
                        "bug",
                        "idea",
                        "follow-up",
                        "deliverable",
                    ],
                    "required_fields": [
                        "title",
                        "project",
                        "type",
                        "owner",
                        "priority",
                        "status",
                        "description",
                    ],
                    "recommended_fields": [
                        "lead_specialist",
                        "model_used",
                        "decision_owner",
                        "blocking_reason",
                        "expected_outcome",
                        "source_link",
                    ],
                }
            ),
            encoding="utf-8",
        )
        (self.root / "JCH_Inbox" / "99_SYSTEM" / "pka_kanban_governance.json").write_text(
            json.dumps(
                {
                    "labels": {
                        "nature": [
                            "decision",
                            "execution",
                            "research",
                            "document",
                            "follow-up",
                            "bug",
                            "idea",
                        ],
                        "domain": [
                            "legal",
                            "finance",
                            "tech",
                            "photo",
                            "branding",
                            "ops",
                            "travel",
                            "science",
                        ],
                        "context": [
                            "urgent",
                            "bloque-externe",
                            "en-attente-jch",
                            "delegue",
                            "a-planifier",
                            "quick-win",
                        ],
                        "level": [
                            "strategique",
                            "tactique",
                            "operationnel",
                        ],
                    },
                    "rules": {
                        "lowercase_only": True,
                        "separator": "-",
                        "state_labels_forbidden": True,
                        "creation_roles": ["Dobby", "Forge"],
                    },
                }
            ),
            encoding="utf-8",
        )

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_load_schema_returns_expected_statuses(self):
        with mock.patch.object(pka_kanban_schema, "ROOT", self.root):
            schema = pka_kanban_schema.load_schema()

        self.assertEqual(
            schema["statuses"],
            [
                "A qualifier",
                "Pret",
                "En cours",
                "En attente",
                "En validation",
                "Termine",
                "Archive",
            ],
        )

    def test_real_repo_files_remain_canonical(self):
        schema = pka_kanban_schema.load_schema()
        governance = pka_kanban_schema.load_governance()

        self.assertEqual(
            schema["statuses"],
            [
                "A qualifier",
                "Pret",
                "En cours",
                "En attente",
                "En validation",
                "Termine",
                "Archive",
            ],
        )
        self.assertEqual(
            schema["required_fields"],
            [
                "title",
                "project",
                "type",
                "owner",
                "priority",
                "status",
                "description",
            ],
        )
        self.assertEqual(
            schema["recommended_fields"],
            [
                "lead_specialist",
                "model_used",
                "decision_owner",
                "blocking_reason",
                "expected_outcome",
                "source_link",
            ],
        )
        self.assertEqual(
            governance["labels"]["nature"],
            ["decision", "execution", "research", "document", "follow-up", "bug", "idea"],
        )
        self.assertEqual(
            governance["labels"]["domain"],
            ["legal", "finance", "tech", "photo", "branding", "ops", "travel", "science"],
        )
        self.assertEqual(
            governance["labels"]["context"],
            ["urgent", "bloque-externe", "en-attente-jch", "delegue", "a-planifier", "quick-win"],
        )
        self.assertEqual(
            governance["labels"]["level"],
            ["strategique", "tactique", "operationnel"],
        )
        self.assertTrue(governance["rules"]["lowercase_only"])
        self.assertEqual(governance["rules"]["separator"], "-")
        self.assertTrue(governance["rules"]["state_labels_forbidden"])
        self.assertEqual(governance["rules"]["creation_roles"], ["Dobby", "Forge"])

    def test_duplicate_labels_are_rejected(self):
        bad_file = self.root / "JCH_Inbox" / "99_SYSTEM" / "pka_kanban_governance.json"
        bad_file.write_text(
            json.dumps(
                {
                    "labels": {
                        "nature": ["decision", "decision"],
                        "domain": [],
                        "context": [],
                        "level": [],
                    },
                    "rules": {
                        "lowercase_only": True,
                        "separator": "-",
                        "state_labels_forbidden": True,
                        "creation_roles": ["Dobby", "Forge"],
                    },
                }
            ),
            encoding="utf-8",
        )

        with mock.patch.object(pka_kanban_schema, "ROOT", self.root):
            with self.assertRaisesRegex(ValueError, "duplicate labels are forbidden"):
                pka_kanban_schema.load_governance()

    def test_lowercase_governance_labels_are_enforced(self):
        bad_file = self.root / "JCH_Inbox" / "99_SYSTEM" / "pka_kanban_governance.json"
        bad_file.write_text(
            json.dumps(
                {
                    "labels": {
                        "nature": ["Decision"],
                        "domain": [],
                        "context": [],
                        "level": [],
                    },
                    "rules": {
                        "lowercase_only": True,
                        "separator": "-",
                        "state_labels_forbidden": True,
                        "creation_roles": ["Dobby", "Forge"],
                    },
                }
            ),
            encoding="utf-8",
        )

        with mock.patch.object(pka_kanban_schema, "ROOT", self.root):
            with self.assertRaisesRegex(ValueError, "must be lowercase"):
                pka_kanban_schema.load_governance()

    def test_separator_governance_labels_are_enforced(self):
        bad_file = self.root / "JCH_Inbox" / "99_SYSTEM" / "pka_kanban_governance.json"
        bad_file.write_text(
            json.dumps(
                {
                    "labels": {
                        "nature": ["decision"],
                        "domain": [],
                        "context": ["en_attente_jch"],
                        "level": [],
                    },
                    "rules": {
                        "lowercase_only": True,
                        "separator": "-",
                        "state_labels_forbidden": True,
                        "creation_roles": ["Dobby", "Forge"],
                    },
                }
            ),
            encoding="utf-8",
        )

        with mock.patch.object(pka_kanban_schema, "ROOT", self.root):
            with self.assertRaisesRegex(ValueError, "must use '-' as separator"):
                pka_kanban_schema.load_governance()

    def test_space_governance_labels_are_enforced_under_dash_separator(self):
        bad_file = self.root / "JCH_Inbox" / "99_SYSTEM" / "pka_kanban_governance.json"
        bad_file.write_text(
            json.dumps(
                {
                    "labels": {
                        "nature": ["quick win"],
                        "domain": [],
                        "context": [],
                        "level": [],
                    },
                    "rules": {
                        "lowercase_only": True,
                        "separator": "-",
                        "state_labels_forbidden": True,
                        "creation_roles": ["Dobby", "Forge"],
                    },
                }
            ),
            encoding="utf-8",
        )

        with mock.patch.object(pka_kanban_schema, "ROOT", self.root):
            with self.assertRaisesRegex(ValueError, "must use '-' as separator"):
                pka_kanban_schema.load_governance()

    def test_dot_governance_labels_are_enforced_under_dash_separator(self):
        bad_file = self.root / "JCH_Inbox" / "99_SYSTEM" / "pka_kanban_governance.json"
        bad_file.write_text(
            json.dumps(
                {
                    "labels": {
                        "nature": ["quick.win"],
                        "domain": [],
                        "context": [],
                        "level": [],
                    },
                    "rules": {
                        "lowercase_only": True,
                        "separator": "-",
                        "state_labels_forbidden": True,
                        "creation_roles": ["Dobby", "Forge"],
                    },
                }
            ),
            encoding="utf-8",
        )

        with mock.patch.object(pka_kanban_schema, "ROOT", self.root):
            with self.assertRaisesRegex(ValueError, "must use '-' as separator"):
                pka_kanban_schema.load_governance()

    def test_state_labels_are_rejected_when_forbidden(self):
        bad_file = self.root / "JCH_Inbox" / "99_SYSTEM" / "pka_kanban_governance.json"
        bad_file.write_text(
            json.dumps(
                {
                    "labels": {
                        "nature": ["en-cours"],
                        "domain": [],
                        "context": [],
                        "level": [],
                    },
                    "rules": {
                        "lowercase_only": True,
                        "separator": "-",
                        "state_labels_forbidden": True,
                        "creation_roles": ["Dobby", "Forge"],
                    },
                }
            ),
            encoding="utf-8",
        )

        with mock.patch.object(pka_kanban_schema, "ROOT", self.root):
            with self.assertRaisesRegex(ValueError, "state-like labels are forbidden"):
                pka_kanban_schema.load_governance()

    def test_underscore_state_labels_are_rejected_when_forbidden(self):
        bad_file = self.root / "JCH_Inbox" / "99_SYSTEM" / "pka_kanban_governance.json"
        bad_file.write_text(
            json.dumps(
                {
                    "labels": {
                        "nature": ["en_attente"],
                        "domain": [],
                        "context": [],
                        "level": [],
                    },
                    "rules": {
                        "lowercase_only": True,
                        "separator": "_",
                        "state_labels_forbidden": True,
                        "creation_roles": ["Dobby", "Forge"],
                    },
                }
            ),
            encoding="utf-8",
        )

        with mock.patch.object(pka_kanban_schema, "ROOT", self.root):
            with self.assertRaisesRegex(ValueError, "state-like labels are forbidden"):
                pka_kanban_schema.load_governance()

    def test_invalid_separator_rule_is_rejected(self):
        bad_file = self.root / "JCH_Inbox" / "99_SYSTEM" / "pka_kanban_governance.json"
        bad_file.write_text(
            json.dumps(
                {
                    "labels": {
                        "nature": ["decision"],
                        "domain": [],
                        "context": [],
                        "level": [],
                    },
                    "rules": {
                        "lowercase_only": True,
                        "separator": "/",
                        "state_labels_forbidden": True,
                        "creation_roles": ["Dobby", "Forge"],
                    },
                }
            ),
            encoding="utf-8",
        )

        with mock.patch.object(pka_kanban_schema, "ROOT", self.root):
            with self.assertRaisesRegex(ValueError, "separator must be one of"):
                pka_kanban_schema.load_governance()

    def test_label_family_content_drift_is_rejected(self):
        bad_file = self.root / "JCH_Inbox" / "99_SYSTEM" / "pka_kanban_governance.json"
        bad_file.write_text(
            json.dumps(
                {
                    "labels": {
                        "nature": ["decision", "execution", "research", "document", "follow-up", "bug", "note"],
                        "domain": ["legal", "finance", "tech", "photo", "branding", "ops", "travel", "science"],
                        "context": ["urgent", "bloque-externe", "en-attente-jch", "delegue", "a-planifier", "quick-win"],
                        "level": ["strategique", "tactique", "operationnel"],
                    },
                    "rules": {
                        "lowercase_only": True,
                        "separator": "-",
                        "state_labels_forbidden": True,
                        "creation_roles": ["Dobby", "Forge"],
                    },
                }
            ),
            encoding="utf-8",
        )

        with mock.patch.object(pka_kanban_schema, "ROOT", self.root):
            with self.assertRaisesRegex(ValueError, "labels.nature must match the canonical order"):
                pka_kanban_schema.load_governance()

    def test_creation_roles_drift_is_rejected(self):
        bad_file = self.root / "JCH_Inbox" / "99_SYSTEM" / "pka_kanban_governance.json"
        bad_file.write_text(
            json.dumps(
                {
                    "labels": {
                        "nature": ["decision", "execution", "research", "document", "follow-up", "bug", "idea"],
                        "domain": ["legal", "finance", "tech", "photo", "branding", "ops", "travel", "science"],
                        "context": ["urgent", "bloque-externe", "en-attente-jch", "delegue", "a-planifier", "quick-win"],
                        "level": ["strategique", "tactique", "operationnel"],
                    },
                    "rules": {
                        "lowercase_only": True,
                        "separator": "-",
                        "state_labels_forbidden": True,
                        "creation_roles": ["Dobby", "Forge", "Sybil"],
                    },
                }
            ),
            encoding="utf-8",
        )

        with mock.patch.object(pka_kanban_schema, "ROOT", self.root):
            with self.assertRaisesRegex(ValueError, "creation_roles must match the canonical order"):
                pka_kanban_schema.load_governance()

    def test_lowercase_only_boolean_drift_is_rejected(self):
        bad_file = self.root / "JCH_Inbox" / "99_SYSTEM" / "pka_kanban_governance.json"
        bad_file.write_text(
            json.dumps(
                {
                    "labels": {
                        "nature": ["decision", "execution", "research", "document", "follow-up", "bug", "idea"],
                        "domain": ["legal", "finance", "tech", "photo", "branding", "ops", "travel", "science"],
                        "context": ["urgent", "bloque-externe", "en-attente-jch", "delegue", "a-planifier", "quick-win"],
                        "level": ["strategique", "tactique", "operationnel"],
                    },
                    "rules": {
                        "lowercase_only": False,
                        "separator": "-",
                        "state_labels_forbidden": True,
                        "creation_roles": ["Dobby", "Forge"],
                    },
                }
            ),
            encoding="utf-8",
        )

        with mock.patch.object(pka_kanban_schema, "ROOT", self.root):
            with self.assertRaisesRegex(ValueError, "lowercase_only must match the canonical value"):
                pka_kanban_schema.load_governance()

    def test_state_labels_forbidden_boolean_drift_is_rejected(self):
        bad_file = self.root / "JCH_Inbox" / "99_SYSTEM" / "pka_kanban_governance.json"
        bad_file.write_text(
            json.dumps(
                {
                    "labels": {
                        "nature": ["decision", "execution", "research", "document", "follow-up", "bug", "idea"],
                        "domain": ["legal", "finance", "tech", "photo", "branding", "ops", "travel", "science"],
                        "context": ["urgent", "bloque-externe", "en-attente-jch", "delegue", "a-planifier", "quick-win"],
                        "level": ["strategique", "tactique", "operationnel"],
                    },
                    "rules": {
                        "lowercase_only": True,
                        "separator": "-",
                        "state_labels_forbidden": False,
                        "creation_roles": ["Dobby", "Forge"],
                    },
                }
            ),
            encoding="utf-8",
        )

        with mock.patch.object(pka_kanban_schema, "ROOT", self.root):
            with self.assertRaisesRegex(ValueError, "state_labels_forbidden must match the canonical value"):
                pka_kanban_schema.load_governance()

    def test_schema_type_drift_is_rejected(self):
        bad_file = self.root / "JCH_Inbox" / "99_SYSTEM" / "pka_kanban_schema.json"
        bad_file.write_text(
            json.dumps(
                {
                    "statuses": [
                        "A qualifier",
                        "Pret",
                        "En cours",
                        "En attente",
                        "En validation",
                        "Termine",
                        "Archive",
                    ],
                    "types": [
                        "task",
                        "decision",
                        "document",
                        "bug",
                        "idea",
                        "follow-up",
                        "note",
                    ],
                    "required_fields": [
                        "title",
                        "project",
                        "type",
                        "owner",
                        "priority",
                        "status",
                        "description",
                    ],
                    "recommended_fields": [
                        "lead_specialist",
                        "model_used",
                        "decision_owner",
                        "blocking_reason",
                        "expected_outcome",
                        "source_link",
                    ],
                }
            ),
            encoding="utf-8",
        )

        with mock.patch.object(pka_kanban_schema, "ROOT", self.root):
            with self.assertRaisesRegex(ValueError, "types must match the canonical order"):
                pka_kanban_schema.load_schema()


if __name__ == "__main__":
    unittest.main()
