# TRAVELS — Index projet

> Dernière mise à jour : 2026-11-05 — navigation et arborescence réelle.
> **Source de vérité opérationnelle : [thread-travels.md](thread-travels.md).**

## Description

Voyages pour observer le monde — réserves naturelles, villes pour l'art, destinations photo wildlife.
Inclut la logistique van **Lupo**, Westfalia Kelsey 2026 sur Ford Transit Custom, comme vecteur de voyage.

Responsable : [[Cigogne]] — Vanlife Travel Planner & Experience Curator.

## Point d'entrée

1. [thread-travels.md](thread-travels.md) — état courant, automatisations et prochaines actions.
2. [pka-decouvertes/MODE_EMPLOI.md](pka-decouvertes/MODE_EMPLOI.md) — mode d'emploi du pipeline DÉCOUVERTES.
3. [lupo-planner/README.md](lupo-planner/README.md) — application et carte de voyage.
4. [vanlife/PREFERENCES.md](vanlife/PREFERENCES.md) — préférences voyage et configuration du van.

## Structure

| Dossier ou fichier | Contenu |
|---|---|
| [`Lupo/`](Lupo/) | Documents, technique et équipement du van |
| [`Lupo/van technique/`](<Lupo/van technique/>) | IOT, électricité, sécurité, dimensions et aménagements |
| [`Lupo/OLDIES/`](Lupo/OLDIES/) | Historique d'achat et anciens documents du van |
| [`Trips/`](Trips/) | Voyages réalisés, notamment Italie et Wadden |
| [`vanlife/`](vanlife/) | Lifestyle, destinations, logistique et préférences |
| [`vanlife/destinations/`](vanlife/destinations/) | Fiches destinations au format Markdown canonique |
| [`vanlife/destinations/exports/`](vanlife/destinations/exports/) | Exports HTML et PDF générés depuis les fiches |
| [`vanlife/logistique/`](vanlife/logistique/) | Stationnement, camping-scout et routines |
| [`vanlife/feedback/`](vanlife/feedback/) | Retours d'expérience et discussions |
| [`lupo-planner/`](lupo-planner/) | Application de carte et planification de voyage |
| [`lupo-planner-import.json`](lupo-planner-import.json) | Import généré pour Lupo Planner |
| [`pka-decouvertes/`](pka-decouvertes/) | Pipeline Telegram DÉCOUVERTES : collecte, analyse et fiches lieux |
| [`pka-decouvertes/raw/`](pka-decouvertes/raw/) | Données brutes collectées |
| [`pka-decouvertes/queue/`](pka-decouvertes/queue/) | Journal de travail du pipeline, à ne pas confondre avec une archive |
| [`pka-decouvertes/drafts/`](pka-decouvertes/drafts/) | Brouillons de fiches lieux |
| [`pka-decouvertes/validated_places/`](pka-decouvertes/validated_places/) | Fiches lieux validées |
| [`pka-decouvertes/logs/`](pka-decouvertes/logs/) | Journaux du collecteur |
| [`pka-decouvertes/reports/`](pka-decouvertes/reports/) | Rapports générés |
| [`pka-decouvertes/maps/`](pka-decouvertes/maps/) | Cartes HTML des lieux |
| [`99_INBOX_NOTES/`](99_INBOX_NOTES/) | Notes brutes à qualifier, non sources d'état courant |

## Fichiers clés

- [Fiche technique Lupo](Lupo/OLDIES/achat-van/fiche-technique-lupo-kelsey.md) — Westfalia Kelsey 2026, rangée avec l'historique d'achat.
- [Documents techniques Lupo](<Lupo/van technique/>) — documentation d'aménagement et d'équipement.
- [Risques et opportunités d'achat UE](Lupo/OLDIES/achat-van/Achat_véhicule_UE_risques_opportunités.md) — document historique.
- [Agenda des expositions vanlife](Lupo/OLDIES/achat-van/Expositions_Vanlife_2026.md) — document historique.
- [Préférences voyage](vanlife/PREFERENCES.md).
- [Guide camping-scout](vanlife/logistique/camping_scout_README.md).
- [Méthodologie stationnement](vanlife/logistique/methodologie-stationnement.md).
- [Cahier des charges DÉCOUVERTES](pka-decouvertes/PKA_DECOUVERTES_Cahier_des_charges_V2.md).

## Archives et état courant

- `Lupo/OLDIES/` est la zone historique du van ; les documents d'aménagement actifs sont sous `Lupo/van technique/`.
- `99_INBOX_NOTES/` contient des entrées non qualifiées.
- Les états de `pka-decouvertes/queue/`, `drafts/` et `validated_places/` se lisent dans le thread, pas dans les seuls noms de dossiers.

## Workflow

1. **Découvertes** : Telegram → `pka-decouvertes/raw/` → `pka-decouvertes/queue/` → analyzer → `pka-decouvertes/drafts/` → validation → `pka-decouvertes/validated_places/`.
2. **Voyages** : recherche → `vanlife/destinations/` → exports dans `vanlife/destinations/exports/`.
3. **Logistique** : stationnement, camping-scout et routines → `vanlife/logistique/`.

## Voir aussi

- [[Cigogne]] — spécialiste vanlife PKA.
- [scripts/camping_scout.py](../../../scripts/camping_scout.py) — outil de recherche de campings.
