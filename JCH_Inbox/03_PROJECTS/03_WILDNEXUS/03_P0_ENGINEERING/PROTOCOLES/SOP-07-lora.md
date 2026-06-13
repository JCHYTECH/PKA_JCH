# SOP-07 — Phase G : Test LoRa SX1262 / RAK3172

**SOP :** SOP-07  
**Projet :** WildNexus P0 — M-02 Prototype banc fonctionnel  
**Phase :** G — Test module LoRa SX1262 ou RAK3172  
**Durée :** ~30 minutes  
**Prérequis :** SOP-05 réussi, module LoRa disponible  
**Auteur :** [[Dobby]]  
**Date :** 2026-06-12  
**Version :** 1.0  

---

## Objectif

Vérifier que le module LoRa s'initialise, envoie un paquet TX, puis retourne en veille sans courant de fuite. Mesurer le pic de consommation lors de la transmission.

---

## Matériel spécifique

| # | Élément |
|---|---------|
| 1 | Module LoRa SX1262 ou RAK3172-T EU868 |
| 2 | Antenne LoRa 868 MHz (SMA ou uFL selon module) |
| 3 | 6-8 câbles Dupont femelle-femelle |

---

## Étape 1 — Pinout du module LoRa

### ⚠️ Avant de brancher, identifier le module exact.

| Signal | ESP32-S3 GPIO | Note |
|--------|:------------:|------|
| VCC | 3V3 | **Jamais 5V** — module 3.3V natif |
| GND | GND | |
| SCK | 12 | Bus SPI partagé avec SD |
| MISO | 13 | Bus SPI partagé avec SD |
| MOSI | 11 | Bus SPI partagé avec SD |
| NSS / CS | **9** | Chip Select LoRa (différent du CS SD = 10) |
| DIO1 | 14 | Interruption |
| BUSY | 15 | État occupé |
| RESET | 16 | Reset module |

> 💡 **Bus SPI partagé :** SCK, MISO, MOSI sont communs à la SD et au LoRa. Seuls les CS sont différents (SD=10, LoRa=9). C'est une configuration standard.

---

## Étape 2 — Firmware `wn_lora_tx` (3 minutes)

Ce firmware utilise la bibliothèque **RadioLib** (installable via Arduino Library Manager).

```cpp
// SOP-07 — wn_lora_tx
// WildNexus P0 — Phase G — Test TX LoRa
// Envoie un paquet LoRa toutes les 60 secondes.

#include "esp_sleep.h"
#include <RadioLib.h>

// Pinout LoRa → ESP32-S3
#define LORA_CS    9
#define LORA_DIO1 14
#define LORA_BUSY 15
#define LORA_RST  16

// Fréquence LoRa EU868
#define FREQ 868.0
#define BW   125.0
#define SF   9

SX1262 radio = new Module(LORA_CS, LORA_DIO1, LORA_RST, LORA_BUSY);

RTC_DATA_ATTR int tx_count = 0;

void setup() {
  Serial.begin(115200);
  delay(500);
  tx_count++;

  Serial.printf("=== LORA TX #%d ===\n", tx_count);

  int state = radio.begin(FREQ, BW, SF);
  if (state == RADIOLIB_ERR_NONE) {
    Serial.println("✅ LoRa init OK");

    // Envoyer un paquet test
    char payload[48];
    snprintf(payload, sizeof(payload), "WN:%d:TEST", tx_count);
    state = radio.transmit(payload);
    if (state == RADIOLIB_ERR_NONE) {
      Serial.printf("✅ TX OK: '%s'\n", payload);
    } else {
      Serial.printf("❌ TX FAILED: code %d\n", state);
    }

    radio.sleep();
    Serial.println("LoRa → sleep");
  } else {
    Serial.printf("❌ LoRa init FAILED: code %d\n", state);
  }

  Serial.flush();
  esp_sleep_enable_timer_wakeup(60ULL * 1000000ULL);
  esp_deep_sleep_start();
}

void loop() {}
```

### 2.1 Installer RadioLib

1. Arduino IDE → **Tools → Manage Libraries**.
2. Rechercher `RadioLib`.
3. Installer **RadioLib by Jan Gromeš**.

