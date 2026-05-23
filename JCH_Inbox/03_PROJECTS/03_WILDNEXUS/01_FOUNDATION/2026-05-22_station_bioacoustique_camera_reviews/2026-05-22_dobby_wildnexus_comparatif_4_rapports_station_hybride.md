# WildNexus — Comparatif des 4 rapports sur la station bioacoustique/caméra

**Date :** 2026-05-22, après 22h  
**Objet :** synthèse différenciée des rapports déposés dans `JCH_Inbox/00_INBOX`  
**Documents comparés :**

1. `fiche_specs_BOM_station_bioacoustique_camera.md` — fiche source specs/BOM
2. `2026-05-22_dobby_wildnexus-station-bioacoustique-camera-review.md` — review Dobby
3. `2026-05-22_dobby_wildnexus-analysis-deepseek.md` — analyse DeepSeek
4. `2026-05-22_dobby_gemini_analyse-fiche-specs-bom-wildnexus.md` — analyse Gemini

**Documents non intégrés comme rapport distinct :**

- `fiche_specs_BOM_station_bioacoustique_camera.md.zip` : archive/duplication probable de la fiche source.
- `2026-05-22_dobby_system_check.md` : contrôle système, pas un rapport produit.

---

## 1. Synthèse exécutive

Les quatre documents convergent sur un point : la fiche décrit une architecture crédible pour une station scientifique multimodale WildNexus. Elle combine caméra, bioacoustique, capteurs environnementaux, stockage local, WiFi de terrain, LTE et BirdNET. Elle est assez concrète pour lancer un prototype exploratoire.

La divergence principale porte sur le **statut du prototype** :

- La fiche source présente l’architecture comme une version “figée” de prototype terrain sérieux.
- Le review Dobby estime que cette architecture est cohérente en **P1/P2**, mais trop large pour le **P0 WildNexus strict**.
- DeepSeek valide l’architecture bi-étagée ESP32 + Pi, mais alerte sur les points d’exécution : latence de réveil, SD, condensation, IR-cut, supercapacité LTE.
- Gemini propose le recadrage le plus fort : passer d’un boîtier tout-en-un à une architecture **satellites + base**, avec LoRa, Base Nexus locale et BirdNET-Go hors cloud obligatoire.

**Décision recommandée :** ne pas remplacer le P0 caméra par cette fiche. La transformer en document de vision **P1 — station scientifique hybride**, tout en extrayant les exigences d’interface que le P0 doit préserver : horodatage, schéma d’événement, stockage robuste, extension capteur/audio, alimentation modulable, connectivité future.

---

## 2. Comparatif des thèses

| Rapport | Thèse centrale | Vision architecture | Statut implicite | Contribution utile | Limite principale |
|---|---|---|---|---|---|
| Fiche source | Construire une station hybride bioacoustique/caméra complète | ESP32-S3 always-on + Pi Zero/CM4 on-demand + LTE + cloud BirdNET | Prototype terrain sérieux | Donne une BOM chiffrée et une vision concrète | Mélange P0, P1 et P2 ; autonomie non quantifiée |
| Review Dobby | Bonne vision P1/P2, mauvaise substitution au P0 strict | Garder P0 caméra ; dériver P1A audio, P1B station hybride, P2 cloud | Reclassification nécessaire | Clarifie phasage et risques produit | Ne propose pas encore de BOM détaillée rephasée |
| Analyse DeepSeek | Architecture bi-étagée valide mais attention aux maillons faibles | ESP32 gardien + Pi réveillé ; fiabilisation terrain | Optimisation technique du proto source | Très utile sur latence Pi, buffer audio, SD read-only, condensation | Ne questionne pas assez le scope P0 |
| Analyse Gemini | Le tout-en-un doit évoluer vers satellites + base | Satellite Lite / Satellite Smart / Base Nexus | Refonte architecture système | Introduit LoRa, Base Nexus, BirdNET-Go local, profils matériels | Plus ambitieux ; peut déplacer le problème vers une architecture plus vaste |

---

## 3. Convergences

Les quatre rapports valident les principes suivants :

1. **Architecture hiérarchisée basse consommation.** Un composant léger doit rester actif, les modules coûteux doivent être réveillés uniquement sur événement ou fenêtre programmée.

2. **Stockage local indispensable.** Même avec LTE ou cloud, le terrain impose un tampon local robuste et consultable hors ligne.

3. **WiFi local utile.** Le portail local est pertinent pour maintenance, téléchargement, configuration et récupération terrain.

