# WildNexus - Resume de chat hardware, architecture et choix strategiques

**Date :** 2026-05-22  
**Auteur :** [[Dobby]]  
**Objet :** synthese lisible de la discussion recente sur WildNexus, les capteurs, l'architecture satellite/base, les alternatives a [[ESP32]], et l'ouverture vers les producteurs chinois.  

## 1. Le point de depart

Tu es revenu avec une nouvelle masse d'informations issue de documents, de discussions avec des experts, d'observations marche et de contenus autour de [[BirdNET]], [[ESP32]], BirdWeather et des usages terrain.

Le message principal etait clair : **il ne fallait pas proteger l'ancien setup WildNexus par habitude**. Il fallait accepter de revoir les positions fondamentales si les nouvelles donnees montraient que le projet devait changer.

La conclusion de [[Dobby]] est que WildNexus ne doit plus etre pense comme un simple piege photo ameliore. Il doit etre pense comme une **machine d'observation ecologique multimodale**, capable de combiner :

- image ;
- video ;
- son ;
- capteurs environnementaux ;
- detection d'evenements ;
- analyse locale ou semi-locale ;
- transmission intelligente des resultats ou donnees lourdes.

Cela change profondement le choix hardware.

## 2. Pivot conceptuel propose

L'ancien projet pouvait encore etre lu comme :

> Un boitier terrain avec camera, puis peut-etre quelques extensions.

Le nouveau WildNexus doit plutot etre lu comme :

> Un reseau modulaire d'observation, avec des noeuds discrets qui captent les signaux du vivant, et une intelligence locale ou proche terrain qui decide ce qui merite d'etre stocke, transmis ou analyse.

Ce pivot ne supprime pas la camera. Il la replace dans un systeme plus large.

### Avant / apres

| Sujet | Vision ancienne | Vision recommandee |
|---|---|---|
| Produit | Piege photo intelligent | Reseau multimodal d'observation ecologique |
| Unité centrale | Un boitier principal | Satellites + eventuelle base locale |
| Donnees | Photo/video surtout | Photo, video, audio, meteo, evenement, contexte |
| IA | Eventuellement dans le boitier | Repartie selon energie, cout et role |
| Transmission | Envoyer ce qu'on capture | Envoyer intelligemment : alerte, metadata, extraits, donnees lourdes a la demande |
| Hardware | Chercher une carte miracle | Associer plusieurs classes de cartes selon role |

## 3. BirdWeather et concurrence

Tu as demande si BirdWeather avait deja ete vu. La reponse est nuancee :

- BirdWeather avait ete croise dans des notes bioacoustiques / Faune Autour.
- Mais il ne semblait pas avoir ete correctement integre a l'analyse concurrentielle WildNexus.

Donc ton intuition etait correcte : **BirdWeather devait etre reconsidere comme un signal marche important**.

### Pourquoi BirdWeather est interessant

BirdWeather montre qu'il existe un public pour :

- un objet terrain dedie a l'ecoute des oiseaux ;
- une integration avec [[BirdNET]] ;
- une contribution vers une plateforme cloud ;
- une experience utilisateur simple ;
- des donnees audio naturalistes automatisees.

### Pourquoi BirdWeather ne ferme pas la porte a WildNexus

BirdWeather reste surtout centre sur la bioacoustique. WildNexus peut se differencier par :

- multimodalite image + audio + environnement ;
- architecture satellite/base ;
- usage terrain plus discret ;
- controle local des donnees ;
- fonctionnement possible sans cloud permanent ;
- logique d'evenements croises : son + mouvement + image + contexte.

## 4. Le probleme [[ESP32]]

Ton inquietude principale est juste : **[[ESP32]] ne tient pas la route comme cerveau principal WildNexus** si WildNexus devient une machine multimodale serieuse.

[[ESP32]] reste utile, mais pas comme coeur du produit final.

### [[ESP32]] : ce qu'il peut faire

| Usage | Pertinence |
|---|---|
| Prototype rapide | Bonne |
| Capteurs simples | Bonne |
| [[LoRa]] / Wi-Fi / BLE | Bonne |
| Camera basique | Possible mais limite |
| TinyML tres leger | Possible |
| Controle d'energie simple | Possible |

