# Skill: [[revue-projet]]

Statut: `approved`
Proprietaire: `JCH`
Derniere revue: `2026-05-13`

## Quand l'utiliser

Utiliser cette skill quand JCH demande de faire le point sur un projet, un dossier ou une initiative existante dans le workspace.

## Objectif

Produire une revue utile pour piloter le projet: etat actuel, objectifs, documents importants, blocages, risques, prochaines actions et hygiene documentaire.

## Entrees requises

- Chemin du projet ou nom du dossier.
- Question principale si connue: etat, priorites, risques, plan d'action, nettoyage, synthese.
- Niveau de detail attendu.

## Procedure

1. Lire l'index du projet s'il existe.
2. Identifier les documents recents et les fichiers structurants.
3. Reconstituer l'objectif du projet et son etat actuel.
4. Reperer:
   - [[decisions]] deja prises;
   - actions ouvertes;
   - contradictions;
   - fichiers obsoletes;
   - risques ou dependances.
5. Proposer un plan d'action court.
6. Si necessaire, recommander une mise a jour de l'index ou du contexte projet.

## Outils autorises

- `rg --files` pour inventorier.
- Lecture locale des fichiers pertinents.
- Statistiques simples si utiles.
- Pas de modification de fichiers sans demande explicite ou validation de JCH.

## Pieges connus

- Ne pas tout lire sans tri.
- Ne pas confondre [[archive]] et source active.
- Ne pas supprimer ou reorganiser sans validation.
- Ne pas conclure trop vite si les documents sont contradictoires.

## Sortie attendue

Format recommande:

```md
## Etat du projet
## Documents structurants
## Decisions connues
## Actions ouvertes
## Risques / blocages
## Recommandations
## Prochaines actions
```

## Criteres qualite

- La revue permet a JCH de reprendre le projet rapidement.
- Les chemins des fichiers importants sont cites.
- Les actions proposees sont priorisees.
- Les incertitudes sont explicites.

## Decision JCH

- decision: `approved`
- date_decision: `2026-05-13`
- commentaire: `Validee par JCH comme skill interne pour faire le point sur un projet du workspace: etat, documents, risques et prochaines actions.`
