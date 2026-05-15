---
date: 2026-05-11
tags: [arteon, backbone, pipeline, phase0, architecture, l-instant-lu]
type: reference
status: actif
owner: Dobby
---

# ARTEON — Colonne vertébrale complétée

> État au 2026-05-11 — Phase 0 close, pipeline technique opérationnel.  
> Ce document décrit ce qui existe et tourne. Pour la roadmap commerciale, voir `plan-action-critique-service.md`. Pour l'état éditorial et les décisions de marque, voir `arteon-etat-projet.md`.

---

## 1. Pipeline Argus — Analyse photo (opérationnel)

**Entrée :** JPEG / CR3 / NEF / DNG  
**Sortie :** PDF rapport critique + XMP preset Lightroom + conseil papier Héron + log DB

```
Image soumise
    │
    ▼
[Haiku — filtre éthique ~€0,002]
    ├── Humain / IA / Trucage / Appâtage → REFUS AUTO (email motivé)
    ├── Captivité → FILE MODÉRATION (JCH décide)
    └── Conforme ──────────────────────────────────────────────┐
                                                               ▼
                                                  [Opus 4.7 — analyse vision]
                                                  5 axes : composition / exposition /
                                                  netteté / technique / impact (0-20)
                                                  + corrections Lightroom (lr_params)
                                                  + couleur dominante + espèce
                                                               │
                                       ┌───────────────────────┤
                                       ▼                       ▼
                               PDF rapport             XMP preset LR
                               (critique + scores     (importable
                               + avant/après)          directement)
                                       │
                                       ▼
                              Héron — conseil papier
                              (baryta / lustre / coton…)
                              fichier _papier.md joint
                                       │
                                       ▼
                              argus_critique.db
                              (log tokens / coût /
                               EXIF / scores / tier)
```

**Scripts clés :**
| Script | Emplacement | Rôle |
|--------|-------------|------|
| `run_analysis.py` | `~/.claude/skills/photo-analyse-wildlife/scripts/` | Pipeline principal — un appel, tout sort |
| `filter_ethics.py` | même dossier | Filtre Haiku pré-analyse |
| `argus_batch.py` | `PKA_JCH/scripts/` | Traitement en lot (avec `--bypass-ethics`) |
| `heron_paper.py` | `PKA_JCH/scripts/` | Recommandation papier Epson ET8550 |
| `chouette_diagnostic.py` | `PKA_JCH/scripts/` | Diagnostic matériel (EXIF vs scores) |
| `argus_progression.py` | `PKA_JCH/scripts/` | Indice de progression (paliers 20/50/100) |
| `backfill_exif.py` | `PKA_JCH/scripts/` | Backfill EXIF sur analyses existantes |

**Base de données :** `/Users/jchavauxm5/PKA_JCH/PHOTO/argus_critique.db`  
Table principale : `analyses` — 58 enregistrements JCH Phase 0, EXIF complets.

---

## 2. Chouette — Diagnostic matériel (opérationnel)

Corrèle les données EXIF avec les scores Argus pour distinguer **problème matériel** (équipement) vs **problème technique** (photographe).

**4 diagnostics :**
1. Netteté vs focale (seuil 400mm)
2. Netteté vs ISO (seuil 3200)
3. Exposition vs ouverture (seuil f/6.3)
4. Profil créatif vs technique (composition+impact vs nettete+tech+expo)

**Résultat Phase 0 JCH (58 photos) :** 0 diagnostic matériel détecté — les scores sont homogènes. L'axe faible (Exposition 14.67/20) relève de la technique photographique.

---

## 3. Héron — Conseil papier (opérationnel, intégré au pipeline)

Recommande le papier optimal pour impression sur Epson ET8550 selon :
- Température couleur dominante (chaud / neutre / froid)
- Niveau de contraste (scores exposition + technique)
- Sujet (macro, action, tons chauds, ambiance douce)

**6 papiers catalogués :** baryta 310g · lustre 260g · fine art cotton 300g · métallique 260g · coton texturé 300g · premium glossy 255g. Chaque recommandation inclut le profil ICC à charger dans Lightroom.

Appelé automatiquement à la fin de chaque analyse — génère un fichier `<stem>_papier.md` dans `PHOTO/analyses/`.

