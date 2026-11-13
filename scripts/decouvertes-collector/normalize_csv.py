#!/usr/bin/env python3
"""Normalise lieux_google_maps.csv vers un schéma unique 6 colonnes
(Name,Description,Latitude,Longitude,Country,Region) et déduplique.

Gère les deux formats historiques :
  - 6 col : Name,Description,Lat,Long,Country,Region        (déjà conforme)
  - 9 col : Name,Lat,Long,Country,Region,Type,Conf,Date,Notes  (écrit par analyzer.py)
Déduplication par (nom normalisé, lat arrondie à 5, lon arrondie à 5), garde la 1re occurrence.

À lancer APRÈS la fin de l'analyzer (pas pendant, sinon race d'écriture).
"""
import csv
import os

BASE = "/Users/jchavauxm5/PKA_JCH/JCH_Inbox/03_PROJECTS/07_TRAVELS/pka-decouvertes"
CSV = os.path.join(BASE, "lieux_google_maps.csv")
HDR = ["Name", "Description", "Latitude", "Longitude", "Country", "Region"]


def normalize(row):
    n = len(row)
    if n == 0:
        return None
    if row[0].strip().lower() == "name":
        return None  # ligne(s) d'en-tête
    if n >= 9:
        name, lat, lon, country, region, typ = row[0], row[1], row[2], row[3], row[4], row[5]
        desc = " · ".join(x for x in (country, region, typ) if x and x.strip())
        return (name, desc, lat, lon, country, region)
    if n == 6:
        return tuple(row[:6])
    # format inconnu : essayer de préserver au mieux
    return tuple(row[:6]) if n >= 6 else None


def key(row):
    name = row[0].strip().lower()
    try:
        lat = round(float(row[2]), 5)
        lon = round(float(row[3]), 5)
    except Exception:
        lat, lon = row[2], row[3]
    return (name, lat, lon)


def main():
    rows = []
    with open(CSV, newline="", encoding="utf-8") as f:
        for r in csv.reader(f):
            n = normalize(r)
            if n:
                rows.append(n)

    seen = set()
    out = []
    for n in rows:
        k = key(n)
        if k in seen:
            continue
        seen.add(k)
        out.append(n)

    with open(CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(HDR)
        w.writerows(out)

    print(f"normalise: {len(out)} lignes | doublons supprimes: {len(rows) - len(out)}")


if __name__ == "__main__":
    main()
