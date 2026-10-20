# LeafNet — Sonification & Monitoring Bioélectrique Végétal

**Date :** 2026-06-22
**Statut :** CONCEPT v0.1 — fork de NEXUS_ACOUSTIC
**Parent :** NEXUS_ACOUSTIC (projet 12)
**Origine :** Note Apple Notes ESP32-S3 → concept WN-BIO → décision JCH
**Spécialiste lead :** à désigner

---

## 1. Vision

LeafNet est le pendant végétal d'InsectNet. Là où InsectNet classifie les orthoptères par l'acoustique, LeafNet **capte les signaux bioélectriques des plantes** pour en dériver :

1. Une **sonification temps réel** (plante → MIDI → audio) — la plante comme instrument
2. Un **monitoring écologique** (stress hydrique, rythmes circadiens, activité animale)
3. Une **modalité de capteur inédite** pour la constellation WildNexus

---

## 2. Architecture

```
[Plante] → [Électrodes acier] → [AD620] → [ADC ESP32-S3] → [Core 0: sampling]
                                                              ↓
                                            [Core 1: BLE MIDI] → [Base Nexus / RPi]
                                                              ↓
                                            [Sonification] ∪ [Data logging]
```

### 2.1 Hardware

- **MCU** : ESP32-S3-DevKitC-1 (dual-core, ADC 12-bit, BLE)
- **Ampli** : AD623ANZ (instrumentation, DIP-8, CMRR 110 dB) — préféré à INA126 (94 dB) et TLC2272 (AOP, ~80 dB) pour les signaux µV en environnement bruyant
- **ADC réserve** : ADS1115 16-bit I2C (footprint optionnel)
- **Coût proto** : ~32 € (Mouser 26.82 € + passifs 5 €)
- **PPK2** : profilage énergétique obligatoire avant déploiement — procédure documentée dans `99_REFERENCES/sonification-iot-vegetal-esp32.md`

> Voir fiche concept complète : [`WILDNEXUS/03_P0_ENGINEERING/01_ARCHITECTURE_SYSTEME/2026-06-22_concept-noeud-bioelectrique.md`](../../03_WILDNEXUS/03_P0_ENGINEERING/01_ARCHITECTURE_SYSTEME/2026-06-22_concept-noeud-bioelectrique.md)

### 2.2 Firmware

- **Core 0** : boucle ADC continue, buffer circulaire, détection d'événements (écart-type glissant)
- **Core 1** : encodeur BLE MIDI → événements vers base
- **Bibliothèques** : ESP32-BLE-MIDI (Arduino IDE)
- **ESP-NOW** : firmware émetteur + récepteur prêts (5 optimisations deep sleep) → `99_REFERENCES/sonification-iot-vegetal-esp32.md`

### 2.3 Protocole

| Octet | Champ | Valeurs |
|---|---|---|
| 1 | Type + Canal | 0x90 = Note On (événement capteur) |
| 2 | ID Capteur | 0-127 (plante A, B, sol, etc.) |
| 3 | Amplitude | 0-127 (signal normalisé) |

---

## 3. Applications

### 3.1 Sonification (Consumer / Art/Science)
- Plante → flux MIDI → synthé / DAW
- « Écouter » le stress hydrique, le toucher, les rythmes jour/nuit
- Usage : démos, science citoyenne, expositions, éducation

### 3.2 Monitoring écologique (Scientific)
- Stress hydrique détecté avant symptômes visuels
- Rythmes circadiens corrélés lumière/température
- Impédance du sol (humidité par résistance)
- Détection de passage animal (pic au frôlement)

### 3.3 Intégration WildNexus P1
- Nœud bioélectrique dédié dans la constellation
- Communication BLE → Base Nexus locale
- Complémentaire au nœud caméra (P0) et au nœud audio (P1)

### 3.4 Intégration Home Assistant
- Hub ESP32 → MQTT → Home Assistant (ESPHome)
- La plante comme capteur domotique (stress hydrique → alerte visuelle)
- Alignement avec architecture HA distribuée (M5 Docker + Esneux RPi + van RPi)

---

## 4. Structure du projet

```
LEAFNET/
├── 00_SCOPE/          ← ce document + roadmap
├── 01_HARDWARE/       ← schémas, BOM, datasheets
├── 02_FIRMWARE/       ← code ESP32-S3 (ADC + BLE MIDI)
├── 03_DATA/           ← logs, visualisations, protocoles de test
└── 99_REFERENCES/     ← papers, liens, notes
```

---

## 5. Liens

| Projet | Relation |
|---|---|
| **WN-BIO** (WildNexus) | Concept hardware parent — le nœud LeafNet est l'instance WN-BIO |
| **InsectNet** (NEXUS_ACOUSTIC) | Projet frère — classification vs. sonification, insectes vs. plantes |
| **NEXUS_ACOUSTIC** | Projet parent — infrastructure bioacoustique commune |
| **Faune Autour** | Frontend PWA — dashboard de visualisation |

---

## 6. Roadmap hardware

| Phase | Matériel | Objectif | Prix |
|---|---|---|---|
| **v0.1 (banc)** | ESP32-S3-DevKitC-1 + AD623 | Validation signal → MIDI audible | ~32 € |
| **v0.2 (mini)** | XIAO ESP32C3 + AD623 | Miniaturisation, LiPo intégrée, terrain | ~15 € |
| **v0.3 (sci)** | XIAO RP2350W | ADC propre (< 1 LSB DNL), PIO sampling | ~20 € |

> Voir analyse complète : [`01_HARDWARE/miniaturization-analysis.md`](../01_HARDWARE/miniaturization-analysis.md)

### Protocoles télémetrie

| Protocole | Usage LeafNet | Portée | Latence |
|---|---|---|---|
| **BLE MIDI** | Sonification temps réel → DAW/synthé | 10-100 m | < 10 ms |
| **ESP-NOW** | Monitoring terrain → Base Nexus | 200-500 m | < 5 ms |
| **Wi-Fi** | Debug, bulk data download | 50-100 m | Variable |

---

## 7. Prochaines étapes

- [x] Concept WN-BIO validé Forge
- [x] BOM Mouser préparé (push depuis RPi)
- [x] Structure LeafNet créée
- [ ] Commande composants
- [ ] Désigner spécialiste lead LeafNet
- [ ] Proto breadboard : ESP32-S3 + AD623 + électrodes sur plante
- [ ] Firmware v0.1 : ADC sampling + BLE MIDI output
- [ ] Test : sonification audible + corrélation arrosage

---

*Généré par Dobby 🦉 — 2026-06-22*
