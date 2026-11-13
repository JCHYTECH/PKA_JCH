#!/usr/bin/env python3
"""Surveille ~/Dropbox/VETALYX/ et logue les changements détectés.
Déclenché par launchd via WatchPaths. Utilise un snapshot JSON pour diff."""
import json, os, sys
from datetime import datetime
from pathlib import Path

WATCH_DIR = Path.home() / "Dropbox" / "VETALYX"
LOG_FILE = Path.home() / "PKA_JCH" / "TEAM_Inbox" / "dropbox_vetalyx_changes.log"
SNAPSHOT_FILE = Path.home() / "PKA_JCH" / "tmp" / "dropbox_vetalyx_snapshot.json"

IGNORE_PATTERNS = {".DS_Store", "Icon\r", ".localized"}

def build_snapshot(root: Path) -> dict:
    """Construit un snapshot {chemin_relatif: mtime} du dossier."""
    if not root.exists():
        return {}
    snapshot = {}
    for path in root.rglob("*"):
        if path.is_file() and path.name not in IGNORE_PATTERNS and "~$" not in path.name:
            rel = str(path.relative_to(root))
            snapshot[rel] = path.stat().st_mtime
    return snapshot

def load_snapshot() -> dict:
    if SNAPSHOT_FILE.exists():
        try:
            return json.loads(SNAPSHOT_FILE.read_text())
        except (json.JSONDecodeError, IOError):
            return {}
    return {}

def save_snapshot(snap: dict):
    SNAPSHOT_FILE.parent.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_FILE.write_text(json.dumps(snap, indent=2))

def main():
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    old = load_snapshot()
    new = build_snapshot(WATCH_DIR)

    if not old:
        # Premier lancement : initialiser sans logger
        save_snapshot(new)
        return

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    changes = []

    for f in set(new) - set(old):
        changes.append(f"[+] {f}")
    for f in set(old) - set(new):
        changes.append(f"[-] {f}")
    for f in set(new) & set(old):
        if new[f] != old[f]:
            changes.append(f"[~] {f}")

    if changes:
        with open(LOG_FILE, "a") as lf:
            lf.write(f"\n--- {now} ---\n")
            for c in sorted(changes):
                lf.write(f"  {c}\n")
        print(f"Logged {len(changes)} changes")

    save_snapshot(new)

if __name__ == "__main__":
    main()
