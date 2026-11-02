# YOLO sur [[ESP32]] pour détection d’oiseaux — WildNexus 2

[[wildnexus]]

Date : 2026-05-23

## Question de départ

YOLO pourrait-il être installé sur [[ESP32]] pour faire une détection d’oiseau dans X images extraites d’une vidéo stockée sur carte SD ?

## Réponse synthétique

Oui, mais pas de façon réaliste avec un vrai YOLO moderne sur [[ESP32]].

Sur un [[ESP32]] ou ESP32-CAM classique, YOLO est trop lourd : la mémoire RAM est très limitée, le processeur est lent pour de l’inférence image, et la taille des images utilisables est fortement contrainte. Même avec un [[ESP32-S3]] équipé de PSRAM, on reste dans le domaine de la TinyML très contrainte : modèle fortement réduit, quantifié, basse résolution et nombre de classes limité.

Pour le projet WildNexus, il faut distinguer trois niveaux :

1. [[ESP32]] seul : non recommandé pour YOLO réel.
2. [[ESP32-S3]] + PSRAM : envisageable pour un mini-modèle “oiseau / pas oiseau”, mais avec précision limitée.
3. [[Raspberry Pi]] : architecture recommandée pour YOLO, extraction d’images depuis vidéo et analyse plus fiable.

## Faisabilité sur [[ESP32]] classique

Un [[ESP32]] classique dispose de ressources trop limitées pour exécuter correctement YOLO.

Les contraintes principales sont :

- mémoire RAM très faible ;
- puissance CPU limitée ;
- pas de vrai GPU ou accélérateur IA ;
- traitement d’image lent ;
- difficulté à charger un modèle YOLO même réduit ;
- impossibilité pratique de traiter des images naturelles complexes avec précision.

Dans ce contexte, l’[[ESP32]] peut éventuellement servir à :

- déclencher une caméra ;
- gérer des capteurs environnementaux ;
- gérer l’énergie ;
- réveiller un système principal ;
- stocker des événements simples ;
- transmettre des données ;
- détecter un mouvement rudimentaire.

Mais il ne doit pas être considéré comme le processeur principal pour une vraie détection d’oiseaux par vision artificielle.

## Cas [[ESP32-S3]] avec PSRAM

L’[[ESP32-S3]] est plus intéressant car il peut disposer de PSRAM et d’instructions plus adaptées à certains traitements embarqués.

Il peut éventuellement exécuter :

- un modèle TinyML ;
- un modèle TensorFlow Lite Micro ;
- un modèle Edge Impulse ;
- une classification très simple ;
- un détecteur binaire “bird / no bird”.

Mais il faut accepter de fortes limites :

- images réduites, typiquement 96×96, 128×128 ou 160×160 pixels ;
- modèle quantifié en int8 ;
- faible nombre de classes ;
- temps d’inférence relativement long ;
- précision variable en conditions naturelles ;
- difficulté avec arrière-plans complexes, branches, feuilles, contre-jour, oiseaux partiellement visibles.

Donc l’[[ESP32-S3]] pourrait servir à faire un préfiltrage, mais pas à produire une détection fiable de type YOLO moderne.

## Détection dans X images extraites d’une vidéo

Le scénario envisagé est :

1. une vidéo est enregistrée sur carte SD ;
2. X images sont extraites de cette vidéo ;
3. chaque image est analysée ;
4. le système décide si un oiseau est présent ;
5. les images positives sont conservées ou transmises.

Sur [[ESP32]], ce flux est problématique, car :

- décoder une vidéo est déjà coûteux ;
- extraire des frames demande du CPU et de la mémoire ;
- analyser ensuite les images avec un modèle IA est encore plus lourd ;
- la carte SD ajoute des accès lents ;
- la consommation énergétique augmente fortement.

Le traitement vidéo + extraction de frames + YOLO n’est donc pas une bonne mission pour l’[[ESP32]].

## Architecture recommandée pour WildNexus

La meilleure architecture est hybride.

### Rôle de l’[[ESP32]]

L’[[ESP32]] doit gérer les fonctions légères :

