---
title: "WildNexus — Dossier ADR imprimable"
subtitle: "ADR-001 MCU · ADR-002 Camera/IR · ADR-003 Radio/LPWAN"
date: "2026-05-18"
lang: fr
geometry: margin=18mm
fontsize: 10pt
---

# WildNexus — Dossier ADR imprimable

**Objet :** support papier pour relire, annoter et arbitrer les trois decisions techniques prioritaires avant `M-01 Architecture P0 gelee`.

**Statut global :** propositions de travail, non acceptees.  
**Jalon cible :** `M-01` — choix suffisamment solides pour autoriser `M-02 Prototype banc fonctionnel`.  
**Principe directeur :** P0 prouve un noeud camera autonome. P1/P2 restent preserves, mais ne doivent pas entrer dans le prototype P0.

## Synthese decisionnelle

| ADR | Sujet | Proposition | Point de vigilance | Decision papier |
|---|---|---|---|---|
| ADR-001 | MCU P0 | ESP32-S3 candidat primaire ; STM32U5 fallback energie | autonomie 60 jours a prouver, pas supposer | [ ] accepter [ ] modifier [ ] rejeter |
| ADR-002 | Camera / IR | benchmark en deux pistes : SPI MCU-native + reference IMX462/IMX327 | ne pas choisir un capteur qui force Linux ou USB lourd | [ ] accepter [ ] modifier [ ] rejeter |
| ADR-003 | Radio / LPWAN | LoRa EU868 evenementiel ; SX1262 comme reference ; Murata 1SJ ou RAK3172(H) | portee foret belge et duty-cycle EU868 | [ ] accepter [ ] modifier [ ] rejeter |

## Questions a trancher sur papier

1. Le risque energie ESP32-S3 est-il acceptable si mesure avant gel definitif ?
2. Le P0 doit-il privilegier une camera facile a integrer ou une qualite nocturne maximale ?
3. Le premier terrain EVT aura-t-il une gateway proche ou doit-il rester strictement point-a-point ?
4. La distance image nuit cible 5 m est-elle un minimum non negociable ?
5. Quel niveau de depense est acceptable pour acheter 2 ou 3 modules concurrents par domaine ?

\newpage

# ADR-001 — Choix MCU P0

**Owner PKA :** Castor + Forge  
**Agent WildNexus :** `wildnexus-firmware-ulp`  
**Statut :** propose  

## Contexte court

P0 doit prouver un noeud camera autonome : veille basse consommation, reveil evenementiel, capture image, filtre animal / non-animal, stockage local, configuration terrain simple et transmission LPWAN evenementielle.

Le P0 ne doit pas dependre d'un Raspberry Pi ou d'un Linux permanent.

## Decision proposee

Retenir **ESP32-S3 comme MCU candidat primaire pour le prototype P0 M-02**, avec une regle de sortie stricte :

- ESP32-S3 reste le choix P0 si le budget energie complet demontre l'objectif de 60 jours batterie seule ;
- STM32U5 reste le fallback basse consommation si ESP32-S3 echoue sur autonomie, stabilite veille/reveil ou robustesse firmware ;
- nRF54L15 reste une option BLE / 2.4 GHz future, non prioritaire P0.

## Comparaison

| Option | Pour | Contre | Statut propose |
|---|---|---|---|
| ESP32-S3 | camera, BLE/Wi-Fi, USB, SPI/I2C/UART, ULP, secure boot, ecosysteme rapide | consommation a prouver ; Wi-Fi a eteindre ; PSRAM probable | candidat primaire |
| STM32U5 | tres basse consommation, securite, trajectoire produit robuste | integration camera plus exigeante ; prototypage plus lent | fallback energie |
| nRF54L15 | BLE basse consommation, securite, coprocesseur RISC-V | radio 2.4 GHz seulement ; ne remplace pas LPWAN ; camera moins directe | option future |
| Raspberry Pi | camera et logiciel faciles | consommation, boot, SD, maintenance, autonomie incompatibles P0 | rejete P0 |

## Tests d'acceptation

| Test | Critere minimal | Resultat terrain/banc |
|---|---|---|
| Courant deep sleep carte complete | compatible 60 jours batterie seule |  |
| Reveil -> capture -> stockage -> sommeil | stable sur 1 000 cycles banc |  |
| Capture image utilisable | exploitable a 5 m jour/nuit |  |
| Transmission LPWAN courte | paquet envoye puis retour sommeil |  |
| Provisioning terrain | configuration sans ordinateur portable |  |

## Notes manuscrites

\vspace{32mm}

## Decision ADR-001

[ ] Accepter tel quel  
[ ] Accepter avec modifications  
[ ] Rejeter  

Modifications demandees :

\vspace{28mm}

\newpage

# ADR-002 — Choix camera / IR P0

**Owner PKA :** Nova + Lynx  
**Agent WildNexus :** `wildnexus-camera-imaging`  
**Statut :** propose  

## Contexte court

P0 doit produire une image exploitable de jour et de nuit sans transformer le noeud en architecture Linux permanente.

Les capteurs Sony STARVIS IMX462 / IMX327 sont pertinents pour la basse lumiere, mais les modules courants sont souvent USB ou MIPI, donc plus lourds a integrer dans un noeud MCU basse consommation.

## Decision proposee

Lancer un **benchmark camera en deux pistes** avant gel definitif :

- **Piste A — integration MCU prioritaire :** Arducam Mega SPI 5MP NoIR/M12 ou equivalent SPI ;
- **Piste B — reference basse lumiere :** IMX462 day/night ou IMX327 MIPI comme reference qualite nocturne, sans acceptation automatique comme choix P0.

Le choix P0 doit maximiser le couple **image exploitable / energie / simplicite d'integration**.

