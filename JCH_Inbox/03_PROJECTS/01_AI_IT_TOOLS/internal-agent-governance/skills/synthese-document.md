# Skill: synthese-document

Statut: `approved`
Proprietaire: `JCH`
Derniere revue: `2026-05-13`

## Quand l'utiliser

Utiliser cette skill quand JCH fournit ou designe un document a transformer en synthese exploitable: note, compte rendu, PDF, transcription, contrat, article, rapport ou document projet.

## Objectif

Produire une synthese courte mais decisionnelle: faits importants, decisions, risques, actions, questions ouvertes.

## Entrees requises

- Document source ou chemin du fichier.
- Objectif de la synthese si precise: decision, briefing, extraction d'actions, resume executif, analyse critique.
- Public cible si different de JCH.

## Procedure

1. Identifier le type de document et son objectif probable.
2. Extraire les faits, chiffres, noms, dates, decisions et contraintes.
3. Distinguer clairement:
   - ce qui est certain;
   - ce qui est implicite;
   - ce qui manque;
   - ce qui demande verification.
4. Produire une synthese orientee action.
5. Ajouter une section risques ou points d'attention si le document a une portee juridique, financiere, operationnelle ou strategique.
6. Proposer les prochaines actions concretes.

## Outils autorises

- Lecture locale du document.
- Extraction texte/OCR si necessaire.
- Recherche web uniquement si JCH demande une verification externe ou si le document cite des informations manifestement recentes.
- Creation d'un document derive si JCH le demande.

## Pieges connus

- Ne pas sur-resumer au point de perdre les decisions.
- Ne pas inventer les informations absentes.
- Ne pas melanger faits et interpretation.
- Ne pas ignorer les dates, montants, obligations ou responsables.

## Sortie attendue

Format recommande:

```md
## Synthese courte
## Points cles
## Decisions ou implications
## Actions proposees
## Risques / points d'attention
## Questions ouvertes
```

## Criteres qualite

- JCH peut decider ou agir sans relire tout le document.
- Les incertitudes sont visibles.
- Les actions sont formulees concretement.
- Les elements critiques ne sont pas noyes dans le resume.

## Decision JCH

- decision: `approved`
- date_decision: `2026-05-13`
- commentaire: `Validee par JCH comme skill interne pour transformer un document en synthese decisionnelle avec actions, risques et questions ouvertes.`