### [[ESP32]] : ce qu'il ne doit pas porter

| Usage | Probleme |
|---|---|
| [[BirdNET]] complet | Compute/RAM insuffisants |
| Vision IA serieuse | Trop limite |
| Multimodalite lourde | Pas assez robuste |
| Produit industriel ambitieux | Trop fragile comme coeur unique |
| Audio + image + decision locale avancee | Mauvais fit |

Verdict : **garder [[ESP32]] comme outil de prototype ou sous-module, mais ne plus le mettre au centre de WildNexus.**

## 5. Trois architectures discutees

Tu as formule trois pistes :

1. Tout a bord : IA, stockage, decision et transmission dans chaque boitier.
2. Capture locale + notification : le boitier signale, puis l'utilisateur demande le telechargement.
3. Satellites + base : petits satellites discrets captent l'information, envoient evenement ou donnees a une base locale cachee, et la base fait l'IA lourde et la transmission.

La troisieme piste est la plus interessante.

### Comparatif des architectures

| Architecture | Principe | Avantages | Faiblesses | Verdict |
|---|---|---|---|---|
| Tout a bord | Chaque noeud fait tout : capture, IA, stockage, 4G/5G | Autonome, simple conceptuellement | Cher, visible, gourmand, difficile a fiabiliser | A reserver a version premium |
| Capture + demande | Le noeud stocke, signale, et envoie seulement si demande | Economise data et energie | Experience utilisateur plus lente, depend stockage local | Bon mode operationnel |
| Satellites + base | Petits capteurs discrets + base locale puissante | Discretion, modularite, IA locale, moins de 4G par noeud | Plus complexe, reseau local a concevoir | Architecture la plus prometteuse |

## 6. Pourquoi la logique satellite/base a du potentiel

La recherche marche a montre que le schema satellite/base n'est pas une fantaisie. On le retrouve dans plusieurs secteurs :

- cameras de chasse en reseau ;
- surveillance de sites ;
- IoT industriel ;
- capteurs environnementaux ;
- defense / surveillance perimeter ;
- bioacoustique distribuee ;
- stations terrain avec passerelle.

L'idee est robuste : **des capteurs petits et discrets autour d'une base plus puissante, mieux cachee, mieux alimentee et mieux connectee.**

Pour WildNexus, cela peut donner :

- satellites moins chers ;
- satellites plus discrets ;
- moins de cartes SIM ;
- une IA plus puissante dans la base ;
- plus de stockage fiable ;
- meilleure autonomie terrain ;
- possibilite de separer les roles : son, image, meteo, presence, etc.

## 7. Architecture WildNexus recommandee

[[Dobby]] recommande une architecture a trois niveaux.

| Niveau | Role | Exemple hardware |
|---|---|---|
| Satellite Lite | veille, capteurs, PIR, audio leger, [[LoRa]], stockage simple | STM32U5, Apollo510 |
| Satellite Smart | camera, audio plus riche, detection locale, prefiltrage IA | STM32N6, Rockchip RV1106, Axera AX630C |
| Base Nexus | stockage lourd, IA locale, [[BirdNET]], orchestration, 4G/5G, dashboard | [[Raspberry Pi 5]], RK3588, NXP i.MX 8M Plus |

Cette architecture evite l'erreur classique : vouloir qu'un seul boitier fasse tout.

## 8. Capteurs embarques possibles

Tu as demande de finaliser une liste de capteurs embarques possibles, parce que cela affecte directement l'architecture.

La conclusion importante : **il ne faut pas mettre tous les capteurs dans tous les boitiers**. Il faut definir des profils.

### Capteurs de base recommandables