4. **Condensation et boîtier sont critiques.** L’étanchéité n’est pas seulement un boîtier IP65/IP66 ; elle implique membranes, évents, fenêtre optique, séparation IR/caméra et gestion humidité.

5. **LTE doit être discipliné.** Upload distant oui, mais activation courte, queue locale, quotas data, retry contrôlé et alimentation capable d’absorber les pics de courant.

6. **BirdNET est une brique forte mais pas neutre.** Il faut clarifier où il tourne, quand il intervient, et sous quelles conditions de licence/usage.

---

## 4. Divergences réelles

### 4.1 Boîtier unique vs réseau distribué

La fiche et DeepSeek restent proches d’un boîtier unique hybride : ESP32 + Pi + caméra + LTE + cloud.

Gemini pousse une architecture distribuée :

- satellites légers pour veille/détection ;
- satellites smart pour caméra/audio ;
- base locale pour stockage lourd, BirdNET-Go, dashboard et 4G/5G.

Le review Dobby tranche entre les deux : ne pas imposer la base distribuée au P0, mais ne pas enfermer WildNexus dans le boîtier unique.

### 4.2 Cloud BirdNET vs BirdNET local

La fiche source met BirdNET dans le cloud.

Gemini recommande BirdNET-Go sur une base locale, cloud comme synchronisation facultative. Cette proposition réduit dépendance réseau, coûts data et exposition RGPD, mais ajoute une brique matérielle de base.

Synthèse : pour P1, privilégier **BirdNET local sur Base Nexus ou batch local**, avec cloud en option. Pour P0, ne pas faire de BirdNET un prérequis.

### 4.3 ESP32-S3 : coeur produit ou contrôleur auxiliaire

La fiche source place l’ESP32-S3 au centre.

Gemini le déclasse : utile pour prototype et contrôle basse conso, mais pas comme cerveau multimodal long terme. Alternatives citées : STM32U5, STM32N6, Apollo510, RV1106 selon niveau.

Synthèse : ESP32-S3 acceptable pour prototype rapide et interface basse consommation ; ne pas le verrouiller comme architecture produit finale.

### 4.4 LTE baseline ou option

La fiche inclut LTE Cat-1 comme transmission distante.

Dobby et Gemini proposent de rendre LTE optionnel, voire déporté vers la base. DeepSeek insiste surtout sur la stabilité électrique des pics 4G.

Synthèse : LTE est un module optionnel ou base-side, pas une exigence par satellite P0.

### 4.5 Capteurs environnementaux

La fiche inclut BME688/BME680, AS7341, GNSS, RTC.

Gemini propose de retirer AS7341 du prototype initial, de remplacer BME688 par BME280 si VOC/eCO2 ne servent pas, et d’ajouter IMU, watchdog, LoRa et capteur humidité interne.

Synthèse : T/H/P + humidité interne + RTC sont prioritaires ; GNSS selon besoin de géolocalisation autonome ; AS7341 et VOC/eCO2 restent expérimentaux.

---

## 5. Tableau de specs comparatif

