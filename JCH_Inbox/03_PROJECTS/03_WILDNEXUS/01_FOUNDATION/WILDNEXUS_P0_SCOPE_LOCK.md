# WildNexus — Verrou de périmètre P0

**Version :** v0.1  
**Date :** 2026-05-18  
**Statut :** Pré-go opérationnel  
**Owner :** Dobby  

## 1. Objet

Ce document verrouille le périmètre P0 pour éviter que les composants déjà documentés mais non critiques ne diluent l'exécution du premier prototype.

Le principe est simple : P0 doit prouver un nœud caméra autonome crédible, pas toute la plateforme WildNexus finale.

## 2. P0 engagé

P0 couvre uniquement :

- un nœud caméra autonome ;
- capture image exploitable de jour et de nuit ;
- détection événementielle ;
- filtre embarqué animal / non-animal ;
- transmission LPWAN événementielle de métadonnées ou alerte ;
- stockage local ;
- configuration terrain simple ;
- autonomie minimale de 60 jours batterie seule, validée par EVT 30 jours avec extrapolation ;
- boîtier terrain IP67 ;
- documentation suffisante pour compiler, flasher et reproduire le socle.

## 3. Hors P0 explicite

Ces éléments sont hors P0, sauf contrainte d'interface minimale :

| Sujet | Statut | Raison |
|---|---|---|
| Bioacoustique | P1 deferred | Travail sérieux existant, mais non nécessaire pour prouver le nœud caméra P0 |
| Faune Autour PWA | Projet adjacent ou P2 | Application utile, mais non requise pour prototype caméra P0 |
| Reconnaissance espèce fine | P1 | P0 se limite au filtre animal / non-animal |
| Reconnaissance individuelle | P1/P2 | Valeur forte mais dépend d'un corpus et de modèles plus avancés |
| Réseau public de stations | P2 | Requiert gouvernance, sécurité, communauté et exploitation de données |
| Bioacoustique multi-taxons | P2 | Complexité scientifique et DSP non nécessaire au premier jalon |
| Cloud scientifique complet | P2 | Ne doit pas précéder la preuve terrain |
| App native iOS/Android | Hors scope | PWA ou interface web suffisante pour les besoins initiaux |

## 4. Interfaces à préserver en P0

P0 ne développe pas les modules P1/P2, mais doit éviter de les bloquer :

- port ou bus d'extension capteur documenté ;
- schéma de métadonnées extensible ;
- horodatage et géolocalisation propres ;
- séparation claire entre capture, détection, stockage et transmission ;
- possibilité future d'ajouter événement acoustique ou environnemental sans refonte complète.

## 5. Relation avec les composants existants

### 03.01 BIOACOUSTIC

Le répertoire bioacoustique est conservé comme matière P1. Il ne doit pas créer de tâche bloquante pour M-01, M-02 ou M-03, sauf si une décision d'interface P0 doit être prise pour ne pas fermer l'extension future.

### 03.02 FAUNE_AUTOUR_APP

Faune Autour est un projet adjacent à forte synergie. Il peut devenir une interface ou une extension WildNexus en P2, mais n'est pas un livrable P0. Son évolution ne doit pas bloquer le prototype caméra.

## 6. Critère anti-scope-creep

Toute proposition ajoutant une capacité P1/P2 à P0 doit répondre à trois questions :

1. Cette capacité est-elle nécessaire pour prouver le nœud caméra autonome ?
2. Son absence rend-elle M-03 invalide ?
3. Peut-elle être remplacée par une interface ou une hypothèse documentée ?

Si les réponses ne justifient pas clairement l'inclusion, la capacité reste hors P0.

## 7. Décision actuelle

Statut recommandé : P0 strict.

Le `go` opérationnel porte sur WP01 à WP06 tels que cadrés dans le document fondateur, avec les exclusions explicites ci-dessus.
