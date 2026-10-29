# Détecteur de Niveau Liquide — Sonde Hydrostatique + ESP32

> **Source :** Inbox JC — 2026-07-01  
> **Projets cibles :** IoT Vanlife (cuve eau propre / eaux grises), IoT Serre (récupérateur eau de pluie)  
> **Technologie :** Pression hydrostatique — solution la plus robuste pour cuve extérieure/enterrée  
> **Statut :** Spécification — à prototyper

---

## Pourquoi cette solution

La sonde hydrostatique est supérieure aux alternatives (ultrasons, capacitif, flotteur) parce que :
- L'électronique sensible (ESP32, ADS1115) reste au sec dans un boîtier étanche
- Seule la sonde en inox est immergée — pas de pièces mobiles, pas d'entartrage
- Fonctionne dans l'eau propre comme dans les eaux grises
- Pas affectée par la mousse, les vapeurs ou les gradients de température

---

## BOM — Détecteur Niveau Hydrostatique

| # | Composant | Spécification | Qté | Prix est. | Lien |
|---|-----------|--------------|-----|-----------|------|
| 1 | Sonde hydrostatique TL-136 | **0-5V**, plage 0-2m (ou 0-1m selon cuve), inox 316L | 1 | 24,59€ | 🔴 Commandé Amazon — 2026-07-01 |
| 2 | ESP32-C3 Mini | RISC-V, compact, basse conso | 1 | 5,33€ | ✅ REÇU Amazon — 3× 15,98€ — 2026-07-02 |
| 3 | ADS1115 | ADC 16-bit I2C, 4 canaux, module breakout | 1 | 3,07€ | ✅ REÇU Amazon — 3 pcs 9,21€ — 2026-07-02 |
| 4 | Alimentation 24V DC | 1A, jack 5.5×2.1mm | 1 | 11,51€ | 🔴 Commandé Amazon — 2026-07-01 |
| 5 | Buck Converter MP1584 | 24V→5V, 3A, ultra-compact | 1 | 2,32€ | 🔴 Commandé Amazon — 5 pcs 11,60€ — 2026-07-01 |
| 5b | Boost Converter MT3608 | 12V→24V pour TL-136, 2-24V→5-28V | 1 | ~1€ | 🔴 Commandé Amazon — 10 pcs — 2026-07-01 |
| 5c | Chargeur TC4056 USB-C | Charge 18650, double protection | 1 | 1,33€ | 🔴 Commandé Amazon — 6 pcs 8€ — 2026-07-01 |
| 5d | Accus 18650 flat top | Li-Ion, Samsung 35E ou équivalent | 1 | 3,29€ | 🔴 Commandé velo-electrique.fr — 20 pcs 65,75€ — 2026-07-01 |
| 6 | Câbles Dupont | Mâle-femelle, lot | 1 | ~2€ | ⏸️ Après tests proto |
| 7 | Boîtier étanche | IP65, pour ESP32 + ADS1115 + alim | 1 | ~8€ | ⏸️ Après tests proto |
| 8 | Presse-étoupe | PG7 ou PG9, pour passage câble sonde | 1 | ~2€ | ⏸️ Après tests proto |
| | **Total par point de mesure** | | | **~60-80€** | |

> **Option multi-cuves :** L'ADS1115 a 4 canaux — un seul module peut lire 4 sondes. Ajouter une sonde par cuve supplémentaire (~30-50€).

---

## Câblage

```
┌──────────────────────────────────────────────────┐
│  Alim 24V DC                                     │
│  ├── +24V ──── Sonde TL-136 (fil rouge)          │
│  ├── +24V ──── Buck Converter ── 5V ─── ESP32    │
│  │                                  └── ADS1115   │
│  └── GND ───── Sonde (fil noir)                  │
│       GND ───── ESP32 GND                        │
│       GND ───── ADS1115 GND                      │
│                                                  │
│  ADS1115 ←→ ESP32 (I2C)                          │
│  ├── VDD ──── 5V                                 │
│  ├── GND ──── GND                                │
│  ├── SCL ──── GPIO 22                            │
│  ├── SDA ──── GPIO 21                            │
│  └── A0  ──── Sonde TL-136 (fil signal jaune)    │
└──────────────────────────────────────────────────┘
```

