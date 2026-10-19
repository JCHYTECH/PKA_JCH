# TRAVELS — Index projet

Dernière mise à jour : 2026-10-04

## Description
Voyages pour observer le monde — réserves naturelles, villes pour l'art, destinations photo wildlife.
Inclut la logistique van (Westfalia Kelsey 2026, porteur Ford Transit Custom) comme vecteur de voyage.

Responsable : [[Cigogne]] 🦩 — Vanlife Travel Planner & Experience Curator

## Structure

| Dossier | Contenu |
|---|---|
| `Lupo Itself/` | Fiche technique, documents et archives du van Westfalia Kelsey 2026 |
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

- `Lupo Itself/OLDIES/achat-van/fiche-technique-lupo-kelsey.md` — Fiche technique Westfalia Kelsey 2026
- `achat-van/Achat_véhicule_UE_risques_opportunités.md` — Risques et opportunités achat UE
- `Lupo Itself/OLDIES/achat-van/` — Prix, checklist et archives d'achat (historique)
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
