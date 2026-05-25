# WildNexus - Etude critique hardware satellite/base

**Date :** 2026-05-22  
**Objet :** relancer le choix hardware apres pivot multimodal et hypothese satellites + base  
**Statut :** etude v0.1, a transformer en ADR apres validation JCH  
**Orchestration :** Dobby  
**Equipe mobilisee :** Forge, Chouette, Furet, Clio, Atlas, Renard

## 1. Decision a prendre

La question n'est plus : faut-il remplacer ESP32 ?

La question correcte est :

> quelle intelligence vit dans le satellite, quelle intelligence vit dans la base, et quels liens transportent seulement des evenements versus des donnees lourdes ?

ESP32-S3 ne doit plus etre le cerveau WildNexus. Il peut rester un controleur simple dans certains prototypes, mais il ne doit pas porter l'ambition multimodale.

## 2. Hypotheses fonctionnelles

WildNexus doit gerer :

- images ;
- video courte ;
- audio oiseaux et potentiellement ultra-sons ;
- capteurs environnementaux ;
- detection evenementielle ;
- stockage local lourd ;
- signalement distant ;
- demande de telechargement par l'utilisateur ;
- IA locale ou proche du terrain ;
- fonctionnement sans retour terrain frequent.

Les donnees lourdes ne passent pas par LoRa. LoRa transporte statut, alerte, index, commande, demande de transfert, metadata.

## 3. Architecture produit recommandee

### 3.1 Satellite Lite

Role : noeud terrain discret, sobre, peu couteux.

Fonctions :

- capture image/audio selon evenement ;
- stockage microSD industriel ;
- capteurs environnementaux ;
- LoRa/LoRaWAN pour alerte et metadata ;
- Wi-Fi local court pour maintenance/telechargement ;
- pas d'IA lourde.

Hardware candidat :

- STM32U5 pour ultra-low-power pur ;
- Ambiq Apollo510/Apollo510B si audio/IA legere always-on devient critique ;
- ESP32-S3 seulement pour prototype rapide ou provisioning Wi-Fi/BLE, pas comme choix final par defaut.

### 3.2 Satellite Smart

Role : noeud plus cher, capable d'IA legere image/audio sur place.

Fonctions :

- verification animal/non-animal ;
- prefiltrage audio ;
- compression/selection ;
- declenchement croise audio -> camera ou camera -> audio ;
- transfert selectif vers base.

Hardware candidat prioritaire :

- STM32N6.

Rationale :

- MCU industriel ;
- NPU Neural-ART jusqu'a 600 GOPS ;
- pipeline camera MIPI CSI-2 + ISP ;
- H264 hardware ;
- RAM embarquee 4.2 MB + memoires externes rapides ;
- meilleur alignement avec camera/vision que ESP32-S3.

Risque :

- ecosysteme encore jeune ;
- integration plus difficile qu'un Raspberry ;
- besoin d'un vrai firmware embarque, pas d'un bricolage maker.

### 3.3 Base Nexus

Role : noeud cache, plus gros, plus puissant, responsable de l'IA lourde et du backhaul utilisateur.

Fonctions :

- reception metadata satellites ;
- demande et recuperation fichiers lourds ;
- BirdNET-Go ou equivalent ;
- vision IA ;
- correlation image/audio/environnement ;
- stockage local massif ;
- 4G/5G ;
- dashboard local/distant ;
- chiffrement et gestion des droits.

Hardware candidat :

- Raspberry Pi 5 + AI HAT+ pour prototype rapide ;
- NXP i.MX 8M Plus SOM industriel pour version robuste ;
- Hailo-8L/Hailo-8 si vision lourde necessaire ;
- SSD/eMMC plutot que microSD pour la base.

## 4. Plateformes evaluees

