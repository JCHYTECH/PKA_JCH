#!/usr/bin/env python3
"""
spots_ville.py — Procédure « fiches spot » pour se garer en van dans une ville.

Pour une ville donnée (test : Ravenne) :
  1. Géolocalise le centre (Nominatim).
  2. Interroge park4night (types parking + aire CC) dans un rayon.
  3. Classe chaque spot par rapport à la ZTL (zone à trafic limité, Italie).
  4. Génère une fiche « spot_van » par spot.

Usage :
  python3 spots_ville.py "Ravenna" --radius 5 --top 20

Sortie : JCH_Inbox/03_PROJECTS/07_TRAVELS/pka-decouvertes/spots_van/<date>_<ville>_<slug>.md
"""
import argparse
import re
import sys
import time
from pathlib import Path

import requests

PKA_ROOT = Path(__file__).resolve().parents[2]
SPOTS_DIR = PKA_ROOT / "JCH_Inbox" / "03_PROJECTS" / "07_TRAVELS" / "pka-decouvertes" / "spots_van"

# Importer le module park4night voisin
sys.path.insert(0, str(Path(__file__).resolve().parent))
import park4night as p4n  # noqa: E402

UA = {"User-Agent": "PKA_DECOUVERTES/1.0 (jean-claude; local tool)"}

# Types « parking ou aire stationnement CC » (on exclut camping/ferme/nature/off-road)
CITY_TYPES = ["ACC_G", "ACC_P", "ACC_PR", "PSS", "P", "AR"]
# Types qui sont des aires CC dédiées (hors ZTL par nature)
AIRE_TYPES = {"ACC_G", "ACC_P", "ACC_PR", "PSS"}

# ── Base de connaissances ZTL (à compléter ville par ville) ────────────────────
# ztl=True → centre historique en zone à trafic limité. centre_km = rayon approximatif du centre.
ZTL_DB = {
    "ravenna": {
        "ztl": True,
        "note": "Centre historique en ZTL (accès limité, caméras) — stationner sur les parkings relais en périphérie.",
        "centre_km": 1.2,
    },
}


def geocode(city: str) -> dict | None:
    try:
        r = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": city, "format": "json", "limit": 8},
            headers=UA, timeout=15,
        )
        d = r.json()
        if not d:
            return None
        # Écarter le centroid de la commune entière (pas de code postal + surface
        # énorme) puis garder le résultat le plus « important » → le nœud de la
        # ville réelle, pas un homonyme mineur (Ravenna, Kentucky…).
        def score(item):
            has_zip = bool(re.search(r"\b\d{4,5}\b", item.get("display_name", "")))
            b = item.get("boundingbox")
            area = 0.0
            if b and len(b) == 4:
                try:
                    area = (float(b[1]) - float(b[0])) * (float(b[3]) - float(b[2]))
                except Exception:
                    area = 0.0
            if not has_zip and area > 0.2:
                return -1.0
            return float(item.get("importance", 0) or 0)
        best = max(d, key=score)
        return {"lat": float(best["lat"]), "lon": float(best["lon"]),
                "display": best["display_name"]}
    except Exception as e:
        print(f"[geocode] erreur: {e}")
    return None


def ztl_info(city: str) -> dict:
    key = re.sub(r"[^a-z]", "", city.lower())
    if key in ZTL_DB:
        return ZTL_DB[key]
    return {"ztl": None, "note": "ZTL à vérifier (non référencée)", "centre_km": 0.0}


def ztl_status(ztl: dict, type_code: str, dist_km: float) -> str:
    """Classe un spot vis-à-vis de la ZTL."""
    if type_code in AIRE_TYPES:
        return "hors ZTL (aire CC dédiée)"
    if ztl.get("ztl") is True and dist_km <= ztl.get("centre_km", 0.0):
        return "⚠️ centre / ZTL — vérifier l'accès"
    if ztl.get("ztl") is True:
        return "hors ZTL (périphérie)"
    return "ZTL à vérifier"


