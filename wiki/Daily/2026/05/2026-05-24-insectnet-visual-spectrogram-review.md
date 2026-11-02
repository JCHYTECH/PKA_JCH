---
date: 2026-05-24
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-05-24 — insectnet-visual-spectrogram-review

## Session — 20:07 — insectnet-visual-spectrogram-review

### Contexte
- Modèle : [[Codex]]
- Projet : WILDNEXUS

### Résumé
Revue visuelle des 5 planches de spectrogrammes InsectNet V0.1 effectuee: Gryllus, Tettigonia et Roeseliana sont les meilleurs candidats core; Leptophyes et Pholidoptera restent exploitables mais demandent un QC segment plus strict.

### Actions
Inspection des contact sheets par espece; creation de visual-spectrogram-review-v0.1.md; identification des risques de leakage par segments adjacents, imbalance de classes et segments faibles.

### Décisions
Ne pas entrainer de modele tout de suite; imposer un split train/test groupe par recording_id; creer un segment_qc.csv avant baseline; equilibrer ou capper les segments par classe.

### Prochaines étapes
Creer segment_qc.csv depuis segments-manifest.csv et spectrogram-manifest.csv; marquer keep/review/reject; selectionner au moins 20 segments propres par espece; ensuite preparer le split grouped train/test.
