# PHOTO_NATURE — Index projet

Dernière mise à jour : 2026-11-05 — navigation ; état opérationnel dans [thread-photo-nature.md](thread-photo-nature.md).

## Description
Activités wildlife et photographie naturaliste de JCH/Arteon.
Couvre la technique photo, le post-traitement, l'impression, les observations terrain, et le projet Faune-Autour.

> **Ce projet est la matière première** des projets [[ARTEON]] (commercialisation) et [[PHOTO_AI_JURY]] (analyse IA).
> Les photos évaluées par [[Argus]] proviennent du terrain documenté ici. Les presets XMP générés reviennent dans `tech/presets-argus/`.

## Point d'entrée

1. [thread-photo-nature.md](thread-photo-nature.md) — état courant et décisions.
2. [README_keyworder.md](README_keyworder.md) — documentation de l'auto-tagging.
3. [executive-summary.md](executive-summary.md) — synthèse du projet.
4. [Structure et fichiers clés ci-dessous](#structure) — accès aux contenus terrain et techniques.

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
| `tech/presets-argus/` | 11 presets XMP générés par [[Argus]] (→ voir [analyses Argus](../05_PHOTO_AI_JURY/analyses/)) |
| `tech/plugins/` | Plugins Lightroom |
| `comms/` | Correspondance ([[Natagora]] 2026-04-16) |
| `FAUNE_AUTOUR/` | PWA gelée — extraite en sous-projet |

## Fichiers clés

- [docs/synthese_systeme_faune.md](docs/synthese_systeme_faune.md) — synthèse système faune JCH.
- [docs/faune-autour.md](docs/faune-autour.md) — vue d'ensemble du projet Faune-Autour.
- [docs/00_Project overview.md](<docs/00_Project overview.md>) — template Faune-Autour, structure et non contenu.
- [docs/Mise_en_page_fiche_terrain.md](docs/Mise_en_page_fiche_terrain.md) — mise en page des fiches terrain.
- [tech/printing/ET8550_Workflow.md](tech/printing/ET8550_Workflow.md) — workflow impression ET8550 de référence.
- [tech/printing/ET8550_color_fix.md](tech/printing/ET8550_color_fix.md) — correction couleur ET8550.
- [tech/matos/Equipment_JCH.md](tech/matos/Equipment_JCH.md) — inventaire complet de l'équipement.
- [Guide focus stacking](tech/onsite/Guide_technique_focus_stacking_macrophotographie.md).
- [Espèce — Grenouille rousse](<content/fiches/Espèce - Grenouille rousse.md>) — fiche espèce modèle.
- [keyword_taxonomy.json](keyword_taxonomy.json) — taxonomie keyworder, 62 catégories.
- [README_keyworder.md](README_keyworder.md) — documentation auto-tagging photos.

## Outils

- **photo_keyworder.py** — Auto-tagging photos nature par vision model local (Ollama). 100% autonome. 62 catégories taxonomiques. Sortie IPTC + XMP + HierarchicalSubject → Lightroom.
- Usage : `python3 scripts/photo_keyworder.py --input ~/Desktop/Photos/ --m1 --dry-run`

## Statut
Actif — 116 fichiers indexés. Keyworder fonctionnel. Presets Argus (11 XMP) stockés dans `tech/presets-argus/`.

## Voir aussi

- [ARTEON](../02_ARTEON/) — commercialisation des photos, shop et L'Instant Lu.
- [WildLens](../02_ARTEON/wildlens/) — journal naturaliste et canal d'acquisition.
- [PHOTO_AI_JURY / Argus](../05_PHOTO_AI_JURY/INDEX.md) — moteur IA de critique photo.
- [Analyses Argus](../05_PHOTO_AI_JURY/analyses/) — rapports PDF correspondant aux presets XMP.

---

*Index créé par [[Dobby]] 🦉 le 2026-07-02 ; navigation révisée le 2026-11-05.*