def slugify(s: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-")
    return s[:60] or "spot"


def confidence(review: int) -> float:
    if review >= 100:
        return 0.90
    if review >= 10:
        return 0.80
    if review >= 1:
        return 0.75
    return 0.70


def build_fiche(spot: dict, city_label: str, country: str, ztl: dict) -> str:
    name = spot["name"]
    type_label = spot["type_label"]
    gps = f"{spot['lat']}, {spot['lng']}"
    svc = "\n".join(f"  - {s}" for s in spot["services_label"]) or "  - —"
    z = spot["ztl_status"]
    van = "oui" if spot["type_code"] in AIRE_TYPES else "incertain"
    conf = spot["confidence"]
    date = time.strftime("%Y-%m-%d")
    return f"""---
type: spot_van
status: validated
source: park4night
ville: {city_label}
pays: {country}
nom_spot: {name}
gps: "{gps}"
type_aire: {type_label}
note: {spot['rating'] if spot['rating'] is not None else '—'}
avis: {spot['review']}
distance_centre_km: {spot['distance']}
ztl: {z}
van_friendly: {van}
confidence: {conf}
url_p4n: {spot['url']}
tags:
  - spot_van
  - {slugify(type_label)}
  - {slugify(city_label)}
---

# {name}

## Infos spot

- **Type** : {type_label}
- **Note** : {spot['rating'] if spot['rating'] is not None else '—'}/5 ({spot['review']} avis)
- **GPS** : `{gps}`
- **Distance centre ({city_label})** : {spot['distance']} km

## Services

{svc}

## ZTL

{z}
> {ztl['note']}

## Accès minivan (2 m hauteur · 5 m longueur)

{'Aire dédiée camping-cars — accès prévu, hauteur 2 m OK.' if spot['type_code'] in AIRE_TYPES else 'Parking — hauteur et accès à vérifier sur place.'}

## Localisation

- GPS : `{gps}`
- [Ouvrir dans Google Maps](https://maps.google.com/?q={spot['lat']},{spot['lng']})
- [Fiche park4night]({spot['url']})

## Source

- park4night (API places/around) — {date}
"""


def main() -> None:
    ap = argparse.ArgumentParser(description="Générer des fiches spot_van pour une ville")
    ap.add_argument("city", help="Nom de la ville (ex: Ravenna)")
    ap.add_argument("--radius", type=int, default=5, help="rayon en km (défaut 5)")
    ap.add_argument("--top", type=int, default=20, help="nb max de spots (défaut 20)")
    ap.add_argument("--min-rating", type=float, default=0.0)
    args = ap.parse_args()

    g = geocode(args.city)
    if not g:
        print(f"Ville introuvable : {args.city}")
        return
    print(f"Centre {args.city} : {g['lat']}, {g['lon']} ({g['display']})")

    ztl = ztl_info(args.city)
    print(f"ZTL : {ztl['note']}")

    places = p4n.around(g["lat"], g["lon"], radius=args.radius, lang="fr",
                        types=CITY_TYPES, use_cache=False)
    print(f"park4night : {len(places)} spots (types parking + aire CC) dans {args.radius} km")

    country = "Italie"  # la procédure est calibrée Italie ; à dériver du geocode à terme
    city_label = args.city

    SPOTS_DIR.mkdir(parents=True, exist_ok=True)
    date = time.strftime("%Y-%m-%d")
    n = 0
    spots_out = []
    for p in places:
        t = p.get("type") or {}
        code = t.get("code", "?")
        addr = p.get("address") or {}
        name = (p.get("name") or "").strip() or (addr.get("street") or "").strip() or t.get("label", "?")
        dist = round(float(p.get("distance", 0)), 2)
        rating = p.get("rating")
        review = p.get("review", 0) or 0
        spot = {
            "name": name,
            "type_code": code,
            "type_label": p4n.TYPES_FR.get(code, t.get("label", "?")),
            "lat": p.get("lat"),
            "lng": p.get("lng"),
            "distance": dist,
            "rating": rating,
            "review": review,
            "services_label": [p4n.SERVICES_FR.get(s, s) for s in (p.get("services") or [])],
            "url": f"{p4n.BASE}/fr/place/{p.get('id')}",
            "confidence": confidence(review),
            "ztl_status": ztl_status(ztl, code, dist),
        }
        spots_out.append(spot)

    spots_out.sort(key=lambda s: s["distance"])
    spots_out = spots_out[: args.top]

    for s in spots_out:
        fiche = build_fiche(s, city_label, country, ztl)
        path = SPOTS_DIR / f"{date}_{slugify(city_label)}_{slugify(s['name'])}.md"
        path.write_text(fiche, encoding="utf-8")
        n += 1
        print(f"  → {path.name}  ({s['distance']} km · {s['type_label']} · {s['ztl_status']})")

    print(f"\n{n} fiche(s) spot générée(s) dans {SPOTS_DIR.relative_to(PKA_ROOT)}")


if __name__ == "__main__":
    main()
