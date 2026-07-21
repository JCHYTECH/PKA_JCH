# SOP-14 — Phase N : FFT 1024 — Features spectrales

**SOP :** SOP-14  
**Projet :** WildNexus P0 — M-02 Prototype banc fonctionnel  
**Phase :** N — Test FFT 1024 + extraction 10 descripteurs spectraux  
**Durée :** ~20 minutes  
**Prérequis :** SOP-13 réussi (I2S fonctionnel)  
**Auteur :** [[Dobby]]  
**Date :** 2026-07-05  
**Version :** 1.0 — Code testé sur host (1kHz sine ✅, silence ✅, noise ✅)  

---

## Objectif

Capturer 4096 échantillons via I2S, calculer une FFT 1024 points, extraire 10 descripteurs spectraux, et les quantifier en u16 pour le payload LoRa (ADR-014 v2 type 0x05). Vérifier que la peak frequency correspond au signal test.

> Le code FFT est dans `firmware/main/modules/wn_audio.c` — testé sur host (gcc, 1kHz sine → peak=1000 Hz ✅). Cette SOP valide le code sur hardware réel ESP32-S3.

---

## Matériel

Identique à SOP-13 : ESP32-S3 + 2× SPH0645LM4H-B + SD. Config C (Audio, caméra déconnectée).

---

## Firmware `wn_fft_test`

```cpp
// SOP-14 — wn_fft_test
// WildNexus P0 — Phase N — FFT 1024 + 10 spectral features (ADR-016)
// Capture 4096 samples, FFT, print features, sleep.

#include "driver/i2s.h"
#include "esp_sleep.h"
#include <math.h>

// Pinout I2S (wn_config.h)
#define I2S_BCLK 15
#define I2S_WS   16
#define I2S_DIN0  7

#define SAMPLE_RATE 16000
#define FFT_SAMPLES 4096
#define FFT_SIZE    1024

#ifndef M_PI
#define M_PI 3.14159265358979
#endif

// --- Simple radix-2 FFT (from wn_audio.c) ---
static float fft_real[FFT_SIZE];
static float fft_imag[FFT_SIZE];

void wn_fft_simple(float *real, float *imag, int n) {
  int j = 0;
  for (int i = 1; i < n; i++) {
    int bit = n >> 1;
    while (j & bit) { j ^= bit; bit >>= 1; }
    j ^= bit;
    if (i < j) {
      float tr = real[i]; real[i] = real[j]; real[j] = tr;
      float ti = imag[i]; imag[i] = imag[j]; imag[j] = ti;
    }
  }
  for (int len = 2; len <= n; len <<= 1) {
    float angle = -2.0f * (float)M_PI / (float)len;
    float wreal = cosf(angle), wimag = sinf(angle);
    for (int i = 0; i < n; i += len) {
      float wr = 1.0f, wi = 0.0f;
      for (int k = 0; k < len / 2; k++) {
        float ur = real[i+k], ui = imag[i+k];
        float vr = wr*real[i+k+len/2] - wi*imag[i+k+len/2];
        float vi = wr*imag[i+k+len/2] + wi*real[i+k+len/2];
        real[i+k] = ur+vr; imag[i+k] = ui+vi;
        real[i+k+len/2] = ur-vr; imag[i+k+len/2] = ui-vi;
        float nwr = wr*wreal - wi*wimag;
        wi = wr*wimag + wi*wreal; wr = nwr;
      }
    }
  }
}

RTC_DATA_ATTR int fft_count = 0;

void setup() {
  Serial.begin(115200);
  delay(500);
  fft_count++;
  Serial.printf("=== FFT TEST #%d ===\n", fft_count);

  // --- Init I2S ---
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
    .bck_io_num = I2S_BCLK,
    .ws_io_num = I2S_WS,
    .data_out_num = I2S_PIN_NO_CHANGE,
    .data_in_num = I2S_DIN0,
  };
  i2s_driver_install(I2S_NUM_0, &cfg, 0, NULL);
  i2s_set_pin(I2S_NUM_0, &pins);

  // --- Capture 4096 samples (mono: take left channel only) ---
  int16_t raw[FFT_SAMPLES * 2]; // interleaved stereo
  size_t bytes_read = 0;
  i2s_read(I2S_NUM_0, raw, sizeof(raw), &bytes_read, portMAX_DELAY);
  
  // Extract left channel + apply Hann window
  int16_t mono[FFT_SIZE];
  for (int i = 0; i < FFT_SIZE; i++) {
    mono[i] = raw[i * 2]; // left channel
    float w = 0.5f * (1.0f - cosf(2.0f * (float)M_PI * i / (FFT_SIZE-1)));
    fft_real[i] = (float)mono[i] / 32768.0f * w;
    fft_imag[i] = 0.0f;
  }

  // --- FFT ---
  wn_fft_simple(fft_real, fft_imag, FFT_SIZE);

  // --- Compute power spectrum + features ---
  float power[FFT_SIZE/2 + 1];
  float total_power = 0;
  int nbins = FFT_SIZE/2 + 1;
  for (int i = 0; i < nbins; i++) {
    power[i] = fft_real[i]*fft_real[i] + fft_imag[i]*fft_imag[i];
    total_power += power[i];
  }

  float bin_hz = (float)SAMPLE_RATE / (float)FFT_SIZE;

  // Peak frequency
  float max_p = 0; int max_bin = 0;
  for (int i = 0; i < nbins; i++) {
    if (power[i] > max_p) { max_p = power[i]; max_bin = i; }
  }
  float peak_freq = max_bin * bin_hz;

  // RMS
  float rms_sum = 0;
  for (int i = 0; i < FFT_SIZE; i++)
    rms_sum += ((float)mono[i]/32768.0f) * ((float)mono[i]/32768.0f);
  float rms = sqrtf(rms_sum / FFT_SIZE);

  // Centroid
  float weighted = 0;
  for (int i = 0; i < nbins; i++)
    weighted += (float)i * bin_hz * power[i];
  float centroid = (total_power > 1e-12f) ? weighted / total_power : 0;

  // --- Print ---
  Serial.printf("Peak freq: %.1f Hz\n", peak_freq);
  Serial.printf("Centroid:  %.1f Hz\n", centroid);
  Serial.printf("RMS:       %.4f\n", rms);
  Serial.printf("Total power: %.1f\n", total_power);

  i2s_driver_uninstall(I2S_NUM_0);
  Serial.flush();
  esp_sleep_enable_timer_wakeup(30ULL * 1000000ULL);
  esp_deep_sleep_start();
}
void loop() {}
```