⚠️ **Règle d'or :** Le câble de la sonde contient un tube capillaire pour la compensation barométrique. **Ne jamais couper le câble.** L'extrémité côté branchements doit être dans un boîtier étanche mais **non hermétique** (à l'air libre).

---

## Code ESPHome

> **Note ESP32-C3 Mini :** Les pins I2C par défaut sont GPIO 4 (SDA) et GPIO 5 (SCL), ou GPIO 8/9 selon la carte. Adapter selon le modèle commandé.

### Configuration complète — pourcentage (0-100%)

```yaml
# ── I2C pour ADS1115 ──
# ESP32 standard : SDA=21, SCL=22
# ESP32-C3 Mini  : SDA=4,  SCL=5  (vérifier sur la fiche)
i2c:
  sda: GPIO21
  scl: GPIO22

# ── Convertisseur ADC 16-bit ──
ads1115:
  - address: 0x48

sensor:
  # ── Lecture tension brute (canal A0) ──
  - platform: ads1115
    multiplexer: 'A0_GND'
    gain: 6.144
    name: "Tension Capteur Cuve"
    id: tension_cuve
    update_interval: 10s
    unit_of_measurement: "V"
    accuracy_decimals: 3

  # ── Conversion tension → pourcentage ──
  - platform: template
    name: "Niveau d'eau Cuve"
    unit_of_measurement: "%"
    accuracy_decimals: 1
    icon: "mdi:water-percent"
    lambda: |-
      return id(tension_cuve).state;
    filters:
      - calibrate_linear:
          - 0.50 -> 0     # Tension cuve VIDE (à calibrer)
          - 4.50 -> 100   # Tension cuve PLEINE (à calibrer)
      - clamp:
          min_value: 0
          max_value: 100
```

### Variante — volume en litres

Remplacer le second capteur par :

```yaml
  - platform: template
    name: "Volume d'eau Cuve"
    unit_of_measurement: "L"
    accuracy_decimals: 0
    icon: "mdi:water"
    lambda: |-
      return id(tension_cuve).state;
    filters:
      - calibrate_linear:
          - 0.50 -> 0       # Vide = 0L
          - 3.85 -> 3000    # Plein = 3000L (adapter au volume réel)
      - clamp:
          min_value: 0
          max_value: 3000
```

### Multi-cuves (vanlife : eau propre + eaux grises)

```yaml
ads1115:
  - address: 0x48

sensor:
  - platform: ads1115
    multiplexer: 'A0_GND'
    gain: 6.144
    name: "Tension Cuve Eau Propre"
    id: tension_eau_propre
    update_interval: 10s
    unit_of_measurement: "V"
    accuracy_decimals: 3

  - platform: ads1115
    multiplexer: 'A1_GND'
    gain: 6.144
    name: "Tension Cuve Eaux Grises"
    id: tension_eaux_grises
    update_interval: 10s
    unit_of_measurement: "V"
    accuracy_decimals: 3

  - platform: template
    name: "Eau Propre"
    unit_of_measurement: "%"
    icon: "mdi:water"
    lambda: return id(tension_eau_propre).state;
    filters:
      - calibrate_linear: [0.50 -> 0, 4.50 -> 100]
      - clamp: [0, 100]

  - platform: template
    name: "Eaux Grises"
    unit_of_measurement: "%"
    icon: "mdi:water-remove"
    lambda: return id(tension_eaux_grises).state;
    filters:
      - calibrate_linear: [0.50 -> 0, 4.50 -> 100]
      - clamp: [0, 100]
```

---

## Calibration

1. **Cuve vide** — sonde à l'air libre. Noter la tension (ex: 0.52V). Remplacer `0.50` dans `calibrate_linear`.
2. **Cuve pleine** — sonde au fond de la cuve remplie. Noter la tension (ex: 3.24V). Remplacer `4.50`.
3. Téléverser → ESPHome fait la conversion automatiquement.

---

## Dashboard Home Assistant

### Carte Jauge (intégrée, sans HACS)

```yaml
type: gauge
entity: sensor.niveau_d_eau_cuve
name: Niveau cuve
unit: '%'
min: 0
max: 100
severity:
  green: 40
  yellow: 15
  red: 0
needle: true
```

### Water Tank Card (via HACS, effet visuel réaliste)

```yaml
type: custom:water-tank-card
entity: sensor.niveau_d_eau_cuve
name: Récupérateur d'eau
tank_type: vertical
fill_color: '#3498db'
warning_level: 20
critical_level: 10
```

Installation : HACS → Frontend → "Water Tank Card".

---

## Automatisation — Remplissage automatique (vanne SWV)

```yaml
alias: "Remplissage auto — Cuve basse"
trigger:
  - platform: numeric_state
    entity_id: sensor.niveau_d_eau_cuve
    below: 20
action:
  - service: switch.turn_on
    target:
      entity_id: switch.0x44e2f8fffe052e46  # SWV
  - delay: "00:00:05"  # laisse la vanne s'ouvrir
mode: single

alias: "Remplissage auto — Cuve pleine"
trigger:
  - platform: numeric_state
    entity_id: sensor.niveau_d_eau_cuve
    above: 90
action:
  - service: switch.turn_off
    target:
      entity_id: switch.0x44e2f8fffe052e46  # SWV
mode: single
```

## Automatisation — Alerte niveau bas

```yaml
alias: "Alerte — Cuve presque vide"
trigger:
  - platform: numeric_state
    entity_id: sensor.niveau_d_eau_cuve
    below: 10
action:
  - service: notify.notify
    data:
      title: "⚠️ Alerte Cuve"
      message: "Niveau inférieur à 10%"
mode: single
```

---

## Use Cases PKA

### Vanlife (Westfalia Kelsey)
| Cuve | Sonde | Usage |
|------|-------|-------|
| Eau propre (~100L) | TL-136 0-1m | Monitoring niveau, alerte remplissage |
| Eaux grises (~80L) | TL-136 0-1m | Alerte vidange nécessaire |
| Réservoir WC | Optionnel | — |

### Serre Esneux
| Cuve | Sonde | Usage |
|------|-------|-------|
| Récupérateur eau de pluie (1000-3000L) | TL-136 0-2m | Pilotage irrigation, alerte sécheresse |
| Cuve tampon | TL-136 0-2m | — |

---

## Prochaines étapes

- [ ] Commander 1 sonde TL-136 0-5V + ADS1115 pour prototype banc
- [ ] Tester sur ESP32 avec ESPHome
- [ ] Calibrer avec un seau gradué
- [ ] Commander les sondes supplémentaires selon use cases validés
- [ ] Intégrer dans le dashboard HA vanlife

---

## Références

- [Forum HACF — Sonde niveau d'eau ESPHome](https://forum.hacf.fr/t/esphome-sonde-de-niveau-d-eau/46246)
- [HA Community — Water level sensor](https://community.home-assistant.io/t/esphome-water-level-sensor/126504)
- [OpenHAB Community — Rainwater tank ESPHome](https://community.openhab.org/t/rainwater-tank-level-measurement-with-esphome/163164)
- [YouTube — TL-136 ESP32](https://www.youtube.com/watch?v=eztjJrg7F94)
- [Instructables — ESP Pressure Measuring](https://www.instructables.com/ESP-Pressure-Measuring-Device/)
- [Arduino Forum — ESP32 + ADS1115 + Transducer](https://forum.arduino.cc/t/esp32-ads1115-linear-transducers-pressure-transducer/1432577)

---

*Document assemblé par Dobby 🦉 — 2026-07-01. Source : note INBOX JC.*
