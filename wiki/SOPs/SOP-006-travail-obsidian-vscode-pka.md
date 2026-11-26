---
type: sop
status: active
dateCreated: 2026-05-26
dateModified: 2026-05-26
tags:
  - [[Obsidian]]
  - vscode
  - pka
owner: "[[Dobby]]"
project: PKA_JCH
---

# SOP-006 — Travail [[Obsidian]] + VS Code dans PKA_JCH

## Objectif

Eviter les collisions de fichiers entre [[Obsidian]], VS Code, [[Codex]] et les scripts PKA, tout en conservant un workflow fluide.

## Principe

VS Code Explorer et [[Obsidian]] peuvent afficher le meme vault sans probleme. Le risque apparait quand deux outils modifient, renomment ou deplacent les memes fichiers en meme temps.

Regle centrale : un seul outil est editeur actif pour une zone donnee.

## Roles des outils

| Outil | Role principal |
|-------|----------------|
| [[Obsidian]] | Lecture, navigation graphe, backlinks, Daily, petites corrections humaines |
| VS Code | Edition precise, recherche globale, scripts, [[Git]], restructurations controlees |
| [[Codex]] / [[Dobby]] | Migrations documentaires, wikilinks, audits, rapports, automatisations |

## Procedure standard

1. Avant une session de modification importante, verifier l'etat du depot avec `git status`.
2. Utiliser [[Obsidian]] comme cockpit de lecture : graph, backlinks, preview, dashboard Dataview.
3. Pendant une edition VS Code ou [[Codex]], ne pas modifier la meme note dans [[Obsidian]].
4. Pendant une passe [[Codex]], ne pas renommer ou deplacer les memes fichiers dans [[Obsidian]].
5. Apres modification, revenir dans [[Obsidian]] et attendre l'indexation.
6. Si [[Obsidian]] ne voit pas les changements, utiliser `Reload app` ou redemarrer [[Obsidian]].
7. Verifier Graph, backlinks et `wiki/INDEX-dashboard.md` si la modification touche le graphe ou les proprietes.

## Renommages et deplacements

Petits renommages de notes liees :

- preferer [[Obsidian]] ;
- laisser [[Obsidian]] mettre a jour les liens internes.

Renommages massifs ou restructuration de dossiers :

- preferer VS Code ou [[Codex]] ;
- faire `git status` avant et apres ;
- verifier les liens avec une passe de controle.

## Usage de Linter

Linter reste en mode prudent :

- pas de lint automatique au debut ;
- pas de `lint on save` tant que la configuration n'est pas validee ;
- tester d'abord sur 5 notes non critiques ;
- ne jamais lancer un lint large pendant qu'un agent ou VS Code modifie beaucoup de fichiers.

## Synchronisation et [[Git]]

Ne pas superposer sans discipline :

- [[Obsidian]] Sync ;
- [[Obsidian]] [[Git]] ;
- commandes [[Git]] manuelles ;
- modifications massives par [[Codex]].

Procedure recommandee :

1. Modifier.
2. Verifier dans [[Obsidian]].
3. Controler `git status`.
4. Commit ou sauvegarde PKA si la session contient des decisions utiles.

## Interdictions pratiques

- Ne pas editer la meme note dans [[Obsidian]] et VS Code simultanement.
- Ne pas renommer un fichier dans [[Obsidian]] si VS Code a une version modifiee ouverte.
- Ne pas activer Linter en auto-save sans validation.
- Ne pas modifier `.obsidian/workspace.json` a la main sauf besoin explicite.

## Resume operationnel

[[Obsidian]] est le cockpit humain. VS Code est l'atelier technique. [[Codex]]/[[Dobby]] est l'operateur documentaire. Le systeme reste stable si une seule couche ecrit a la fois.
