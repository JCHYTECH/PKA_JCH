# SOP-06 — Phase F : Test microSD SPI

**SOP :** SOP-06  
**Projet :** WildNexus P0 — M-02 Prototype banc fonctionnel  
**Phase :** F — Test module microSD SPI  
**Durée :** ~25 minutes  
**Prérequis :** SOP-05 réussi, module microSD SPI 3.3V + carte microSD FAT32 disponibles  
**Auteur :** [[Dobby]]  
**Date :** 2026-06-12  
**Version :** 1.0  

---

## Objectif

Vérifier que le module microSD fonctionne avec l'ESP32-S3 : initialisation, écriture d'un fichier test, retour au deep sleep. Mesurer la consommation de l'écriture SD.

---

## Matériel spécifique à cette phase

| # | Élément |
|---|---------|
| 1 | Module microSD SPI 3.3V |
| 2 | Carte microSD 8-32 Go |
| 3 | Adaptateur microSD→USB ou lecteur SD pour Mac |
| 4 | 6 câbles Dupont femelle-femelle |

---

## Étape 0 — Préparer la carte microSD (3 minutes)

1. Insérer la microSD dans l'adaptateur USB.
2. Brancher l'adaptateur au Mac.
3. Ouvrir **Utilitaire de disque** (Disk Utility).
4. Sélectionner la carte microSD (pas le Mac !).
5. Cliquer **Effacer** :
   - Format : **MS-DOS (FAT32)**
   - Schéma : **Master Boot Record** (MBR)
   - Nom : `WILDNEXUS`
6. Cliquer **Effacer**, attendre la fin.
7. Éjecter proprement (clic droit → Éjecter).
8. Insérer la microSD dans le module microSD.

---

## Étape 1 — Firmware `wn_sd_test` (3 minutes)

```cpp
// SOP-06 — wn_sd_test
// WildNexus P0 — Phase F — Test microSD SPI
// Initialise la SD, écrit un fichier, puis deep sleep 30s.

#include "FS.h"
#include "SD.h"
#include "SPI.h"
#include "esp_sleep.h"

// Pinout microSD → ESP32-S3
#define SD_CS   10
#define SD_MOSI 11
#define SD_SCK  12
#define SD_MISO 13

RTC_DATA_ATTR int cycle = 0;

void setup() {
  Serial.begin(115200);
  delay(500);
  cycle++;

  Serial.printf("=== SD TEST #%d ===\n", cycle);

  // Initialiser le bus SPI avec les broches spécifiques
  SPI.begin(SD_SCK, SD_MISO, SD_MOSI, SD_CS);

  if (!SD.begin(SD_CS, SPI)) {
    Serial.println("❌ SD INIT FAILED — check wiring");
  } else {
    Serial.println("✅ SD init OK");

    // Écrire un fichier test
    File f = SD.open("/wn_test.txt", FILE_APPEND);
    if (f) {
      f.printf("Cycle %d — WildNexus SD write OK\n", cycle);
      f.close();
      Serial.println("✅ SD write OK");

      // Vérifier que le fichier existe
      if (SD.exists("/wn_test.txt")) {
        File r = SD.open("/wn_test.txt", FILE_READ);
        if (r) {
          Serial.print("📄 Content: ");
          while (r.available()) Serial.write(r.read());
          r.close();
        }
      }
    } else {
      Serial.println("❌ SD write FAILED");
    }
    SD.end();
  }

  Serial.flush();
  esp_sleep_enable_timer_wakeup(30ULL * 1000000ULL);
  esp_deep_sleep_start();
}

void loop() {}
```

---

## Étape 2 — Branchement (5 minutes)

### ⚠️ Vérifier la tension du module

→ Votre module microSD doit être **3.3V compatible**. Si le module a un régulateur 5V→3.3V intégré, brancher sur **5V** de l'ESP32. Sinon, brancher sur **3V3**.

| Module microSD | ESP32-S3 | Couleur fil suggéré |
|---------------|----------|---------------------|
| VCC | **3V3** (ou 5V si régulateur intégré) | Rouge |
| GND | GND | Noir |
| SCK (CLK) | GPIO 12 | Jaune |
| MISO (DO) | GPIO 13 | Bleu |
| MOSI (DI) | GPIO 11 | Vert |
| CS (SS) | GPIO 10 | Orange |