---

## 4. Argus Progression — Paliers (opérationnel)

Calcule l'indice de progression par palier de 20/50/100 photos avec delta par axe et note pédagogique sur le biais de sélection.

**Résultat JCH :** 58 photos analysées. Score moyen : 76.7/100.  
Point fort : Impact visuel (16.26/20). Axe prioritaire : Exposition (14.67/20).  
Progression globale : -2.3 pts entre palier 20 et 100 (normal — biais de sélection).

---

## 5. Skill memory system (opérationnel)

Auto-génération et recherche de procédures réutilisables. Réplique le mécanisme central d'Hermes Agent en natif, sans dépendance externe.

| Script | Rôle |
|--------|------|
| `skill_write.py` | Upsert d'une procédure (par trigger_pattern) |
| `skill_search.py` | Recherche full-text, incrémente usage_count |

Pré-tâche : chargement silencieux des skills pertinents. Post-tâche : capture automatique si ≥3 étapes.

---

## 6. Multi-model routing (opérationnel)

Sélection dynamique du modèle par type de tâche — aucune modification de code nécessaire, tout passe par `model_config.json`.

**Providers disponibles :** Claude (Anthropic) · Codex CLI · Gemini CLI · Gemma4 (Ollama local) · Qwen3.6 (Ollama local)

Launcher : `dobby.sh --model claude|codex|gemini|gemma4|qwen3`

---

## 7. Identité éditoriale ARTEON (validée)

| Élément | Décision | Fichier |
|---------|----------|---------|
| Slogan | *L'instant figé, la pensée en mouvement.* | `arteon-etat-projet.md` |
| Manifeste | 2 versions livrées (court ~250 mots, long ~515 mots) | `arteon-manifeste-{court,long}.md` |
| Domaine | arteon.be enregistré | — |
| Stack | Shopify Basic + Ghost (WildLens) + WhiteWall | `arteon-architecture-charte.md` |
| Ton | 20% militant · 30% contemplatif · 30% scientifique · 20% technicien | `arteon-etat-projet.md` |
| Langue | FR/EN/IT (site) · EN (WildLens) | — |

---

## 8. Service L'Instant Lu (plan validé, backend à construire)

**Prix :** €1,90 TTC l'analyse · 1ère gratuite à l'inscription  
**KPI :** €1 000/mois CA (280 analyses + 2 clubs B2B)  
**Délai lancement :** J+49 depuis top départ backend  
**Validation humaine :** JCH valide chaque analyse avant livraison (SLA 2h) — différenciateur vs concurrents 100% auto

Roadmap complète : `plan-action-critique-service.md`

---

## 9. Juridique (rédigé, à valider JCH)

| Document | Fichier |
|----------|---------|
| CGU L'Instant Lu | `legal/CGU-instant-lu.md` |
| Contrat B2B clubs | `legal/contrat-b2b-clubs.md` |
| Licence badge certifié | `legal/contrat-licence-badge.md` |
| Politique confidentialité | `legal/politique-confidentialite.md` |
| Droits images client | `legal/texte-droits-images-client.md` |

---

## 10. Ce qui reste à construire

| Priorité | Tâche | Owner |
|----------|-------|-------|
| 🔴 | Phase 0.3 — JCH évalue les 58 rapports PDF (qualité prompt) | JCH |
| 🔴 | Charte graphique ARTEON (étape 4) | Vega |
| 🟠 | Backend FastAPI — endpoint `/analyse` | Forge |
| 🟠 | Stripe + système crédits | Forge |
| 🟠 | Interface validation JCH (notification + aperçu + 1 clic) | Forge |
| 🟡 | Landing page `critique.arteon.be` | Vega |
| 🟡 | Setup Shopify + WhiteWall | Forge |
| 🟡 | Profils boîtier C1/C2/C3 (R10 + 90D) | Chouette |
| 🟡 | Interface web Dobby (model selector + team.db view) | Forge + Vega |
| ⚪ | Article WILDLENS "Comment l'IA juge votre photo" | Miel |
| ⚪ | Approche 2 clubs photo B2B | Delphi |

---

*Référence Dobby — mis à jour 2026-05-11*