## Comparaison

| Option | Pour | Contre | Statut propose |
|---|---|---|---|
| Arducam Mega SPI 5MP NoIR/M12 | SPI compatible MCU, SDK ouvert, peu de broches, prototype rapide | vision nocturne a verifier ; IR externe ; qualite wildlife inconnue | candidat primaire benchmark |
| IMX462 USB day/night | excellent basse lumiere / NIR, modules disponibles, IR-cut/LED IR possibles | USB plus lourd ; risque Linux/host USB ; portee nuit parfois courte | reference qualite |
| IMX327 MIPI avec ISP | STARVIS, bonne basse lumiere, MIPI CSI, IR-cut possible | MIPI/ISP lourd ; integration MCU difficile ; conso module | reference/fallback host dedie |
| ESP32-CAM OV2640 | simple, bon marche | qualite nocturne probablement insuffisante | baseline seulement |

## Tests d'acceptation

| Test | Critere minimal | Resultat terrain/banc |
|---|---|---|
| Image jour a 5 m | sujet animal ou mire naturaliste exploitable |  |
| Image nuit IR a 5 m | presence animal / non-animal validable |  |
| Reveil -> capture -> stockage | stable et sous budget energie |  |
| Extinction camera | consommation residuelle negligeable |  |
| Montage boitier | fenetre + IR alignables, pas de reflets dominants |  |

## Notes manuscrites

\vspace{32mm}

## Decision ADR-002

[ ] Accepter tel quel  
[ ] Accepter avec modifications  
[ ] Rejeter  

Modifications demandees :

\vspace{28mm}

\newpage

# ADR-003 — Choix radio / LPWAN P0

**Owner PKA :** Forge + Chouette  
**Agent WildNexus :** `wildnexus-rf-propagation`  
**Statut :** propose  

## Contexte court

P0 transmet des evenements, metadonnees et etats de sante. Il ne transmet pas d'images completes.

Le mesh LoRa est rejete pour P0 : collisions, duty-cycle EU868, latence, temps d'air et consommation de relayage.

## Decision proposee

Retenir **LoRa EU868 evenementiel point-a-point ou LoRaWAN prive leger** comme candidat radio P0, avec **SX1262 comme reference technique** et module certifie pour prototypage.

Choix recommande M-02 :

- module **Murata Type 1SJ** ou **RAK3172(H)** ;
- abstraction firmware radio via UART/SPI ;
- aucun mesh P0 ;
- aucun transfert massif d'image ;
- campagne RF terrain avant acceptation M-01.

## Comparaison

| Option | Pour | Contre | Statut propose |
|---|---|---|---|
| LoRa EU868 SX1262 certifie | basse conso, longue portee, petits paquets, modules disponibles | duty-cycle, faible debit, antenne critique, pas d'image | candidat primaire |
| LoRaWAN prive leger | standard, gateways, trajectoire P1 | serveur/gateway, complexite | option si gateway disponible |
| LoRa mesh | resilience apparente, heritage WildMesh | collisions, duty-cycle, latence, relayage energivore | rejete P0 |
| BLE longue portee | provisioning utile, faible energie | portee foret insuffisante pour alertes | provisioning seulement |
| LTE-M / NB-IoT | cloud direct, sites distants | abonnement, conso, couverture variable | P1/P2 ou sites critiques |

## Tests d'acceptation

| Test | Critere minimal | Resultat terrain/banc |
|---|---|---|
| Portee terrain foret | RSSI/SNR a plusieurs distances et positions |  |
| Paquet evenement | paquet court transmis apres reveil |  |
| Retour sommeil | radio eteinte ou basse conso validee |  |
| Duty-cycle EU868 | calcul documente pour scenario EVT |  |
| Antenne en boitier | perte acceptable avec montage IP67 |  |

## Notes manuscrites

\vspace{32mm}

## Decision ADR-003

[ ] Accepter tel quel  
[ ] Accepter avec modifications  
[ ] Rejeter  

Modifications demandees :

\vspace{28mm}

\newpage

# Page de synthese — decisions et achats de test

## Decisions finales

| ADR | Decision | Conditions | Owner |
|---|---|---|---|
| ADR-001 MCU |  |  | Castor + Forge |
| ADR-002 Camera/IR |  |  | Nova + Lynx |
| ADR-003 Radio/LPWAN |  |  | Forge + Chouette |

## Achats ou prets a organiser pour benchmark

| Domaine | Item | Quantite | Fournisseur pressenti | Priorite |
|---|---|---:|---|---|
| MCU | ESP32-S3 dev board avec PSRAM |  |  | haute |
| MCU | STM32U5 dev board |  |  | moyenne |
| Camera | Arducam Mega SPI 5MP NoIR/M12 ou equivalent |  |  | haute |
| Camera | IMX462 day/night reference |  |  | moyenne |
| Camera | IMX327 MIPI/ISP reference |  |  | basse/moyenne |
| Radio | Murata Type 1SJ evaluation/module |  |  | haute |
| Radio | RAK3172(H) EU868 |  |  | haute |
| Terrain | Antennes EU868 candidates |  |  | haute |

## Feu vert JCH

[ ] Autoriser benchmark banc minimal  
[ ] Demander revision avant achat  
[ ] Suspendre M-01  

Notes :

\vspace{40mm}

# Sources

- ADR-001 : `../02_DECISIONS/ADR/ADR-001-choix-mcu-p0.md`
- ADR-002 : `../02_DECISIONS/ADR/ADR-002-choix-camera-ir-p0.md`
- ADR-003 : `../02_DECISIONS/ADR/ADR-003-choix-radio-lpwan-p0.md`
- Index : `../02_DECISIONS/WILDNEXUS_ADR_INDEX.md`
