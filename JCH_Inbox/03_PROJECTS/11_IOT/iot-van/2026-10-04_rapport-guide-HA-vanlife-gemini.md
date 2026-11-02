# Rapport — Système Home Assistant Vanlife « Lupo » (source pour générer un guide)

> **Objet :** ce document est un rapport d'état consolidé, rédigé pour être utilisé comme **source** dans Gemini Notebook afin de générer un guide pas-à-pas d'installation et de configuration du système domotique du van.
> **Rédigé par :** Dobby 🦉 — 2026-10-04
> **Véhicule :** Lupo 🐺 — Westfalia Kelsey 2026, porteur Ford Transit Custom Tourneo (V710), 2.0 EcoBlue 170 ch, 4×4, BVA8
> **Deadline projet :** 1er novembre 2026 (installation IOT dans le van)

---

## 1. Contexte & objectif

Le van Westfalia Kelsey 2026 (« Lupo ») est équipé d'un système domotique autonome basé sur **Home Assistant**, qui mutualise :

- La **sécurité** (portes, hayon, intrusion, toit relevable).
- Le **confort** (température, condensation, inclinaison, gaz, eaux).
- L'**énergie** (batteries cellule/porteur, solaire, autonomie).
- Le **véhicule** (CAN bus via OBD : carburant, RPM, température moteur, codes défaut, turbo, pression pneus).

Objectif final : un van pilotable et surveillé depuis l'iPhone (via l'app Home Assistant + Tailscale), même hors réseau.

---

## 2. Architecture globale — 3 instances HA distribuées

| Instance | Localisation | Rôle | État |
|----------|-------------|------|------|
| **HA Docker M5** | Belgique (maison, Mac M5) | Serveur principal maison + dev | 🟢 opérationnel |
| **HA OS RPi 5 Esneux** | Serre + maison (Esneux) | Serre / maison secondaire | ⚪ gelé |
| **HA OS RPi 5 van** | Van Lupo | Instance embarquée autonome | 🔴 P0 (focus actuel) |

- Supervision unifiée sur iPhone via **Tailscale**.
- Chaque instance est **autonome** (le van fonctionne sans réseau externe).

---

## 3. État actuel du système van (au 2026-10-01)

### Matériel

