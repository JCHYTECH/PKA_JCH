---
date: 2026-11-11
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-11-11 — RPi Home ressuscité + Z2M réinstallé + serre_temp_hum re-appairé

## Session — 16:00 — RPi Home ressuscité + Z2M réinstallé + serre_temp_hum re-appairé

### Contexte
- Modèle : deepseek-v4-pro
- Projet : 11_IOT

### Résumé
RPi Home (JC home) remis en service : HA Core fonctionne sur le port 80 (pas 8123, d'où le faux diagnostic de plantage du 07/11), SSH debug permanent activé (clé USB CONFIG), mot de passe jc réinitialisé. Zigbee2MQTT réinstallé pour débloquer le port série (figé sur ttyACM0 par un bug Supervisor/addon) puis dongle reconnu sur ttyUSB0, MQTT connecté. serre_temp_hum (SNZB-02DR2) re-appairé et renommé, remonte 21.9 C / 59.7 %. En parallèle : surveillance ping box Proximus automatisée.

### Actions
Activation SSH debug RPi Home (clé USB label CONFIG + authorized_keys à la racine) ; réinitialisation mot de passe jc (ha authentication reset) ; diagnostic Core : port 80 (pas 8123), OOMKilled=false, pas de plantage ; réinstallation addon Z2M (uninstall+install) pour vider les options serial/mqtt figées, port lu depuis configuration.yaml (ttyUSB0) ; re-appairage serre_temp_hum (permit join MQTT + bouton 10s) + rename friendly name ; surveillance box Proximus (pka-watch-box + relevé 1h sous caffeinate).

### Décisions
RPi Home reste sur HAOS 18.5 (pas de re-flash 18.3, le plantage était un faux diagnostic de port) ; port 80 conservé (remise à 8123 = option) ; Z2M réinstallé plutôt que bidouille du store apps.json ; serre_temp_hum renommé (friendly name).

### Prochaines étapes
Re-appairer vanne_serre + LuxSerre (permit join + bouton physique) ; confirmer stabilité Core 24h ; option port 80 vers 8123 ; lire le résultat du relevé 1h box Proximus.
