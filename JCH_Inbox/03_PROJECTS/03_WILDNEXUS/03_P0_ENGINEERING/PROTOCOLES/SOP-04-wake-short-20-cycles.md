# SOP-04 — Phase D : Réveil court 20 cycles

**SOP :** SOP-04  
**Projet :** WildNexus P0 — M-02 Prototype banc fonctionnel  
**Phase :** D — Réveil court, cycle sleep/wake 20 répétitions  
**Durée :** ~30 minutes  
**Prérequis :** SOP-03 réussi (PPK2 maîtrisé, mesures deep sleep OK)  
**Auteur :** [[Dobby]]  
**Date :** 2026-06-12  
**Version :** 1.0  

---

## Objectif

Mesurer un cycle complet réveil/action/sommeil sur 20 répétitions. Vérifier que l'ESP32-S3 se réveille proprement, exécute une courte tâche, puis retourne en deep sleep **sans dérive ni blocage**.

---

## ⚠️ Mêmes règles de sécurité que SOP-03

- Jamais USB + PPK2 en même temps
- Sortie PPK2 OFF avant branchement/débranchement
- Polarité VOUT→5V, GND→GND

---

## Matériel

Identique à SOP-03 : ESP32-S3 DevKit, PPK2, 2 fils Dupont, Mac.

---

## Étape 1 — Firmware `wn_wake_short` (3 minutes)

### 1.1 Créer le sketch

```cpp
// SOP-04 — wn_wake_short
// WildNexus P0 — Phase D — Réveil court 20 cycles
// L'ESP32 se réveille, fait une courte action (~2s), puis se rendort.
// Cycle de 15 secondes. On mesure 20 cycles pour vérifier la stabilité.

#include "esp_sleep.h"

#define CYCLE_COUNT 20

RTC_DATA_ATTR int boot_count = 0;  // Survit au deep sleep

void setup() {
  Serial.begin(115200);
  delay(500);

  boot_count++;
  Serial.printf("WN wake #%d — action start\n", boot_count);
  Serial.flush();

  // Simuler une courte action : lecture PIR + décision
  delay(2000);  // 2 secondes de traitement

  Serial.printf("WN wake #%d — going to sleep\n", boot_count);
  Serial.flush();

  // Après 20 cycles, arrêter et rester éveillé
  if (boot_count >= CYCLE_COUNT) {
    Serial.println("WN 20 cycles complete — staying awake");
    while (1) { delay(1000); }
  }

  // Sinon, dormir 15 secondes
  esp_sleep_enable_timer_wakeup(15ULL * 1000000ULL);
  esp_deep_sleep_start();
}

void loop() {}
```

### 1.2 Ce que fait ce firmware

```
Cycle 1:  wake → "WN wake #1" → action 2s → sleep 15s
Cycle 2:  wake → "WN wake #2" → action 2s → sleep 15s
...
Cycle 20: wake → "WN wake #20" → action 2s → STAY AWAKE
```

> 💡 `RTC_DATA_ATTR` conserve la variable `boot_count` dans la mémoire RTC (Real-Time Clock), qui survit au deep sleep. Sans cet attribut, `boot_count` serait remis à 0 à chaque réveil.

---

## Étape 2 — Vérifier sans PPK2 (5 minutes)

1. ESP32 branché en USB.
2. Flasher `wn_wake_short`.
3. Ouvrir le moniteur série (115200 baud).
4. Observer :

```
WN wake #1 — action start
WN wake #1 — going to sleep

--- 15 secondes ---

WN wake #2 — action start
WN wake #2 — going to sleep

...

WN wake #20 — action start
WN wake #20 — going to sleep
WN 20 cycles complete — staying awake
```

> ✅ Si les 20 cycles s'exécutent sans intervention → firmware OK.

> ❌ Si l'ESP32 se bloque avant le cycle 20 → réduire `CYCLE_COUNT` à 5 pour diagnostiquer.

---

## Étape 3 — Mesure PPK2 (15 minutes)

### 3.1 Branchement

1. **Débrancher l'USB** de l'ESP32.
2. Sortie PPK2 **OFF**.
3. Brancher PPK2 VOUT→5V, GND→GND (ordre : noir d'abord, rouge ensuite).
4. Power Profiler : Source Meter, 5.0 V, démarrer l'acquisition.
5. Activer la sortie PPK2.

### 3.2 Ce que vous devez voir

```
Courant
  │
  │  ┌──┐              ┌──┐              ┌──┐
  │  │  │ action 2s    │  │              │  │
  │  │  │ (~40-80 mA)  │  │              │  │
  │──┘  └──────────────┘  └──────────────┘  └───
  │   ←── 15 secondes ──→
  │
  │  ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔  ← deep sleep
  └────────────────────────────────────────────→
```

- 20 pics d'activité de ~2 secondes
- 15 secondes de deep sleep entre chaque
- Après le 20ᵉ pic : courant actif constant (normal, l'ESP32 reste éveillé)

### 3.3 Mesures à noter

Pour chaque cycle (ou moyenne sur 20 cycles) :

| Mesure | Où | Valeur |
|--------|-----|--------|
| Courant pic actif (mA) | Max pic | _____ mA |
| Durée pic actif (s) | Largeur pic | _____ s |
| Charge par cycle (mAh) | Power Profiler → Energy | _____ mAh |
| Deep sleep entre cycles (µA) | Moyenne zone plate | _____ µA |

### 3.4 Grille de décision

| Critère | ✅ GO | 🟠 Orange | ❌ NO-GO |
|---------|:-----:|:---------:|:--------:|
| Cycles complétés | 20/20 | 18-19/20 | < 18/20 |
| Retour deep sleep | Propre | Oscillations | Ne dort plus |
| Dérive courant deep sleep | Stable | ±20% | Croissance continue |
| Blocage | Aucun | 1 erreur récupérée | Blocage permanent |

---

## Étape 4 — Arrêt (2 minutes)

1. Sortie PPK2 OFF.
2. Débrancher rouge (VOUT) puis noir (GND).
3. Stop acquisition, sauvegarder.

---

## Clôture

### Checklist

- [ ] `wn_wake_short` compilé et flashé sans erreur
- [ ] 20 cycles vérifiés au moniteur série avant PPK2
- [ ] 20 pics mesurés au PPK2
- [ ] Retour au deep sleep après chaque pic
- [ ] Pas de blocage

### CSV

| Date | Test | Firmware | Tension | Cycles OK | Dérive | Résultat |
|------|------|----------|---------|-----------|--------|----------|
| YYYY-MM-DD | Phase D — réveil court | wn_wake_short | 5.0 V | __/20 | __ | GO / ORANGE / NO-GO |

---

**Fin de SOP-04. Prochaine étape : SOP-05 Phase E — Simulation cycle événement.**
