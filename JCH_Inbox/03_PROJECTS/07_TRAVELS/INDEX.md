# TRAVELS — Index projet

Dernière mise à jour : 2026-06-06

## Description
Voyages pour observer le monde — réserves naturelles, villes pour l'art, destinations photo wildlife.
Inclut la logistique van (Stylevan Equinox IV Ford) comme vecteur de voyage.

Responsable : [[Cigogne]] 🦩 — Vanlife Travel Planner & Experience Curator

## Structure

| Dossier | Contenu |
|---|---|
| `achat-van/` | Achat du van Stylevan Equinox IV — checklist, prix, risques UE, expositions vanlife |
| `achat-van/docs/` | Brochures, catalogues, transcripts — PDF, PPT, sources externes |
| `vanlife/` | Lifestyle van, destinations, logistique, préférences |
| `vanlife/destinations/` | Fiches destinations — format `.md` canonique |
| `vanlife/destinations/exports/` | Exports `.html` / `.pdf` générés à partir des fiches destinations |
| `vanlife/logistique/` | Stationnement, camping-scout, routine, templates ARTEON |
| `vanlife/feedback/` | Retours d'expérience et discussions |
| `pka-decouvertes/` | Pipeline Telegram DÉCOUVERTES — collecte, analyse, fiches lieux |
| `pka-decouvertes/raw/` | Données brutes collectées (images, liens, textes, métadonnées) |
| `pka-decouvertes/queue/` | Éléments en attente d'analyse |
| `pka-decouvertes/drafts/` | Brouillons de fiches lieux générées par l'analyzer |
| `pka-decouvertes/validated_places/` | Fiches lieux validées (prêtes à publier) |
| `pka-decouvertes/logs/` | Logs du collecteur |
| `pka-decouvertes/reports/` | Rapports générés (cartes, analyses) |
| `pka-decouvertes/maps/` | Cartes HTML des lieux |

## Fichiers clés

- `achat-van/checklist-achat-stylevan-equinox-iv-ford.md` — Checklist achat van Stylevan
- `achat-van/Achat_véhicule_UE_risques_opportunités.md` — Risques et opportunités achat UE
- `achat-van/Prix_Stylevan_Equinox_4_2026.md` — Prix du modèle
- `achat-van/Expositions_Vanlife_2026.md` — Agenda expositions vanlife
- `vanlife/PREFERENCES.md` — Préférences voyage, configuration van
- `vanlife/logistique/camping_scout_README.md` — Guide camping-scout CLI
- `vanlife/logistique/methodologie-stationnement.md` — Méthodologie stationnement
- `pka-decouvertes/PKA_DECOUVERTES_Cahier_des_charges_V2.md` — Cahier des charges du pipeline

## Workflow

1. **Découvertes** → Bot Telegram collecte → `pka-decouvertes/raw/` → `queue/` → Analyzer → `drafts/` → validation → `validated_places/`
2. **Voyages** → Recherche destinations → `vanlife/destinations/` (fiche `.md`) → exports vers `exports/`
3. **Logistique** → Stationnement, camping-scout, routines → `vanlife/logistique/`

## Voir aussi

- [[Cigogne]] 🦩 — spécialiste vanlife PKA
- [[scripts/camping_scout.py]] — outil de recherche de campings
