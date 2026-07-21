# SOP-07 — Phase G : Test LoRa SX1262 / RAK3172

**SOP :** SOP-07  
**Projet :** WildNexus P0 — M-02 Prototype banc fonctionnel  
**Phase :** G — Test module LoRa SX1262 ou RAK3172  
**Durée :** ~30 minutes  
**Prérequis :** SOP-05 réussi, module LoRa disponible  
**Auteur :** [[Dobby]]  
**Date :** 2026-06-12  
**Version :** 2.0 — 2026-07-05 : pinout corrigé (SPI2), test payload spectral 0x05 (ADR-014 v2)  

---

## Objectif

Vérifier que le module LoRa s'initialise, envoie un paquet TX (caméra + spectral), puis retourne en veille sans courant de fuite. Mesurer le pic de consommation lors de la transmission.

> ⚠️ **Config de test :** Config B (Radio). **Caméra DÉCONNECTÉE** — les GPIO 8-11 sont libérés pour LoRa.

---

## Matériel spécifique

| # | Élément |
|---|---------|
| 1 | Module LoRa SX1262 ou RAK3172-T EU868 |
| 2 | Antenne LoRa 868 MHz (SMA ou uFL) |
| 3 | 6-8 câbles Dupont femelle-femelle |

---

## Pinout (wn_config.h — SPI2_HOST)

| Signal | ESP32-S3 GPIO | Note |
|--------|:------------:|------|
| VCC | 3V3 | **Jamais 5V** |
| GND | GND | |
| SCK | **12** | SPI2 — indépendant de SPI3 (SD) |
| MISO | **13** | SPI2 |
| MOSI | **14** | SPI2 |
| NSS / CS | **10** | ⚠️ partagé avec Camera D6 (caméra déconnectée en Config B) |
| DIO1 | **9** | ⚠️ partagé avec Camera D5 |
| BUSY | **8** | ⚠️ partagé avec Camera D4 |
| RESET | **11** | ⚠️ partagé avec Camera D7 |

> ⚠️ **Ancien pinout (v1.0) :** NSS=9, DIO1=14, BUSY=15, RST=16, MOSI=11. **Obsolète.** Ces pins sont maintenant utilisés différemment. Voir `wn_config.h`.

> 💡 **SPI2 ≠ SPI3 :** LoRa utilise SPI2 (GPIO 12,13,14), SD utilise SPI3 (GPIO 39,40,41,42). Les deux bus sont indépendants. LoRa et SD peuvent coexister (Config B/D).

```
        ESP32-S3 DevKit              Module LoRa
        ┌──────────────┐             ┌──────────┐
        │  3V3 ────────┼──[rouge]────┼── VCC    │
        │  GND ────────┼──[noir]─────┼── GND    │
        │  IO12 ───────┼──[jaune]────┼── SCK    │
        │  IO13 ───────┼──[bleu]─────┼── MISO   │
        │  IO14 ───────┼──[vert]─────┼── MOSI   │
        │  IO10 ───────┼──[orange]───┼── NSS/CS │
        │  IO9  ───────┼──[violet]───┼── DIO1   │
        │  IO8  ───────┼──[gris]─────┼── BUSY   │
        │  IO11 ───────┼──[blanc]────┼── RESET  │
        └──────────────┘             └──────────┘
```

---

## Étape 1 — Firmware `wn_lora_tx` (5 minutes)

Ce firmware teste **deux types de payload** (ADR-014 v2) :
1. **Payload caméra** (0x01=motion) — 48 bytes
2. **Payload spectral** (0x05=spectral) — 48 bytes avec 10 features

