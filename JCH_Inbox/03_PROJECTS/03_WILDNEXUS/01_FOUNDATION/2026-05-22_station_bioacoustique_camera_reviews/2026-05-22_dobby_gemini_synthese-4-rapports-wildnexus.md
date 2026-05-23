# Synthèse comparative — 4 rapports WildNexus du 22 mai 2026

**Date :** 2026-05-22 (après 22h)  
**Auteur :** Dobby 🦉  
**Objet :** comparaison, convergence et différenciation des 4 rapports d'analyse émis ce soir  
**Rapports analysés :**

| # | Fichier | Objet |
|---|---|---|
| R1 | `2026-05-22_dobby_wildnexus-multimodal-reset.md` | Redéfinition conceptuelle : WildNexus comme machine multimodale |
| R2 | `2026-05-22_dobby_wildnexus-hardware-architecture-study.md` | Étude critique hardware : choix plateformes satellite/base |
| R3 | `2026-05-22_dobby_wildnexus-onboard-sensor-matrix.md` | Matrice des capteurs embarqués par profil |
| R4 | `2026-05-22_dobby_wildnexus-satellite-base-market-scan.md` | Scan marché : validité du modèle satellite/base |
| R5 | `2026-05-22_dobby_wildnexus-hardware-chine-norton-safe.md` | Extension : alternatives chinoises (Rockchip, Axera, Sophgo…) |

*R5 est une extension de R2, incluse pour exhaustivité.*

---

## 1. Tableau synoptique des 4 rapports

| Dimension | R1 – Multimodal Reset | R2 – Hardware Architecture | R3 – Sensor Matrix | R4 – Market Scan |
|---|---|---|---|---|
| **Question centrale** | WildNexus est-il un piège photo amélioré ou une machine multimodale ? | Quelle intelligence vit dans le satellite, laquelle dans la base ? | Quels capteurs justifient leur impact énergie/coût/stockage ? | Le modèle satellite/base a-t-il un potentiel utilisateur réel ? |
| **Verdict** | Machine d'observation écologique multimodale. La caméra est la 1ʳᵉ modalité, pas la seule. | Architecture 3 niveaux : Satellite Lite / Smart / Base Nexus. ESP32 déclassé comme cerveau. | Capteurs par profil, pas tout dans chaque nœud. Obligatoire ≠ utile ≠ optionnel. | Modèle validé par 4 marchés. C'est l'architecture la plus cohérente pour WildNexus multimodal. |
| **Décision clé** | Remplacer « camera d'abord, audio plus tard » par « architecture multimodale d'abord, validation caméra en premier » | ESP32-S3 → contrôleur basse conso seulement. STM32U5 pour Lite, STM32N6 pour Smart | PIR + T/H + batterie + RTC = obligatoires. Audio = P0-AUDITIF. Vision NoIR/Starvis = cœur Smart | 3 gammes produit, pas une machine unique. Produit utilisateur = 1 base + 2-3 satellites |
| **Phasage** | P0-CAM → P0-AUDITIF → P1-FUSION → P2-RESEAU | Prototype Pi Zero 2 W → validation → STM32N6 / NXP i.MX | Obligatoire / Recommandé / Option / Spécialisé | Satellite Lite → Satellite Smart → Base Nexus |
| **Points de vigilance** | BirdNET sur ESP32 = erreur. Pi always-on = incompatible autonomie. Audio pas secondaire. | LoRa pour metadata, pas pour médias lourds. microSD = risque corruption. | AS7341 spectral = faible priorité. CO₂/VOC = rejeté baseline. | Risque dual-use si trop performant. Garde-fous positionnement/licence requis. |

---

## 2. Convergences entre les 4 rapports

### Accord unanime

1. **Architecture distribuée satellite/base** — les 4 rapports convergent. R1 la définit conceptuellement, R2 la spécifie techniquement, R3 la segmente par capteurs, R4 la valide par le marché.

2. **ESP32-S3 déclassé** — R1 et R2 le disent explicitement : pas le cerveau. R3 ne le mentionne pas comme plateforme cible. R4 confirme que faire du BirdNET/vision lourde sur MCU type ESP32 n'est pas crédible.