| Domaine | Fiche source | Review Dobby | Analyse DeepSeek | Analyse Gemini | Synthèse recommandée |
|---|---|---|---|---|---|
| Statut produit | Prototype terrain sérieux figé | Vision P1/P2, pas P0 strict | Prototype validable avec durcissement | Architecture à refondre satellites + base | Créer `WildNexus_P1_station_bioacoustique_camera.md` |
| P0 WildNexus | Non séparé explicitement | P0 caméra strict conservé | Non distingué fortement | P0-CAM / P0-AUDITIF / P1-FUSION / P2-RESEAU | Garder P0 caméra autonome ; audio en P0-AUDITIF séparé |
| Architecture | ESP32-S3 + Pi + LTE + cloud | P0 caméra, P1A audio, P1B station hybride, P2 cloud | ESP32 always-on + Pi on-demand | Satellite Lite / Smart + Base Nexus | P0 simple ; P1 station hybride ; P2 réseau distribué |
| Contrôleur basse conso | ESP32-S3 avec PSRAM | ESP32-S3 acceptable P0/P1 proto | ESP32-S3 validé comme gardien | STM32U5/Apollo510 ou STM32N6/RV1106 à terme | ESP32-S3 prototype ; cible produit à réévaluer |
| Calcul média | Pi Zero 2 W prototype ; CM4 pré-série | Pi uniquement P1B, réveillé à la demande | Pi OK mais boot 20-40 s problématique | Base Nexus ou satellite smart plus adapté | Pi Zero pour banc rapide ; CM4/eMMC ou Base Nexus pour pré-série |
| Caméra | Pi Camera Module 3 NoIR IMX708 ; IMX462 alternative | IMX708 pour station hybride ; OV5640 M12 pour P0 ESP32 | Ajouter IR-cut motorisé | Distinguer Satellite Smart et Base ; P0 ADR-002 à respecter | P0 : OV5640 M12 DVP ; P1 station : IMX708/IMX462 selon besoin |
| Audio | 2 MEMS I2S, extraits 5-15 s | À spécifier : sample rate, pre-roll, vent/pluie, calibration | Buffer circulaire ESP32 10 s pour pré-trigger | P0-AUDITIF minimal ; double micro plutôt Smart | 1 micro P0 auditif ; 2 MEMS P1 ; pre-roll obligatoire |
| BirdNET | Cloud complet | P1/P2, licence à vérifier | Cloud possible mais non questionné | BirdNET-Go local sur Base Nexus | P0 sans BirdNET ; P1 BirdNET local/batch ; cloud optionnel |
| Connectivité locale | Hotspot WiFi Pi | WiFi local utile | WiFi maintenance conservé | Gateway/base locale | WiFi maintenance P1 ; config P0 simple BLE/WiFi selon coût |
| Connectivité distante | LTE Cat-1 ; Cat-4 si vidéo | LTE optionnel, fenêtre courte | Supercapacité pour pics 4G | LoRa pour satellites, LTE sur base | P0 LoRa alerte ; P1 LTE optionnel ; P2 base connectée |
| LoRa | Absent | Mentionné comme P0 existant à préserver | Absent | Obligatoire entre satellites/base | Ajouter LoRa/LoRaWAN au schéma et BOM P0/P1 |
| Stockage | microSD audio + microSD média | Queue atomique, checksum, eMMC si Linux | OS Pi read-only / OverlayFS ; partition données | Une SD industrielle unifiée plutôt que deux | SD industrielle + append-only ; eMMC si Linux produit |
| Energie | Batterie 50-80 Wh, USB-C, solaire | Budget Wh/jour obligatoire | Attention boot Pi, IR, LTE, thermique | Déclasser tout-en-un pour autonomie | Table énergie par mode avant achat |
| Boîtier | IP65/IP66, presse-étoupes, évent | Mécanique/optique chapitre critique | Évent compensation, silice, dissipation | Évent membrane + humidité interne | IP67 cible P0 ; membranes micro + fenêtre IR séparée |
| Capteurs env. | BME688/BME680, AS7341, GNSS, RTC | VOC/eCO2 expérimental ; AS7341 optionnel | Non détaillé | Retirer AS7341 ; BME280 ; ajouter IMU/watchdog | T/H/P + humidité interne + RTC ; GNSS/AS7341 optionnels |
| RGPD / privacy | Non traité | Capture humaine accidentelle à flagger | Non traité | RGPD audio bloquant Europe | Ajouter privacy flag et politique audio avant terrain |
| Coût prototype | 450-550 EUR ; éco 320-380 EUR | Pas de BOM rephasée | Ajouts techniques modestes | Ajouts/remplacements coût net limité | Refaire BOM par profil : P0-CAM, P0-AUDITIF, P1 station |
| Risque principal | À valider en prototype | Scope creep et autonomie | Latence Pi, SD, condensation | Mauvais niveau d’architecture | Décider phase, budget énergie et architecture de communication |

---

## 6. Synthèse différenciée des propositions

### Proposition A — Fiche source : station hybride tout-en-un

**Position :** construire un appareil autonome complet, intégrant audio, caméra, Pi, LTE, cloud BirdNET et WiFi local.

**Intérêt :** rapide à comprendre, vendable comme prototype de terrain, BOM concrète.

**Risque :** trop lourd pour P0 ; autonomie, fiabilité Linux et coût data peuvent devenir bloquants.

**Usage recommandé :** base de cahier des charges P1, pas cahier de P0.

### Proposition B — Dobby : reclassification par phases

**Position :** conserver la fiche mais la reclasser : P0 caméra strict, P1A bioacoustique add-on, P1B station hybride, P2 réseau/cloud.

**Intérêt :** protège l’exécution P0 tout en gardant la vision multimodale.

**Risque :** demande un travail de réécriture des specs et BOM par phase.

**Usage recommandé :** ligne directrice de gouvernance projet.

### Proposition C — DeepSeek : durcissement technique du tout-en-un

**Position :** l’architecture bi-étagée est valide si l’on corrige les faiblesses d’exécution.

**Ajouts clés :**

- buffer circulaire audio sur ESP32 ;
- Pi en read-only / OverlayFS ;
- eMMC ou partition données robuste ;
- évent de décompression ;
- membrane ePTFE ;
- IR-cut motorisé ;
- supercapacité pour LTE.

