---
date: 2026-05-29
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-05-29 — -e RPI BirdNET mobile — stabilisation DB et config

## Session — 09:08 — -e RPI BirdNET mobile — stabilisation DB et config

### Contexte
- Modèle : deepseek
- Projet : Diagnostic et correction des conflits WAL SQLite entre jchavaux et caddy sur le RPi BirdNET-Pi. Fixes appliqués : User=caddy, HOME=/home/jchavaux, UMask=0002, ExecStartPre checks, CONFIDENCE 0.6, Wi-Fi autoconnect OFF, coordonnées GPS corrigées. BirdSongs/ passé en jchavaux:caddy setgid. Détections stables sans erreurs.

### Résumé
Actions :
- Override systemd birdnet_analysis.service (User=caddy + Environment=HOME + ExecStartPre)
- chown -R jchavaux:caddy /home/jchavaux/BirdSongs/
- CONFIDENCE 0.25 → 0.6 dans birdnet.conf
- Coordonnées 51.1904/4.4294 → 50.55/5.57
- nmcli device set wlan0 autoconnect no
- Prochaine étape : câble USB-C PD pour test terrain 24h
