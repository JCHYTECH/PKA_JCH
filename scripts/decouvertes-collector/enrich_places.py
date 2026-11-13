#!/usr/bin/env python3
"""Enrichit les fiches 'a_enrichir' (nom+GPS) en fiches complètes via LLM + Overpass.

Réutilise les fonctions de analyzer.py (call_model, VAN_PROMPT, Overpass, générateurs).
Usage : python3 enrich_places.py [--limit N]
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analyzer as A

ENRICH = """Tu es l'agent PKA_DECOUVERTES. Enrichis cette fiche de lieu à visiter.

Lieu : {nom}
GPS : {lat}, {lon}

Le nom du lieu est correct, garde-le tel quel. Complète les autres champs.

Retourne UNIQUEMENT un JSON valide (sans texte autour) :
{{
  "pays": "pays",
  "region": "région",
  "ville": "ville ou commune",
  "type_lieu": "nature | monument | village | plage | montagne | foret | lac | autre",
  "description": "2-3 phrases sur l'intérêt du lieu",
  "interet_photo": 0,
  "interet_nature": 0,
  "interet_patrimoine": 0,
  "confidence": 0.9,
  "action": "validated"
}}

Scores de 0 à 5. Si tu n'es pas sûr d'un détail, choisis la valeur la plus probable.
"""

MODEL = "haiku"
BASE = A.BASE
VALID = BASE / "validated_places"
DATA = BASE / "data"


def main():
    limit = None
    if "--limit" in sys.argv:
        limit = int(sys.argv[sys.argv.index("--limit") + 1])

    targets = []
    for p in sorted(VALID.glob("*.md")):
        txt = p.read_text(encoding="utf-8")
        if "status: a_enrichir" not in txt:
            continue
        nom = re.search(r"^nom_lieu:\s*(.+)$", txt, re.M).group(1).strip()
        gps = re.search(r'^gps:\s*"([\d.,\-\s]+)"', txt, re.M)
        if not gps:
            continue
        parts = [x.strip() for x in gps.group(1).split(",")]
        lat, lon = float(parts[0]), float(parts[1])
        targets.append((p, nom, lat, lon))

    if limit:
        targets = targets[:limit]

    print(f"{len(targets)} fiches à enrichir")
    ok = 0
    for p, nom, lat, lon in targets:
        print(f"\n[{nom}] ({lat:.4f},{lon:.4f})", flush=True)
        try:
            raw = A.call_model(MODEL, ENRICH.format(nom=nom, lat=lat, lon=lon))
            analysis = A._extract_json(raw)
        except Exception as e:
            print(f"  enrich LLM erreur: {e}")
            continue
        if not analysis:
            print("  enrich LLM: pas de JSON")
            continue
        analysis["nom_lieu"] = nom  # garde le nom curaté

        try:
            van_info = A.call_model(MODEL, A.VAN_PROMPT.format(
                nom_lieu=nom,
                region=analysis.get("region", ""),
                pays=analysis.get("pays", ""),
                type_lieu=analysis.get("type_lieu", ""),
                description=analysis.get("description", ""),
            ))
        except Exception as e:
            van_info = f"_Erreur van : {e}_"

        gps = {"lat": lat, "lon": lon}
        # Overpass hors service (2026-08-31 : No route to host / 502) — réserves/attractions/restos à compléter plus tard
        reserves = []
        attractions = []
        restaurants = []

        meta = {"media_files": [], "datetime": "2026-08-31T07:27:00+00:00", "author": "JCH", "text": ""}
        slug = A.slugify(nom)
        today = "2026-08-31"
        A.generate_place_json(lat, lon, analysis, van_info, meta, reserves, restaurants, attractions, DATA, slug, today)
        note = A.generate_note(meta, analysis, van_info, gps, reserves, restaurants, slug)
        (VALID / f"{today}_{slug}.md").write_text(note, encoding="utf-8")
        print(f"  ✓ {slug} — {analysis.get('type_lieu')} (photo {analysis.get('interet_photo')}/nat {analysis.get('interet_nature')}/pat {analysis.get('interet_patrimoine')})")
        ok += 1

    print(f"\n{ok}/{len(targets)} enrichies")


if __name__ == "__main__":
    main()
