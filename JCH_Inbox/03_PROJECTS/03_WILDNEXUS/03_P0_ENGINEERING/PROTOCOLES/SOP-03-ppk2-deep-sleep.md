# SOP-03 — Phase C : Mesure deep sleep PPK2

**SOP :** SOP-03  
**Projet :** WildNexus P0 — M-02 Prototype banc fonctionnel  
**Phase :** C — Mesure PPK2 en Source Meter (deep sleep)  
**Durée :** ~25 minutes  
**Prérequis :** SOP-02 réussi — ESP32 débranché de l'USB, PPK2 disponible  
**Auteur :** [[Dobby]]  
**Date :** 2026-06-12  
**Version :** 1.0  

---

## ⚠️ RÈGLES DE SÉCURITÉ — À LIRE AVANT DE COMMENCER

| # | Règle | Pourquoi |
|---|-------|----------|
| 1 | **Jamais USB + PPK2 en même temps** sur l'ESP32 | Double alimentation = destruction du DUT ou du PPK2 |
| 2 | **Sortie PPK2 toujours OFF** avant de brancher/débrancher | Évite les courts-circuits au branchement |
| 3 | **Polarité : VOUT → 5V, GND → GND** | Inversion = destruction immédiate |
| 4 | **VOUT ne touche aucune broche GPIO** | 5 V sur une GPIO 3.3 V = destruction |
| 5 | Si la carte **chauffe** → couper immédiatement la sortie PPK2 | Surchauffe = court-circuit ou défaut |
| 6 | Si courant **> 500 mA** → couper immédiatement | Anormal pour un ESP32-S3 au repos |

> ⚠️ **Ces règles sont non-négociables. Une seule erreur peut détruire le matériel.**

---

## Matériel

| # | Élément | Rôle |
|---|---------|------|
| 1 | ESP32-S3 DevKit (firmware `wn_deep_sleep_30s` flashé) | DUT |
| 2 | Nordic PPK2 | Alimentation + mesure |
| 3 | Câble USB (PPK2 → Mac) | Communication PPK2 |
| 4 | 2 câbles Dupont femelle-femelle : 1 rouge, 1 noir | Alimentation ESP32 |
| 5 | Mac + nRF Connect + Power Profiler | Acquisition |

---

## Étape 1 — Préparer le PPK2 (5 minutes)

### 1.1 Installer nRF Connect et Power Profiler (une seule fois)

Si pas déjà fait :

1. Télécharger **nRF Connect for Desktop** depuis https://www.nordicsemi.com/Products/Development-tools/nRF-Connect-for-desktop
2. Installer et ouvrir.
3. Dans nRF Connect, trouver l'application **Power Profiler** et cliquer **Install**.
4. Une fois installée, cliquer **Open**.

### 1.2 Brancher le PPK2 au Mac

1. Prendre le câble USB du PPK2 (micro-USB ou USB-C selon modèle).
2. Brancher côté PPK2, côté Mac.
3. Ouvrir **Power Profiler** depuis nRF Connect.
4. Dans Power Profiler, cliquer **Select Device**.
5. Le PPK2 doit apparaître dans la liste (ex: `PPK2 - 000682XXXXXX`).
6. Sélectionner le PPK2.

> ✅ **VÉRIFICATION :** Le PPK2 apparaît dans Power Profiler. La LED sur le PPK2 s'allume.

### 1.3 Configurer le mode Source Meter

Dans Power Profiler :