| Plateforme | Role possible | Force | Faiblesse | Verdict |
|---|---|---|---|---|
| ESP32-S3 | Satellite Lite prototype | cout, communaute, Wi-Fi/BLE, camera DVP simple | IA limitee, memoire, camera qualite, audio lourd | Declasser comme cerveau |
| STM32U5 | Satellite Lite final | ultra basse consommation, industriel, securite | pas IA/camera lourde native | Tres bon controleur sobre |
| Ambiq Apollo510/B | Satellite Lite audio/always-on | tres basse conso edge AI, Cortex-M55 Helium, BLE sur 510B | moins mature pour camera lourde WildNexus | Candidat audio/veille IA |
| Sony Spresense | Prototype audio/GPS/camera | audio hi-res, GPS, camera, LTE option, faible conso | ecosysteme niche, industrialisation a verifier | Banc interessant, pas choix central |
| STM32N6 | Satellite Smart | NPU 600 GOPS, MIPI CSI-2, ISP, H264, MCU industriel | ecosysteme jeune, integration exigeante | Candidat prioritaire Smart |
| Raspberry Pi 5 | Base prototype | vitesse dev, Linux, BirdNET-Go, communautaire | conso, SD, boot, robustesse terrain | Base proto seulement |
| Raspberry Pi 5 + Hailo | Base IA proto | 13/26 TOPS, vision temps reel | conso/thermique, Linux | Excellent banc IA |
| NXP i.MX 8M Plus | Base industrielle | NPU 2.3 TOPS, dual ISP, audio, Linux industriel, eMMC/SOM | cout, complexite, conso | Candidat base finale |
| Hailo-8L/8 | Coprocesseur base | 13/26 TOPS, edge vision mature | depend host Linux/PCIe, audio pas coeur | Pour base, pas satellite lite |
| Quectel EG916Q | Backhaul base/smart | LTE Cat 1 bis 10/5 Mbps, global, temperature -40/+85 | pas low-power extreme | Bon pour data lourde ponctuelle |
| Quectel BG95 / Nordic nRF9161 | Telemetrie cellulaire basse conso | LTE-M/NB-IoT/GNSS, PSM/eDRX | debit limite pour video/audio lourd | Bon pour metadata, pas media lourd |

## 5. Modes de communication

### LoRa / LoRaWAN

Bon pour :

- alerte evenement ;
- statut batterie ;
- metadata ;
- index fichier ;
- commande de reveil ;
- demande de transfert differe.

Mauvais pour :

- images haute resolution ;
- video ;
- audio brut ;
- update firmware lourd ;
- flux temps reel.

### Wi-Fi local

Bon pour :

- telechargement terrain ;
- satellite vers base proche ;
- configuration ;
- transfert par rafales.

Mauvais pour :

- longue distance en foret ;
- autonomie si laisse actif ;
- reseau mesh complexe non maitrise.

### 4G/5G/LTE Cat 1 bis

Bon pour :

- base vers utilisateur ;
- satellite smart premium ;
- envoi ponctuel de medias selectionnes ;
- gestion distante.

Mauvais pour :

- chaque satellite en standard ;
- autonomie longue si mal gere ;
- abonnement multiple ;
- zones blanches.

### LTE-M / NB-IoT

Bon pour :

- metadata ;
- statut ;
- GNSS ;
- alerte faible debit.

Mauvais pour :

- sons/images/videos lourds.

## 6. Stockage

Satellite :

- microSD industrielle seulement ;
- journalisation append-only ;
- index local separe ;
- politique anti-corruption apres coupure ;
- fichiers lourds conserves localement par defaut.

Base :

- eMMC ou SSD ;
- microSD seulement pour prototype ;
- chiffrement ;
- retention configurable ;
- synchronisation cloud optionnelle.

## 7. Impact budget

Le pivot change la structure budgetaire :

- les satellites Lite peuvent rester raisonnables ;
- les satellites Smart seront plus chers ;
- la base devient le composant couteux mais mutualise ;
- le cout d'abonnement baisse si une seule base cellulaire sert plusieurs satellites.

