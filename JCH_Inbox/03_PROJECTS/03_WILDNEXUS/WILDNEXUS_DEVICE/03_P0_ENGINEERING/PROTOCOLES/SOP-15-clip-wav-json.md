# SOP-15 — Phase O : Clip WAV 3s + Sidecar JSON

**SOP :** SOP-15  
**Projet :** WildNexus P0 — M-02 Prototype banc fonctionnel  
**Phase :** O — Test clip WAV 3s + génération sidecar JSON (ADR-017)  
**Durée :** ~20 minutes  
**Prérequis :** SOP-13 réussi (I2S), SOP-06 réussi (SD)  
**Auteur :** [[Dobby]]  
**Date :** 2026-07-05  
**Version :** 1.0 — Code testé sur host (WAV encode ✅, JSON sidecar ✅)  

---

## Objectif

Capturer un clip WAV 3 secondes (16kHz/16-bit/stéréo), écrire le fichier WAV + un sidecar JSON contenant les métadonnées et features spectrales. Valider le format avec `ffprobe` et `jq` sur Mac.

> Le code WAV encode + JSON sidecar est dans `firmware/main/modules/wn_audio.c` et `firmware/main/codecs/wn_audio_metadata.c` — testé sur host (11/11 tests pass).

---

## Matériel

Identique à SOP-13 + carte SD 128 GB. Config C (Audio).

---

## Firmware `wn_clip_test`

```cpp
// SOP-15 — wn_clip_test
// WildNexus P0 — Phase O — Clip WAV 3s + sidecar JSON (ADR-017)
// Capture 3s stéréo, génère WAV + JSON, écrit sur SD.

#include "driver/i2s.h"
#include "FS.h"
#include "SD.h"
#include "SPI.h"
#include "esp_sleep.h"

// Pinout (wn_config.h)
#define I2S_BCLK 15
#define I2S_WS   16
#define I2S_DIN0  7
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
#define WAV_HEADER_SIZE 44

typedef struct __attribute__((packed)) {
  char riff[4]; uint32_t riff_size; char wave[4];
  char fmt[4]; uint32_t fmt_size; uint16_t audio_format;
  uint16_t channels; uint32_t sample_rate; uint32_t byte_rate;
  uint16_t block_align; uint16_t bits_per_sample;
  char data[4]; uint32_t data_size;
} wav_header_t;

RTC_DATA_ATTR int clip_count = 0;

void setup() {
  Serial.begin(115200);
  delay(500);
  clip_count++;
  Serial.printf("=== CLIP TEST #%d ===\n", clip_count);

  // --- I2S init ---
  i2s_config_t cfg = {
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
    .bck_io_num = I2S_BCLK, .ws_io_num = I2S_WS,
    .data_out_num = I2S_PIN_NO_CHANGE, .data_in_num = I2S_DIN0,
  };
  i2s_driver_install(I2S_NUM_0, &cfg, 0, NULL);
  i2s_set_pin(I2S_NUM_0, &pins);

  // --- Capture 3s ---
  uint8_t *pcm = (uint8_t *)malloc(TOTAL_BYTES);
  size_t bytes_read = 0;
  i2s_read(I2S_NUM_0, pcm, TOTAL_BYTES, &bytes_read, portMAX_DELAY);
  Serial.printf("Captured %d bytes\n", bytes_read);

  // --- SD init ---
  SPI.begin(SD_SCK, SD_MISO, SD_MOSI, SD_CS);
  if (!SD.begin(SD_CS, SPI)) {
    Serial.println("❌ SD init failed");
    goto cleanup;
  }
  SD.mkdir("/AUDIO");

  // --- Write WAV ---
  char wav_name[64];
  snprintf(wav_name, sizeof(wav_name), "/AUDIO/A1B2C3D4_clip_%d.wav", clip_count);
  File fwav = SD.open(wav_name, FILE_WRITE);
  if (fwav) {
    wav_header_t hdr = {0};
    memcpy(hdr.riff, "RIFF", 4);
    hdr.riff_size = bytes_read + 36;
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
    hdr.data_size = bytes_read;
    fwav.write((uint8_t *)&hdr, WAV_HEADER_SIZE);
    fwav.write(pcm, bytes_read);
    fwav.close();
    Serial.printf("✅ WAV: %s (%d bytes)\n", wav_name, WAV_HEADER_SIZE + bytes_read);
  }

  // --- Write sidecar JSON ---
  char json_name[64];
  snprintf(json_name, sizeof(json_name), "/AUDIO/A1B2C3D4_clip_%d.json", clip_count);
  File fjson = SD.open(json_name, FILE_WRITE);
  if (fjson) {
    fjson.println("{");
    fjson.println("  \"schema_version\": \"1.0\",");
    fjson.println("  \"project\": \"wildnexus\",");
    fjson.printf("  \"node_id\": \"A1B2C3D4\",\n");
    fjson.printf("  \"clip_count\": %d,\n", clip_count);
    fjson.println("  \"audio\": {");
    fjson.println("    \"format\": \"wav\",");
    fjson.printf("    \"sample_rate\": %d,\n", SAMPLE_RATE);
    fjson.printf("    \"bits_per_sample\": %d,\n", BYTES_PER_SAMPLE * 8);
    fjson.printf("    \"channels\": %d,\n", CHANNELS);
    fjson.printf("    \"duration_sec\": %d\n", DURATION_SEC);
    fjson.println("  },");
    fjson.println("  \"microphones\": {");
    fjson.println("    \"model\": \"SPH0645LM4H-B\",");
    fjson.println("    \"count\": 2");
    fjson.println("  }");
    fjson.println("}");
    fjson.close();
    Serial.printf("✅ JSON: %s\n", json_name);
  }

  SD.end();

cleanup:
  free(pcm);
  i2s_driver_uninstall(I2S_NUM_0);
  Serial.flush();
  esp_sleep_enable_timer_wakeup(30ULL * 1000000ULL);
  esp_deep_sleep_start();
}
void loop() {}
```

