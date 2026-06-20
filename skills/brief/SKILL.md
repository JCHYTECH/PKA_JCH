---
name: brief
description: Générer un brief structuré pour déléguer une tâche à un membre de l'équipe PKA. Version PKA améliorée (shadow du skill fondation) avec priority et deadline.
---

# /brief — Génération de brief

Génère un brief clair et complet pour déléguer une tâche à un spécialiste PKA.

> **Version PKA** — ajout des champs `priority` et `deadline`.

## Usage

```
/brief <membre> <tâche>
/brief Forge "créer endpoint API certification badge"
/brief Renard "analyser contrat fournisseur cloud"
```

## Étapes d'exécution

### 1. Identifier le membre et la tâche

- Vérifier que le membre existe dans `team.db`
- Si membre non précisé → identifier le bon spécialiste selon la nature de la tâche

### 2. Construire le brief

Générer un brief avec les sections suivantes :

```
BRIEF — [Membre] [Emoji] — [Date]
════════════════════════════════

PRIORITY : [high / medium / low]
DEADLINE : [YYYY-MM-DD ou "pas de deadline"]

MISSION
[Une phrase : ce qui doit être livré]

CONTEXTE
[2-3 phrases : pourquoi cette tâche, dans quel projet, quelle contrainte]

ENTRÉES DISPONIBLES
- [fichier ou info 1]
- [fichier ou info 2]

LIVRABLE ATTENDU
[Format exact : fichier .md, code Python, entrée DB, etc.]
[Destination : TEAM_Inbox/ ou chemin précis]

CONTRAINTES
- [Contrainte technique, délai, ou scope à ne pas dépasser]

INTERACTIONS
- [Membres à consulter si besoin]
```

### 3. Sauvegarder dans team.db

Les champs `priority` et `deadline` sont inclus dans le corps du brief (colonne `body`), pas comme colonnes séparées de la table `inbox`. Le skill `status` les extrait pour le tableau de bord.

```sql
INSERT INTO inbox (direction, from_name, to_name, subject, body, status)
VALUES ('JCH→TEAM', 'Dobby', '<membre>', '<titre_tâche>', '<brief_complet>', 'pending');
```

### 4. Confirmer

Afficher le brief et confirmer l'insertion en DB.

## Règles

- Le brief doit être auto-suffisant — le membre ne doit pas avoir besoin de demander des précisions
- Toujours préciser le format et la destination du livrable
- Toujours inclure `PRIORITY` et `DEADLINE`
- Ne jamais briffer un membre en veille active (Nova, Vasco, Miel) sans accord de JCH

## Skills liés

- **`status`** — Pour visualiser les tâches en attente avec leur priorité et deadline. Les briefs créés ici apparaissent dans le tableau de bord `status`.
