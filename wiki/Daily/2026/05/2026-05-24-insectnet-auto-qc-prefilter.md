---
date: 2026-05-24
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-05-24 — insectnet-auto-qc-prefilter

## Session — 21:54 — insectnet-auto-qc-prefilter

### Contexte
- Modèle : codex
- Projet : WILDNEXUS

### Résumé
Ajout d'un prefiltre auto-QC InsectNet base sur les spectrogrammes: 559 segments scores, 494 auto_keep_candidate, 21 auto_reject_candidate, 44 human_review; l'app QC affiche maintenant ces suggestions.

### Actions
Creation de scripts/insectnet_auto_qc.py; ajout des tests auto-QC; generation de segment_qc_auto.csv; mise a jour de scripts/insectnet_qc_review_app.py pour afficher auto_qc/auto_reason/auto_score; regeneration et ouverture de insectnet-qc-review.html; creation du log auto-qc-prefilter-log.md.

### Décisions
L'auto-QC reste un prefiltre non autoritaire: il ne modifie jamais visual_qc en keep; JCH valide toujours keep/reject; les suggestions servent a prioriser la revue.

### Prochaines étapes
JCH poursuit la revue dans l'app avec les suggestions auto visibles; exporter segment_qc_reviewed.csv; importer ensuite les decisions et regenerer le split groupe.
