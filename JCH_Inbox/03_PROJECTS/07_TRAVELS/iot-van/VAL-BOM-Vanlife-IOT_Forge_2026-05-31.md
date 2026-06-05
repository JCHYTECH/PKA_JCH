# BOM — Vanlife IOT Phase 0-1
# Raspberry Pi 5 + Home Assistant pour Stylevan Equinox 4

**Date :** 2026-05-31
**Base :** [[projet-vanlife-iot]].md + [[rpi-vanlife-guide-complet]].md
**Mise à jour :** Spécifications solaires 280W validées (MPPT 100/20).

---

## Phase 0-1 — Setup base

| # | Composant | Modele | Qté | Prix unit. | Total |
|---|----------|--------|-----|-----------|-------|
| 1 | Raspberry Pi 5 8 Go | RPi5-8GB | 1 | ~80 | 80 |
| 2 | Boitier alu passif | Flirc RPi 5 | 1 | ~15 | 15 |
| 3 | SSD NVMe M.2 128 Go | Samsung/WD | 1 | ~20 | 20 |
| 4 | Adaptateur HAT NVMe | Pimoroni NVMe Base | 1 | ~25 | 25 |
| 5 | Convertisseur DC 12V-5V USB-C PD 5A | DFRobot DFR1017 | 1 | ~10 | 10 |
| 6 | Cable USB-C PD e-mark 1m | 5A | 1 | ~5 | 5 |
| 7 | Porte-fusible derivateur mini ATP | | 1 | ~3 | 3 |
| 8 | Fusible 5A mini | ATP 5A | 2 | ~1 | 2 |
| 9 | Interrupteur a bascule 12V | SPST 10A | 1 | ~5 | 5 |
| 10 | Cle USB Zigbee | Sonoff ZBDongle-E | 1 | ~20 | 20 |
| 11 | Capteur temperature Zigbee | Sonoff SNZB-02 | 2 | ~8 | 16 |
| 12 | Capteur ouverture porte | Aqara MCCGQ11LM | 5 | ~8 | 40 |
| 13 | Cables electriques + gaine | 1.5mm2 rouge/noir 2m | 1 | ~5 | 5 |
| **Total Phase 0-1** | | | | **~246 EUR** |

---

## Phase 2 — GPS + Inclinaison + Relais + Présence extérieure

| # | Composant | Modele | Qté | Prix | Total |
|---|----------|--------|-----|------|-------|
| 14 | Cle USB GPS | u-blox 7 VK-172 | 1 | ~12 | 12 |
| 15 | ESP32 + MPU6050 | AZDelivery + GY-521 | 1 | ~10 | 10 |
| 16 | Module relais 12V 2 canaux | SRD-12VDC | 1 | ~5 | 5 |
| 17 | Electro-aimant 12V | pour verrou tiroir | 2 | ~2 | 4 |
| 18 | PIR extérieur 12V IP65 | alarme-grade (ex. Optex/Paradox) | 1 | ~12 | 12 |
| 19 | Contact sec Zigbee | Sonoff SNZB-04 | 1 | ~8 | 8 |
| 20 | Spot LED extérieur 12V + câbles | | 1 | ~5 | 5 |
| **Total Phase 2** | | | | **~56 EUR** |

---

## Phase 3 — Solaire + Jauges

| # | Composant | Modele | Qté | Prix | Total |
|---|----------|--------|-----|------|-------|
| 18 | MPPT Victron SmartSolar 100/20 | SCC110020060R | 1 | ~105 | 105 |
| 19 | Victron SmartShunt 500A | SHU050150050 | 1 | ~90 | 90 |
| 20 | Cable VE.Direct USB | ASS030530009 | 2 | ~20 | 40 |
| 21 | Capteur ultrason etanche | JSN-SR04T | 2 | ~5 | 10 |
| 22 | Cable + divers | | 1 | ~5 | 5 |
| **Total Phase 3** | | | | **~250 EUR** |

---

## Total general : ~552 EUR

---

## A commander avant demarrage

- [ ] Phase 0-1 complete (13 lignes)
- [ ] Validation garantie [[Renard]] prealable
- [ ] Mesure longueur cables dans le van

## Lecons WildNexus integrees

- SSD obligatoire (pas microSD) — corruption chronique
- USB-C PD 5A obligatoire pour Pi 5 — undervoltage sinon
- Porte-fusible derivateur sur F3 du DS300 — cf cahier technique
- Stockage API REST, pas SQLite direct
