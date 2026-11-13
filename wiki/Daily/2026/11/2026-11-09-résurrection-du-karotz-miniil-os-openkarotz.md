---
date: 2026-11-09
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-11-09 — Résurrection du Karotz (miniil OS + OpenKarotz)

## Session — 23:55 — Résurrection du Karotz (miniil OS + OpenKarotz)

### Contexte
- Modèle : deepseek-v4-pro
- Projet : 11_IOT

### Résumé
Karotz (lapin Violet) ressuscité : WiFi WPA/TKIP sur RUT240 dédié, flash miniil Karotz OS, correctif serveur web (inetd), installation OpenKarotz. LED verte, interface web opérationnelle sur http://192.168.129.250.

### Actions
Configuration RUT240 (SSID Karotz, WPA/TKIP, mode 11g) · flash firmware miniil via clé USB · diagnostic de 6 pannes (WPA2 refusé, 11n invisible, clé restée branchée, serveur web bloqué, firmware corrompu, route RUT240) · correctif inetd dans waitfornetwork.sh · installation OpenKarotz · fichier synthèse resurrection-karotz-2026-11-09.md.

### Décisions
WPA/TKIP (pas WPA2 seul) · mode 802.11g · retirer la clé USB après flash · lancer inetd directement dans waitfornetwork.sh pour contourner le blocage dbus · re-flash pour corriger la corruption firmware.

### Prochaines étapes
Intégration Home Assistant (Dobby comme cerveau vs IA-HA) · documenter une procédure générique pour dautres jouets (Cozmo) · ne pas laisser la clé USB dans le lapin.