| Composant | État |
|-----------|------|
| RPi 5 4 Go | ✅ assemblé, **boot résolu** (01/10) |
| Stockage | Samsung PRO Endurance 256 Go **microSD** (NVMe retiré — cause du blocage boot) |
| OS | **HAOS 18.3** (fix GitHub #5005), auto-update OFF, statut Healthy |
| Alimentation | USB-C directe (les pogo pins X1205 ne suffisent pas pour le NVMe) |
| UPS | Geekworm X1205 (accus 18650) — conservé pour l'UPS uniquement |
| Boîtier | Geekworm X1201-C1 métal ✅ monté — reste silentblocs + coating |
| Refroidissement | Refroidisseur actif + Noctua NF-A4x10 |
| Coordinateur Zigbee | Sonoff ZBDongle-E (EmberZNet) |
| CAN/OBD | **WiCAN Pro installé** (HS-CAN + MS-CAN, 17+ entités) |

### Logiciel

- **HAOS 18.3** + Core + Supervisor à jour.
- **Zigbee2MQTT v5** (adapter `ember`, canal 15) → **Mosquitto MQTT** (`:1883`) → **Home Assistant** (intégration MQTT).
- Intégrations actives : MQTT, go2rtc (caméras), Google Translate (TTS), app companion iPhone (×2), + defaults.
- **Aucune automatisation/script/scène encore écrit** — c'est le chantier principal.

### Reste à faire (avant le 01/11)

1. Silentblocs + coating du RPi.
2. Commander les **8 capteurs Zigbee** (~88 €, liste finalisée).
3. Intégrer le WiCAN Pro dans HA (spec complète prête : `specs/SPEC-CAN-BUS.md`).
4. Écrire les automatisations (voir §6).
5. Installation physique dans le van + validation Tailscale.

---

## 4. Sources de données & capteurs

### 4.1 Ouverture (portes/panneaux)

| Capteur | Technologie | Entité HA |
|---------|-------------|-----------|
| Porte AV conducteur / passager, 2 portes coulissantes, hayon, toit relevable, frigo, tiroirs | Aqara MCCGQ11LM (Zigbee, ×8) | `binary_sensor.door_*` |

### 4.2 Interface CBE DS300 (électrique cellule) — « DS300 Tap »

| Signal | Entité HA |
|--------|-----------|
| Tension batterie cellule | `sensor.leisure_battery_voltage` |
| Tension batterie porteur | `sensor.starter_battery_voltage` |
| Moteur tournant (signal D+) | `binary_sensor.engine_running` |
| Présence 230 V secteur | `binary_sensor.shore_power` |
| Niveau eau propre | `sensor.fresh_water_level` |
| Niveau eaux grises | `sensor.grey_water_level` |

> Spec : `ds300-tap/SPEC-DS300-TAP.md` (pinout CBE DS300, source WomoNET).

### 4.3 CAN bus véhicule (WiCAN Pro, OBD)

| Signal | Entité HA |
|--------|-----------|
| Vitesse | `sensor.speed` |
| Régime moteur | `sensor.rpm` |
| Niveau carburant | `sensor.fuel_level` |
| Température liquide refroidissement | `sensor.coolant_temp` |
| Codes défaut moteur | `sensor.dtc` / `binary_sensor.dtc_active` |
| Batterie porteur SOC/tension/courant | `sensor.battery_soc`, `sensor.battery_voltage_bcm`, `sensor.battery_current` |
| Pression turbo (boost) | `sensor.boost_pressure` |
| Pression pneus | TPMS ×6 (remplace un TPMS externe) |

> Spec : `specs/SPEC-CAN-BUS.md`. Attention : compatibilité WiCAN Pro ↔ Exosfer OBD Protect à vérifier.

### 4.4 Énergie avancée (P3)

| Capteur | Technologie |
|---------|-------------|
| SOC + courant batterie cellule | Victron SmartShunt 500A (VE.Direct → USB) |
| Production solaire | Victron SmartSolar MPPT 100/20 (VE.Direct → USB) |

### 4.5 Divers (ESP32 / BLE / USB)

| Capteur | Usage |
|---------|-------|
| MPU6050 (IMU) | Inclinaison roll/pitch (repérage terrain) |
| BME280 | Station météo extérieure (T°, pression, humidité) |
| Mopeka Pro Check (BLE) | Niveau gaz propane/butane |
| u-blox 7 (USB) | Position GPS spots |
| INMP441 + Whisper | Commande vocale locale |
| ESP32-CAM ×2 | Caméras intérieures/extérieures |

---

## 5. Conventions de nommage & réglage

- **Tous les seuils** sont des helpers `input_number`, jamais en dur dans le YAML :

```
input_number.vanlife_<scenario>_<parametre>
```

Exemples : `input_number.vanlife_porte_roulage_seuil_vitesse`, `input_number.vanlife_hayon_delai`, `input_number.vanlife_frigo_timer`.

- Un panneau Lovelace « Réglages Vanlife » regroupe tous les sliders.
- Chaque scénario a un **filtre anti faux-positifs** (vitesse nulle, mode nuit, cross-check média, etc.).

---

## 6. Les 7 familles d'automatisations (conception complète)

### Famille 1 — OUVERTURE

| # | Scénario | Règle (résumé) | Action | Seuils | Priorité |
|---|----------|----------------|--------|--------|----------|
| 1.1 | Porte oubliée en roulage | SI moteur ET porte > 15 s → ALERTE | Push iPhone + warning dashboard | 15 s (30 s hayon) | 🔴 P1 |
| 1.2 | Hayon resté ouvert (bivouac) | SI hayon ouvert ET départ → alerte | Push | délai configurable | 🟡 P2 |
| 1.3 | Frigo ouvert trop longtemps | SI frigo ouvert > timer | Push | `frigo_timer` | 🔴 P1 |
| 1.4 | Verrouillage tiroirs | SI vitesse > seuil → verrouiller | Relais | seuil vitesse | 🟡 P2 |
| 1.5 | Détection intrusion | SI porte/capot s'ouvre mode absent | Alarme + push | — | 🟡 P2 |

### Famille 2 — CLIMAT / ENVIRONNEMENT

| # | Scénario | Règle | Action | Priorité |
|---|----------|-------|--------|----------|
| 2.1 | Condensation habitacle | SI HR > seuil → alerte aérer | Push | 🟡 P2 |
| 2.2 | Surchauffe habitacle | SI T° int > seuil → alerte + ventilation | Push + relais ventilo | 🔴 P1 |
| 2.3 | Confort sonore | dB > seuil + contexte nuit | Log | 🟢 P3 |
| 2.4 | Alarme sonore (pic dB) | pic > 85 dB en < 100 ms la nuit | Log + notification | 🔵 P4 |
| 2.5 | Gel batterie / eau | T° < 0 → vidange/gel | Push saisonnier | 🔵 P4 |
| 2.6 | Inclinaison (repérage) | angle > 3° → recaler | Dashboard | 🟡 P2 |

### Famille 3 — ÉNERGIE

| # | Scénario | Règle | Action | Priorité |
|---|----------|-------|--------|----------|
| 3.1 | Autonomie prédictive | SOC × capacité / (conso − prod) | Dashboard (heures/jours) | 🟢 P3 |
| 3.2 | Shutdown batterie faible | SOC < 20 % sans recharge → shutdown | Shutdown propre RPi | 🟢 P3 |
| 3.3 | Niveau gaz | < 20 % avertir, < 10 % critique | Push | 🟢 P3 |
| 3.4 | Niveaux d'eau | propre < 20 %, grise > 80 % | Push | 🟢 P3 |

### Famille 4 — STATION MÉTÉO EXTERNE

| # | Scénario | Règle | Priorité |
|---|----------|-------|----------|
| 4.1 | Décision toit relevable | vent < 30 km/h + pas de pluie | 🟢 P3 |
| 4.2 | Alerte intempérie | pluie OU pression chute > 3 hPa/h → rentrer stores | 🔵 P4 |

### Famille 5 — ÉQUIPEMENTS

| # | Scénario | Priorité |
|---|----------|----------|
| 5.1 | GPS spots (profil complet au spot) | 🟢 P3 |
| 5.2 | Pression pneus | remplacé par TPMS BCM ×6 (CAN) |

### Famille 6 — SÉCURITÉ (reprise intrusion/capot via CAN en backup des Aqara)

### Famille 7 — CAN BUS (WiCAN Pro)

| # | Scénario | Règle (résumé) | Priorité |
|---|----------|----------------|----------|
| 7.1 | Jauge carburant | niveau < seuil → alerte | 🔴 P1 |
| 7.2 | Conso trajet | conso anormale → alerte | 🔴 P1 |
| 7.3 | DTC moteur | code défaut actif → alerte | 🔴 P1 |
| 7.4 | Surveillance turbo | boost hors plage → alerte | 🟡 P2 |
| 7.5 | Préchauffage Webasto | coolant < 5 °C + départ prévu → suggestion | 🟡 P2 |
| 7.6 | Batterie porteur faible | SOC < 50 % moteur off > 24 h → alerte | 🟡 P2 |

> **Impact CAN sur scénarios existants :** la vitesse/RPM CAN remplace l'attente GPS ; le TPMS BCM supprime le TPMS externe ; le capot/portes CAN sert de backup aux Aqara.

---

## 7. Roadmap de priorisation

| Priorité | Scénarios | Phase |
|----------|-----------|-------|
| 🔴 Critique | 1.1 Porte roulage, 2.2 Surchauffe, 1.3 Frigo, 7.1 Carburant, 7.2 Conso, 7.3 DTC | P1 |
| 🟡 Important | 1.2 Hayon, 1.4 Tiroirs, 1.5 Intrusion, 2.1 Condensation, 2.6 Angle, 7.4 Turbo, 7.5 Webasto, 7.6 Batterie porteur | P2 |
| 🟢 Confort | 3.1 Autonomie, 3.2 Shutdown, 4.1 Toit, 5.1 GPS, 2.3 dB | P3 |
| 🔵 Évolution | 2.4 Alarme sonore, 2.5 Gel, 4.2 Intempérie | P4 |

---

## 8. Étapes concrètes restantes (pour le guide)

1. **Finaliser le RPi** : silentblocs + coating conformal.
2. **Commander et appairer les 8 capteurs Zigbee** (Aqara MCCGQ11LM + SNZB-02DR2 déjà reçus ; nommer `door_*`, `LuxSerre` déjà nommé).
3. **Brancher le WiCAN Pro** sur l'OBD et vérifier compatibilité Exosfer OBD Protect.
4. **Créer les helpers `input_number.vanlife_*`** (tous les seuils).
5. **Écrire les automatisations P1** (6 scénarios critiques) en premier.
6. **Puis P2, P3, P4** selon la roadmap.
7. **Installer dans le van** + valider Tailscale depuis l'iPhone.

---

## 9. Notes techniques à transmettre au guide

- **Zigbee** : ZHA *non* utilisé — c'est Zigbee2MQTT + Mosquitto. Adapter `ember`, canal 15, coordinateur Sonoff ZBDongle-E.
- **DS300 Tap** : les signaux CBE (batteries, D+, secteur, cuves) arrivent via l'interface DS300, spec pinout déjà rédigée.
- **CAN** : WiCAN Pro en HS-CAN + MS-CAN, 17+ entités, remplace plusieurs capteurs externes (vitesse, TPMS).
- **Énergie avancée** : Victron SmartShunt + SmartSolar en VE.Direct → USB (P3, après le socle P1/P2).
- **Pas de valeurs en dur** : tout passe par `input_number` pour ajuster en conditions réelles.

---

## 10. Références internes

- `hardware-state.md` (section STATION-DOMO / IoT) — matériel reçu/commandé
- `11_IOT/thread-iot.md` — thread vivant du projet
- `11_IOT/iot-van/scenarios-algorithmes-vanlife.md` — conception complète des scénarios
- `11_IOT/iot-van/specs/SPEC-CAN-BUS.md` — spec CAN/WiCAN
- `11_IOT/iot-van/ds300-tap/SPEC-DS300-TAP.md` — spec interface CBE DS300
- `11_IOT/iot-van/ASSEMBLAGE-RPi5-VANLIFE.md` — assemblage RPi
- `11_IOT/iot-van/SOLUTION-BOOT-NVME-2026-07-09.md` — diagnostic boot NVMe
