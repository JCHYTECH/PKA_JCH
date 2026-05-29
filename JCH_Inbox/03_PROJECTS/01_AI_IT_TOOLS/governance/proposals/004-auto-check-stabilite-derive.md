# Proposition: Auto-check regulier de stabilite et derive

## Metadonnees

- id: `governance.regular_stability_drift_check`
- statut: `APPROVED`
- proprietaire: `JCH`
- suggere_par: `JCH + assistant`
- date_creation: `2026-05-13`
- niveau_cout: `low`
- niveau_risque: `low`

## Pourquoi

Le systeme va accumuler memoires, skills, politiques et [[decisions]]. Sans controle regulier, il peut deriver: informations obsoletes, skills redondantes, regles trop larges, exceptions oubliees ou procedures qui ne correspondent plus aux besoins de JCH.

Gain attendu: garder un systeme stable, sobre, explicable et utile.

Risque evite: auto-complexification, memoire fausse, skills inutiles, politiques incoherentes.

## Comment

Organiser un auto-check regulier, non autonome au debut, declenche par l'assistant quand le contexte s'y prete ou a la demande de JCH.

Frequence proposee:

- Revue legere: apres chaque serie de modifications de gouvernance.
- Revue complete: toutes les 4 a 6 semaines ou apres 10 nouvelles [[decisions]].

Points a verifier:

- Les fichiers `memory/` restent courts, utiles et non sensibles.
- Les skills `approved` sont encore pertinentes.
- Les policies ne sont pas trop larges ni contradictoires.
- Les [[decisions]] `accepted.md` correspondent aux fichiers reellement en place.
- Les propositions anciennes en `PROPOSED` sont acceptees, rejetees ou reformulees.
- Aucun fichier ne transforme une suggestion en permission implicite.

Sortie attendue:

```md
## Etat general
## Derives detectees
## Elements obsoletes
## Decisions a confirmer
## Actions recommandees
## Cout / risque des corrections
```

## Cout

- Mise en place: faible.
- Maintenance: faible si revue courte, moyenne si le registre grossit.
- Cout API/infra: nul hors temps d'analyse.
- Complexite: faible.

## Risques

- Auto-check trop frequent qui ajoute du bruit.
- Revue trop theorique sans action concrete.
- Tentation de modifier directement sans validation.

Garde-fous:

- L'auto-check produit des recommandations, pas des changements automatiques.
- Toute correction importante repasse par validation JCH.
- Les modifications simples de cohérence peuvent etre proposees en bloc.

## Critere de validation

La brique est utile si elle detecte les obsolescences ou incoherences avant qu'elles n'affectent les travaux reels.

## Decision JCH

- decision: `approved`
- date_decision: `2026-05-13`
- commentaire: `Validee par JCH. Les auto-checks doivent detecter stabilite, derive, obsolescence et incoherences, avec recommandations uniquement sauf validation explicite.`