| Capteur | Role | Priorite | Commentaire |
|---|---|---:|---|
| Camera visible/IR | Identification, photo, video, preuve | Haute | Coeur du satellite camera |
| PIR | Detection mouvement basse conso | Haute | Declencheur simple et efficace |
| Micro audible | Oiseaux, mammiferes, contexte sonore | Haute selon version | Important pour multimodalite |
| Temperature / humidite | Contexte ecologique et diagnostic boitier | Haute | Peu couteux, utile |
| Mesure batterie | Energie, maintenance, prediction autonomie | Haute | Obligatoire |
| RTC | Horodatage fiable | Haute | Obligatoire terrain |
| Carte SD ou eMMC | Stockage local | Haute | SD pour proto, eMMC preferable si industrialise |
| [[LoRa]] | Alerte et metadata | Haute si satellites | Pas pour audio/video lourd |
| 4G/5G | Backhaul | Haute pour base, option satellite premium | Cher en energie et abonnement |

### Capteurs optionnels

| Capteur | Role | Quand l'utiliser |
|---|---|---|
| GNSS | Position et temps precis | Sur base ou satellites mobiles, pas forcement partout |
| Lux / UV | Contexte lumiere | Utile pour interpretation camera |
| Pression | Meteo locale | Si orientation scientifique |
| IMU | Orientation, choc, vol, mouvement du boitier | Bon pour diagnostic |
| mmWave radar | Presence sans image, detection fine | A tester, pas baseline |
| Micro ultrason | Chauves-souris | Module specialise |
| Capteur sol/eau | Humidite sol, niveau eau, temperature eau | Module habitat specifique |
| Camera thermique | Detection nuit / mammiferes | Premium, couteux |

## 9. Hardware non chinois : conclusions

Voici le resume des plateformes occidentales ou classiques et leur role possible.

| Plateforme | Role WildNexus | Verdict |
|---|---|---|
| STM32U5 | Satellite Lite basse consommation | Tres bon choix industriel pour capteurs/veille |
| Ambiq Apollo510 | Satellite Lite audio/IA ultra basse conso | Tres interessant pour always-on audio, ecosysteme plus niche |
| STM32N6 | Satellite Smart avec camera + NPU | Candidat prioritaire hors Chine |
| [[Raspberry Pi 5]] | Base prototype, apprentissage, BirdNET-Go | Excellent pour demarrer, pas satellite autonome |
| [[Raspberry Pi]] AI HAT+ | Acceleration IA sur base prototype | Tres bon banc vision |
| [[Raspberry Pi]] AI Camera | Test in-sensor AI | Pedagogique, pas baseline terrain |
| NXP i.MX 8M Plus | Base industrielle | Robuste et credible, plus cher |
| Quectel EG916Q | 4G Cat 1 bis | Bon module backhaul base/smart |
| Nordic nRF9161 | LTE-M/NB-IoT metadata | Utile pour telemetrie, pas medias lourds |
| Sony Spresense | Banc audio/GNSS/camera | Interessant pour apprendre, supply a verifier |

## 10. Extension Chine : pourquoi c'est important

Tu as precise que tu as des activites economiques en Chine et que tu peux y acceder si quelque chose est vraiment interessant. Cela change l'analyse.

La Chine est particulierement forte sur :

- SoC camera low-cost ;
- modules IA vision ;
- SBC puissants a prix agressif ;
- supply industrielle en volume ;
- modules 4G/5G ;
- ecosystemes maker qui permettent d'apprendre vite.

Mais il y a des risques :

- SDK parfois fragile ;
- documentation incomplete ;
- kernels Linux vendor ;
- cycle de vie produit incertain ;
- support fournisseur variable ;
- certification et securite a verifier ;
- differencier board maker, module industriel et composant final.

### Plateformes chinoises interessantes

| Plateforme | Producteur / ecosysteme | Role possible | Verdict |
|---|---|---|---|
| Rockchip RV1106 / RV1103 | Rockchip, Luckfox, Waveshare | Satellite Camera Smart low-cost | A tester en priorite |
| Rockchip RK3588 / RK3588S | Rockchip, Orange [[Pi]], Radxa, Firefly | Base Nexus puissante | Tres bon challenger [[Raspberry Pi]] |
| Axera AX630C | Axera, Sipeed MaixCAM2 | Camera IA compacte | Tres prometteur, maturite a valider |
| Axera AX650N | Axera | Vision premium / surveillance | Potentiel si acces fournisseur direct |
| Sophgo SG2002 / SG2000 | Sophgo, Milk-V, Sipeed | Apprentissage IA vision low-cost | Excellent pour R&D |
| Kendryte K230 | Canaan Kendryte | Banc vision/multi-camera RISC-V | Bon outil de test |
| Allwinner V853 | Allwinner | Camera economique avec NPU/ISP | A auditer |
| GigaDevice GD32H7 | GigaDevice | Alternative MCU STM32-like | Supply utile, pas IA lourde |
| Quectel / Fibocom / SIMCom | Modules cellulaires | Backhaul 4G/5G/NB-IoT | Strategique |

