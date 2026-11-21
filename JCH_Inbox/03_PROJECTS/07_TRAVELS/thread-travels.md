# Thread — TRAVELS

> Living document — mis à jour par Dobby 🦉 en fin de session.
> **Dernière mise à jour** : 2026-11-12 — fiche alimentation SELPHY CP1300 (12V van) déposée dans `LUPO/TECHNIQUES/ELECTRICITE/`
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
| Fiches destinations | 🟢 | `VANLIFE/destinations/` — format `.md` canonique |
| Logistique stationnement | 🟢 | `VANLIFE/logistique/` — camping-scout, méthodologie |
| Voyages réalisés | ✅ | Italie (21/08–19/09), Wadden (30/06) dans `VANLIFE/TRIPS/` |
| Van — équipement | 🟡 | Meuble banquette (design 104×55×25) ; boîte vélo pliant ADO (plan v1) |

**Volumétrie** : 729 fichiers `.md`, 726 Mo — le projet le plus volumineux du
workspace PKA.

---

## Décisions clés

| Date | Décision | Contexte |
|------|----------|----------|
| 2026-11-12 | SELPHY CP1300 : alimentation 12V du van — boost DC-DC 12V→24V retenu | Fiche + BOM dans `LUPO/TECHNIQUES/ELECTRICITE/selphy-cp1300-alimentation-12v.md` ; écartés 30V et 220V AC |
| 2026-10-19 | Lupo Planner synchronisé avec DÉCOUVERTES | Import JSON généré |
| 2026-10-04 | INDEX restructuré | 4 axes clarifiés |
| 2026-08-21 | Voyage Italie documenté | 21/08 → 19/09 |

---

## TTD — Pending

- [ ] **P2 · — · (Cigogne + Dobby)** Traiter 36 `skipped` (OCR échoué → vision forcée) + 9 `parked_routes` + 5 `rejected`
- [ ] **P2 · — · (Cigogne)** Finaliser le meuble banquette (design 104×55×25)
- [ ] **P2 · — · (JC + Dobby)** Maquette boîte vélo pliant → marquer axes/boîtier/chainring → valider encoches

## TTD — Done (session 2026-11-12)

- [x] 2026-11-12 · Fiche alimentation SELPHY CP1300 12V (boost 12V→24V + porte-fusible 5A + schéma de montage) déposée et imprimée

## TTD — Done (session 2026-11-05)

- [x] 2026-11-05 · Revue documentaire : 590 entrées de queue confirmées comme journal, reste réel de 50 éléments ; aucun traitement du pipeline lancé

## TTD — Done (session 2026-10-22)

- [x] 2026-10-22 · Thread file créé ; arriéré DÉCOUVERTES requalifié (590 = journal, pas arriéré)

## TTD — Done (session 2026-10-28)

- [x] 2026-10-28 · Fiche roadtrip **Moselle** (Liège → Koblenz → source, 4 jours) — `.md` + carte Leaflet dans `VANLIFE/destinations/`

---

## Pipeline DÉCOUVERTES — fonctionnement

```
Telegram (groupe DÉCOUVERTES)
    ↓ collector.py  (process actif, en continu)
PKA-DECOUVERTES/raw/          6 éléments
    ↓
PKA-DECOUVERTES/queue/        590 entrées (journal), dont 540 analysées
    ↓ analyzer
PKA-DECOUVERTES/drafts/       0
    ↓ validation
PKA-DECOUVERTES/validated_places/   647 fiches
    ↓ decouvertes-to-planner.py
lupo-planner-import.json      191 Ko
```

La queue conserve **590 entrées historiques**, dont **540 déjà analysées**.
Le reste à traiter est de **50 éléments** : 36 `skipped`, 5 `rejected` et
9 `parked_routes`. L'analyseur reste le point d'attention pour ces cas résiduels ;
il ne faut pas compter les 590 entrées comme un arriéré.

---

## Structure

| Dossier | Contenu |
|---------|---------|
| `LUPO/` | Fiche technique, documents, stickers, `LUPO/TECHNIQUES/` (IOT, électricité, sécurité) |
| `LUPO-PLANNER/` | Application carte de voyage (import JSON) |
| `PKA-DECOUVERTES/` | Pipeline complet (collector, queue, validated_places, maps, reports) |
| `VANLIFE/` | Destinations, logistique, préférences |
| `VANLIFE/TRIPS/` | Voyages réalisés (Italie, Wadden) |

---

## Historique sessions

| Date | Résumé session | Livrable |
|------|---------------|----------|
| 2026-11-10 | Routage achats Lupo : factures suspension VB Air (2 417,58 € TTC) + douche intérieure (233,15 € TTC) vers `LUPO/TECHNIQUES/ACHATS/` + indexées file_index | `thread-travels.md`, `LUPO/TECHNIQUES/ACHATS/` |
| 2026-11-05 | Revue de cohérence : 590 entrées = journal, 50 résidus ; aucune exécution du pipeline | `thread-travels.md`, `index.md` |
| 2026-11-03 | Plan v1 boîte vélo pliant ADO (Lupo) — dimensions + débit | `VANLIFE/velo-pliant-boite-rangement.md` |
| 2026-10-28 | Roadtrip Moselle : fiche 4 jours + carte interactive | `Moselle_Koblenz_a_la_source.md` + `.html` |
| 2026-10-22 | Thread file créé après re-vérification des projets | ce fichier |
| 2026-10-19 | Génération `lupo-planner-import.json` | 191 Ko |
| 2026-10-04 | INDEX restructuré | — |

---

## Liens

- INDEX : `03_PROJECTS/07_TRAVELS/index.md`
- Pipeline : `PKA-DECOUVERTES/PKA_DECOUVERTES_Cahier_des_charges_V2.md`
- Planner : `03_PROJECTS/07_TRAVELS/LUPO-PLANNER/`
- Spécialiste : [[Cigogne]] 🦩

---

*Fichier créé le 2026-10-22 — il manquait alors que TRAVELS est le projet le
plus volumineux du workspace. Maintenu par Dobby 🦉 via `pka-thread-file`.*