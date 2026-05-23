# Review Dobby — WildNexus station bioacoustique/camera

Date : 2026-05-22
Source : `JCH_Inbox/00_INBOX/fiche_specs_BOM_station_bioacoustique_camera.md`
Mandats : Chouette (terrain/capteurs), Nova (photo/R&D), Forge (architecture), Renard (risques usage/RGPD)

## Verdict

La fiche est techniquement coherente comme vision de station scientifique multimodale P1/P2. Elle n'est pas coherente comme P0 WildNexus strict.

Le verrou P0 actuel limite le premier jalon au noeud camera autonome : capture jour/nuit, detection evenementielle, filtre animal/non-animal, LPWAN evenementiel, stockage local, configuration terrain, autonomie minimale, boitier IP67. La fiche ajoute bioacoustique continue, Raspberry Pi, LTE, cloud BirdNET complet, portail WiFi et capteurs environnementaux avances. Ce sont de bons axes, mais ils doivent etre traites comme extension "station scientifique hybride", pas comme remplacement du P0.

## Ce qui est fort

- Architecture hierarchisee saine : ESP32-S3 always-on, sous-systemes lourds reveilles a la demande.
- Separation claire entre detection locale legere et analyse cloud BirdNET.
- Bonne intuition de terrain : stockage local, WiFi local, upload differe, solaire, boitier IP65/IP66, condensation identifiee.
- BOM suffisamment concrete pour permettre un prototype rapide.
- La fiche porte la vraie differenciation WildNexus : donnees ecologiques multimodales synchronisees, pas seulement camera.

## Points de friction majeurs

1. Scope creep P0

La bioacoustique, BirdNET cloud et LTE massif sont hors P0 actuel. Les integrer maintenant dilue l'objectif : prouver un noeud camera autonome fiable.

2. Raspberry Pi comme dependance centrale

Le Pi Zero 2 W est excellent pour prototypage camera, compression, hotspot et upload. Il reste mauvais comme dependance critique d'un systeme longue autonomie : boot, consommation, corruption SD, arret propre, maintenance Linux.

3. Autonomie non quantifiee

La fiche mentionne batterie 50-80 Wh, solaire et modes energie, mais sans budget Wh/jour. C'est le verrou technique principal. Une station avec Pi + LTE + IR + audio frequent peut exploser la consommation si les cycles evenementiels sont trop nombreux.

4. Audio continu sous-specifie

Deux MEMS I2S et des extraits 5-15 s ne suffisent pas. Il faut specifier sample rate, bit depth, pre-roll, seuils, fenetrage DSP, compression, stockage circulaire, bruit du boitier, vent/pluie, et membrane acoustique.

5. Boitier trop peu separe par fonction

Camera, IR, micros, event, antennes LTE/GNSS et solaire ont des contraintes contradictoires. Il faut traiter la mecanique comme un sous-systeme critique, pas comme une ligne de BOM.

6. Cloud et droits BirdNET

BirdNET-Analyzer est adapte aux traitements scientifiques a grande echelle, mais tout usage commercial ou derive doit etre verifie dans les licences de modeles. Ne pas construire une offre produit avant clarification licence.

## Reclassification recommandee

### P0 strict : noeud camera autonome

Garder le P0 existant : ESP32-S3, camera OV5640 M12 DVP, IR pulse, PIR/event, stockage local, LoRa alerte, configuration locale simple, autonomie longue.

### P1A : module bioacoustique add-on

Ajouter audio comme module d'extension, sans Pi obligatoire :

- ESP32-S3 ou MCU audio dedie ;
- 1 ou 2 MEMS I2S avec ports acoustiques valides ;
- enregistrement court avec pre-roll ;
- stockage local WAV/FLAC ou Opus selon contrainte ;
- metadata commune avec les evenements camera ;
- upload local ou differe.

### P1B : station scientifique hybride

La fiche actuelle devient le cahier de vision de cette station :

- ESP32-S3 gardien energie ;
- Pi Zero 2 W/CM4 reveille a la demande ;
- camera Pi/Starvis ;
- WiFi local ;
- LTE optionnel ;
- BirdNET cloud ou batch local.

### P2 : reseau/cloud scientifique

Dashboard, stockage long terme, modele BirdNET complet, exports scientifiques, API, gouvernance donnees.

## Ameliorations concretes a apporter a la fiche

