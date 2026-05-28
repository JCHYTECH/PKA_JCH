---
date: 2026-05-24
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-05-24 — insectnet-qc-app-auto-filter

## Session — 21:59 — insectnet-qc-app-auto-filter

### Contexte
- Modèle : [[Codex]]
- Projet : WILDNEXUS

### Résumé
Ajout d'un filtre Auto suggestion dans l'application QC InsectNet pour isoler les auto_reject_candidate, auto_keep_candidate, human_review ou les segments sans suggestion.

### Actions
Modification de scripts/insectnet_qc_review_app.py; mise a jour du test test_insectnet_qc_review_app.py; regeneration de insectnet-qc-review.html depuis segment_qc_auto.csv; ouverture locale de la page.

### Décisions
Les auto_reject_candidate peuvent maintenant etre filtres directement dans l'interface, mais restent des suggestions a verifier avant reject humain.

### Prochaines étapes
Dans l'app, choisir Auto suggestion > Auto rejects pour voir les 21 candidats rejet; valider ou corriger manuellement; exporter ensuite segment_qc_reviewed.csv.
