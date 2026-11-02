# EventNET — Indice de pollution sonore anthropique V1

**Date :** 2026-06-03  
**Projet :** [[WildNexus]] / [[EventNET]]  
**Owner orchestration :** [[Dobby]]  
**Specialistes mobilises :** [[Clio]], [[Chouette]], [[Forge]]  
**Statut :** design mis a jour pour plan d'implementation

## Objectif

Etendre l'EventNET actuel du [[Raspberry Pi]] BirdNET-Pi pour produire un indice de pollution sonore anthropique utile au monitoring wildlife.

La detection des bruits anthropiques est un moyen, pas le livrable principal. Le livrable principal est un score simple, lisible et historisable qui indique a quel point l'environnement sonore d'une fenetre temporelle est perturbe par des sources humaines.

La V1 doit rester simple : reutiliser YAMNet TFLite, le flux WAV BirdNET existant, la base SQLite `events.db` et le dashboard PHP actuel. Elle ne modifie pas le satellite [[WildNexus]] P0 et ne deplace aucune inference vers l'ESP32.

## Perimetre V1

Classes anthropiques a surveiller :

- avion ;
- voiture / moteur routier ;
- voix humaine ;
- chien / aboiement ;
- tronconneuse.

Indice V1 :

- `anthropic_noise_score` : score 0-100 par fenetre temporelle ;
- `anthropic_noise_level` : `none`, `low`, `moderate`, `high` ;
- `dominant_anthropic_source` : source dominante sur la fenetre ;
- `anthropic_event_count` : nombre d'evenements anthropiques detectes ;
- `max_anthropic_score` : score YAMNet maximum observe sur la fenetre.

Hors V1 :

- entrainement ou fine-tuning YAMNet ;
- reconnaissance d'especes ;
- marquage automatique des detections BirdNET comme invalides ;
- nouveaux services systemd separes ;
- analyse temps reel depuis le micro en concurrence avec BirdNET.
- mesure acoustique calibree en dB SPL ou LAeq, car le micro BirdNET-Pi n'est pas calibre ;
- indice reglementaire de bruit urbain.

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

Un module d'agregation calcule ensuite un indice par fenetre temporelle fixe, recommande en V1 a 15 minutes. Cette granularite evite de sur-interpreter un seul WAV, reste lisible sur le terrain, et permet des courbes jour/nuit exploitables.

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

Une nouvelle table SQLite `noise_index` stocke l'indice :

- `id INTEGER PRIMARY KEY AUTOINCREMENT` ;
- `window_start TEXT NOT NULL` ;
- `window_end TEXT NOT NULL` ;
- `anthropic_noise_score REAL NOT NULL` ;
- `anthropic_noise_level TEXT NOT NULL` ;
- `dominant_anthropic_source TEXT` ;
- `anthropic_event_count INTEGER NOT NULL` ;
- `max_anthropic_score REAL NOT NULL` ;
- `weather_event_count INTEGER NOT NULL` ;
- `sample_count INTEGER NOT NULL` ;
- `created_at TEXT NOT NULL`.

La clef logique est la fenetre temporelle `window_start` / `window_end`. Si une fenetre est recalculee, la ligne existante est remplacee.

## Seuils

Le service actuel utilise `--threshold 0.15`. La V1 conserve ce comportement par defaut pour ne pas casser le deploiement existant.

Le code doit cependant permettre d'introduire des seuils par groupe ou par classe ensuite. La premiere implementation peut rester a seuil global si elle isole clairement la taxonomie.

Pour l'indice V1, la formule est volontairement explicable :

```text
raw = (max_anthropic_score * 70) + min(anthropic_event_count, 6) * 5
anthropic_noise_score = min(100, round(raw))
```

Niveaux :

- `none` : 0 ;
- `low` : 1-29 ;
- `moderate` : 30-59 ;
- `high` : 60-100.

Cette formule privilegie l'intensite du signal YAMNet tout en tenant compte de la recurrence. Elle n'est pas une mesure physique de bruit ; c'est un indice de perturbation anthropique pour contexte wildlife.

## Dashboard

`eventnet.php` affiche :

- les cartes meteo existantes ;
- un bloc equivalent pour les evenements anthropiques ;
- l'indice de pollution sonore anthropique courant ;
- les dernieres fenetres d'indice ;
- les 30 derniers evenements avec badge de groupe ;
- le total par groupe.

Le dashboard reste auto-rafraichi, sans dependance front-end nouvelle.

## Qualite scientifique et terrain

Les detections anthropiques servent d'abord de contexte acoustique pour interpreter l'activite wildlife. Une detection forte d'avion, moteur, voix, aboiement ou tronconneuse sur le meme segment qu'une detection BirdNET pourra alimenter plus tard un statut "a verifier".

En V1, cette interaction reste documentaire : EventNET logue le bruit anthropique mais ne modifie pas la base BirdNET.

L'indice doit toujours etre presente comme un proxy non calibre. Il permet de comparer des periodes sur le meme site et le meme materiel, pas de produire une mesure absolue de pollution sonore au sens reglementaire.

## Risques

- YAMNet peut confondre vent fort, pluie intense, moteur lointain et avion.
- Les voix humaines peuvent etre peu fiables selon distance et reverberation.
- Les classes chien et aboiement peuvent se chevaucher ; la V1 doit accepter plusieurs MIDs pour un meme libelle francais.
- Les scores bas generent du bruit. Les seuils devront etre ajustes apres observation terrain.
- Un indice 0-100 peut donner une fausse impression de precision. Le dashboard doit afficher le niveau qualitatif autant que le nombre.
- Une fenetre sans detection anthropique n'est pas necessairement silencieuse ; elle signifie seulement qu'aucune classe cible n'a depasse le seuil.

## Verification attendue

- `eventnet_detect.py --stats` fonctionne avec l'ancienne base et affiche les groupes.
- `eventnet_detect.py --once <wav>` peut analyser un fichier WAV sans erreur.
- La migration SQLite n'efface pas les evenements existants.
- `eventnet.php` reste lisible si aucun evenement anthropique n'est encore detecte.
- Le calcul d'indice produit `none`, `low`, `moderate` et `high` sur des jeux d'evenements controles.
- Le dashboard affiche le dernier indice et les dernieres fenetres sans dependance externe.

## Voir aussi

- [[WILDNEXUS_P0_SCOPE_LOCK]]
- [[ADR-007-detection-evenementielle-p0]]
- [[2026-05-30-session-deepseek-eventnet-wildnexus]]