```cpp
// SOP-07 — wn_lora_tx v2
// WildNexus P0 — Phase G — Test TX LoRa (ADR-014 v2)
// Envoie alternativement un payload caméra et un payload spectral.

#include "esp_sleep.h"
#include <RadioLib.h>

// Pinout LoRa SPI2 (wn_config.h)
#define LORA_CS    10
#define LORA_DIO1   9
#define LORA_BUSY   8
#define LORA_RST   11
#define LORA_SCK   12
#define LORA_MISO  13
#define LORA_MOSI  14

#define FREQ 868.1
#define BW   125.0
#define SF   7

SX1262 radio = new Module(LORA_CS, LORA_DIO1, LORA_RST, LORA_BUSY);

RTC_DATA_ATTR int tx_count = 0;

void setup() {
  Serial.begin(115200);
  delay(500);
  tx_count++;
  Serial.printf("=== LORA TX #%d ===\n", tx_count);

  SPI.begin(LORA_SCK, LORA_MISO, LORA_MOSI, LORA_CS);
  int state = radio.begin(FREQ, BW, SF);
  if (state != RADIOLIB_ERR_NONE) {
    Serial.printf("❌ LoRa init FAILED: %d\n", state);
    goto sleep;
  }
  Serial.println("✅ LoRa init OK (SF7, 868.1 MHz)");

  if (tx_count % 2 == 1) {
    // === Payload caméra (0x01=motion) ===
    uint8_t payload[48] = {0};
    payload[0] = 0x01;       // version
    payload[1] = 0x01;       // flags: ack_request
    payload[2] = 0xEF; payload[3] = 0xBE; payload[4] = 0xAD; payload[5] = 0xDE; // node_id
    payload[6] = 0x00; payload[7] = 0x00; payload[8] = 0x02; payload[9] = 0x00; // timestamp
    payload[10] = 0x01;      // event_type = motion
    payload[11] = 87;        // ia_score
    payload[12] = 1;         // ia_class = mammal
    payload[13] = 0xD8; payload[14] = 0x16; // battery = 5848 mV
    // CRC sera ignoré pour ce test
    state = radio.transmit(payload, 48);
    Serial.printf("📸 Camera payload TX: %s\n", state == RADIOLIB_ERR_NONE ? "✅" : "❌");
  } else {
    // === Payload spectral (0x05) ===
    uint8_t payload[48] = {0};
    payload[0] = 0x01;       // version
    payload[1] = 0x10;       // flags: audio_clip_ready
    payload[2] = 0xEF; payload[3] = 0xBE; payload[4] = 0xAD; payload[5] = 0xDE;
    payload[6] = 0x00; payload[7] = 0x00; payload[8] = 0x02; payload[9] = 0x00;
    payload[10] = 0x05;      // event_type = spectral (ADR-014 v2)
    payload[11] = 2;         // audio_channels = stereo
    // features[0..9] = 20 bytes (offset 12-31) — laisser à 0 pour test
    payload[12] = 0xAA; payload[13] = 0xBB; // centroid placeholder
    // CRC ignoré pour ce test
    state = radio.transmit(payload, 48);
    Serial.printf("🎵 Spectral payload TX: %s\n", state == RADIOLIB_ERR_NONE ? "✅" : "❌");
  }

  radio.sleep();
  Serial.println("LoRa → sleep");

sleep:
  Serial.flush();
  esp_sleep_enable_timer_wakeup(60ULL * 1000000ULL);
  esp_deep_sleep_start();
}
void loop() {}
```

---

## Étape 2 — Installer RadioLib

1. Arduino IDE → **Tools → Manage Libraries**.
2. Rechercher `RadioLib`.
3. Installer **RadioLib by Jan Gromeš**.

---

## Étape 3 — Branchement

1. **Visser l'antenne** sur le connecteur SMA/uFL.  
   ⚠️ **Ne jamais alimenter un module LoRa sans antenne.** Risque de destruction de l'amplificateur RF.
2. GND → VCC → signaux. Vérifier **3V3, pas 5V**.

---

## Étape 4 — Test sans PPK2

1. ESP32 USB + module LoRa câblé + antenne vissée.
2. Flasher `wn_lora_tx`.
3. Moniteur série 115200 baud.

```
=== LORA TX #1 ===
✅ LoRa init OK (SF7, 868.1 MHz)
📸 Camera payload TX: ✅
LoRa → sleep

--- 60 secondes ---

=== LORA TX #2 ===
✅ LoRa init OK (SF7, 868.1 MHz)
🎵 Spectral payload TX: ✅
LoRa → sleep
```

> ❌ `LoRa init FAILED` : vérifier câblage (CS=10, DIO1=9, BUSY=8, RST=11, SCK=12, MISO=13, MOSI=14).

---

## Étape 5 — Mesure PPK2

| Mesure | Valeur attendue |
|--------|-----------------|
| Courant init LoRa | 5-10 mA |
| Courant pic TX SF7 | 80-120 mA |
| Durée TX SF7 (48 bytes) | ~0.1-0.3 s |
| Deep sleep avec LoRa | < 150 µA |

> ⚠️ Si deep sleep > 300 µA → `radio.sleep()` n'a pas fonctionné. Power gating MOSFET nécessaire sur PCB.

---

## Grille de décision

| Critère | ✅ GO | 🟠 Orange | ❌ NO-GO |
|---------|:-----:|:---------:|:--------:|
| Init LoRa | OK | 1 retry | Échec |
| TX payload caméra (0x01) | OK | Timeout | Pas de TX |
| TX payload spectral (0x05) | OK | Timeout | Pas de TX |
| Deep sleep avec LoRa | < 150 µA | 150-300 µA | > 300 µA |
| Antenne vissée | Oui | — | Non (RISQUE) |

---

## Clôture

- [ ] Module LoRa identifié (SX1262 ou RAK3172)
- [ ] Antenne vissée avant mise sous tension
- [ ] Pinout SPI2 vérifié (CS=10, DIO1=9, BUSY=8, RST=11)
- [ ] TX payload caméra 0x01 OK
- [ ] TX payload spectral 0x05 OK
- [ ] Mesure PPK2 : pic TX + deep sleep
- [ ] Conso veille module LoRa documentée

---

**Fin de SOP-07 v2.0. Prochaine étape : SOP-08 Phase H — Test caméra OV5640.**
