import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import scripts.google_calendar_bridge as bridge


class GoogleCalendarBridgeTests(unittest.TestCase):
    def test_build_event_applies_category_color_from_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / "colors.json"
            config.write_text(
                json.dumps({"ADMIN": {"colorId": "8", "label": "Admin / Sante"}}),
                encoding="utf-8",
            )
            with mock.patch.object(bridge, "COLORS_FILE", config):
                event = bridge.build_event(
                    summary="BMW X3 - gros entretien",
                    description="Rendez-vous BMW X3",
                    location="",
                    start="2026-06-04T14:00:00",
                    end="2026-06-04T15:00:00",
                    timezone="Europe/Brussels",
                    category="ADMIN",
                )

        self.assertEqual(event["colorId"], "8")

    def test_build_event_rejects_unknown_category(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = Path(tmp) / "colors.json"
            config.write_text("{}", encoding="utf-8")
            with mock.patch.object(bridge, "COLORS_FILE", config):
                with self.assertRaisesRegex(ValueError, "Unknown calendar category"):
                    bridge.build_event(
                        summary="Event",
                        description="",
                        location="",
                        start="2026-06-04T14:00:00",
                        end="2026-06-04T15:00:00",
                        timezone="Europe/Brussels",
                        category="MISSING",
                    )

    def test_pka_calendar_name_uses_guarded_prefix(self):
        self.assertEqual(
            bridge.pka_calendar_name("WILDNEXUS", {"WILDNEXUS": {"label": "WildNexus"}}),
            "PKA — WildNexus",
        )

    def test_require_pka_calendar_rejects_unmanaged_name(self):
        with self.assertRaisesRegex(ValueError, "Refusing to manage non-PKA calendar"):
            bridge.require_pka_calendar_name("WORK")

    def test_scope_set_detects_missing_saved_scopes(self):
        self.assertFalse(
            bridge.has_required_saved_scopes(
                ["https://www.googleapis.com/auth/calendar.events"],
                [
                    "https://www.googleapis.com/auth/calendar.events",
                    "https://www.googleapis.com/auth/calendar.calendarlist",
                ],
            )
        )

    def test_read_saved_token_scopes_reads_json_scope_list(self):
        with tempfile.TemporaryDirectory() as tmp:
            token = Path(tmp) / "token.json"
            token.write_text(
                json.dumps({"scopes": ["https://www.googleapis.com/auth/calendar.events"]}),
                encoding="utf-8",
            )
            self.assertEqual(
                bridge.read_saved_token_scopes(token),
                ["https://www.googleapis.com/auth/calendar.events"],
            )


if __name__ == "__main__":
    unittest.main()
