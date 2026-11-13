#!/usr/bin/env python3
"""Backfill data/*.json pour les fiches DÉCOUVERTES qui n'en ont pas (ex: fiches vision).

La page interactive place.html lit data/<slug>.json. Les fiches produites par
identify_skips.py (passe vision) n'en généraient pas → « lieu introuvable ».
Ce script régénère un data/*.json minimal depuis le frontmatter + le corps de la fiche.

Usage :
  python3 backfill_data_json.py
"""
import json
import re
import os
from pathlib import Path

PKA_ROOT = Path(os.getenv("PKA_ROOT", Path(__file__).resolve().parents[2]))
BASE = PKA_ROOT / "JCH_Inbox/03_PROJECTS/07_TRAVELS/pka-decouvertes"
DATA = BASE / "data"
QUEUE = BASE / "queue"
DATA.mkdir(parents=True, exist_ok=True)


def parse_frontmatter(txt: str) -> dict:
    fm = {}
    lines = txt.split("\n")
    if not lines or lines[0].strip() != "---":
        return fm
    for line in lines[1:]:
        if line.strip() == "---":
            break
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", line)
        if m:
            fm[m.group(1)] = m.group(2).strip().strip('"')
    return fm


def body_after_frontmatter(txt: str) -> str:
    parts = txt.split("---", 2)
    return parts[2] if len(parts) >= 3 else txt


def section(body: str, name: str) -> str:
    m = re.search(rf"^## {re.escape(name)}\s*\n(.*?)(?=^## |\Z)", body, re.M | re.S)
    return m.group(1).strip() if m else ""


def slugify(name: str) -> str:
    """Slug sûr pour URL/nom de fichier : [A-Za-z0-9._-], sans accents, tronqué à 40."""
    import unicodedata
    s = unicodedata.normalize("NFKD", name or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^A-Za-z0-9._-]+", "-", s).strip("-")
    return s[:40] or "lieu"


def slug_of(name: str) -> str:
    return slugify(name)


# index source_file -> media file_path (depuis la file d'attente)
media_by_source: dict[str, str] = {}
for q in QUEUE.glob("*.json"):
    try:
        d = json.loads(q.read_text())
        sf = d.get("source_file")
        mf = (d.get("media_files") or [{}])[0].get("file_path")
        if sf and mf:
            media_by_source[sf] = mf
    except Exception:
        pass


count = 0
for d in (BASE / "drafts", BASE / "validated_places"):
    if not d.is_dir():
        continue
    for md in sorted(d.glob("*.md")):
        txt = md.read_text(encoding="utf-8")
        fm = parse_frontmatter(txt)
        nom = fm.get("nom_lieu") or md.stem.split("_", 1)[-1]
        slug = slug_of(nom)
        if (DATA / f"{slug}.json").exists():
            continue
        body = body_after_frontmatter(txt)
        descr = section(body, "Résumé")

        gps_raw = fm.get("gps", "").strip().strip('"')
        lat = lon = None
        if "," in gps_raw:
            try:
                lat, lon = [float(x.strip()) for x in gps_raw.split(",", 1)]
            except ValueError:
                lat = lon = None

        src_line = section(body, "Source")
        m = re.search(r"Image source\s*:\s*([^\s]+)", src_line)
        source_file = m.group(1) if m else None
        media = [media_by_source[source_file]] if source_file in media_by_source else []

        payload = {
            "slug": slug,
            "nom_lieu": nom,
            "pays": fm.get("pays", ""),
            "region": fm.get("region", ""),
            "ville": fm.get("ville", ""),
            "gps": {"lat": lat, "lon": lon} if lat is not None else None,
            "scores": {
                "photo": int(fm.get("interet_photo") or 0),
                "nature": int(fm.get("interet_nature") or 0),
                "patrimoine": int(fm.get("interet_patrimoine") or 0),
                "van": int(fm.get("interet_van") or 0),
            },
            "type_lieu": fm.get("type_lieu", "autre"),
            "confidence": float(fm.get("confidence") or 0),
            "action": fm.get("status", "needs_review"),
            "description": descr,
            "van_info": "",
            "reserves": [],
            "restaurants": [],
            "attractions": [],
            "media_files": media,
            "source": {
                "author": fm.get("auteur", ""),
                "datetime": fm.get("date_capture", ""),
                "text": "",
            },
            "date_analyse": fm.get("date_analyse", ""),
        }
        (DATA / f"{slug}.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        count += 1
        print(f"  data/{slug}.json  <- {md.name}")

print(f"\n{count} data JSON généré(s).")
