# Brief — [[Forge]] 🦦 : Firmware WiFi/MQTT + Test Harness Caméra

**Date :** 2026-06-17  
**Émis par :** [[Dobby]]  
**Deadline :** 2026-06-28 (2 semaines)  
**Priorité :** P0 — livrables bloquants pour l'intégration  

## Contexte

Les composants WildNexus arrivent progressivement. L'OV2640 (ESP32-CAM) est déjà reçue (~10€). L'OV5640 NoIR arrivera fin juin/début juillet. Le NULA DeepSleep ESP32-S3 arrivera début juillet. Pour maximiser le temps avant réception, on développe et teste en simulation.

## Missions

### 1. Firmware de transmission WiFi/MQTT
- Cirkit Designer (https://www.cirkitdesigner.com) supporte le WiFi réel sur ESP32-S3 : HTTP, HTTPS, MQTT, WebSocket, UDP
- **Action :** Développer le firmware qui lit les données capteurs (BME688, SHT31 simulés en I2C) → formate en JSON → publie via MQTT
- **Test :** Dans Cirkit Designer, avec un broker MQTT public (test.mosquitto.org)
- **Livrable :** `03_P0_ENGINEERING/04_FIRMWARE/mqtt-transmitter/` + rapport de test Cirkit

### 2. Test harness caméra (rappel deadline 21 juin)
- Approche découplée : lire des images SD → exécuter l'inférence → benchmark
- L'ESP32-CAM OV2640 déjà reçue peut fournir des images de test réelles
- **Action :** Finaliser le test harness. Objectif : 1 cycle complet (capture → stockage SD → inférence → rapport) fonctionnel
- **Livrable :** `03_P0_ENGINEERING/05_SIMULATION/camera-harness/` + benchmark

### 3. (Bonus) Préparer l'intégration BME688 + SHT31
- Les capteurs sont commandés (Mouser #39492997, reçu ?)
- **Action :** Écrire le driver I2C pour BME688 (gas/humidity/pressure/temp) et SHT31, testable dans Wokwi ou Cirkit
- **Livrable :** `03_P0_ENGINEERING/04_FIRMWARE/drivers/bme688/` + `sht31/`

## Quality Gate
- `auto_review: true`
- `review_threshold: 4`
- `max_iterations: 3`

## Références
- `03_P0_ENGINEERING/05_SIMULATION/wokwi/` — smoke test existant
- `03_P0_ENGINEERING/PROTOCOLES/2026-06-08_protocole-m02-esp32s3-ppk2.md`
- `TEAM_Inbox/2026-06-14_dobby_brief-forge-nova_test-harness-camera.md` — brief précédent
- Cirkit Designer ESP32-S3 docs : https://www.cirkitdesigner.com/blog/2026-05-05-esp32-s3-simulator
