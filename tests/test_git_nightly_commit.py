import subprocess
import unittest
from unittest import mock
from pathlib import Path

from scripts.modules import git_nightly_commit


class GitNightlyCommitTest(unittest.TestCase):

    def test_build_commit_message(self):
        msg = git_nightly_commit.build_commit_message("2026-05-28")
        self.assertEqual(msg, "chore(vault): nightly maintenance 2026-05-28")

    def test_build_add_args_contains_main_paths(self):
        args = git_nightly_commit.build_add_args()
        for path in ["JCH_Inbox/", "TEAM/", "TEAM_Inbox/", "docs/", "scripts/"]:
            self.assertIn(path, args)

    def test_build_add_args_excludes_security(self):
        args = git_nightly_commit.build_add_args()
        self.assertNotIn("JCH_Inbox/99_SYSTEM/security/", args)

    def test_nothing_to_commit_returns_false(self):
        with mock.patch("scripts.modules.git_nightly_commit._git_status_empty", return_value=True):
            result = git_nightly_commit.run(date_str="2026-05-28")
        self.assertFalse(result["committed"])
        self.assertEqual(result["reason"], "nothing_to_commit")

    def test_dry_run_does_not_call_subprocess(self):
        with mock.patch("scripts.modules.git_nightly_commit._git_status_empty", return_value=False), \
             mock.patch("subprocess.run") as mock_run:
            result = git_nightly_commit.run(date_str="2026-05-28", dry_run=True)
        mock_run.assert_not_called()
        self.assertFalse(result["committed"])
        self.assertEqual(result["reason"], "dry_run")

    def test_commit_called_when_changes_present(self):
        with mock.patch("scripts.modules.git_nightly_commit._git_status_empty", return_value=False), \
             mock.patch("subprocess.run") as mock_run:
            mock_run.return_value = mock.Mock(returncode=0)
            result = git_nightly_commit.run(date_str="2026-05-28", dry_run=False)
        self.assertTrue(result["committed"])
        add_call = mock_run.call_args_list[0]
        self.assertIn("add", add_call.args[0])

    def test_commit_failure_returns_error(self):
        with mock.patch("scripts.modules.git_nightly_commit._git_status_empty", return_value=False), \
             mock.patch("subprocess.run", side_effect=subprocess.CalledProcessError(1, "git")):
            result = git_nightly_commit.run(date_str="2026-05-28", dry_run=False)
        self.assertFalse(result["committed"])
        self.assertIn("error", result)

    def test_default_date_is_today(self):
        with mock.patch("scripts.modules.git_nightly_commit._git_status_empty", return_value=True):
            result = git_nightly_commit.run()
        # Juste vérifier que ça ne plante pas sans date_str
        self.assertFalse(result["committed"])
