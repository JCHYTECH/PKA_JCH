```yaml
---
date: 2026-05-24
author: Sybil
type: journal
status: automatique
---
```

# 24 mai 2026

## Modifications système et infrastructure

Deux scripts utilitaires ont été modifiés : `bin/pka` et `bin/pka-save`. Ce dernier a également fait l'objet de tests spécifiques (`tests/test_pka_save_shortcut.py` et `tests/test_pka_save.py`), suggérant une amélioration ou une correction du système de sauvegarde rapide.

La mémoire partagée (`MEMORY.md`) a été mise à jour, probablement pour refléter l'état courant des projets en cours.

## Travaux InsectNet

### Segmentation et qualité

Trois domaines ont reçu attention :

- **Segmentation audio** : modifications du code de segmentation avec tests associés (`test_insectnet_segment_audio.py`)
- **Contrôle qualité segmenté** : développement ou amélioration du workflow QC pour segments (`test_insectnet_segment_qc.py`, `wiki/Daily/2026/05/2026-05-24-insectnet-segment-qc-grouped-split.md`)
- **Split groupé** : implémentation de logique de regroupement-division avec tests (`test_insectnet_grouped_split.py`)

### Spectrogrammes et visualisation

La création de spectrogrammes et de planches de contact a été documentée (`test_insectnet_spectrograms.py`, `wiki/Daily/2026/05/2026-05-24-insectnet-spectrograms-contact-sheets.md`). Un workflow de revue visuelle des spectrogrammes a également été enregistré (`wiki/Daily/2026/05/2026-05-24-insectnet-visual-spectrogram-review.md`).

### Application de contrôle qualité

L'application QC a bénéficié de développements : auto-filtrage (`wiki/Daily/2026/05/2026-05-24-insectnet-qc-app-auto-filter.md`) et possibilité de revue interactive (`test_insectnet_qc_review_app.py`).

### Gestion des données

Trois modules de gestion des données audio ont été testés :
- Sélection de candidats audio (`test_insectnet_select_audio_candidates.py`)
- Inventaire audio (`test_insectnet_audio_inventory.py`)
- Téléchargement audio (`test_insectnet_download_audio.py`)

Les métadonnées XenoCanto ont été traitées (`test_insectnet_xc_metadata.py`).

## Documentation et spécifications

Deux documents de planification et conception ont été créés pour la segmentation QC InsectNet :
- Plan d'exécution (`docs/superpowers/plans/2026-05-24-insectnet-qc-segmentation.md`)
- Spécification de conception (`docs/superpowers/specs/2026-05-24-insectnet-qc-segmentation-design.md`)

## Rapports et suivi

- Rapport hebdomadaire Dobby/JCH généré (`wiki/Daily/2026/05/2026-05-24-dobby-jch-rapport-hebdo.md`)
- Vérification système Dobby documentée (`TEAM_Inbox/2026-05-24_dobby_system_check.md`)
- Mise à jour du journal wiki (`wiki/log.md`) et index (`wiki/index.md`)

## BirdNet et infrastructure réseau

Travaux de connexion du Raspberry Pi BirdNet au réseau Tailnet (`wiki/Daily/2026/05/2026-05-24-birdnet-rpi-connexion-tailnet.md`).

## Maintenance et logs

Un log d'auto-démarrage plane a été enregistré (`tmp/plane-autostart.log`). Un SOP terrain bioacoustique a été mis à jour (`wiki/SOPs/SOP-005-checklist-terrain-bioacoustique.md`).