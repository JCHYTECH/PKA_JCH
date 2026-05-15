# Proposition: Memoire bornee utilisateur et projet

## Metadonnees

- id: `memory.bounded_user_project`
- statut: `APPROVED`
- proprietaire: `JCH`
- suggere_par: `assistant`
- date_creation: `2026-05-13`
- niveau_cout: `low`
- niveau_risque: `medium`

## Pourquoi

Le systeme doit conserver les informations stables sans reinjecter tout l'historique des conversations. Une memoire bornee permet de garder les preferences, conventions et decisions utiles tout en evitant l'accumulation floue.

Gain attendu: moins de repetitions, meilleure continuite, contexte plus fiable.

Risque evite: memoire infinie, obsolescence non controlee, personnalisation implicite non verifiable.

## Comment

Creer trois fichiers internes:

```text
memory/
  USER_PROFILE.md
  PROJECT_CONTEXT.md
  SYSTEM_MEMORY.md
```

Roles:

- `USER_PROFILE.md`: preferences de JCH, style attendu, contraintes personnelles stables.
- `PROJECT_CONTEXT.md`: contexte technique et operationnel du projet actif.
- `SYSTEM_MEMORY.md`: decisions transversales, conventions d'agent, limites, interdits.

Regles proposees:

- Taille limitee: 3 000 a 5 000 caracteres par fichier au depart.
- Entrees courtes, datees si necessaire.
- Aucune entree ajoutee sans validation de JCH.
- Revue mensuelle ou a chaque changement important.
- Les informations temporaires restent dans les notes de travail, pas dans la memoire.

## Cout

- Mise en place: faible, creation de fichiers et format.
- Maintenance: faible a moyenne, revue periodique.
- Cout API/infra: nul.
- Complexite: faible.

## Risques

- Information obsolete qui influence mal l'agent.
- Memoire trop generale, donc peu utile.
- Confusion entre preference stable et instruction temporaire.

Garde-fous:

- Taille limitee.
- Validation manuelle.
- Revue periodique.
- Historique conserve dans le workspace.

## Critere de validation

La brique est utile si l'assistant retrouve les preferences et conventions stables sans les redemander, tout en restant capable de signaler quand une information semble obsolete.

## Decision JCH

- decision: `approved`
- date_decision: `2026-05-13`
- commentaire: `Valide par JCH, avec revue ulterieure obligatoire pour verifier le format, la taille et l'utilite reelle de la memoire.`
