# SOP — Email Import And Classification

## But

Standardiser la réception, le filtrage, l'ouverture, l'import et le classement des emails utiles à PKA.

## Agents concernés

- [[Dobby]] : arbitrage, feu vert utilisateur, classement final
- [[Pie]] : lecture, qualification, typologie du contenu
- [[Corbeau]] : capitalisation durable si le contenu devient connaissance récurrente
- [[Forge]] : tuyauterie d'import et automatisation

## Principe

- La boîte mail de [[Dobby]] est un canal d'entrée contrôlé
- Les expéditeurs non autorisés sont éliminés sans lecture du corps
- Les emails autorisés ne sont pas ouverts sans accord explicite de JCH
- Le contenu n'est importé localement qu'après instruction

## Préflight obligatoire

Avant toute exploitation :

- vérifier que l'expéditeur fait partie de la whitelist active
- vérifier que l'email est bien en statut `pending_user_instruction`
- vérifier que JCH a explicitement dit quand le traiter
- vérifier si des pièces jointes sont attendues ou probables

## Pipeline

1. Scan de la boîte
2. Filtrage par whitelist expéditeur
3. Élimination des expéditeurs non autorisés
4. Mise en attente des emails autorisés
5. Demande à JCH : traiter maintenant / plus tard
6. Import local du mail et des pièces jointes
7. Lecture et qualification du contenu
8. Classement au bon emplacement
9. Conservation d'un import brut traçable

## Protocole de décision

### Étape 1 — autorisation

[[Dobby]] demande toujours :
- faut-il le traiter ?
- faut-il le traiter maintenant ou plus tard ?

### Étape 2 — qualification

[[Pie]] ou [[Dobby]] qualifie le mail selon son usage dominant :
- action à faire
- référence à conserver
- information ponctuelle
- [[archive]] simple

### Étape 3 — destination

Le dossier cible est choisi selon le futur usage réel du contenu.

## Règle d'ouverture

Avant toute lecture d'un mail autorisé, [[Dobby]] demande explicitement à JCH s'il faut le traiter.

## Règle de classement

Le classement se fait par usage final du contenu, pas par association vague.

## Questions de classement

Avant de ranger, déterminer :

1. Ce contenu sert-il à un projet précis ?
2. Sert-il à la stratégie, au légal, au marché, à la technique, à l'édition, à la création, ou à l'[[archive]] ?
3. Va-t-il être réutilisé comme référence durable ?
4. Son intérêt est-il métier, artistique, technique ou administratif ?
5. Son usage principal est-il de décider, d'exécuter, d'inspirer ou de documenter ?

## Heuristiques utiles

### Classer dans ARTEON si

- la matière nourrit la curation
- la matière nourrit le positionnement ou l'offre
- la matière concerne un artiste, un service, un cadre éditorial, une logique de galerie

### Classer dans `PHOTO_NATURE/tech/editing` si

- la matière nourrit le post-traitement
- la matière documente un style visuel
- la matière éclaire une signature artistique de rendu
- la matière concerne les procédés d'image ou d'édition

### Classer dans `research` si

- le contenu sert surtout de référence à consulter
- il n'appelle pas d'action opérationnelle immédiate
- il doit rester retrouvable comme source d'inspiration, benchmark ou documentation

### Classer dans `content` si

- le contenu est déjà une matière à transformer en texte, publication, fiche ou corpus éditorial

### Classer en `admin` ou `legal` si

- le document fait foi
- la valeur réside dans sa portée administrative, juridique ou contractuelle
- l'original et sa traçabilité priment sur la synthèse

### Classer en `market`, `legal`, `strategy`, `admin` si

- l'usage dominant est explicitement commercial, juridique, stratégique ou administratif

## Anti-patterns à éviter

- classer par intuition de projet sans lire l'usage réel du contenu
- laisser un import utile dans `00_INBOX`
- produire une synthèse sans conserver l'import brut
- ranger une référence visuelle dans une zone business par simple proximité thématique
- ouvrir un mail autorisé sans feu vert explicite de JCH

## Sorties obligatoires

- une note synthétique utile
- un import brut conservé
- un emplacement final clair

## Convention recommandée

- note synthétique : `YYYY-MM-DD_<slug>_reference.md`
- import brut : `YYYY-MM-DD_<slug>_import/`

## Règle de traçabilité

La note synthétique doit toujours mentionner :
- source email
- date
- expéditeur
- objet
- chemin de l'import brut

## Contrôle qualité avant clôture

Avant de considérer le traitement terminé, vérifier :

1. le mail n'est plus ambigu quant à son statut
2. le dossier final est cohérent avec l'usage principal
3. l'import brut est conservé
4. la synthèse est exploitable sans rouvrir l'email
5. JCH peut retrouver le contenu sans connaître l'ID Gmail

## Sortie attendue à l'écran

[[Dobby]] doit toujours restituer à JCH :

- ce qui a été fait
- où le contenu a été rangé
- pourquoi ce dossier a été choisi
- quelle règle de classement cela renforce pour l'avenir

## Amélioration continue

Quand un classement semble ambigu, JCH tranche.
La décision devient une règle implicite pour les prochains cas similaires.
