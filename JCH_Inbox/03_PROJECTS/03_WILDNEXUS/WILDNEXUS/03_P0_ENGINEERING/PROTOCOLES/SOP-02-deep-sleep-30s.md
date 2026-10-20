# SOP-02 — Phase B : Deep sleep 30 secondes

**SOP :** SOP-02  
**Projet :** WildNexus P0 — M-02 Prototype banc fonctionnel  
**Phase :** B — Deep sleep 30s  
**Durée :** ~10 minutes  
**Prérequis :** SOP-01 réussi (ESP32 alive confirmé)  
**Auteur :** [[Dobby]]  
**Date :** 2026-06-12  
**Version :** 1.0  

---

## Objectif

Flasher un firmware qui met l'ESP32-S3 en sommeil profond (*deep sleep*) pendant 30 secondes, puis le réveille automatiquement. Vérifier que le cycle sleep/wake fonctionne avant de mesurer la consommation.

---

## Matériel

| # | Élément |
|---|---------|
| 1 | ESP32-S3 DevKitC-1 (déjà branché en USB depuis SOP-01) |
| 2 | Câble USB-C data |
| 3 | Mac + Arduino IDE |

> **Le PPK2 n'est PAS utilisé dans cette phase.** On vérifie le comportement logiciel uniquement.

---

## Étape 1 — Créer le firmware `wn_deep_sleep_30s` (3 minutes)

### 1.1 Nouveau sketch

1. Dans Arduino IDE : **File → New**.
2. Effacer tout.
3. Copier-coller :

```cpp
// SOP-02 — wn_deep_sleep_30s
// WildNexus P0 — Phase B — Deep sleep 30s
// L'ESP32-S3 s'endort 30 secondes, se réveille, imprime un message,
// puis se rendort. Cycle infini.

#include "esp_sleep.h"

void setup() {
  Serial.begin(115200);
  delay(1000);  // Laisser le temps au moniteur série de s'ouvrir

  Serial.println("WildNexus deep sleep test");
  Serial.println("Endormissement 30s...");
  Serial.flush();  // Vider le buffer avant de dormir

  // Configurer le réveil par timer : 30 secondes
  // La valeur est en microsecondes : 30 × 1 000 000
  esp_sleep_enable_timer_wakeup(30ULL * 1000000ULL);

  // Entrer en deep sleep
  esp_deep_sleep_start();
}

void loop() {
  // Ce code n'est jamais exécuté.
  // Après deep sleep, l'ESP32 redémarre → setup() est appelé à nouveau.
}
```

4. **File → Save As** → `wn_deep_sleep_30s` → sauvegarder.

### 1.2 Comprendre ce que fait ce code

```
┌──────────────────────────────────────────────────────┐
│                 CYCLE DEEP SLEEP                      │
│                                                      │
│  setup() ──→ "WildNexus deep sleep test"             │
│           ──→ esp_deep_sleep_start()                 │
│           ──→ [ ESP32 dort 30 secondes ]             │
│           ──→ [ Timer interne réveille l'ESP32 ]     │
│           ──→ setup() redémarre                      │
│           ──→ "WildNexus deep sleep test"            │
│           ──→ ...                                    │
└──────────────────────────────────────────────────────┘
```

> 💡 `loop()` est vide parce qu'après un deep sleep, l'ESP32 redémarre complètement. Il repasse toujours par `setup()`. C'est normal.

---

## Étape 2 — Flasher et observer (5 minutes)

### 2.1 Upload

1. Vérifier que l'ESP32 est branché en USB (port UART).
2. Vérifier **Tools → Board** : `ESP32S3 Dev Module`.
3. Vérifier **Tools → Port** : le bon port sélectionné.
4. Cliquer **Upload**.

### 2.2 Ouvrir le moniteur série

1. Ouvrir le **Serial Monitor** (icône loupe).
2. Vérifier vitesse : **115200 baud**.

### 2.3 Ce que vous devez voir

```
WildNexus deep sleep test
Endormissement 30s...

--- [silence 30 secondes] ---

WildNexus deep sleep test
Endormissement 30s...

--- [silence 30 secondes] ---

WildNexus deep sleep test
...
```

Le message apparaît, puis plus rien pendant **exactement 30 secondes**, puis le message réapparaît.

> ⏱️ **Utiliser le chronomètre** du Mac ou d'un téléphone pour vérifier que l'intervalle est bien 30 secondes (à ±2 secondes près).

> ✅ **GO — Le cycle deep sleep fonctionne.**
>
> L'ESP32-S3 sait s'endormir et se réveiller sur timer interne.

> ❌ **Si le message apparaît en continu sans pause :**
>
> → Le deep sleep n'a pas fonctionné. Vérifier le code :
>   - `esp_sleep_enable_timer_wakeup` est-il présent ?
>   - `esp_deep_sleep_start()` est-il appelé ?
>   - Le `#include "esp_sleep.h"` est-il en haut ?
> → Reflasher.

> ❌ **Si rien ne réapparaît après 30 secondes :**
>
> 1. Attendre 60 secondes (certains DevKits ont un délai de boot plus long après deep sleep).
> 2. Appuyer sur le bouton **EN** (Reset) — le message doit apparaître immédiatement.
> 3. Si le Reset manuel fonctionne mais pas le réveil automatique :
>    → Problème de timer RTC. Vérifier que la carte sélectionnée est bien **ESP32S3 Dev Module**.
>    → Certaines vieilles versions du package ESP32 ont un bug. Mettre à jour via Boards Manager.

> ❌ **Si le message est coupé en plein milieu :**
>
> → Le `Serial.flush()` n'a pas vidé le buffer. Vérifier qu'il est bien avant `esp_deep_sleep_start()`.

---

## Étape 3 — Fermer proprement (1 minute)

1. **Fermer le moniteur série.** (Obligatoire avant la Phase C, sinon le port reste occupé.)
2. Laisser l'ESP32 branché en USB pour l'instant.

---

## Clôture de la Phase B

### Checklist

- [x] `wn_deep_sleep_30s` compile sans erreur
- [x] Le message "WildNexus deep sleep test" apparaît
- [x] Silence de ~30 secondes entre chaque message
- [x] Le cycle se répète au moins 3 fois sans intervention
- [x] Moniteur série fermé

### CSV

| Date | Test | Firmware | Résultat |
|------|------|----------|----------|
| YYYY-MM-DD | Phase B — deep sleep 30s | wn_deep_sleep_30s | ✅ GO |

---

## Transition vers la Phase C

> ⚠️ **POINT DE RUPTURE — À PARTIR D'ICI, LE PPK2 ENTRE EN JEU.**
>
> Avant de passer à la Phase C :
> 1. **Débrancher le câble USB de l'ESP32.**
> 2. Sortir le PPK2 de sa boîte.
> 3. Passer à SOP-03.

---

**Fin de SOP-02. Prochaine étape : SOP-03 Phase C — Mesure deep sleep PPK2.**
