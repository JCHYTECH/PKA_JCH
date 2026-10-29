# ADR-016 — Firmware intégré P0 — Machine d'états complète

**Date :** 2026-06-30  
**Dernière mise à jour :** 2026-07-05 — Ajout du cycle AUDIO (timer-triggered) — Dobby 🦉  
**Statut :** accepté  
**Owner PKA :** [[Forge]]  
**Jalon :** M-02 — Prototype banc fonctionnel  

## Contexte

Les SOPs A→C (alive check, deep sleep, PPK2 mesure) et les firmware de test individuels (wn_blink, wn_cam_test, wn_edge_bench) ont validé les composants matériels individuellement. Cependant, **aucun firmware intégré P0 n'existe** : le cycle complet (veille → PIR wake → caméra → IA → stockage → LoRa → sleep) n'est pas implémenté.

Ce gap est identifié comme critique dans `Start.md` §9. La transition de "tests dans des Markdown" vers "firmware produit" nécessite :

1. Un repo Git dédié WildNexus
2. Un projet ESP-IDF structuré en modules
3. Une machine d'états centrale qui chaîne les SOPs

### Gap identifié le 2026-07-05

La machine d'états originale n'avait **aucun état pour la capture audio programmée** — pourtant requise par ADR-013 (micros stéréo SPH0645LM4H-B) et le scope lock P0 (capture audio locale courte). Sans cet état, les micros seraient physiquement présents mais muets. Le pipeline InsectNet et NEXUS_ACOUSTIC n'aurait aucune source de données.

**Correctif appliqué :** ajout d'un cycle parallèle timer-triggered pour la capture audio, coexistant avec le cycle PIR caméra. Les deux sources de réveil (PIR GPIO + timer) sont natives sur ESP32-S3.

## Décision proposée

### 1. Créer un repo Git WildNexus

```
wildnexus-firmware/
├── CMakeLists.txt
├── main/
│   ├── main.c                    # Entry point — machine d'états
│   ├── wn_state_machine.h         # États et transitions
│   ├── wn_config.h                # Configuration globale (pins, timing)
│   ├── modules/
│   │   ├── wn_camera.c/.h         # SOP-08 — OV5640 capture
│   │   ├── wn_power.c/.h          # SOP-03/10 — deep sleep, PPK2 mesures
│   │   ├── wn_storage.c/.h        # SOP-06 — microSD read/write
│   │   ├── wn_lora.c/.h           # SOP-07 — SX1262 TX/RX + ADR-014 codec
│   │   ├── wn_pir.c/.h            # SOP-09 — PIR EKMB wake source
│   │   ├── wn_ai.c/.h             # SOP-11 — Edge AI inference
│   │   ├── wn_audio.c/.h          # ADR-013 — I2S MEMS capture + FFT
│   │   └── wn_provisioning.c/.h   # SOP-12 — BTLE/Wi-Fi config
│   └── codecs/
│       ├── wn_payload_codec.c/.h  # ADR-014 — encode/decode 48-byte payload
│       ├── wn_metadata.c/.h        # Camtrap-DP metadata format (images)
│       └── wn_audio_metadata.c/.h  # ADR-017 — audio metadata + WAV header
├── components/
│   └── tflite-micro/              # TensorFlow Lite Micro (submodule)
├── test/
│   ├── test_payload_codec.c        # Unit tests ADR-014
│   ├── test_state_machine.c        # State transition tests
│   ├── test_mock_camera.c          # Camera mock for CI
│   └── test_audio_cycle.c          # Audio cycle mock for CI
├── boards/
│   └── esp32s3_devkit/             # Pin mappings per board
├── docs/
│   └── firmware_architecture.md
└── sdkconfig.defaults
```

### 2. Machine d'états P0 — double cycle

Le firmware gère **deux sources de réveil indépendantes** qui déclenchent deux cycles distincts :

- **Cycle CAMÉRA** — déclenché par PIR (mouvement)
- **Cycle AUDIO** — déclenché par timer (programmé)

Les deux cycles ne s'exécutent jamais simultanément : si un réveil PIR survient pendant un cycle audio, le cycle audio est interrompu et reprogrammé. Si un timer audio se déclenche pendant un cycle caméra, le cycle audio est différé à la fin du cycle caméra.

