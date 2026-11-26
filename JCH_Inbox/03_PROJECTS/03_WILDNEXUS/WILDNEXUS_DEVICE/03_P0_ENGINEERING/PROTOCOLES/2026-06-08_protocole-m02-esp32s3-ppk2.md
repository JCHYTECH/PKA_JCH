# Protocole M-02 — Tests ESP32-S3 + PPK2

**Date :** 2026-06-08  
**Projet :** [[WildNexus]]  
**Objet :** Mode operatoire complet pour tester le candidat [[ESP32-S3]] du prototype P0 avec Nordic PPK2.  
**Pilotage :** [[Dobby]]  
**Equipe :** [[Araignée]] embarque, [[Forge]] integration, [[Chouette]] manipulation terrain/banc, [[Bruno]] autonomie, [[Castor]] decision systeme, [[Corbeau]] tracabilite.

---

## 1. But du test

Ce protocole doit permettre a une personne non-specialiste de repondre a une question simple :

> L'ESP32-S3 peut-il rester le MCU primaire du prototype P0 WildNexus ?

Le test ne valide pas encore le produit final. Il valide un banc M-02.

### Criteres de decision

| Mesure | Cible | Zone orange | No-go |
|---|---:|---:|---:|
| Deep sleep carte complete | < 100 uA | 100-150 uA | > 150-200 uA irreductible |
| Cycle complet par evenement | < 1.5 mAh | 1.5-2.5 mAh | > 2.5 mAh |
| Autonomie extrapolee a 3 evenements/heure | >= 60 jours | 45-60 jours | < 45 jours |
| Stabilite sleep/wake | 100 cycles OK | 1-2 erreurs | blocage recurrent |

Important : une mauvaise mesure sur DevKit ne condamne pas directement l'ESP32-S3. Le DevKit contient un regulateur, des LEDs et une interface USB-UART qui peuvent consommer plus qu'un PCB final. On mesure donc par paliers.

---

## 2. Materiel necessaire

### Obligatoire pour la premiere session

- 1 x ESP32-S3 DevKitC-1-N8R8.
- 1 x Nordic PPK2.
- 1 x ordinateur Mac.
- 1 x cable USB-C data pour programmer l'ESP32-S3.
- 1 x cable USB pour brancher le PPK2 au Mac.
- Cables Dupont femelle-femelle.
- Carnet ou tableur de mesures.

### Pour les tests etendus

- Module microSD SPI 3.3 V.
- Carte microSD 8-32 Go, formatee FAT32.
- Module camera DVP OV5640 M12 quand disponible.
- Module LoRa SX1262 / RAK3172 quand disponible.
- PIR Panasonic EKMB1303111K quand disponible.
- Buck TPS62840 et alimentation 4S2P AA quand le banc alimentation sera monte.

### Logiciels

- Arduino IDE ou PlatformIO.
- Board package ESP32 Espressif.
- nRF Connect for Desktop.
- App Power Profiler dans nRF Connect.

---

## 3. Vocabulaire minimum

| Mot | Sens pratique |
|---|---|
| DUT | Device Under Test : la carte ESP32-S3 testee |
| PPK2 | Appareil qui alimente et mesure le courant |
| Source Meter | Mode ou le PPK2 alimente l'ESP32 et mesure le courant |
| Ampere Meter | Mode ou le PPK2 mesure le courant d'une alimentation externe |
| Deep sleep | Mode sommeil profond ESP32-S3 |
| Cycle evenement | Reveil -> action -> retour sommeil |

---

## 4. Regles de securite

1. Ne jamais alimenter l'ESP32 par USB et par PPK2 en meme temps pendant une mesure.
2. USB ESP32 = programmation uniquement.
3. PPK2 = alimentation et mesure uniquement.
4. Avant de brancher le PPK2 sur l'ESP32, la sortie PPK2 doit etre sur OFF.
5. Verifier deux fois la polarite : VOUT vers 5V, GND vers GND.
6. Si la carte chauffe, couper immediatement la sortie PPK2.
7. Si le courant depasse 500 mA sans raison pendant un test simple, couper et verifier le cablage.
8. Ne jamais brancher du 5 V sur une broche GPIO.
9. Les modules externes doivent etre en 3.3 V logique, sauf documentation contraire.

