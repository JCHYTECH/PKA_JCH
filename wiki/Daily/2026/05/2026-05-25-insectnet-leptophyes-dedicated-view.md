---
date: 2026-05-25
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-05-25 — InsectNet Leptophyes dedicated view

## Session — 09:34 — InsectNet Leptophyes dedicated view

### Contexte
- Modèle : [[Codex]] CLI / GPT-5
- Projet : WILDNEXUS

### Résumé
Création d'une vue QC dédiée à Leptophyes punctatissima, filtrée et triée pour la revue rapide des enregistrements difficiles à entendre.

### Actions
- scripts/insectnet_qc_review_app.py accepte maintenant --species et --preview-rate.\n- Une vue dédiée a été générée pour Leptophyes punctatissima avec pré-écoute 0.25x.\n- Les tests QC passent après ajout du filtrage/sortie dédiée.

### Décisions
La vue dédiée conserve l'app QC générale mais ne charge qu'une seule espèce pour réduire le bruit visuel et accélérer la décision humaine.

### Prochaines étapes
Utiliser la vue dédiée pour marquer keep/reject sur les segments les plus nets, puis régénérer le split si besoin.
