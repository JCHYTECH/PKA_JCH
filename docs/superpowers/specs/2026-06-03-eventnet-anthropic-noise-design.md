# EventNET — Detection de bruit anthropique V1

**Date :** 2026-06-03  
**Projet :** [[WildNexus]] / [[EventNET]]  
**Owner orchestration :** [[Dobby]]  
**Specialistes mobilises :** [[Clio]], [[Chouette]], [[Forge]]  
**Statut :** design approuve pour plan d'implementation

## Objectif

Etendre l'EventNET actuel du [[Raspberry Pi]] BirdNET-Pi pour detecter les bruits anthropiques de base en plus des evenements meteo acoustiques deja suivis.

La V1 doit rester simple : reutiliser YAMNet TFLite, le flux WAV BirdNET existant, la base SQLite `events.db` et le dashboard PHP actuel. Elle ne modifie pas le satellite [[WildNexus]] P0 et ne deplace aucune inference vers l'ESP32.

## Perimetre V1

Classes anthropiques a surveiller :

- avion ;
- voiture / moteur routier ;
- voix humaine ;
- chien / aboiement ;
- tronconneuse.

Hors V1 :

- entrainement ou fine-tuning YAMNet ;
- reconnaissance d'especes ;
- marquage automatique des detections BirdNET comme invalides ;
- nouveaux services systemd separes ;
- analyse temps reel depuis le micro en concurrence avec BirdNET.

## Architecture

Flux conserve :

```text
BirdNET StreamData/*.wav
  -> eventnet_detect.py
  -> YAMNet TFLite
  -> events.db
  -> eventnet.php
```

`eventnet_detect.py` charge une seule fois YAMNet et analyse chaque WAV ferme par BirdNET dans `StreamData/`. Les classes cible sont regroupees dans une taxonomie unique avec un champ `event_group` :

- `weather` pour les classes meteo existantes ;
- `anthropic` pour les nouvelles classes de bruit humain.

## Donnees

La table SQLite `events` garde les colonnes existantes et ajoute :

- `event_group TEXT NOT NULL DEFAULT 'weather'`

La migration est automatique au demarrage : si la colonne n'existe pas, le script l'ajoute sans supprimer les donnees historiques.

Chaque ligne d'evenement conserve :

- timestamp ;
- AudioSet MID ;
- nom francais ;
- nom anglais YAMNet ;
- score ;
- fichier source ;
- duree du WAV ;
- groupe `weather` ou `anthropic`.

## Seuils

Le service actuel utilise `--threshold 0.15`. La V1 conserve ce comportement par defaut pour ne pas casser le deploiement existant.

Le code doit cependant permettre d'introduire des seuils par groupe ou par classe ensuite. La premiere implementation peut rester a seuil global si elle isole clairement la taxonomie.

## Dashboard

`eventnet.php` affiche :

- les cartes meteo existantes ;
- un bloc equivalent pour les evenements anthropiques ;
- les 30 derniers evenements avec badge de groupe ;
- le total par groupe.

Le dashboard reste auto-rafraichi, sans dependance front-end nouvelle.

## Qualite scientifique et terrain

Les detections anthropiques servent d'abord de contexte acoustique. Une detection forte d'avion, moteur, voix, aboiement ou tronconneuse sur le meme segment qu'une detection BirdNET pourra alimenter plus tard un statut "a verifier".

En V1, cette interaction reste documentaire : EventNET logue le bruit anthropique mais ne modifie pas la base BirdNET.

## Risques

- YAMNet peut confondre vent fort, pluie intense, moteur lointain et avion.
- Les voix humaines peuvent etre peu fiables selon distance et reverberation.
- Les classes chien et aboiement peuvent se chevaucher ; la V1 doit accepter plusieurs MIDs pour un meme libelle francais.
- Les scores bas generent du bruit. Les seuils devront etre ajustes apres observation terrain.

## Verification attendue

- `eventnet_detect.py --stats` fonctionne avec l'ancienne base et affiche les groupes.
- `eventnet_detect.py --once <wav>` peut analyser un fichier WAV sans erreur.
- La migration SQLite n'efface pas les evenements existants.
- `eventnet.php` reste lisible si aucun evenement anthropique n'est encore detecte.

## Voir aussi

- [[WILDNEXUS_P0_SCOPE_LOCK]]
- [[ADR-007-detection-evenementielle-p0]]
- [[2026-05-30-session-deepseek-eventnet-wildnexus]]
