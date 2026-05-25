# WildNexus WP02 — matrice hardware P0 et encombrement v0.1

**Date :** 2026-05-23  
**Statut :** travail — base pour shortlist achat et fermeture ADR-006  
**Owner :** Dobby + Forge + Chouette + Castor  

## 1. Decision de cadrage

Le P0 reste un **Satellite Lite autonome** :

- ESP32-S3 ;
- camera OV5640/IR + lentille M12 ;
- PIR ;
- micro mono ;
- microSD ;
- LoRa metadata ;
- Wi-Fi local maintenance/extraction ;
- holder AA ;
- bloc capteurs reserve ;
- antenne LoRa la moins visible possible.

Le **Raspberry Pi 5** est considere maintenant, mais uniquement comme **Base/Master Nexus P1**. Il ne rentre pas dans le satellite terrain P0.

## 2. Principe mecanique

Le P0 doit etre fonctionnellement simple, mais mecaniquement prevoyant. Le boitier et le PCB doivent eviter de fermer trop tot :

- reserve bloc capteurs environnementaux ;
- antenne LoRa interne ou camouflee ;
- acces microSD ;
- passage micro acoustique et membrane/protection ;
- calage sur support rond ;
- option future skin camouflage.

Objectif JCH : **moins on change de choses apres P0, mieux c'est**.

## 3. Matrice hardware Satellite Lite P0

| Bloc | Choix v0.1 | Role | Encombrement a reserver | Decision / risque |
|---|---|---|---|---|
| MCU prototype | ESP32-S3-DevKitC-1 N8R8 | banc M-02, firmware, mesure conso | dev board a traiter comme temporaire ; PCB final plus compact | ne pas dimensionner le boitier final sur le devkit |
| MCU final PCB | ESP32-S3-WROOM-1U N8R8 ou equivalent | controle, capture, stockage, radio, Wi-Fi local | module + zone antenne/ipex + routage camera | verifier PSRAM, pins camera, consommation sleep |
| Camera | OV5640 5MP DVP M12 | capture image jour/nuit | module + nappe + support M12 + fenetre optique | module exact encore a sourcer ; DVP explicite obligatoire |
| Lentille | M12 IR-corrigee f/1.8, 4-6 mm | qualite image et focus jour/nuit | profondeur lentille + reglage focus + protection fenetre | Lensation/Evetar priorites ; eviter lentille collee |
| IR | 850 nm + 940 nm en test | eclairage nocturne pulse | cluster LED + dissip/driver + angle | decision finale apres test faune/portee |
| PIR | Panasonic EKMB low-power ou equivalent | declenchement basse conso | fenetre PIR + volume Fresnel + orientation | FOV a choisir avec boitier |
| Micro mono | MEMS I2S/PDM type SPH0645 ou equivalent | clips audio courts locaux | port acoustique + membrane/protection eau + decouplage bruit boitier | standard P0, sans BirdNET embarque |
| Stockage | microSD industrielle 8-16 GB | raws image/audio, logs, index | socket accessible ou trappe service | attention coupure propre et etancheite acces |
| Radio | RAK3172/RAK3172-T EU868 ou SX1262 equivalent | LoRa P2P metadata | module + zone RF + antenne interne/camouflee | RF a tester dans boitier final |
| Antenne | interne prioritaire ; camouflee branche si besoin | portee LoRa discrete | volume RF sans metal proche ; option relief boitier | antenne fouet visible = dernier recours |
| Batterie | 8x AA 4S2P reference mecanique ; 4x AA a tester | autonomie terrain | holder 8x AA ou 2x holder 4x AA | 8x AA peut etre surdimensionne ; decision apres modele + mesures |
| Buck | TPS62840 ou equivalent faible Iq | conversion 4-6 V vers 3.3 V | petite zone PCB + inductance | pic courant carte complete a verifier |
| Bloc capteurs | BME688/AS7341 reserve ; GPS reserve P1 | environnement, lumiere, extension | petit module expose/ventile + chemin optique si AS7341 | reserve mecanique P0, montage fonctionnel optionnel |
| Boitier | IP67 commerce P0 ; forme bio/3D P1 | protection terrain | cible initiale 150 x 100 x 60 mm a challenger | ADR-006 reste propose jusqu'a dimensionnement |
| Sangle/support | sangle UV + dos concave/patins | fixation sur tronc/poteau | rainures, berceau, anti-rotation | tester support rond 10-40 cm |

## 4. Encombrement v0.1

Cette estimation est volontairement conservatrice. Elle sert a comparer 4 AA vs 8 AA et a choisir un boitier de banc.

