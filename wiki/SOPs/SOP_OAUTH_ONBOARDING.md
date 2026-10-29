# SOP — OAuth Onboarding Plateforme Externe

## But

Standardiser l'amorçage d'une intégration OAuth entre une plateforme externe (Google, Microsoft, Meta, etc.) et le système PKA.

## Agents concernés

- [[Dobby]] : orchestration, séquencement, validation finale
- [[Ariane]] : guidage pas-à-pas de plateforme et onboarding
- [[Forge]] : intégration locale, scripts, tests, automatisation

## Principe de répartition

### JCH

JCH garde la main sur :
- console cloud propriétaire
- création ou sélection du projet
- consentement navigateur
- téléchargement éventuel du fichier client OAuth

### [[Dobby]] / équipe

[[Dobby]] et l'équipe prennent en charge :
- préparation locale
- scripts et configuration
- vérification technique
- relance auth locale
- tests fonctionnels
- automatisation

## Préflight obligatoire

Avant de commencer, verrouiller noir sur blanc :

- compte externe qui doit se connecter
- nom exact du projet cloud visé
- API cible à activer
- type de client OAuth attendu
- emplacement local de `credentials.json`
- emplacement local de `token.json`

Si un de ces points est flou, ne pas lancer l'auth locale.

## Ordre obligatoire

1. Identifier le bon compte externe
2. Créer ou sélectionner le bon projet cloud
3. Configurer l'écran de consentement / audience
4. Définir le statut de test si nécessaire
5. Ajouter les test users
6. Créer le client OAuth adapté
7. Activer l'API nécessaire
8. Installer ou remplacer le fichier `credentials.json` local
9. Supprimer les anciens tokens si le client ou les scopes ont changé
10. Lancer l'auth locale
11. Vérifier les scopes réels obtenus
12. Lancer un test fonctionnel réel

## Protocole d'exécution

### Phase 1 — cadrage

- [[Dobby]] annonce explicitement :
  - ce que JCH doit faire dans la console
  - ce que l'équipe fera localement
- [[Ariane]] donne le chemin exact dans l'interface cloud

### Phase 2 — plateforme

- JCH réalise les actions console
- [[Dobby]] ne suppose rien : il demande confirmation après chaque jalon critique
  - audience
  - test user
  - client OAuth
  - activation API

### Phase 3 — local

- [[Forge]] remplace les credentials si nécessaire
- [[Forge]] supprime les tokens obsolètes si client ou scopes modifiés
- [[Forge]] relance une auth locale propre

### Phase 4 — validation

- [[Dobby]] vérifie :
  - auth réussie
  - API joignable
  - action réelle réussie
  - automatisation saine si prévue

## Checklist minimale Google

- Projet correct sélectionné
- `Audience` : `External` si compte hors organisation
- `Publishing status` : `Testing` si app non vérifiée
- `Test users` : compte cible bien ajouté
- Client OAuth : `Desktop app` si flux local
- API activée : ex. Gmail API, Calendar API
- Nouveau `credentials.json` installé si client recréé
- `token.json` supprimé si client/scopes modifiés

## Checklist minimale Microsoft / Meta

- tenant / organisation correct(e)
- application enregistrée
- redirect URI adaptée au flux local
- permissions API déclarées
- consentement administrateur si requis
- compte cible autorisé
- secret / certificat local cohérent avec l'app enregistrée

## Règles de sécurité

- Ne jamais supposer que le projet cloud visible est le bon
- Ne jamais supposer qu'un ancien token reste valide après changement de client
- Ne jamais contourner le flux natif OAuth d'une librairie sans nécessité forte
- Vérifier d'abord les scopes et l'activation API avant d'accuser un bug code
- Ne jamais mélanger plusieurs projets cloud actifs dans la même tentative sans l'annoncer explicitement
- Ne jamais réutiliser un ancien onglet de consentement après une relance d'auth

## Anti-patterns à éviter

- lancer l'auth locale avant d'avoir ajouté le test user
- déboguer le code alors que l'API n'est pas activée
- garder un ancien token après changement de client OAuth
- ouvrir manuellement une URL OAuth différente de celle attendue par la librairie
- raisonner sur le "nom du projet historique" au lieu du projet réellement porté par `credentials.json`

## Symptômes fréquents

### `403 access_denied`

Causes probables :
- test user absent
- mauvais compte connecté
- mauvais projet cloud

### `invalid_grant`

Causes probables :
- token expiré
- token révoqué
- client remplacé

### `insufficient authentication scopes`

Cause probable :
- consentement OAuth effectué sans les scopes requis

### `API not enabled`

Cause probable :
- API non activée sur le projet du client OAuth réellement utilisé

### `mismatching_state`

Cause probable :
- ancien onglet OAuth réutilisé
- flux navigateur non aligné avec la session locale attendue

## Questions de diagnostic prioritaires

En cas d'échec, poser dans cet ordre :

1. Quel compte est connecté dans le navigateur ?
2. Quel projet cloud porte le `client_id` local ?
3. Le test user est-il ajouté sur ce projet précis ?
4. L'API visée est-elle activée sur ce projet précis ?
5. Le token local a-t-il été régénéré après changement de client ou de scope ?
6. La tentative navigateur en cours correspond-elle bien à la session locale ouverte maintenant ?

## Fin de procédure

L'onboarding n'est considéré terminé que si :
- l'auth locale réussit
- un test réel passe
- l'automatisation éventuelle démarre
- le chemin des secrets et le projet source sont documentés

## Sortie attendue

Une note de fin de setup doit conserver :

- projet cloud utilisé
- compte cible connecté
- API activées
- chemin local des credentials
- chemin local du token
- scopes demandés
- date du dernier test réel
