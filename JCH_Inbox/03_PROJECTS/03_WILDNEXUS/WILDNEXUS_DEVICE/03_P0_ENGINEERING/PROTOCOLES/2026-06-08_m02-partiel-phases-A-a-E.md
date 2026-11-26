# Protocole M-02 Partiel — Phases A→E (ESP32-S3 + PPK2)

**Date :** 2026-06-08  
**Projet :** [[WildNexus]]  
**Session :** Partielle — deep sleep, wake, cycle simulé  
**Matériel :** ESP32-S3 DevKit × 1, Nordic PPK2, Mac, câbles Dupont  
**Durée estimée :** ~2h  

---

## Matériel nécessaire

### Hardware

- 1 × ESP32-S3 DevKitC-1-N8R8
- 1 × Nordic PPK2
- 1 × câble USB-C data (programmation ESP32)
- 1 × câble USB (PPK2 → Mac)
- Câbles Dupont femelle-femelle (2 minimum : rouge + noir)
- Table non conductrice

### Logiciels

- Arduino IDE ou PlatformIO + board package ESP32 Espressif
- nRF Connect for Desktop + app Power Profiler

### Fichiers

| Fichier | Usage |
|---------|-------|
| `PROTOCOLES/2026-06-08_protocole-m02-esp32s3-ppk2.md` | Protocole complet (674 lignes) |
| `PROTOCOLES/2026-06-08_mesures-esp32s3-ppk2_template.csv` | Gabarit de mesures — lignes Phase C/D/E pré-remplies |

---

## Grille de décision

| Mesure | Go | Orange | No-Go |
|--------|:--:|:------:|:-----:|
| Deep sleep | < 100 µA | 100-150 µA | > 200 µA |
| Charge/événement | < 1.5 mAh | 1.5-2.5 mAh | > 2.5 mAh |
| Autonomie 3 evt/h | ≥ 60 j | 45-60 j | < 45 j |
| Stabilité | 100 cycles OK | 1-2 erreurs | Blocage récurrent |

> ⚠️ Le DevKit a un régulateur et des LEDs qui gonflent la conso. Un deep sleep à 150 µA sur DevKit ne condamne pas l'ESP32-S3 — on documente et on retestera sur PCB nu.

**En cas de No-Go :** alerter immédiatement [[Dobby]] → convocation [[Castor]] + [[Forge]] pour arbitrage migration MCU.
**En cas de Go ou Orange :** ESP32-S3 validé pour la suite P0.

---

## Règles de sécurité

1. Ne jamais alimenter l'ESP32 par USB et par PPK2 en même temps pendant une mesure.
2. USB ESP32 = programmation uniquement. PPK2 = alimentation et mesure uniquement.
3. Avant de brancher le PPK2 sur l'ESP32, la sortie PPK2 doit être sur OFF.
4. Vérifier deux fois la polarité : VOUT vers 5V, GND vers GND.
5. Si la carte chauffe, couper immédiatement la sortie PPK2.
6. Si le courant dépasse 500 mA sans raison, couper et vérifier le câblage.
7. Ne jamais brancher du 5V sur une broche GPIO.

> ⚠️ **DANGER — Destruction matérielle :** la double alimentation (USB + PPK2 simultanés) ou une inversion de polarité provoque des dommages irréversibles au DUT ou au PPK2. Vérifier que la sortie Power Profiler est sur **OFF** avant chaque changement de câblage.

---

## Vocabulaire

| Mot | Sens |
|-----|------|
| DUT | Device Under Test : l'ESP32-S3 testée |
| PPK2 | Appareil qui alimente et mesure le courant |
| Source Meter | Mode où le PPK2 alimente l'ESP32 et mesure |
| Deep sleep | Mode sommeil profond ESP32-S3 |
| Cycle événement | Réveil → action → retour sommeil |

---

## Phase A — Vérification ESP32 alive (10 min)

**But :** vérifier que l'ESP32 fonctionne avant d'ajouter la mesure.

1. Poser l'ESP32-S3 sur une table non conductrice.
2. Brancher le câble USB-C entre le Mac et l'ESP32. **PPK2 débranché.**
3. Ouvrir Arduino IDE → choisir la carte ESP32-S3 DevKit → choisir le port série.
4. Flasher le firmware `wn_blink`.
5. Ouvrir le moniteur série à 115200 bauds.
6. Vérifier que "WildNexus ESP32-S3 alive" apparaît toutes les secondes.
7. Si rien : maintenir BOOT pendant l'upload.

### Firmware `wn_blink`

```cpp
void setup() {
  Serial.begin(115200);
}
void loop() {
  Serial.println("WildNexus ESP32-S3 alive");
  delay(1000);
}
```

> ⚠️ **POINT DE RUPTURE — BASCULE D'ALIMENTATION :** à partir d'ici, le PPK2 prend le relais. **Débrancher le câble USB de l'ESP32 avant toute intervention sur le PPK2.**

---

## Phase B — Deep sleep vérification (10 min)

**But :** préparer la carte pour une mesure de sommeil profond.

1. Flasher `wn_deep_sleep_30s` par USB.
2. Ouvrir le moniteur série → message "WildNexus deep sleep test".
3. Attendre 30 secondes → le message revient → firmware OK.
4. Fermer le moniteur série.
5. Débrancher le câble USB de l'ESP32.

### Firmware `wn_deep_sleep_30s`

