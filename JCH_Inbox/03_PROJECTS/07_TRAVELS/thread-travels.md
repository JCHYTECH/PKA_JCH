# Thread — TRAVELS

> Living document — mis à jour par Dobby 🦉 en fin de session.
> **Dernière mise à jour** : 2026-10-22 — thread file créé (absent jusqu'ici)
> **Statut** : 🟢 actif — pipeline DÉCOUVERTES en fonctionnement continu

---

## Vue d'ensemble

Voyages et logistique van. Vecteur principal : **Lupo**, Westfalia Kelsey 2026
(Ford Transit Custom). Quatre axes : destinations, logistique vanlife,
pipeline **DÉCOUVERTES** (lieux captés via Telegram → fiches), et **Lupo Planner**
(carte de voyage importable).

Responsable : [[Cigogne]] 🦩 — Vanlife Travel Planner & Experience Curator

---

## État actuel

| Axe | Statut | Détail |
|-----|--------|--------|
| DÉCOUVERTES — collecteur | 🟢 | Process actif, interroge Telegram en continu (log du 22/10 16:47) |
| DÉCOUVERTES — fiches validées | 🟢 | **647 lieux** validés dans `validated_places/` |
| DÉCOUVERTES — file d'attente | 🟢 | **590 éléments** en `queue/`, dont **540 déjà analysés** (523 avec fiche validée). **Ce n'est pas un arriéré** : la queue est un journal historique. Reste réel : 36 `skipped` + 5 `rejected` + 9 `parked_routes` |
| Lupo Planner | 🟢 | `lupo-planner-import.json` (191 Ko) généré le 19/10 |
| Fiches destinations | 🟢 | `vanlife/destinations/` — format `.md` canonique |
| Logistique stationnement | 🟢 | `vanlife/logistique/` — camping-scout, méthodologie |
| Voyages réalisés | ✅ | Italie (21/08–19/09), Wadden (30/06) dans `Trips/` |
| Van — équipement | 🟡 | Meuble banquette en design (104×55×25) |

**Volumétrie** : 729 fichiers `.md`, 726 Mo — le projet le plus volumineux du
workspace PKA.

---

## Décisions clés

| Date | Décision | Contexte |
|------|----------|----------|
| 2026-10-19 | Lupo Planner synchronisé avec DÉCOUVERTES | Import JSON généré |
| 2026-10-04 | INDEX restructuré | 4 axes clarifiés |
| 2026-08-21 | Voyage Italie documenté | 21/08 → 19/09 |

---

## Prochaine étape

**Action prioritaire** : *corrigée le 22/10* — il n'y a **pas d'arriéré de 590
éléments**. Mesure réelle : 540/590 analysés, dont 523 avec fiche validée
présente. 17 noms de fichiers ont simplement évolué après validation.

**Reste à traiter** : 36 `skipped` (screenshots où l'OCR échoue — voir
`identify_skips.py`, passe vision forcée) + 9 `parked_routes` + 5 `rejected`.

**Action secondaire** : finaliser le meuble banquette (design en cours).

**Deadline** : —
**Responsable** : Cigogne 🦩 + Dobby 🦉

---

## Pipeline DÉCOUVERTES — fonctionnement

```
Telegram (groupe DÉCOUVERTES)
    ↓ collector.py  (process actif, en continu)
pka-decouvertes/raw/          6 éléments
    ↓
pka-decouvertes/queue/        590 éléments  ← GOULOT
    ↓ analyzer
pka-decouvertes/drafts/       0
    ↓ validation
pka-decouvertes/validated_places/   647 fiches
    ↓ decouvertes-to-planner.py
lupo-planner-import.json      191 Ko
```

**Le goulot est l'analyseur**, pas le collecteur. 590 éléments en attente
représentent plusieurs semaines de traitement au rythme actuel.

---

## Structure

| Dossier | Contenu |
|---------|---------|
| `Lupo/` | Fiche technique, documents, stickers, `van technique/` (IOT, électricité, sécurité) |
| `Lupo-planner/` | Application carte de voyage (import JSON) |
| `pka-decouvertes/` | Pipeline complet (collector, queue, validated_places, maps, reports) |
| `vanlife/` | Destinations, logistique, préférences |
| `Trips/` | Voyages réalisés (Italie, Wadden) |

---

## Historique sessions

| Date | Résumé session | Livrable |
|------|---------------|----------|
| 2026-10-22 | Thread file créé après re-vérification des projets | ce fichier |
| 2026-10-19 | Génération `lupo-planner-import.json` | 191 Ko |
| 2026-10-04 | INDEX restructuré | — |

---

## Liens

- INDEX : `03_PROJECTS/07_TRAVELS/INDEX.md`
- Pipeline : `pka-decouvertes/PKA_DECOUVERTES_Cahier_des_charges_V2.md`
- Planner : `03_PROJECTS/07_TRAVELS/Lupo-planner/`
- Spécialiste : [[Cigogne]] 🦩

---

*Fichier créé le 2026-10-22 — il manquait alors que TRAVELS est le projet le
plus volumineux du workspace. Maintenu par Dobby 🦉 via `pka-thread-file`.*
