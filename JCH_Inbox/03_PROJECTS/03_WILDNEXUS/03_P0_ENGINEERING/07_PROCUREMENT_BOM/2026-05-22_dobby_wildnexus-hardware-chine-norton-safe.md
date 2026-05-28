# WildNexus - Extension Chine hardware, version Norton-safe

**Date :** 2026-05-22  
**Objet :** completer l'etude STM32U5 / Apollo510 / STM32N6 / Raspberry / NXP avec des producteurs et ecosystemes chinois.  
**Note Norton :** ce fichier evite volontairement les URL cliquables brutes. Les sources sont citees par nom en fin de document pour limiter les faux positifs antivirus sur les fichiers Markdown contenant beaucoup de liens techniques.

## 1. Verdict rapide

L'acces Chine change la donne pour WildNexus, surtout sur deux segments :

- **Satellite Camera Smart low-cost** : petits SoC camera avec ISP, MIPI CSI, encodeur video et NPU leger.
- **Base Nexus IA locale** : SBC/SOM puissants moins chers que certaines alternatives occidentales.

Les pistes a prendre au serieux :

1. **Rockchip RV1106 / RV1103** : meilleure piste immediate pour un petit satellite camera IA.
2. **Rockchip RK3588 / RK3588S** : alternative puissante a [[Raspberry Pi 5]] pour la Base Nexus.
3. **Axera AX630C** : tres prometteur pour camera IA compacte.
4. **Sophgo SG2002 / SG2000** : excellent pour apprendre et prototyper en IA vision low-cost.
5. **Kendryte K230** : bon banc R&D vision/multi-camera RISC-V.
6. **Allwinner V853** : interessant pour camera economique avec ISP/NPU.
7. **GigaDevice GD32H7** : alternative MCU Chine a STM32H7, utile supply, pas IA lourde.

## 2. Tableau comparatif

| Plateforme | Producteur / ecosysteme | Type | Specs utiles | Prix indicatif | Role WildNexus possible | Verdict |
|---|---|---|---|---:|---|---|
| Rockchip RV1106 / RV1103 | Rockchip, Luckfox, Waveshare | Vision SoC Linux compact | Cortex-A7, RISC-V MCU, ISP, MIPI CSI, NPU 0.5-1 TOPS selon version, H.264/H.265 | Luckfox Pico Ultra env. 39-83 USD selon options | Satellite Smart low-cost camera, piege photo IA leger | Tres interessant a tester vite |
| Rockchip RK3568 | Rockchip, Geniatech, Boardcon, Firefly | Application processor Linux industriel | 4x Cortex-A55, NPU 1 TOPS, MIPI CSI, 4K decode, 1080p encode | SBC/SOM souvent 60-150+ USD selon format | Base legere, passerelle terrain | Stable mais moins puissant que RK3588 |
| Rockchip RK3588 / RK3588S | Rockchip, Orange [[Pi]], Radxa, Firefly | SBC/SOM Linux edge AI | 4x A76 + 4x A55, NPU 6 TOPS, ISP, MIPI CSI, encode/decode 8K, PCIe/NVMe | Orange [[Pi]] 5 / ROCK 5B souvent env. 150-250 USD selon RAM | Base Nexus puissante, bench IA/video, serveur terrain | Excellent rapport puissance/prix, software a auditer |
| Allwinner V853 | Allwinner | Vision SoC basse conso | Cortex-A7 + RISC-V E907, NPU 1 TOPS INT8, MIPI CSI, H.265/H.264 5MP@25fps | variable selon module/devkit | Satellite camera economique | A garder dans shortlist si support fournisseur bon |
| Sophgo SG2002 / SG2000 | Sophgo, Sipeed, Milk-V, Seeed | RISC-V/Arm AI camera SoC | SG2002 : 1 TOPS INT8, 256 MB SiP, H.264/H.265 5MP@30fps, MIPI CSI | Milk-V Duo 256M env. 8 USD ; Duo S/boards complets env. 20-40+ USD | Apprentissage IA vision/audio, prototypes satellites | Tres bon pour apprendre, prudence produit final |
| Kendryte K230 | Canaan Kendryte, CanMV, Banana [[Pi]] | RISC-V AI vision SoC | dual RISC-V C908, KPU INT8/INT16, 3x MIPI CSI, H.264/H.265/JPEG/MJPEG | CanMV-K230 env. 40-90 USD selon kit | Banc vision embarquee, experimentation multi-camera | R&D interessante, industrialisation a valider |
| Axera AX630C | Axera, Sipeed MaixCAM2 | AI camera SoC | dual Cortex-A53, NPU 3.2 TOPS INT8 / 12.8 TOPS INT4, camera 4K selon modules | premiers kits annonces autour de 69+ USD, disponibilite a confirmer | Satellite Smart vision premium, banc vision local | Tres prometteur, encore jeune cote produit |
| Axera AX650N | Axera | Smart IP camera SoC | NPU annoncee 72 TOPS INT4, cible camera/vision pro | prix non public, relation fournisseur requise | Base vision/surveillance avancee ou module premium | A ouvrir si acces industriel direct |
| Bouffalo BL808 | Bouffalo Lab | RISC-V multimedia MCU/SoC | MIPI CSI/DVP, Wi-Fi/BLE selon design, NPU BLAI-100 | boards rares/variables | Idee camera+wireless compacte | Trop risque pour trajectoire critique |
| GigaDevice GD32H7 | GigaDevice | MCU Cortex-M7 industriel | jusqu'a 600 MHz, 1-3.84 MB flash, env. 1 MB SRAM, camera DVP, LCD, SDIO, Ethernet | composant/devboard a verifier via canaux Chine | Alternative MCU puissante a STM32H7 | Bon plan supply, pas IA lourde |
| WCH CH32V / CH32H | WCH | MCU RISC-V tres bas cout | RISC-V, nombreux peripheriques, ecosysteme specifique | souvent <1-5 USD selon reference/quantite | Sous-modules capteurs, auxiliaires | Pas coeur WildNexus |
| Quectel / Fibocom / SIMCom | Producteurs cellular IoT | Modules 4G/LTE-M/NB-IoT/5G | Cat 1 bis, LTE-M, NB-IoT, GNSS selon module, temperature industrielle | Quectel EG916Q env. 30-35 USD en distribution, moins en volume possible | Backhaul base/satellite smart, telemetry | A integrer dans la strategie Chine |