```
┌─────────────────────────────────────────────────────────────┐
│                  WILDNEXUS P0 STATE MACHINE                   │
│                  Dual-cycle : CAMÉRA + AUDIO                   │
└─────────────────────────────────────────────────────────────┘

  ┌──────────┐
  │  SLEEP   │ ← deep sleep
  └────┬─────┘    Sources de réveil :
       │          ├── PIR GPIO (ext0_wakeup)     → Cycle CAMÉRA
       │          ├── Timer FFT (15 min)          → Cycle AUDIO (FFT)
       │          └── Timer CLIP (60 min)         → Cycle AUDIO (CLIP)
       │
       ├──[PIR]──────────────────────────────────────────────┐
       │                                                    │
       │   ┌──────────┐     ┌──────────┐     ┌──────────┐    │
       │   │  WAKE    │ →   │ CAPTURE   │ →   │ AI_FILTER│    │
       │   └──────────┘     └──────────┘     └────┬─────┘    │
       │                                        │          │
       │               ┌────────────────────────┤          │
       │               │ non-animal → LOG_ONLY → SLEEP     │
       │               │ human → DISCARD → LOG_ONLY → SLEEP│
       │               └─ animal ──┐                        │
       │                            ▼                        │
       │                     ┌──────────┐     ┌──────────┐  │
       │                     │ STORE     │ →  │ TX_LORA   │ │
       │                     └──────────┘     └────┬─────┘  │
       │                                           │        │
       │                                           ▼        │
       │                                      ┌──────────┐  │
       │                                      │ SLEEP    │  │
       │                                      └──────────┘  │
       │                                                    │
       ├──[Timer FFT 15min]─────────────────────────────────┐
       │                                                    │
       │   ┌──────────────┐     ┌──────────────┐            │
       │   │ AUDIO_WAKE    │ →  │ AUDIO_FFT     │            │
       │   └──────────────┘     └──────┬───────┘            │
       │                               │                    │
       │                               ▼                    │
       │                        ┌──────────────┐            │
       │                        │ AUDIO_STORE   │ ← FFT     │
       │                        └──────┬───────┘   features │
       │                               │            sur SD  │
       │                               ▼                    │
       │                        ┌──────────────┐            │
       │                        │ TX_LORA       │ ← spectral│
       │                        └──────┬───────┘   payload  │
       │                               │            (ADR-014)│
       │                               ▼                    │
       │                        ┌──────────┐               │
       │                        │ SLEEP    │               │
       │                        └──────────┘               │
       │                                                    │
       ├──[Timer CLIP 60min]───────────────────────────────┐
       │                                                    │
       │   ┌──────────────┐     ┌──────────────┐            │
       │   │ AUDIO_WAKE    │ →  │ AUDIO_RECORD  │ ← 3s WAV  │
       │   └──────────────┘     └──────┬───────┘   stéréo    │
       │                               │            16kHz    │
       │                               ▼            16-bit   │
       │                        ┌──────────────┐            │
       │                        │ AUDIO_STORE   │ ← clip     │
       │                        └──────┬───────┘   WAV +     │
       │                               │            metadata │
       │                               │            JSON     │
       │                               ▼                    │
       │                        ┌──────────┐               │
       │                        │ SLEEP    │               │
       │                        └──────────┘               │
       │  (pas de TX LoRa pour les clips — trop gros,       │
       │   récupération Wi-Fi ou SD physique.               │
       │   Notification optionnelle : 1 paquet spectral     │
       │   avec flag bit4=audio_clip_ready)                  │
       └──────────────────────────────────────────────────────┘
```

### 3. Transitions et timers

#### Cycle CAMÉRA (PIR-triggered)

| Transition | Trigger | Timeout | Action en cas d'échec |
|------------|---------|---------|----------------------|
| SLEEP → WAKE | PIR GPIO (ext0_wakeup) | — | — |
| WAKE → CAPTURE | Boot complete | 2s | Si timeout → LOG_ERROR → SLEEP |
| CAPTURE → AI_FILTER | Image JPEG disponible | 5s | Si échec caméra → LOG_ERROR → SLEEP |
| AI_FILTER → STORE/LOG | Inférence complète | 2s | Si OOM/latence >2s → ADR-010 R4 trigger |
| AI_FILTER → LOG_ONLY | Score < 0.3 | — | Log minimal, pas de stockage |
| STORE → TX_LORA | Écriture SD OK | 3s | Si SD pleine → flag sd_full, skip TX |
| TX_LORA → SLEEP | TX complete ou timeout | 10s | Si pas d'ACK → retry queue (max 3) |
| TX_LORA → SLEEP | Duty cycle respecté | Toff = Tair×99 | Queue FIFO 16 événements max |

#### Cycle AUDIO FFT (timer 15 min)

| Transition | Trigger | Timeout | Action en cas d'échec |
|------------|---------|---------|----------------------|
| SLEEP → AUDIO_WAKE | Timer 15 min (timer_wakeup) | — | — |
| AUDIO_WAKE → AUDIO_FFT | I2S init + capture 250ms buffer | 1s | Si I2S fail → LOG_ERROR → SLEEP |
| AUDIO_FFT → AUDIO_STORE | FFT 1024 points calculée | 500ms | Si FFT fail → LOG_ERROR → SLEEP |
| AUDIO_STORE → TX_LORA | Features spectrales écrites SD | 1s | Si SD pleine → flag sd_full, skip TX |
| TX_LORA → SLEEP | Spectral payload TX (ADR-014 0x05) | 10s | Si duty cycle saturé → queue |
| TX_LORA → SLEEP | Duty cycle respecté | Toff = Tair×99 | — |