1. Ajouter une table de budget energie

Colonnes minimales : etat, courant, tension, duree, frequence/jour, Wh/jour, hypotheses. Etats obligatoires :

- deep sleep ESP32 + RTC ;
- ecoute audio ;
- capture audio ;
- reveil Pi ;
- capture photo jour ;
- capture photo nuit IR ;
- compression ;
- upload LTE ;
- hotspot maintenance ;
- recharge solaire hiver.

2. Definir trois profils operationnels

- Profil A : camera-only P0, autonomie maximale.
- Profil B : bioacoustique locale, upload manuel.
- Profil C : station connectee LTE/cloud, autonomie plus courte assumee.

3. Transformer LTE en option, pas en baseline

Le LTE doit etre :

- coupe physiquement par load switch ;
- active par fenetres courtes ;
- avec queue locale persistante ;
- retry exponentiel ;
- quotas data ;
- upload thumbnails/metadonnees avant medias complets.

4. Durcir le stockage

Preferer :

- Pi avec eMMC en pre-serie si Linux reste present ;
- microSD high endurance uniquement pour media/ring buffer ;
- racine Linux read-only si possible ;
- shutdown propre par GPIO ;
- file queue atomique avec checksum.

5. Ajouter un schema de donnees evenementiel

Chaque evenement doit avoir :

- event_id ;
- node_id ;
- timestamp RTC + qualite GNSS ;
- type : acoustic, camera, PIR, schedule, manual ;
- capteurs environnementaux ;
- fichiers lies ;
- hash/checksum ;
- privacy flag : human_possible / animal_only / unknown ;
- upload_status.

6. Preciser l'audio terrain

Ajouter :

- frequence cible : 24, 32 ou 48 kHz selon taxons ;
- 16 ou 24 bit ;
- mono vs stereo et distance inter-micros ;
- pre-roll 2-5 s ;
- fenetre d'analyse locale ;
- seuils par bande de frequence ;
- protection vent/pluie ;
- calibration micro ;
- test bruit du boitier.

7. Revoir les capteurs environnementaux

Pour P1 scientifique :

- garder temperature/humidite/pression ;
- traiter VOC/eCO2 comme indicateurs experimentaux, pas mesures ecologiques fortes ;
- AS7341 utile si question lumiere/phenologie, sinon option.

8. Clarifier le choix camera

Pour la station hybride, Camera Module 3 NoIR Wide est un bon prototype Pi : IMX708 12 MP, autofocus, NoIR, FoV large. Pour le P0 camera autonome ESP32-S3, rester aligne avec ADR-002 : OV5640 M12 DVP + lentille IR-corrigee.

9. Ajouter mecanique/optique comme chapitre critique

Inclure :

- fenetre optique anti-reflet ;
- separation IR/camera pour eviter flare interne ;
- membrane hydrophobe micro ;
- event ePTFE ;
- silica gel ou autre gestion humidite ;
- drainage/positionnement boitier ;
- connecteurs antennes et presse-etoupes ;
- fixation arbre/tried avec orientation reproductible.

10. Ajouter un registre des risques

Risques prioritaires :

- autonomie insuffisante hiver belge ;
- faux positifs audio trop nombreux ;
- corruption SD ;
- condensation ;
- lueur IR perturbante ;
- cout data LTE ;
- licence BirdNET en usage commercial ;
- capture humaine accidentelle.

## Decision proposee

Ne pas remplacer le P0 par cette fiche.

Creer plutot un document derive : `WildNexus_P1_station_bioacoustique_camera.md`, avec statut "vision P1/P2". Garder le P0 camera autonome comme preuve terrain. Utiliser cette fiche pour garantir que le P0 preserve les interfaces necessaires : horodatage, geolocalisation, event schema, connecteur extension capteur, stockage local propre et alimentation modulable.

## Sources de verification rapide

- Raspberry Pi Camera Module 3 : IMX708 12 MP, NoIR, FoV standard/wide, autofocus, CSI-2.
- BirdNET-Analyzer : outil officiel pour traitements scientifiques massifs audio, avec vigilance licence modeles.
- ESP32-S3 : modes sleep disponibles, a valider sur carte reelle car les DevKits consomment plus que le silicium nu.
- LoRaWAN EU868 : duty-cycle et temps d'air limitent fortement les transferts massifs ; a reserver aux alertes/metadonnees.