Le bon kit de depart n'est probablement pas "1 appareil complet", mais :

- 1 Base Nexus ;
- 2 ou 3 satellites Lite ;
- option 1 satellite Smart pour test IA locale.

## 8. Risques

### Risque technique

La complexite principale devient la synchronisation des evenements et la gestion d'energie, pas le capteur isole.

### Risque produit

Un systeme base + satellites est plus difficile a expliquer qu'une camera unique. Il faut une UX tres simple : "placez les petits capteurs, cachez la base, ouvrez l'app".

### Risque dual-use

La meme architecture existe en UGS defense : capteurs acoustiques/sismiques/PIR/camera, reseau radio, base de commandement, discretion. WildNexus doit maintenir son exclusion defense et eviter toute communication marketing "surveillance perimetrique".

### Risque dependance plateforme

Raspberry accelere le prototype mais ne doit pas enfermer la version finale.

## 9. Recommandation Dobby

Je recommande de geler provisoirement cette architecture :

1. **Satellite Lite v0** : STM32U5 ou ESP32-S3 de prototypage, capteurs, LoRa, SD, audio/image capture, pas IA lourde.
2. **Satellite Smart v0** : STM32N6, camera MIPI, IA image/audio legere, stockage local.
3. **Base Nexus v0** : Raspberry Pi 5 + SSD + 4G + BirdNET-Go, puis migration vers NXP i.MX 8M Plus si le concept est valide.

ESP32-S3 reste dans le laboratoire, pas au centre du produit final.

## 10. Prochaines actions

1. Transformer ADR-001 en "choix controleur Satellite Lite" au lieu de "choix MCU WildNexus".
2. Creer ADR-007 "architecture satellite/base".
3. Creer une grille de tests comparatifs :
   - boot/reveil ;
   - capture image ;
   - capture audio ;
   - stockage ;
   - inference ;
   - transfert ;
   - consommation par cycle ;
   - robustesse coupure ;
   - temperature/humidite.
4. Acheter ou preparer trois bancs :
   - Raspberry Pi 5 + SSD + modem 4G pour Base Nexus prototype ;
   - STM32N6 devkit/camera pour Satellite Smart ;
   - STM32U5 ou ESP32-S3 pour Satellite Lite.
5. Tester un scenario simple :
   - satellite detecte evenement ;
   - envoie metadata LoRa ;
   - base decide si fichier lourd necessaire ;
   - satellite transfere par Wi-Fi local ou liaison haut debit ponctuelle ;
   - base analyse et pousse un resume utilisateur.

## 11. Sources consultees

- CuddeLink : https://www.cuddeback.com/cuddelink
- STM32N6 : https://www.st.com/en/microcontrollers-microprocessors/stm32n6-series.html
- NXP i.MX 8M Plus : https://www.nxp.com/products/i.MX8MPLUS
- Raspberry Pi AI HAT+ : https://www.raspberrypi.com/news/raspberry-pi-ai-hat/
- Hailo AI accelerators : https://hailo.ai/products/ai-accelerators/
- Raspberry Pi AI Camera : https://www.raspberrypi.com/products/ai-camera/
- Sony Spresense : https://developer.sony.com/spresense
- Ambiq Apollo510 : https://ambiq.com/product/apollo510/
- Quectel EG916Q-GL : https://www.quectel.com/product/lte-cat-1-bis-eg916q-gl/
- Nordic nRF9161 : https://www.nordicsemi.com/Products/nRF9161
- Wildlife Acoustics Song Meter Mini Bat 2 : https://www.wildlifeacoustics.com/products/song-meter-mini-bat-2-li-ion
- HARK bioacoustic monitor : https://www.hark.nz/
- Exensor UGS : https://www.exensor.com/products/flexnet-flexible-network-of-sensors/unattended-ground-sensors-ugs/
- Rheinmetall ASN100 : https://www.rheinmetall.com/en/products/reconnaissance-and-sensor-systems/asn100

