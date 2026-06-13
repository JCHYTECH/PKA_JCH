# SOP-01 — Phase A : Vérification ESP32-S3 alive

**SOP :** SOP-01  
**Projet :** WildNexus P0 — M-02 Prototype banc fonctionnel  
**Phase :** A — Vérification ESP32-S3 fonctionnel  
**Durée :** ~10 minutes  
**Prérequis :** Aucun (première manipulation)  
**Auteur :** [[Dobby]]  
**Date :** 2026-06-12  
**Version :** 1.0  

---

## Objectif

Vérifier que l'ESP32-S3 DevKit fonctionne, communique avec le Mac, et exécute un programme simple, **avant** toute manipulation de mesure ou de périphériques.

Si cette étape échoue, inutile de continuer. L'ESP32-S3 doit d'abord prouver qu'il est vivant.

---

## Matériel nécessaire

| # | Élément | Photo / Description |
|---|---------|---------------------|
| 1 | **ESP32-S3 DevKitC-1-N8R8** | Carte verte ~7×2.5 cm. Deux ports USB-C (un marqué "UART", l'autre "USB"). Broches noires en double rangée de chaque côté. |
| 2 | **Câble USB-C data** | Câble qui transfère les données, pas seulement l'alimentation. Le câble fourni avec le DevKit est data. |
| 3 | **Mac** avec Arduino IDE installé | Si pas encore installé → voir Annexe A |

---

## Préparation du poste (1 minute)

### Étape 0.1 — Dégager la surface de travail

```
┌─────────────────────────────────────┐
│                                     │
│         SURFACE DE TRAVAIL          │
│         (table non conductrice)     │
│                                     │
│   [Mac]          [ESP32-S3]         │
│                                     │
└─────────────────────────────────────┘
```

1. Poser le Mac sur la gauche.
2. Poser l'ESP32-S3 sur la droite, **broches vers le haut** (la face avec les composants visibles).
3. Rien d'autre sur la table. Pas de métal, pas de liquide.
4. **Le PPK2 n'est PAS branché.** On n'en a pas besoin pour cette phase.

> ⚠️ L'ESP32-S3 se pose sur ses broches. Les broches sont traversantes — elles ne doivent toucher aucun objet métallique.

---

## Étape 1 — Branchement (30 secondes)

### 1.1 Identifier le bon port USB-C

L'ESP32-S3 DevKit a **deux ports USB-C** :

```
        ┌──────────────────┐
        │   ESP32-S3       │
        │   DevKitC-1      │
        │                  │
  USB ──┤ □  UART          │
        │                  │
 UART ──┤ □  USB           │
        └──────────────────┘
```

- **Port "UART"** (à gauche sur la carte, marqué `UART`) → Celui qu'on utilise. Il contient le convertisseur USB-série intégré.
- **Port "USB"** (à droite, marqué `USB`) → USB OTG natif de l'ESP32-S3. On ne l'utilise pas pour le flashage.

**Brancher le câble USB-C sur le port marqué "UART".**

### 1.2 Brancher au Mac

1. Prendre l'autre extrémité du câble USB-C.
2. La brancher sur un port USB-C du Mac.
3. Une LED rouge doit s'allumer sur l'ESP32-S3 DevKit.

> ✅ **VÉRIFICATION : LED rouge allumée = la carte est alimentée.**
>
> Si la LED reste éteinte : changer de câble, changer de port Mac, ou vérifier que le câble est bien enfoncé.

---

## Étape 2 — Arduino IDE : sélection de la carte (2 minutes)

### 2.1 Ouvrir Arduino IDE

1. Lancer Arduino IDE depuis le Dock ou le dossier Applications.
2. Si c'est la première utilisation, l'assistant de bienvenue s'affiche. Le fermer.

### 2.2 Installer le support ESP32 (une seule fois)

Si le package ESP32 n'est **pas encore installé** :

1. Aller dans **Arduino IDE → Settings** (ou Preferences sur anciennes versions).
2. Dans le champ **Additional Boards Manager URLs**, ajouter cette ligne (si elle n'y est pas déjà) :

   ```
   https://espressif.github.io/arduino-esp32/package_esp32_index.json
   ```

3. Cliquer **OK**.
4. Aller dans **Tools → Board → Boards Manager**.
5. Taper `ESP32` dans la barre de recherche.
6. Installer **esp32 by Espressif Systems** (la dernière version).
7. Fermer le Boards Manager.

### 2.3 Sélectionner la carte

1. Aller dans **Tools → Board → ESP32 Arduino**.
2. Sélectionner **ESP32S3 Dev Module**.

   > Si "ESP32S3 Dev Module" n'apparaît pas, sélectionner **ESP32-S3-DevKitC-1-N8R8** ou l'entrée la plus proche.

### 2.4 Configurer les paramètres de la carte

Dans **Tools**, vérifier ces réglages :

| Paramètre | Valeur |
|-----------|--------|
| USB CDC On Boot | **Enabled** |
| USB Mode | **Hardware CDC and JTAG** |
| PSRAM | **OPI PSRAM** |
| Flash Size | **8MB (64Mb)** |
| Partition Scheme | **Default 4MB with spiffs** |
| Upload Speed | **921600** |

> Si un paramètre n'apparaît pas, ce n'est pas grave. Les deux essentiels sont **USB CDC On Boot = Enabled** et **PSRAM = OPI PSRAM**.

---

## Étape 3 — Premier flash : `wn_blink` (5 minutes)

### 3.1 Créer un nouveau sketch

1. Dans Arduino IDE : **File → New**.
2. Effacer tout le contenu par défaut.
3. Copier-coller exactement ce code :

```cpp
// SOP-01 — wn_blink
// WildNexus P0 — Phase A — Vérification ESP32-S3 alive
// Flasher ce programme pour confirmer que l'ESP32-S3 fonctionne.

void setup() {
  Serial.begin(115200);
  delay(500);
}

void loop() {
  Serial.println("WildNexus ESP32-S3 alive");
  delay(1000);
}
```

4. **File → Save As** → nommer `wn_blink` → sauvegarder.

### 3.2 Vérifier le port série

1. Aller dans **Tools → Port**.
2. Un port doit apparaître avec un nom comme :
   - `/dev/cu.usbmodemXXXX` (Mac)
   - `SLAB_USBtoUART`
   - Quelque chose contenant `ESP32` ou `USB`

   > Si **aucun port n'apparaît** → Annexe B : Dépannage port série.

3. Sélectionner ce port.

### 3.3 Flasher

1. Cliquer sur le bouton **Upload** (flèche vers la droite, en haut à gauche).
2. Observer la console en bas de l'IDE Arduino.

**Ce que vous devez voir dans la console :**

```
Compiling sketch...
...
Linking...
...
Writing at 0x00000000... (X %)
Writing at 0x00010000... (X %)
...
Hard resetting via RTS pin...
```

3. Attendre que la barre de progression atteigne 100% et que le message `Hard resetting via RTS pin...` apparaisse.

> ❌ **ERREUR : "Failed to connect to ESP32-S3"**
>
> → Maintenir le bouton **BOOT** (le plus à gauche, marqué `BOOT` ou `0`) enfoncé.
> → Cliquer Upload dans l'IDE.
> → Relâcher BOOT quand la console affiche `Connecting...`.
>
> Si ça échoue encore :
> → Débrancher et rebrancher le câble USB-C.
> → Réessayer l'upload.

> ❌ **ERREUR : "A fatal error occurred: Timed out waiting for packet header"**
>
> → Le port série n'est pas le bon. Vérifier **Tools → Port**.
> → Essayer un autre port si plusieurs apparaissent.

---

## Étape 4 — Vérification moniteur série (2 minutes)

### 4.1 Ouvrir le moniteur série

1. Cliquer sur l'icône **Serial Monitor** (loupe en haut à droite).
2. **Ou** aller dans **Tools → Serial Monitor**.

### 4.2 Régler la vitesse

En bas à droite du moniteur série, vérifier que la vitesse est **115200 baud**.

```
┌─ Serial Monitor ──────────────────────────────┐
│                                                │
│ WildNexus ESP32-S3 alive                       │
│ WildNexus ESP32-S3 alive                       │
│ WildNexus ESP32-S3 alive                       │
│                                                │
├────────────────────────────────────────────────┤
│ [Autoscroll ✓]  [Show timestamp]  [115200 baud ▼] │
└────────────────────────────────────────────────┘
```

### 4.3 Ce que vous devez voir

Le message **"WildNexus ESP32-S3 alive"** doit apparaître une fois par seconde, en continu.

> ✅ **GO — Phase A réussie.**
>
> L'ESP32-S3 est vivant. Il compile, il flashe, il communique.

> ❌ **Si rien n'apparaît :**
>
> 1. Vérifier que la vitesse est bien 115200.
> 2. Vérifier que le bon port est sélectionné.
> 3. Appuyer sur le bouton **EN** (Reset) de l'ESP32-S3 — le message doit réapparaître.
> 4. Si toujours rien, refaire l'Étape 3.3 (Upload).

> ❌ **Si des caractères illisibles apparaissent (`` `?⸮⸮ ``) :**
>
> → La vitesse du moniteur série n'est pas 115200. La régler.

---

## Clôture de la Phase A

### Ce que vous avez accompli

- [x] L'ESP32-S3 est alimenté et reconnu par le Mac
- [x] Arduino IDE détecte la carte et le port série
- [x] Le firmware `wn_blink` compile et flashe sans erreur
- [x] Le moniteur série affiche le message alive en continu

### Avant de passer à la Phase B

1. **Fermer le moniteur série.**
2. **NE PAS débrancher l'ESP32** si vous enchaînez sur la Phase B.
3. Noter dans le CSV de mesures :

| Date | Test | Firmware | Résultat |
|------|------|----------|----------|
| YYYY-MM-DD | Phase A — alive check | wn_blink | ✅ GO |

---

## Schéma récapitulatif

```
MacBook                    ESP32-S3 DevKit
┌──────────┐               ┌──────────────┐
│          │   USB-C data  │              │
│  USB-C ──┼───────────────┼── UART (gauche)│
│          │               │              │
│          │               │  [LED rouge] │ ← allumée = alimenté
│          │               │              │
│ Arduino  │               │  BOOT  EN    │ ← boutons
│ IDE      │               │  [□□]  [□□]  │
└──────────┘               └──────────────┘

Moniteur série : "WildNexus ESP32-S3 alive" × 1/sec
Vitesse : 115200 baud
```

---

## Annexes

### Annexe A — Installer Arduino IDE (5 minutes, une seule fois)

1. Aller sur https://www.arduino.cc/en/software
2. Télécharger la version pour macOS (Apple Silicon si Mac M1/M2/M3/M5).
3. Ouvrir le `.dmg` et glisser Arduino IDE dans Applications.
4. Lancer Arduino IDE.
5. Suivre l'Étape 2.2 pour installer le support ESP32.

### Annexe B — Dépannage port série

| Symptôme | Cause probable | Solution |
|----------|---------------|----------|
| Aucun port n'apparaît dans Tools → Port | Câble non-data (charge seule) | Essayer un autre câble USB-C |
| Port apparaît/disparaît | Mauvais contact | Nettoyer le port USB-C de l'ESP32, changer de câble |
| Port nommé `Bluetooth-Incoming-Port` | Mauvais port sélectionné | Choisir le port avec `usbmodem` ou `SLAB` |
| Plusieurs ports apparaissent | Normal, le Mac a plusieurs ports | Débrancher/rebrancher : le nouveau port est le bon |

### Annexe C — Photo des boutons de l'ESP32-S3 DevKitC-1

```
Vue de dessus — ESP32-S3 DevKitC-1

    ┌─────────────────────────────────┐
    │  ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ │ ← broches (rangée du haut)
    │                                 │
    │  [BOOT] [EN]  ┌──────┐         │
    │   □      □    │ESP32-│         │ ← puce principale
    │               │ S3   │         │
    │               └──────┘         │
    │                    □ UART      │ ← port USB-C "UART"
    │  LED rouge          □ USB      │ ← port USB-C "USB"
    │  (alimentation)                 │
    │  ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ ○ │ ← broches (rangée du bas)
    └─────────────────────────────────┘

BOOT = bouton le plus à gauche (parfois marqué "0")
EN   = bouton Reset
UART = port USB-C de programmation (côté gauche de la carte)
USB  = port USB-C OTG (côté droit) — NE PAS UTILISER pour le flashage
```

---

**Fin de la SOP-01. Prochaine étape : SOP-02 Phase B — Deep sleep 30 secondes.**
