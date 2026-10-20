# 🌳 Arbor H1 — Protocole de test (mode « dummy-proof »)

> **Nœud Arbor :** 1 — GPIO zero-leakage + PSRAM power-down  
> **Hypothèse :** Le firmware optimisé réduit la conso deep sleep de > 15% (de 1052 µA vers < 900 µA)  
> **Firmware :** `wn_deep_sleep_30s_arbor_h1.ino` (dans `06_COMPONENTS/PPK2/firmware/`)  
> **Temps total :** ~30 minutes | **Difficulté :** ⭐☆☆☆☆ (débutant)

---

## 📦 Ce dont tu as besoin

| # | Élément | Où le trouver |
|---|---------|---------------|
| 1 | ESP32-S3 DevKitC-1 | Sur le banc (boîte blanche "ESP32-S3-DevKitC-1-N8R8") |
| 2 | Nordic PPK2 | Sur le banc (boîte noire "Nordic PPK2") |
| 3 | Câble USB-C → USB (pour l'ESP32) | Sur le banc |
| 4 | Câble micro-USB → USB (pour le PPK2) | Dans la boîte PPK2 |
| 5 | 2 câbles Dupont femelle-femelle (1 rouge, 1 noir) | Kit breadboard Miuzei |
| 6 | Mac avec Arduino IDE installé | Ton Mac M5 |
| 7 | nRF Connect + Power Profiler installé | Ton Mac M5 (si pas installé → voir Annexe A) |

---

## ⚠️ RÈGLES DE SÉCURITÉ — À LIRE AVANT DE COMMENCER

> **Ces règles ne sont PAS optionnelles. Une erreur = matériel détruit.**

| # | Règle | Pourquoi |
|---|-------|----------|
| 🔴 1 | **Jamais USB + PPK2 branchés en même temps sur l'ESP32** | Double alimentation = destruction |
| 🔴 2 | **Sortie PPK2 toujours OFF avant de brancher/débrancher** | Court-circuit au branchement |
| 🔴 3 | **Fil rouge = PPK2 VOUT → ESP32 5V | Fil noir = PPK2 GND → ESP32 GND** | Inversion = destruction |
| 🔴 4 | **Si la carte chauffe → débrancher immédiatement** | Court-circuit |
| 🔴 5 | **Si courant > 500 mA → couper la sortie PPK2** | Anormal |

---

## Étape 1 — Flasher le firmware optimisé (5 minutes)

### 1.1 Ouvrir le firmware

1. Ouvre **Arduino IDE** sur ton Mac.
2. **File → Open**.
3. Navigue vers : `PKA_JCH/JCH_Inbox/03_PROJECTS/03_WILDNEXUS/06_COMPONENTS/PPK2/firmware/`
4. Ouvre `wn_deep_sleep_30s_arbor_h1.ino`.

> ✅ **VÉRIFICATION :** Tu vois un code qui commence par `// SOP-03-H1 — wn_deep_sleep_30s_arbor_h1`

### 1.2 Configurer Arduino IDE

1. En haut de la fenêtre, clique sur le menu déroulant des cartes.
2. Sélectionne **"ESP32-S3 Dev Module"** (ou "ESP32S3 Dev Module").
3. **Tools → USB CDC On Boot** → **Enabled** (pour voir les messages série après le flash).
4. **Tools → PSRAM** → **OPI PSRAM** (si l'option existe — le DevKit N8R8 a 8MB de PSRAM octo).

### 1.3 Brancher et flasher

1. **Vérifie que le PPK2 est DÉBRANCHÉ de l'ESP32.**
2. Branche le câble **USB-C** entre le Mac et l'ESP32-S3 (port USB-C sur le DevKit).
3. Dans Arduino IDE, sélectionne le port série (ex: `/dev/cu.usbmodemXXXX`).
4. Clique sur **Upload** (flèche →).

> Ce que tu dois voir :
> ```
> Compiling sketch...
> Uploading...
> Writing at 0x00000000... (100%)
> Leaving... Hard resetting via RTS pin...
> ```

### 1.4 Vérifier que ça marche

1. **Tools → Serial Monitor** (ou l'icône loupe en haut à droite).
2. Règle le baud rate à **115200** (menu déroulant en bas à droite).
3. Appuie sur le bouton **RESET** de l'ESP32 (petit bouton à côté du port USB-C).

> ✅ **VÉRIFICATION :** Tu dois voir apparaître dans le moniteur série :
> ```
> === WildNexus Arbor H1 : GPIO + PSRAM + RTC power-down ===
> Configuration des GPIOs inutilises en INPUT_PULLDOWN...
>   GPIOs configures : XX
> Power-down des domaines RTC...
> Desactivation du brownout detector en deep sleep...
> Power-down PSRAM...
> Endormissement 30s...
> ```
> Puis ~30 secondes de silence, puis le message réapparaît.

4. **Débranche le câble USB-C** de l'ESP32. Maintenant.

> ✅ Checklist Étape 1 :
> - [ ] Firmware flashé sans erreur
> - [ ] Message "Arbor H1" visible dans le moniteur série
> - [ ] Cycle de 30 secondes confirmé (message → silence → message)
> - [ ] Câble USB DÉBRANCHÉ de l'ESP32

---

## Étape 2 — Brancher le PPK2 (5 minutes)

### 2.1 Installer Power Profiler (si pas déjà fait — une seule fois)

1. Ouvre **nRF Connect for Desktop** (cherche dans Applications).
2. Si pas installé : [télécharge ici](https://www.nordicsemi.com/Products/Development-tools/nRF-Connect-for-desktop).
3. Dans nRF Connect, trouve l'app **Power Profiler** → **Install** puis **Open**.

### 2.2 Brancher le PPK2 au Mac

1. Prends le câble micro-USB (ou USB-C selon modèle PPK2).
2. Branche côté PPK2, côté Mac.
3. Dans Power Profiler, clique sur **Select Device**.
4. Le PPK2 apparaît (ex: `PPK2 - 000682XXXXXX`) → sélectionne-le.

> ✅ **VÉRIFICATION :** La LED sur le PPK2 s'allume. Power Profiler affiche "Connected".

### 2.3 Configurer le PPK2

Dans Power Profiler, sur le panneau de droite :

1. **Mode** → **Source Meter**.
2. **Voltage** → **5000 mV** (5.0 V).
3. La sortie doit être sur **OFF** (bouton gris/éteint).

> ✅ **VÉRIFICATION :** La sortie est OFF. La courbe est plate à 0.

### 2.4 Brancher le PPK2 à l'ESP32 (ORDRE IMPÉRATIF)

```
PPK2                           ESP32-S3 DevKit
┌──────────┐                   ┌──────────────┐
│          │                   │              │
│  VOUT ───┼───[fil rouge]─────┼── 5V         │
│  GND  ───┼───[fil noir]──────┼── GND        │
│          │                   │              │
└──────────┘                   └──────────────┘
```

1. **D'abord le fil noir :** branche entre PPK2 **GND** et ESP32 **GND**.
2. **Ensuite le fil rouge :** branche entre PPK2 **VOUT** et ESP32 **5V**.
3. Vérifie que les broches ne se touchent PAS entre elles.
4. Vérifie que le câble USB est **toujours DÉBRANCHÉ** de l'ESP32.

> 🔍 **DOUBLE CHECK :** Suis chaque fil du doigt. PPK2 VOUT → ESP32 5V. PPK2 GND → ESP32 GND. C'est tout.

> ✅ Checklist Étape 2 :
> - [ ] PPK2 reconnu dans Power Profiler
> - [ ] Mode Source Meter, 5.0V, sortie OFF
> - [ ] Fil noir : PPK2 GND → ESP32 GND
> - [ ] Fil rouge : PPK2 VOUT → ESP32 5V
> - [ ] Rien branché sur l'USB de l'ESP32

---

## Étape 3 — Mesurer (15 minutes)

### 3.1 Démarrer la mesure

1. Dans Power Profiler, clique sur **[[Start]]** (la courbe commence mais aucun courant ne circule encore).
2. Active la sortie : clique sur **Output ON**.

> Ce que tu dois voir immédiatement :
> ```
> Courant
>   │
>   │  ┌─┐                    ┌─┐
>   │  │ │ pic réveil         │ │ pic réveil
>   │  │ │ (~40-80 mA)        │ │
>   │──┘ └────────────────────┘ └──────────────
>   │   ←── 30 secondes ────→
>   │  ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔  ← plateau deep sleep
>   └──────────────────────────────────────────→ Temps
> ```

### 3.2 Ce que tu observes

| Ce que tu vois | Signification | Action |
|----------------|---------------|--------|
| Pics toutes les ~30s | ✅ Cycle normal | Continue |
| Ligne plate entre les pics | ✅ L'ESP32 dort | Mesure le plateau |
| Courant 0 mA en permanence | Mauvais branchement | Vérifie les fils |
| Courant > 20 mA constant | Carte ne dort pas | Vérifie le firmware |
| Pas de pic | Timer non configuré | Re-flashe |

### 3.3 Prendre la mesure

1. **Attends au moins 3 cycles** (~90 secondes) pour que la mesure se stabilise.
2. **Zoom** sur un plateau (zone plate entre deux pics) :
   - Dans Power Profiler, clique et glisse la souris pour sélectionner une zone plate.
   - La sélection devient bleue.
3. **Lis les valeurs** dans le panneau de droite :
   - **Average** = la consommation moyenne du plateau → c'est ton **deep sleep current**
   - Note aussi le **Min** et le **Max**

4. **Répète pour 3 plateaux différents** (pour avoir une moyenne fiable).

> 📝 Note ici :
> ```
> Plateau 1 : Average = _____ µA | Min = _____ | Max = _____
> Plateau 2 : Average = _____ µA | Min = _____ | Max = _____
> Plateau 3 : Average = _____ µA | Min = _____ | Max = _____
> 
> MOYENNE GLOBALE = (P1 + P2 + P3) / 3 = _____ µA
> ```

### 3.4 Sauvegarder

1. Clique **Stop** dans Power Profiler.
2. **File → Save** → nomme le fichier : `2026-06-18_arbor_h1_deep_sleep.ppk2`
3. Sauvegarde dans : `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/06_COMPONENTS/PPK2/`

> ⚠️ **Ne ferme PAS Power Profiler avant d'avoir sauvegardé !**

---

## Étape 4 — Arrêter et rapporter (2 minutes)

### 4.1 Arrêt propre

1. Dans Power Profiler, **Output OFF** (désactive la sortie).
2. **Débranche d'abord le fil rouge** (VOUT), **puis le fil noir** (GND).
3. Tu peux fermer Power Profiler.

### 4.2 Remplir le rapport

Copie-remplis ce bloc et envoie-le à [[Dobby]] :

```
=== ARBOR H1 — RÉSULTAT ===
Date : 2026-06-18
Firmware : wn_deep_sleep_30s_arbor_h1
Tension PPK2 : 5.0V Source Meter

Plateau 1 : average = _____ µA
Plateau 2 : average = _____ µA
Plateau 3 : average = _____ µA
MOYENNE   : _____ µA

Baseline (rappel) : 1052 µA
Delta vs baseline : _____ µA (_____ %)
Seuil merge (15%) : < 894 µA → MERGE, sinon PRUNE

Observations (bruit, stabilité, anomalies) :
_______________________________________________
_______________________________________________

Fichier PPK2 sauvegardé : oui / non
Chemin : JCH_Inbox/03_PROJECTS/03_WILDNEXUS/06_COMPONENTS/PPK2/2026-06-18_arbor_h1_deep_sleep.ppk2
```

---

## 🆘 En cas de problème

| Problème | Cause probable | Solution |
|----------|---------------|----------|
| "ESP32-S3 not found" dans Arduino IDE | Câble USB data manquant | Utilise un câble USB-C DATA (pas charge seule) |
| "Failed to connect" au flash | ESP32 en mauvais mode | Maintiens **BOOT** appuyé, puis **RESET**, relâche **BOOT** |
| Rien dans le moniteur série | USB CDC pas activé | Tools → USB CDC On Boot → Enabled |
| PPK2 pas détecté | Câble ou driver | Débranche/rebranche le PPK2, vérifie le câble |
| Courant = 0 en permanence | Fils mal branchés | Vérifie VOUT→5V, GND→GND, et que la sortie est ON |
| Courant très élevé (>50 mA) | USB branché en même temps | Débranche immédiatement le câble USB de l'ESP32 |
| La carte chauffe | Court-circuit | Débranche TOUT immédiatement |

---

## 📎 Annexe A — Installer nRF Connect + Power Profiler (première fois)

1. Va sur https://www.nordicsemi.com/Products/Development-tools/nRF-Connect-for-desktop
2. Télécharge la version **macOS**.
3. Installe et ouvre.
4. Dans l'application, trouve **Power Profiler** → **Install**.
5. Une fois installé, clique **Open**.
6. Branche le PPK2 → **Select Device** → le PPK2 apparaît.

> C'est tout. Cette étape n'est à faire qu'une seule fois.