3. **BirdNET en local, pas cloud-only** — R1 recommande BirdNET-Go sur gateway/module compute. R2 le place dans la Base Nexus. R4 valide l'IA dans la base plutôt que dans chaque capteur.

4. **LoRa pour événements, pas pour médias** — R2 et R4 sont alignés : LoRa transporte alerte, statut, metadata. WiFi local ou 4G pour transferts lourds.

5. **Trois profils de nœuds** — R2 définit Satellite Lite / Smart / Base Nexus. R3 les segmente par capteurs. R4 les valide comme gammes produit. R1 les implique via niveaux A/B/C.

6. **PIR obligatoire pour déclenchement caméra** — R3 le classe « obligatoire camera ». R2 l'intègre dans le Satellite Lite.

7. **Stockage local par défaut, transmission sélective** — R2 et R4 convergent : fichiers lourds conservés localement, transférés sur demande.

8. **Vigilance dual-use** — R4 l'explicite fortement. R1 et R2 le mentionnent via le contexte defense/surveillance.

### Accords partiels

| Sujet | Consensus | Nuance |
|---|---|---|
| Audio dans P0 | Oui, mais pas BirdNET complet | R1 : P0-AUDITIF = capture + metadata. R2 : audio léger dans Satellite Lite. R3 : 1 micro audible = standard audio |
| GNSS | Utile, pas partout | R2 : Base ou Smart, Lite option. R3 : localisation manuelle suffisante pour Lite. R1 : pas priorisé P0 |
| Caméra NoIR/Starvis | Cœur du système | R2 : Pi Camera Module 3 pour proto. R3 : Starvis = Smart prioritaire. R1 : validation terrain par caméra en premier |

---

## 3. Divergences et propositions différenciées

### 3.1 Choix hardware Satellite Smart

| Source | Proposition | Argument |
|---|---|---|
| **R2** | STM32N6 (prioritaire) | NPU 600 GOPS, MIPI CSI-2, ISP, H264, MCU industriel |
| **R2 + R5** | Rockchip RV1106 (alternative chinoise) | MIPI CSI, ISP, NPU 0.5-1 TOPS, encodeur, Linux compact, 39-83 USD |
| **R5** | Axera AX630C | NPU 3.2 TOPS, 4K camera, ~69+ USD |
| **R5** | Allwinner V853 | NPU 1 TOPS, MIPI CSI, H.265, basse conso |

→ **Différenciation :** R2 privilégie la robustesse industrielle (STM32N6). R5 ouvre un couloir low-cost chinois (RV1106). Ces deux pistes ne sont pas exclusives mais complémentaires : STM32N6 pour la cible produit, RV1106 pour prototypage rapide et exploration coût.

### 3.2 BirdNET : local vs cloud vs gateway

| Source | Position | Localisation BirdNET |
|---|---|---|
| **R1** | BirdNET-Go sur gateway/module compute révélable P1 | Base Nexus ou module séparé |
| **R2** | BirdNET-Go dans la Base Nexus | Base Nexus (Pi 5 / NXP i.MX / Hailo) |
| **R4** | IA dans la base plutôt que dans chaque capteur | Base Nexus |
| **Fiche specs originale** | BirdNET dans le cloud | Cloud externe |

→ **Différenciation :** tous les rapports convergent vers BirdNET local (Base Nexus), en rupture avec la fiche specs qui le plaçait dans le cloud. La nuance porte sur le « quand » : R1 dit P1, R2 l'intègre dans la Base Nexus dès la conception.

### 3.3 Nombre de micros

| Source | Recommandation |
|---|---|
| **R3** | 1 micro MEMS audible = standard audio. Double micro = P1/P2 |
| **Fiche specs** | 2 micros MEMS I2S |
| **R1** | 1 ou 2 micros, à décider |

→ **Différenciation :** R3 est le plus conservateur (1 micro pour P0). R1 laisse ouvert. La fiche specs a déjà 2 micros. Impact BOM : ~4 € d'écart.

### 3.4 Capteur spectral AS7341

