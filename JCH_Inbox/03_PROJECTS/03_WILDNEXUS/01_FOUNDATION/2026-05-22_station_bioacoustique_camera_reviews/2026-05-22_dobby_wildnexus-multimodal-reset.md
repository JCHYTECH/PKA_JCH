# WildNexus — Analyse reset multimodal apres nouvelles donnees

**Date :** 2026-05-22  
**Orchestration :** Dobby  
**Specialistes mobilises :** Furet, Chouette, Forge, Clio, Atlas  
**Statut :** Note de decision pour figer l'orientation WildNexus

## Verdict Dobby

Les nouvelles donnees ne detruisent pas WildNexus. Elles corrigent son centre de gravite.

La formulation precedente "P0 = noeud camera autonome, bioacoustique P1" etait saine pour eviter le scope creep. Mais elle risque maintenant de figer une erreur de vision : WildNexus ne doit pas etre une camera a laquelle on ajoutera du son. WildNexus doit etre un noeud d'observation multimodal, dont la camera est seulement la premiere modalite prouvee.

Je recommande donc de remplacer le verrou mental :

> camera d'abord, acoustique plus tard

par :

> architecture multimodale d'abord, validation terrain par camera en premier, audio en piste parallele controlee.

## Ce que les nouveaux documents changent

### 1. Le son n'est pas une extension secondaire

La note `Wildnexus.md` remet l'audio au centre : 1 ou 2 micros, BirdNET, conservation des sons d'oiseaux, analyse des sons non oiseaux, declenchement par chant, bruit caracterise ou demande distante.

Ce point est fort. Pour les oiseaux, chauves-souris, amphibiens, orthopteres et certains mammiferes, l'audio capte une presence que la camera manque souvent. Le dossier bioacoustique Faune Autour disait deja que de nombreux animaux sont plus faciles a detecter par le son que par la vue, et que la bioacoustique est assez mature pour un prototype.

Conclusion : l'audio doit entrer dans les exigences d'interface P0, meme si BirdNET complet ne tourne pas dans le premier noeud P0.

### 2. BirdWeather a ete vu, mais mal classe

Recherche locale : BirdWeather apparait dans `06_COMPONENTS/BIOACOUSTIC/Faune_Autour_Acoustic_Project_Report.md` et dans une transcription BirdNET-Pi, mais pas dans le scan marche P0 du 18 mai.

Donc oui : BirdWeather avait ete repere, mais pas traite comme concurrent/benchmark central de WildNexus. C'est une lacune.

BirdWeather PUC est important parce qu'il combine deja :

- double micro ;
- Wi-Fi ;
- GPS ;
- capteurs environnementaux ;
- boitier weatherproof ;
- app mobile ;
- integration BirdNET/BirdWeather ;
- usage portable ou station fixe.

Mais il est aussi limite pour WildNexus :

- detections traitees cote serveur BirdWeather, pas a bord ;
- dependance cloud pour la detection ;
- pas de camera ;
- pas de LoRa/LPWAN terrain ;
- pas de logique multimodale image + audio + environnement ;
- pas de souverainete complete des donnees.

Verdict : BirdWeather PUC n'est pas un substitut a WildNexus, mais c'est un benchmark UX/produit incontournable.

### 3. "BirdNET a bord" est probablement faux si on parle ESP32 seul

L'ESP32-S3 peut faire de l'inference TinyML : keyword spotting, petits modeles image, detecteurs simples. Les videos ESP32 confirment que c'est interessant pour filtrer ou classifier des signaux simples.

Mais BirdNET complet est une autre classe de charge. BirdNET-Go annonce un usage Raspberry Pi 4 ou equivalent 64-bit, traitement local possible, modeles BirdNET/Perch/BattyBirdNET, sortie SQLite/MySQL, UI web et integration BirdWeather. Ce n'est pas un workload naturel pour ESP32.

Donc :

- ESP32 seul : bon pour veille, orchestration, capteurs, radio, declencheurs simples, buffers courts, event detection basique.
- Raspberry Pi / SBC / accelerateur : bon pour BirdNET-Go, analyse audio continue, modeles plus lourds.
- Architecture hybride : la plus realiste.

### 4. Les videos Raspberry Pi AI Camera sont tres utiles, mais pas une architecture finale telle quelle

Les projets IMX500 / Raspberry Pi montrent trois choses utiles :

- la camera intelligente peut faire de l'inference objet directement cote camera ;
- la logique evenementielle doit reduire les faux positifs et les ecritures inutiles ;
- l'audio est reconnu par les praticiens comme souvent meilleur que l'image pour oiseaux, chauves-souris et grenouilles.

Mais le Raspberry Pi permanent reste mauvais pour l'objectif WildNexus 60 jours batterie seule, sauf usage programme, solaire important, ou wake-on-event pilote par microcontroleur.

Conclusion : Raspberry Pi est excellent comme banc P1/P2 et comme module compute reveillable, mais il ne doit pas devenir le coeur toujours actif du noeud P0.

### 5. Les videos LLM sur ESP32 ne sont pas pertinentes pour WildNexus

Elles prouvent que l'on peut pousser un ESP32, mais pas que c'est utile ici. Un micro-LLM TinyStories ou un appel API ChatGPT via Wi-Fi n'apporte rien au noeud terrain. Cela consomme du temps mental et brouille les criteres.