---

## 5. Preparation du poste

### 5.1 Installer le logiciel PPK2

1. Sur le Mac, installer nRF Connect for Desktop.
2. Ouvrir nRF Connect.
3. Installer l'application Power Profiler.
4. Brancher le PPK2 au Mac avec son cable USB.
5. Ouvrir Power Profiler.
6. Verifier que le PPK2 apparait dans la liste des appareils.

### 5.2 Preparer un fichier de mesures

Creer un tableau avec ces colonnes :

| Date | Test | Firmware | Tension | Mode PPK2 | Deep sleep | Pic boot | Courant actif moyen | Duree active | Charge evenement | Commentaire |
|---|---|---|---:|---|---:|---:|---:|---:|---:|---|

Nom recommande :

`2026-06-08_mesures-esp32s3-ppk2.csv`

---

## 6. Phase A — Verification simple ESP32 sans PPK2

But : verifier que l'ESP32 fonctionne avant d'ajouter la mesure.

### 6.1 Brancher l'ESP32 au Mac

1. Poser l'ESP32-S3 sur une table non conductrice.
2. Brancher le cable USB-C entre le Mac et l'ESP32.
3. Ouvrir Arduino IDE.
4. Choisir la carte ESP32-S3 correspondant au DevKit.
5. Choisir le port serie detecte.

### 6.2 Flasher un programme blink

Charger un programme simple qui imprime dans le moniteur serie :

```cpp
void setup() {
  Serial.begin(115200);
}

void loop() {
  Serial.println("WildNexus ESP32-S3 alive");
  delay(1000);
}
```

1. Cliquer Upload.
2. Ouvrir le moniteur serie a 115200 bauds.
3. Verifier que le message apparait toutes les secondes.
4. Si rien n'apparait, regler le port serie ou maintenir BOOT pendant l'upload selon le comportement du DevKit.

Resultat attendu : l'ESP32 repond.

---

## 7. Phase B — Firmware deep sleep minimal

But : preparer la carte pour une mesure de sommeil profond.

### 7.1 Flasher le firmware

Brancher l'ESP32 en USB et flasher :

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

### 7.2 Verifier le comportement

1. Ouvrir le moniteur serie.
2. Attendre le message.
3. Attendre 30 secondes.
4. Verifier que le message revient.
5. Fermer le moniteur serie.
6. Debrancher le cable USB de l'ESP32.

Resultat attendu : la carte se reveille toutes les 30 secondes.

---

## 8. Phase C — Mesure PPK2 en Source Meter

Mode recommande pour debuter : le PPK2 alimente l'ESP32 et mesure.

### 8.1 Reglage PPK2

Dans Power Profiler :

1. Selectionner `Source Meter`.
2. Regler la tension de sortie a `5.0 V`.
3. Regler la limite de courant a `500 mA` si l'option est disponible.
4. Verifier que la sortie est `OFF`.
5. Cliquer `Start` pour preparer l'acquisition.

### 8.2 Branchement PPK2 -> ESP32

ESP32 debranche de l'USB.

| PPK2 | ESP32-S3 DevKit |
|---|---|
| VOUT | 5V |
| GND | GND |

Ordre :

1. Brancher le fil noir ou sombre : PPK2 GND -> ESP32 GND.
2. Brancher le fil rouge : PPK2 VOUT -> ESP32 5V.
3. Verifier que rien n'est branche sur USB ESP32.
4. Verifier que VOUT ne touche aucune broche GPIO.

### 8.3 Allumer

1. Dans Power Profiler, activer la sortie PPK2.
2. Observer la courbe.
3. Attendre au moins 2 minutes.
4. Chercher les pics de reveil toutes les 30 secondes.
5. Zoomer sur les zones plates entre les pics.

### 8.4 Mesures a noter

Noter :

- courant deep sleep stable entre deux pics ;
- courant pic au reveil ;
- duree du pic actif ;
- charge consommee sur un cycle de 30 secondes si Power Profiler l'affiche.

