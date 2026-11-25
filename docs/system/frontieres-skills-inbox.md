# Frontières des skills « inbox » — Référence

> Dobby 🦉 — 2026-11-25
> Clarifie quand utiliser `ingest`, `inbox-analysis`, `analyse-transcript`, `system-improvement-ingest`.

## Les 4 skills en une ligne

| Skill | Question centrale | Livrable |
|---|---|---|
| `ingest` | **Où ranger ce fichier ?** | Fichier déplacé + indexé (`file_index`) + scan sécurité |
| `inbox-analysis` | **Qu'est-ce que ce fichier dit, et qu'en faire ?** | Analyse 7 phases + actions projets |
| `analyse-transcript` | **Ce transcript est-il fiable, et qu'en faire ?** | Comprendre + confirmer (fact-check) + conseiller |
| `system-improvement-ingest` | **Que peut-on tirer de ce document pour améliorer PKA ?** | Grille 6 axes + améliorations système |

## Arbre de décision

Un fichier arrive dans `00_INBOX/` :

1. Objectif = **ranger / classer** (pas d'analyse de fond) → **`ingest`**.
2. Objectif = **analyser le contenu** :
   - C'est un **transcript** (vidéo / podcast / NoteGPT) → **`analyse-transcript`**.
   - Tout autre type (papier, article, document) → **`inbox-analysis`**.
3. Objectif = **améliorer le système PKA** (quel que soit le type, même par analogie) → **`system-improvement-ingest`**.

## Cas limites

- **Transcript + « améliore le système avec ça »** → `system-improvement-ingest` (l'angle système prime sur le fact-check).
- **Fichier + « analyse-le et propose »** → `inbox-analysis` (générique).
- **Fichier + « range-le »** → `ingest` (routage seul).
- Un même fichier peut enchaîner `ingest` (routage) **puis** un des 3 skills d'analyse.

## Ce qui distingue `system-improvement-ingest`

Il ne route pas et ne fait pas d'analyse de contenu « projet ». Son angle unique :
transposer le document en **améliorations du système PKA-JCH** via la grille 6 axes
(exactitude, mémoire, transversalité, intuition, Arbor/Loops, innovation).
Applicable à n'importe quel document, même sans lien apparent avec PKA.

## Point commun (routage final)

Tous les skills d'analyse finissent par router le fichier source vers
`03_PROJECTS/<projet>/99_REFERENCES/` — c'est le point commun avec `ingest`.
La différence : **`ingest` route sans analyser ; les autres analysent puis routent.**

## Tableau récapitulatif (skill → ne pas utiliser si…)

| Skill | Ne pas l'utiliser pour… |
|---|---|
| `ingest` | comprendre le contenu ou en extraire des décisions |
| `inbox-analysis` | un transcript (→ `analyse-transcript`) ou une amélioration système (→ `system-improvement-ingest`) |
| `analyse-transcript` | un fichier non-transcript (→ `inbox-analysis`) |
| `system-improvement-ingest` | router un fichier ou l'analyser pour un projet précis |