## 11. Decision provisoire sur les familles hardware

La conclusion n'est pas "choisir Chine" ou "choisir Europe/US". La conclusion est de separer les lots d'evaluation.

### Lot A - Industriel classique

| Composant | Pourquoi le tester |
|---|---|
| STM32U5 | Satellite Lite sobre |
| Apollo510 | Audio always-on basse conso |
| STM32N6 | Satellite Smart avec NPU |
| [[Raspberry Pi 5]] | Base prototype rapide |
| NXP i.MX 8M Plus | Base industrielle robuste |

### Lot B - Chine offensive

| Composant | Pourquoi le tester |
|---|---|
| Rockchip RV1106 | Camera IA low-cost terrain |
| Rockchip RK3588 | Base locale IA puissante |
| Axera AX630C | Camera IA compacte plus ambitieuse |
| Sophgo SG2002 | Apprentissage et prototypage low-cost |
| Kendryte K230 | Vision/multi-camera R&D |

## 12. Decisions techniques importantes

### [[LoRa]]

[[LoRa]] est utile pour :

- alerte ;
- metadata ;
- etat batterie ;
- commande courte ;
- signalement d'evenement.

[[LoRa]] n'est pas fait pour :

- audio brut ;
- photo lourde ;
- video ;
- transfert massif.

Donc [[LoRa]] doit etre vu comme le reseau nerveux du systeme, pas comme son canal media principal.

### 4G/5G

La 4G/5G doit etre concentree de preference sur :

- la base ;
- quelques satellites smart premium ;
- les moments ou il faut vraiment remonter de la donnee lourde.

Mettre une SIM dans chaque petit satellite augmente vite :

- cout ;
- consommation ;
- complexite antenne ;
- abonnement ;
- certification ;
- maintenance.

### Stockage

La carte SD est acceptable pour apprendre et prototyper. Pour une version terrain serieuse, il faudra regarder :

- eMMC ;
- SSD sur base ;
- endurance ;
- corruption apres coupure ;
- cycles d'ecriture ;
- chiffrement eventuel ;
- journalisation.

## 13. Risques a ne pas oublier

| Risque | Pourquoi c'est important | Action recommandee |
|---|---|---|
| Mauvais choix du cerveau satellite | Peut bloquer tout le produit | Tester STM32U5, STM32N6, RV1106 et Apollo510 separement |
| Sous-estimation de l'energie | Terrain = batterie, froid, humidite | Mesurer consommation reelle, pas seulement datasheet |
| Trop de media a transmettre | Audio/video coutent cher en data | Envoyer metadata et extraits, telechargement a la demande |
| IA trop lourde dans chaque noeud | Cout, energie, chaleur | Mettre l'IA lourde dans la base |
| Mauvais stockage | Perte de donnees, corruption | Tester SD/eMMC/SSD selon role |
| SDK chinois fragile | Prototypage rapide mais produit instable | Audit logiciel avant choix final |
| Camera low-light insuffisante | Usage nature surtout nuit/aube | Tester capteurs reels, IR, optique, exposition |
| Boitier mal pense | Condensation, son etanche, chaleur | Prototyper mecanique tot |
| Confusion entre prototype et produit | Une board maker peut tromper | Distinguer devkit, SOM et design final |

## 14. Ce qui est interessant

Les idees vraiment interessantes sorties du chat :