Interpretation rapide :

| Observation | Interpretation |
|---|---|
| pics toutes les 30 s | firmware OK |
| pas de pic, courant nul | mauvais cablage ou sortie OFF |
| courant tres eleve constant | carte pas en sleep ou court-circuit |
| deep sleep en mA | DevKit probablement trop consommateur, a documenter |

---

## 9. Phase D — Mesure de reference active

But : mesurer un reveil simple et un retour sommeil propre.

### 9.1 Flasher le firmware reveil court

Rebrancher l'ESP32 en USB. Deconnecter d'abord le PPK2 de l'ESP32.

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

Puis :

1. Flasher.
2. Debrancher USB.
3. Rebrancher PPK2 comme en Phase C.
4. Mesurer 20 cycles.

### 9.2 Resultat attendu

- Un pic actif d'environ 2 a 3 secondes.
- Retour net au deep sleep.
- 20 cycles sans blocage.

Si le courant ne redescend jamais, le firmware ne dort pas ou un peripherique reste actif.

---

## 10. Phase E — Simulation du cycle WildNexus

But : mesurer un cycle proche de la logique P0 sans attendre tous les modules.

### 10.1 Firmware simulation

```cpp
#include "esp_sleep.h"

void setup() {
  Serial.begin(115200);
  delay(500);
  Serial.println("WN event start");

  delay(2000); // reveil + traitement PIR simule
  delay(5000); // capture camera simulee
  delay(2000); // ecriture SD simulee
  delay(2000); // transmission LoRa simulee

  Serial.println("WN event sleep");
  Serial.flush();
  esp_sleep_enable_timer_wakeup(60ULL * 1000000ULL);
  esp_deep_sleep_start();
}

void loop() {}
```

### 10.2 Mesure

1. Flasher par USB.
2. Debrancher USB.
3. Alimenter par PPK2.
4. Mesurer 10 cycles.
5. Noter la charge par evenement.

Calcul manuel si besoin :

```text
mAh_evenement = courant_actif_moyen_mA x duree_active_secondes / 3600
```

Exemple : 120 mA pendant 11 s = 120 x 11 / 3600 = 0.367 mAh.

---

## 11. Phase F — Test microSD SPI

A faire seulement si le module microSD est disponible.

### 11.1 Preparer la carte microSD

1. Inserer la microSD dans un adaptateur Mac.
2. Formater en FAT32.
3. Nommer le volume `WILDNEXUS`.
4. Ejecter proprement.
5. Inserer la microSD dans le module microSD.

### 11.2 Branchement microSD

Attention : utiliser un module compatible logique 3.3 V.

| Module microSD | ESP32-S3 |
|---|---|
| VCC | 3V3 |
| GND | GND |
| SCK | GPIO12 |
| MISO / DO | GPIO13 |
| MOSI / DI | GPIO11 |
| CS | GPIO10 |

Si ces broches sont deja occupees par une camera ou un autre module, ne pas improviser : noter le conflit et demander arbitrage [[Forge]].

### 11.3 Ordre d'allumage

1. ESP32 debranche de l'USB.
2. PPK2 sortie OFF.
3. Brancher la microSD a l'ESP32.
4. Verifier VCC sur 3V3, jamais 5V sauf module explicitement prevu pour 5V.
5. Flasher le firmware SD par USB si necessaire.
6. Debrancher USB.
7. Brancher PPK2 sur 5V/GND.
8. Activer PPK2.

### 11.4 Firmware test SD minimal

```cpp
#include "FS.h"
#include "SD.h"
#include "SPI.h"
#include "esp_sleep.h"

#define SD_CS 10
#define SD_MOSI 11
#define SD_SCK 12
#define SD_MISO 13

void setup() {
  Serial.begin(115200);
  delay(500);

  SPI.begin(SD_SCK, SD_MISO, SD_MOSI, SD_CS);
  if (SD.begin(SD_CS, SPI)) {
    File f = SD.open("/wn_test.txt", FILE_APPEND);
    if (f) {
      f.println("WildNexus SD write ok");
      f.close();
    }
    SD.end();
  }

  Serial.flush();
  esp_sleep_enable_timer_wakeup(60ULL * 1000000ULL);
  esp_deep_sleep_start();
}

void loop() {}
```

