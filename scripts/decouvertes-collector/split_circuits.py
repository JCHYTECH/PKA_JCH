#!/usr/bin/env python3
"""Split les fiches 'circuit/liste' en fiches individuelles (nom + GPS via Nominatim).

Usage: python3 split_circuits.py
  - Crée une fiche minimale (status: a_enrichir) par lieu dans drafts/
  - Dédup contre drafts/ + validated_places/
"""
import json
import re
import sys
import time
import unicodedata
from pathlib import Path

import requests

PKA_ROOT = Path(__file__).resolve().parents[2]
BASE = PKA_ROOT / "JCH_Inbox/03_PROJECTS/07_TRAVELS/pka-decouvertes"
DRAFTS = BASE / "drafts"
VALID = BASE / "validated_places"

PLACES = [
    ("Château d'Albrechtsburg", "Albrechtsburg Meißen Allemagne"),
    ("Château d'Eltz", "Burg Eltz Allemagne"),
    ("Château de Cochem", "Reichsburg Cochem Allemagne"),
    ("Château de Neuschwanstein", "Neuschwanstein Castle Hohenschwangau Allemagne"),
    ("Château de Linderhof", "Schloss Linderhof Allemagne"),
    ("Forteresse de Hohensalzburg", "Festung Hohensalzburg Salzburg Autriche"),
    ("Château de Heidelberg", "Heidelberg Castle Allemagne"),
    ("Château de Nymphenburg", "Schloss Nymphenburg München Allemagne"),
    ("Château de la Wartburg", "Wartburg Castle Eisenach Allemagne"),
    ("Burg Katzenstein", "Burg Katzenstein Dischingen Allemagne"),
    ("Burg Harburg", "Burg Harburg Donau-Ries Allemagne"),
    ("Schloss Hochstadt", "Schloss Hochstadt Allemagne"),
    ("Schloss Kapfenburg", "Schloss Kapfenburg Lauchheim Allemagne"),
    ("Schloss Baldern", "Schloss Baldern Allemagne"),
    ("Château de Montquintin", "Montquintin Belgique"),
    ("Château de Franchimont", "Château de Franchimont Theux Belgique"),
    ("Château de Walhain", "Château de Walhain Brabant wallon Belgique"),
    ("Château d'Écaussinnes", "Château d'Écaussinnes Hainaut Belgique"),
    ("Frías", "Frías Burgos Espagne"),
    ("Tobera", "Tobera Burgos Espagne"),
    ("Puentedey", "Puentedey Burgos Espagne"),
    ("Orbaneja del Castillo", "Orbaneja del Castillo Burgos Espagne"),
    ("Peñaranda de Duero", "Peñaranda de Duero Burgos Espagne"),
    ("Salto de Poveda", "Salto de Poveda Guadalajara Espagne"),
    ("Lagune de Taravilla", "Laguna de Taravilla Guadalajara Espagne"),
    ("Barranco de la Hoz", "Barranco de la Hoz Guadalajara Espagne"),
    ("Sigüenza", "Sigüenza Guadalajara Espagne"),
    ("Brihuega", "Brihuega Guadalajara Espagne"),
    ("Cifuentes", "Cifuentes Guadalajara Espagne"),
    ("Castillo de Torija", "Castillo de Torija Guadalajara Espagne"),
    ("Spello", "Spello Ombrie Italie"),
    ("Deruta", "Deruta Ombrie Italie"),
    ("Palena", "Palena Abruzzes Italie"),
    ("Pescocostanzo", "Pescocostanzo Abruzzes Italie"),
    ("Roccaraso", "Roccaraso Abruzzes Italie"),
    ("Area Faunistica dell'Orso Bruno", "Area Faunistica Orso Bruno Palena Italie"),
]


def slugify(name: str) -> str:
    s = unicodedata.normalize("NFKD", name or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^A-Za-z0-9._-]+", "-", s).strip("-")
    return s[:40] or "lieu"


def existing_slugs():
    slugs = set()
    for p in list((DRAFTS).glob("*.md")) + list(VALID.glob("*.md")):
        stem = re.sub(r"^\d{4}-\d{2}-\d{2}_", "", p.stem)
        slugs.add(stem)
    return slugs


def geocode(query: str):
    try:
        r = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": query, "format": "json", "limit": 1},
            headers={"User-Agent": "PKA_DECOUVERTES/1.0"},
            timeout=15,
        )
        data = r.json()
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"]), data[0].get("display_name", "")
    except Exception as e:
        print(f"  [geocode] {query}: {e}")
    return None


def main():
    known = existing_slugs()
    created = 0
    skipped = 0
    for nom, query in PLACES:
        slug = slugify(nom)
        if slug in known:
            print(f"  skip (déjà présent) : {nom}  [{slug}]")
            skipped += 1
            continue
        g = geocode(query)
        if not g:
            print(f"  ✗ GPS introuvable    : {nom}")
            continue
        lat, lon, disp = g
        pays = disp.split(",")[-1].strip() if disp else ""
        body = f"""---
type: lieu_a_visiter
status: a_enrichir
source: sites
source_group: SITES
date_capture: 2026-08-31
date_analyse: 2026-08-31
auteur: JCH
pays: {pays}
region: ""
ville: ""
nom_lieu: {nom}
gps: "{lat}, {lon}"
van_friendly: incertain
parking: incertain
interet_photo: 0
interet_nature: 0
interet_patrimoine: 0
interet_van: 0
priorite: 2
confidence: 0.5
tags:
  - decouvertes
  - lieu_a_visiter
  - a_enrichir
---

# {nom}

## Résumé

Lieu extrait d'une liste/itinéraire (capture SITES). Fiche minimale — à enrichir (description, scores, accès van).

## Localisation
- GPS : `{lat}, {lon}`
- [Ouvrir dans Google Maps](https://www.google.com/maps/search/{lat},{lon})
- Pays : {pays}
"""
        (DRAFTS / f"2026-08-31_{slug}.md").write_text(body, encoding="utf-8")
        print(f"  ✓ {nom}  [{slug}]  ({lat:.4f},{lon:.4f}) {pays}")
        created += 1
        known.add(slug)
        time.sleep(1.1)  # politesse Nominatim (≤1 req/s)

    print(f"\n{created} créées, {skipped} déjà présentes, {len(PLACES) - created - skipped} échecs GPS")


if __name__ == "__main__":
    main()
