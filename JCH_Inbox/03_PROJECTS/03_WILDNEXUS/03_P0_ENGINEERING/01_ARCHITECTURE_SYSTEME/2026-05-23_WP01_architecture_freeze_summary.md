# WildNexus WP01 — Architecture P0 gelee / passage WP02

**Date :** 2026-05-23  
**Statut :** reference de transition M-01 -> WP02  
**Owner :** [[Dobby]] + [[Castor]]  
**Equipe mobilisee :** [[Forge]], [[Chouette]], [[Bruno]], [[Nova]], [[Lynx]], [[Hermine]], [[Renard]]  

## 1. Objet

Ce document consolide WP01 apres les arbitrages JCH du 2026-05-23. Il sert a eviter que WP02 reparte de notes dispersees.

WP01 n'est pas un dossier d'achat. C'est le gel d'architecture qui autorise WP02 a travailler sur le hardware, le boitier, l'encombrement et la shortlist.

## 2. Decision P0 gelee

Le P0 est un **Satellite Lite autonome**.

Composition fonctionnelle :

- [[ESP32-S3]] ;
- camera OV5640/IR + lentille M12 ;
- PIR ;
- micro mono pour clips audio courts locaux ;
- microSD industrielle ;
- [[LoRa]] P2P EU868 pour metadonnees/statuts/commandes courtes ;
- Wi-Fi local pour maintenance et extraction ;
- holder AA + buck faible Iq ;
- bloc capteurs reserve dans l'encombrement ;
- boitier IP67, vert, discret, calage support rond ;
- antenne [[LoRa]] interne ou camouflee en priorite.

Exclusions P0 :

- [[Raspberry Pi]] dans le satellite ;
- [[BirdNET]] embarque ;
- YOLO embarque lourd ;
- cloud obligatoire ;
- mesh [[LoRa]] ;
- flux raw continu ;
- LTE-M actif dans le satellite P0 ;
- boitier imprime 3D IP67 comme exigence P0.

## 3. Architecture cible preservee

WildNexus est structure en trois niveaux :

| Niveau | Statut | Role |
|---|---|---|
| Satellite Lite | P0 | capter, stocker, survivre dehors, transmettre seulement alertes/metadonnees |
| Base/Master Nexus | P1 parallele | [[Raspberry Pi 5]], SSD, BirdNET-Go, YOLO, indexation, orchestration locale |
| Cloud | P1/P2 | [[archive]] selective, acces distant, partage controle |

Decision cle : le Satellite Lite P0 doit rester utile sans Base/Master et sans cloud.

## 4. ADR et statut

| ADR | Sujet | Statut WP01 |
|---|---|---|
| ADR-001 | MCU [[ESP32-S3]] | accepte |
| ADR-002 | camera OV5640/IR | accepte |
| ADR-003 | [[LoRa]] P2P EU868 | accepte |
| ADR-004 | stockage local microSD | accepte |
| ADR-005 | energie AA + buck | accepte |
| ADR-006 | boitier IP67 / terrain | propose, non bloquant WP02 |
| ADR-007 | detection evenementielle | accepte |
| ADR-008 | interface capteurs extensible | accepte |
| ADR-009 | architecture Satellite/Base/Cloud | accepte |

ADR-006 reste propose volontairement : le modele exact du boitier depend du choix hardware, de la batterie 4 AA vs 8 AA, de l'antenne [[LoRa]] et de l'encombrement capteurs.

## 5. Decisions critiques prises

### 5.1 Batterie

Reference actuelle : 8x AA 4S2P.

Mais WP02/M-02 doit tester 4x AA comme variante compacte. Le modele autonomie `WildNexus_P0_Autonomy_Model.xlsx` devient l'outil de comparaison theorique, puis les mesures banc trancheront.

Regle :

- 8 AA = enveloppe mecanique prudente ;
- 4 AA = variante compacte a prouver ;
- pas de LiPo/LiFePO4/BMS/solaire en P0.

### 5.2 Micro

Le micro mono est integre au P0 pour capture locale de clips courts. Il ne transforme pas P0 en station bioacoustique.

[[BirdNET]], reconnaissance espece et DSP avance restent P1 via Base/Master Nexus.

### 5.3 Capteurs

