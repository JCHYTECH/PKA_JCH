---
date: 2026-05-30
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-05-30 — session-deepseek-homeassistant-mac

## Session — 15:27 — session-deepseek-homeassistant-mac

### Contexte
- Modèle : deepseek
- Projet : AI_IT_TOOLS

### Résumé
Session DeepSeek TUI v0.8.39. Installation Home Assistant Container Docker sur Mac M5. Accès distant via Tailscale confirmé (100.108.55.44:8123). Documentation dans MEMORY.md.

### Actions
Vérifié Docker (29.4.3) et ressources Mac (M5, 16GB, 409GB libre). Pull image ghcr.io/home-assistant/home-assistant:stable. Lancé container avec restart=unless-stopped, config dans _local/homeassistant/. Vérifié accès localhost:8123 + accès distant via IP Tailscale 100.108.55.44:8123. Mis à jour MEMORY.md (date, projet actif, décision structurelle).

### Décisions
Home Assistant en Container Docker sur Mac — pas sur le RPi (réservé BirdNET/EventNET). Config stockée dans PKA_JCH/_local/homeassistant/. Accès distant via Tailscale existant, pas besoin de container séparé.

### Prochaines étapes
JCH doit terminer le wizard de configuration Home Assistant. Ensuite : intégrations domotiques.
