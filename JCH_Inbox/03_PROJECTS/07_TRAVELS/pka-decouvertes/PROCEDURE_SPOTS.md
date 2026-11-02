# Procédure — fiches « spot_van » pour se garer dans une ville

Génère des fiches de stationnement/nuit (parkings + aires CC) pour une ville,
avec prise en compte des ZTL (zones à trafic limité, Italie).

## 1. Lancer

```bash
cd ~/PKA_JCH/scripts/decouvertes-collector
python3 spots_ville.py "Ravenna" --radius 5 --top 20
```

Sortie : `JCH_Inbox/03_PROJECTS/07_TRAVELS/pka-decouvertes/spots_van/<date>_<ville>_<slug>.md`

## 2. Ce que fait le script

1. **Géolocalise le centre** de la ville (Nominatim) — en écartant le centroid de
   la commune (surface énorme) pour garder le nœud de la ville réelle (importance).
2. **Interroge park4night** (`/api/places/around`) filtré sur les types
   `ACC_G, ACC_P, ACC_PR, PSS, P, AR` (parking + aire stationnement CC).
3. **Classe chaque spot vis-à-vis de la ZTL** :
   - aires CC dédiées (`ACC_*`, `PSS`) → `hors ZTL (aire CC dédiée)`
   - parking (`P`, `AR`) dans le rayon du centre → `⚠️ centre / ZTL — vérifier l'accès`
   - parking au-delà → `hors ZTL (périphérie)`
4. **Écrit une fiche** `type: spot_van` (GPS, type, note, avis, services, distance centre, statut ZTL, lien park4night).

## 3. Base de connaissances ZTL

Les zones ZTL ne sont **pas cartographiées** dans OpenStreetMap (vérifié : 0 élément
`boundary=restriction` autour de Ravenne). On maintient donc une mini-base à la main
dans `spots_ville.py` :

```python
ZTL_DB = {
    "ravenna": {"ztl": True, "note": "…", "centre_km": 1.2},
    # "firenze": {"ztl": True, "note": "…", "centre_km": 1.5},
}
```

- `ztl=True` : centre historique en zone à trafic limité.
- `centre_km` : rayon approximatif du centre (seuil de classification des parkings).
- Ville absente → `ZTL à vérifier` dans les fiches.

À compléter au fil des villes visitées (Florence, Sienne, Bologne, Vérone…).

## 4. Limites connues

- Le geocode vise le centre-ville, pas la zone piétonne exacte (seuil `centre_km` approché).
- La classification ZTL est **heuristique** : toujours recouper sur place (panneaux, horaires, caméras).
- Le nom des spots park4night est parfois vide → on retombe sur l'adresse (rue).

## 5. Évolutions possibles

- Intégrer les fiches spot dans la page DÉCOUVERTES (section « étapes nuit »).
- Enrichir la base ZTL avec les horaires d'accès par ville.
- Croiser avec un second géocodeur si une ville renvoie un mauvais centre.
