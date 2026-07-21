# SOP-06 — Phase F : Test microSD SPI

**SOP :** SOP-06  
**Projet :** WildNexus P0 — M-02 Prototype banc fonctionnel  
**Phase :** F — Test module microSD SPI  
**Durée :** ~25 minutes  
**Prérequis :** SOP-05 réussi, module microSD SPI 3.3V + carte microSD 128 GB FAT32  
**Auteur :** [[Dobby]]  
**Date :** 2026-06-12  
**Version :** 2.0 — 2026-07-05 : pinout corrigé (SPI3), carte 128 GB (ADR-017), structure DCIM+AUDIO  

---

## Objectif

Vérifier que le module microSD fonctionne avec l'ESP32-S3 : initialisation, écriture de fichiers test dans la structure `DCIM/` et `AUDIO/`, retour au deep sleep. Mesurer la consommation de l'écriture SD.

> ⚠️ **Config de test :** Config B (Radio) ou C (Audio). **Caméra DÉCONNECTÉE** — les GPIO 4-11 sont libérés.

---

## Matériel spécifique

| # | Élément |
|---|---------|
| 1 | Module microSD SPI 3.3V |
| 2 | **Carte microSD 128 GB** (ADR-017 §6 — minimum requis pour P0→P1) |
| 3 | Adaptateur microSD→USB ou lecteur SD pour Mac |
| 4 | 6 câbles Dupont femelle-femelle |

---

## Pinout (wn_config.h — SPI3_HOST)

| Signal | ESP32-S3 GPIO | Couleur fil suggéré |
|--------|:------------:|:-------------------:|
| VCC | **3V3** (ou 5V si régulateur intégré) | Rouge |
| GND | GND | Noir |
| SCK (CLK) | **GPIO 40** | Jaune |
| MISO (DO) | **GPIO 41** | Bleu |
| MOSI (DI) | **GPIO 42** | Vert |
| CS (SS) | **GPIO 39** | Orange |

> ⚠️ **SPI3 est indépendant de SPI2 (LoRa).** Les deux bus ne partagent pas de pins. SD et LoRa peuvent être connectés simultanément (Config B/D).

> ⚠️ **Ancien pinout (v1.0) :** SCK=12, MISO=13, MOSI=11, CS=10. **Obsolète.** Ces pins appartiennent maintenant à SPI2 (LoRa) et à la caméra DVP. Utiliser le pinout ci-dessus.

```
        ESP32-S3 DevKit              Module microSD
        ┌──────────────┐             ┌──────────┐
        │  3V3 ────────┼──[rouge]────┼── VCC    │
        │  GND ────────┼──[noir]─────┼── GND    │
        │  IO40 ───────┼──[jaune]────┼── SCK    │
        │  IO41 ───────┼──[bleu]─────┼── MISO   │
        │  IO42 ───────┼──[vert]─────┼── MOSI   │
        │  IO39 ───────┼──[orange]───┼── CS     │
        └──────────────┘             └──────────┘
```

---

## Étape 0 — Préparer la carte microSD (3 minutes)

1. Insérer la microSD 128 GB dans l'adaptateur USB.
2. Brancher l'adaptateur au Mac.
3. Ouvrir **Utilitaire de disque** (Disk Utility).
4. Sélectionner la carte microSD (pas le Mac !).
5. Cliquer **Effacer** :
   - Format : **MS-DOS (FAT32)** (⚠️ FAT32 max partition = 32 GB sur Mac. Pour 128 GB complet, utiliser `diskutil` en ligne de commande ou exFAT)
   - Schéma : **Master Boot Record** (MBR)
   - Nom : `WILDNEXUS`
6. Cliquer **Effacer**, attendre la fin.
7. Éjecter proprement.