#### Cycle AUDIO CLIP (timer 60 min)

| Transition | Trigger | Timeout | Action en cas d'échec |
|------------|---------|---------|----------------------|
| SLEEP → AUDIO_WAKE | Timer 60 min (timer_wakeup) | — | — |
| AUDIO_WAKE → AUDIO_RECORD | I2S init + capture stéréo 3s | 4s | Si I2S fail → LOG_ERROR → SLEEP |
| AUDIO_RECORD → AUDIO_STORE | WAV encodé + metadata JSON | 2s | Si SD pleine → LOG_ERROR → SLEEP |
| AUDIO_STORE → SLEEP | Fichier WAV + sidecar JSON sur SD | — | Pas de TX LoRa (clip trop gros pour LoRa) |

#### Gestion des conflits

| Situation | Règle |
|-----------|-------|
| PIR pendant cycle AUDIO | Interrompt l'audio, reprogramme le timer audio au prochain sleep, exécute le cycle caméra |
| Timer audio pendant cycle CAMÉRA | Diffère l'audio à la fin du cycle caméra (flag `audio_pending`) |
| PIR + Timer audio simultanés | Priorité caméra (événement animal > capture programmée) |
| 2 timers audio simultanés (FFT + CLIP) | FFT en priorité (plus court, libère le timer plus vite) |

### 4. Configuration cible

```c
// wn_config.h — defaults

// === CYCLE CAMÉRA ===
#define WN_SLEEP_DURATION_SEC      900     // 15 min fallback timer (si pas de PIR)
#define WN_PIR_GPIO                4       // GPIO4 — PIR EKMB
#define WN_CAM_XCLK_GPIO           17
#define WN_CAM_SIOC_GPIO           21
#define WN_CAM_SIOD_GPIO           20

// === CYCLE AUDIO FFT (ADR-013) ===
#define WN_AUDIO_FFT_INTERVAL_SEC  900     // 15 min — features spectrales
#define WN_AUDIO_FFT_SAMPLES       4096     // 250ms @ 16kHz
#define WN_AUDIO_FFT_SIZE          1024     // FFT points
#define WN_AUDIO_FFT_FEATURES      10      // descripteurs spectraux

// === CYCLE AUDIO CLIP (ADR-013) ===
#define WN_AUDIO_CLIP_INTERVAL_SEC 3600     // 60 min — clip WAV stéréo
#define WN_AUDIO_CLIP_DURATION_SEC 3        // 3 secondes
#define WN_AUDIO_SAMPLE_RATE       16000    // 16 kHz
#define WN_AUDIO_BITS_PER_SAMPLE   16       // PCM 16-bit
#define WN_AUDIO_CHANNELS          2        // stéréo (ADR-013)

// === I2S PINS (SPH0645LM4H-B ×2) ===
#define WN_I2S_PORT                I2S_NUM_0
#define WN_I2S_BCLK_GPIO           41       // à confirmer sur PCB final
#define WN_I2S_WS_GPIO             42       // à confirmer sur PCB final
#define WN_I2S_DIN_GPIO            43       // micro L
#define WN_I2S_DIN2_GPIO           44       // micro R (ESP32-S3 dual I2S)

// === LORA ===
#define WN_LORA_SPI_HOST           SPI2_HOST
#define WN_LORA_NSS_GPIO           10
#define WN_LORA_RST_GPIO           11
#define WN_LORA_DIO1_GPIO          12

// === STORAGE ===
#define WN_SD_SPI_HOST             SPI3_HOST
#define WN_SD_CS_GPIO              13

// === AI ===
#define WN_AI_THRESHOLD_ANIMAL     0.7
#define WN_AI_THRESHOLD_HUMAN      0.5

// === LORA ===
#define WN_LORA_SF_DEFAULT         7
#define WN_LORA_FREQ               868100000  // EU868
#define WN_LORA_TX_POWER           17         // dBm
```

### 5. Budget énergétique audio

| Élément | Consommation | Fréquence | mAh/jour |
|---------|--------------|-----------|----------|
| FFT : I2S wake + capture 4096 samples | ~30 mA × 250ms | 96×/jour | ~0,2 mAh |
| FFT : calcul 1024 points | ~80 mA × 100ms | 96×/jour | ~0,2 mAh |
| Clip : I2S wake + capture 3s stéréo | ~30 mA × 3s | 24×/jour | ~0,6 mAh |
| Clip : WAV encode + SD write | ~50 mA × 500ms | 24×/jour | ~0,2 mAh |
| SPH0645 sleep entre cycles | 10 µA | continu | ~0,24 mAh |
| **Total audio** | | | **~1,4 mAh/jour** |