1. Dans le panneau de configuration (à droite ou en bas) :
   - **Mode** : sélectionner **Source Meter**.
   - **Voltage** : régler à **5000 mV** (5.0 V).
   - **Current limit** : régler à **500 mA** (si l'option existe).
2. **Vérifier que la sortie est sur OFF** (bouton ou interrupteur visuel).
3. Cliquer **[[Start]]** pour préparer l'acquisition (la courbe démarre mais aucun courant ne circule encore).

```
┌─ Power Profiler ─────────────────────────────────┐
│                                                   │
│  Mode: [Source Meter ▼]                           │
│  Voltage: [5000 mV]                               │
│  Current limit: [500 mA]                          │
│                                                   │
│  Output: ⚫ OFF  →  Cliquer pour ON               │
│                                                   │
│  ┌─────────────────────────────────────────┐      │
│  │                                         │      │
│  │        COURBE (plate à 0 mA)            │      │
│  │                                         │      │
│  └─────────────────────────────────────────┘      │
│                                                   │
│  [Start]  [Stop]  [Clear]                         │
└───────────────────────────────────────────────────┘
```

> ⚠️ **Ne PAS activer la sortie maintenant.**

---

## Étape 2 — Brancher le PPK2 à l'ESP32 (3 minutes)

### 2.1 Vérifications AVANT branchement

- [ ] ESP32-S3 **débranché** du câble USB
- [ ] Sortie PPK2 sur **OFF**
- [ ] Power Profiler en mode **Source Meter, 5.0 V**
- [ ] Fils Dupont identifiés : **rouge = VOUT, noir = GND**

### 2.2 Branchement physique

```
PPK2                           ESP32-S3 DevKit
┌──────────┐                   ┌──────────────┐
│          │                   │              │
│  VOUT ───┼───[fil rouge]─────┼── 5V         │
│  GND  ───┼───[fil noir]──────┼── GND        │
│          │                   │              │
└──────────┘                   └──────────────┘
```

**Ordre impératif :**

1. **D'abord le GND** : brancher le fil noir entre PPK2 GND et ESP32 GND.
2. **Ensuite le VOUT** : brancher le fil rouge entre PPK2 VOUT et ESP32 5V.
3. Vérifier que les broches **ne se touchent pas entre elles**.
4. Vérifier que **rien n'est branché sur l'USB de l'ESP32**.

> 🔍 **DOUBLE CHECK :** Suivre chaque fil du doigt. PPK2 VOUT → ESP32 5V. PPK2 GND → ESP32 GND. Aucun autre branchement.

---

## Étape 3 — Mesure (10 minutes)

### 3.1 Activer la sortie PPK2

1. Dans Power Profiler, cliquer pour activer la sortie (**Output ON**).
2. Observer immédiatement la courbe.

**Ce que vous devez voir apparaître :**

```
Courant
  │
  │  ┌─┐                    ┌─┐
  │  │ │ pic réveil         │ │ pic réveil
  │  │ │ (~40-80 mA)        │ │
  │  │ │                    │ │
  │──┘ └────────────────────┘ └──────────────
  │   ←── 30 secondes ────→
  │
  │  ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔  ← deep sleep (quelques µA)
  └──────────────────────────────────────────→ Temps
```

### 3.2 Ce que vous observez

| Ce que vous voyez | Signification |
|-------------------|---------------|
| Pics toutes les ~30 secondes | ✅ Cycle deep sleep normal |
| Ligne plate entre les pics | ✅ L'ESP32 dort |
| Courant nul (0 mA) en permanence | Mauvais branchement ou sortie OFF |
| Courant élevé constant (>20 mA) | Carte ne dort pas, vérifier firmware |
| Pas de pic, ligne droite basse | Timer RTC non configuré |

### 3.3 Prendre les mesures

1. **Attendre au moins 3 cycles** (90 secondes) pour que la mesure se stabilise.
2. **Zoomer** sur une zone plate entre deux pics.

   ```
   Dans Power Profiler :
   - Sélectionner une zone plate entre deux pics (glisser la souris)
   - Lire la valeur moyenne (Average)
   ```

3. **Noter dans le CSV :**

   | Mesure | Où la trouver | Valeur |
   |--------|--------------|--------|
   | Deep sleep (µA) | Moyenne zone plate | _____ µA |
   | Pic réveil (mA) | Maximum d'un pic | _____ mA |
   | Durée pic actif (s) | Largeur du pic | _____ s |

### 3.4 Interprétation — Grille de décision

| Mesure | ✅ GO | 🟠 Orange | ❌ NO-GO |
|--------|:-----:|:---------:|:--------:|
| Deep sleep DevKit | < 100 µA | 100-150 µA | > 200 µA |
| Pic réveil | < 80 mA | 80-120 mA | > 150 mA |
| Stabilité | Pics réguliers | 1-2 sauts | Aucun pic |

> ⚠️ **IMPORTANT — Overhead du DevKit :** Le DevKit a un régulateur AMS1117 et des LEDs qui consomment en permanence. Un deep sleep à 120-150 µA sur DevKit **ne condamne pas** l'ESP32-S3. Le PCB final (sans régulateur superflu) consommera moins. Si mesure entre 100 et 150 µA → noter **ORANGE** et documenter. On retestera sur PCB nu.

---

## Étape 4 — Arrêt propre (2 minutes)

1. Dans Power Profiler, **désactiver la sortie PPK2** (Output OFF).
2. **Débrancher d'abord le fil rouge (VOUT)**, puis le fil noir (GND).
3. Cliquer **Stop** dans Power Profiler.
4. **Sauvegarder la session** Power Profiler : File → Save → `2026-06-XX_phaseC_deep_sleep.ppk2`

---

## Clôture de la Phase C

### Checklist

- [ ] PPK2 reconnu dans Power Profiler
- [ ] Mode Source Meter, 5.0 V configuré
- [ ] Branchement vérifié deux fois (polarité, pas d'USB)
- [ ] Pics de réveil toutes les ~30 secondes observés
- [ ] Mesures notées dans le CSV
- [ ] Session Power Profiler sauvegardée
- [ ] Sortie PPK2 OFF, fils débranchés

### CSV

| Date | Test | Firmware | Tension | Mode PPK2 | Deep sleep | Pic boot | Courant actif | Durée active | Résultat |
|------|------|----------|---------|-----------|-----------|---------|-------------|------------|----------|
| YYYY-MM-DD | Phase C — deep sleep PPK2 | wn_deep_sleep_30s | 5.0 V | Source Meter | __ µA | __ mA | __ mA | __ s | GO / ORANGE / NO-GO |

---

## Dépannage Phase C

| Symptôme | Cause probable | Solution |
|----------|---------------|----------|
| Courant = 0 mA, pas de pic | Mauvais branchement | Vérifier VOUT→5V, GND→GND. Vérifier que sortie PPK2 est ON |
| Courant > 20 mA constant | Firmware pas en deep sleep | Reflasher `wn_deep_sleep_30s` via USB, puis rebrancher PPK2 |
| Pics irréguliers ou absents | Timer RTC instable | Mettre à jour le package ESP32 dans Boards Manager |
| PPK2 non reconnu | Câble USB ou driver | Changer de câble, changer de port Mac, redémarrer Power Profiler |
| "Current limit exceeded" | Court-circuit ou branchement inversé | **COUPER IMMÉDIATEMENT LA SORTIE.** Vérifier tout le câblage |

---

**Fin de SOP-03. Prochaine étape : SOP-04 Phase D — Réveil court 20 cycles.**
