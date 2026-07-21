# Capteur Niveau Sonore (dB) — ESP32 + INMP441

> Fiche technique d'intégration du capteur de bruit ambiant dans le Stylevan Equinox 4
> Date : 2026-06-07 | Rédacteur : [[Dobby]] 🦉

## Résumé

Capteur de niveau sonore ambiant intérieur van basé sur **ESP32-S3 + INMP441 (MEMS I2S)**.
Exposition dans Home Assistant via **ESPHome** → entité `sensor.sound_level` avec valeur en dB SPL (A-weighted).

Budget : ~8 € | Phase : P1 (partage ESP32 avec l'inclinomètre MPU6050)

---

## 1. Matériel

| Composant | Qté | Prix |
|-----------|-----|------|
| Micro MEMS I2S INMP441 | 1 | ~3 € |
| ESP32-S3 (partagé avec MPU6050) | 1 | ~5 € (mutualisé) |
| Connecteurs + breadboard | 1 lot | ~2 € |
| Condensateur 100nF découplage | 1 | ~0.10 € |
| **Total capteur dB** | | **~6 €** |

---

## 2. Schéma de câblage

```
ESP32-S3               INMP441
───────                ───────
3.3V  ──────────────── VDD
                    ┌── GND
GND  ──────────────┼── L/R (→ GND = canal gauche)
                    │
                    └── GND (pad)

GPIO 4  ──────────── SD (DOUT)
GPIO 5  ──────────── WS (LRCLK)
GPIO 6  ──────────── SCK (BCLK)
```

Règles : fils < 10 cm, condensateur 100nF entre VDD et GND au plus près du micro.

---

## 3. ESPHome — Configuration

Framework obligatoire : **ESP-IDF** (l'I2S Arduino est instable sur S3).

```yaml
esphome:
  name: vanlife-sensor

esp32:
  board: esp32-s3-devkitc-1
  framework:
    type: esp-idf

i2s_audio:
  i2s_lrclk_pin: GPIO5
  i2s_bclk_pin: GPIO6

microphone:
  - platform: i2s_audio
    id: van_mic
    i2s_din_pin: GPIO4
    channel: left
    bits_per_sample: 16
    sample_rate: 16000
```

---

## 4. Algorithme de calcul dB

**Pipeline** : Buffer I2S 512 samples → float → filtre DC → RMS fenêtre 50ms → pondération A → dB SPL = 20 × log10(rms/rms_ref) → moyenne glissante 5s

**Calibration** : mesurer avec sonomètre d'appoint (NIOSH SLM sur iPhone), ajuster rms_ref.

| Environnement | dB typique |
|---------------|------------|
| Van campagne nuit | 25-35 dB |
| Van ville léger | 40-50 dB |
| Ventilateur toit | 45-55 dB |
| Conversation | 55-65 dB |
| Frigo cycle | 50-60 dB |
| Claquement porte | 75-85 dB |
| Seuil intrusion | > 85 dB pic |

---

## 5. Mutualisation ESP32 unique

Un seul ESP32-S3 = INMP441 (I2S) + MPU6050 (I2C) :

| Capteur | Protocole | Pins | Fréquence |
|---------|-----------|------|-----------|
| INMP441 | I2S | GPIO4/5/6 | Audio temps réel |
| MPU6050 | I2C | GPIO21/22 | 10 Hz suffit |

---

## 6. Entités HA exposées

- `sensor.vanlife_sound_level` — dB (moyenne 5s)
- `binary_sensor.vanlife_sound_peak` — pic > 85 dB
- `button.vanlife_sound_calibrate` — recalibration

---

## 7. Checklist validation terrain

- [ ] ESP32 flashé → entité visible dans HA
- [ ] Niveau cohérent avec app iPhone
- [ ] Pas de saturation à voix forte
- [ ] Mise à jour 5s réactive
- [ ] Pic > 85 dB détecté (claquer porte)
- [ ] Calibration avec sonomètre de référence
- [ ] Coexistence MPU6050 — pas de conflit I2C/I2S

---

## Références

- [[scenarios-algorithmes-vanlife]] — Scénarios 2.3 (confort dB) et 2.4 (alarme sonore)
- [[Liste IOT pour van]] — Capteur dB ajouté
- [INMP441 datasheet](https://invensense.tdk.com/wp-content/uploads/2015/02/INMP441.pdf)
- [ESPHome I2S Audio](https://esphome.io/components/i2s_audio.html)

---

*Document v1.0 — [[Dobby]] 🦉, 2026-06-07.*
