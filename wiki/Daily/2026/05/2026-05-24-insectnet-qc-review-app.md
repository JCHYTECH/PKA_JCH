---
date: 2026-05-24
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-05-24 — insectnet-qc-review-app

## Session — 21:34 — insectnet-qc-review-app

### Contexte
- Modèle : [[Codex]]
- Projet : WILDNEXUS

### Résumé
Creation d'une application HTML autonome de revue QC InsectNet pour inspecter spectrogrammes et audio, marquer keep/reject/review, puis exporter un CSV mis a jour.

### Actions
Ajout de scripts/insectnet_qc_review_app.py; ajout de tests/test_insectnet_qc_review_app.py; generation de INSECTNET/04_PIPELINE/insectnet-qc-review.html avec 559 segments integres; ouverture locale de la page; creation du log qc-review-app-log.md.

### Décisions
Ne pas ecraser segment_qc.csv automatiquement depuis le navigateur; exporter segment_qc_reviewed.csv puis remplacer intentionnellement le CSV apres inspection; commencer la revue par Gryllus, Tettigonia et Roeseliana.

### Prochaines étapes
JCH utilise la page QC pour marquer keep/reject/review; importer ensuite le CSV exporte; regenerer train-test-split.csv; lancer la baseline seulement apres avoir 20-40 keep par espece.