---

## Étape 3 — Branchement (5 minutes)

```
        ESP32-S3 DevKit              Module LoRa
        ┌──────────────┐             ┌──────────┐
        │  3V3 ────────┼──[rouge]────┼── VCC    │
        │  GND ────────┼──[noir]─────┼── GND    │
        │  IO12 ───────┼──[jaune]────┼── SCK    │
        │  IO13 ───────┼──[bleu]─────┼── MISO   │
        │  IO11 ───────┼──[vert]─────┼── MOSI   │
        │  IO9  ───────┼──[orange]───┼── NSS/CS │
        │  IO14 ───────┼──[violet]───┼── DIO1   │
        │  IO15 ───────┼──[gris]─────┼── BUSY   │
        │  IO16 ───────┼──[blanc]────┼── RESET  │
        └──────────────┘             └──────────┘
```

**Ordre :** GND → VCC → signaux. **Vérifier deux fois 3V3, pas 5V.**

---

## Étape 4 — Test sans PPK2 (5 minutes)

1. ESP32 USB branché + module LoRa câblé.
2. **Visser l'antenne** sur le connecteur SMA/uFL du module.  
   ⚠️ **Ne jamais alimenter un module LoRa sans antenne.** La puissance RF réfléchie peut détruire l'amplificateur.
3. Flasher `wn_lora_tx`.
4. Moniteur série 115200 baud.

```
=== LORA TX #1 ===
✅ LoRa init OK
✅ TX OK: 'WN:1:TEST'
LoRa → sleep

--- 60 secondes ---

=== LORA TX #2 ===
...
```

> ✅ Messages « init OK » et « TX OK » → LoRa fonctionne.

> ❌ `LoRa init FAILED` :
> - Vérifier le câblage (CS=9, DIO1=14, BUSY=15, RST=16)
> - Vérifier 3V3, pas 5V
> - Le module RAK3172 nécessite parfois une commande AT ; ici on le pilote directement via SX1262

---

## Étape 5 — Mesure PPK2 (10 minutes)

1. Débrancher USB ESP32.
2. PPK2 OFF → VOUT→5V, GND→GND.
3. Source Meter 5.0V, acquisition, sortie ON.
4. Observer la courbe :

```
Courant
  │
  │                ┌──────┐
  │                │TX LoRa│ ← pic ~80-120 mA pendant 1-3 secondes
  │  ┌────┐        │      │
  │  │init│        │      │
  │──┘    └────────┘      └──────────────────────────┐
  │                                                  │
  │  ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔  ← sleep      │
  └──────────────────────────────────────────────────────→
```

### Mesures

| Mesure | Valeur |
|--------|--------|
| Courant init LoRa (mA) | _____ mA |
| Courant pic TX (mA) | _____ mA |
| Durée TX (s) | _____ s |
| Charge cycle TX (mAh) | _____ mAh |
| Deep sleep avec LoRa branché (µA) | _____ µA |
| ⚠️ Module LoRa fuit-il en veille ? | Oui / Non |

> ⚠️ Le module LoRa doit entrer en veille après TX. Si le deep sleep est > 200 µA avec le module branché, le `radio.sleep()` n'a pas fonctionné → documenter. Un MOSFET de power gating sera nécessaire.

---

## Grille de décision

| Critère | ✅ GO | 🟠 Orange | ❌ NO-GO |
|---------|:-----:|:---------:|:--------:|
| Init LoRa | OK | 1 retry | Échec |
| TX paquet | OK | Timeout occasionnel | Pas de TX |
| Deep sleep avec LoRa | < 150 µA | 150-300 µA | > 300 µA |
| Antenne vissée | Oui | — | Non (RISQUE) |

---

## Clôture

- [ ] Module LoRa identifié (SX1262 ou RAK3172)
- [ ] Antenne vissée avant mise sous tension
- [ ] Firmware compile et flashe
- [ ] TX paquet OK (moniteur série)
- [ ] Mesure PPK2 : pic TX + deep sleep
- [ ] Conso veille module LoRa documentée

---

**Fin de SOP-07. Prochaine étape : SOP-08 Phase H — Test caméra OV5640.**
