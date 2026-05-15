import unittest

from scripts import pka_system_check


class PkaSystemCheckTest(unittest.TestCase):
    def test_global_status_turns_red_when_any_check_is_red(self):
        result = pka_system_check.combine_results(
            {"status": "green", "findings": []},
            {"status": "red", "findings": [{"severity": "high"}]},
            {"status": "green", "details": []},
            {"status": "green", "details": []},
        )
        self.assertEqual(result["status"], "red")

    def test_global_status_turns_orange_when_any_check_is_orange(self):
        result = pka_system_check.combine_results(
            {"status": "green", "findings": []},
            {"status": "orange", "findings": [{"severity": "medium"}]},
            {"status": "green", "details": []},
            {"status": "green", "details": []},
        )
        self.assertEqual(result["status"], "orange")

    def test_global_status_turns_orange_when_promotion_backlog_exists(self):
        result = pka_system_check.combine_results(
            {"status": "green", "findings": []},
            {"status": "green", "findings": []},
            {"status": "green", "details": []},
            {"status": "orange", "details": ["2 instincts ready for promotion"]},
        )
        self.assertEqual(result["status"], "orange")

    def test_markdown_report_includes_promotion_section(self):
        result = {
            "generated_at": "2026-05-14T13:00:00",
            "status": "orange",
            "security": {"status": "green", "findings": []},
            "improvement": {"status": "green", "findings": []},
            "pointers": {"status": "green", "details": []},
            "promotion": {"status": "orange", "details": ["1 instinct ready for promotion"]},
        }
        markdown = pka_system_check.markdown_report(result)
        self.assertIn("Instinct Promotion", markdown)
        self.assertIn("1 instinct ready for promotion", markdown)


if __name__ == "__main__":
    unittest.main()
