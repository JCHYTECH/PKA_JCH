---
date: 2026-05-25
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-05-25 — Diagnostic [[BirdNET]] et Consolidation Skills

## Session — 10:49 — Diagnostic [[BirdNET]] et Consolidation Skills

### Contexte
- Modèle : Gemini 2.0 Pro
- Projet : WILDNEXUS / ARTEON

### Résumé
Réparation de la base [[BirdNET]] sur le RPi, création de SOP-005 pour le terrain, et mise en place de deux nouvelles skills consolidées (Brand Identity et WildNexus Governance). Maintenance système complète effectuée.

### Actions
- Réparation SQL 'Database is busy' sur RPi (mode WAL activé)\n- Création SOP-005 (Check-list terrain)\n- Création scripts/birdnet_check.sh sur RPi\n- Création skill pka-brand-identity (Arteon/WildLens/L'Instant Lu)\n- Création skill wildnexus-governance (Scope P0)\n- Correction permissions logs et credentials\n- Backup team.db et suppression drift root

### Décisions
- Activation mode WAL sur [[BirdNET]] RPi par défaut\n- Adoption du principe 'Satellite-Lite' comme contrainte skill WildNexus\n- Verrouillage charte Arteon via skill

### Prochaines étapes
- Tester le RPi sur le terrain avec la SOP-005 et une batterie PD\n- Déployer les premières maquettes L'Instant Lu avec la nouvelle skill brand-identity
