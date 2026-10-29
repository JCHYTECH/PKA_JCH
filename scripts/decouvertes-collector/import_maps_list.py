#!/usr/bin/env python3
"""Importe une liste Google Maps partagée (lien maps.app.goo.gl / placelists) dans PKA DÉCOUVERTES.

Lit une liste publique partagée depuis Google Maps, extrait les lieux (nom + coordonnées
GPS exactes) via l'endpoint interne entitylist/getlist, et fusionne dans
lieux_google_maps.csv (schéma 6 colonnes), en dédupliquant contre l'existant.

Usage :
  python3 import_maps_list.py "https://maps.app.goo.gl/xxx"
  python3 import_maps_list.py --dry-run --no-geocode "https://maps.app.goo.gl/xxx"

Options :
  --dry-run      Affiche ce qui serait ajouté, sans écrire.
  --no-geocode   N'interroge pas Nominatim (pays/région laissés vides).
"""
import argparse
import csv
import html
import json
import os
import re
import sys
import time
from pathlib import Path
from urllib.parse import urljoin

import requests

PKA_ROOT = Path(os.getenv("PKA_ROOT", Path(__file__).resolve().parents[2]))
BASE = PKA_ROOT / "JCH_Inbox/03_PROJECTS/07_TRAVELS/pka-decouvertes"
CSV_PATH = BASE / "lieux_google_maps.csv"
HDR = ["Name", "Description", "Latitude", "Longitude", "Country", "Region"]

# UA « curl » : Google sert la page server-side (avec le preload entitylist/getlist).
# Un UA navigateur déclenche l'interstitielle JS (page ~34 Ko sans données).
UA = {"User-Agent": "curl/8.4.0"}

GETLIST_RE = re.compile(r"/maps/preview/entitylist/getlist[^\"'\\\s]+")


def http_get(url: str) -> requests.Response:
    return requests.get(url, headers=UA, allow_redirects=True, timeout=25)


def resolve_getlist_url(link: str) -> str | None:
    """Résout le lien court → page → URL interne entitylist/getlist."""
    r = http_get(link)
    page = html.unescape(r.text).replace("\\/", "/")
    m = GETLIST_RE.search(page)
    if not m:
        return None
    return urljoin(r.url, m.group(0))


def fetch_entitylist(url: str) -> dict:
    r = http_get(url)
    text = r.text.strip()
    if text.startswith(")]}'"):
        text = text[4:].lstrip("\n")
    return json.loads(text)


def extract_places(data: dict) -> tuple[str, list[dict]]:
    """Extrait (nom de liste, [lieux]) depuis la structure entitylist."""
    root = data[0]
    list_name = root[4] if len(root) > 4 and isinstance(root[4], str) else ""
    places_raw = root[8] if len(root) > 8 and isinstance(root[8], list) else []
    places = []
    for p in places_raw:
        if not isinstance(p, list) or len(p) < 3:
            continue
        name = p[2]
        if not isinstance(name, str) or not name.strip():
            continue
        coord = None
        meta = p[1] if isinstance(p[1], list) and len(p[1]) > 5 else None
        if meta and isinstance(meta[5], list) and len(meta[5]) >= 4:
            coord = meta[5]
        if not coord:
            continue
        try:
            lat = float(coord[2])
            lon = float(coord[3])
        except (TypeError, ValueError, IndexError):
            continue
        places.append({"name": name.strip(), "lat": lat, "lon": lon})
    return list_name, places


def reverse_geocode(lat: float, lon: float) -> tuple[str, str]:
    try:
        r = requests.get(
            "https://nominatim.openstreetmap.org/reverse",
            params={"lat": lat, "lon": lon, "format": "json", "addressdetails": 1},
            headers={"User-Agent": "PKA_DECOUVERTES/1.0"},
            timeout=10,
        )
        addr = r.json().get("address", {})
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
            if len(row) < 4 or row[0].strip().lower() == "name":
                continue
            try:
                keys.add((row[0].strip().lower(), round(float(row[2]), 5), round(float(row[3]), 5)))
            except ValueError:
                keys.add((row[0].strip().lower(), row[2], row[3]))
    return keys


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("link", help="lien de partage Google Maps (maps.app.goo.gl/… ou google.com/maps/…)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-geocode", action="store_true")
    args = ap.parse_args()

    print("Résolution du lien…")
    getlist = resolve_getlist_url(args.link)
    if not getlist:
        print("✗ Impossible de trouver les données de la liste.")
        print("  Vérifie que la liste est bien PUBLIQUE (paramètre de partage « Tous »).")
        return 1

    data = fetch_entitylist(getlist)
    list_name, places = extract_places(data)
    print(f"Liste : {list_name!r} — {len(places)} lieu(x)")

    if not places:
        print("✗ Aucun lieu extrait.")
        return 1

    existing = load_existing_keys()
    new_rows, skipped = [], 0
    for p in places:
        k = (p["name"].lower(), round(p["lat"], 5), round(p["lon"], 5))
        if k in existing:
            skipped += 1
            continue
        country, region = ("", "")
        if not args.no_geocode:
            country, region = reverse_geocode(p["lat"], p["lon"])
            time.sleep(1.0)
        new_rows.append([p["name"], list_name, f"{p['lat']:.7f}", f"{p['lon']:.7f}", country, region])

    print(f"Nouveaux lieux : {len(new_rows)}   (déjà présents ignorés : {skipped})")

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
