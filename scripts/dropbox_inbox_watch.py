#!/usr/bin/env python3
"""
Surveille ~/Dropbox/00_INBOX/ et importe les nouveaux fichiers dans JCH_Inbox/00_INBOX/.

Déclenché par launchd via WatchPaths.
Utilise un snapshot JSON pour détecter les ajouts.
Les fichiers sont copiés (pas déplacés) — l'original reste dans Dropbox.
"""

import json
import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

DROPBOX_INBOX = Path.home() / "Dropbox" / "00_INBOX"
PKA_INBOX = Path.home() / "PKA_JCH" / "JCH_Inbox" / "00_INBOX"
SNAPSHOT_FILE = Path.home() / "PKA_JCH" / "_local" / "dropbox_inbox_snapshot.json"
LOG_FILE = Path.home() / "PKA_JCH" / "TEAM_Inbox" / "dropbox_inbox_imports.log"

IGNORE_PATTERNS = {".DS_Store", "Icon\r", ".localized", ".processed"}


def build_snapshot(root: Path) -> dict[str, float]:
    """Construit un snapshot {chemin_relatif: mtime} du dossier."""
    if not root.exists():
        return {}
    snapshot = {}
    for path in root.rglob("*"):
        if path.is_file() and path.name not in IGNORE_PATTERNS and "~$" not in path.name:
            rel = str(path.relative_to(root))
            snapshot[rel] = path.stat().st_mtime
    return snapshot


def load_snapshot() -> dict[str, float]:
    if SNAPSHOT_FILE.exists():
        try:
            return json.loads(SNAPSHOT_FILE.read_text())
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def save_snapshot(snap: dict[str, float]) -> None:
    SNAPSHOT_FILE.parent.mkdir(parents=True, exist_ok=True)
    SNAPSHOT_FILE.write_text(json.dumps(snap, indent=2))


def main() -> None:
    PKA_INBOX.mkdir(parents=True, exist_ok=True)
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    if not DROPBOX_INBOX.exists():
        print(f"⚠️  Dropbox 00_INBOX introuvable: {DROPBOX_INBOX}", file=sys.stderr)
        return

    old = load_snapshot()
    new = build_snapshot(DROPBOX_INBOX)

    if not old:
        # Premier lancement : initialiser sans importer
        save_snapshot(new)
        print(f"Snapshot initialisé — {len(new)} fichiers existants ignorés")
        return

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    imported = []

    for rel_path in set(new) - set(old):
        src = DROPBOX_INBOX / rel_path
        dst = PKA_INBOX / rel_path

        # Créer les sous-dossiers si nécessaire
        dst.parent.mkdir(parents=True, exist_ok=True)

        try:
            shutil.copy2(src, dst)
            imported.append(rel_path)
        except OSError as e:
            print(f"  ⚠️  Erreur copie {rel_path}: {e}", file=sys.stderr)

    if imported:
        with open(LOG_FILE, "a") as lf:
            lf.write(f"\n--- {now} — {len(imported)} fichier(s) importé(s) ---\n")
            for f in sorted(imported):
                lf.write(f"  [+] {f}\n")
        print(f"Importé {len(imported)} fichier(s) dans JCH_Inbox/00_INBOX/")

    save_snapshot(new)


if __name__ == "__main__":
    main()
