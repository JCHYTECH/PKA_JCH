# SOP-05 — Phase E : Simulation cycle événement WildNexus

**SOP :** SOP-05  
**Projet :** WildNexus P0 — M-02 Prototype banc fonctionnel  
**Phase :** E — Simulation cycle complet (PIR + caméra + SD + LoRa)  
**Durée :** ~30 minutes  
**Prérequis :** SOP-04 réussi (cycles sleep/wake stables)  
**Auteur :** [[Dobby]]  
**Date :** 2026-06-12  
**Version :** 1.0  

---

## Objectif

Simuler un cycle événementiel complet **sans les périphériques physiques** : réveil PIR → capture caméra → écriture SD → transmission LoRa → retour sommeil. Cette simulation donne la charge de référence (mAh/événement) pour le calcul d'autonomie.

> ⚠️ Les délais sont simulés avec `delay()`. Quand les vrais modules seront branchés, on remplacera les `delay()` par les opérations réelles et on refera cette mesure.

---

## Matériel

Identique SOP-03/04 : ESP32-S3, PPK2, 2 fils Dupont, Mac.

---

## Étape 1 — Firmware `wn_sim_event` (3 minutes)

### 1.1 Créer le sketch

```cpp
// SOP-05 — wn_sim_event
// WildNexus P0 — Phase E — Simulation cycle événement complet
// Simule : PIR wake → caméra capture → écriture SD → TX LoRa → deep sleep
// Cycle de 60 secondes entre événements.

#include "esp_sleep.h"

RTC_DATA_ATTR int event_count = 0;

void setup() {
  Serial.begin(115200);
  delay(500);

  event_count++;
  Serial.printf("=== WN EVENT #%d ===\n", event_count);

  // 1. Réveil + traitement PIR simulé
  Serial.println("[1/4] PIR wake + decision");
  delay(2000);

  // 2. Capture caméra simulée
  Serial.println("[2/4] Camera capture");
  delay(5000);

  // 3. Écriture SD simulée
  Serial.println("[3/4] SD write");
  delay(2000);

  // 4. Transmission LoRa simulée
  Serial.println("[4/4] LoRa TX");
  delay(2000);

  Serial.printf("=== EVENT #%d SLEEP ===\n", event_count);
  Serial.flush();

  // Dormir 60 secondes avant le prochain événement
  esp_sleep_enable_timer_wakeup(60ULL * 1000000ULL);
  esp_deep_sleep_start();
}

void loop() {}
```

### 1.2 Timeline d'un événement

```
      0s       2s              7s      9s     11s        71s
      │────────│───────────────│───────│──────│──────────│
      │  PIR   │   CAMERA      │  SD   │ LORA │  SLEEP   │
      │ 2 sec  │   5 sec       │ 2 sec │ 2 sec│  60 sec  │
      │────────│───────────────│───────│──────│──────────│
      ←─────────── 11 secondes actives ──────────→
```

---

## Étape 2 — Vérifier sans PPK2 (5 minutes)

1. ESP32 branché USB.
2. Flasher `wn_sim_event`.
3. Moniteur série 115200 baud.
4. Observer 2-3 cycles :

```
=== WN EVENT #1 ===
[1/4] PIR wake + decision
[2/4] Camera capture
[3/4] SD write
[4/4] LoRa TX
=== EVENT #1 SLEEP ===

--- 60 secondes ---

=== WN EVENT #2 ===
...
```

> ✅ Les 4 phases s'affichent → firmware OK.

---

## Étape 3 — Mesure PPK2 (15 minutes)

### 3.1 Branchement (identique SOP-03/04)

1. Débrancher USB ESP32.
2. PPK2 OFF → brancher VOUT→5V, GND→GND.
3. Source Meter 5.0V, démarrer acquisition.
4. Sortie PPK2 ON.

### 3.2 Courbe attendue

```
Courant
  │
  │  ┌──────────────────────┐
  │  │  11 secondes actives │
  │  │  PIR│CAMERA  │SD│LORA│
  │  │  ~40-80 mA           │
  │──┘                      └──────────────────────────┐
  │                                                    │
  │  ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔  ← 60s   │
  └────────────────────────────────────────────────────────→
```

### 3.3 Mesures à prendre (sur la moyenne de 5 cycles)

| Mesure | Méthode | Valeur |
|--------|---------|--------|
| Courant actif moyen (mA) | Sélectionner la zone active de 11s → Average | _____ mA |
| Durée active (s) | Distance entre début pic et retour sleep | _____ s |
| Charge par événement (mAh) | Power Profiler → Energy / Charge | _____ mAh |
| Deep sleep (µA) | Moyenne zone plate entre événements | _____ µA |
| Pic max (mA) | Maximum absolu du pic | _____ mA |

### 3.4 Calcul autonomie

Si Power Profiler n'affiche pas la charge, utiliser cette formule :

```
Charge (mAh) = Courant_actif_moyen (mA) × Durée_active (s) / 3600
```

**Exemple :** 80 mA × 11 s / 3600 = **0.244 mAh par événement**

Puis :

```
Autonomie (jours) = Capacité_batterie (mAh) / (Charge_événement × Événements_jour + Conso_veille_jour)
```

| Scénario | Événements/jour | Autonomie avec 8000 mAh (8×AA) |
|----------|:---------------:|--------------------------------|
| Faible activité | 72 (3/h) | _____ jours |
| Activité moyenne | 240 (10/h) | _____ jours |
| Activité intense | 720 (30/h) | _____ jours |

### 3.5 Grille de décision

| Critère | ✅ GO | 🟠 Orange | ❌ NO-GO |
|---------|:-----:|:---------:|:--------:|
| Charge/événement | < 0.5 mAh | 0.5-1.0 mAh | > 1.0 mAh |
| Autonomie 3 evt/h | ≥ 60 jours | 45-60 jours | < 45 jours |
| Stabilité 10 cycles | 10/10 | 1-2 erreurs | Blocage |

---

## Clôture

### Checklist

- [ ] `wn_sim_event` compilé et flashé
- [ ] 4 phases simulées visibles au moniteur série
- [ ] 10 cycles mesurés au PPK2
- [ ] Charge par événement calculée
- [ ] Autonomie extrapolée pour 3 scénarios

### CSV

| Date | Test | Firmware | Charge/evt | Durée active | Deep sleep | Autonomie 3evt/h | Résultat |
|------|------|----------|------------|-------------|-----------|-----------------|----------|
| YYYY-MM-DD | Phase E — sim event | wn_sim_event | __ mAh | __ s | __ µA | __ jours | GO / ORANGE / NO-GO |

---

## Transition

> Les phases A→E valident l'ESP32-S3 **seul**. Les phases F→J ajoutent les périphériques un par un. Chaque phase F→J doit réussir individuellement avant de passer à l'intégration complète.

---

**Fin de SOP-05. Prochaine étape : SOP-06 Phase F — Test microSD.**
