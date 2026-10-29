---
date: 2026-06-01
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-06-01 — Achat capteur lux Aqara T1

## Session — 22:55 — Achat capteur lux Aqara T1

### Contexte
- Modèle : codex
- Projet : WILDNEXUS

### Résumé
JCH a validé l'achat d'un capteur Aqara Light Sensor T1 / GZCGQ11LM via AliExpress, environ 20 euros, pour mesurer la luminosité réelle en lux comme variable complémentaire lever/coucher du soleil et nébulosité. Le choix Ecowitt WS90 a été abandonné pour ce besoin car trop volumineux et peu compatible avec l'esprit WildNexus léger.

### Actions
Comparaison conceptuelle Hue Outdoor / Ecowitt WS90 / Aqara T1 / ESPHome BH1750-VEML7700. Recentrage sur une solution compacte Nexus-compatible. Achat confirmé par JCH sur AliExpress.

### Décisions
Capteur lux retenu : Aqara Light Sensor T1, petit capteur Zigbee lux jusqu'à environ 83 000 lx, à intégrer dans Home Assistant puis utiliser pour un Light Context Index WildNexus. Positionnement prévu : sous abri ou emplacement protégé, pas exposition extérieure brute.

### Prochaines étapes
À réception : appairer le capteur Aqara dans Home Assistant via ZHA ou Zigbee2MQTT selon coordinateur disponible; nommer l'entité sensor.base_nexus_lux ou équivalent; enregistrer 7 jours de courbe lux; définir seuils Light Context Index pour BirdNET/EventNET.
