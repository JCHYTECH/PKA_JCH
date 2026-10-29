---
date: 2026-07-09
project: 11_IOT
type: session-summary
model: deepseek-v4
---

# Session 2026-07-09 — Analyse & intégration OBD/CAN bus Transit Custom

## Résumé

Analyse approfondie de l'apport du bus CAN (OBD-II) du Ford Transit Custom 170CV 4x4 (Westfalia Kelsey « Lupo ») pour le projet IoT Vanlife. Décision validée par JCH : intégration WiCAN Pro.

## Décisions clés

1. **WiCAN Pro retenu** (~82€) — seul device compatible MS-CAN + HS-CAN avec PIDs Ford Transit prêts
2. **Aqara Zigbee conservés (×9)** — indispensables pour la détection porte temps réel en camping (CAN s'endort après 30-60 min)
3. **TPMS Bluetooth supprimé** (-20€) → BCM pneus ×6 gratuits
4. **BME280 extérieur supprimé** (-5€) → PCM ambient air temp gratuit
5. **GPS rétrogradé P2→P3** — vitesse via CAN, position seule conservée
6. **6 nouveaux scénarios** créés (carburant, conso, DTC, turbo, Webasto, batterie porteur)

## Fichiers modifiés

- ✅ Créé : `iot-van/specs/SPEC-CAN-BUS.md`
- ✅ Mis à jour : `BOM-VANLIFE.md` (v5→6 sections, +82€, -25€)
- ✅ Mis à jour : `scenarios-algorithmes-vanlife.md` (v1.0→v1.1, +section 7 CAN)
- ✅ Mis à jour : `hardware-state.md` (WiCAN Pro ajouté)
- ✅ Mis à jour : `ds300-tap/SPEC-DS300-TAP.md` (impact CAN)
- ✅ Mis à jour : `MEMORY.md` (log session)

## Commandes à passer

| # | Contenu | Montant | Où | Deadline |
|---|---------|---------|-----|----------|
| 1 | Capteurs Zigbee §3.1 (27 items) + Divers §6 | ~282€ | Amazon BE | Cette semaine |
| 2 | WiCAN Pro ×1 | ~82€ | Crowd Supply / Mouser | Cette semaine |
| 3 | SNZB-04P ×2 + INMP441 + Tap composants | ~30€ | ITEAD + AliExpress | Cette semaine |
| 4 | Victron SmartShunt + MPPT | ~210€ | Amazon | Avant départ |

## Briefs spécialistes

### Brief Forge 🦦 — Intégration réseau WiCAN Pro

**Priorité :** P1 | **Deadline :** 17 juillet 2026

Contexte : Le WiCAN Pro est un bridge OBD-II → WiFi/MQTT basé sur ESP32-S3. Il doit être intégré au réseau local du RPi 5 vanlife.

Tâches :
1. Commander WiCAN Pro sur Crowd Supply (~82€)
2. Flasher le dernier firmware stable WiCAN
3. Configurer WiFi : RPi 5 = AP local (HostAPD), WiCAN = client
4. Configurer MQTT broker Mosquitto sur RPi 5
5. Charger le preset PIDs depuis le repo `WiCAN-Ford-Transit`
6. Configurer power saving : sleep <1mA, periodic wake 5 min, low-voltage cutoff 11.8V
7. Valider que les 17+ entités HA remontent dans Home Assistant

Références :
- `iot-van/specs/SPEC-CAN-BUS.md`
- https://github.com/anthonysecco/WiCAN-Ford-Transit
- https://wambs.github.io/wican-fw/how-to-guides/power-management/

### Brief Araignée 🕷️ — Configuration MQTT → HA + automatisations CAN

**Priorité :** P1 | **Deadline :** 24 juillet 2026

Contexte : Les 17+ entités MQTT du WiCAN Pro doivent être intégrées dans Home Assistant et les 6 nouveaux scénarios CAN bus implémentés.

Tâches :
1. Configurer les entités MQTT → HA (templates YAML) pour toutes les données CAN
2. Implémenter les 6 nouveaux scénarios (section 7 de `scenarios-algorithmes-vanlife.md`) :
   - 7.1 Jauge carburant + range anxiety (P1)
   - 7.2 Conso réelle par trajet (P1)
   - 7.3 Diagnostic moteur DTC live (P1)
   - 7.4 Surveillance turbo (P2)
   - 7.5 Préchauffage Webasto intelligent (P2)
   - 7.6 Alerte batterie porteur faible (P2)
3. Mettre à jour les scénarios existants avec les nouvelles entités CAN :
   - 1.1 → `sensor.vehicle_speed` + `sensor.engine_rpm` (triple confirmation)
   - 1.4 → `sensor.vehicle_speed` (remplace GPS)
   - 1.5 → `binary_sensor.door_driver` + `binary_sensor.hood` (backup)
   - 2.2 → `sensor.coolant_temp` (cross-check)
   - 5.1 → enrichi avec fuel_level + coolant_temp + RPM
4. Créer le dashboard Lovelace "Cockpit Vanlife" avec widgets CAN bus

Références :
- `iot-van/specs/SPEC-CAN-BUS.md`
- `iot-van/scenarios-algorithmes-vanlife.md` (section 7)
