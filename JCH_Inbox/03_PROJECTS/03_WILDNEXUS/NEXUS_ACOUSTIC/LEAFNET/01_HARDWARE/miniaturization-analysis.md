# LeafNet — Analyse Miniaturisation & Alternatives Hardware

**Date :** 2026-06-22
**Source :** Note Apple Notes ESP32-S3 (mise à jour 2026-06-22 07:37)
**Statut :** Analyse pour roadmap LeafNet v0.2

---

## 1. Résumé

La note Apple Notes mise à jour apporte une section cruciale sur la miniaturisation. Le ESP32-S3-DevKitC-1 (~8 cm × 5 cm) est le point de départ pour le prototypage, mais le déploiement terrain exige des formats bien plus compacts. La note identifie deux familles de candidats.

---

## 2. Candidats miniaturisés

### 2.1 XIAO ESP32C3 (Seeed Studio) ⭐ Recommandé

| Caractéristique | Valeur |
|---|---|
| Dimensions | 21 × 17.5 mm (timbre-poste) |
| MCU | ESP32-C3 (RISC-V 32-bit, 160 MHz) |
| Wi-Fi / BLE 5.0 | ✅ |
| ADC | 12-bit SAR (4 canaux) |
| Charge LiPo | ✅ Intégré (connecteur JST) |
| GPIO | 11 pins |
| Prix | ~5 € |

**Avantages pour LeafNet** :
- Charge LiPo intégrée → simplification massive de l'alimentation terrain
- Format assez petit pour être suspendu à une branche
- Wi-Fi + BLE pour télémetrie
- Prix imbattable

**Limites** :
- ADC 12-bit avec les mêmes non-linéarités que l'ESP32-S3
- Single-core (pas de dual-core comme le S3)
- Moins de GPIO pour capteurs additionnels

### 2.2 M5Stack AtomS3 / StampS3

| Caractéristique | Valeur |
|---|---|
| Dimensions | 24 × 24 mm (AtomS3) |
| MCU | ESP32-S3 (dual-core Xtensa LX7) |
| Wi-Fi / BLE 5.0 | ✅ |
| Écran | 0.85" LCD RGB (AtomS3 uniquement) |
| Gyroscope 6 axes | ✅ (AtomS3) |
| GPIO | 6 pins (StampS3: plus) |
| Prix | ~15 € (AtomS3) / ~8 € (StampS3) |

**Avantages pour LeafNet** :
- Dual-core comme le DevKit → même architecture firmware
- Écran intégré sur AtomS3 → feedback visuel direct (niveau signal, statut BLE)
- Boîtier fermé, prêt à l'emploi

**Limites** :
- Plus cher que XIAO
- Peu de GPIO exposés sur AtomS3

### 2.3 XIAO RP2350 (Raspberry Pi Pico 2)

| Caractéristique | Valeur |
|---|---|
| Dimensions | 21 × 17.5 mm |
| MCU | RP2350 (dual-core ARM Cortex-M33 + RISC-V Hazard3) |
| ADC | **12-bit, 500 ksps, < 1 LSB DNL** |
| PIO (Programmable I/O) | ✅ 12 machines d'état |
| Wi-Fi / BLE | Version "W" uniquement |
| Prix | ~6 € (version W: ~8 €) |

**Avantages pour LeafNet** :
- **Meilleur ADC de sa catégorie** — DNL < 1 LSB, pas de non-linéarité comme l'ESP32
- PIO permet échantillonnage déterministe sans CPU
- Dual-core Cortex-M33 puissant pour DSP embarqué
- La note le cite explicitement pour la « précision scientifique du signal »

**Limites** :
- Version Wi-Fi plus chère et moins mature que l'écosystème ESP32
- Pas de BLE MIDI natif — bibliothèques à vérifier
- Écosystème plus jeune que ESP-IDF/Arduino pour ESP32

---

## 3. Roadmap hardware LeafNet

| Phase | Matériel | Objectif |
|---|---|---|
| **Proto v0.1** | ESP32-S3-DevKitC-1 + AD623 | Validation concept : signal plante → BLE MIDI audible |
| **Proto v0.2** | XIAO ESP32C3 + AD623 | Miniaturisation, test autonomie LiPo |
| **Proto v0.3** | XIAO RP2350W | Évaluation ADC supérieur, PIO sampling |
| **Déploiement** | À déterminer selon résultats v0.2/v0.3 | |

---

## 4. Impact sur l'architecture LeafNet

### 4.1 Protocole : BLE MIDI vs ESP-NOW

La note mentionne ESP-NOW comme troisième option (avec Wi-Fi et BLE). Comparaison :

| Protocole | Portée | Latence | Conso | Bibliothèques |
|---|---|---|---|---|
| BLE MIDI | 10-100 m | < 10 ms | Moyenne | Excellentes (ESP32-BLE-MIDI) |
| ESP-NOW | 200-500 m | < 5 ms | Très faible | Bonnes (ESPNOW.h) |
| Wi-Fi | 50-100 m | Variable | Élevée | Excellentes |

**Recommandation** : BLE MIDI pour la sonification (compatibilité DAW/synthé), ESP-NOW pour le monitoring terrain (portée, conso). Les deux peuvent coexister sur le même MCU.

### 4.2 Alimentation

La charge LiPo intégrée du XIAO change la donne. Plus besoin de powerbank externe — une simple LiPo 500 mAh suffit pour :
- XIAO + AD623 en continu : ~35 mA → ~14 heures
- XIAO en sleep cyclique (ESP-NOW) : ~5 mA moyen → ~100 heures

---

## 5. Points à intégrer dans le scope LeafNet

1. **Roadmap hardware en 3 phases** (DevKit → XIAO → RP2350)
2. **ESP-NOW comme protocole monitoring** (en parallèle du BLE MIDI sonification)
3. **LiPo intégrée** comme standard d'alimentation à partir de v0.2
4. **ADC sampling** : prévoir abstraction layer pour supporter ESP32 ADC ET RP2350 ADC/PIO
5. **Référence PlantWave** : la note cite implicitement ce produit commercial comme benchmark

---

*Analyse Dobby 🦉 — 2026-06-22*
