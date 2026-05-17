# WildNexus — Démarrage opérationnel

**Version :** v0.1  
**Date :** 2026-05-17  
**Statut :** Référence de démarrage  
**Propriétaire :** Jean-Claude Havaux — JCHYTECH  
**Pilotage :** Dobby 🦉

---

## 1. Objet

Ce document décrit ce que Dobby déclenche au moment où JCH donne le `go` pour démarrer réellement WildNexus.

Le principe de pilotage est le suivant :
- automatiser au maximum ce qui peut l'être ;
- produire des traces et des livrables dans le repo ;
- maintenir le suivi visible via la page web de pilotage et via le terminal ;
- ne solliciter JCH que lorsqu'un arbitrage réel est nécessaire.

---

## 2. Base de référence au démarrage

Au `go`, le projet démarre à partir des documents de référence suivants :
- `wildnexus-founding-document-v0.2.md`
- `wildnexus-plane-operating-model.md`
- `wildnexus-plane-seed-backlog.md`
- `wildnexus-usage-policy-and-license-principles.md`
- `wildnexus-usage-matrix.md`
- les `SKILL.md` des agents WildNexus retenus

Ces documents constituent la base de vérité initiale. Tant qu'un arbitrage explicite n'est pas pris, Dobby exécute à partir de ce socle.

---

## 3. Ce que Dobby fait immédiatement au `go`

### 3.1 Passage en mode exécution

Dobby passe WildNexus d'un projet cadré à un projet piloté en exécution documentaire, technique et opérationnelle.

Cela signifie :
- activation du backlog dans Plane ;
- lancement effectif de `WP01` ;
- production des premiers livrables de décision ;
- suivi visible et continu de l'avancement ;
- orchestration des agents cœur et agents support.

### 3.2 Noyau d'agents activés

Le noyau de travail activé en priorité est :
- `wildnexus-program-manager-system-architect`
- `wildnexus-embedded-platform-engineer`
- `wildnexus-power-systems-engineer`
- `wildnexus-mechanical-reliability-engineer`
- `wildnexus-imaging-systems-engineer`
- `wildnexus-scientific-data-protocols`

Agents support activés selon besoin :
- `wildnexus-edge-ai-cv`
- `wildnexus-rf-propagation`
- `wildnexus-industrialisation`
- `wildnexus-bioacoustics-dsp`

---

## 4. Séquence de démarrage

### 4.1 Immédiatement

Dobby déclenche :
- la synchronisation du backlog WildNexus dans Plane ;
- la vérification de l'état réel des items, milestones et dépendances ;
- l'ouverture de `WP01` comme chantier actif ;
- la création ou mise à jour des documents de travail nécessaires au premier cycle.

### 4.2 J+1

Les premiers fronts de travail sont :
- `T01.1` analyse comparative concurrents ;
- `T01.2` cadrage FTO / licence / exclusions d'usage ;
- `T01.3` préparation campagne RF terrain ;
- `T01.4` benchmark caméra IMX462 vs IMX327 ;
- `T01.5` arbitrage MCU.

### 4.3 Semaine 1-2

Dobby convertit les premières inconnues en décisions formelles :
- choix du modèle de diffusion `source-available / ethical-source`
- choix radio P0
- choix image P0
- choix MCU
- verrouillage du périmètre P0 strict

### 4.4 Objectif de la première phase

Le premier objectif de pilotage est :

> **M-01 — Architecture P0 gelée**

avec :
- FTO suffisamment cadré pour ne pas bloquer l'architecture ;
- standard radio retenu ;
- module caméra retenu ;
- MCU retenu ;
- périmètre P0 clarifié.

---

## 5. Automatisation maximale

Le projet doit être automatisé au maximum tant que cela n'affaiblit ni la qualité ni le contrôle.

### 5.1 Ce que Dobby automatise

Dobby automatise autant que possible :
- le seeding et la maintenance du backlog Plane ;
- le suivi des milestones, états et blocages ;
- la production de synthèses d'avancement ;
- la mise à jour des documents de travail dérivés ;
- l'archivage des preuves dans le repo ;
- l'identification des écarts entre documents de référence et exécution ;
- la remontée des blockers et décisions en attente.

### 5.2 Ce que Dobby ne t'impose pas manuellement

JCH ne doit pas avoir à :
- recopier des tâches dans Plane ;
- surveiller en continu les dépendances ;
- chercher lui-même les blockers dans les outils ;
- suivre à la main les livrables déjà produits ;
- relancer le projet sur des points de routine.

### 5.3 Principe d'autonomie opérationnelle

Par défaut :
- Dobby exécute ;
- les agents produisent ;
- le repo garde la trace ;
- la page web expose l'état ;
- le terminal sert aux notifications directes.

---

## 6. Sollicitation minimale de JCH

JCH ne doit être sollicité que dans les cas suivants :
- arbitrage stratégique réel ;
- choix juridique ou produit non déductible du cadre existant ;
- conflit entre non-négociables ;
- dépendance externe bloquante ;
- décision coût / délai / ambition qui change le projet de fond.

JCH ne doit pas être sollicité pour :
- des confirmations de routine ;
- des validations intermédiaires sans enjeu ;
- des questions déjà tranchées par les documents de référence ;
- des suivis de détail sans impact décisionnel.

---

## 7. Canaux de suivi et d'escalade

### 7.1 Page web de pilotage

La page web de pilotage doit devenir le point d'entrée visuel principal.

Elle doit afficher au minimum :
- état global du projet ;
- milestones et avancement ;
- tâches en cours ;
- décisions en attente ;
- blockers actifs ;
- risques prioritaires ;
- derniers livrables déposés.

Elle doit aussi servir de surface d'escalade :
- si un arbitrage JCH est requis, il doit y apparaître explicitement ;
- si un blocker critique survient, il doit être visible sans lecture du repo ;
- si une décision attend JCH, elle doit être isolée du bruit opérationnel.

### 7.2 Terminal

Le terminal reste le canal direct pour :
- les alertes critiques ;
- les confirmations d'exécution importantes ;
- les demandes d'arbitrage courtes ;
- les retours de contrôle rapides.

### 7.3 Règle de communication

La page web porte la vision consolidée.  
Le terminal porte les signaux immédiats.

Dobby doit utiliser les deux :
- page web pour la visibilité continue ;
- terminal pour la tension décisionnelle ou les événements bloquants.

---

## 8. Archivage et preuve

À chaque étape importante validée, Dobby s'assure que les éléments suivants sont déposés ou mis à jour dans `03_WILDNEXUS` :
- documents de décision ;
- rapports de benchmark ;
- notes RF ;
- matrices ;
- backlog structuré ;
- scripts ou automatisations associés ;
- code, si le chantier le nécessite.

Le repo est l'archive de référence.  
Plane est la couche d'exécution.  
La page web est la couche de lecture.  
Le terminal est la couche d'escalade.

---

## 9. Résumé exécutif

Au `go`, Dobby :
- initialise ou synchronise l'exécution dans Plane ;
- lance `WP01` sur les fronts critiques ;
- automatise le suivi au maximum ;
- centralise l'état sur la page web ;
- te remonte uniquement ce qui mérite réellement ton attention.

En une phrase :

> Dobby prend en charge le `comment`, l'exécution, le suivi et l'orchestration, pour que JCH intervienne seulement sur les vraies décisions.
