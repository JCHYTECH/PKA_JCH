# Thread — PHOTO_AI_JURY

> Living document — mis à jour automatiquement par Dobby 🦉 en fin de session.
> **Dernière mise à jour** : 2026-11-22 — filtre éthique Argus : risque d'artificialité (captivité) signalé mais non bloquant (warning) ; analyse poursuivie
> **Statut** : 🟢 actif

---

## Vue d'ensemble

Moteur IA Argus de critique photo naturaliste — bilan historique Phase 0 : 58 analyses, score moyen 73.8/100, 81% taux d'acceptation JC. Prompt calibré (14/06). Base canonique réconciliée ; socle de retouche explicite JCH créé mais vide. Test technique MCP Lightroom réussi sur copie virtuelle RAW ; validation artistique toujours à faire.

---

## État actuel

| Axe | Statut | Détail |
|-----|--------|--------|
| Global | 🟢 | Actif, modèle calibré |
| Bases | 🟢 | Base canonique projet : **52 analyses**, 16 évaluations de rapports, schéma v1, intégrité `ok`, aucune violation FK. `run_analysis.py` et les scripts internes utilisent `scripts/argus_db.py`. `PHOTO/argus_critique.db` reste vide et intact ; l'orphelin ID 1 est conservé |
| Modèle | 🟢 | Prompt calibré (14/06), score 73.8/100 moyen |
| Retour JCH | 🟡 | `jch_feedback.py` testé sur copie puis appliqué : trois tables de sessions/propositions/validations **vides**. Aucun style déduit des votes sur les rapports ; aucune application ou lot automatique |
| MCP LR | 🟢 | Test technique réussi le 06/11 sur copie virtuelle RAW confirmée par JC : 8/8 lectures, exposition `0 → +0,10 → 0`, restauration dans `finally` et lecture indépendante à `0`. Aucun preset ni lot ; validation artistique distincte |
| Détection IA | 🟢 | **Nouveau 22/10** — `scripts/pka_ai_image_check.py`, **niveau 1 uniquement** (C2PA + EXIF). Classifieurs ViT mesurés inutilisables (12/12 faux positifs) → désactivés. Hook de rappel actif |
| EXIF + crop | 🟡 | **Nouveau 20/11** — `exif_raw.py` (EXIF enrichie), `exif_analysis.py` (6 audits : ETTR, bougé, netteté, diffraction, DOF, bruit), `crop_advisor.py` (recadrage tiers/nombre d'or, overlays A4). Crop gravé dans le XMP mais **LrC ne l'applique pas** (bloquant) |
| Filtre éthique | 🟢 | **Nouveau 22/11** — `captive_animal` ne bloque plus : passé en `warning` non bloquant, `artificiality_risk` transmis à l'analyse principale (risque signalé dans la critique, image non rejetée) |

---

## Décisions clés

| Date | Décision | Contexte |
|------|----------|----------|
| 2026-11-22 | Filtre éthique Argus non bloquant — `captive_animal` → `warning` : le risque d'artificialité est signalé dans la critique mais ne bloque plus l'analyse (seuls `human_visible` / `ai_generated` / `composite` / `bait` restent rejetés) | JC : « l'oiseau est libre » — indiquer le risque sans bloquer |
| 2026-11-06 | Conserver les votes sur les rapports séparés du style de retouche | Les 16 évaluations mesurent l'acceptation des critiques, pas les préférences artistiques ; le nouveau socle reste vide jusqu'aux choix explicites de JCH |
| 2026-11-06 | Limiter le premier test Lightroom à une variation réversible | Baseline → `Exposure2012 +0,10` → relecture → restauration dans `finally`, uniquement sur copie virtuelle RAW ; validation technique distincte de la validation artistique |
| 2026-07-02 | INDEX créé avec cross-réfs ARTEON + PHOTO_NATURE | Manquait auparavant |
| 2026-06-14 | Prompt calibré | 81% acceptation JC |
| 2026-11-20 | Ratio de base A4 (1:√2) paysage + portrait | Recadrage assisté ; nombre d'or retenu comme guide |
| 2026-11-20 | LrC ne lit que la racine de `CameraRaw/Settings/` | Les sous-dossiers sont ignorés ; presets « in work » rangés en racine avec préfixe |
| 2026-11-20 | Crop XMP = position des bords (0-1) | Pas « fraction rognée » ; CropBottom/CropRight initialement inversés |

---

## TTD — Pending

- [ ] **P2 · — · (JCH + Argus)** Enregistrer des comparaisons A/B avec tutoriel et une validation sur image inédite ; aucune généralisation ou lot automatique avant ces données réelles
- [ ] **P2 · — · (Argus)** Prochaine fournée d'analyses seulement après décision de JC ; aucun appel IA payant effectué dans ce chantier
- [ ] **P1 · — · (Dobby)** Résoudre l'application du crop dans LrC : piste sidecar `.xmp` à côté du CR3 (au lieu du preset) ; test à refaire demain matin
- [ ] **P2 · — · (Dobby)** Repasser `untitled-2643.CR3` pour lui donner son crop (nombre d'or)

## TTD — Done

- [x] 2026-11-06 · Lightroom MCP activé manuellement par JC ; copie virtuelle RAW `Evieux-42.CR3` confirmée, 8/8 lectures, test borné `Exposure2012 0 → +0,10 → 0` dans `finally`, restauration revérifiée indépendamment ; aucun autre réglage appliqué
- [x] 2026-11-06 · Base canonique consolidée : 52 analyses IDs 7–58, 52 hashes/PDF/XMP, 16 évaluations, orphelin ID 1 conservé ; `scripts/argus_db.py` partagé, ancien fichier `PHOTO/` vide et intact
- [x] 2026-11-06 · Sauvegarde SQLite intègre `backups/20261106-120424-argus-feedback-foundation/`, migration v1 testée deux fois sur copie puis appliquée ; trois tables de retour JCH vides, historique inchangé
- [x] 2026-11-05 · Revue de cohérence documentaire et contrôle SQLite en lecture seule : 52 enregistrements projet, base `PHOTO/` vide, aucune donnée modifiée
- [x] 2026-10-22 · Outil détection IA niveau 1 (C2PA + EXIF) ajouté

---

## Historique sessions

| Date | Résumé session | Livrable |
|------|---------------|----------|
| 2026-11-22 | Filtre éthique rendu non bloquant : `captive_animal` → `warning`, `artificiality_risk` transmis à l'analyse ; `filter_ethics.py` + `run_analysis.py` modifiés | `~/.claude/skills/photo-analyse-wildlife/scripts/filter_ethics.py`, `run_analysis.py` |
| 2026-11-20 | Pipeline Argus enrichi : télémétrie EXIF + 6 audits + recadrage assisté (overlays A4) ; analyses CR3 untitled-2643/2648 (76-79/100) ; crop gravé dans le XMP mais non appliqué par LrC | `scripts/exif_raw.py`, `scripts/exif_analysis.py`, `scripts/crop_advisor.py`, `run_analysis.py`, `generate_xmp.py` |
| 2026-11-06 | Test technique Lightroom réussi sur copie virtuelle RAW confirmée par JC ; 8/8 lectures, variation +0,10 EV puis restauration exacte et revérifiée ; validation artistique non réalisée | `_local/lightroom-mcp/tests/e2e/mcp-runner.mjs`, `INDEX.md`, `roadmap-mcp-integration.md`, `executive-summary.md`, `thread-photo-ai-jury.md`, `wiki/Daily/2026/11/2026-11-06-mcp-home-assistant-et-lightroom-testes.md` |
| 2026-11-06 | Base canonique confirmée ; socle vide de retour JCH migré et vérifié ; test Lightroom documenté mais bloqué par Start Server et la sélection manuelle | `jch_feedback.py`, sauvegarde SQLite, `INDEX.md`, `roadmap-mcp-integration.md`, `executive-summary.md`, `thread-photo-ai-jury.md` |
| 2026-11-05 | Contrôle SQLite en lecture seule : 52 enregistrements projet, fichier `PHOTO/` vide ; aucune modification de base | `INDEX.md`, `thread-photo-ai-jury.md` |
| 2026-10-22 | Outil détection IA (niveau 1) + veille état de l'art | `scripts/pka_ai_image_check.py`, `ai-image-detection.md` |
| 2026-07-02 | INDEX créé, cross-réfs | — |
| 2026-06-14 | Prompt calibré | — |

---

## Liens

- INDEX : `03_PROJECTS/05_PHOTO_AI_JURY/INDEX.md`
- Base canonique : `03_PROJECTS/05_PHOTO_AI_JURY/argus_critique.db` (52 analyses, schéma v1)
- Socle de retour explicite : `03_PROJECTS/05_PHOTO_AI_JURY/jch_feedback.py`
- Ancien chemin vide conservé intact : `PHOTO/argus_critique.db` (0 octet au 06/11)
- Presets : `03_PROJECTS/06_PHOTO_NATURE/tech/presets-argus/`

---

*Fichier maintenu par Dobby 🦉 via le skill `pka-thread-file`.*