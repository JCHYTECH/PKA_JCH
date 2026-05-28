#!/usr/bin/env python3
"""Utilitaire partagé — écriture dans memory_log pour les scripts automatisés."""

import sqlite3
from datetime import date
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "TEAM" / "team.db"


def log_run(
    script: str,
    status: str,
    body: str,
    project_key: str | None = None,
    model: str = "automation",
) -> None:
    """Enregistre une exécution automatisée dans memory_log.

    Args:
        script: nom du script (ex. 'backup_team_db')
        status: 'ok' ou 'error'
        body: résumé de l'exécution (1-2 lignes)
        project_key: projet PKA concerné (optionnel)
        model: identifiant runtime (défaut: 'automation')
    """
    event_type = "cron_ok" if status == "ok" else "cron_error"
    try:
        with sqlite3.connect(DB) as con:
            con.execute(
                """INSERT INTO memory_log
                   (memory_file, memory_name, memory_type, model,
                    event_type, body, project_key, created_at)
                   VALUES (?, ?, 'automation', ?, ?, ?, ?, ?)""",
                (
                    f"scripts/{script}.py",
                    f"{script}-{date.today().isoformat()}",
                    model,
                    event_type,
                    body[:500],
                    project_key,
                    date.today().isoformat(),
                ),
            )
    except (OSError, sqlite3.DatabaseError):
        pass