### 11.5 Mesures a noter

- courant pendant initialisation SD ;
- duree initialisation SD ;
- courant pendant ecriture ;
- charge totale du cycle ;
- retour ou non au deep sleep.

Verifier ensuite sur le Mac que `wn_test.txt` existe.

---

## 12. Phase G — Test LoRa simule puis reel

### 12.1 Avant module LoRa

Utiliser la Phase E comme simulation TX.

### 12.2 Quand le module SX1262 / RAK3172 est disponible

Ne pas brancher sans verifier le pinout du module exact.

Mapping SPI propose pour SX1262 breakout standard :

| Module LoRa | ESP32-S3 |
|---|---|
| VCC | 3V3 |
| GND | GND |
| SCK | GPIO12 |
| MISO | GPIO13 |
| MOSI | GPIO11 |
| NSS / CS | GPIO9 |
| DIO1 | GPIO14 |
| BUSY | GPIO15 |
| RESET | GPIO16 |

Regle : si la microSD utilise deja le meme bus SPI, SCK/MISO/MOSI peuvent etre partages, mais chaque module doit avoir son propre CS. SD_CS = GPIO10, LORA_CS = GPIO9.

### 12.3 Test attendu

1. Envoyer un paquet court toutes les 60 secondes.
2. Mesurer le pic TX.
3. Verifier que le module retourne en sleep.
4. Noter duree TX et charge TX.

Critere : pas de module LoRa laisse en idle permanent.

---

## 13. Phase H — Test camera

A faire seulement quand le module camera exact est recu.

### 13.1 Regle

Ne pas cabler la camera DVP sans pinout du module exact. Les modules OV5640 / OV2640 / Arducam ont des brochages differents selon les versions.

### 13.2 Preparation physique

1. Couper PPK2.
2. Debrancher USB.
3. Inserer la nappe camera dans son connecteur si module a nappe.
4. Verifier le sens de la nappe.
5. Ne jamais forcer le connecteur.

### 13.3 Test de mesure

Mesures a produire :

- courant boot camera ;
- duree boot camera ;
- courant capture ;
- duree capture ;
- charge capture ;
- retour deep sleep apres capture.

Critere M-02 : image utilisable + retour sommeil stable. La qualite image finale est traitee dans ADR-002, pas ici.

---

## 14. Phase I — Test PIR wake

A faire quand le PIR est disponible.

### 14.1 Branchement typique

| PIR | ESP32-S3 |
|---|---|
| VCC | 3V3 |
| GND | GND |
| OUT | GPIO4 |

GPIO4 est choisi car il peut etre utilise comme broche de reveil RTC selon configuration ESP32-S3. Verifier avant PCB final.

### 14.2 Manipulation

1. Flasher le firmware reveil GPIO.
2. Debrancher USB.
3. Alimenter par PPK2.
4. Laisser la carte dormir.
5. Passer la main devant le PIR.
6. Verifier pic de reveil.
7. Verifier retour sommeil.

Critere : 50 reveils manuels sans blocage.

---

## 15. Phase J — Test alimentation AA + buck

A faire seulement quand le buck TPS62840 ou equivalent est cable.

### 15.1 Pourquoi

Le PPK2 a 5 V mesure le DevKit. Le produit P0 utilisera 8 x AA en 4S2P avec buck 3.3 V. Il faut donc mesurer le banc alimentation reel.

### 15.2 Deux modes possibles

Mode simple :

| Source | Connexion |
|---|---|
| PPK2 Source Meter 5 V | ESP32 5V/GND |

Mode produit :

| Source | Connexion |
|---|---|
| Pack AA ou alim labo 4.8-6.0 V | entree buck |
| sortie buck 3.3 V | rail 3V3 du systeme |
| PPK2 Ampere Meter | en serie entre source et buck |

### 15.3 Branchement PPK2 en Ampere Meter

