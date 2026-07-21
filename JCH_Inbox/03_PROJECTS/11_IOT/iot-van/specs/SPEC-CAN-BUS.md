# SPEC-CAN-BUS — Interface OBD-II / CAN bus Ford Transit Custom

> **Statut :** SPEC v1.0 — Validé, à implémenter  
> **Date :** 2026-07-09 | **Rédacteur :** [[Dobby]] 🦉  
> **Matériel cible :** Westfalia Kelsey 2026 — Ford Transit Custom 170CV 4x4 (alias « Lupo »)  
> **Hardware :** WiCAN Pro (ESP32-S3 + STN OBD interpreter, MS-CAN + HS-CAN)  
> **Source PIDs :** [WiCAN-Ford-Transit](https://github.com/anthonysecco/WiCAN-Ford-Transit) — repo dédié Ford Transit + HA

---

## 1. Objectif

Lire les données des bus CAN du Ford Transit Custom (HS-CAN + MS-CAN) via le port OBD-II, pour exposer dans Home Assistant **17+ capteurs véhicule** sans aucun capteur physique additionnel :

**HS-CAN (PCM 0x7E0) — Groupe motopropulseur :**
- Vitesse véhicule, régime moteur, température liquide refroidissement
- Niveau carburant, débit carburant, conso instantanée
- Pression admission (turbo), température air admission
- Charge moteur, position papillon, tension ECU
- Codes défaut (DTC)

**MS-CAN (BCM 0x726) — Carrosserie :**
- État portes (conducteur, passager, AR gauche, AR droite, hayon, capot)
- Pression pneus ×6 (AVG, AVD, ARG ext, ARD ext, ARG int, ARD int)
- Batterie porteur (SOC %, courant A, tension V)

---

## 2. Architecture

```
[Port OBD Transit] ←→ [WiCAN Pro]
                           │
                  WiFi → MQTT → HA OS RPi 5
                           │
                  Expose 17+ entités HA
```

### 2.1 WiCAN Pro — Pourquoi c'est le seul choix

| Critère | WiCAN basic | WiCAN Pro | DIY ESP32+CAN |
|---------|------------|-----------|---------------|
| MS-CAN (pins 3/11) | ❌ Non | ✅ Oui | ⚠️ Hardware OK, firmware à écrire |
| PIDs Ford Transit prêts | HS-CAN seul | ✅ Repo dédié | ❌ Reverse engineering complet |
| Sleep mode <1mA | ✅ | ✅ | ⚠️ À implémenter |
| Periodic wake | ✅ | ✅ | ❌ |
| MQTT → HA natif | ✅ | ✅ | ⚠️ ESPHome manuel |
| Firmware updates | Limité | ✅ Full | — |
| Prix | ~38€ | ~82€ | ~15€ + temps dev |

**Verdict : WiCAN Pro.** Le surcoût de 44€ par rapport au WiCAN basic est justifié par le MS-CAN (obligatoire pour BCM = portes + pneus + batterie) et le repo de PIDs déjà mappés pour le Ford Transit.

---

## 3. Données exposées dans Home Assistant

### 3.1 HS-CAN — PCM Powertrain Control Module (0x7E0)

| Entité HA | PID | Source | Description | Unité | Mode |
|-----------|-----|--------|-------------|-------|------|
| `sensor.vehicle_speed` | 0x0D | PCM Mode 01 | Vitesse véhicule | km/h | Roulage |
| `sensor.engine_rpm` | 0x0C | PCM Mode 01 | Régime moteur | tr/min | Roulage |
| `sensor.coolant_temp` | 0x05 | PCM Mode 01 | T° liquide refroidissement | °C | Roulage |
| `sensor.fuel_level` | 0x2F | PCM Mode 01 | Niveau carburant | % | Roulage |
| `sensor.fuel_rate` | 0x5E | PCM Mode 01 | Débit carburant | L/h | Roulage |
| `sensor.intake_air_temp` | 0x0F | PCM Mode 01 | T° air admission | °C | Roulage |
| `sensor.ambient_air_temp` | 0x46 | PCM Mode 01 | T° air extérieure | °C | Roulage |
| `sensor.engine_load` | 0x04 | PCM Mode 01 | Charge moteur calculée | % | Roulage |
| `sensor.throttle_position` | 0x11 | PCM Mode 01 | Position papillon | % | Roulage |
| `sensor.manifold_pressure` | 0x0B | PCM Mode 01 | Pression admission (turbo) | kPa | Roulage |
| `sensor.ecu_voltage` | 0x42 | PCM Mode 01 | Tension batterie ECU | V | Roulage |
| `sensor.dtc_count` | Mode 03 | PCM | Nombre de codes défaut actifs | — | Tout moment |

### 3.2 MS-CAN — BCM Body Control Module (0x726)

| Entité HA | PID | Source | Description | Mode |
|-----------|-----|--------|-------------|------|
| `binary_sensor.door_driver` | 0x225B1D bit 0 | BCM | Porte conducteur | Periodic wake |
| `binary_sensor.door_passenger` | 0x225B1D bit 1 | BCM | Porte passager | Periodic wake |
| `binary_sensor.door_left_rear` | 0x225B1D bit 3 | BCM | Porte AR gauche (coulissante G) | Periodic wake |
| `binary_sensor.door_right_rear` | 0x225B1D bit 4 | BCM | Porte AR droite (coulissante D) | Periodic wake |
| `binary_sensor.door_luggage` | 0x225B1D bit 5 | BCM | Hayon/coffre | Periodic wake |
| `binary_sensor.hood` | 0x225B1D bit 2 | BCM | Capot moteur | Periodic wake |
| `sensor.tpms_front_left` | 0x222813 | BCM | Pression pneu AVG | Periodic wake |
| `sensor.tpms_front_right` | 0x222814 | BCM | Pression pneu AVD | Periodic wake |
| `sensor.tpms_rear_left_outer` | 0x222816 | BCM | Pression pneu ARG ext | Periodic wake |
| `sensor.tpms_rear_right_outer` | 0x222815 | BCM | Pression pneu ARD ext | Periodic wake |
| `sensor.tpms_rear_left_inner` | 0x222818 | BCM | Pression pneu ARG int | Periodic wake |
| `sensor.tpms_rear_right_inner` | 0x222817 | BCM | Pression pneu ARD int | Periodic wake |
| `sensor.battery_soc` | 0x224028 | BCM | Batterie SOC | Periodic wake |
| `sensor.battery_current` | 0x22402B | BCM | Batterie courant | Periodic wake |
| `sensor.battery_voltage_bcm` | 0x22402A | BCM | Batterie tension | Periodic wake |

> **Note PIDs :** Certains PIDs BCM sont marqués 🚧 (en développement) dans le repo WiCAN-Ford-Transit. À valider sur le véhicule réel avec un premier flash FORScan. Les PIDs PCM Mode 01 sont standard SAE J1979 — compatibilité quasi garantie.

---

## 4. Gestion de l'alimentation et du sommeil CAN

### 4.1 Comportement du CAN bus Ford

| État véhicule | CAN bus | Données disponibles |
|---------------|---------|-------------------|
| Contact ON, moteur tournant | HS-CAN + MS-CAN actifs | Toutes (PCM + BCM), temps réel <100ms |
| Contact OFF, < 30 min | CAN partiellement actif | BCM répond encore aux requêtes |
| Contact OFF, > 60 min | CAN en deep sleep | Rien — modules en veille |
| Ouverture porte (véhicule endormi) | BCM se réveille ~5-10s | BCM porte concernée, puis se rendort |

### 4.2 Stratégie WiCAN Pro

```
┌─────────────────────────────────────────────────┐
│ Mode roulage (voltage > 13.2V détecté)          │
│ → WiCAN actif, polling continu, données live    │
│ → Conso : ~200mA @ 12V (négligeable alternateur) │
├─────────────────────────────────────────────────┤
│ Mode stationnement (voltage < 12.8V)            │
│ → WiCAN deep sleep <1mA                         │
│ → Periodic wake configurable (recommandé 5 min) │
│ → Réveil → poll BCM + PCM → MQTT → re-sleep    │
│ → Protection batterie : si < 11.8V, stop wake   │
└─────────────────────────────────────────────────┘
```

### 4.3 Conséquence pour les scénarios

- **Portes en roulage** : temps réel via CAN (redondance Aqara)
- **Portes en camping** : Aqara Zigbee en source primaire (<1s), CAN en backup (0-5 min)
- **TPMS, batterie, carburant** : periodic wake suffit (pas besoin de temps réel porte fermée)
- **Pas de risque batterie** : le WiCAN en sleep <1mA est négligeable (~0.02Ah/jour)

---

## 5. Économies réalisées vs BOM précédente

| Capteur supprimé | Économie | Remplacement |
|------------------|----------|-------------|
| TPMS Bluetooth externe | -20€ | BCM pneus ×6 |
| BME280 T° extérieure | -5€ | PCM ambient air temp (0x46) |
| ~~Aqara portes (×5)~~ | 0€ | Conservés — indispensables en camping/stationnement |
| **Économie nette** | **-25€** | |
| **Coût WiCAN Pro** | **+82€** | |
| **Delta** | **+57€** | |

---

## 6. Impact sur les scénarios existants

| Scénario | Avant | Après CAN bus |
|----------|-------|--------------|
| 1.1 Porte oubliée roulage | D+ DS300 + Aqara Zigbee (~1s) | D+ + CAN speed + RPM + Aqara (triple confirmation, <100ms) |
| 1.2 Hayon resté ouvert | Aqara uniquement | Aqara (primaire) + CAN hayon (backup) |
| 1.4 Verrouillage tiroirs | GPS vitesse > 10 km/h | CAN vitesse instantanée + RPM > 0 |
| 1.5 Détection intrusion | Aqara portes + PIR | Aqara (primaire) + CAN capot/portes (backup) |
| 2.2 Surchauffe habitacle | T° cellule seule | T° cellule + T° liquide refroidissement (cross-check) |
| 5.1 GPS spots | GPS uniquement | GPS + fuel level + RPM + coolant par spot |
| 5.2 Alerte pression pneus | TPMS P4 (~20€) | BCM pneus ×6 — gratuit |

---

## 7. Nouveaux scénarios créés

| # | Scénario | Capteurs CAN | Phase |
|---|----------|-------------|-------|
| 7.1 | **Jauge carburant + range anxiety** | Fuel level + fuel rate + GPS distance | P1 |
| 7.2 | **Conso réelle par trajet (L/100km)** | Fuel rate + speed + odometer | P1 |
| 7.3 | **Diagnostic moteur live (DTC)** | Mode 03 + description codes | P1 |
| 7.4 | **Surveillance turbo** | Manifold pressure vs attendu @ RPM | P2 |
| 7.5 | **Préchauffage Webasto intelligent** | Coolant temp < 5°C + van occupé | P2 |
| 7.6 | **Alerte batterie porteur faible** | Battery SOC + voltage + current | P2 |

---

## 8. Procédure d'installation

### Phase 0 — Préparation (avant réception du van)

1. Commander WiCAN Pro (~82€, Mouser ou Crowd Supply)
2. Flasher firmware WiCAN (dernière version stable)
3. Configurer WiFi + MQTT broker (HA OS RPi 5)
4. Charger le preset PIDs depuis le repo `WiCAN-Ford-Transit`
5. Configurer power saving : sleep <1mA, periodic wake 5 min
6. Vérifier dans HA que le device MQTT apparaît

### Phase 1 — Installation van (5 min)

1. Brancher WiCAN Pro sur le port OBD (sous le tableau de bord, côté conducteur)
2. Vérifier connexion WiFi (le RPi 5 fait AP local ou le WiCAN se connecte au WiFi du RPi)
3. Vérifier dans HA que toutes les entités apparaissent

### Phase 2 — Validation sur véhicule réel

1. Contact ON → vérifier que PCM PIDs arrivent (vitesse, RPM, carburant, T°C)
2. Moteur tournant → vérifier DTC, turbo, conso
3. Contact OFF → vérifier que WiCAN passe en sleep après 30-60 min
4. Periodic wake → vérifier que BCM data (TPMS, batterie) arrive
5. Ouverture porte → vérifier que Aqara détecte avant le prochain wake CAN

---

## 9. Risques et inconnues

| Risque | Probabilité | Mitigation |
|--------|------------|------------|
| PIDs BCM non supportés sur Transit Custom 2026 | Faible | Repo testé sur Transit 2020+ ; valider avec FORScan si doute |
| WiCAN Pro en rupture de stock | Moyenne | Commander maintenant (délai Crowd Supply ~2-3 semaines) |
| WiFi instable dans le garage/stationnement | Faible | RPi 5 = AP local, WiCAN en client ; ou WiCAN AP → RPi client |
| Interférence OBD avec garantie Ford | Nulle | WiCAN est passif (listen-only polling), aucun écriture ECU |
| Batterie porteur déchargée par WiCAN | Très faible | Sleep <1mA + low-voltage cutoff <11.8V activé |

---

## 10. Références

- [WiCAN-Ford-Transit — PIDs Ford Transit + HA](https://github.com/anthonysecco/WiCAN-Ford-Transit) — Repo de référence
- [WiCAN Pro — MeatPi Electronics](https://www.meatpi.com/products/wican-pro) — Hardware
- [WiCAN Pro — Crowd Supply](https://www.crowdsupply.com/meatpi-electronics/wican-pro) — Achat (~$89)
- [WiCAN Firmware Docs — Power Management](https://wambs.github.io/wican-fw/how-to-guides/power-management/) — Sleep/wake
- [FORScan — Ford-specific diagnostics](https://forscan.org/) — Validation PIDs
- [SAE J1979 — OBD-II PIDs (Wikipedia)](https://en.wikipedia.org/wiki/OBD-II_PIDs) — Standard PIDs
- [`SPEC-DS300-TAP.md`](../ds300-tap/SPEC-DS300-TAP.md) — Interface CBE complémentaire
- [`scenarios-algorithmes-vanlife.md`](../scenarios-algorithmes-vanlife.md) — Scénarios complets
- [`BOM-VANLIFE.md`](../BOM-VANLIFE.md) — BOM maître

---

*Document créé par [[Dobby]] 🦉 — 2026-07-09  
Issu de l'analyse OBD/CAN bus session du 2026-07-09 (modèle: deepseek-v4)  
À faire valider par [[Forge]] 🦦 (intégration réseau) et [[Araignée]] 🕷️ (MQTT/HA)*
