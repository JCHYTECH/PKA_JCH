# SPEC-CAPTEUR-ENV — Station météo intérieure Lupo

> **Date :** 2026-07-16 | **Rédacteur :** [[Dobby]] 🦉  
> **Matériel :** ESP32-C3 Super Mini + BME688 + SHT31 (stock WildNexus Mouser #39492997)  
> **Coût :** 0€ (composants déjà reçus)  
> **Jalon :** Niveau 2 — avant arrivée Lupo (7 août)

---

## 1. Objectif

Une carte unique qui mesure et expose dans Home Assistant :

- **Température intérieure cellule** (BME688 + SHT31 — double mesure, cross-check)
- **Humidité relative** (BME688 + SHT31)
- **Pression atmosphérique** (BME688 — baromètre, prévisions météo)
- **Qualité d'air / VOC** (BME688 — indice IAQ, CO₂ équivalent, polluants)

Le tout sans acheter un seul capteur. Les composants viennent de la commande Mouser WildNexus.

---

## 2. Composants

| Composant | Réf | Qté | Source | Rôle |
|-----------|-----|-----|--------|------|
| ESP32-C3 Super Mini | Heemol | 1 | IOT (reçu ×3) | µC WiFi + I2C master |
| BME688 | Bosch | 1 | Mouser #39492997 (×2) | T°/HR/Pression/VOC |
| SHT31-DIS-B | Sensirion | 1 | Mouser #39492997 (×2) | T°/HR haute précision |
| Buck TPS62840 | TI | 1 | Mouser #39492997 (×5) | Alim 5V→3.3V |
| Résistance 4.7kΩ | 0603 | 2 | Kit SparkFun Mouser | Pull-up I2C |
| Condensateur 10µF | 0603 | 2 | Kit SparkFun Mouser | Découplage |
| Breadboard + jumpers | — | 1 | Miuzei Starter Kit | Proto rapide |

### Pourquoi deux capteurs ?

| | BME688 | SHT31 |
|---|---|---|
| Température | ±0.5°C | ±0.2°C |
| Humidité | ±3% RH | ±2% RH |
| Pression | ±0.6 hPa (baromètre) | ❌ |
| VOC / IAQ | ✅ IAQ index, eCO₂, b-VOC | ❌ |
| I2C | 0x76 ou 0x77 | 0x44 |

Le SHT31 donne la mesure précise, le BME688 donne la pression + qualité d'air + backup T°/HR. Les deux sur le même bus I2C, aucune complexité.

---

## 3. Architecture

```
┌──────────────┐
│   BME688     │──I2C (0x77)──┐
│ T/HR/P/VOC   │              │
└──────────────┘              │     ┌─────────────┐
                              ├─────│ ESP32-C3    │──WiFi──▶ MQTT ──▶ Home Assistant
┌──────────────┐              │     │ Super Mini  │
│   SHT31      │──I2C (0x44)──┘     └──────┬──────┘
│ T/HR précise │                            │
└──────────────┘                    Alim 5V USB ou
                                    buck TPS62840 (12V→3.3V)
```

- I2C partagé (SDA=GPIO4, SCL=GPIO5)
- Alimentation : USB-C du ESP32-C3 pour le proto banc, puis buck TPS62840 sur le 12V cellule pour le déploiement
- WiFi : se connecte à l'AP `VanLife_Network` du RPi 5

---

## 4. Pinout ESP32-C3 Super Mini

| ESP32-C3 | Connexion | Notes |
|----------|-----------|-------|
| GPIO4 | SDA (I2C) | BME688 (0x77) + SHT31 (0x44) |
| GPIO5 | SCL (I2C) | Bus partagé |
| 3.3V | VDD BME688 + SHT31 | Alim depuis régulateur ESP32 |
| GND | GND BME688 + SHT31 | Masse commune |
| 5V / USB | Alim ESP32 | USB-C pour proto, TPS62840 pour final |

> Les résistances pull-up I2C (4.7kΩ) sont généralement déjà présentes sur les breakout BME688/SHT31. À vérifier — sinon ajouter entre SDA/3.3V et SCL/3.3V.

---

## 5. Firmware ESPHome

```yaml
# ESPHome config — Station météo van
# Flasher sur ESP32-C3 Super Mini
# Carte : esp32-c3-devkitm-1

esphome:
  name: lupo-meteo
  friendly_name: "Lupo Météo"
  comment: "BME688 + SHT31 — T°/HR/Pression/IAQ cellule"

esp32:
  board: esp32-c3-devkitm-1
  variant: esp32c3
  framework:
    type: arduino

# I2C — bus partagé
i2c:
  sda: GPIO4
  scl: GPIO5
  scan: true
  frequency: 100kHz

# Capteurs
sensor:
  # === BME688 ===
  - platform: bme68x_bsec2
    temperature:
      name: "Cellule T° (BME)"
      id: temp_bme
    pressure:
      name: "Pression atmosphérique"
      id: pressure
    humidity:
      name: "Cellule HR (BME)"
      id: hum_bme
    gas_resistance:
      name: "Résistance gaz"
      id: gas_resistance
    iaq:
      name: "IAQ Index"
      id: iaq
    iaq_accuracy:
      name: "IAQ Accuracy"
    co2_equivalent:
      name: "eCO₂"
    breath_voc_equivalent:
      name: "b-VOC"
    temperature_offset: 0  # Ajuster après calibration
    sample_rate: LP
    state_save_interval: 1h

  # === SHT31 ===
  - platform: sht3xd
    temperature:
      name: "Cellule T° (SHT)"
      id: temp_sht
    humidity:
      name: "Cellule HR (SHT)"
      id: hum_sht
    address: 0x44
    update_interval: 30s

  # === Template : moyenne T° cross-check ===
  - platform: template
    name: "Cellule T° (moyenne)"
    unit_of_measurement: "°C"
    accuracy_decimals: 1
    lambda: |-
      return (id(temp_bme).state + id(temp_sht).state) / 2.0;
    update_interval: 30s

  # === Template : moyenne HR cross-check ===
  - platform: template
    name: "Cellule HR (moyenne)"
    unit_of_measurement: "%"
    accuracy_decimals: 0
    lambda: |-
      return (id(hum_bme).state + id(hum_sht).state) / 2.0;
    update_interval: 30s

  # === Template : alerte écart T° (détection panne capteur) ===
  - platform: template
    name: "Écart T° BME vs SHT"
    unit_of_measurement: "°C"
    accuracy_decimals: 2
    lambda: |-
      return abs(id(temp_bme).state - id(temp_sht).state);
    update_interval: 60s

# WiFi
wifi:
  ssid: !secret van_wifi_ssid
  password: !secret van_wifi_password
  ap:
    ssid: "Lupo-Meteo-Fallback"
    password: !secret fallback_ap_password

# MQTT
mqtt:
  broker: !secret mqtt_broker
  username: !secret mqtt_user
  password: !secret mqtt_pass

# API Home Assistant
api:
  encryption:
    key: !secret api_encryption_key

ota:
  - platform: esphome
    password: !secret ota_password

# Logging
logger:
  level: INFO

# Status LED
status_led:
  pin:
    number: GPIO8
    inverted: true
```

---

## 6. Emplacement dans le van

La carte se place dans le volume habitable, à mi-hauteur, à l'abri du soleil direct et des courants d'air :

- **Emplacement recommandé :** paroi du meuble central Kelsey, face intérieure, à ~1m du sol
- **Éviter :** près de la baie coulissante (soleil direct), au-dessus du frigo (chaleur), dans le coffre (isolation différente)
- **Fixation :** bande Velcro ou vis M2 sur le boîtier imprimé

---

## 7. Étalonnage

### BME688
- L'IAQ a besoin de **24-48h de burn-in** pour se calibrer (fonctionnement continu)
- Le `state_save_interval: 1h` sauvegarde l'état d'étalonnage sur flash (survit aux reboots)
- Premier cycle : laisser tourner 48h dans les conditions réelles avant de se fier à l'IAQ/eCO₂

### SHT31
- Étalonné d'usine, aucune calibration nécessaire
- Utiliser le SHT31 comme référence pour ajuster l'offset du BME688 si besoin

---

## 8. Scénarios Home Assistant

### 8.1 Alerte condensation
```yaml
alias: "Alerte condensation"
trigger:
  - platform: numeric_state
    entity_id: sensor.cellule_hr_moyenne
    above: 75
action:
  - service: notify.mobile_app_jc_iphone
    data:
      title: "💧 Lupo — Humidité élevée"
      message: "HR à {{ states('sensor.cellule_hr_moyenne') }}% — aérer le van."
```

### 8.2 Prévision météo locale (pression)
```yaml
alias: "Alerte chute de pression"
trigger:
  - platform: template
    value_template: >
      {{ (state_attr('sensor.pression_atmospherique', 'trend') | float(0)) < -1.5 }}
action:
  - service: notify.mobile_app_jc_iphone
    data:
      title: "🌧️ Lupo — Chute de pression"
      message: "Baisse rapide — risque de pluie dans les 6-12h."
```

### 8.3 Qualité d'air dégradée
```yaml
alias: "Alerte qualité d'air"
trigger:
  - platform: numeric_state
    entity_id: sensor.iaq_index
    above: 150
action:
  - service: notify.mobile_app_jc_iphone
    data:
      title: "🫁 Lupo — Air dégradé"
      message: "IAQ {{ states('sensor.iaq_index') | int }} — aérer ou vérifier cuisson/humidité."
```

---

## 9. Intégration avec le reste du système van

Ce capteur complète le tableau de bord environnement :

| Capteur | Fournit |
|---------|---------|
| **BME688** (intérieur) | T°/HR/pression/IAQ |
| **SHT31** (intérieur) | T°/HR précise, cross-check |
| **SNZB-02DR2** (backup Zigbee) | T°/HR — fonctionne même si WiFi down |
| **CAN bus** (OBD) | T° extérieure (PCM 0x46) + T° admission (0x0F) |
| **DS300 Tap** | Tensions B1/B2, D+, 230V |

---

## 10. Coût & délai

| Poste | Coût | Statut |
|-------|------|--------|
| BME688 | 0€ | Déjà reçu (Mouser #39492997, ×2) |
| SHT31 | 0€ | Déjà reçu (Mouser #39492997, ×2) |
| ESP32-C3 | 0€ | Déjà reçu (Heemol, ×3) |
| Buck TPS62840 | 0€ | Déjà reçu (Mouser #39492997, ×5) |
| Passifs (R, C) | 0€ | Déjà reçu (Kit SparkFun 0603) |
| Breadboard + jumpers | 0€ | Déjà reçu (Miuzei Starter Kit) |
| **Total** | **0€** | |

**Économie vs achat capteurs Zigbee dédiés :** 30€ (SNZB-02D ×3 supprimés du panier Amazon).

---

*Document créé par [[Dobby]] 🦉 — 2026-07-16 — modèle: deepseek-v4*  
*Composants issus de la commande Mouser #39492997 (WildNexus P0, gelé septembre)*  
*Firmware ESPHome à flasher avant le 7 août*
