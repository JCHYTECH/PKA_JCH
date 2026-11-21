# TRAVELS — Index projet

> Dernière mise à jour : 2026-11-21 — réorganisation structurelle (dossiers MAJUSCULES / fichiers minuscules).
> **Source de vérité opérationnelle : [thread-travels.md](thread-travels.md).**

## Description

Voyages pour observer le monde — réserves naturelles, villes pour l'art, destinations photo wildlife.
Inclut la logistique van **Lupo**, Westfalia Kelsey 2026 sur Ford Transit Custom, comme vecteur de voyage.

Responsable : [[Cigogne]] — Vanlife Travel Planner & Experience Curator.

## Convention de nommage

- **Dossiers : MAJUSCULES** (séparateur `-`).
- **Fichiers : minuscules** (séparateur `-` ou `_`).
- Exceptions (sous-systèmes techniques, casse d'origine préservée) : `LUPO-PLANNER/`, `PKA-DECOUVERTES/` et leurs sous-dossiers, `STICKERS/deco/`, `MEUBLE-BANQUETTE/archive/`.

## Point d'entrée

1. [thread-travels.md](thread-travels.md) — état courant, automatisations et prochaines actions.
2. [PKA-DECOUVERTES/MODE_EMPLOI.md](PKA-DECOUVERTES/MODE_EMPLOI.md) — mode d'emploi du pipeline DÉCOUVERTES.
3. [LUPO-PLANNER/README.md](LUPO-PLANNER/README.md) — application et carte de voyage.
4. [VANLIFE/preferences.md](VANLIFE/preferences.md) — préférences voyage et configuration du van.

## Structure

| Dossier ou fichier | Contenu |
|---|---|
| `LUPO/DOCS/` | Documents officiels du véhicule : CI, certificats conformité, immatriculation, assurance, autosecurité |
| `LUPO/TECHNIQUES/` | Équipement et aménagement du van (électricité, clim, sécurité, manuel, achats) |
| `LUPO/TECHNIQUES/AMENAGEMENT/` | Boîte vélo pliant, dimensions soute, mobilier |
| `LUPO/TECHNIQUES/MATERIEL-CANDIDAT/` | Équipements en cours d'évaluation |
| `LUPO/OLDIES/` | Historique d'achat du van |
| `LUPO/STICKERS/` | Déco et stickers |
| `VANLIFE/DESTINATIONS/` | Fiches destinations (`.md` canonique) |
| `VANLIFE/DESTINATIONS/EXPORTS/` | Exports HTML/PDF générés |
| `VANLIFE/LOGISTIQUE/` | Stationnement, camping-scout, routines |
| `VANLIFE/FEEDBACK/` | Retours d'expérience |
| `VANLIFE/TRIPS/` | Voyages réalisés (Wadden ; Italie à documenter) |
| `LUPO-PLANNER/` | Application de carte et planification de voyage |
| `lupo-planner-import.json` | Import généré pour Lupo Planner |
| `PKA-DECOUVERTES/` | Pipeline Telegram DÉCOUVERTES |
| `NOTEBOOKLM/` | Transcripts d'analyse NotebookLM (sources) |
| `99_REFERENCES/` | Références et sources de recherche (transcripts) |

## Fichiers clés

- Fiche technique Lupo : `LUPO/OLDIES/ACHAT-VAN/fiche-technique-lupo-kelsey.md`
- Préférences voyage : `VANLIFE/preferences.md`
- Guide camping-scout : `VANLIFE/LOGISTIQUE/camping_scout_README.md`
- Méthodologie stationnement : `VANLIFE/LOGISTIQUE/methodologie-stationnement.md`
- Cahier des charges DÉCOUVERTES : `PKA-DECOUVERTES/PKA_DECOUVERTES_Cahier_des_charges_V2.md`

## Archives et état courant

- `LUPO/OLDIES/` est la zone historique du van ; les documents d'aménagement actifs sont sous `LUPO/TECHNIQUES/`.
- Les états du pipeline (`queue/`, `drafts/`, `validated_places/`) se lisent dans le thread, pas dans les seuls noms de dossiers.

## Workflow

1. **Découvertes** : Telegram → `PKA-DECOUVERTES/raw/` → `queue/` → analyzer → `drafts/` → validation → `validated_places/`.
2. **Voyages** : recherche → `VANLIFE/DESTINATIONS/` → exports dans `VANLIFE/DESTINATIONS/EXPORTS/`.
3. **Logistique** : stationnement, camping-scout et routines → `VANLIFE/LOGISTIQUE/`.

## Voir aussi

- [[Cigogne]] — spécialiste vanlife PKA.
- [scripts/camping_scout.py](../../../scripts/camping_scout.py) — outil de recherche de campings.
