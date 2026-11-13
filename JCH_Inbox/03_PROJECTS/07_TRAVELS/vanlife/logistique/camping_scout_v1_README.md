# Camping-Car Scout 🏕️

Outil de recherche multi-sites pour trouver des emplacements camping-car dans un rayon donné.

## Sites couverts
- **park4night** — aires, campings, spots libres
- **campspace.com** (ex-HomeCamper) — chez l'habitant, jardins privés
- **bienvenue-a-la-ferme.com** — aires à la ferme
- **france-passion.com** — étapes chez producteurs/vignerons (login requis)
- **nomady.camp** — chez l'habitant (principalement DACH, France limitée)

## Installation (une seule fois)

Ouvre le Terminal et exécute ces commandes une par une :

```bash
pip install playwright --break-system-packages
pip install geopy --break-system-packages
playwright install chromium
```

## Utilisation

### Recherche simple (sans France Passion)
```bash
python3 camping_scout.py --location "Le Crotoy" --radius 15
```

### Avec France Passion (login requis)
```bash
python3 camping_scout.py --location "Le Crotoy" --radius 15 --fp-user tonmail@example.com --fp-pass tonmotdepasse
```

### Mode invisible (sans fenêtre de navigateur)
```bash
python3 camping_scout.py --location "Le Crotoy" --radius 15 --headless
```

### Changer le répertoire de sortie
```bash
python3 camping_scout.py --location "Bayonne" --radius 20 --output-dir ~/Desktop/camping
```

## Résultats

Le script génère deux fichiers dans le répertoire courant :

- **camping_results.csv** — tableau de tous les résultats
- **camping_map.html** — carte interactive + tableau, à ouvrir dans Safari/Chrome

Pour ouvrir la carte directement :
```bash
open camping_map.html
```

## Notes

- Le script ouvre un navigateur visible par défaut (mode headless désactivé)
  Pour le voir travailler, c'est normal qu'il ouvre et ferme des pages rapidement.
- France Passion nécessite un compte adhérent actif (guide annuel acheté).
- Nomady couvre peu la France — utile si tu voyages vers l'Allemagne ou la Suisse.
- Park4night et campspace nécessitent Playwright car leur contenu est dynamique (JavaScript).

## Dépannage

**"playwright not found"** → Relancer `pip install playwright --break-system-packages`

**"chromium not found"** → Relancer `playwright install chromium`

**0 résultats sur un site** → Le site a peut-être changé sa structure HTML.
Ouvrir l'URL correspondante manuellement dans le navigateur pour vérifier.

**Login France Passion échoue** → Vérifier identifiants sur france-passion.com directement.
