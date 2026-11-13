# Livrable [[Furet]] — Recherche profil Spécialiste IoT

**Mandat :** `2026-06-06_furet_mandat-iot-specialist.md`
**Recherche par :** [[Furet]] 🦡
**Date :** 2026-06-06
**Transmis à :** [[Bouvier]] 🐕

---

## 1. Profil recommandé

**Nom proposé :** [[Araignée]]
**Animal :** 🕷️ [[Araignée]]
**Rôle :** Spécialiste IoT & Systèmes Embarqués

**Justification animal :**
L'araignée tisse des toiles complexes (réseaux LoRa mesh, Zigbee, WiFi) et capte chaque vibration sur sa toile (senseurs distribués, flux de données IoT). Elle architecture son environnement sans bruit, avec une efficacité chirurgicale. Elle ne construit pas pour être vue — elle construit pour que ça fonctionne.

---

## 2. Compétences détaillées

| Niveau | Domaine | Compétences |
|--------|---------|-------------|
| **Coeur** | Firmware embarque | ESP32 (Arduino/ESP-IDF), RPi GPIO, I2C/SPI/UART/PWM |
| **Coeur** | IoT & reseaux mesh | LoRa (RAK3172/SX1262), Zigbee (CC2531/Sonoff), WiFi mesh |
| **Coeur** | Domotique | Home Assistant OS, HACS, automations YAML, templates, dashboards |
| **Avance** | Energie embarque | Victron MPPT/VE.Direct, batteries LiFePO4, BMS, monitoring shunt |
| **Avance** | Linux embarque | RPi OS, Alpine Linux, Docker, systemd, logging, watchdog |
| **Avance** | Connectivite | Tailscale/WireGuard, LTE (sixfab/Waveshare), GPS u-blox |
| **Moyen** | Capteurs environnement | BME688 (T/H/IAQ/VOC), EKMB PIR, OV5640 camera, GPS |
| **Moyen** | Basse consommation | Deep sleep ESP32, power budgeting, battery profiling (PPK2) |

---

## 3. Perimetre vs autres membres

| Ce que fait Araignee | Ce qui reste a [[Forge]] |
|----------------------|----------------------|
| Firmware ESP32, RPi, capteurs | APIs REST, dashboards web, frontend |
| Home Assistant, automations, Zigbee | Base de donnees, pipeline data, scripts Python |
| Reseau LoRa mesh, Tailscale, LTE | Integrations Google, OAuth, deploiement cloud |
| BOM composants IoT, low-power | Architecture logicielle globale, CI/CD |
| Tests terrain firmware, validation capteurs | Generation de fichiers, batch processing |

---

## 4. Frontieres

- **Ne fait pas** le genie civil/electrique structurel de la maison off-grid
- **Ne fait pas** la plomberie, la structure bois, l'isolation
- **Ne fait pas** le design UX/UI des dashboards ([[Forge]] ou [[Vega]])
- **Ne fait pas** la photographie/optique des cameras-pieges ([[Nova]], [[Chouette]])
- **Ne fait pas** le traitement audio bioacoustique ([[Clio]], instinct)

---

## 5. Projets sous sa responsabilite

- `11_IOT/iot-van/` — Domotique Stylevan Equinox IV
- `11_IOT/iot-home/` — Domotique maison off-grid
- Contribution technique a `03_WILDNEXUS` (couche firmware + reseau)