| Source | Position |
|---|---|
| **R3** | Non listé dans les capteurs recommandés. La catégorie « multispectral/NIR végétation » est classée « hors baseline » |
| **Fiche specs** | Inclus dans la BOM à 20 € |
| **R1, R2, R4** | Non mentionné |

→ **Divergence :** seul R3 couvre ce capteur, et il l'exclut implicitement. Les autres rapports ne le mentionnent pas. Recommandation : retirer du prototype.

### 3.5 CO₂ / VOC (BME688)

| Source | Position |
|---|---|
| **R3** | CO₂ = « rejeter baseline ». VOC = « option faible priorité » |
| **Fiche specs** | BME688 inclus (VOC/eCO₂/AQI) |

→ **Divergence :** R3 est explicite : CO₂ n'a pas de valeur faune en extérieur. Remplacer BME688 par BME280 (T/H/P) ou utiliser BME688 pour T/H/P seulement.

### 3.6 Plateforme Base Nexus

| Source | Proposition proto | Proposition produit |
|---|---|---|
| **R2** | Raspberry Pi 5 + AI HAT+ | NXP i.MX 8M Plus SOM |
| **R5** | Orange Pi 5 / RK3588S | RK3588 (si software audité) |

→ **Différenciation :** R2 privilégie la piste industrielle occidentale (NXP). R5 ouvre la piste chinoise puissance/prix (RK3588, NPU 6 TOPS). Décision : Pi 5 pour le proto pédagogique, RK3588 à tester en parallèle, NXP pour la cible industrielle.

### 3.7 Module 4G/LTE : par satellite ou base seulement ?

| Source | Position |
|---|---|
| **R2** | 4G dans la Base Nexus. Satellite Smart premium seulement |
| **R4** | Un seul backhaul cellulaire pour plusieurs nœuds |
| **Fiche specs** | 4G dans le boîtier unique |

→ **Convergence R2+R4 contre fiche specs :** pas de 4G dans chaque satellite. La Base Nexus porte le backhaul cellulaire.

---

## 4. Tableau de specs comparatif — Architecture 3 niveaux

Synthèse intégrée des 4 rapports, projetée sur les 3 profils.

### 4.1 Satellite Lite

| Spécification | R1 | R2 | R3 | R4 | **Synthèse intégrée** |
|---|---|---|---|---|---|
| **Rôle** | Contrôleur basse conso always-on | Veille, capteurs, PIR, audio léger, LoRa | Capteurs essentiels, basse conso | Petit nœud discret, pas d'IA lourde | Nœud sobre de veille et capture légère |
| **CPU recommandé** | ESP32-S3 ou STM32U5 | STM32U5, Apollo510, Ambiq Apollo510B | — | — | **STM32U5** (cible), ESP32-S3 (proto) |
| **Caméra** | Non prioritaire | — | — | Oui (capture) | **Option** (non cœur Lite) |
| **Audio** | — | Audio léger | 1 MEMS audible | Oui | **1 micro MEMS I2S**, fenêtré |
| **PIR** | Oui (event sensor) | Oui | Obligatoire caméra | — | **Obligatoire** |
| **Environnement** | Oui | — | T/H interne + T/H externe + pression | — | **BME280** (T/H/P) |
| **Luminosité** | — | — | Recommandé | — | **Option** (lux sensor) |
| **GNSS** | — | Option | Localisation manuelle suffisante | — | **Non baseline** (saisie app) |
| **RTC** | Oui | Oui | Obligatoire | — | **Obligatoire** (DS3231) |
| **IMU** | — | — | Recommandé système | — | **Recommandé** (anti-tamper) |
| **Stockage** | — | microSD industrielle | — | Local | **1× microSD industriel 32 GB** |
| **LoRa** | Oui | Oui (metadata) | — | Oui (événementiel) | **Obligatoire** (RFM95W) |
| **WiFi** | — | Local court (maintenance) | — | Local court | **WiFi local** (maintenance) |
| **4G/LTE** | Non | Non | — | Non | **Non** |
| **IA locale** | Non | Non | — | Non | **Non** |
| **Alimentation** | Gestion énergie | Batterie + solaire | Tension batterie obligatoire | — | **LiFePO4 + MPPT solaire** |
| **Boîtier** | — | — | — | Discret | **IP65**, discret, fixation arbre |

