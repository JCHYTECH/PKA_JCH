# SOP-11 — Phase K : Benchmark Edge AI

**SOP :** SOP-11  
**Projet :** WildNexus P0 — M-02 Prototype banc fonctionnel  
**Phase :** K — Benchmark inférence Edge AI (MobileNet-SSD sur ESP32-S3)  
**Durée :** ~45 minutes (nécessite préparation du modèle)  
**Prérequis :** SOP-05 réussi, modèle MobileNet-SSD quantifié INT8 disponible  
**Auteur :** [[Dobby]]  
**Date :** 2026-06-12  
**Version :** 1.0  

---

## Objectif

Mesurer la latence d'inférence et la consommation énergétique d'un modèle de détection binaire (animal / non-animal) sur ESP32-S3. Cette mesure est **bloquante pour ADR-010 R4** : si la latence dépasse 2s ou si la consommation est excessive, une migration MCU (STM32U5) doit être envisagée.

---

## ⚠️ Prérequis bloquants

Avant de commencer cette SOP, vérifier :

- [ ] **Modèle TensorFlow Lite quantifié INT8** disponible (`.tflite` ou `.h`)
- [ ] **ESP-IDF** installé (TensorFlow Lite Micro nécessite ESP-IDF, pas Arduino IDE)
- [ ] **Caméra OV5640** validée (SOP-08) pour la capture d'image réelle

> Si le modèle n'est pas encore entraîné ou quantifié, cette phase ne peut pas être exécutée. Passer directement à SOP-12.

---

## Architecture du test

```
Image (OV5640 ou fichier test) → Preprocessing → MobileNet-SSD → Classification
                                                                    │
                                                    ┌───────────────┴──────────────┐
                                                    │ animal (> 0.7)               │ non-animal (< 0.3)
                                                    │ → "trigger capture"          │ → "discard"
                                                    └──────────────────────────────┘
```

---

## Étape 1 — Préparer l'environnement (15 minutes, une seule fois)

### 1.1 Installer ESP-IDF

```bash
# Sur Mac
brew install esp-idf
# ou
git clone --recursive https://github.com/espressif/esp-idf.git ~/esp-idf
cd ~/esp-idf && ./install.sh esp32s3
```

### 1.2 Installer TensorFlow Lite Micro

```bash
git clone https://github.com/espressif/tflite-micro-esp-examples.git
```

### 1.3 Convertir le modèle en tableau C

Si le modèle est au format `.tflite` :

```bash
# Linux/macOS
xxd -i model.tflite > model_data.h
```

Le fichier `.h` contient le modèle sous forme de tableau d'octets, directement compilable.

---

## Étape 2 — Firmware `wn_edge_bench` (5 minutes)

Ce firmware est un **template**. Les chemins et includes exacts dépendent de l'installation ESP-IDF.

