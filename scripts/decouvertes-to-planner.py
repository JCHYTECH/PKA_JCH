#!/usr/bin/env python3
"""Pont DÉCOUVERTES → Lupo Planner.

Convertit les fiches de pka-decouvertes en un JSON importable par le Lupo Planner
(bouton « Importer JSON »). Deux sources :

  - spots_van/*.md          → spots de bivouac (type aire/camping/prive/sauvage)
  - validated_places/*.md   → points d'intérêt à visiter (type poi)

Les fiches sans coordonnées exploitables (gps: "à compléter") sont ignorées.

Usage :
  python3 scripts/decouvertes-to-planner.py                # JSON dans le dossier TRAVELS
  python3 scripts/decouvertes-to-planner.py --out /tmp/x.json
  python3 scripts/decouvertes-to-planner.py --dry-run      # stats sans écrire
"""
import argparse
import hashlib
import re
import sys
import time
import uuid
from pathlib import Path

PKA_ROOT = Path(__file__).resolve().parents[1]
BASE = PKA_ROOT / "JCH_Inbox/03_PROJECTS/07_TRAVELS/pka-decouvertes"
SPOTS_VAN = BASE / "spots_van"
VALIDATED = BASE / "validated_places"
DEFAULT_OUT = PKA_ROOT / "JCH_Inbox/03_PROJECTS/07_TRAVELS" / "lupo-planner-import.json"

# Pays → code ISO (le Planner ne connaît que FR ES IT DE BE NL)
PAYS_TO_ISO = {
    "france": "FR",
    "espagne": "ES",
    "italie": "IT",
    "allemagne": "DE",
    "belgique": "BE",
    "pays-bas": "NL",
    "pays bas": "NL",
    "néerlande": "NL",
    "netherlands": "NL",
    "belgium": "BE",
    "germany": "DE",
    "spain": "ES",
    "italy": "IT",
    "france": "FR",
}

# type_aire → type Planner (pour spots_van)
TYPE_AIRE_TO_TYPE = {
    "aire": "aire",
    "camping": "camping",
    "ferme": "prive",
    "prive": "prive",
    "sauvage": "sauvage",
    "isole": "camping_isole",
}

# source → source Planner (valeurs connues, sinon "other")
KNOWN_SOURCES = {
    "park4night", "france_passion", "campspace", "huttopia",
    "campercontact", "ioverlander", "landvergnugen", "agricamper",
    "espana_discovery",
}


def parse_frontmatter(text: str) -> dict:
    """Extrait le frontmatter YAML simple (clé: valeur, tags en liste)."""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end]
    fm = {}
    for line in block.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm


def parse_gps(gps: str):
    """'lat, lng' → (lat, lng) floats, ou None si invalide."""
    if not gps:
        return None
    m = re.match(r"\s*(-?\d+\.?\d*)\s*[,;]\s*(-?\d+\.?\d*)\s*$", gps)
    if not m:
        return None
    try:
        lat, lng = float(m.group(1)), float(m.group(2))
    except ValueError:
        return None
    # coordonnées plausibles
    if not (-90 <= lat <= 90 and -180 <= lng <= 180):
        return None
    if lat == 0 and lng == 0:
        return None
    return lat, lng


def stable_id(name: str, lat: float, lng: float) -> str:
    """UUID v5-like déterministe : le ré-import fusionne sans doublon."""
    key = f"{name}|{lat:.5f}|{lng:.5f}".encode("utf-8")
    h = hashlib.md5(key).hexdigest()
    return str(uuid.UUID(hex=h))


def iso_country(pays: str) -> str:
    p = (pays or "").strip().lower()
    return PAYS_TO_ISO.get(p, "FR")


def map_type_aire(type_aire: str) -> str:
    t = (type_aire or "").strip().lower()
    for needle, out in TYPE_AIRE_TO_TYPE.items():
        if needle in t:
            return out
    return "aire"


def map_source(source: str) -> str:
    s = (source or "").strip().lower().replace(" ", "_")
    return s if s in KNOWN_SOURCES else "other"


def spot_from_van_fiche(fm: dict) -> dict | None:
    name = fm.get("nom_spot") or fm.get("nom_lieu") or ""
    if not name:
        return None
    g = parse_gps(fm.get("gps", ""))
    if not g:
        return None
    lat, lng = g
    notes = []
    if fm.get("note"):
        notes.append(f"Note {fm['note']}/5")
    if fm.get("avis"):
        notes.append(f"{fm['avis']} avis")
    if fm.get("type_aire"):
        notes.append(fm["type_aire"])
    return {
        "id": stable_id(name, lat, lng),
        "name": name,
        "lat": lat,
        "lng": lng,
        "type": map_type_aire(fm.get("type_aire", "")),
        "country": iso_country(fm.get("pays", "")),
        "source": map_source(fm.get("source", "")),
        "notes": " · ".join(notes),
        "visited": False,
        "favorite": False,
        "createdAt": int(time.time() * 1000),
    }


def poi_from_validated_fiche(fm: dict) -> dict | None:
    name = fm.get("nom_lieu") or fm.get("nom_spot") or ""
    if not name:
        return None
    g = parse_gps(fm.get("gps", ""))
    if not g:
        return None
    lat, lng = g
    notes = []
    if fm.get("interet_photo"):
        notes.append(f"Photo {fm['interet_photo']}/5")
    if fm.get("interet_patrimoine"):
        notes.append(f"Patrimoine {fm['interet_patrimoine']}/5")
    if fm.get("van_friendly"):
        notes.append(f"Van: {fm['van_friendly']}")
    return {
        "id": stable_id(name, lat, lng),
        "name": name,
        "lat": lat,
        "lng": lng,
        "type": "poi",
        "country": iso_country(fm.get("pays", "")),
        "source": map_source(fm.get("source", "")),
        "notes": " · ".join(notes),
        "visited": False,
        "favorite": False,
        "createdAt": int(time.time() * 1000),
    }


def collect() -> tuple[list[dict], dict]:
    spots = []
    stats = {"spots_van_total": 0, "spots_van_ok": 0,
             "validated_total": 0, "validated_ok": 0,
             "skipped_no_gps": 0}

    for p in sorted(SPOTS_VAN.glob("*.md")) if SPOTS_VAN.is_dir() else []:
        stats["spots_van_total"] += 1
        fm = parse_frontmatter(p.read_text(encoding="utf-8"))
        s = spot_from_van_fiche(fm)
        if s:
            spots.append(s)
            stats["spots_van_ok"] += 1
        else:
            stats["skipped_no_gps"] += 1

    for p in sorted(VALIDATED.glob("*.md")) if VALIDATED.is_dir() else []:
        stats["validated_total"] += 1
        fm = parse_frontmatter(p.read_text(encoding="utf-8"))
        s = poi_from_validated_fiche(fm)
        if s:
            spots.append(s)
            stats["validated_ok"] += 1
        else:
            stats["skipped_no_gps"] += 1

    return spots, stats


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    spots, stats = collect()
    data = {
        "version": 1,
        "exportedAt": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "source": "pka-decouvertes",
        "spots": spots,
        "roadtrips": [],
    }

    print(f"spots_van       : {stats['spots_van_ok']}/{stats['spots_van_total']} convertis")
    print(f"validated_places: {stats['validated_ok']}/{stats['validated_total']} convertis (POI)")
    print(f"ignorés (sans GPS): {stats['skipped_no_gps']}")
    print(f"total spots     : {len(spots)}")

    if args.dry_run:
        return 0

    out = Path(args.out)
    out.write_text(
        __import__("json").dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\n✓ JSON écrit → {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
