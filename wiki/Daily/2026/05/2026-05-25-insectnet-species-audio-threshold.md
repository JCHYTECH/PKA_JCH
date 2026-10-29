---
date: 2026-05-25
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-05-25 — InsectNet species audio threshold

## Session — 09:46 — InsectNet species audio threshold

### Contexte
- Modèle : [[Codex]] CLI / GPT-5
- Projet : WILDNEXUS

### Résumé
Ajout d'un registre audio par espece dans l'auto-QC avec seuil median a 28 kHz. Aucune des 5 especes V0.1 ne depasse le seuil; elles restent toutes dans la liste audible.

### Actions
- scripts/insectnet_auto_qc.py calcule un profil audio par espece.\n- segment_qc_auto.csv a ete enrichi avec species_audio_* sur chaque ligne.\n- species_audio_profile.csv a ete genere pour la synthese.\n- Les vues QC affichent maintenant aussi le statut audio d'espece.

### Décisions
La regle operative est mediane dominante > 28 kHz => exclusion de la liste audible. Avec les donnees actuelles, aucune espece n'est retiree.

### Prochaines étapes
Utiliser species_audio_profile.csv pour filtrer plus vite les futures especes candidates et garder la liste audible sous controle.
