#!/usr/bin/env python3
"""Daily backup of team.db. Castor's tool — keeps the last 30 days, prunes older."""

import shutil, sqlite3
from datetime import datetime, timedelta
from pathlib import Path

DB    = Path(__file__).resolve().parent.parent / "TEAM" / "team.db"
DEST  = Path(__file__).resolve().parent.parent / "TEAM" / "backups"
KEEP  = 30  # days

def main() -> None:
    DEST.mkdir(exist_ok=True)
    stamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    target = DEST / f"team_{stamp}.db"

    # use SQLite Online Backup API for a consistent snapshot
    src = sqlite3.connect(DB)
    dst = sqlite3.connect(target)
    with dst:
        src.backup(dst)
    src.close()
    dst.close()

    cutoff = datetime.now() - timedelta(days=KEEP)
    for f in DEST.glob("team_*.db"):
        if datetime.fromtimestamp(f.stat().st_mtime) < cutoff:
            f.unlink()

    print(f"Backup written: {target.name}")

if __name__ == "__main__":
    main()