### 4.2 Satellite Smart

| Spécification | R1 | R2 | R3 | R4 | **Synthèse intégrée** |
|---|---|---|---|---|---|
| **Rôle** | Modules révélables : caméra, audio, stockage | Caméra, audio riche, détection locale, préfiltrage IA | Capteurs + IA légère, meilleure caméra/audio | IA légère image/audio, transfert sélectif | Nœud de capture riche avec préfiltrage IA |
| **CPU recommandé** | — | **STM32N6** (prioritaire) | — | STM32N6 ou équivalent | **STM32N6** (cible) ; **Rockchip RV1106** (proto low-cost) |
| **Caméra** | Oui | Pi Camera Module 3 NoIR (proto) | Sony STARVIS = Smart prioritaire | Oui | **Sony STARVIS IMX462** (cible), IMX708 NoIR (proto) |
| **IR** | Oui | — | IR-cut motorisé = Smart/P1 | — | **LEDs IR 850 nm** + MOSFET driver |
| **Audio** | Micro(s) | Audio riche | 1-2 MEMS, electret P1 | — | **1-2 MEMS I2S**, fenêtres événementielles |
| **PIR** | Oui | Oui | Obligatoire | — | **Obligatoire** |
| **Radar mmWave** | — | — | P1 Smart test | — | **Option test P1** |
| **Environnement** | — | — | T/H externe + pression + luminosité | — | **BME280 + lux sensor** |
| **GNSS** | — | Option | Base ou Smart | — | **Option** (ponctuel) |
| **RTC** | Oui | Oui | Obligatoire | — | **Obligatoire** |
| **IMU** | — | — | Recommandé | — | **Recommandé** |
| **Stockage** | Oui | microSD industriel, journalisation append-only | — | Local | **1× microSD industriel 128 GB** |
| **LoRa** | — | Oui | — | Oui | **Obligatoire** |
| **WiFi** | Oui (local) | Oui (transfert par rafales) | — | — | **WiFi local** (transfert vers base) |
| **4G/LTE** | LTE-M optionnel | Premium seulement | — | Non | **Non baseline** (option premium) |
| **IA locale** | Filtre animal/non-animal | Détection + compression + sélection | Préfiltrage audio | IA légère | **Préfiltrage animal/non-animal + compression** |
| **Alimentation** | Batterie + réveil | Batterie + solaire | — | — | **LiFePO4 50-80 Wh + MPPT** |
| **Boîtier** | — | — | — | — | **IP65/IP66**, presse-étoupes, évent membrane |

### 4.3 Base Nexus

| Spécification | R1 | R2 | R3 | R4 | **Synthèse intégrée** |
|---|---|---|---|---|---|
| **Rôle** | — | Stockage lourd, BirdNET-Go, 4G/5G, orchestration, dashboard | Capteurs système + IA lourde + stockage + backhaul | IA lourde, stockage, backhaul, dashboard | Station maîtresse : IA, stockage, connectivité |
| **CPU recommandé** | Module compute révélable | **Raspberry Pi 5** (proto), **NXP i.MX 8M Plus** (industriel) | — | Raspberry Pi / NXP i.MX / Hailo | **Pi 5** (proto) ; **RK3588** (test coût) ; **NXP i.MX 8M Plus** (cible) |
| **Accélération IA** | — | Hailo-8L (13 TOPS) ou Hailo-8 (26 TOPS) | — | — | **Hailo-8L** ou NPU intégré (RK3588 = 6 TOPS) |
| **Caméra** | — | — | — | — | Non (la base ne capture pas) |
| **Audio** | — | — | — | — | Non (reçoit des satellites) |
| **BirdNET** | BirdNET-Go P1 | BirdNET-Go dans la base | — | IA dans la base | **BirdNET-Go local** |
| **Vision IA** | — | Oui | — | — | **Classification + corrélation multimodale** |
| **Stockage** | — | SSD/eMMC (pas microSD) | — | Gros stockage | **SSD 256+ GB** ou **eMMC 64+ GB** |
| **LoRa** | — | Réception metadata satellites | — | — | **Passerelle LoRa** (réception) |
| **WiFi** | — | Oui | — | — | **WiFi AP** (transfert satellites + maintenance) |
| **4G/5G** | — | 4G/5G (backhaul utilisateur) | — | Un seul backhaul | **LTE Cat-4 ou 5G** (backhaul unique) |
| **Ethernet** | — | Option | — | — | **Option** (installation fixe) |
| **Dashboard** | — | Local + distant | — | Tableau de bord | **Interface web locale + cloud sync** |
| **Sécurité** | — | Chiffrement, gestion droits | — | Garde-fous dual-use | **Chiffrement données + ACL + licence** |
| **Alimentation** | — | — | — | Plus robuste | **Secteur ou gros solaire 100-150 Wh** |
| **Boîtier** | — | — | — | Caché | **IP66**, discret, ventilé, accessible |