A retenir seulement : ESP32-S3 + PSRAM + SIMD peut depasser l'usage IoT classique pour de petites inférences. A rejeter : toute idee de LLM embarque dans le produit.

## Architecture recommandee a figer

### Definition produit

WildNexus est une plateforme terrain d'observation ecologique multimodale.

Le noeud doit pouvoir combiner :

- image/video ;
- audio ;
- environnement ;
- temps ;
- position ;
- evenement ;
- qualite/confiance de detection ;
- donnees locales et transmissions faibles.

La valeur n'est pas le boitier. La valeur est la correlation propre entre modalites.

### Architecture technique cible

**Niveau A - Controleur basse consommation toujours actif**

- ESP32-S3, STM32U5 ou equivalent selon arbitrage final ;
- deep sleep ;
- PIR/radar/event sensor ;
- capteurs environnementaux ;
- RTC ;
- gestion energie ;
- LoRa/LoRaWAN ;
- reveil des sous-systemes.

**Niveau B - Modules reveillables**

- camera ;
- IR ;
- micro(s) ;
- stockage ;
- Wi-Fi local ;
- LTE-M optionnel ;
- SBC/accelerateur pour analyse lourde.

**Niveau C - Analyse locale differenciee**

- P0 : filtre animal/non-animal image + metadonnees propres ;
- P0bis : enregistrement audio + metadonnees + export, sans pretendre BirdNET embarque ;
- P1 : BirdNET-Go local sur module compute ou gateway ;
- P2 : multi-taxons, fusion image/audio/environnement, dashboard scientifique.

## Ce qui est interessant

1. BirdWeather PUC : excellent benchmark produit, app, UX terrain, "citizen science", GPS, capteurs, double micro.
2. BirdNET-Go : tres bon socle local pour station/gateway bioacoustique, surtout Raspberry Pi.
3. Raspberry Pi AI Camera IMX500 : utile pour prototypage vision edge et event logic.
4. PVPi / energie solaire : inspiration forte pour power management, MPPT, LiFePO4, scheduling.
5. Audio comme declencheur : strategiquement majeur pour oiseaux, chauves-souris, amphibiens.
6. Sons non oiseaux : pluie, vent, trafic, tronconneuse, activite humaine, chiens, coups de feu eventuels. Ce sont des variables ecologiques et contextuelles, pas du bruit pur.
7. Correlation multimodale : le vrai coeur de WildNexus.

## Ce qui est moins interessant ou dangereux

1. BirdNET complet sur ESP32 : probablement mauvais objectif technique.
2. Raspberry Pi toujours allume en noeud final : incompatible avec autonomie longue sans gros solaire.
3. LLM sur ESP32 : hors sujet produit.
4. LoRa mesh lourd : risque de collisions, duty-cycle EU868, complexite et consommation.
5. "Tout enregistrer tout le temps" : bon pour BirdWeather, mauvais pour WildNexus batterie si non maitrise.
6. App mobile native trop tot : le Wi-Fi local + PWA/interface web suffisent pour P0.
7. Figer P0 comme camera-only sans interface audio : erreur strategique.

## Conseils pour orienter les demarches futures

1. Recrire le document fondateur en placant WildNexus comme "multimodal ecological observation node", pas "camera trap augmentee".
2. Conserver P0 strict, mais ajouter un P0bis audio : micro(s), stockage audio court, timestamp, metadonnees, export, sans classification embarquee obligatoire.
3. Acheter ou tester BirdWeather PUC comme benchmark obligatoire, pas comme solution a copier.
4. Monter un banc BirdNET-Go Raspberry Pi separe, connecte au schema de donnees WildNexus.
5. Decider formellement : BirdNET embarque dans le noeud, dans une gateway, ou dans le backend local ? Ma recommandation : gateway/module compute reveillable pour P1.
6. Definir un schema evenement commun : image_event, audio_event, env_event, system_event.
7. Traiter les sons non oiseaux comme donnees utiles : meteo acoustique, activite humaine, perturbation, bruit de fond.
8. Ne pas choisir l'ESP32 par principe. Le garder comme controleur basse consommation, pas comme ordinateur universel.
9. Faire une matrice "modalite x energie x valeur scientifique" avant tout achat.
10. Refaire le scan concurrence avec quatre familles separees : camera traps connectes, bioacoustic recorders, edge AI wildlife cameras, plateformes citizen science.
11. Verifier les licences BirdNET, BirdNET-Go, Perch, eBird/Clements, BirdWeather avant usage commercial.
12. Prevoir une politique RGPD audio en plus de l'image : voix humaines, conversations, localisation.
13. Ne pas courir vers le mesh. Commencer par standalone + LoRa evenementiel + gateway.
14. Construire un prototype de correlation simple : un chant detecte reveille camera ou marque une fenetre video.
15. Documenter les hypotheses fausses explicitement : "BirdNET sur ESP32", "Raspberry Pi final always-on", "audio secondaire".

## Decision proposee

Je recommande de ne pas jeter le P0 existant, mais de le renommer et de l'encadrer :

- **P0-CAM** : preuve camera autonome basse consommation.
- **P0-AUDITIF** : preuve audio minimale, pas BirdNET complet embarque.
- **P1-FUSION** : correlation camera + audio + environnement.
- **P2-RESEAU** : ecosysteme distribue, app, API, cloud/local science.

La table doit etre bousculee sur la vision, pas sur la discipline d'execution.

