# Camping Scout v2 — Guide d'utilisation

Script PKA pour trouver des spots nuit en van autour d'une destination.

**Fichier :** `scripts/camping_scout.py`

---

## Architecture

| Niveau | Sources | Dépendances | Résultats |
|--------|---------|-------------|-----------|
| 1 (toujours) | OSM / Overpass | `requests`, `geopy` | Campings, aires motorhome, fermes — données officielles |
| 2 (optionnel) | park4night, campspace, france-passion | + `playwright` | Données communautaires, chez l'habitant |

---

## Installation

### Niveau 1 seulement (rapide, sans navigateur)

```bash
pip install requests geopy
```

### Niveau 2 complet (inclut park4night)

```bash
pip install requests geopy playwright
playwright install chromium
```

---

## Usage

### Recherche rapide — OSM uniquement, sans navigateur

```bash
python3 scripts/camping_scout.py --location "Honfleur" --radius 15 --quick
```

### Recherche complète avec carte sauvegardée dans destinations/

```bash
python3 scripts/camping_scout.py --location "Honfleur" --radius 15 --save
```

### Avec France Passion (login adhérent requis)

```bash
python3 scripts/camping_scout.py --location "Honfleur" --radius 15 --fp-user email@x.com --fp-pass motdepasse
```

### Mode invisible (sans fenêtre navigateur)

```bash
python3 scripts/camping_scout.py --location "Honfleur" --radius 15 --headless
```

---

## Résultats

| Fichier | Description |
|---------|-------------|
| `camping_scout_[Lieu].html` | Carte interactive Leaflet + tableau trié par distance |
| `camping_scout_[Lieu].csv` | Données brutes exportables |

Avec `--save` → sauvegardé dans `destinations/` directement.

```bash
open JCH_Inbox/03_PROJECTS/07_TRAVELS/vanlife/destinations/camping_scout_[Lieu].html
```

---

## Score JCH

Chaque spot reçoit un score 0–10 calculé automatiquement :

| Critère | Points |
|---------|--------|
| Proximité réserve naturelle < 3 km | +4 |
| Proximité réserve naturelle 3–8 km | +2 |
| Type ferme ou France Passion | +1 |
| Distance > 15 km du centre | -1 |
| Distance > 20 km | -2 |

Score 8–10 = spot idéal pour photo aube/crépuscule.

---

## Sources couvertes

| Source | Type | Niveau |
|--------|------|--------|
| **OSM / Overpass** | Campings, aires CC, parkings motorhome | 1 |
| **park4night** | Spots communautaires (gold standard vanlife) | 2 |
| **Campspace** | Chez l'habitant, jardins privés | 2 |
| **France Passion** | Étapes gratuites chez producteurs/vignerons | 2 (login) |

Sources à ajouter (TODO) :
- Campercontact (aires officielles — API payante ou scraping)
- Bienvenue à la Ferme (Playwright)
- iOverlander (spots hors réseau)

---

## Notes

- OSM est la source la plus fiable (données ouvertes, pas de scraping)
- park4night est la référence communautaire — installer Playwright pour l'activer
- Les réserves naturelles trouvées par Overpass apparaissent sur la carte en vert (non-campables, pour repérage JCH)
- France Passion nécessite un compte adhérent actif