Comparaison : le cycle caméra (PIR + capture + IA + store + TX) est estimé à ~5-8 mAh/jour (24 événements). L'audio ajoute ~20% au budget quotidien — acceptable dans le budget 60 jours ADR-005.

## Alternatives considérées

| Option | Pour | Contre | Statut |
|--------|------|--------|--------|
| ESP-IDF project structuré (modulaire) | Maintenable, testable, production-ready | Plus lent à setup que Arduino | **Retenu** |
| Arduino IDE (sketch unique) | Rapide, simple | Non maintenable, pas de tests, pas de CI | Rejeté |
| PlatformIO | Abstraction multi-platform | Dépendance supplémentaire | P1 si besoin |
| Attendre la fin de toutes les SOPs | Tout testé individuellement | Le chaînage est le vrai risque — retarder ne le réduit pas | Rejeté |
| Audio en thread parallèle | Parallélisme apparent | ESP32-S3 freeRTOS en deep sleep = thread tué | Rejeté — incompatible deep sleep |
| Audio uniquement sur déclenchement PIR | Simplicité | Manque les chants programmés (ortho crépuscule, aube) — fenêtre acoustique perdue | Rejeté — InsectNet/NEXUS_ACOUSTIC |

## Conséquences

- [[Forge]] crée le repo `wildnexus-firmware/` (Git local ou GitHub privé)
- Chaque module `wn_*.c` encapsule une SOP et expose une API claire
- Le codec ADR-014 (`wn_payload_codec.c`) est le premier module testable unitairement (pas de hardware requis)
- Le module `wn_audio.c` gère : I2S init, capture buffer, FFT (esp_dsp), WAV encode, SD write
- Le module `wn_audio_metadata.c` gère : sidecar JSON par clip (ADR-017)
- Les tests unitaires (`test_payload_codec.c`, `test_state_machine.c`, `test_audio_cycle.c`) tournent en CI via Wokwi ou natif
- Le firmware de production sera le résultat de l'intégration des modules, pas un monolithe
- **L'ESP32-S3 doit activer `esp_sleep_enable_timer_wakeup` en plus de `esp_sleep_enable_ext0_wakeup`** — les deux sources coexistent

## Tests obligatoires avant acceptation

| Test | Critère minimal |
|---|---|
| Cycle caméra complet SLEEP→WAKE→CAPTURE→AI→STORE→TX→SLEEP | 100 cycles sans crash |
| Cycle audio FFT SLEEP→AUDIO_WAKE→AUDIO_FFT→AUDIO_STORE→TX→SLEEP | 50 cycles sans crash |
| Cycle audio CLIP SLEEP→AUDIO_WAKE→AUDIO_RECORD→AUDIO_STORE→SLEEP | 20 cycles sans crash |
| Conflit PIR pendant audio | Audio interrompu proprement, caméra exécutée, timer audio reprogrammé |
| Conflit timer audio pendant caméra | Audio différé après cycle caméra, pas de perte |
| Payload codec roundtrip (caméra + spectral) | Encode → decode → comparaison byte-à-byte pour 0x01 et 0x05 |
| Duty cycle LoRa (caméra + spectral combinés) | Respect EU868 1% sur 1h de simulation |
| Filtre humain | Aucune image humaine stockée en clair |
| Deep sleep courant | < 1 mA mesuré au PPK2 sur cycle complet (caméra + audio) |
| WAV clip valide | Fichier WAV lisible par ffmpeg/audacity, 16kHz, 16-bit, stéréo, 3s |
| FFT features | 10 descripteurs spectraux non nuls sur signal test (1kHz sine) |

## Critère de révision

Réviser cette ADR si :
- L'architecture modulaire s'avère trop lourde pour les contraintes RAM ESP32-S3
- Un MCU de fallback (STM32U5) nécessite une structure différente
- Le Edge AI nécessite un coprocesseur externe qui change l'architecture
- Le budget énergétique audio dépasse 3 mAh/jour mesuré (vs ~1,4 estimé)
- La coexistence des deux timers (FFT 15min + CLIP 60min) génère des race conditions non résolvables
- Les pins I2S entrent en conflit avec la caméra DVP sur le PCB final

---

*Mis à jour le 2026-07-05 par Dobby 🦉 — ajout du cycle AUDIO suite à l'audit de cohérence WildNexus ↔ InsectNet/NEXUS_ACOUSTIC. — Forge : intégration technique.*