- La structure satellite/base est probablement plus forte qu'un boitier unique.
- [[ESP32]] doit etre declasse, pas abandonne.
- BirdWeather valide un segment bioacoustique mais ne couvre pas toute l'ambition WildNexus.
- [[LoRa]] est excellent pour l'alerte, mauvais pour les medias.
- STM32U5 est solide pour le satellite sobre.
- STM32N6 est le candidat occidental le plus interessant pour satellite smart.
- Apollo510 merite une evaluation audio/always-on.
- [[Raspberry Pi 5]] est le meilleur outil d'apprentissage/base prototype.
- NXP i.MX 8M Plus est credible pour une base industrielle.
- Rockchip RV1106 pourrait etre un vrai choc positif pour camera IA low-cost.
- RK3588 peut challenger [[Raspberry Pi 5]] pour la base.
- Axera est une piste Chine a ouvrir serieusement.

## 15. Ce qui est moins interessant ou dangereux

| Idee | Probleme |
|---|---|
| Tout faire sur [[ESP32]] | Trop limite pour WildNexus reel |
| Mettre [[BirdNET]] complet dans chaque satellite | Trop lourd pour petits MCU |
| Envoyer toutes les videos par [[LoRa]] | Techniquement incoherent |
| Mettre 4G partout | Cout/energie/maintenance explosent |
| Acheter toutes les cartes possibles | Dispersion |
| Choisir seulement sur les TOPS | Les TOPS ne disent rien de l'ecosysteme camera/audio/SDK |
| Confondre board maker et produit industriel | Gros risque d'industrialisation |
| Ne regarder que les composants occidentaux | On raterait des options camera IA chinoises tres pertinentes |

## 16. Plan de demarche propose

### Phase 1 - Apprentissage rapide

Acheter ou reunir peu de plateformes, mais bien choisies :

1. [[Raspberry Pi 5]] + SSD : base prototype, BirdNET-Go, stockage, dashboard.
2. STM32U5 devkit : satellite sobre.
3. STM32N6 devkit + camera : satellite smart occidental.
4. Rockchip RV1106 board : satellite camera Chine low-cost.
5. RK3588 board : base Chine alternative.

### Phase 2 - Mesures reelles

Pour chaque plateforme, mesurer :

- consommation veille ;
- consommation capture ;
- temps de reveil ;
- qualite image de jour ;
- qualite image nuit/IR ;
- audio utile ;
- stockage ;
- temperature ;
- stabilite logiciel ;
- conversion de modele IA ;
- facilite de developpement.

### Phase 3 - Architecture figée

Une fois les mesures reelles faites, figer :

- role exact du Satellite Lite ;
- role exact du Satellite Smart ;
- role exact de la Base Nexus ;
- protocole [[LoRa]] ;
- [[strategie]] 4G/5G ;
- capteurs baseline ;
- capteurs optionnels ;
- boitier ;
- cout cible.

## 17. Recommandation finale [[Dobby]]

Ne pas chercher le "cerveau unique" de WildNexus.

La bonne orientation est :

> un systeme modulaire, avec satellites sobres, satellites camera intelligents, et base locale capable de porter l'IA lourde.

Le choix le plus prudent serait :

- **STM32U5** pour Satellite Lite ;
- **STM32N6** comme candidat occidental Satellite Smart ;
- **Rockchip RV1106** comme challenger Chine Satellite Smart ;
- **[[Raspberry Pi 5]]** pour apprendre et prototyper la Base Nexus ;
- **RK3588** comme challenger Chine Base Nexus ;
- **NXP i.MX 8M Plus** comme option base industrielle robuste.

Le point de vigilance majeur : **ne pas se faire hypnotiser par les fiches techniques**. Pour WildNexus, les vraies questions sont energie, camera de nuit, stockage, robustesse terrain, SDK, cout en volume, et simplicite de maintenance.

## 18. Fichiers produits pendant cette sequence

| Fichier | Contenu |
|---|---|
| `2026-05-22_dobby_wildnexus-multimodal-reset.md` | Redefinition de WildNexus comme machine multimodale |
| `2026-05-22_dobby_wildnexus-satellite-base-market-scan.md` | Analyse marche de la logique satellite/base |
| 
| `2026-05-22_dobby_wildnexus-onboard-sensor-matrix.md` | Matrice des capteurs embarques possibles |
| `2026-05-22_dobby_wildnexus-hardware-chine-norton-safe.md` | Extension Chine du comparatif hardware, sans URL brutes |

