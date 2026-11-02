---
date: 2026-05-30
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-05-30 — session-deepseek-eventnet-wildnexus

## Session — 12:11 — session-deepseek-eventnet-wildnexus

### Contexte
- Modèle : deepseek
- Projet : WILDNEXUS

### Résumé
Session DeepSeek TUI v0.8.39. Installation d'EventNET sur le RPi BirdNET-Pi : YAMNet TFLite en parallèle pour détection acoustique météo (orage, pluie, vent, tonnerre). Service systemd eventnet.service + dashboard PHP auto-rafraîchissant. Premières détections confirmées pendant un orage en cours.

### Actions
Téléchargé YAMNet TFLite et class map AudioSet (521 classes) sur le RPi. Écrit eventnet_detect.py avec inotify pour capture immédiate des WAV BirdNET. Corrigé reshape tensor et input fixe 15600 samples. Créé service systemd eventnet.service (démarrage auto). Créé dashboard PHP eventnet.php servi par Caddy sur le port 80. Fichiers locaux : scripts/eventnet_detect.py, scripts/eventnet.php, scripts/eventnet.service.

### Décisions
Seuil YAMNet fixé à 0.15. 6 classes météo surveillées. Architecture : inotify sur StreamData/ → YAMNet chunk 0.975s → events.db. Dashboard PHP accessible via Tailscale partout.

### Prochaines étapes
Surveiller les détections pendant le prochain orage. Ajuster le seuil si trop/pas assez de faux positifs. Envisager un graphique temporel dans le dashboard.
