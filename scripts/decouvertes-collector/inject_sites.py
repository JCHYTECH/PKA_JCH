#!/usr/bin/env python3
"""Injecte les screenshots de JCH_Inbox/00_INBOX/SITES/ dans la file d'attente DÉCOUVERTES.

Comble le gap MODE A du SKILL pka-decouvertes (injection manuelle image par image).

Usage :
  python3 inject_sites.py                          # tous les .jpeg/.jpg/.png de SITES/
  python3 inject_sites.py IMG_0797.jpeg IMG_0798.jpeg   # fichiers précis
"""
import datetime
import json
import os
import shutil
import sys
from pathlib import Path

PKA_ROOT = Path(os.getenv("PKA_ROOT", Path(__file__).resolve().parents[2]))
BASE = PKA_ROOT / "JCH_Inbox/03_PROJECTS/07_TRAVELS/pka-decouvertes"
SITES = PKA_ROOT / "JCH_Inbox/00_INBOX/SITES"
RAW_IMAGES = BASE / "raw/images"
QUEUE = BASE / "queue"

RAW_IMAGES.mkdir(parents=True, exist_ok=True)
QUEUE.mkdir(parents=True, exist_ok=True)

# Déduplication : on n'injecte pas une source déjà présente en file.
injected_sources = set()
for q in QUEUE.glob("*.json"):
    try:
        d = json.loads(q.read_text())
        sf = d.get("source_file")
        if sf:
            injected_sources.add(sf)
    except Exception:
        pass

args = sys.argv[1:]
if args:
    files = [SITES / a for a in args]
else:
    files = sorted(
        f for f in SITES.glob("*")
        if f.suffix.lower() in {".jpeg", ".jpg", ".png"}
    )

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
n = 0
for f in files:
    if not f.is_file():
        print(f"skip (absent)   : {f.name}")
        continue
    if f.name in injected_sources:
        print(f"skip (déjà en file) : {f.name}")
        continue
    n += 1
    slug = f"{ts}_{n}"
    dst = RAW_IMAGES / f"{slug}.jpg"
    shutil.copy2(f, dst)
    payload = {
        "telegram_message_id": "0",
        "telegram_group": "SITES",
        "author": "JCH",
        "datetime": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "content_type": "screenshot",
        "text": "",
        "links": [],
        "media_files": [{
            "file_path": str(dst.relative_to(PKA_ROOT)),
            "media_type": "screenshot",
        }],
        "analysis_status": "pending",
        "place_candidates": [],
        "confidence": None,
        "source_file": f.name,
    }
    (QUEUE / f"{slug}.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2)
    )
    print(f"injected {slug} <- {f.name}")

print(f"\n{n} image(s) injectée(s).")
