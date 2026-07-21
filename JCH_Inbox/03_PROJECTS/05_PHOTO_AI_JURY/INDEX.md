---
tags:
  - type/project
  - status/active
  - photo-ai-jury
  - argus
owner: "[[Dobby]]"
last_updated: 2026-07-02
---
# PHOTO_AI_JURY — Moteur IA de critique photo ([[Argus]])

> Pipeline d'analyse critique automatisé pour photographies wildlife.
> Sert **[[L'Instant Lu]]** (service payant ARTEON) et l'auto-évaluation JCH.
> Spécialistes : [[Argus]] 🦅 (critique), [[Chouette]] 🦉 (diagnostic matériel), [[Héron]] 🦢 (conseil papier)

---

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

→ Architecture complète : `02_ARTEON/strategy/arteon-colonne-vertebrale.md` §1

## Structure

```
05_PHOTO_AI_JURY/
├── INDEX.md              ← ce fichier
├── analyses/             ← 11 PDF rapports critiques (échantillon Phase 0.3)
├── argus_critique.db     ← base de données (58 analyses Phase 0, EXIF, scores, lr_params)
├── mcp_apply_lr.py       ← module application automatique Lightroom (51 clés SDK mappées)
├── moderation_admin.py   ← interface de modération (captivité, cas limites)
└── roadmap-mcp-integration.md  ← roadmap MCP Lightroom + Photoshop
```

## Données clés

| Indicateur | Valeur | Source |
|------------|--------|--------|
| Analyses totales | 58 | `argus_critique.db` |
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

→ Dashboard : `02_ARTEON/phase03-evaluation-argus.html`

## MCP Lightroom — Automatisation

| Composant | État |
|-----------|------|
| Plugin Lua (LightroomMCP.lrplugin) | ✅ Installé |
| Serveur MCP (v0.4.1) | ✅ Dans `_local/lightroom-mcp/` |
| Module Argus `mcp_apply_lr.py` | ✅ 51 clés SDK mappées |
| Activation plugin (Start Server) | ⚠️ À faire dans LR → Plug-in Manager |
| Pipeline complet (photo → analyse → LR auto) | ⏳ |

→ Roadmap : `roadmap-mcp-integration.md`

## Presets XMP

11 presets Argus générés et stockés dans `06_PHOTO_NATURE/tech/presets-argus/`. Ces presets correspondent aux 11 PDF analyses de ce projet (même ensemble de photos, deux emplacements : livrable PDF ici, preset technique dans PHOTO_NATURE).

## Scripts externes

| Script | Emplacement | Rôle |
|--------|-------------|------|
| `run_analysis.py` | `~/.claude/skills/photo-analyse-wildlife/scripts/` | Pipeline principal |
| `filter_ethics.py` | même dossier | Filtre Haiku pré-analyse |
| `argus_batch.py` | `PKA_JCH/scripts/` | Traitement en lot |
| `heron_paper.py` | `PKA_JCH/scripts/` | Recommandation papier ET8550 |
| `chouette_diagnostic.py` | `PKA_JCH/scripts/` | Diagnostic matériel (EXIF vs scores) |
| `argus_progression.py` | `PKA_JCH/scripts/` | Indice de progression (paliers 20/50/100) |

DB principale : `/Users/jchavauxm5/PKA_JCH/PHOTO/argus_critique.db`

## Voir aussi

- [[ARTEON]] — projet parent, L'Instant Lu (`../02_ARTEON/`)
- [[WildLens]] — journal naturaliste, canal d'acquisition (`../02_ARTEON/wildlens/`)
- PHOTO_NATURE — matière première terrain et technique (`../06_PHOTO_NATURE/`)
- `02_ARTEON/strategy/arteon-colonne-vertebrale.md` — architecture pipeline complète
- `02_ARTEON/phase03-evaluation-argus.md` — évaluation Phase 0.3

---

*Index créé par [[Dobby]] 🦉 le 2026-07-02*
