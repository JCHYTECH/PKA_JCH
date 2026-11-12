---
tags:
  - type/project
  - status/active
  - photo-ai-jury
  - argus
owner: "[[Dobby]]"
last_updated: 2026-11-06
---
# PHOTO_AI_JURY — Moteur IA de critique photo ([[Argus]])

> Pipeline d'analyse critique automatisé pour photographies wildlife.
> Sert **[[L'Instant Lu]]** (service payant ARTEON) et l'auto-évaluation JCH.
> Spécialistes : [[Argus]] 🦅 (critique), [[Chouette]] 🦉 (diagnostic matériel), [[Héron]] 🦢 (conseil papier)

---

## Point d'entrée

1. [thread-photo-ai-jury.md](thread-photo-ai-jury.md) — état opérationnel, décisions et prochaine action.
2. [roadmap-mcp-integration.md](roadmap-mcp-integration.md) — chantier d'automatisation Lightroom.
3. [ai-image-detection.md](ai-image-detection.md) — limites mesurées de la détection d'images IA.
4. [executive-summary.md](executive-summary.md) — synthèse du projet.

## Description

Le projet PHOTO_AI_JURY est le **moteur IA** qui analyse les photos wildlife de JCH (et futures photos clientes) selon 5 axes : composition, exposition, netteté, technique, impact. Il génère un rapport PDF + un preset XMP Lightroom + une recommandation papier.

## Pipeline

```
Image soumise (JPEG/CR3/NEF/DNG)
    │
    ▼
[Haiku — filtre éthique ~€0,002]
    ├── Humain / IA / Trucage / Appâtage → REFUS AUTO
    ├── Captivité → FILE MODÉRATION (JCH décide)
    └── Conforme ─────────────────────────────────────┐
                                                     ▼
                                        [Opus 4.7 — analyse vision]
                                        5 axes (0-20) + lr_params (JSON)
                                        + couleur dominante + espèce
                                                     │
                             ┌───────────────────────┤
                             ▼                       ▼
                     PDF rapport             XMP preset LR
                     (scores + critique)     (importable directement)
                             │
                             ▼
                    Héron — conseil papier
                    (baryta / lustre / coton…)
                             │
                             ▼
                    argus_critique.db
```

→ [Architecture complète](../02_ARTEON/strategy/arteon-colonne-vertebrale.md) §1

## Structure

```
05_PHOTO_AI_JURY/
├── INDEX.md              ← ce fichier
├── analyses/             ← 11 PDF rapports critiques (échantillon Phase 0.3)
├── argus_critique.db     ← base canonique (52 analyses ; schéma v1 vérifié le 06/11)
├── jch_feedback.py       ← migration et statut du socle de retour explicite JCH
├── mcp_apply_lr.py       ← préparation des réglages Lightroom (51 clés SDK mappées)
├── moderation_admin.py   ← interface de modération (captivité, cas limites)
└── roadmap-mcp-integration.md  ← roadmap MCP Lightroom + Photoshop
```

## Données clés

| Indicateur | Valeur | Source |
|------------|--------|--------|
| Analyses historiques Phase 0 | 58 | Bilan Phase 0 — distinct du comptage SQLite actuel |
| Score moyen | 73.8/100 | Phase 0.3 |
| Tier ⭐ Excellent | 9 photos (83.9) | Phase 0.3 |
| Tier 🟣 Très Bon | 24 photos (74.9) | Phase 0.3 |
| Tier 🟡 Bon | 24 photos (67.7) | Phase 0.3 |
| Tier 🟠 À améliorer | 1 photo (57.0) | Phase 0.3 |
| Axe fort | Impact visuel (15.7/20) | Phase 0.3 |
| Axe faible | Exposition (14.7/20) | Phase 0.3 |
| Coût total Phase 0 | ~$9.85 | 58 analyses × ~$0.17 |
| Diagnostic matériel | 0 problème détecté | Chouette — scores homogènes |

## Évaluation JCH (Phase 0.3)

16/58 analyses évaluées par JC. Résultat : **81% d'acceptation** (2👍 + 11👌), 19% de rejet (3👎).

Points faibles corrigés : identification d'espèces ambiguë, scènes complexes. Prompt mis à jour dans `run_analysis.py` (+ règles géographiques, + règles scènes complexes).

→ [Dashboard historique](../02_ARTEON/passe-utile/phase03-evaluation-argus.html)

## MCP Lightroom — Automatisation

| Composant | État |
|-----------|------|
| Plugin Lua (LightroomMCP.lrplugin) | ✅ Installé |
| Serveur MCP (v0.4.1) | ✅ Dans `_local/lightroom-mcp/` |
| Module Argus `mcp_apply_lr.py` | ✅ 51 clés SDK mappées |
| Activation plugin (Start Server) | ✅ Activé et vérifié le 06/11 sur les ports locaux 58763/58764 |
| Test MCP sûr sur copie virtuelle RAW | ✅ 8/8 lectures ; exposition `0 → +0,10 → 0`, restauration revérifiée |
| Pipeline complet avec validation JCH | ⏳ Non validé de bout en bout |

`mcp_apply_lr.py` prépare le JSON SDK ; il n'applique rien seul. Le 2026-11-06, JC a confirmé la sélection de la copie virtuelle RAW `Evieux-42.CR3`. Le mode borné `exposure-restore --virtual-copy-confirmed` de `_local/lightroom-mcp/tests/e2e/mcp-runner.mjs` a lu la baseline `0`, appliqué uniquement `Exposure2012 +0,10`, relu la valeur puis restauré `0` dans un `finally`. Une nouvelle lecture indépendante et les 8 tests `read` ont réussi. Ce résultat technique ne constitue pas une validation artistique ; aucun lot ni preset n'a été appliqué.

## Retour explicite JCH — socle du 2026-11-06

`jch_feedback.py migrate` a créé le schéma SQLite v1 après validation sur une copie ; `status` confirme **52 analyses, 16 évaluations de rapports, intégrité `ok`, aucune violation de clé étrangère**. Les tables `retouch_sessions`, `retouch_proposals` et `retouch_validations` sont **vides** : elles préparent baselines/finaux, comparaisons A/B avec tutoriel et validation sur image inédite, sans déduire un style des votes sur les rapports. Aucune application en lot ni aucun apprentissage automatique n'est implémenté. Une validation enregistrée appartient explicitement à JCH.

→ Roadmap : `roadmap-mcp-integration.md`

## Presets XMP

11 presets Argus générés et stockés dans [`06_PHOTO_NATURE/tech/presets-argus/`](../06_PHOTO_NATURE/tech/presets-argus/). Ces presets correspondent aux 11 PDF analyses de ce projet (même ensemble de photos, deux emplacements : livrable PDF ici, preset technique dans PHOTO_NATURE).

## Scripts externes

| Script | Emplacement | Rôle |
|--------|-------------|------|
| `run_analysis.py` | `~/.claude/skills/photo-analyse-wildlife/scripts/` | Pipeline principal |
| `filter_ethics.py` | même dossier | Filtre Haiku pré-analyse |
| `argus_batch.py` | `PKA_JCH/scripts/` | Traitement en lot |
| `heron_paper.py` | `PKA_JCH/scripts/` | Recommandation papier ET8550 |
| `chouette_diagnostic.py` | `PKA_JCH/scripts/` | Diagnostic matériel (EXIF vs scores) |
| `argus_progression.py` | `PKA_JCH/scripts/` | Indice de progression (paliers 20/50/100) |

**Bases — état vérifié le 2026-11-06 :** `05_PHOTO_AI_JURY/argus_critique.db` est la base canonique : 52 analyses (IDs 7–58), 52 hashes/PDF/XMP, 16 évaluations de rapports et l'orphelin historique ID 1 dans la file de modération, conservé. Les 58 analyses sont le bilan historique de Phase 0, pas le nombre de lignes actuel. `scripts/argus_db.py` fournit ce chemin à `run_analysis.py`, `argus_progression.py`, `chouette_diagnostic.py`, `heron_paper.py` et `backfill_exif.py`. `PHOTO/argus_critique.db` reste vide (0 octet) et intact ; aucune fusion n'a été nécessaire. La sauvegarde pré-migration est dans `backups/20261106-120424-argus-feedback-foundation/`.

## Voir aussi

- [ARTEON](../02_ARTEON/) — projet parent, L'Instant Lu.
- [WildLens](../02_ARTEON/wildlens/) — journal naturaliste, canal d'acquisition.
- [PHOTO_NATURE](../06_PHOTO_NATURE/) — matière première terrain et technique.
- [Architecture du pipeline](../02_ARTEON/strategy/arteon-colonne-vertebrale.md).
- [Évaluation Phase 0.3 — document historique](../02_ARTEON/passe-utile/phase03-evaluation-argus.md).

---

*Index créé par [[Dobby]] 🦉 le 2026-07-02 ; état technique révisé le 2026-11-06.*