```cpp
#include "esp_sleep.h"
void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("WildNexus deep sleep test");
  Serial.flush();
  esp_sleep_enable_timer_wakeup(30ULL * 1000000ULL);
  esp_deep_sleep_start();
}
void loop() {}
```

---

## Phase C — Mesure deep sleep PPK2 (20 min)

**But :** première mesure réelle de la consommation en sommeil profond.

### Réglage PPK2

Dans Power Profiler :
1. Sélectionner **Source Meter**.
2. Régler tension de sortie à **5.0 V**.
3. Limite de courant à **500 mA** si l'option est disponible.
4. Vérifier que la sortie est **OFF**.
5. Cliquer **[[Start]]** pour préparer l'acquisition.

### Branchement

ESP32 débranché de l'USB.

| PPK2 | ESP32-S3 DevKit |
|------|-----------------|
| VOUT | 5V |
| GND | GND |

1. Brancher le fil noir : PPK2 GND → ESP32 GND.
2. Brancher le fil rouge : PPK2 VOUT → ESP32 5V.
3. Vérifier que rien n'est branché sur USB ESP32.
4. Vérifier que VOUT ne touche aucune broche GPIO.

### Mesure

1. Activer la sortie PPK2 dans Power Profiler.
2. Observer la courbe — attendre au moins 2 minutes.
3. Chercher les pics de réveil toutes les 30 secondes.
4. Zoomer sur les zones plates entre les pics.
5. Noter dans le CSV :
   - Courant deep sleep stable entre deux pics (µA)
   - Courant pic au réveil (mA)
   - Durée du pic actif (s)
   - Charge consommée sur un cycle si Power Profiler l'affiche

| Observation | Signification |
|-------------|--------------|
| Pics toutes les 30s | ✅ Firmware OK |
| Pas de pic, courant nul | Mauvais câblage ou sortie OFF |
| Courant très élevé constant | Carte pas en sleep ou court-circuit |
| Deep sleep en mA | DevKit probablement trop consommateur, à documenter |

> ⚠️ **POINT DE RUPTURE :** débrancher le PPK2 avant de rebrancher l'USB pour le flashage du firmware suivant.

---

## Phase D — Réveil court (30 min)

**But :** mesurer un réveil simple et un retour sommeil propre.

1. **Débrancher d'abord le PPK2** de l'ESP32.
2. Rebrancher l'ESP32 en USB.
3. Flasher `wn_wake_short`.
4. Débrancher USB.
5. Rebrancher PPK2 comme en Phase C.
6. Mesurer 20 cycles.

**Résultat attendu :**
- Pic actif d'environ 2 à 3 secondes
- Retour net au deep sleep
- 20 cycles sans blocage

Si le courant ne redescend jamais, le firmware ne dort pas ou un périphérique reste actif.

### Firmware `wn_wake_short`

```cpp
#include "esp_sleep.h"
void setup() {
  Serial.begin(115200);
  delay(500);
  Serial.println("WildNexus wake short");
  delay(2000);
  Serial.flush();
  esp_sleep_enable_timer_wakeup(30ULL * 1000000ULL);
  esp_deep_sleep_start();
}
void loop() {}
```

---

> ⚠️ **POINT DE RUPTURE :** débrancher le PPK2 avant de rebrancher l'USB pour le flashage du firmware suivant.

## Phase E — Cycle simulé WildNexus (30 min)

**But :** mesurer un cycle proche de la logique P0 sans attendre tous les modules.

Le firmware simule : réveil PIR (2s) → capture caméra (5s) → écriture SD (2s) → transmission LoRa (2s) = **11 secondes actives**.

1. Débrancher PPK2 → rebrancher USB → flasher `wn_event_simulated`.
2. Débrancher USB → rebrancher PPK2 comme en Phase C.
3. Mesurer 10 cycles.
4. Noter dans le CSV : `courant_actif_moyen_mA`, `duree_active_s`, `charge_evenement_mAh`.

> 💡 Power Profiler peut donner la charge directement (onglet « Charge » ou « Energy ») — plus fiable que le calcul manuel `mA × s / 3600`.

### Firmware `wn_event_simulated`

```cpp
#include "esp_sleep.h"
void setup() {
  Serial.begin(115200);
  delay(500);
  Serial.println("WN event start");
  delay(2000);  // réveil + PIR simulé
  delay(5000);  // capture caméra simulée
  delay(2000);  // écriture SD simulée
  delay(2000);  // transmission LoRa simulée
  Serial.println("WN event sleep");
  Serial.flush();
  esp_sleep_enable_timer_wakeup(60ULL * 1000000ULL);
  esp_deep_sleep_start();
}
void loop() {}
```

### Calcul d'autonomie

```
Autonomie (jours) = capacité_batterie_mAh / (charge_evenement_mAh × evt_par_heure × 24)
```

Exemple avec 4 piles AA lithium (4S1P, ~3000 mAh) à 3 événements/heure :
```
3000 / (charge × 3 × 24) = 3000 / (charge × 72)
```
- Si charge = 0.37 mAh → 3000 / 26.6 = **~113 jours** ✅
- Si charge = 1.5 mAh → 3000 / 108 = **~28 jours** ❌

---

## Après la session

1. Remplir les colonnes Phase C/D/E dans `2026-06-08_mesures-esp32s3-ppk2_template.csv`
2. Comparer aux seuils Go / Orange / No-Go
3. Si tout est en Go ou Orange → ESP32-S3 reste candidat P0
4. Si No-Go sur plusieurs critères → alerter [[Dobby]] → convocation [[Castor]] + [[Forge]] pour arbitrage migration MCU