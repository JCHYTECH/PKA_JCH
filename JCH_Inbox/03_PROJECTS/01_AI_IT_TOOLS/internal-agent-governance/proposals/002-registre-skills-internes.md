# Proposition: Registre de skills internes

## Metadonnees

- id: `skills.internal_registry`
- statut: `APPROVED`
- proprietaire: `JCH`
- suggere_par: `assistant`
- date_creation: `2026-05-13`
- niveau_cout: `medium`
- niveau_risque: `medium`

## Pourquoi

Les bonnes procedures doivent devenir reutilisables. Un registre de skills permet de transformer les meilleures methodes en documents courts, charges uniquement quand ils sont pertinents.

Gain attendu: qualite plus constante, moins d'improvisation, transmission facile des workflows.

Risque evite: prompts disperses, procedures perdues dans les conversations, automation basee sur des habitudes implicites.

## Comment

Creer un dossier:

```text
skills/
  code-review.md
  document-analysis.md
  repo-audit.md
  project-synthesis.md
```

Format standard d'une skill:

```md
# Skill: <nom>

## Quand l'utiliser

## Objectif

## Entrees requises

## Procedure

## Outils autorises

## Pieges connus

## Sortie attendue

## Criteres qualite
```

Regles proposees:

- L'assistant peut proposer une skill.
- JCH valide avant activation.
- Toute skill active doit etre courte, testable et revisable.
- Une skill qui produit des erreurs recurrentes passe en revue.

## Cout

- Mise en place: moyen, il faut rediger les premieres skills.
- Maintenance: moyenne, surtout si le nombre de skills augmente.
- Cout API/infra: nul direct, mais peut reduire les tokens en evitant les longs prompts repetes.
- Complexite: moyenne.

## Risques

- Skills trop nombreuses ou redondantes.
- Skills obsoletes.
- Skills trop directives qui empechent le jugement.

Garde-fous:

- Catalogue limite au debut.
- Statut par skill: `draft`, `active`, `retired`.
- Revue apres usage problematique.

## Critere de validation

La brique est utile si une meme tache recurrente est traitee plus vite, avec moins d'instructions repetitives, et avec une qualite plus stable.

## Decision JCH

- decision: `approved`
- date_decision: `2026-05-13`
- commentaire: `Valide par JCH. Le registre de skills internes peut etre mis en place avec validation manuelle avant activation de chaque skill.`
