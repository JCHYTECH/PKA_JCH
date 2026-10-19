#!/usr/bin/env python3
"""Importe les lieux enregistrés Google Maps (export Google Takeout) dans PKA DÉCOUVERTES.

Lit les fichiers JSON de « Maps (vos adresses) » (export Google Takeout) :
  - Adresses enregistrées.json   (Enregistrés / Saved)
  - Lieux favoris.json           (Favoris)
  - Envie d'y aller.json         (Want to go)
  - Lieux suivis.json            (Suivis / Starred)
  - ... et tout autre *.json présent dans le dossier Maps

Fusionne les lieux dans lieux_google_maps.csv (schéma 6 colonnes), avec les
coordonnées GPS EXACTES (pas de re-géocodage par nom). Gère le format récent
(keys snake_case : location.name, google_maps_url, geometry.coordinates) ET
l'ancien format (Title, Location.Business Name, Geo Coordinates).

Usage :
  python3 import_takeout.py "~/Downloads/Takeout"                       # dossier extrait
  python3 import_takeout.py "~/Downloads/Takeout/Maps (vos adresses)"   # ou le sous-dossier Maps
  python3 import_takeout.py ".../Adresses enregistrées.json"            # ou un fichier précis
  python3 import_takeout.py --dry-run --no-geocode "..."                # aperçu sans réseau

Options :
  --dry-run      Affiche ce qui serait ajouté, sans écrire.
  --no-geocode   N'interroge pas Nominatim (pays/région via country_code si dispo).
  --list         Liste les fichiers reconnus, sans importer.
"""
import argparse
import csv
import json
import os
import sys
import time
from pathlib import Path

import requests

PKA_ROOT = Path(os.getenv("PKA_ROOT", Path(__file__).resolve().parents[2]))
BASE = PKA_ROOT / "JCH_Inbox/03_PROJECTS/07_TRAVELS/pka-decouvertes"
CSV_PATH = BASE / "lieux_google_maps.csv"
HDR = ["Name", "Description", "Latitude", "Longitude", "Country", "Region"]

# Étiquettes FR/EN des listes connues (affichage --list uniquement)
LIST_LABELS = {
    "adresses enregistrées": "enregistrés",
    "lieux favoris": "favoris",
    "envie d'y aller": "envie d'y aller",
    "lieux suivis": "suivis",
    "lieux libellés": "libellés",
    "saved places": "enregistrés",
    "favorites": "favoris",
    "want to go": "envie d'y aller",
    "starred places": "suivis",
    "my labeled places": "libellés",
    "labeled places": "libellés",
}

UA = {"User-Agent": "PKA_DECOUVERTES/1.0 (import_takeout)"}

# Code pays ISO 3166-1 alpha-2 → nom FR (fallback offline)
CC2COUNTRY = {
    "FR": "France", "BE": "Belgique", "CH": "Suisse", "DE": "Allemagne",
    "NL": "Pays-Bas", "LU": "Luxembourg", "IT": "Italie", "ES": "Espagne",
    "PT": "Portugal", "GB": "Royaume-Uni", "IE": "Irlande", "AT": "Autriche",
    "DK": "Danemark", "NO": "Norvège", "SE": "Suède", "FI": "Finlande",
    "PL": "Pologne", "CZ": "Tchéquie", "HU": "Hongrie", "HR": "Croatie",
    "SI": "Slovénie", "SK": "Slovaquie", "RO": "Roumanie", "GR": "Grèce",
    "US": "États-Unis", "CA": "Canada", "MA": "Maroc", "TN": "Tunisie",
    "DZ": "Algérie", "JP": "Japon", "CN": "Chine", "AU": "Australie",
}


def _maps_dir(path: Path) -> Path | None:
    """Retourne le sous-dossier 'Maps (vos adresses)' / 'Maps (your places)'. """
    if path.is_dir():
        for name in ("Maps (vos adresses)", "Maps (your places)", "Maps"):
            cand = path / name
            if cand.is_dir():
                return cand
        # sinon le dossier lui-même s'il contient directement des .json de lieux
        if any(path.glob("*.json")):
            return path
    return None


def find_takeout_files(path: Path) -> list[Path]:
    """Retourne les .json de lieux à importer (fichier, dossier, ou sous-dossier Maps)."""
    if path.is_file():
        return [path]
    maps = _maps_dir(path)
    if maps:
        return sorted(maps.glob("*.json"))
    # recherche récursive de secours (profondeur limitée)
    return sorted(p for p in path.rglob("*.json") if "archive_browser" not in p.name)


def _label(f: Path) -> str:
    return LIST_LABELS.get(f.stem.lower(), "liste")


