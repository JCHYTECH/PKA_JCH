#!/usr/bin/env python3
"""Purge les images brutes traitées + nettoie les media_files cassés de la queue.

Objectif : libérer l'espace de raw/images/ une fois les captures traitées,
et maintenir la queue propre (sans références à des fichiers disparus).

Règles (basées sur la référence queue -> image, pas sur l'extension) :
1. Pour chaque queue/*.json, chaque media_files[].file_path :
   - fichier absent sur disque  -> retire l'entrée (référence cassée)
   - fichier présent et plus vieux que --days -> supprime le fichier + retire l'entrée
2. Réécrit le JSON uniquement si modifié.

Usage :
  python3 purge_raw_images.py            # purge standard (7 jours)
  python3 purge_raw_images.py --days 0   # purge immédiate des références cassées
  python3 purge_raw_images.py --dry-run  # ne rien écrire
"""
import argparse
import json
import os
import time
from pathlib import Path

PKA_ROOT = Path(os.getenv("PKA_ROOT", Path(__file__).resolve().parents[2]))
BASE = PKA_ROOT / "JCH_Inbox/03_PROJECTS/07_TRAVELS/PKA-DECOUVERTES"
QUEUE = BASE / "QUEUE"


def resolve(fp: str) -> Path:
    p = Path(fp)
    return p if p.is_absolute() else (PKA_ROOT / p)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=7,
                    help="âge (jours) au-delà duquel supprimer une image existante")
    ap.add_argument("--dry-run", action="store_true", help="ne rien écrire")
    args = ap.parse_args()

    cutoff = time.time() - args.days * 86400
    removed_files = 0
    removed_refs = 0
    touched = 0

    for q in sorted(QUEUE.glob("*.json")):
        try:
            data = json.loads(q.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"  skip {q.name}: {e}")
            continue

        mfs = data.get("media_files") or []
        if not mfs:
            continue

        kept = []
        changed = False
        for mf in mfs:
            if not isinstance(mf, dict):
                kept.append(mf)
                continue
            fp = mf.get("file_path", "")
            if not fp:
                kept.append(mf)
                continue
            p = resolve(fp)
            if not p.exists():
                removed_refs += 1
                changed = True
                continue
            try:
                if p.stat().st_mtime < cutoff:
                    if not args.dry_run:
                        p.unlink()
                    removed_files += 1
                    removed_refs += 1
                    changed = True
                    continue
            except OSError:
                removed_refs += 1
                changed = True
                continue
            kept.append(mf)

        if changed:
            data["media_files"] = kept
            if not args.dry_run:
                q.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                             encoding="utf-8")
            touched += 1

    print(f"fichiers image supprimés : {removed_files}")
    print(f"références media_files purgées : {removed_refs}")
    print(f"JSON de queue modifiés : {touched}")


if __name__ == "__main__":
    main()
