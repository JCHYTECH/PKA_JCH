#!/usr/bin/env python3
"""Backfill Overpass (réserves/attractions/restos) pour les fiches qui n'en ont pas.

À lancer quand Overpass est de nouveau en ligne.
Usage : python3 backfill_overpass.py [--limit N]
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analyzer as A

BASE = A.BASE
DATA = BASE / "data"
VALID = BASE / "validated_places"


def main():
    limit = None
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])

    targets = []
    for p in sorted(DATA.glob("*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        if not d.get("reserves") and not d.get("attractions") and not d.get("restaurants"):
            targets.append(p)

    if limit:
        targets = targets[:limit]

    print(f"{len(targets)} JSON à backfiller")
    ok = 0
    for p in targets:
        d = json.loads(p.read_text(encoding="utf-8"))
        slug = d.get("slug", p.stem)
        nom = d.get("nom_lieu", "?")
        gps = d.get("gps", {}) or {}
        lat, lon = gps.get("lat"), gps.get("lon")
        if lat is None or lon is None:
            print(f"  skip (pas de GPS): {nom}")
            continue

        print(f"\n[{nom}] ({lat:.4f},{lon:.4f})", flush=True)
        reserves = A.get_nature_reserves(lat, lon, 25)
        attractions = A.get_nearby_attractions(lat, lon, 30)
        restaurants = A.get_restaurants(lat, lon, 15)

        d["reserves"] = reserves
        d["attractions"] = attractions
        d["restaurants"] = restaurants
        p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")

        sc = d.get("scores", {}) or {}
        analysis = {
            "nom_lieu": nom, "pays": d.get("pays", ""), "region": d.get("region", ""),
            "ville": d.get("ville", ""), "type_lieu": d.get("type_lieu", ""),
            "description": d.get("description", ""),
            "interet_photo": sc.get("photo", 0), "interet_nature": sc.get("nature", 0),
            "interet_patrimoine": sc.get("patrimoine", 0), "interet_van": sc.get("van", 0),
            "confidence": d.get("confidence", 0), "action": d.get("action", "validated"),
        }
        meta = {"media_files": [], "datetime": d.get("source", {}).get("datetime", "2026-08-31"), "author": "JCH", "text": ""}
        note = A.generate_note(meta, analysis, d.get("van_info", ""), {"lat": lat, "lon": lon}, reserves, restaurants, slug)
        today = d.get("date_analyse", "2026-08-31")
        (VALID / f"{today}_{slug}.md").write_text(note, encoding="utf-8")
        print(f"  ✓ {slug} — réserves {len(reserves)} / attractions {len(attractions)} / restos {len(restaurants)}")
        ok += 1

    print(f"\n{ok}/{len(targets)} backfillées")


if __name__ == "__main__":
    main()