## 3. Analyse critique

### Rockchip RV1106

C'est probablement la meilleure piste chinoise court terme pour WildNexus. Le RV1106 apporte ce que l'[[ESP32-S3]] ne peut pas porter correctement : vrai pipeline camera, MIPI CSI, ISP, encodeur video, NPU leger et Linux compact.

Il ne remplace pas STM32U5 pour un satellite dormant tres basse consommation. Il cree plutot une nouvelle categorie : **Satellite Camera Smart low-cost**.

### RK3588 / RK3588S

Le RK3588 est un concurrent serieux de [[Raspberry Pi 5]] pour la Base Nexus : CPU puissant, NPU 6 TOPS, video, PCIe/NVMe, camera, Linux. Il peut etre tres attractif si l'objectif est une base locale capable d'analyser image/son/video.

Point faible : logiciel et maintenance. Il faut auditer kernel, RKNN, support long terme, securite, stabilite stockage et qualite camera avant d'en faire une base industrielle.

### Axera AX630C / AX650N

Axera merite une vraie ouverture fournisseur. Le AX630C colle bien a notre besoin camera IA compacte. Le AX650N vise plus haut, type smart camera ou surveillance avancee.

Questions a poser cote Chine : temperature industrielle, SDK complet, conversion ONNX/PyTorch, support capteurs low-light, documentation complete, prix par 100 / 1 000 / 10 000, disponibilite module ou composant nu.

### Sophgo SG2002 et Kendryte K230

Tres bons pour apprendre vite et tester des modeles. Le prix est bas, les boards sont disponibles, et l'orientation camera/IA est claire.

Pour un produit final, il faut auditer SDK, documentation, cycle de vie, support, temperature, humidite, stockage et possibilite de passer d'une board maker a un SOM ou design custom.

### GigaDevice

GigaDevice peut aider sur le cout et la supply d'une architecture MCU, mais ne resout pas l'IA embarquee. A comparer a STM32H7/U5, pas a STM32N6.

## 4. Shortlist achat/test

1. **Luckfox Pico Ultra W / RV1106G3** : test satellite camera IA low-cost.
2. **Orange [[Pi]] 5 ou Radxa ROCK 5B / RK3588(S)** : test Base Nexus alternative a [[Raspberry Pi 5]].
3. **Milk-V Duo 256M ou Duo S / SG2002-SG2000** : apprentissage Linux + camera + NPU tres bas cout.
4. **CanMV-K230** : test vision embarquee multi-camera et toolchain Kendryte.
5. **Sipeed MaixCAM2 / AX630C** : achat quand disponibilite hors premiers lots est claire.
6. **Carte GD32H7** : seulement pour evaluer une alternative MCU Chine.

## 5. Consequence architecture WildNexus

| Niveau | Role | Candidats non chinois | Candidats chinois |
|---|---|---|---|
| Satellite Lite sobre | capteurs, veille, [[LoRa]], audio leger | STM32U5, Apollo510 | GD32H7 seulement si logique STM32-like ; WCH pour sous-modules |
| Satellite Camera Smart low-cost | image/video, detection locale, compression, alerte | STM32N6 | Rockchip RV1106, Allwinner V853, Axera AX630C |
| Base Nexus IA locale | stockage, [[BirdNET]], vision, orchestration, 4G/5G | [[Raspberry Pi 5]], NXP i.MX 8M Plus | RK3588/RK3588S |

Je recommande deux lots d'evaluation :

**Lot A - industriel classique :** STM32U5, Apollo510, STM32N6, [[Raspberry Pi 5]], NXP i.MX 8M Plus.  
**Lot B - Chine offensive :** RV1106, RK3588, AX630C, SG2002, K230.

## 6. Decision provisoire

Je ne remplacerais pas STM32U5 par une puce chinoise pour le **Satellite Lite sobre** tant qu'on n'a pas un excellent dossier energie/supply/support.

En revanche, je challengerais fortement STM32N6 avec **Rockchip RV1106** et **Axera AX630C** pour le **Satellite Camera Smart**.

Pour la **Base Nexus**, je garderais [[Raspberry Pi 5]] comme point de depart pedagogique, mais je testerais vite **RK3588/RK3588S** comme alternative cout/puissance. Pour une version industrielle robuste, NXP i.MX 8M Plus reste plus rassurant, mais probablement plus cher.

## 7. Sources neutralisees

Sources consultees : Rockchip RK3588S product brief et datasheet, Orange [[Pi]] 5, Radxa ROCK 5B, Geniatech RK3568, Allwinner V853, Luckfox Pico Ultra, Milk-V Duo, Sipeed MaixCAM, Kendryte K230 product brief, CanMV-K230, Hiwonder CanMV K230, Axera AX630C, Sipeed MaixCAM2, GigaDevice GD32H7.

Les URL completes sont volontairement absentes de cette version pour eviter une nouvelle quarantaine Norton. Les liens peuvent etre conserves dans une bibliographie separee au format texte neutralise si necessaire.