| Sous-ensemble | Hypothese volume / footprint | Commentaire |
|---|---:|---|
| Holder 8x AA | ~110 x 60 x 20 mm | bloc dominant ; reference mecanique prudente |
| Holder 4x AA | ~60 x 60 x 20 mm | variante compacte a tester energie |
| PCB principal custom | cible 80 x 55 mm | ESP32-S3, buck, LoRa, microSD, connecteurs, MOSFET |
| Camera + M12 + fenetre | ~30 x 30 x 25 mm | profondeur optique importante |
| PIR + fenetre | ~25 x 25 x 15 mm | depend du Fresnel/FOV |
| Micro + protection | ~15 x 15 x 8 mm | inclut port acoustique et membrane |
| Bloc capteurs reserve | ~25 x 20 x 10 mm | BME688/AS7341/GPS reserve selon version |
| Antenne interne/camouflee | ~80-90 mm de developpe RF | quart d'onde 868 MHz a adapter mecaniquement |
| Silica gel + joints + cablage | ~20 x 20 x 10 mm | maintenance terrain |

### Lecture

- **8 AA** donne une enveloppe plus sure pour 60 jours, mais pousse vers un boitier moins discret.
- **4 AA** peut etre suffisant pour un Satellite Lite calme, mais doit etre prouve par modele theorique + mesures M-02.
- Le boitier P0 doit peut-etre accepter physiquement 8 AA, tout en permettant une version interne 4 AA pour test.

## 5. Decision batterie a traiter avec le modele autonomie

Le classeur `WildNexus_P0_Autonomy_Model.xlsx` devient l'outil de decision 4 AA vs 8 AA.

Tests a faire avant figer le boitier :

1. scenario calme, moyen, dense ;
2. photo standard ;
3. video standard ;
4. video longue event X ;
5. audio-only ;
6. 4 AA lithium vs 8 AA lithium ;
7. 4 AA NiMH vs 8 AA NiMH ;
8. marge froid/vieillissement.

Decision recommandee a ce stade :

- garder **8 AA comme enveloppe mecanique de reference** ;
- tester **4 AA comme variante compacte** ;
- ne pas fermer ADR-006 avant mesures M-02.

## 6. Base/Master Nexus P1 — visible mais non bloquant P0

| Bloc | Choix v0.1 | Role | Statut |
|---|---|---|---|
| Compute | Raspberry Pi 5 | BirdNET-Go, YOLO, indexation, gateway locale | P1 parallele |
| Stockage | SSD USB/NVMe | raws, index, dataset terrain | P1 |
| Reseau | Wi-Fi/Ethernet, 4G optionnelle | synchro locale/cloud | P1 |
| Alimentation | secteur/powerbank/solaire P1 | station fixe ou semi-fixe | hors satellite |

Raison : le Pi est excellent pour accelerer l'intelligence WildNexus, mais mauvais comme coeur d'un satellite 60 jours.

## 7. Points a verifier avant achat

1. Module OV5640 exact : DVP, M12, NoIR ou IR-cut gere, pinout documente.
2. Holder AA exact : footprint et acces terrain.
3. Boitier candidat : volume utile reel, pas seulement dimensions externes.
4. PIR : FOV compatible hauteur de pose et fenetre boitier.
5. Micro : protection eau/vent et bruit mecanique du boitier.
6. Antenne LoRa : interne/camouflee vs fouet visible, test RF obligatoire.
7. Bloc capteurs : BME688/AS7341 reserve sans complexifier le P0.

## 8. Sources techniques consultees

- Espressif ESP32-S3-DevKitC-1 : https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32s3/esp32-s3-devkitc-1/user_guide_v1.0.html
- RAK3172 datasheet : https://docs.rakwireless.com/product-categories/wisduo/rak3172-module/datasheet/
- Bosch BME688 : https://www.bosch-sensortec.com/products/environmental-sensors/gas-sensors/bme688/
- ams OSRAM AS7341 : https://ams-osram.com/products/sensor-solutions/ambient-light-color-spectral-proximity-sensors/ams-as7341-11-channel-spectral-color-sensor
- Knowles SPH0645LM4H-B : https://www.digikey.com/htmldatasheets/production/1794128/0/0/1/sph0645lm4h-b-datasheet.html
- Raspberry Pi 5 mechanical drawing : https://datasheets.raspberrypi.com/rpi5/raspberry-pi-5-mechanical-drawing.pdf

## 9. Prochaine action

Produire une shortlist achat v0.1 avec 2 options :

- **Option A — banc rapide** : modules dev/evaluation pour mesurer energie et flux.
- **Option B — proto terrain compact** : composants proches PCB final et boitier test.

Puis fermer ADR-006 quand les dimensions et le choix batterie seront assez solides.