```cpp
// SOP-11 — wn_edge_bench
// WildNexus P0 — Phase K — Benchmark inférence Edge AI
// Mesure la latence d'inférence MobileNet-SSD sur ESP32-S3.
// À compiler avec ESP-IDF (pas Arduino IDE).

#include <stdio.h>
#include "esp_sleep.h"
#include "esp_timer.h"
#include "esp_log.h"
#include "model_data.h"         // Modèle TFLite converti en .h
#include "tensorflow/lite/micro/all_ops_resolver.h"
#include "tensorflow/lite/micro/micro_interpreter.h"

static const char *TAG = "WN_BENCH";

// Buffer pour le modèle
static tflite::MicroInterpreter *interpreter = nullptr;
static TfLiteTensor *input = nullptr;
static TfLiteTensor *output = nullptr;

// Zone mémoire pour l'interpréteur
constexpr int kTensorArenaSize = 512 * 1024;  // 512 KB
static uint8_t tensor_arena[kTensorArenaSize];

RTC_DATA_ATTR int bench_count = 0;

extern "C" void app_main() {
  bench_count++;
  ESP_LOGI(TAG, "=== EDGE AI BENCH #%d ===", bench_count);

  // 1. Charger le modèle
  const tflite::Model *model = tflite::GetModel(model_data);
  if (model->version() != TFLITE_SCHEMA_VERSION) {
    ESP_LOGE(TAG, "Model schema version mismatch");
    esp_deep_sleep(60ULL * 1000000ULL);
    return;
  }

  // 2. Setup l'interpréteur
  static tflite::AllOpsResolver resolver;
  static tflite::MicroInterpreter static_interpreter(
    model, resolver, tensor_arena, kTensorArenaSize
  );
  interpreter = &static_interpreter;

  if (interpreter->AllocateTensors() != kTfLiteOk) {
    ESP_LOGE(TAG, "AllocateTensors failed");
    esp_deep_sleep(60ULL * 1000000ULL);
    return;
  }

  input = interpreter->input(0);
  output = interpreter->output(0);

  // 3. Remplir l'input avec des données de test (image VGA 640×480×3)
  //    En conditions réelles : copier le framebuffer OV5640 ici
  for (int i = 0; i < input->bytes; i++) {
    input->data.uint8[i] = (uint8_t)(i % 255);  // Données factices
  }

  // 4. Inférence — MESURE
  int64_t start = esp_timer_get_time();
  if (interpreter->Invoke() != kTfLiteOk) {
    ESP_LOGE(TAG, "Invoke failed");
  }
  int64_t end = esp_timer_get_time();

  int64_t latency_us = end - start;
  float latency_ms = latency_us / 1000.0f;

  // 5. Lire le résultat
  float score_animal = output->data.f[1];    // Classe 1 = animal (à adapter)
  float score_bg     = output->data.f[0];    // Classe 0 = background

  ESP_LOGI(TAG, "Latency: %.1f ms | animal: %.2f | bg: %.2f",
           latency_ms, score_animal, score_bg);

  // 6. Décision
  if (score_animal > 0.7f) {
    ESP_LOGI(TAG, "→ TRIGGER: animal detected");
  } else {
    ESP_LOGI(TAG, "→ DISCARD: no animal");
  }

  ESP_LOGI(TAG, "Bench done → sleep");
  esp_sleep_enable_timer_wakeup(60ULL * 1000000ULL);
  esp_deep_sleep_start();
}
```

---

## Étape 3 — Compiler et flasher (10 minutes)

```bash
cd ~/wildnexus-firmware/edge_bench
idf.py set-target esp32s3
idf.py build
idf.py -p /dev/cu.usbmodemXXXX flash monitor
```

Sortie attendue :

```
=== EDGE AI BENCH #1 ===
Latency: 847.3 ms | animal: 0.12 | bg: 0.88
→ DISCARD: no animal
Bench done → sleep
```

---

## Étape 4 — Mesure PPK2 (10 minutes)

1. Débrancher USB.
2. PPK2 OFF → VOUT→5V, GND→GND.
3. Source Meter 5.0V, acquisition, sortie ON.

```
Courant
  │
  │  ┌────────────────────────────┐
  │  │  chargement modèle + inférence │
  │  │  ~80-150 mA                    │
  │  │  pendant ~800-2000 ms          │
  │──┘                                └──────────────────────┐
  │                                                          │
  │  ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔  ← sleep           │
  └──────────────────────────────────────────────────────────────→
```

| Mesure | Valeur |
|--------|--------|
| Latence inférence (ms) | _____ ms |
| Courant pic inférence (mA) | _____ mA |
| Charge inférence (mAh) | _____ mAh |
| RAM utilisée (tensor_arena) | _____ KB |

---

## Grille de décision (ADR-010 R4)

| Critère | ✅ GO | 🟠 Orange | ❌ NO-GO → STM32U5 |
|---------|:-----:|:---------:|:------------------:|
| Latence inférence | < 1000 ms | 1000-2000 ms | **> 2000 ms** |
| RAM disponible après modèle | > 100 KB | 50-100 KB | < 50 KB |
| Charge inférence | < 0.3 mAh | 0.3-0.5 mAh | > 0.5 mAh |
| ESP32-S3 stable 20 inférences | 20/20 | 1-2 erreurs | Crash ou OOM |

> ⚠️ **DÉCISION CRITIQUE :** si la latence > 2000 ms (NO-GO), convoquer [[Castor]] + [[Forge]] pour arbitrage migration MCU. L'ESP32-S3 resterait le MCU principal mais l'inférence serait déportée ou le modèle simplifié.

---

## Clôture

- [ ] ESP-IDF et TFLite Micro installés
- [ ] Modèle TFLite quantifié INT8 converti en `.h`
- [ ] `wn_edge_bench` compilé sans erreur
- [ ] Latence inférence mesurée
- [ ] Mesure PPK2 effectuée
- [ ] Résultat comparé à la grille GO/NO-GO
- [ ] Si NO-GO → escalade [[Castor]] + [[Forge]]

---

**Fin de SOP-11. Prochaine étape : SOP-12 Phase L — Micro + Provisioning.**