---

## 5. Matrice de couverture : quel rapport couvre quel sujet

| Sujet | R1 | R2 | R3 | R4 | R5 |
|---|---|---|---|---|---|
| Vision produit / concept | ● | ○ | ○ | ● | ○ |
| Architecture distribuée | ● | ● | ○ | ● | ○ |
| Choix CPU/MCU | ● | ● | ○ | ○ | ● |
| Capteurs embarqués | ○ | ○ | ● | ○ | ○ |
| Communication (LoRa/WiFi/4G) | ○ | ● | ○ | ● | ○ |
| Stockage | ○ | ● | ○ | ○ | ○ |
| IA locale vs cloud | ● | ● | ○ | ● | ○ |
| BirdNET | ● | ● | ○ | ○ | ○ |
| Alimentation/énergie | ○ | ○ | ● | ○ | ○ |
| Boîtier/environnement | ○ | ○ | ○ | ○ | ○ |
| Marché/concurrence | ● | ○ | ○ | ● | ○ |
| Dual-use / sécurité | ○ | ○ | ○ | ● | ○ |
| Phasage P0/P1/P2 | ● | ○ | ○ | ○ | ○ |
| Hardware chinois | ○ | ○ | ○ | ○ | ● |
| RGPD / licences | ● | ○ | ○ | ○ | ○ |

● = couvert en profondeur · ○ = mentionné ou implicite · vide = non couvert

---

## 6. Angles morts globaux

Aucun des 4 rapports ne couvre en profondeur :

1. **Boîtier et contraintes mécaniques** — IP65/IP66, presse-étoupes, évent membrane, fixation, matériaux, poids. La fiche specs originale est plus complète sur ce point.
2. **Alimentation détaillée** — dimensionnement batterie, profil solaire hiver belge, BMS, power-path. R3 mentionne les mesures obligatoires mais pas le dimensionnement.
3. **Licences BirdNET** — R1 mentionne la vérification nécessaire mais ne l'effectue pas.
4. **RGPD audio** — R1 l'évoque, les autres non.
5. **Coût total produit** — seul le market scan (R4) aborde le modèle économique (1 base + 2-3 satellites). Aucun ne chiffre le coût complet par profil.
6. **Interface utilisateur** — WiFi local + portail web mentionnés mais non spécifiés.

---

## 7. Recommandation finale

Les 4 rapports sont **cohérents et complémentaires**, pas redondants. Ils forment un corpus décisionnel à 4 faces :

| Rapport | Rôle dans le corpus |
|---|---|
| R1 – Multimodal Reset | **Pourquoi** on change de vision |
| R2 – Hardware Architecture | **Avec quoi** on construit |
| R3 – Sensor Matrix | **Quoi** on embarque, et pourquoi |
| R4 – Market Scan | **Pour qui** et **est-ce que ça existe déjà** |
| R5 – Hardware Chine | **À quel prix** et **quelles alternatives** |

**Prochaine étape :** produire une **ADR consolidée** (Architecture Decision Record) qui fige les choix issus de ces 4 rapports, en intégrant les recommandations de l'analyse de la fiche specs BOM (`2026-05-22_dobby_gemini_analyse-fiche-specs-bom-wildnexus.md`).

---

*Synthèse produite par Dobby 🦉 — 2026-05-22, 23h.*
