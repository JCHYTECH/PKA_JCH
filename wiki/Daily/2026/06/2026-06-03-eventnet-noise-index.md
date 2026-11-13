---
date: 2026-06-03
tags: [daily, WILDNEXUS, EventNET, bioacoustics]
type: daily
status: active
---

# 2026-06-03 — EventNET noise index

## Session

### Contexte
- Projet : [[WildNexus]] / [[EventNET]]
- Objectif : transformer la detection de bruit anthropique en indice de pollution sonore wildlife sur le [[Raspberry Pi]] BirdNET-Pi.

### Actions
- Ajout taxonomie YAMNet groupee `weather` / `anthropic`.
- Ajout migration SQLite `event_group` et table `noise_index`.
- Ajout indice 0-100 par fenetre de 15 minutes.
- Dashboard PHP enrichi avec indice courant et groupes.

### Decisions
- L'indice est un proxy non calibre, pas une mesure dB SPL ou LAeq.
- L'ESP32 / Satellite Lite P0 n'est pas modifie.
- Les detections BirdNET ne sont pas invalidees automatiquement en V1.

### Verification
- `python3 -m pytest tests/test_eventnet_noise_index.py -q`
- `php -l scripts/eventnet.php` : a executer sur le RPi, PHP n'est pas installe sur le Mac.

## Voir aussi

- [[WILDNEXUS_P0_SCOPE_LOCK]]
- [[ADR-007-detection-evenementielle-p0]]
- [[2026-05-30-session-deepseek-eventnet-wildnexus]]
