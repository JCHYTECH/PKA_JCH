# SOP-13 — Phase M : Test I2S MEMS stéréo (SPH0645LM4H-B ×2)

**SOP :** SOP-13  
**Projet :** WildNexus P0 — M-02 Prototype banc fonctionnel  
**Phase :** M — Test micros MEMS I2S stéréo  
**Durée :** ~25 minutes  
**Prérequis :** SOP-05 réussi, SPH0645LM4H-B ×2 disponibles (Mouser #39492997)  
**Auteur :** [[Dobby]]  
**Date :** 2026-07-05  
**Version :** 1.0 — Créée suite à ADR-013 (I2S stéréo) + extraction de SOP-12  

---

## Objectif

Vérifier que les 2 micros MEMS SPH0645LM4H-B s'initialisent via I2S, captent un signal audio stéréo, et retournent en veille. Mesurer la consommation.

> ⚠️ **Config de test :** Config C (Audio). **Caméra DÉCONNECTÉE** — GPIO 6,7 libérés pour I2S DIN.

---

## Matériel spécifique

| # | Élément |
|---|---------|
| 1 | 2× SPH0645LM4H-B ( Knowles, I2S digital MEMS) |
| 2 | 6-8 câbles Dupont femelle-femelle |
| 3 | Casque ou écouteurs (pour vérifier le WAV sur Mac) |

---

## Pinout (wn_config.h — ADR-013)

| Signal | ESP32-S3 GPIO | Note |
|--------|:------------:|------|
| VCC (mic L) | 3V3 | 3.3V |
| GND (mic L) | GND | |
| BCLK | **GPIO 15** | Bit clock — partagé par les 2 micros |
| WS / LRCL | **GPIO 16** | Word select (L/R) — partagé |
| DIN (mic L) | **GPIO 7** | Data from mic #1 — ⚠️ partagé Camera D3 |
| VCC (mic R) | 3V3 | |
| GND (mic R) | GND | |
| DIN (mic R) | **GPIO 6** | Data from mic #2 — ⚠️ partagé Camera D2 |

> **Configuration stéréo :** Les 2 micros partagent BCLK et WS. Le signal WS détermine le canal : L sur front descendant, R sur front montant. DIN de chaque micro sur un GPIO séparé (I2S0 pour L, I2S1 pour R).

> ⚠️ **Ancien pinout SOP-12 (v1.0) :** micro analogique sur ADC GPIO 4. **Obsolète.** ADR-013 (19/06) a remplacé le micro analogique par 2× SPH0645LM4H-B I2S digital stéréo.

```
        ESP32-S3 DevKit          Mic L (SPH0645)      Mic R (SPH0645)
        ┌──────────────┐         ┌──────────┐         ┌──────────┐
        │  3V3 ────────┼─[rouge]─┼── VCC    │         │          │
        │  GND ────────┼─[noir]──┼── GND    │  3V3────┼── VCC    │
        │  IO15 ───────┼─[jaune]─┼── BCLK   │  GND────┼── GND    │
        │  IO16 ───────┼─[bleu]──┼── WS     │  IO15───┼── BCLK   │
        │  IO7  ───────┼─[vert]──┼── DIN    │  IO16───┼── WS     │
        │              │         └──────────┘  IO6────┼── DIN    │
        │              │                        └──────────┘
        └──────────────┘
```

---

## Étape 1 — Firmware `wn_i2s_test` (5 minutes)

Ce firmware initialise l'I2S, capture 3 secondes de stéréo, sauve un WAV sur SD, puis dort.

```cpp
// SOP-13 — wn_i2s_test v1
// WildNexus P0 — Phase M — Test I2S MEMS stéréo (ADR-013)
// Capture 3s de stéréo 16kHz/16-bit, sauve WAV sur SD.

#include "driver/i2s.h"
#include "FS.h"
#include "SD.h"
#include "SPI.h"
#include "esp_sleep.h"

// Pinout I2S (wn_config.h)
#define I2S_BCLK  15
#define I2S_WS    16
#define I2S_DIN0   7  // Mic L
#define I2S_DIN1   6  // Mic R (I2S1)

// Pinout SD (wn_config.h)
#define SD_CS   39
#define SD_SCK  40
#define SD_MISO 41
#define SD_MOSI 42

#define SAMPLE_RATE 16000
#define DURATION_SEC 3
#define CHANNELS 2
#define BYTES_PER_SAMPLE 2
#define TOTAL_SAMPLES (SAMPLE_RATE * DURATION_SEC)
#define TOTAL_BYTES (TOTAL_SAMPLES * CHANNELS * BYTES_PER_SAMPLE)

// WAV header (44 bytes — ADR-017)
typedef struct __attribute__((packed)) {
  char     riff[4]; uint32_t riff_size; char wave[4];
  char     fmt[4];  uint32_t fmt_size;   uint16_t audio_format;
  uint16_t channels; uint32_t sample_rate; uint32_t byte_rate;
  uint16_t block_align; uint16_t bits_per_sample;
  char     data[4]; uint32_t data_size;
} wav_header_t;

RTC_DATA_ATTR int test_count = 0;

void setup() {
  Serial.begin(115200);
  delay(500);
  test_count++;
  Serial.printf("=== I2S TEST #%d ===\n", test_count);

  // --- Init I2S ---
  i2s_config_t i2s_config = {
    .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX),
    .sample_rate = SAMPLE_RATE,
    .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
    .channel_format = I2S_CHANNEL_FMT_RIGHT_LEFT,
    .communication_format = I2S_COMM_FORMAT_STAND_I2S,
    .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
    .dma_buf_count = 4,
    .dma_buf_len = 1024,
    .use_apll = false,
  };
  i2s_pin_config_t pins = {
    .bck_io_num = I2S_BCLK,
    .ws_io_num = I2S_WS,
    .data_out_num = I2S_PIN_NO_CHANGE,
    .data_in_num = I2S_DIN0,
  };
  
  esp_err_t err = i2s_driver_install(I2S_NUM_0, &i2s_config, 0, NULL);
  if (err != ESP_OK) {
    Serial.printf("❌ I2S init failed: %s\n", esp_err_to_name(err));
    goto sleep;
  }
  i2s_set_pin(I2S_NUM_0, &pins);
  Serial.println("✅ I2S init OK (16kHz, 16-bit, stereo)");

  // --- Capture 3s ---
  uint8_t *buffer = (uint8_t *)malloc(TOTAL_BYTES);
  if (!buffer) {
    Serial.println("❌ malloc failed");
    goto sleep;
  }
  
  size_t bytes_read = 0;
  esp_err_t rd = i2s_read(I2S_NUM_0, buffer, TOTAL_BYTES, &bytes_read, portMAX_DELAY);
  Serial.printf("Captured %d bytes (%d samples)\n", bytes_read, bytes_read / (CHANNELS * BYTES_PER_SAMPLE));

  // --- Init SD + write WAV ---
  SPI.begin(SD_SCK, SD_MISO, SD_MOSI, SD_CS);
  if (SD.begin(SD_CS, SPI)) {
    SD.mkdir("/AUDIO");
    
    // Build filename
    char fname[64];
    snprintf(fname, sizeof(fname), "/AUDIO/wn_i2s_test_%d.wav", test_count);
    
    File f = SD.open(fname, FILE_WRITE);
    if (f) {
      // Write WAV header
      wav_header_t hdr;
      memcpy(hdr.riff, "RIFF", 4);
      hdr.riff_size = TOTAL_BYTES + 36;
      memcpy(hdr.wave, "WAVE", 4);
      memcpy(hdr.fmt, "fmt ", 4);
      hdr.fmt_size = 16;
      hdr.audio_format = 1;
      hdr.channels = CHANNELS;
      hdr.sample_rate = SAMPLE_RATE;
      hdr.byte_rate = SAMPLE_RATE * CHANNELS * BYTES_PER_SAMPLE;
      hdr.block_align = CHANNELS * BYTES_PER_SAMPLE;
      hdr.bits_per_sample = 16;
      memcpy(hdr.data, "data", 4);
      hdr.data_size = TOTAL_BYTES;
      
      f.write((uint8_t *)&hdr, sizeof(hdr));
      f.write(buffer, bytes_read);
      f.close();
      Serial.printf("✅ WAV written: %s (%d bytes)\n", fname, sizeof(hdr) + bytes_read);
    } else {
      Serial.println("❌ SD write failed");
    }
    SD.end();
  } else {
    Serial.println("⚠️ SD not available — audio not saved");
  }

  free(buffer);
  i2s_driver_uninstall(I2S_NUM_0);

sleep:
  Serial.flush();
  esp_sleep_enable_timer_wakeup(30ULL * 1000000ULL);
  esp_deep_sleep_start();
}
void loop() {}
```

---

## Étape 2 — Branchement (5 minutes)

1. **Caméra DÉCONNECTÉE** (Config C).
2. Brancher les 2 micros : VCC 3V3, GND, BCLK→15, WS→16, DIN L→7, DIN R→6.
3. Brancher le module SD (Config B/C — pins 39-42).
4. Insérer carte SD 128 GB formatée FAT32.

---

## Étape 3 — Test fonctionnel (5 minutes)

1. ESP32 USB branché + micros + SD.
2. Flasher `wn_i2s_test`.
3. Moniteur série 115200 baud.

```
=== I2S TEST #1 ===
✅ I2S init OK (16kHz, 16-bit, stereo)
Captured 192000 bytes (48000 samples)
✅ WAV written: /AUDIO/wn_i2s_test_1.wav (192044 bytes)
```

4. **Pendant la capture (3s) : parler ou claquer des doigts devant les micros.**
5. Retirer la SD, l'insérer dans le Mac.
6. Ouvrir `/AUDIO/wn_i2s_test_1.wav` dans Audacity ou VLC.

> ✅ Le WAV s'ouvre, stéréo, 16kHz, 16-bit, 3 secondes, signal audible → micros fonctionnels.

> ❌ `I2S init failed` : vérifier BCLK=15, WS=16, DIN sur 7 et 6.
> ❌ WAV silencieux : vérifier VCC 3V3 sur les micros, polarité DIN.

---

## Étape 4 — Mesure PPK2 (5 minutes)

| Mesure | Valeur attendue |
|--------|-----------------|
| Deep sleep avec micros branchés | < 150 µA (SPH0645 sleep = ~10 µA) |
| Pic I2S capture (3s) | ~30 mA (ESP32 + I2S actif) |
| Durée active | ~4s (init + capture + SD write) |
| Charge cycle audio (mAh) | ~0,03 mAh |

---

## Grille de décision

| Critère | ✅ GO | 🟠 Orange | ❌ NO-GO |
|---------|:-----:|:---------:|:--------:|
| I2S init | OK | 1 retry | Échec |
| Capture stéréo | 2 canaux actifs | 1 canal | Aucun |
| WAV lisible | Signal audible | Bruit seul | Fichier corrompu |
| WAV format | 16kHz/16-bit/stéréo/3s | — | Mauvais format |
| Deep sleep + micros | < 150 µA | 150-300 µA | > 300 µA |

---

## Clôture

- [ ] 2 micros SPH0645LM4H-B branchés (BCLK=15, WS=16, DIN L=7, DIN R=6)
- [ ] I2S init OK
- [ ] Capture stéréo 3s sur SD
- [ ] WAV lisible sur Mac (Audacity/VLC)
- [ ] Mesure PPK2 : capture + deep sleep micros

---

**Fin de SOP-13. Prochaine étape : SOP-14 — FFT features spectrales.**
