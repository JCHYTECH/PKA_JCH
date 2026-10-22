# Thread — PHOTO_AI_JURY

> Living document — mis à jour automatiquement par Dobby 🦉 en fin de session.
> **Dernière mise à jour** : 2026-10-22 — outil de détection IA ajouté (niveau 1) ; MCP Lightroom toujours non activé
> **Statut** : 🟢 actif

---

## Vue d'ensemble

Moteur IA Argus de critique photo naturaliste — 58 analyses cumulées, score moyen 73.8/100, 81% taux d'acceptation JC. Prompt calibré (14/06). MCP Lightroom partiellement installé.

---

## État actuel

| Axe | Statut | Détail |
|-----|--------|--------|
| Global | 🟢 | Actif, modèle calibré |
| Base | 🟢 | argus_critique.db — 58 analyses |
| Modèle | 🟢 | Prompt calibré (14/06), score 73.8/100 moyen |
| MCP LR | 🟡 | Partiellement installé — activation Start Server manquante (inchangé depuis 03/07) |
| Détection IA | 🟢 | **Nouveau 22/10** — `scripts/pka_ai_image_check.py`, **niveau 1 uniquement** (C2PA + EXIF). Classifieurs ViT mesurés inutilisables (12/12 faux positifs) → désactivés. Hook de rappel actif |

---

## Décisions clés

| Date | Décision | Contexte |
|------|----------|----------|
| 2026-07-02 | INDEX créé avec cross-réfs ARTEON + PHOTO_NATURE | Manquait auparavant |
| 2026-06-14 | Prompt calibré | 81% acceptation JC |

---

## Prochaine étape

**Action** : Activer MCP Lightroom (Start Server) + prochaine fournée d'analyses
**Deadline** : —
**Responsable** : Argus

---

## Historique sessions

| Date | Résumé session | Livrable |
|------|---------------|----------|
| 2026-10-22 | Outil détection IA (niveau 1) + veille état de l'art | `scripts/pka_ai_image_check.py`, `ai-image-detection.md` |
| 2026-07-02 | INDEX créé, cross-réfs | — |
| 2026-06-14 | Prompt calibré | — |

---

## Liens

- INDEX : `03_PROJECTS/05_PHOTO_AI_JURY/INDEX.md`
- Base : `03_PROJECTS/05_PHOTO_AI_JURY/argus_critique.db`
- Presets : `03_PROJECTS/05_PHOTO_AI_JURY/presets/`

---

*Fichier maintenu par Dobby 🦉 via le skill `pka-thread-file`.*
