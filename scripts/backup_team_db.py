#!/usr/bin/env python3
"""Daily backup of team.db. Castor's tool — keeps the last 30 days, prunes older."""

import os
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

from pka_memory_log import log_run

DB    = Path(__file__).resolve().parent.parent / "TEAM" / "team.db"
DEST  = Path(__file__).resolve().parent.parent / "TEAM" / "backups"
KEEP  = 30  # days

def integrity_check(path: Path) -> None:
    con = sqlite3.connect(path)
    try:
        result = con.execute("PRAGMA integrity_check;").fetchone()
    finally:
        con.close()

    if not result or result[0] != "ok":
        raise RuntimeError(f"SQLite integrity check failed for {path}")


def main() -> None:
    if not DB.exists():
        raise FileNotFoundError(f"Source database not found: {DB}")

    DEST.mkdir(exist_ok=True)
    os.chmod(DEST, 0o755)

    stamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    target = DEST / f"team_{stamp}.db"

    # use SQLite Online Backup API for a consistent snapshot
    src = sqlite3.connect(DB)
    dst = sqlite3.connect(target)
    with dst:
        src.backup(dst)
    src.close()
    dst.close()
    os.chmod(target, 0o600)
    try:
        integrity_check(target)
    except Exception:
        target.unlink(missing_ok=True)
        raise

    cutoff = datetime.now() - timedelta(days=KEEP)
    pruned = 0
    for f in DEST.glob("team_*.db"):
        if datetime.fromtimestamp(f.stat().st_mtime) < cutoff:
            f.unlink()
            pruned += 1

    msg = f"Backup written: {target.name} size={target.stat().st_size} mode=0600 pruned={pruned}"
    print(msg)
    log_run("backup_team_db", "ok", msg)

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        log_run("backup_team_db", "error", str(exc))
        raise
