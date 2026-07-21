# PHOTO_NATURE — Index projet

Dernière mise à jour : 2026-07-02

## Description
Activités wildlife et photographie naturaliste de JCH/Arteon.
Couvre la technique photo, le post-traitement, l'impression, les observations terrain, et le projet Faune-Autour.

> **Ce projet est la matière première** des projets [[ARTEON]] (commercialisation) et [[PHOTO_AI_JURY]] (analyse IA).
> Les photos évaluées par [[Argus]] proviennent du terrain documenté ici. Les presets XMP générés reviennent dans `tech/presets-argus/`.

## Structure
| Dossier | Contenu |
|---|---|
| `docs/` | Synthèses, guides fiches terrain, projet [[faune-autour]], templates |
| `content/faune-autour/` | 7 fiches projet Faune-Autour (espèces, lieux, sorties, matériel…) |
| `content/fiches/` | Fiches espèces (grenouille rousse, Acrida ungarica, arbres Wallonie…) |
| `content/observations/` | Observations terrain (canard colvert, corbeaux, grenouille rousse…) |
| `content/lieux/` | Fiches sites ([[Camargue]]) |
| `content/taxonomie/` | Fiches taxonomie ([[Acrididae]]) |
| `content/` | Articles wildlife, projets photo (canards) |
| `tech/editing/` | Post-traitement : Lightroom, presets, focus stack, Helicon, Zerene |
| `tech/printing/` | Impression ET8550 : workflows, color fix, papiers, drivers |
| `tech/matos/` | Équipement JCH, objectifs, accessoires macro |
| `tech/onsite/` | Techniques terrain : macro, chronophotographie, voie lactée, WeMacro |
| `tech/presets-argus/` | 11 presets XMP générés par [[Argus]] (→ voir `05_PHOTO_AI_JURY/analyses/`) |
| `tech/plugins/` | Plugins Lightroom |
| `comms/` | Correspondance ([[Natagora]] 2026-04-16) |
| `FAUNE_AUTOUR/` | PWA gelée — extraite en sous-projet |

## Fichiers clés
- `docs/synthese_systeme_faune.md` — Synthèse système faune JCH
- `docs/faune-autour.md` — Vue d'ensemble projet Faune-Autour
- `docs/00_Project overview.md` — Template projet Faune-Autour (structure, pas contenu)
- `docs/Mise_en_page_fiche_terrain.md` — Mise en page fiche terrain
- `tech/printing/ET8550_Workflow.md` — Workflow impression ET8550 (référence principale)
- `tech/printing/ET8550_color_fix.md` — Correction couleur ET8550
- `tech/matos/Equipment_JCH.md` — Inventaire équipement complet
- `tech/onsite/Guide_technique_focus_stacking_macrophotographie.md` — Guide focus stacking
- `content/fiches/Espèce - Grenouille rousse.md` — Fiche espèce modèle
- `keyword_taxonomy.json` — Taxonomie keyworder (62 catégories)
- `README_keyworder.md` — Documentation auto-tagging photos

## Outils

- **photo_keyworder.py** — Auto-tagging photos nature par vision model local (Ollama). 100% autonome. 62 catégories taxonomiques. Sortie IPTC + XMP + HierarchicalSubject → Lightroom.
- Usage : `python3 scripts/photo_keyworder.py --input ~/Desktop/Photos/ --m1 --dry-run`

## Statut
Actif — 116 fichiers indexés. Keyworder fonctionnel. Presets Argus (11 XMP) stockés dans `tech/presets-argus/`.

## Voir aussi

- [[ARTEON]] — commercialisation des photos (shop, L'Instant Lu, manifeste) → `../02_ARTEON/`
- [[WildLens]] — journal naturaliste, canal d'acquisition → `../02_ARTEON/wildlens/`
- [[PHOTO_AI_JURY]] / [[Argus]] — moteur IA critique photo → `../05_PHOTO_AI_JURY/INDEX.md`
- `../05_PHOTO_AI_JURY/analyses/` — 11 PDF rapports critiques (correspondent aux 11 XMP presets ici)

---

*Index mis à jour par [[Dobby]] 🦉 le 2026-07-02*
