# Matériel Lupo — liste canonique

> **State vivant** — source de vérité unique pour l'équipement du van Lupo (domotique, capteurs, énergie, réseau, sécurité).
> Registre d'achats détaillé (prix, dates, sources) : `hardware-state.md`. Ce fichier est la **vue opérationnelle** par catégorie.
> `last_updated : 2026-11-13`

## Véhicule

| Élément | Statut | Note |
|---|---|---|
| Ford Transit Custom Westfalia Kelsey 2026 | POSSÉDÉ | livré 30/07/2026, 170 CV, 4x4, blanc |

## Contrôleur & domotique (RPi 5)

| Élément | Statut | Note |
|---|---|---|
| RPi 5 (hôte HAOS `lupo`) | POSSÉDÉ | 8 Go mesurés, HAOS 18.3 |
| Samsung PRO Endurance 256GB microSD | POSSÉDÉ | remplace la SD 128 Go |
| Alim officielle RPi5 27W | POSSÉDÉ | |
| Refroidisseur actif RPi5 | POSSÉDÉ | |
| Noctua NF-A4x10 PWM | POSSÉDÉ | ventilateur 40×10 mm silencieux |
| Geekworm X1205 UPS HAT + accus 18650 ×20 | POSSÉDÉ | identification physique UPS/accus à revérifier |
| Geekworm X1201-C1 boîtier métal ×2 | POSSÉDÉ | |
| PCIe to M.2 NVMe Shield ×2 + SSD NVMe Fanxiang 256GB | POSSÉDÉ | NVMe retiré le 01/10 |
| PV PI HAT | POSSÉDÉ | |
| Bidirectional Level Shifter 8CH ×2 | POSSÉDÉ | 3.3V ↔ 5V, I2C/SPI/UART |

## Réseau & connectivité

| Élément | Statut | Note |
|---|---|---|
| Sonoff ZBDongle-E (coordinateur Zigbee Lupo) | POSSÉDÉ | port noyau `3-2`, Z2M + MQTT actifs |
| Teltonika RUT240 (routeur 4G/LTE) | POSSÉDÉ | SIM 4G → Ethernet → RPi, remplace le ZTE |
| ZTE MF833U1 LTE USB (dongle) | POSSÉDÉ | supplanté par le RUT240 |

## Capteurs & actuateurs

| Élément | Statut | Note |
|---|---|---|
| SNZB-02UL AirGuard TH E-Ink | POSSÉDÉ | T°/H°, ré-appairé le 06/11 (LQI 255/255) |
| Sonoff Smart Water Valve | POSSÉDÉ | électrovanne connectée |
| Sonoff ZBMiniR2 | POSSÉDÉ | smart switch Zigbee |
| ADS1115 ADC 16-bit I2C ×6 | POSSÉDÉ | 3 Heemol + 3 HW-19S |
| ESP32-C3 Super Mini ×3 | POSSÉDÉ | détecteur niveau liquide |
| Step-Down HW-133 3A 5V ×5 | POSSÉDÉ | buck 24V-9V → 5V fixe |
| Power Supply Adapter HS24A (24V) | POSSÉDÉ | alim sonde TL-136 |
| Sonde hydrostatique TL-136 | POSSÉDÉ | capteur 4-20 mA, niveau liquide |
| XKC-Y25-V capteur niveau sans contact ×4 | POSSÉDÉ | cuves Lupo |
| Module relais optocoupleur 12V 2CH ×3 | POSSÉDÉ | |
| GY-521 MPU-6050 IMU ×4 | POSSÉDÉ | gyro + accéléro |

## Énergie nomade (à commander)

| Élément | Statut | Note |
|---|---|---|
| Bluetti Elite 100 V2 | À COMMANDER | 1 024 Wh LiFePO4, onduleur 1 800 W |
| Bluetti PV200 (panneau 200 W) | À COMMANDER | plié 59×63 cm, IP67 |
| Rallonge MC4 (5–10 m) | À COMMANDER | PV200 → Bluetti |
| Charger 1 (alternateur 560 W) | OPTION | recharge en roulant |

## Caméras & sécurité

| Élément | Statut | Note |
|---|---|---|
| Reolink Argus MagiCam | POSSÉDÉ | dashcam/sécurité, fixation aimantée |
| Wolfbox G900 TriPro Bumper | POSSÉDÉ | miroir 12", avant 4K + arrière 2.5K + pare-chocs |
| Wolfbox OEM bracket | POSSÉDÉ | à faire fixer par Be Camper |
| Kit hardwire Wolfbox (mode parking) | POSSÉDÉ | fusible tap + coupure basse tension |
| Rallonge câble caméra arrière 10/15 m | POSSÉDÉ | van 5,45 m |
| microSD High Endurance 256 Go (dashcam) | À COMMANDER | séparée de celle du RPi |
| Exosfer OBD Protect | POSSÉDÉ | antivol électronique prise OBD |

## OBD / véhicule

| Élément | Statut | Note |
|---|---|---|
| WiCAN Pro (OBD/CAN Ford) | POSSÉDÉ | MS-CAN + HS-CAN, installé physiquement |

## Audio

| Élément | Statut | Note |
|---|---|---|
| BOYA BY-MM1 | POSSÉDÉ | micro shotgun |
| UGREEN USB Audio | POSSÉDÉ | adaptateur audio RPi |
| INMP441 MEMS I2S ×3 | POSSÉDÉ | acquisition vocale |
