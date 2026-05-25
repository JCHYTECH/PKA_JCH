---
date: 2026-05-25
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-05-25 — InsectNet audio-band preview

## Session — 09:28 — InsectNet audio-band preview

### Contexte
- Modèle : Codex CLI / GPT-5
- Projet : WILDNEXUS

### Résumé
Ajout d'un tag audio non-humain dans l'auto-QC et d'un mode de pré-écoute ralentie dans l'app QC.

### Actions
- scripts/insectnet_auto_qc.py: analyse audio et classification en ultrasonic/audible/mixed.\n- scripts/insectnet_qc_review_app.py: filtre par bande audio et selecteur de preview mode.\n- tests/test_insectnet_auto_qc.py et tests/test_insectnet_qc_review_app.py mis à jour et passants.\n- segment_qc_auto.csv et insectnet-qc-review.html régénérés.

### Décisions
Le tag audio n'écrase pas la QC humaine; il sert au filtrage et à la priorisation. La pré-écoute utilise une réduction de vitesse pour rendre les fichiers ultrasoniques plus audibles.

### Prochaines étapes
Faire écouter les cas Leptophyes punctatissima avec le mode 0.25x ou 0.5x et décider quels segments restent keep/reject.