Le P0 doit reserver l'encombrement et l'interface pour un petit bloc capteurs. Les capteurs type BME688/AS7341/GPS ne doivent pas forcer la complexite fonctionnelle du premier prototype, mais le boitier/PCB doivent les anticiper.

### 5.4 Boitier

P0 utilise probablement un boitier commerce IP67 pour aller vite. P1 pourra exploiter l'imprimante 3D JCH pour forme bio, skin camouflage, texture tronc/pierre et boitier plus organique.

Le boitier P0 doit deja anticiper :

- couleur verte ;
- silhouette moins detectable qu'une camera de chasse classique ;
- calage sur supports ronds ;
- sangle discrete ;
- antenne [[LoRa]] interne ou camouflee ;
- reserve skin camouflage.

### 5.5 [[Raspberry Pi]]

Le [[Raspberry Pi 5]] doit etre considere maintenant pour Base/Master Nexus P1. Il est exclu du satellite P0.

## 6. WP01 — livrables couverts

| Livrable WP01 | Statut | Reference |
|---|---|---|
| D01.1 comparaison/concurrence | partiel/historique | notes marche et produits dans `03_P0_ENGINEERING` |
| D01.2 FTO / licence / usage | ouvert | 
| D01.3 RF / standard radio | accepte architecture | ADR-003 ; mesures terrain restent WP05/M-02 |
| D01.4 camera | accepte architecture | ADR-002 ; benchmark terrain reste M-02 |
| D01.5 architecture P0 gelee | produit | ce document + ADR index |
| SUPPLY-01 registre composants | actif | `WILDNEXUS_SUPPLY_REGISTER.md` |

WP01 est donc suffisamment ferme pour autoriser WP02, avec deux reserves explicites :

1. FTO/licence reste a traiter comme risque juridique, pas comme blocage hardware immediat.
2. ADR-006 reste ouvert jusqu'a estimation dimensionnelle et choix boitier.

## 7. Anticipation WP02

WP02 doit produire rapidement :

1. shortlist achat v0.1 ;
2. estimation encombrement v0.2 ;
3. comparaison 4 AA vs 8 AA avec le modele autonomie ;
4. choix de 1-2 boitiers candidats ;
5. [[strategie]] antenne [[LoRa]] discrete ;
6. architecture PCB v0.1 ;
7. liste des mesures M-02 au PPK2.

Deux options a suivre en parallele :

| Option | But | Contenu |
|---|---|---|
| A — banc rapide | mesurer vite | DevKit [[ESP32-S3]], module camera, [[LoRa]] dev/breakout, PIR, micro, microSD, buck, batteries |
| B — proto terrain compact | converger boitier | composants proches PCB final, holder AA, boitier IP67, antenne discrete, fenetres camera/PIR/micro |

## 8. Anticipation WP03

WP03 doit demarrer sans attendre le PCB final sur dev board :

- machine d'etats sleep -> wake -> capture -> stockage -> [[LoRa]] -> sleep ;
- power gating camera/microSD/IR/[[LoRa]] ;
- gestion undervoltage ;
- logs energie par evenement ;
- configuration Wi-Fi locale minimale ;
- format metadata extensible.

WP03 ne doit pas demarrer [[BirdNET]]/YOLO embarque.

## 9. Anticipation WP04

WP04 se limite pour P0 a :

- prefiltrage animal/non-animal ;
- seuils simples ;
- preparation dataset a partir des captures P0 ;
- comparaison offline future via Base/Master.

Pas de reconnaissance espece fine dans le satellite P0.

## 10. Passage recommande

Decision [[Dobby]]/equipe :

**WP01 peut etre considere comme suffisamment gelee pour lancer WP02/WP03/WP04 en parallele controle.**

Condition de discipline :

- aucune nouvelle fonction P0 sans ADR ou decision JCH ;
- tout ajout doit passer par le modele autonomie et l'encombrement ;
- ADR-006 ne sera acceptee qu'apres shortlist hardware et estimation dimensionnelle.

## 11. Prochaine action

Produire `WP02_shortlist_achat_P0_v0.1` :

- composants exacts ;
- fournisseur primaire et alternative ;
- prix livre Belgique ;
- delai ;
- risque supply ;
- impact encombrement ;
- indication banc rapide vs proto terrain.
