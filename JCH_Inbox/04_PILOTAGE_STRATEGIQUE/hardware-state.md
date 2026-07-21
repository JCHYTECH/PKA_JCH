# HARDWARE STATE — Single Source of Truth

> **Règle :** Dobby lit ce fichier AVANT de faire une affirmation sur le matériel.
> **Mise à jour :** immédiate après chaque info de JC (réception, commande, panne, prêt).
> **Ne pas déduire, ne pas deviner.** Si pas dans ce fichier → demander à JC.
> **Dernière mise à jour :** 2026-07-19 — Noctua NF-A4x10 PWM reçu

---

## WildNexus P0

| Composant | Qté | Statut | Notes |
|-----------|-----|--------|-------|
| Nordic PPK2 | 1 | ✅ REÇU | ~100€, utilisé actif |
| ESP32-S3-DevKitC-1 N16R8 | 2 | ✅ REÇU | Amazon MiMiU, 21,98€ |
| ESP32-CAM OV2640 (avec modules caméra) | 2 | ✅ REÇU | Hailege Amazon.de, ~25€, 21 juin |
| ESP32-CAM OV2640 (cartes seules) | 4 | ✅ REÇU | 23 juin |
| OV5640 DVP M12 | 5 | ✅ REÇU | 1× Camemake.eu (12 juin) + 4× AliExpress (24 juin) |
| USB-C TTL FT232RL | 3 | ✅ REÇU | AZDelivery Amazon, 9€, 21 juin |
| Commande Mouser #39492997 | 1 | ✅ REÇU | 8 juillet. MEMS TDK×2, IR 940nm×10, PIR×2, Buck TPS62840×5, Inductance 10µH×5, MOSFET SI2302×5, BME688×2, SHT31×2, Antenne LoRa×2, Dissipateur×4, Lot passifs CMS SparkFun 0603×1. 105,94€ + port. TPS62840DLCR arrivé avec 1 semaine d'avance sur ETA. |
| Miuzei Starter Kit Arduino | 1 | ✅ REÇU | 235 composants, breadboard — 10 juin |
| MP1584 DC-DC Step Down 3A | 5 | ✅ REÇU | Ultra-Small, réglable, remplace LM2596 — 3 juillet |
| Panier Mouser restant (11 composants BOM) | — | ⏳ À COMMANDER | ~279€ |

## STATION-DOMO / IoT

| Composant | Qté | Statut | Notes |
|-----------|-----|--------|-------|
| RPi 5 4GB | 1 | ✅ REÇU | Amazon, 132,09€, 10 juin |
| Alim officielle RPi5 27W | 1 | ✅ REÇU | 15,32€ |
| Refroidisseur actif RPi5 | 1 | ✅ REÇU | 9,99€ |
| Geekworm X1205 UPS HAT | 1 | ✅ REÇU | AliExpress, 42,39€ |
| Accus 18650 Flat 3400mAh CCC-5 SDIR18T | 20 | ✅ REÇU | Rose, 8 juillet 2026 |
| Geekworm X1201-C1 boîtier métal | 2 | ✅ REÇU | AliExpress, 18,59€, 29 juin |
| Sonoff ZBDongle-E (Zigbee) | 1 | ✅ REÇU | Amazon, 25,32€, 7 juin |
| SNZB-02DR2 Temphumid Zigbee | 1 | ✅ REÇU | 15,15€ |
| Sonoff Smart Water Valve | 1 | ✅ REÇU | Électrovanne connectée |
| Sonoff ZBMiniR2 (Zigbee) | 1 | ✅ REÇU | 8 juillet — smart switch Zigbee |
| PV PI HAT | 1 | ✅ REÇU | 150 AUD, reçu 1er juillet (avance sur prévision 15/08) |
| ADS1115 ADC Module 16-bit I2C (Heemol) | 3 | ✅ REÇU | Heemol, 9,21€, reçu 2 juillet |
| ADS1115 ADC 16-bit I2C HW-19S | 3 | ✅ REÇU | 8 juillet — PCB vert |
| ESP32-C3 Super Mini (Heemol) | 3 | ✅ REÇU | Heemol, 15,98€, reçu 2 juillet — détecteur niveau liquide |
| Step-Down HW-133 3A 5V DC-DC (Tecnoiot) | 5 | ✅ REÇU | 8 juillet — buck 24V-9V → 5V fixe, ultra-small |
| Aqara Light Sensor T1 (GZCGQ11LM) | 1 | ✅ REÇU | Zigbee — appairé 2 juillet, friendly_name: LuxSerre |
| Power Supply Adapter HS24A (24V) | 1 | ✅ REÇU | 8 juillet — alim 24V pour sonde TL-136 |
| Sonde hydrostatique TL-136 | 1 | ✅ REÇU | 8 juillet — capteur 4-20mA, détecteur niveau liquide |
| BOYA BY-MM1 | 1 | ✅ REÇU | Micro shotgun |
| UGREEN USB Audio | 1 | ✅ REÇU | Adaptateur audio RPi |
| PCIe to M.2 NVMe Shield | 2 | ✅ REÇU | 29 juin, pour SSD NVMe RPi 5 vanlife |
| SSD NVMe M.2 Fanxiang 256GB | 1 | ✅ REÇU | 1er juillet, pour RPi 5 vanlife |
| Assemblage RPi 5 vanlife | 1 | ✅ ASSEMBLÉ | RPi 5 + SSD + UPS HAT + accus 18650 — 8 juillet. Reste : mise en boîtier X1201-C1. |
| Samsung PRO Endurance 256GB microSD | 1 | ✅ REÇU | 17 juillet, Amazon. Remplace SD 128 Go actuelle pour HA OS 24/7. |
| Noctua NF-A4x10 PWM | 1 | ✅ REÇU | 19 juillet. Ventilateur 40×10mm silencieux pour RPi Lupo. |
| Reolink Argus MagiCam | 1 | ✅ REÇU | 17 juillet. Dashcam/sécurité Lupo, fixation aimantée. Voir `07_TRAVELS/van technique/securite/camera-reolink-argus-magicam-lupo.md`. |

## IT / Divers

| Composant | Qté | Statut | Notes |
|-----------|-----|--------|-------|
| UGREEN USB-C → Micro USB ×2 | 2 | ✅ REÇU | 10 juin |
| UGREEN USB-C Ethernet Gigabit | 1 | ✅ REÇU | 10 juin |
| ZTE MF833U1 LTE USB Modem | 1 | ✅ REÇU | Dongle 4G USB pour internet van — voir briefs vanlife-iot. |
| WiCAN Pro (OBD/CAN Ford) | 1 | ⏳ COMMANDÉ (backorder) | ~82€, Mouser. MS-CAN + HS-CAN. 17+ capteurs véhicule → HA. Voir `specs/SPEC-CAN-BUS.md` |
| Exosfer OBD Protect | 1 | ✅ REÇU | Antivol électronique prise OBD. ⚠️ Compatibilité WiCAN Pro à vérifier. |

## LEAFNET / WN-BIO

| Composant | Qté | Statut | Notes |
|-----------|-----|--------|-------|
| AD623ANZ | ? | ⏳ À COMMANDER | Ampli instrumentation |
| XIAO ESP32 | ? | ⏳ À ACQUÉRIR | Miniaturisation v0.2 |

---

*Source autoritaire. Synchronisé avec `docs/system/registre-achats.md`.*