Uniquement avec une alimentation externe.

| Element | Connexion |
|---|---|
| + alimentation externe | PPK2 VIN |
| PPK2 VOUT | entree + du buck |
| - alimentation externe | GND commun |
| GND buck / ESP32 | GND commun |

Ordre :

1. Alimentation externe OFF.
2. PPK2 connecte au Mac.
3. Power Profiler en `Ampere Meter`.
4. Brancher + alim -> PPK2 VIN.
5. Brancher PPK2 VOUT -> entree buck +.
6. Brancher tous les GND ensemble.
7. Allumer alimentation externe.
8. Demarrer mesure.

Ne pas utiliser Ampere Meter si le cablage n'est pas clair.

---

## 16. Calcul autonomie

### 16.1 Formule

```text
sleep_mAh_jour = courant_sleep_mA x 24
event_mAh_jour = mAh_evenement x nombre_evenements_jour
conso_totale_jour = sleep_mAh_jour + event_mAh_jour + housekeeping_mAh_jour
autonomie_jours = capacite_batterie_mAh / conso_totale_jour
```

Pour premiere estimation, mettre `housekeeping_mAh_jour = 0.5`.

### 16.2 Scenarios obligatoires

| Scenario | Evenements/jour |
|---|---:|
| calme | 24 |
| normal | 72 |
| charge | 120 |

### 16.3 Capacites a utiliser

| Batterie | Capacite de calcul |
|---|---:|
| 8 x AA NiMH 4S2P | 5000 mAh |
| 8 x AA Lithium 4S2P | 7000 mAh |

---

## 17. Fiche de resultats a remplir

```text
Date :
Operateur :
Carte ESP32 :
Firmware :
Modules branches :
Mode PPK2 :
Tension :

Deep sleep stable :
Pic boot :
Duree active :
Charge evenement :
Cycles testes :
Cycles OK :
Blocages :

Autonomie 24 evt/j :
Autonomie 72 evt/j :
Autonomie 120 evt/j :

Decision :
[ ] ESP32-S3 OK pour continuer
[ ] ESP32-S3 OK mais optimisation obligatoire
[ ] ESP32-S3 douteux, tester STM32U5
[ ] ESP32-S3 no-go

Commentaires :
```

---

## 18. Escalade

Appeler [[Araignée]] si :

- deep sleep superieur a 150 uA apres firmware minimal ;
- reveil GPIO/PIR instable ;
- conflit de broches SPI/camera/SD/LoRa ;
- code bloque avant retour sommeil.

Appeler [[Forge]] si :

- cablage d'un module externe est incertain ;
- microSD ou LoRa ne s'initialise pas ;
- integration multi-modules cree des conflits ;
- besoin de script de collecte automatique.

Appeler [[Chouette]] si :

- test PIR ou scenario terrain est ambigu ;
- protocole de manipulation n'est pas executable par un operateur ;
- preparation M-03 terrain commence.

Appeler [[Bruno]] si :

- autonomie calculee est proche du seuil ;
- changement batterie ou buck modifie le budget ;
- cout d'une alternative MCU devient pertinent.

Appeler [[Castor]] si :

- la decision impacte ADR-001 ou ADR-005 ;
- il faut formaliser go/no-go M-02 ;
- les donnees doivent entrer dans un registre structure.

Appeler [[Corbeau]] si :

- resultats doivent etre indexes dans NotebookLM / Obsidian ;
- une fiche de synthese doit etre produite pour le dossier projet.

---

## 19. References

- [[ADR-001-choix-mcu-p0]] — ESP32-S3 candidat primaire.
- [[ADR-005-energie-autonomie-p0]] — seuils energie et autonomie.
- [[ADR-003-choix-radio-lpwan-p0]] — LoRa P0.
- Nordic PPK2 User Guide — Source Meter / Ampere Meter.
- Espressif ESP32-S3 Sleep Modes — deep sleep, wake sources, Wi-Fi/BLE off before sleep.
- Espressif ESP32-S3 DevKitC-1 User Guide — alimentation 5V/GND et broches carte.