```
        ESP32-S3 DevKit              Module microSD
        ┌──────────────┐             ┌──────────┐
        │              │             │          │
        │  3V3 ────────┼──[rouge]────┼── VCC    │
        │  GND ────────┼──[noir]─────┼── GND    │
        │  IO12 ───────┼──[jaune]────┼── SCK    │
        │  IO13 ───────┼──[bleu]─────┼── MISO   │
        │  IO11 ───────┼──[vert]─────┼── MOSI   │
        │  IO10 ───────┼──[orange]───┼── CS     │
        └──────────────┘             └──────────┘
```

**Ordre de branchement :** GND d'abord, puis VCC, puis les signaux.

> ⚠️ **Vérifier que VCC n'est PAS sur 5V sauf si le module a un régulateur.** La plupart des modules microSD « pour Arduino » ont un régulateur LDO 3.3V intégré et acceptent 5V. En cas de doute : brancher sur 3V3.

---

## Étape 3 — Test sans PPK2 (5 minutes)

1. ESP32 branché en USB (pas de PPK2 pour l'instant).
2. Brancher le module microSD comme ci-dessus.
3. Flasher `wn_sd_test`.
4. Moniteur série 115200 baud.
5. Observer :

```
=== SD TEST #1 ===
✅ SD init OK
✅ SD write OK
📄 Content: Cycle 1 — WildNexus SD write OK
```

> ✅ Si ce message apparaît → SD fonctionnelle.

> ❌ `SD INIT FAILED` :
> - Vérifier le câblage (CS=10, MOSI=11, SCK=12, MISO=13)
> - Vérifier que la microSD est bien insérée
> - Vérifier que la carte est formatée FAT32
> - Essayer un autre module ou une autre carte SD

> ❌ `SD write FAILED` mais init OK :
> - La carte est peut-être en lecture seule (vérifier le petit switch sur l'adaptateur SD)
> - ou formatée en exFAT au lieu de FAT32

### 3.1 Vérifier le fichier sur Mac

1. Après 2-3 cycles, débrancher l'USB.
2. Retirer la microSD du module.
3. Insérer dans l'adaptateur USB, brancher au Mac.
4. Ouvrir la carte `WILDNEXUS`.
5. Le fichier `wn_test.txt` doit être présent avec plusieurs lignes.

---

## Étape 4 — Mesure PPK2 (10 minutes)

1. Débrancher l'USB de l'ESP32.
2. PPK2 OFF → brancher VOUT→5V, GND→GND de l'ESP32.
3. **Le module microSD reste branché à l'ESP32** (3V3 ou 5V, GND, SPI).
4. Source Meter 5.0V, acquisition, sortie ON.
5. Observer la courbe :

```
Courant
  │
  │  ┌────────────────┐
  │  │ init SD + write│
  │  │ ~50-100 mA     │
  │──┘                └──────────────────────────┐
  │                                              │
  │  ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔  ← sleep   │
  └──────────────────────────────────────────────────→
```

### Mesures à noter

| Mesure | Valeur |
|--------|--------|
| Courant pic init SD + write (mA) | _____ mA |
| Durée active (s) | _____ s |
| Charge cycle SD (mAh) | _____ mAh |
| Deep sleep avec module SD branché (µA) | _____ µA |
| ⚠️ Le module SD consomme-t-il en veille ? | Oui / Non |

> ⚠️ **POINT CRITIQUE :** Certains modules microSD consomment en continu même quand l'ESP32 dort. Si le deep sleep dépasse 200 µA avec le module branché, le module SD consomme en veille → documenter. Il faudra un MOSFET de power gating sur le rail SD dans le PCB final.

---

## Grille de décision

| Critère | ✅ GO | 🟠 Orange | ❌ NO-GO |
|---------|:-----:|:---------:|:--------:|
| Init SD | OK | 1-2 retries | Échec systématique |
| Écriture 1 cycle | OK | Erreurs sporadiques | Fichier absent |
| Deep sleep avec SD | < 150 µA | 150-300 µA | > 300 µA (module fuit) |

---

## Clôture

### Checklist

- [ ] Carte microSD formatée FAT32
- [ ] Module branché (3V3, GND, SCK, MISO, MOSI, CS)
- [ ] `wn_sd_test` flashé et init OK
- [ ] Fichier `wn_test.txt` vérifié sur Mac
- [ ] Mesure PPK2 : pic écriture + deep sleep SD branché
- [ ] Conso veille module SD documentée

---

**Fin de SOP-06. Prochaine étape : SOP-07 Phase G — Test LoRa.**
