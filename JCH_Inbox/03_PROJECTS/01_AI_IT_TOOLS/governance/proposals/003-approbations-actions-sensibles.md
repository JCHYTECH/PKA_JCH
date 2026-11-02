# Proposition: Politique d'approbation des actions sensibles

## Metadonnees

- id: `security.sensitive_action_approvals`
- statut: `APPROVED`
- proprietaire: `JCH`
- suggere_par: `assistant`
- date_creation: `2026-05-13`
- niveau_cout: `medium`
- niveau_risque: `low`

## Pourquoi

Un agent utile finit par modifier des fichiers, lancer des commandes, consulter des donnees ou proposer des automatisations. Il faut separer les actions courantes des actions sensibles qui demandent une validation explicite.

Gain attendu: plus de securite, moins de risque de suppression, fuite de secret ou modification non souhaitee.

Risque evite: execution destructive, propagation d'erreurs, acces involontaire a des donnees sensibles.

## Comment

Creer une politique simple:

```text
policies/
  approvals.yaml
  sandbox.yaml
  secrets.yaml
```

Actions qui demandent approbation:

- Suppression recursive ou massive.
- Modification de fichiers de configuration critiques.
- Acces ou exposition de secrets.
- Appel reseau non necessaire a la tache.
- Installation de dependances.
- Deploiement.
- Automatisation planifiee.
- Modification de memoire ou de skill active.

Actions interdites par defaut:

- Suppression du workspace.
- Execution de scripts distants non audites.
- Envoi de secrets vers un service externe.
- Activation d'un mode autonome sans limite.

## Cout

- Mise en place: moyen.
- Maintenance: faible a moyenne.
- Cout API/infra: nul.
- Complexite: moyenne si automatisee, faible si appliquee comme regle documentaire au debut.

## Risques

- Trop d'approbations peuvent ralentir le travail.
- Regles trop vagues peuvent etre mal appliquees.
- Une allowlist trop large peut annuler le benefice.

Garde-fous:

- Commencer par une politique documentaire.
- Ajouter l'automatisation seulement apres stabilisation.
- Journaliser les exceptions.

## Critere de validation

La brique est utile si les actions sensibles sont identifiees avant execution, sans bloquer les taches normales de lecture, synthese et edition controlee.

## Decision JCH

- decision: `approved`
- date_decision: `2026-05-13`
- commentaire: `Valide par JCH comme politique de gouvernance. Application documentaire dans un premier temps, automatisation a definir separement.`
