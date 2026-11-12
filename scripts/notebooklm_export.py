#!/usr/bin/env python3
"""Exporte les artefacts (sorties) de NotebookLM vers 00_INBOX/notebooklm/.

Pour chaque notebook, télécharge la DERNIÈRE version de chaque type d'artefact
(slide-deck, report, mind-map, infographic, audio, flashcards, video, data-table).
Les artefacts de type "file" ne sont pas téléchargeables via le CLI (signalés).

Usage : .venv/bin/python scripts/notebooklm_export.py
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys

NLM = "/Users/jchavauxm5/PKA_JCH/.venv/bin/notebooklm"
BASE = "/Users/jchavauxm5/PKA_JCH/JCH_Inbox/00_INBOX/notebooklm"

DL_MAP = {
    "audio": "audio",
    "slide_deck": "slide-deck",
    "report": "report",
    "mind_map": "mind-map",
    "infographic": "infographic",
    "flashcards": "flashcards",
    "video": "video",
    "data_table": "data-table",
    "quiz": "quiz",
}


def run(args: list[str], cwd: str | None = None) -> str:
    r = subprocess.run([NLM] + args, capture_output=True, text=True, cwd=cwd)
    return r.stdout


def jload(s: str):
    i = s.find("{")
    return json.loads(s[i:]) if i >= 0 else None


def slug(t: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]+", "-", t).strip("-").lower()[:60]


def main() -> int:
    os.makedirs(BASE, exist_ok=True)
    nbs = (jload(run(["list", "--json"])) or {}).get("notebooks", [])
    downloaded = 0
    skipped_files: list[tuple[str, str]] = []

    for nb in nbs:
        aid, title = nb["id"], nb["title"]
        adata = jload(run(["artifact", "list", "-n", aid, "--json"]))
        arts = (adata or {}).get("artifacts", [])
        if not arts:
            continue
        d = os.path.join(BASE, slug(title))
        os.makedirs(d, exist_ok=True)
        run(["use", aid])
        for t in sorted({a["type_id"] for a in arts}):
            if t == "file":
                for a in arts:
                    if a["type_id"] == "file":
                        skipped_files.append((title, a["title"]))
                continue
            cmd = DL_MAP.get(t)
            if not cmd:
                continue
            run(["download", cmd], cwd=d)
            downloaded += 1
            print(f"OK {title[:50]:50s} [{t}]", flush=True)

    print(f"\nTOTAL téléchargé : {downloaded} (dernière version par type)", flush=True)
    if skipped_files:
        print("\nFichiers 'file' non téléchargeables via CLI (à récupérer manuellement) :", flush=True)
        for t, f in skipped_files:
            print(f"  - {t} :: {f}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