def parse_feature(feature: dict) -> dict | None:
    """Extrait un lieu d'un feature GeoJSON-like (format récent snake_case + ancien)."""
    geom = feature.get("geometry") or {}
    props = feature.get("properties") or {}

    lat = lon = None
    coords = geom.get("coordinates")
    if isinstance(coords, list) and len(coords) >= 2:
        lon, lat = coords[0], coords[1]

    # ── format récent : properties.location.{name,address,country_code} ──
    loc = props.get("location") or props.get("Location") or {}
    name = (
        loc.get("name")
        or loc.get("Name")
        or loc.get("Business Name")
        or props.get("title")
        or props.get("Title")
        or props.get("name")
        or ""
    ).strip()

    addr = loc.get("address") or loc.get("Address") or ""
    cc = loc.get("country_code") or loc.get("Country Code") or ""
    url = (
        props.get("google_maps_url")
        or props.get("Google Maps URL")
        or props.get("url")
        or ""
    )
    note = props.get("note") or props.get("Note") or ""

    # coordonnées via Geo Coordinates (ancien format) si absentes de geometry
    if lat is None:
        geo = props.get("Geo Coordinates") or {}
        if geo:
            lat = geo.get("Latitude", geo.get("latitude"))
            lon = geo.get("Longitude", geo.get("longitude"))

    if not name:
        return None
    try:
        lat = float(lat)
        lon = float(lon)
    except (TypeError, ValueError):
        return None

    return {
        "name": name,
        "lat": lat,
        "lon": lon,
        "address": (addr or "").strip(),
        "url": (url or "").strip(),
        "note": (note or "").strip(),
        "country_code": (cc or "").strip().upper(),
    }


def reverse_geocode(lat: float, lon: float) -> tuple[str, str]:
    """Reverse geocode (pays, région) via Nominatim. Respecte la politesse (1 req)."""
    try:
        r = requests.get(
            "https://nominatim.openstreetmap.org/reverse",
            params={"lat": lat, "lon": lon, "format": "json", "addressdetails": 1},
            headers=UA,
            timeout=10,
        )
        data = r.json()
        addr = data.get("address", {})
        country = addr.get("country", "")
        region = (
            addr.get("state")
            or addr.get("county")
            or addr.get("region")
            or addr.get("province")
            or ""
        )
        return country, region
    except Exception:
        return "", ""


def load_existing_keys() -> set:
    if not CSV_PATH.is_file():
        return set()
    keys = set()
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        for row in csv.reader(f):
            if len(row) < 4:
                continue
            if row[0].strip().lower() == "name":
                continue
            try:
                k = (row[0].strip().lower(), round(float(row[2]), 5), round(float(row[3]), 5))
            except ValueError:
                k = (row[0].strip().lower(), row[2], row[3])
            keys.add(k)
    return keys


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("path", help="fichier, dossier extrait Takeout, ou sous-dossier Maps")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-geocode", action="store_true")
    ap.add_argument("--list", action="store_true", help="liste les fichiers reconnus")
    args = ap.parse_args()

    src = Path(os.path.expanduser(args.path))
    if not src.exists():
        print(f"✗ Introuvable : {src}")
        return 1

    files = find_takeout_files(src)
    if not files:
        print("✗ Aucun fichier JSON de lieux trouvé (attendu : 'Adresses enregistrées.json', …).")
        print("  Pointe vers le dossier extrait 'Takeout' ou vers 'Takeout/Maps (vos adresses)'.")
        return 1

    if args.list:
        for f in files:
            print(f"  • {f.name}  ({_label(f)})")
        return 0

    # Parsing
    places: list[dict] = []
    for f in files:
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"✗ Erreur lecture {f.name} : {e}")
            continue
        feats = data.get("features", []) if isinstance(data, dict) else []
        n_before = len(places)
        for feat in feats:
            p = parse_feature(feat)
            if p:
                p["_list"] = _label(f)
                places.append(p)
        print(f"  {f.name} : {len(places) - n_before} lieu(x)")

    if not places:
        print("✗ Aucun lieu trouvé dans ces fichiers.")
        return 1

    existing = load_existing_keys()
    new_rows: list[list] = []
    skipped = 0
    for p in places:
        k = (p["name"].lower(), round(p["lat"], 5), round(p["lon"], 5))
        if k in existing:
            skipped += 1
            continue
        country, region = ("", "")
        if args.no_geocode:
            country = CC2COUNTRY.get(p["country_code"], p["country_code"])
        else:
            country, region = reverse_geocode(p["lat"], p["lon"])
            time.sleep(1.0)  # politesse Nominatim
        desc_bits = [x for x in (p["note"], p["address"], p["url"]) if x]
        desc = " · ".join(desc_bits)
        new_rows.append([p["name"], desc, f"{p['lat']:.7f}", f"{p['lon']:.7f}", country, region])

    print(f"\n  Nouveaux lieux : {len(new_rows)}   (déjà présents ignorés : {skipped})")

    if args.dry_run:
        print("\n── aperçu (dry-run) ──")
        for r in new_rows:
            print(f"  + {r[0]}  ({r[2]}, {r[3]})  {r[4]} / {r[5]}")
        return 0

    existing_rows = []
    if CSV_PATH.is_file():
        with open(CSV_PATH, newline="", encoding="utf-8") as f:
            existing_rows = list(csv.reader(f))
    body = existing_rows[1:] if existing_rows and existing_rows[0][0].strip().lower() == "name" else existing_rows

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(HDR)
        w.writerows(body)
        w.writerows(new_rows)

    print(f"\n✓ {len(new_rows)} lieu(x) ajouté(s) à {CSV_PATH.name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
