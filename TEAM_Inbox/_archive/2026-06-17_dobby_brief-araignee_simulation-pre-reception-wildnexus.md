# Brief — [[Araignée]] 🕷️ : Simulation pré-réception WildNexus

**Date :** 2026-06-17  
**Émis par :** [[Dobby]]  
**Deadline :** 2026-06-28 (2 semaines)  
**Priorité :** P0 — débloque le travail pendant l'attente du hardware  

## Contexte

Les composants WildNexus sont en transit (OV5640 NoIR ~15-25j AliExpress, NULA DeepSleep ~début juillet). Pour ne pas perdre 3-4 semaines, on maximise le travail in silico. On a déjà Wokwi pour les smoke tests. Deux nouveaux outils viennent d'être identifiés.

## Missions

### 1. Porter le smoke test Wokwi → Cirkit Designer
- Cirkit est un simulateur ESP32-S3 **instruction-accurate** (Rust/WASM, mai 2026)
- Il exécute du vrai firmware Xtensa, boot ROM Espressif incluse
- Supporte WiFi réel (HTTP, MQTT, WebSocket)
- **Action :** Reproduire le smoke test actuel (`03_P0_ENGINEERING/05_SIMULATION/wokwi/`) dans Cirkit Designer. Comparer les résultats.
- **Livrable :** `03_P0_ENGINEERING/05_SIMULATION/cirkit/smoke-test.md` + lien projet Cirkit

### 2. Simuler le protocole LoRaWAN
- IoT Virtual Lab : https://virtual-labs.github.io/exp-lorawan-dei/simulation/index.html
- Permet de configurer device ESP32 + paramètres LoRaWAN réels (SF, bandwidth, coding rate)
- **Action :** Modéliser un nœud WildNexus type (ESP32-S3 + capteurs → LoRaWAN), tester les paramètres de transmission, documenter la config optimale
- **Livrable :** `03_P0_ENGINEERING/05_SIMULATION/lorawan/simulation-config.md`

### 3. (Bonus) Évaluer CupCarbon pour le digital twin
- CupCarbon : modélisation de réseau de capteurs avec MQTT
- **Action :** Évaluer si l'outil peut modéliser un déploiement multi-nœuds WildNexus

## Références
- `docs/system/pka-memory-layer.md`
- `03_P0_ENGINEERING/05_SIMULATION/wokwi/` — smoke test existant
- `03_P0_ENGINEERING/PROTOCOLES/2026-06-08_protocole-m02-esp32s3-ppk2.md`
