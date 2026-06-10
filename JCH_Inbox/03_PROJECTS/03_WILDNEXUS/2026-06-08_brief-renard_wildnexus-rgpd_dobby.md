# Brief — Procédure droit d'accès RGPD + Template signalétique terrain

**De :** [[Dobby]] 🦉
**Pour :** [[Renard]] 🦊
**Date :** 2026-06-08
**Priorité :** M-03
**ADR lié :** ADR-010 — points de réserve R3 + R6

## Contexte

L'ADR-010 a identifié deux obligations RGPD concrètes pour le déploiement terrain :

- **R3 — Droit d'accès** : si un faux négatif du filtre humain laisse passer une image, une personne filmée peut exercer son droit d'accès. Il faut une procédure.
- **R6 — Signalétique** : chaque nœud doit porter un panneau informant le public de l'observation automatisée.

## Mission

### R3 — Procédure droit d'accès RGPD

Rédiger une procédure terrain (1 page max) couvrant :
1. Comment une personne concernée contacte le projet (adresse [[email]]/github)
2. Délai de réponse (30 jours max)
3. Procédure technique : extraction câblée SD → vérification manuelle → suppression/floutage
4. Modèle de registre RGPD minimal (finalité, base légale, conservation, sécurité)

### R6 — Template signalétique

Proposer un **texte de panneau** (français + anglais) à graver ou imprimer sur chaque boîtier :
- Zone sous observation automatisée
- Finalité : suivi de faune
- Traitement Edge, aucune image humaine conservée ni transmise
- Contact
- Format compact (max 400 caractères)

## Format livrable

`YYYY-MM-DD_renard_wildnexus-rgpd-procedure-signaletique.md` dans `TEAM_Inbox/`

## Deadline

Avant premier déploiement terrain (M-03).

## Voir aussi

- `ADR-010` — §5 Signalétique terrain et droit d'accès RGPD