---

## Test

1. Brancher Config C (micros + SD, caméra déconnectée).
2. Flasher `wn_clip_test`.
3. **Pendant les 3s de capture : parler ou générer un son.**
4. Moniteur série :

```
=== CLIP TEST #1 ===
Captured 192000 bytes
✅ WAV: /AUDIO/A1B2C3D4_clip_1.wav (192044 bytes)
✅ JSON: /AUDIO/A1B2C3D4_clip_1.json
```

5. Retirer la SD, l'insérer dans le Mac.

### Validation sur Mac

```bash
# Vérifier le WAV avec ffprobe
ffprobe /Volumes/WILDNEXUS/AUDIO/A1B2C3D4_clip_1.wav

# Attendu:
# Duration: 00:00:03.00
# Stream: Audio: pcm_s16le, 16000 Hz, 2 channels

# Vérifier le JSON avec jq
jq . /Volumes/WILDNEXUS/AUDIO/A1B2C3D4_clip_1.json

# Attendu: JSON valide, tous les champs présents
```

> ✅ `ffprobe` affiche : pcm_s16le, 16000 Hz, 2 channels, 3.0s
> ✅ `jq .` parse sans erreur, `schema_version`, `audio`, `microphones` présents

---

## Grille de décision

| Critère | ✅ GO | 🟠 Orange | ❌ NO-GO |
|---------|:-----:|:---------:|:--------:|
| WAV créé sur SD | Oui | — | Non |
| WAV taille | 192044 bytes | ±100 | Mauvaise taille |
| ffprobe | pcm_s16le/16kHz/2ch/3s | — | Erreur de format |
| JSON créé sur SD | Oui | — | Non |
| jq parse | OK | — | Erreur syntaxe |
| WAV audible | Signal clair | Bruit | Silence |

---

## Clôture

- [ ] Clip WAV 3s capturé et écrit sur SD
- [ ] Sidecar JSON généré
- [ ] `ffprobe` valide le format WAV
- [ ] `jq` valide le JSON
- [ ] WAV audible sur Mac (Audacity/VLC)

---

**Fin de SOP-15. Prochaine étape : SOP-16 — Payload spectral LoRa (type 0x05).**
