#!/usr/bin/env python3
"""Génère une fiche Obsidian « vanlife » pour chaque lieu de la catégorie Réserves naturelles.

Lit les lieux depuis pka-decouvertes/Réserves naturelles/*.csv (nom + GPS exact + pays/région),
interroge Claude (Anthropic) pour la section vanlife/parking, et écrit une fiche .md par lieu
dans Réserves naturelles/fiches/. Ne touche pas à lieux_google_maps.csv.

Usage :
  python3 generate_van_fiches.py                     # toutes les fiches (modèle haiku)
  python3 generate_van_fiches.py --model sonnet      # meilleure qualité
  python3 generate_van_fiches.py --limit 5           # test sur 5 lieux
  python3 generate_van_fiches.py --dry-run           # aperçu des lieux sans appel LLM
"""
import argparse
import csv
import json
import os
import sys
import time
import unicodedata
from pathlib import Path

from dotenv import load_dotenv

PKA_ROOT = Path(os.getenv("PKA_ROOT", Path(__file__).resolve().parents[2]))
BASE = PKA_ROOT / "JCH_Inbox/03_PROJECTS/07_TRAVELS/pka-decouvertes"
CAT = BASE / "Réserves naturelles"
FICHES = CAT / "fiches"

CLAUDE_MODELS = {
    "haiku": "claude-haiku-4-5-20251001",
    "sonnet": "claude-sonnet-4-6",
    "opus": "claude-opus-4-8",
}

VAN_PROMPT = """Tu es un expert en voyage en minivan (hauteur 2m, longueur 5m, Stylevan Equinox IV Ford).

Lieu : {nom}, {region}, {pays}

Rédige une section pratique pour un voyageur en minivan. Sois TRÈS concret — donne des noms, distances en km, tarifs en € si connus.

1. **Accès** : type de route (D, N, A), état, praticabilité pour 2m de haut
2. **Parking** : nom du parking le plus proche, hauteur max en mètres, gratuit/payant (tarif)
3. **Nuit sur place** : camping-car autorisé ? aire officielle la plus proche (nom + distance km) ? stationnement nocturne toléré ?
4. **Services** : borne eau/électricité/vidange la plus proche (nom + km), supermarché (nom + km)
5. **Astuce vanlife** : meilleure saison, durée visite, heure idéale pour photos, spot secret si connu

Si tu ne connais pas un détail précis, ne l'invente pas — écris "à vérifier sur place".
"""


def slugify(name: str) -> str:
    s = unicodedata.normalize("NFKD", name or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = "".join(c if c.isalnum() or c in " -_" else "" for c in s)
    s = s.replace(" ", "-").strip("-")
    s = s[:60] or "lieu"
    return s


def load_places() -> list[dict]:
    places = []
    skipped_placeholders = 0
    for fp in sorted(CAT.glob("*.csv")):
        with open(fp, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                name = (r.get("Name") or "").strip()
                if not name:
                    continue
                # Les repères anonymes / lieux à vérifier n'ont pas de nom réel :
                # pas de fiche vanlife (le modèle ne peut rien en dire).
                if name.startswith(("Épinglé", "À vérifier")):
                    skipped_placeholders += 1
                    continue
                places.append({
                    "name": name,
                    "lat": r["Latitude"].strip(),
                    "lon": r["Longitude"].strip(),
                    "country": r.get("Country", "").strip(),
                    "region": r.get("Region", "").strip(),
                })
    if skipped_placeholders:
        print(f"  (ignorés : {skipped_placeholders} repères anonymes / à vérifier)")
    return places


def call_claude(model_id: str, prompt: str) -> str:
    import anthropic
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    resp = client.messages.create(
        model=model_id,
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text


def build_fiche(p: dict, van_info: str) -> str:
    gps = f"{p['lat']}, {p['lon']}"
    gmaps = f"https://www.google.com/maps/search/{p['lat']},{p['lon']}"
    yaml = f"""---
type: lieu_a_visiter
status: a_enrichir
source: google_maps
pays: {p['country']}
region: {p['region']}
nom_lieu: {p['name']}
gps: "{gps}"
categorie: reserves_naturelles
tags:
  - decouvertes
  - reserve_naturelle
  - vanlife
---"""
    return f"""{yaml}

# {p['name']}

## Vanlife & parking

{van_info}

## Localisation

- GPS : `{gps}`
- [Ouvrir dans Google Maps]({gmaps})
- Pays : {p['country']} | Région : {p['region']}
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default="haiku", choices=list(CLAUDE_MODELS))
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    _env = PKA_ROOT / "JCH_PRIVATE" / "decouvertes.env"
    if _env.exists():
        load_dotenv(_env)
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("✗ ANTHROPIC_API_KEY introuvable (JCH_PRIVATE/decouvertes.env).")
        return 1

    places = load_places()
    print(f"Lieux dans Réserves naturelles/ : {len(places)}")
    if args.limit:
        places = places[: args.limit]
        print(f"Limite : {args.limit}")

    if args.dry_run:
        for p in places:
            print(f"  - {p['name']}  ({p['lat']}, {p['lon']})  {p['country']} / {p['region']}")
        return 0

    FICHES.mkdir(parents=True, exist_ok=True)
    model_id = CLAUDE_MODELS[args.model]
    ok, skip, fail = 0, 0, 0
    for i, p in enumerate(places, 1):
        out = FICHES / f"{slugify(p['name'])}.md"
        if out.exists():
            print(f"[{i}/{len(places)}] ⏭ {p['name']} (fiche existante)")
            skip += 1
            continue
        prompt = VAN_PROMPT.format(nom=p["name"], region=p["region"] or "région inconnue", pays=p["country"] or "pays inconnu")
        try:
            print(f"[{i}/{len(places)}] ✍ {p['name']} ...", flush=True)
            van_info = call_claude(model_id, prompt)
            out.write_text(build_fiche(p, van_info), encoding="utf-8")
            ok += 1
        except Exception as e:
            print(f"   ✗ erreur : {e}")
            fail += 1
        time.sleep(0.5)

    print(f"\n✓ {ok} fiche(s) générée(s), {skip} déjà présentes, {fail} échec(s) → {FICHES.relative_to(PKA_ROOT)}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
