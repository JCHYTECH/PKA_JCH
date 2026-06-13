# SOP-09 — Phase I : Test PIR EKMB

**SOP :** SOP-09  
**Projet :** WildNexus P0 — M-02 Prototype banc fonctionnel  
**Phase :** I — Test capteur PIR Panasonic EKMB1303111K  
**Durée :** ~20 minutes  
**Prérequis :** SOP-05 réussi, PIR EKMB disponible  
**Auteur :** [[Dobby]]  
**Date :** 2026-06-12  
**Version :** 1.0  

---

## Objectif

Vérifier que le PIR EKMB déclenche correctement le réveil de l'ESP32-S3 depuis le deep sleep, et mesurer sa consommation propre.

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

Le PIR EKMB est idéal pour le deep sleep : il consomme quasi rien et peut réveiller l'ESP32 via une GPIO configurée en wake-up.

---

## Étape 1 — Firmware `wn_pir_wake` (3 minutes)

```cpp
// SOP-09 — wn_pir_wake
// WildNexus P0 — Phase I — Test PIR EKMB wake-up
// L'ESP32 dort. Le PIR le réveille. L'ESP32 imprime un message et se rendort.

#include "esp_sleep.h"

#define PIR_PIN 3  // GPIO pour le signal PIR

RTC_DATA_ATTR int wake_count = 0;

void setup() {
  Serial.begin(115200);
  delay(500);
  wake_count++;

  Serial.printf("=== PIR WAKE #%d ===\n", wake_count);

  // Vérifier l'état du PIR
  pinMode(PIR_PIN, INPUT);
  int pir_state = digitalRead(PIR_PIN);
  Serial.printf("PIR pin state: %s\n", pir_state ? "HIGH (mouvement)" : "LOW (calme)");

  Serial.flush();

  // Configurer le réveil par PIR (front montant)
  esp_sleep_enable_ext0_wakeup((gpio_num_t)PIR_PIN, 1);  // 1 = HIGH

  // Timer de sécurité : si pas de PIR pendant 120 secondes, réveil auto
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

```
        ESP32-S3 DevKit              PIR EKMB
        ┌──────────────┐             ┌──────────┐
        │  3V3 ────────┼──[rouge]────┼── VCC    │
        │  GND ────────┼──[noir]─────┼── GND    │
        │  IO3  ───────┼──[jaune]────┼── OUT    │
        └──────────────┘             └──────────┘
```

> Le PIR EKMB n'a que 3 broches. La doc est généralement sérigraphiée au dos.

---

## Étape 3 — Test fonctionnel (5 minutes)

1. ESP32 branché en USB, PIR câblé.
2. Flasher `wn_pir_wake`.
3. Moniteur série 115200 baud.
4. Observer :

```
=== PIR WAKE #1 ===
PIR pin state: LOW (calme)
Going to sleep — agitez la main devant le PIR

--- PIR détecte un mouvement ---

=== PIR WAKE #2 ===
PIR pin state: HIGH (mouvement)
Going to sleep — agitez la main devant le PIR
```

5. **Agiter la main à ~1-2 mètres** du PIR. Le message doit apparaître à chaque mouvement.

> ✅ Réveil à chaque mouvement → PIR fonctionnel en mode wake-up.

> ❌ Pas de réveil :
> - Vérifier le câblage (3V3 — pas 5V !)
> - Le PIR EKMB a un temps de stabilisation de ~10-30 secondes après mise sous tension
> - Certains modèles EKMB ont une sortie à collecteur ouvert — essayer avec une pull-up externe de 10kΩ sur OUT

---

## Étape 4 — Mesure PPK2 (5 minutes)

1. Débrancher USB.
2. PPK2 OFF → VOUT→5V, GND→GND de l'ESP32 (le PIR reste sur 3V3 de l'ESP32).
3. Source Meter 5.0V, acquisition, sortie ON.

```
Courant
  │
  │                                                  ┌──┐
  │                                                  │  │ wake PIR
  │                                                  │  │
  │──▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔┘  └────
  │   ←── deep sleep + PIR (quelques µA) ──→
  └──────────────────────────────────────────────────────→
```

| Mesure | Valeur |
|--------|--------|
| Deep sleep ESP32 + PIR (µA) | _____ µA |
| Pic réveil sur mouvement (mA) | _____ mA |
| Durée active (s) | _____ s |
| ⚠️ Le PIR déclenche-t-il des faux réveils ? | Oui / Non |

> 💡 Le PIR EKMB consomme ~1-6 µA. Ajouté aux ~50-150 µA du DevKit en deep sleep, le total devrait rester sous 150 µA. Si > 200 µA, le PIR n'est pas en cause — c'est le DevKit.

---

## Grille de décision

| Critère | ✅ GO | 🟠 Orange | ❌ NO-GO |
|---------|:-----:|:---------:|:--------:|
| Wake-up PIR | < 2s après mouvement | 2-5s | Pas de réveil |
| Faux réveils (10 min) | 0 | 1-2 | > 2 |
| Deep sleep + PIR | < 150 µA | 150-200 µA | > 200 µA |

---

## Clôture

- [ ] PIR branché (3V3, GND, OUT→IO3)
- [ ] Réveil ESP32 confirmé sur mouvement
- [ ] Pas de faux réveil en 10 minutes sans mouvement
- [ ] Mesure PPK2 : deep sleep + PIR notée
- [ ] Délai de réveil PIR noté

---

**Fin de SOP-09. Prochaine étape : SOP-10 Phase J — Alimentation AA + buck.**