**Intérêt :** très utile pour fiabiliser un prototype P1B.

**Risque :** ne résout pas le mélange P0/P1/P2.

### Proposition D — Gemini : architecture satellites + base

**Position :** la fiche décrit en réalité une base compacte ; WildNexus devrait être conçu comme un réseau de satellites différenciés et une Base Nexus.

**Ajouts clés :**

- Satellite Lite ;
- Satellite Smart ;
- Base Nexus ;
- LoRa entre satellites et base ;
- BirdNET-Go local ;
- cloud facultatif ;
- phasage P0-CAM / P0-AUDITIF / P1-FUSION / P2-RESEAU.

**Intérêt :** meilleur alignement avec la vision “infrastructure distribuée d’observation écologique”.

**Risque :** ambition plus large ; nécessite discipline pour ne pas ralentir P0.

---

## 7. Décision proposée

### Décision 1 — Ne pas fusionner cette fiche avec le P0

Le P0 doit rester un nœud caméra autonome, reproductible, mesurable, autonome et robuste.

### Décision 2 — Créer un document P1 dédié

Créer :

`JCH_Inbox/03_PROJECTS/03_WILDNEXUS/01_FOUNDATION/WildNexus_P1_station_bioacoustique_camera.md`

Ce document doit reprendre la fiche source en la transformant en vision P1/P2, avec :

- profils opérationnels ;
- architecture de communication ;
- BOM par profil ;
- budget énergie ;
- schéma de données événementiel ;
- risques RGPD/audio ;
- stratégie BirdNET local/cloud.

### Décision 3 — Réviser la fiche source autour de trois profils

| Profil | But | Matériel indicatif | Connectivité | Analyse IA | Statut |
|---|---|---|---|---|---|
| P0-CAM | Prouver caméra autonome basse conso | ESP32-S3 + OV5640 M12 + IR + LoRa + SD | LoRa alertes + local | Animal/non-animal léger | Prioritaire |
| P0-AUDITIF | Prouver capture audio horodatée | ESP32-S3 + 1 MEMS + RTC + SD | Local ou LoRa metadata | Pas de BirdNET requis | Secondaire court |
| P1-STATION | Fusion caméra/audio/environnement | ESP32 gardien + Pi/CM4 + 2 MEMS + IMX708/IMX462 | WiFi local + LTE optionnel | BirdNET local/batch/cloud | Vision de la fiche |
| P2-RESEAU | Infrastructure distribuée | Satellites Lite/Smart + Base Nexus | LoRa + base LTE/5G | BirdNET-Go local + cloud sync | Écosystème |

---

## 8. Actions recommandées

### Immédiat

1. Marquer la fiche source comme **P1/P2 vision**, pas P0.
2. Ajouter LoRa comme lien événementiel dans les specs comparatives.
3. Ajouter un tableau de budget énergie avant toute décision d’achat.
4. Séparer la BOM en P0-CAM, P0-AUDITIF et P1-STATION.
5. Ajouter une section RGPD/audio et licence BirdNET.

### Technique

1. Tester le réveil Pi et mesurer latence réelle.
2. Prototyper buffer circulaire audio sur ESP32-S3.
3. Valider OverlayFS/read-only sur Pi.
4. Tester membrane micro + boîtier + pluie/vent.
5. Mesurer pics modem LTE avec supercapacité ou rail dédié.

### Gouvernance

1. Conserver le verrou P0 actuel.
2. Créer une ADR ou note de décision : “BirdNET cloud vs Base Nexus locale”.
3. Créer une ADR : “Boîtier unique vs satellites + base”.
4. Créer une fiche “privacy by design” pour audio et photo.

---

## 9. Conclusion

La fiche source ne doit pas être rejetée : elle capture très bien la vision WildNexus comme station scientifique multimodale. Mais elle ne doit pas gouverner le P0.

La bonne lecture est :

- **P0 :** nœud caméra autonome fiable.
- **P0-AUDITIF :** preuve audio minimale séparée.
- **P1 :** station hybride bioacoustique/caméra.
- **P2 :** réseau écologique distribué avec Base Nexus et cloud optionnel.

La synthèse la plus solide combine :

- la concrétude BOM de la fiche source ;
- la discipline de phase du review Dobby ;
- le durcissement terrain DeepSeek ;
- l’architecture distribuée Gemini.

Le prochain livrable utile est une fiche P1 réécrite, non plus comme “architecture figée”, mais comme **cahier de vision différencié par profils opérationnels**.