- gestion de l’énergie ;
- mise en veille et réveil ;
- capteurs environnementaux ;
- température ;
- humidité ;
- luminosité ;
- détection PIR éventuelle ;
- horloge ;
- bouton utilisateur ;
- Wi-Fi local pour téléchargement ;
- communication avec le module principal ;
- watchdog et redémarrage si blocage.

### Rôle du [[Raspberry Pi]]

Le [[Raspberry Pi]] doit gérer les fonctions lourdes :

- caméra ;
- enregistrement vidéo ;
- lecture de la carte SD ;
- extraction de frames ;
- analyse image ;
- YOLO ou modèle équivalent ;
- [[BirdNET]] ou BirdNET-Go pour l’audio ;
- stockage structuré des résultats ;
- interface locale ;
- synchronisation éventuelle vers cloud.

### Rôle éventuel du cloud

Le cloud peut être utilisé pour :

- analyse lourde ;
- revalidation des images douteuses ;
- entraînement ou amélioration des modèles ;
- centralisation des données ;
- tableau de bord ;
- partage scientifique ou naturaliste.

Mais le cloud ne doit pas être obligatoire si l’objectif est de garder un appareil de terrain autonome.

## Décision technique

Pour WildNexus, la décision recommandée est :

- ne pas installer YOLO sur [[ESP32]] comme moteur principal ;
- utiliser l’[[ESP32]] comme microcontrôleur de terrain ;
- utiliser un [[Raspberry Pi]] Zero 2 W, [[Raspberry Pi]] 4 ou [[Raspberry Pi 5]] pour l’analyse image ;
- réserver l’[[ESP32-S3]] à un éventuel prototype de préfiltrage très simple ;
- garder YOLO sur [[Raspberry Pi]] ou cloud.

## Options possibles

### Option A — [[ESP32]] seul

Non recommandée.

Usage possible :

- capture simple ;
- détection PIR ;
- prise d’image ;
- stockage brut ;
- transmission.

Limite :

- pas de vraie détection fiable d’oiseaux.

### Option B — [[ESP32-S3]] avec modèle TinyML

Possible pour expérimentation.

Usage possible :

- classification “oiseau / pas oiseau” ;
- détection très simplifiée ;
- préfiltrage avant transmission.

Limite :

- précision limitée ;
- modèle à entraîner spécifiquement ;
- faible résolution ;
- performances incertaines en forêt.

### Option C — [[ESP32]] + [[Raspberry Pi]]

Recommandée.

Usage possible :

- [[ESP32]] pour gestion bas niveau ;
- [[Raspberry Pi]] pour caméra, vidéo, IA, audio et stockage ;
- analyse locale plus fiable ;
- architecture évolutive.

### Option D — [[ESP32]] + [[Raspberry Pi]] + Cloud

Recommandée pour version avancée.

Usage possible :

- appareil autonome sur le terrain ;
- préanalyse locale ;
- analyse lourde dans le cloud ;
- amélioration progressive des modèles ;
- dashboard centralisé.

## Conclusion

YOLO sur [[ESP32]] n’est pas la bonne voie pour WildNexus si l’objectif est une détection fiable d’oiseaux dans des images extraites d’une vidéo.

L’[[ESP32]] doit rester un contrôleur intelligent de terrain, sobre et robuste. La vision artificielle sérieuse doit être confiée à un [[Raspberry Pi]] ou à un service cloud.

La meilleure architecture pour WildNexus est donc :

[[ESP32]] = énergie, capteurs, réveil, Wi-Fi local  
[[Raspberry Pi]] = vidéo, extraction d’images, YOLO, [[BirdNET]]  
Cloud = analyse avancée optionnelle et centralisation

## Formule de décision

Si l’objectif est simplement de savoir qu’un événement a eu lieu : [[ESP32]] possible.

Si l’objectif est de savoir s’il y a probablement un oiseau : [[ESP32-S3]] possible mais expérimental.

Si l’objectif est de détecter correctement un oiseau dans des images naturelles : [[Raspberry Pi]] recommandé.

Si l’objectif est d’identifier, classer, archiver et exploiter les données : [[Raspberry Pi]] + cloud recommandé.
