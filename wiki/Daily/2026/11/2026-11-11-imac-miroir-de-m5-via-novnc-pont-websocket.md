---
date: 2026-11-11
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-11-11 — iMac miroir de M5 via noVNC (pont WebSocket)

## Session — 23:34 — iMac miroir de M5 via noVNC (pont WebSocket)

### Contexte
- Modèle : deepseek-v4-pro
- Projet : 01_AI_IT_TOOLS

### Résumé
L'iMac 27 Retina 5K 2017 affiche l'écran du M5 en miroir via un pont noVNC. Constats matériels : l'iMac 2017 n'est pas éligible AirPlay Receiver (Apple supporte iMac 2019+), et le partage d'écran Apple Ventura↔macOS 26 est incompatible (l'app Apple se bloque sur l'auth Apple sans basculer sur VNC). Solution : websockify + noVNC 1.7.0 sur le M5 (launchd com.dobby.m5-vnc-novnc, port 6080), accès Safari sur l'iMac. Correctif noVNC : retrait du type ARD pour forcer l'auth VNC standard. SSH activé sur l'iMac pour injection future.

### Actions
- Diagnostiqué l'éligibilité AirPlay de l'iMac 2017 (non supporté, matériel).
- Activé le partage d'écran du M5 via kickstart (Remote Management + VNC legacy).
- Installé websockify (pip) + cloné noVNC 1.7.0 (local/novnc).
- Créé le plist launchd com.dobby.m5-vnc-novnc (RunAtLoad + KeepAlive).
- Patché noVNC (core/rfb.js) : retiré securityTypeARD → auth VNC standard.
- Injecté l'URL dans Safari iMac via SSH + osascript (open seul affiche la page par défaut).
- Corrigé le .vncloc (IP .14 morte → nom Bonjour MacBook-Pro-de-JC.local).

### Décisions
- noVNC navigateur plutôt que RealVNC : zéro install sur l'iMac, survit aux rallumages et à l'effacement.
- Nom Bonjour plutôt qu'IP brute (l'IP avait changé .14→.56).
- Remote Management + VNC legacy (le VNC simple seul ne s'authentifiait pas).

### Prochaines étapes
- (Optionnel) Remplacer le mot de passe VNC (actuellement l'admin) par un mot de passe dédié.
- À chaque besoin : « ouvre le miroir sur l'iMac » (injection via SSH).
