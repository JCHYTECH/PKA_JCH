---
date: 2026-11-10
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-11-10 — Surveillance box Proximus + RPi Lupo et Home

## Session — 23:06 — Surveillance box Proximus + RPi Lupo et Home

### Contexte
- Modèle : deepseek-v4-pro
- Projet : 11_IOT

### Résumé
Session IOT. Routage des achats Lupo (suspension VB Air, douche interieure) vers 07_TRAVELS et analyse du transcript MCP Home Assistant. Surveillance ping box Proximus (15 min, stable) puis automatisation via pka-watch-box (launchd 08h/11h, mail si anomalie). Verification RPi Lupo : en ligne, sous-tension non active, alerte Under-voltage acquittee. RPi Home non joignable : HAOS non boote, diagnostic physique a prevoir.

### Actions
- Route et indexe 2 PDF achats Lupo (07_TRAVELS/Lupo/van technique/achats/)
- Analyse et route transcript NoteGPT MCP HA (11_IOT/iot-van/99_REFERENCES/claude-ha-mcp_2026-11-10/)
- Efface doublons inbox (DNG + transcript teles)
- Surveillance ping box Proximus 15 min : 0 coupure, latence WAN 28 ms
- Cree bin/pka-watch-box + scripts/box_monitor.py + LaunchAgent (08:00/11:00, mail si anomalie)
- Verifie RPi Lupo (MCP HA + Playwright) : ping OK, sous-tension off, alerte acquittee (Repairs vide)
- Diagnostique RPi Home : non joignable (mDNS, scan IP/MAC, Tailscale, ports 8123/22 fermes)

### Décisions
- Mail de surveillance box uniquement si anomalie (pas de spam quotidien)
- Horaires de surveillance box : 08:00 et 11:00
- Alerte sous-tension Lupo historique (mois dernier), acquittee apres confirmation etat off

### Prochaines étapes
- RPi Home : diagnostic physique (alimentation/LED, microSD flash rpi5-64, Ethernet) puis probable re-flash HAOS
- Box Proximus : relever 1 h sur fenetre de pointe (matin) pour capturer l episode
- Lupo : surveiller binary_sensor.raspberry_pi_power_status (rester off)
