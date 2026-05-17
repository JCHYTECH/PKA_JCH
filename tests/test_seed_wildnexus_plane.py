import unittest

from scripts.seed_wildnexus_plane import module_name_from_epic, parse_seed_backlog, BACKLOG_PATH


class SeedWildNexusPlaneTest(unittest.TestCase):
    def test_parse_seed_backlog_extracts_core_sections(self):
        seed = parse_seed_backlog(BACKLOG_PATH)

        self.assertIn("M-01 Architecture gelee", seed["milestones"])
        self.assertIn("EPIC: WP01 - Conception & Architecture", seed["epics"])
        self.assertIn("WP01", seed["tasks"])
        self.assertIn(
            "T01.3 Campagne mesures RF terrain",
            seed["tasks"]["WP01"],
        )

    def test_module_name_from_epic_matches_operating_model(self):
        self.assertEqual(
            module_name_from_epic("EPIC: WP05 - Validation terrain EVT"),
            "WP05 - Validation terrain EVT",
        )


if __name__ == "__main__":
    unittest.main()