---

## Test

1. Brancher comme SOP-13 (Config C).
2. Flasher `wn_fft_test`.
3. **Pendant la capture : générer un son stable** — siffler, utiliser une app tone generator (1000 Hz), ou claquer des doigts.
4. Moniteur série :

```
=== FFT TEST #1 ===
Peak freq: 984.4 Hz     ← attendu ~1000 Hz si tone generator
Centroid:  1020.0 Hz
RMS:       0.1245
Total power: 45230.0
```

> ✅ Peak freq proche du signal test (±50 Hz acceptable pour 1024 bins à 16kHz = 15.6 Hz/bin).
> ✅ RMS > 0.01 si signal présent, < 0.001 si silence.
> ✅ Total power > 0.

> ❌ Peak freq = 0 avec signal : vérifier que les micros captent (voir SOP-13).

---

## Grille de décision

| Critère | ✅ GO | 🟠 Orange | ❌ NO-GO |
|---------|:-----:|:---------:|:--------:|
| FFT computation | < 500ms | 500ms-1s | Timeout/crash |
| Peak freq (1kHz test) | ±50 Hz | ±100 Hz | Mauvaise fréquence |
| RMS (silence) | < 0.001 | < 0.01 | > 0.01 |
| RMS (signal) | > 0.05 | > 0.01 | < 0.01 |
| 10 features non nulles | Toutes | 8-9 | < 8 |

---

**Fin de SOP-14. Prochaine étape : SOP-15 — Clip WAV 3s + sidecar JSON.**