> 💡 **Formatage 128 GB en FAT32 :** Disk Utility limite FAT32 à 32 GB. Pour formater 128 GB en FAT32, utiliser en terminal :
> ```bash
> diskutil eraseDisk MS-DOS FAT32 WILDNEXUS MBR /dev/diskN
> ```
> (Remplacer `diskN` par le numéro de disque de la carte — vérifier avec `diskutil list` d'abord.)

---

## Étape 1 — Firmware `wn_sd_test` (5 minutes)

Le firmware teste l'init SD + écriture dans la structure ADR-017 :
- `DCIM/` — répertoire images caméra
- `AUDIO/` — répertoire clips WAV + features spectrales

```cpp
// SOP-06 — wn_sd_test v2
// WildNexus P0 — Phase F — Test microSD SPI3 + structure ADR-017
#include "FS.h"
#include "SD.h"
#include "SPI.h"
#include "esp_sleep.h"

// Pinout SPI3 (wn_config.h)
#define SD_CS   39
#define SD_MOSI 42
#define SD_SCK  40
#define SD_MISO 41

RTC_DATA_ATTR int cycle = 0;

void setup() {
  Serial.begin(115200);
  delay(500);
  cycle++;
  Serial.printf("=== SD TEST #%d ===\n", cycle);

  SPI.begin(SD_SCK, SD_MISO, SD_MOSI, SD_CS);
  if (!SD.begin(SD_CS, SPI)) {
    Serial.println("❌ SD INIT FAILED");
  } else {
    Serial.println("✅ SD init OK");
    
    // Créer la structure de répertoires (ADR-017 §5)
    SD.mkdir("/DCIM");
    SD.mkdir("/AUDIO");
    Serial.println("✅ DCIM/ + AUDIO/ créés");

    // Test écriture DCIM
    File f = SD.open("/DCIM/wn_test.txt", FILE_APPEND);
    if (f) {
      f.printf("Cycle %d — DCIM write OK\n", cycle);
      f.close();
      Serial.println("✅ DCIM write OK");
    }

    // Test écriture AUDIO
    f = SD.open("/AUDIO/wn_audio_test.txt", FILE_APPEND);
    if (f) {
      f.printf("Cycle %d — AUDIO write OK\n", cycle);
      f.close();
      Serial.println("✅ AUDIO write OK");
    }

    // Lister les fichiers
    File root = SD.open("/");
    Serial.println("📁 Root:");
    while (root) {
      File entry = root.openNextFile();
      if (!entry) break;
      Serial.printf("  %s%s\n", entry.isDirectory() ? "[" : "  ", entry.name());
      entry.close();
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

**Ordre de branchement :** GND d'abord, puis VCC, puis les signaux.

> ⚠️ Vérifier que VCC n'est PAS sur 5V sauf si le module a un régulateur. En cas de doute : 3V3.

---

## Étape 3 — Test sans PPK2 (5 minutes)

1. ESP32 branché en USB.
2. Flasher `wn_sd_test`.
3. Moniteur série 115200 baud.
4. Observer :

```
=== SD TEST #1 ===
✅ SD init OK
✅ DCIM/ + AUDIO/ créés
✅ DCIM write OK
✅ AUDIO write OK
📁 Root:
  [DCIM]
  [AUDIO]
```

> ❌ `SD INIT FAILED` : vérifier câblage (CS=39, MOSI=42, SCK=40, MISO=41), carte insérée, format FAT32.

---

## Étape 4 — Mesure PPK2 (10 minutes)

| Mesure | Valeur attendue |
|--------|-----------------|
| Courant pic init SD + write | 50-100 mA |
| Durée active | ~2-3 s |
| Deep sleep avec module SD branché | < 150 µA idéal |

> ⚠️ Si deep sleep > 300 µA avec module SD branché → power gating MOSFET nécessaire sur PCB final.

---

## Grille de décision

| Critère | ✅ GO | 🟠 Orange | ❌ NO-GO |
|---------|:-----:|:---------:|:--------:|
| Init SD | OK | 1-2 retries | Échec systématique |
| Structure DCIM + AUDIO | Créée | — | Absente |
| Écriture DCIM + AUDIO | OK | Erreurs sporadiques | Fichier absent |
| Deep sleep avec SD | < 150 µA | 150-300 µA | > 300 µA (fuite module) |

---

**Fin de SOP-06 v2.0. Prochaine étape : SOP-07 Phase G — Test LoRa.**
