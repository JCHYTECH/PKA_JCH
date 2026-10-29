# SOP-09 — Phase I : Test PIR EKMB

**SOP :** SOP-09  
**Projet :** WildNexus P0 — M-02 Prototype banc fonctionnel  
**Phase :** I — Test capteur PIR Panasonic EKMB1303111K  
**Durée :** ~20 minutes  
**Prérequis :** SOP-05 réussi, PIR EKMB disponible  
**Auteur :** [[Dobby]]  
**Date :** 2026-06-12  
**Version :** 2.0 — 2026-07-05 : pin corrigé GPIO 4 (wn_config.h), conflit PIR/D0 documenté  

---

## Objectif

Vérifier que le PIR EKMB déclenche correctement le réveil de l'ESP32-S3 depuis le deep sleep, et mesurer sa consommation propre.

> ⚠️ **Config de test :** Config A (Caméra) ou B (Radio) ou C (Audio). Le PIR est sur GPIO 4 qui est **partagé avec Camera D0**.
>
> **Conflit PIR / Camera D0 :**
> - En Config A (caméra), le PIR déclenche le réveil puis la caméra prend le contrôle de GPIO 4 (D0). C'est acceptable : le PIR passe à LOW après le trigger.
> - En Config B/C (pas de caméra), GPIO 4 est libre pour le PIR seul.
> - **Ne pas connecter le PIR ET la caméra D0 simultanément sans comprendre ce conflit.**

---

## Matériel spécifique

| # | Élément |
|---|---------|
| 1 | PIR Panasonic EKMB1303111K |
| 2 | 3 câbles Dupont femelle-femelle |

---

## À propos du PIR EKMB

- **Tension :** 2.3 - 4.0 V (alimenté en 3.3 V)
- **Consommation :** ~1-6 µA (extrêmement basse)
- **Sortie :** digitale, passe à HIGH lors d'une détection
- **Lentille :** intégrée, angle ~90°
- **Stabilisation :** 10-30 secondes après mise sous tension

---

## Pinout (wn_config.h)

| Signal | ESP32-S3 GPIO | Note |
|--------|:------------:|------|
| VCC | 3V3 | **Jamais 5V** — PIR 2.3-4.0V |
| GND | GND | |
| OUT | **GPIO 4** | ⚠️ partagé avec Camera D0. ext0_wakeup (front montant) |

> ⚠️ **Ancien pinout (v1.0) :** `PIR_PIN 3`. **Obsolète.** `wn_config.h` définit `WN_PIR_GPIO 4`. GPIO 3 est utilisé par `WN_BATTERY_ADC_GPIO` (diviseur de tension batterie).

```
        ESP32-S3 DevKit              PIR EKMB
        ┌──────────────┐             ┌──────────┐
        │  3V3 ────────┼──[rouge]────┼── VCC    │
        │  GND ────────┼──[noir]─────┼── GND    │
        │  IO4  ───────┼──[jaune]────┼── OUT    │
        └──────────────┘             └──────────┘
```

---

## Étape 1 — Firmware `wn_pir_wake` (3 minutes)

```cpp
// SOP-09 — wn_pir_wake v2
// WildNexus P0 — Phase I — Test PIR EKMB wake-up
// L'ESP32 dort. Le PIR le réveille sur GPIO 4 (ext0, front montant).

#include "esp_sleep.h"

#define PIR_PIN 4  // wn_config.h: WN_PIR_GPIO = 4

RTC_DATA_ATTR int wake_count = 0;

void setup() {
  Serial.begin(115200);
  delay(500);
  wake_count++;
  Serial.printf("=== PIR WAKE #%d ===\n", wake_count);

  pinMode(PIR_PIN, INPUT);
  int pir_state = digitalRead(PIR_PIN);
  Serial.printf("PIR pin state: %s\n", pir_state ? "HIGH (mouvement)" : "LOW (calme)");

  Serial.flush();

  // Réveil par PIR (front montant sur GPIO 4)
  esp_sleep_enable_ext0_wakeup((gpio_num_t)PIR_PIN, 1);  // 1 = HIGH

  // Timer de sécurité : si pas de PIR pendant 120s, réveil auto
  esp_sleep_enable_timer_wakeup(120ULL * 1000000ULL);

  Serial.println("Going to sleep — agitez la main devant le PIR");
  Serial.flush();
  delay(100);
  esp_deep_sleep_start();
}
void loop() {}
```

---

## Étape 2 — Branchement (3 minutes)

1. Attendre que le PIR soit stable (10-30s après mise sous tension).
2. GND → VCC → OUT sur GPIO 4.
3. Vérifier **3V3, pas 5V**.

---

## Étape 3 — Test fonctionnel (5 minutes)

1. ESP32 USB branché, PIR câblé sur GPIO 4.
2. Flasher `wn_pir_wake`.
3. Moniteur série 115200 baud.

```
=== PIR WAKE #1 ===
PIR pin state: LOW (calme)
Going to sleep — agitez la main devant le PIR

--- PIR détecte un mouvement ---

=== PIR WAKE #2 ===
PIR pin state: HIGH (mouvement)
Going to sleep — agitez la main devant le PIR
```

5. **Agiter la main à ~1-2 mètres** du PIR.

> ❌ Pas de réveil :
> - Vérifier câblage (3V3, GND, OUT→**GPIO 4**)
> - Attendre stabilisation 30s
> - Certains EKMB ont sortie à collecteur ouvert → pull-up 10kΩ sur OUT

---

## Étape 4 — Mesure PPK2 (5 minutes)

| Mesure | Valeur attendue |
|--------|-----------------|
| Deep sleep ESP32 + PIR | < 150 µA (PIR = ~1-6 µA) |
| Pic réveil sur mouvement | 40-80 mA (ESP32 boot) |
| Faux réveils (10 min) | 0 |

> 💡 Le PIR EKMB consomme ~1-6 µA. Si total > 200 µA → le DevKit fuit, pas le PIR.

---

## Grille de décision

| Critère | ✅ GO | 🟠 Orange | ❌ NO-GO |
|---------|:-----:|:---------:|:--------:|
| Wake-up PIR (GPIO 4) | < 2s | 2-5s | Pas de réveil |
| Faux réveils (10 min) | 0 | 1-2 | > 2 |
| Deep sleep + PIR | < 150 µA | 150-200 µA | > 200 µA |

---

## Clôture

- [ ] PIR branché (3V3, GND, OUT→**GPIO 4**)
- [ ] Réveil ESP32 confirmé sur mouvement
- [ ] Pas de faux réveil en 10 minutes
- [ ] Mesure PPK2 : deep sleep + PIR
- [ ] Conflit PIR/D0 camera documenté

---

**Fin de SOP-09 v2.0. Prochaine étape : SOP-10 Phase J — Alimentation AA + buck.**
