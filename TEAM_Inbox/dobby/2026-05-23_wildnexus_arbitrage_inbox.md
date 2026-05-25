# WildNexus — arbitrage apres nouveaux depots inbox

Date: 2026-05-23
Auteur: Dobby
Sources inbox:
- `JCH_Inbox/00_INBOX/batteries discussion.md`
- `JCH_Inbox/00_INBOX/birdweather compo.md`
- `JCH_Inbox/00_INBOX/yolo wildnexus 1.md`
- `JCH_Inbox/00_INBOX/yolo_wildnexus_2.md`
- `JCH_Inbox/00_INBOX/wildnexus shema 1.png`

## Decision recommandee

Verrouiller WildNexus P0 comme **Satellite Lite autonome**:
- ESP32-S3 pour controle, reveil, capture, stockage, metadonnees.
- Camera P0 OV5640/IR, PIR, micro mono, microSD, LoRa P2P, Wi-Fi local maintenance/telechargement.
- Alimentation P0: 8x AA 4S2P + buck efficace, pas LiPo/BMS ni solaire obligatoire.
- IA P0: filtre evenementiel simple animal/non-animal ou prefiltrage basique; capture audio locale possible, mais pas YOLO/BirdNET complet sur ESP32.
- Donnees natives: stockees localement sur SD; LoRa transporte uniquement statut, alertes, metadonnees et commandes courtes.

Lancer en parallele un **Base/Master Nexus prototype P1**:
- Raspberry Pi 5 ou equivalent + SSD + Wi-Fi/4G optionnel.
- BirdNET-Go, YOLO, indexation des raws, interface de consultation et synchronisation cloud selective.
- Le Master/Base peut demander a un satellite de remonter un statut ou d'enregistrer, mais ne devient pas une dependance P0.

Le cloud reste **P1/P2**:
- Depot distant et acces utilisateur.
- Pas de flux raw continu en P0.
- Upload raw seulement sur action explicite, proximite Wi-Fi, LTE on-demand ou base locale.

## Lecture des nouveaux depots

### Batteries

La note batteries confirme que le choix AA reste le plus sain pour le terrain. Les piles lithium AA sont robustes au froid, les NiMH rechargeables restent pratiques, et les LiPo ajoutent charge, protection, connectique et risques de maintenance.

Impact decision: garder ADR-005 comme reference P0 et corriger le registre d'approvisionnement qui mentionne encore LiFePO4/solaire.

### BirdWeather PUC

BirdWeather valide une architecture ESP32-S3 + capteurs + microSD + alimentation AA/USB, mais ne valide pas BirdNET complet local sur ESP32. L'inference espece est principalement cloud ou hors microcontroleur.

Impact decision: integrer un micro mono au Satellite Lite P0 pour enregistrer des clips courts locaux, mais utiliser BirdWeather comme inspiration capteurs et packaging, pas comme preuve qu'un satellite P0 peut faire de la reconnaissance bioacoustique locale complete.

### YOLO / ESP32

Les deux notes convergent: YOLO moderne et extraction video fiable sur ESP32 ne sont pas realistes pour WildNexus P0. L'ESP32-S3 peut faire du reveil, de la capture, du prefiltrage tiny et de la transmission metadonnees. Le Pi/Base doit prendre la vision lourde et BirdNET.

Impact decision: ADR-007 doit interdire l'hypothese "YOLO P0 embarque ESP32" et formaliser YOLO/BirdNET cote Base ou Satellite Smart P1.

### Mesh / Master / Cloud

Le schema JCH introduit une bonne structure: Satellite, Master, Cloud, User. La bonne interpretation est une architecture en trois plans:
- Satellite: capter et survivre dehors.
- Master/Base: analyser, indexer, orchestrer localement.
- Cloud: consulter, synchroniser, archiver selectivement.

Impact decision: creer un ADR "Architecture Satellite/Base/Cloud". Ne pas transformer le P0 en reseau mesh ou station cloud complete.

## Avis equipe

Furet: les depots confirment les limites marche/techniques. BirdWeather est utile, mais pas une preuve d'IA locale lourde sur ESP32.

Castor: il faut separer controle, donnees et inference. Le P0 doit rester un satellite autonome; le Master/Base doit etre une brique separee.

Forge: ESP32 + YOLO video est une impasse produit. ESP32 gere energie, capture, watchdog, metadata; Pi/Base gere frame extraction, YOLO, BirdNET.

Chouette: terrain d'abord. AA + SD + LoRa metadata + Wi-Fi local est beaucoup plus maintenable qu'un P0 LiPo/cloud/streaming. Le micro est utile en P0 si l'on reste sur clips courts locaux.

Hermine: eviter le vocabulaire surveillance/mesh commande. Positionner WildNexus comme observation ecologique, donnees locales, souverainete utilisateur.

Dobby: decision finale proposee: ne pas elargir le P0; ajouter Base/Master comme trajectoire P1 parallele.

## ADR a finaliser ou corriger

1. ADR-004 stockage local: microSD industrielle, raws locaux, index evenementiel append-only, extraction Wi-Fi locale.
2. ADR-007 detection evenementielle: PIR + prefiltrage image simple + declenchement/capture audio locale; YOLO/BirdNET exclus du P0 ESP32.
3. ADR-008 capteurs extensibles: temp/humidite interne P0; micro mono P0; BME688, AS7341, GPS et audio scientifique avancee comme options P1/Smart.
4. Nouvel ADR-009 architecture Satellite/Base/Cloud: roles, flux, dependances interdites en P0.
5. ADR-006 boitier: retirer le solaire comme gland obligatoire P0; garder reserve mecanique P1.
6. Supply register: remplacer LiFePO4/solaire par 8x AA 4S2P + buck TPS62840 comme reference P0.

## Point dur a trancher par JCH

La vraie decision n'est plus "ESP32 ou Pi". Elle est:

**WildNexus P0 est-il un satellite autonome simple, pendant que Base Nexus evolue en parallele, ou veut-on retarder le P0 pour integrer directement Master/Base/Cloud ?**

Avis Dobby/equipe: ne pas retarder le P0. Verrouiller Satellite Lite maintenant, et ouvrir Base Nexus comme P1 prototype.
