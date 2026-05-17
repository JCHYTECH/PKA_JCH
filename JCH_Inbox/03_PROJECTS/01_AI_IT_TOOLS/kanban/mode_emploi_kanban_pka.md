# Mode d'emploi Kanban PKA

## Acces

Ouvrir la vue kanban ici :

- `JCH_Inbox/01_DASHBOARDS/kanban.html`

Depuis le hub, cliquer sur :

- `Liste Kanban`

## Ce que montre la vue

La page affiche une liste transversale des cartes normalisees depuis Plane.

Chaque carte montre :

- le titre
- le projet
- le statut
- l'owner
- la description
- les labels

## Filtres disponibles

En haut de page :

- `Projet`
- `Statut`
- `Owner`
- `Attente JCH uniquement`

Chaque changement de filtre recharge automatiquement la liste.

## Lecture des signaux

- bord rouge : carte bloquee, typiquement `En attente`
- bord ocre : carte en attente JCH
- puces : projet, statut, owner, puis labels

## Usage quotidien recommande

### 1. Vue globale

Ouvrir la page sans filtre.

But :

- sentir le volume du moment
- voir quels owners sont actifs
- repérer les cartes qui dominent visuellement

### 2. Attente JCH

Cocher `Attente JCH uniquement`.

C'est la vue prioritaire pour JCH.

Elle sert a voir ce qui attend :

- un arbitrage
- une validation
- un go
- une decision de reprise

### 3. Blocages

Decocher `Attente JCH uniquement`, puis choisir :

- `Statut = En attente`

But :

- voir ce qui est bloque
- distinguer ce qui stagne de ce qui avance

### 4. Focus projet

Passer projet par projet :

- `02_ARTEON`
- `03_WILDNEXUS`
- `08_VETALYX`
- autres projets actifs selon besoin

But :

- voir si un projet derive
- voir s'il accumule trop de cartes
- voir s'il manque de mouvement

### 5. Charge par owner

Utiliser le filtre `Owner`.

But :

- repérer la surcharge
- repérer la dispersion
- repérer les cartes mal attribuees
- voir qui porte trop de sujets en parallele

## Ordre de lecture conseille chaque jour

1. `Attente JCH uniquement`
2. `Statut = En attente`
3. revue rapide par projet
4. revue rapide par owner

## Rituel quotidien minimal

### Matin

- verifier les cartes en attente JCH
- verifier les blocages
- choisir ou mettre l'energie du jour

### Soir

- verifier si les cartes JCH ont ete debloquees
- voir si de nouveaux blocages sont apparus
- repérer les projets qui accumulent sans fermeture

## Rituel hebdomadaire

Une fois par semaine :

- revue projet par projet
- revue par owner
- repérage des cartes qui restent trop longtemps en `En attente`
- repérage des cartes qui restent trop longtemps en `En validation`

## Ce qu'il faut surveiller

Chercher en priorite :

- cartes en attente JCH qui trainent
- cartes bloquees sans action claire
- owners avec trop de dispersion
- projets avec trop de cartes ouvertes et peu de progression

## Limites actuelles de la vue

Pour l'instant, la vue est en lecture seule.

Elle ne permet pas encore :

- creer une carte
- modifier un statut
- changer un owner
- ecrire dans Plane

## Suite logique

Les evolutions naturelles seront :

- actions directes depuis la vue
- changement de statut
- reassignation owner
- write-back vers Plane
