---
date: 2026-05-24
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-05-24 — insectnet-spectrograms-contact-sheets

## Session — 20:04 — insectnet-spectrograms-contact-sheets

### Contexte
- Modèle : codex
- Projet : WILDNEXUS

### Résumé
InsectNet V0.1 a genere 559 spectrogrammes PNG 1024x512 depuis les segments audio et 5 planches de controle par espece.

### Actions
Creation de scripts/insectnet_generate_spectrograms.py et scripts/insectnet_contact_sheets.py; ajout des tests pytest associes; generation de spectrogram-manifest.csv; generation des PNG dans spectrograms; generation des contact sheets par espece; mise a jour du log pipeline audio-qc-segmentation-log.md.

### Décisions
Utiliser ffmpeg showspectrumpic avec legend=disabled pour produire des spectrogrammes stricts 1024x512; conserver Pillow uniquement pour assembler les planches de controle; ne pas entrainer de classifieur avant revue visuelle des planches.

### Prochaines étapes
Inspecter les 5 planches de controle; marquer les segments bruit/sature/faible signal; definir ensuite le split train/test et la baseline CNN spectrogrammes.
