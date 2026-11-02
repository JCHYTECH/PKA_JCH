---
date: 2026-05-25
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-05-25 — Bioacoustics skill created

## Session — 09:53 — Bioacoustics skill created

### Contexte
- Modèle : [[Codex]] CLI / GPT-5
- Projet : WILDNEXUS

### Résumé
Création de la skill bioacoustics-qc-playbook pour pérenniser le workflow QC InsectNet/bioacoustique. L'agent dédié est différé; le mapping WildNexus existant reste le point d'ancrage.

### Actions
- Skill auto-discoverable créée dans ~/.[[Codex]]/skills/bioacoustics-qc-playbook.\n- Reference file added with the 28 kHz audible-list rule and QC conventions.\n- openai.yaml metadata fixed and skill validated successfully.

### Décisions
La skill est le bon niveau de capture procédurale pour l'instant. Un agent spécialisé n'est pas nécessaire tant que le flux reste occasionnel et rattaché à wildnexus-bioacoustics-dsp.

### Prochaines étapes
Réutiliser la skill sur les prochains lots bioacoustiques; créer un agent seulement si le volume ou la fréquence d'analyse devient récurrente.
