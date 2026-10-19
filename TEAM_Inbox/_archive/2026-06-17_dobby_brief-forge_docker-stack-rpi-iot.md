# Brief — [[Forge]] 🦦 : Docker Stack RPi IoT — Pré-déploiement

**Date :** 2026-06-17  
**Émis par :** [[Dobby]]  
**Deadline :** 2026-06-28 (2 semaines)  
**Priorité :** P0 — déploiement RPi Belgique bloqué par la config logicielle  

## Contexte

Le RPi 5 4GB est reçu (10 juin). SSD, alim, boîtier, ZBDongle-E sont là. La stack Docker (HA + Mosquitto + Zigbee2MQTT) tourne déjà sur M5 — il faut l'adapter et la packager pour le RPi.

PI-CI (https://github.com/ptrsr/pi-ci) permet d'émuler un RPi 5 dans Docker, de tester la config, puis de flasher l'image SD.

## Missions

### 1. Adapter le docker-compose M5 → RPi ARM64
- Le `docker-compose.yml` M5 (`_local/` + conteneurs Docker existants) doit être adapté pour ARM64
- Inclure : Home Assistant, Mosquitto, Zigbee2MQTT
- Appliquer `--restart unless-stopped` (leçon du 16 juin)
- **Livrable :** `JCH_Inbox/03_PROJECTS/11_IOT/rpi-belgique/docker-compose.yml`

### 2. Tester dans PI-CI
- PI-CI : `docker run -it ptrsr/pi-ci` émule un RPi 5
- Déployer le docker-compose dans l'émulateur
- Vérifier : HA accessible, Mosquitto publie, Zigbee2MQTT écoute (même sans dongle)
- **Livrable :** `JCH_Inbox/03_PROJECTS/11_IOT/rpi-belgique/pi-ci-test-report.md`

### 3. Adapter le script d'installation
- `_local/install-zigbee-ha.sh` est déjà écrit pour le M5
- L'adapter pour RPi : chemins de ports série (`/dev/serial/by-id/...`), architecture ARM64
- **Livrable :** `JCH_Inbox/03_PROJECTS/11_IOT/rpi-belgique/install-rpi.sh`

### 4. (Bonus) Préparer la config Van offline
- Le van doit fonctionner sans internet (alarme portes, frigo)
- Préparer un `docker-compose-van.yml` avec les services essentiels uniquement
- Tester dans PI-CI en mode offline
- **Livrable :** `JCH_Inbox/03_PROJECTS/11_IOT/iot-van/docker-compose-van.yml`

## Quality Gate
- `auto_review: true`
- `review_threshold: 4`
- `max_iterations: 3`

## Références
- `_local/install-zigbee-ha.sh` — script M5 existant
- `_local/homeassistant/` — config HA actuelle
- `docs/system/station-domotique-plan-rpi5.md` — plan RPi5
- `MEMORY.md` — section architecture distribuée (13 juin)
- `docker update --restart unless-stopped` — leçon Docker du 16 juin
