---
date: 2026-05-25
model: GPT-5 [[Codex]]
type: validation-report
status: draft
---

# Validation Phase 2 - Dictionnaire [[Obsidian]]

## Statut

La Phase 2 consolide le dictionnaire genere en Phase 1 sans appliquer de wikilinks dans le vault.

Objectif atteint :

- le scan ignore les sorties generees du projet `obsidian-knowledge-graph` ;
- les agents privilegient `TEAM` comme dossier canonique lorsqu'une fiche equipe existe ;
- les projets privilegient leur dossier sous `JCH_Inbox/03_PROJECTS` ;
- les journaux quotidiens ne deviennent pas dossier canonique par simple frequence de mentions.

## Decisions de curation

Agents :

- source canonique : `TEAM/` ;
- les mentions dans `wiki/Daily/` restent des occurrences, pas des sources d'identite ;
- `Heron` et `Héron` doivent etre traites comme alias a fusionner apres validation JCH.

Projets :

- source canonique : `JCH_Inbox/03_PROJECTS/<projet>/` ;
- le dictionnaire peut servir de base pour un futur index [[Obsidian]], mais ne remplace pas les 

Technologies :

- les entrees sont des candidats de graphe, pas encore des entites definitives ;
- les termes ambigus doivent rester exclus de tout wikilinking automatique tant qu'ils ne sont pas decides.

## File d'attente JCH

Validation requise avant Phase 3 :

- `Claude` : modele, runtime, app ou agent externe selon contexte ;
- `ChatGPT` : produit, runtime ou interface ;
- `Python` : langage, runtime local ou script specifique ;
- `Apple` : entreprise, appareil ou ecosysteme ;
- `Pi` : raccourci trop vague ; preferer `Raspberry Pi 5` quand c'est l'intention ;
- `Heron` / `Héron` : confirmer la forme canonique avec accents.

## Recommandation

Phase 3 doit etre un dry-run uniquement :

1. proposer les wikilinks a creer ;
2. produire un diff lisible par fichier ;
3. ne modifier aucune note source sans validation explicite.
