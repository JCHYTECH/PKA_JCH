---
type: guideline
status: active
dateCreated: 2026-05-26
dateModified: 2026-05-26
tags:
  - [[Obsidian]]
  - graph
  - pka
owner: "[[Dobby]]"
project: PKA_JCH
---

# GL-003 — Vue Graphe [[Obsidian]] projets uniquement

## Objectif

Faire du graphe [[Obsidian]] une carte strictement centree sur les projets actifs PKA_JCH, sans pollution visuelle par les agents, outils IA, notes Daily ou procedures.

## Configuration appliquee

Le graphe global utilise le filtre :

```text
path:JCH_Inbox/03_PROJECTS/ -path:JCH_Inbox/03_PROJECTS/archive/
```

Ce filtre conserve uniquement les notes situees dans les projets actifs et retire l'[[archive]].

Les liens non resolus sont masques :

```json
"hideUnresolved": true
```

Cela evite que des concepts comme `Claude`, `Codex` ou d'autres wikilinks sans note projet visible restent affiches comme noeuds gris.

## Groupes de couleur

Les projets sont colores individuellement :

- `01_AI_IT_TOOLS`
- `02_ARTEON`
- `03_WILDNEXUS`
- `05_PHOTO_AI_JURY` + `06_PHOTO_NATURE`
- `07_TRAVELS`
- `08_VETALYX`
- `09_DIM3`

## Regle d'usage

La vue globale doit repondre a la question : quels projets structurent PKA_JCH et comment leurs documents internes sont connectes ?

Pour analyser l'equipe, les outils IA, les procedures ou le journal, modifier temporairement le filtre ou ouvrir une vue locale depuis la note concernee.

## Sauvegarde

La configuration precedente du graphe est conservee dans :

`.obsidian/backups/2026-05-26-graph-project-view/graph.json`

La version intermediaire orientee projets + organisation du vault est conservee dans :

`.obsidian/backups/2026-05-26-graph-project-view/graph-before-projects-only.json`

La version avant masquage des liens non resolus est conservee dans :

`.obsidian/backups/2026-05-26-graph-project-view/graph-before-hide-unresolved.json`
