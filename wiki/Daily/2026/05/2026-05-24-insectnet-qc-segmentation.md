---
date: 2026-05-24
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-05-24 — insectnet-qc-segmentation

## Session — 19:54 — insectnet-qc-segmentation

### Contexte
- Modèle : codex
- Projet : WILDNEXUS

### Résumé
InsectNet V0.1 a franchi l'etape QC audio et segmentation: 100 fichiers sources verifies avec ffprobe et 559 segments WAV mono 48 kHz de 3 secondes generes sans erreur.

### Actions
Creation de scripts/insectnet_audio_inventory.py et scripts/insectnet_segment_audio.py; ajout des tests pytest associes; generation de audio-inventory.csv; generation de segments-manifest.csv et du dossier segments; creation du log pipeline audio-qc-segmentation-log.md.

### Décisions
Conserver BirdNET-Pi intact; garder InsectNet comme module separe; ne pas entrainer de modele avant generation et inspection des spectrogrammes.

### Prochaines étapes
Generer les spectrogrammes depuis segments-manifest.csv; produire une planche de controle par espece; valider visuellement un echantillon avant baseline classifier.
