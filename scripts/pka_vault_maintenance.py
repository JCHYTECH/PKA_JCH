#!/usr/bin/env python3
"""Entry point — maintenance nocturne du vault PKA_JCH."""

from __future__ import annotations

import logging
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]  # racine du vault
LOG_PATH = ROOT / "scripts" / "logs" / "vault_maintenance.log"
MAX_FILES_SILENT = 50

try:
    from scripts.modules import wikilink_patcher, file_placement_checker, git_nightly_commit
except ModuleNotFoundError:
    from modules import wikilink_patcher, file_placement_checker, git_nightly_commit


def main() -> int:
    # Setup logging — WARNING level uniquement, handler vers LOG_PATH
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[logging.FileHandler(LOG_PATH, encoding="utf-8")],
    )
    log = logging.getLogger(__name__)

    errors = 0
    today = date.today().isoformat()

    # Étape 1 — wikilink_patcher
    try:
        modified = wikilink_patcher.run(ROOT)
        if len(modified) > MAX_FILES_SILENT:
            log.warning("wikilink_patcher: %d fichiers modifiés (> %d)", len(modified), MAX_FILES_SILENT)
    except Exception as exc:
        log.error("wikilink_patcher failed: %s", exc)
        errors += 1

    # Étape 2 — file_placement_checker
    try:
        anomalies = file_placement_checker.check(ROOT)
        for anomaly in anomalies:
            log.warning("file_placement_checker anomaly: path=%s expected=%s", anomaly.get("path"), anomaly.get("expected"))
    except Exception as exc:
        log.error("file_placement_checker failed: %s", exc)
        errors += 1

    # Étape 3 — git_nightly_commit
    try:
        result = git_nightly_commit.run(date_str=today, root=ROOT)
        if result.get("error"):
            log.error("git_nightly_commit error: %s", result["error"])
            errors += 1
    except Exception as exc:
        log.error("git_nightly_commit failed: %s", exc)
        errors += 1

    return 1 if errors > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
