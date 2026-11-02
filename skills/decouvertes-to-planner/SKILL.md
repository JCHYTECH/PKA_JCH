---
name: decouvertes-to-planner
description: Convertir les fiches DÉCOUVERTES (spots_van/, validated_places/) en JSON importable par Lupo Planner. Déclencher sur "mets les découvertes dans le planner", "export planner", "sync découvertes planner".
---

# Skill — decouvertes-to-planner

Pont DÉCOUVERTES → Lupo Planner. Convertit les fiches de `pka-decouvertes` en
JSON importable par le Lupo Planner (bouton « Importer JSON »).

## Déclencheur
- « mets les découvertes dans le planner », « export planner »
- Après génération de nouvelles fiches via le skill `pka-decouvertes`

## Sources
- `spots_van/*.md`          → spots de bivouac (aire/camping/privé/sauvage)
- `validated_places/*.md`   → points d'intérêt à visiter (poi)
- Les fiches sans coordonnées exploitables (`gps: "à compléter"`) sont ignorées.

## Procédure
1. `python3 scripts/decouvertes-to-planner.py --dry-run` — stats sans écrire
2. `python3 scripts/decouvertes-to-planner.py` — génère `lupo-planner-import.json`
3. Importer le JSON dans Lupo Planner (bouton « Importer JSON »)

## Voir aussi
- [[pka-decouvertes]] — génération des fiches source
- `JCH_Inbox/03_PROJECTS/07_TRAVELS/Lupo-planner/`
