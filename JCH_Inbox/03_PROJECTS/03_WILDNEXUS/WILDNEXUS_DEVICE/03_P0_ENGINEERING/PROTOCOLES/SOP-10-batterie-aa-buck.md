# SOP-10 — Phase J : Alimentation AA + buck TPS62840

**SOP :** SOP-10  
**Projet :** WildNexus P0 — M-02 Prototype banc fonctionnel  
**Phase :** J — Test alimentation 6×AA + buck 3.3V  
**Durée :** ~30 minutes  
**Prérequis :** SOP-05 réussi, buck TPS62840 et porte-piles AA disponibles  
**Auteur :** [[Dobby]]  
**Date :** 2026-06-12  
**Version :** 1.1 — Ajout note dropout voltage AMS1117 (2026-06-19, source: system-improvement-ingest ESP32 Battery)

---

## ⚠️ DANGER — LIRE AVANT DE COMMENCER

Cette phase est la plus risquée électriquement.

1. **Polarité des piles :** une pile inversée = court-circuit = chaleur extrême.
2. **Sortie buck avant branchement ESP32 :** mesurer la tension de sortie AVANT de brancher l'ESP32. Si > 3.6V → le buck est mal configuré → ne pas brancher.
3. **Ne jamais court-circuiter les bornes du porte-piles** avec un outil métallique.
4. **Mode Ampère Meter du PPK2 :** branchement en série entre une source d'énergie et une charge. Risque d'inversion si on se trompe.

