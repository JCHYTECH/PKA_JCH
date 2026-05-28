---
date: 2026-05-14
type: retro
author: [[Dobby]]
tags: [retro, gmail, oauth, workflow, organisation]
---

# Rétrospective — Gmail Gatekeeper [[Dobby]]

## Ce que nous avons mis en place

- Intégration Gmail fonctionnelle pour l'adresse dédiée de [[Dobby]].
- Flux strict de garde-barrière :
  - whitelist explicite des expéditeurs autorisés
  - élimination des autres messages sans lecture du corps
  - aucun traitement d'un mail autorisé sans accord explicite de JCH
  - import local du contenu et des pièces jointes seulement après instruction
- Watcher automatique `launchd` configuré avec un scan toutes les 20 minutes.

## Ce que nous avons appris

- Le bon modèle n'est pas une "boîte mail librement consultable", mais un canal d'entrée contrôlé.
- Le classement d'un email doit être déterminé par l'usage réel de son contenu, pas par association vague au projet.
- Le cas Niall Staines a confirmé qu'une référence d'esthétique et de post-traitement relève mieux de `06_PHOTO_NATURE/tech/editing` que d'`ARTEON`.

## Ce qui a ralenti la session

- Multiplication simultanée des variables Google :
  - projet cloud
  - client OAuth
  - test user
  - scopes
  - activation de l'API Gmail
- Erreur d'implémentation côté [[Dobby]] :
  - ouverture initiale de Chrome avec une URL OAuth différente de celle attendue par la librairie
  - conséquence : erreurs `mismatching_state`
- Changement de projet OAuth en cours de route (`jch-pka` vers `extended-argon-496307-j3`) sans verrouillage immédiat du contexte.

## Règles de fonctionnement à retenir

### Répartition des rôles

- JCH tient la main sur :
  - console cloud
  - création de projet
  - consentement navigateur
  - récupération éventuelle des fichiers client OAuth
- [[Dobby]] prend en charge :
  - scripts
  - configuration locale
  - validation technique
  - automatisation
  - exploitation opérationnelle après amorçage

### Protocole futur pour intégrations OAuth

Ordre recommandé :

1. créer ou sélectionner le projet cloud
2. configurer `Audience`
3. ajouter les `Test users`
4. créer le client OAuth `Desktop app`
5. activer l'API nécessaire
6. seulement ensuite lancer l'auth locale

### Taxonomie de classement

- `ARTEON` si la référence nourrit la curation, l'offre, les artistes ou le positionnement du projet
- `PHOTO_NATURE/tech/editing` si la référence nourrit les styles visuels, procédés de traitement, signatures esthétiques ou techniques d'image

## Décisions utiles prises

- Ajout de `jc.havaux@gmail.com` à la whitelist autorisée.
- Mode d'élimination des messages non autorisés : corbeille Gmail plutôt que suppression définitive.
- Scan automatique fixé à 20 minutes.

## Améliorations à envisager

- Rédiger une SOP courte `SETUP_GMAIL_DOBBY.md`
- Formaliser une taxonomie stable pour les imports mail utiles :
  - `tech/editing`
  - `tech/tools`
  - `market`
  - `legal`
  - `strategy`
  - `references/artists`
- Tenir un petit journal de décisions de classement pour homogénéiser les prochains imports

## Conclusion

- Le coût d'amorçage a été élevé, mais la chaîne est maintenant robuste et réutilisable.
- La leçon centrale est de séparer nettement :
  - l'amorçage plateforme
  - l'exploitation opérationnelle