> ### 🧠 Leçon apprise — Piège dropout voltage AMS1117
> Les DevKits ESP32 standard (et l'ESP32-CAM A02a) utilisent un régulateur **AMS1117** dont le **dropout voltage est de 1.2V**. Pour réguler correctement à 3.3V, il faut **minimum 4.5V en entrée**. Une batterie lithium 3.7V (4.2V max chargée) connectée directement au VIN est **sous le seuil** → le régulateur passe en pass-through → la tension 3.3V devient instable → **les lectures ADC sont faussées** (tension batterie lue incorrectement).
> 
> **Solution :** toujours utiliser un boost converter (5V) ou un buck (notre TPS62840) entre la batterie et l'ESP32. Ne jamais connecter une li-ion directement au VIN si on a besoin de lectures ADC fiables.
> **Source :** Transcript « How to Power an Arduino ESP32 with a 3.7V Lithium Battery » — analysé via system-improvement-ingest, 2026-06-19.

---

## Matériel spécifique

| # | Élément |
|---|---------|
| 1 | Buck TPS62840 (module breakout) |
| 2 | 6× piles AA (alcalines ou NiMH) |
| 3 | Porte-piles 6×AA (configuration 4S2P impossible en porte-piles standard → utiliser 6×AA en série pour ce test, soit ~9V nominal) |
| 4 | Multimètre |

> 💡 **Note BOM :** Le BOM final prévoit 8×AA en 4S2P (~6V nominal). Pour ce test banc, on utilise ce qu'on a — l'important est de valider le buck et la consommation batterie.

---

## Étape 1 — Vérifier la tension du buck AVANT branchement (5 minutes)

### 1.1 Alimenter le buck seul

1. Insérer les 6×AA dans le porte-piles (vérifier les polarités !).
2. Brancher le (+) du porte-piles sur VIN du buck.
3. Brancher le (-) du porte-piles sur GND du buck.
4. **Ne rien brancher sur la sortie du buck.**
5. Allumer le multimètre, mode voltmètre DC.
6. Mesurer entre VOUT et GND du buck :

```
Porte-piles (+) ─── VIN ─── [BUCK TPS62840] ─── VOUT ─── (multimètre +)
Porte-piles (-) ─── GND ───                   ─── GND ─── (multimètre -)
```

**Tension attendue : 3.3V ± 0.1V**

> ✅ 3.3V stable → buck OK.

> ❌ 0V → vérifier les soudures du buck, la connexion des piles.
> ❌ > 3.6V → le buck n'est pas configuré correctement (résistance de feedback). **Ne pas brancher l'ESP32.**

---

## Étape 2 — Firmware `wn_battery_test` (3 minutes)

```cpp
// SOP-10 — wn_battery_test
// WildNexus P0 — Phase J — Test alimentation batterie
// Simule le cycle événementiel complet sur alimentation AA+buck.

#include "esp_sleep.h"

RTC_DATA_ATTR int cycle = 0;

void setup() {
  Serial.begin(115200);
  delay(500);
  cycle++;

  Serial.printf("=== BATT TEST #%d ===\n", cycle);

  // Simuler cycle événementiel (11 secondes actives)
  delay(2000);  // PIR
  delay(5000);  // Caméra
  delay(2000);  // SD
  delay(2000);  // LoRa

  Serial.println("Cycle done → sleep");
  Serial.flush();
  esp_sleep_enable_timer_wakeup(60ULL * 1000000ULL);
  esp_deep_sleep_start();
}

void loop() {}
```

---

## Étape 3 — Mesure PPK2 en Ampère Meter (15 minutes)

### 3.1 Configuration

Le mode **Ampère Meter** mesure le courant entre une source externe (batterie) et le DUT.

```
Piles AA → Buck 3.3V → PPK2 (Ampère Meter) → ESP32-S3
                         │
                         └── Mesure le courant
```

### 3.2 Branchement

1. **Débrancher tout.**
2. Brancher les piles → buck → sortie 3.3V.
3. **PPK2 en mode Ampère Meter.**
4. Brancher la sortie du buck sur PPK2 **VIN+** et **VIN-** (entrée mesure).
5. Brancher PPK2 **VOUT+** et **VOUT-** sur ESP32 **5V** et **GND**.

```
Piles AA ─── Buck 3.3V ─── VOUT ─── PPK2 VIN+
                         ─── GND  ─── PPK2 VIN-
                                        │
                                   PPK2 VOUT+ ─── ESP32 5V
                                   PPK2 VOUT- ─── ESP32 GND
```

> ⚠️ **Double vérification de la polarité à chaque étape.**

### 3.3 Mesure

1. Power Profiler : Ampère Meter, acquisition.
2. Observer au moins 3 cycles.
3. Courbe attendue : identique à la Phase E (simulation), mais la tension d'entrée est 3.3V (buck) au lieu de 5V (USB/PPK2). Les courants seront différents.

| Mesure | Valeur |
|--------|--------|
| Tension buck en charge (V) | _____ V |
| Courant deep sleep buck+ESP32 (µA) | _____ µA |
| Courant pic actif (mA) | _____ mA |
| Charge par cycle (mAh) | _____ mAh |
| Rendement estimé buck | _____ % |

### 3.4 Calcul du rendement buck

```
Rendement = (P_sortie / P_entrée) × 100

P_entrée = V_piles × I_piles
P_sortie = 3.3V × I_ESP32_actif_moyen
```

> Un buck TPS62840 devrait avoir > 85% de rendement à faible charge.

---

## Grille de décision

| Critère | ✅ GO | 🟠 Orange | ❌ NO-GO |
|---------|:-----:|:---------:|:--------:|
| Tension buck | 3.3V ± 0.1V | 3.2-3.5V | < 3.1V ou > 3.6V |
| Deep sleep buck | < 200 µA | 200-400 µA | > 400 µA |
| Rendement buck | > 85% | 70-85% | < 70% |
| Stabilité sur 30 min | Aucune variation | < 5% variation | Variations > 5% |

---

## Clôture

- [ ] Buck vérifié au multimètre AVANT branchement ESP32 (3.3V)
- [ ] Piles insérées dans le bon sens
- [ ] PPK2 en Ampère Meter correctement câblé
- [ ] 3 cycles mesurés sur batterie
- [ ] Rendement buck estimé
- [ ] Conso veille sur batterie notée

---

**Fin de SOP-10. Prochaine étape : SOP-11 Phase K — Benchmark Edge AI.**