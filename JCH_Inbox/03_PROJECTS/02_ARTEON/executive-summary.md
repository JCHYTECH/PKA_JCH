# ARTEON & WildLens — Executive Summary

> Document externe — partenaires et prestataires.
> Version 1.1 — état consolidé le 2026-11-05 ; source opérationnelle : `thread-arteon.md`.

## En une phrase

**ARTEON est la marque de photographie naturaliste éditoriale de Jean-Claude Havaux ; WildLens est son journal d'acquisition, avant la galerie de tirages et le futur service L'Instant Lu.**

## Positionnement

ARTEON associe beauté visuelle, contexte naturaliste, éthique de prise de vue et narration. L'objectif est de proposer un canal plus durable que le seul flux des réseaux sociaux.

Trois services complémentaires structurent le projet :

1. **WildLens** — journal naturaliste hebdomadaire en anglais, destiné à l'acquisition et à l'identité éditoriale.
2. **ARTEON Gallery** — galerie Shopify et tirages via WhiteWall, encore à configurer.
3. **L'Instant Lu** — futur service de critique photo personnalisée, dont le backend reste à construire.

## WildLens : architecture éditoriale actuelle

L'architecture v2 comprend trois sections, et non l'ancienne structure à cinq rubriques :

- **The Frame** — une photo de JC et son analyse éditoriale ;
- **The Shift** — un développement technique, scientifique ou éthique ;
- **The Field** — un exercice terrain concret.

Une section d'essai/philosophie est expérimentée séparément et n'est pas encore intégrée à cette architecture v2. Six fichiers d'édition sont présents, du 28/03 au 31/10/2026 ; leur statut de rédaction ou de publication doit être vérifié individuellement et ne se déduit pas du nom de fichier.

## Funnel prévu

```text
Instagram (découverte)
    → WildLens / Ghost (lecture et abonnement)
    → arteon.be (marque et services)
    → L'Instant Lu puis ARTEON Gallery
```

Instagram est techniquement préparé, mais **aucune publication ne peut être effectuée sans nouvelle demande explicite de JC**. Ghost renvoie actuellement une 404 ; le support a été contacté et ce chantier est en pause.

## Chaîne de production photo

```text
PHOTO_NATURE → PHOTO_AI_JURY / Argus → ARTEON / WildLens
   terrain       critique et presets       édition et services
```

Cette chaîne documente un flux de travail ; elle ne signifie pas que la galerie, les ventes ou les automatisations Lightroom sont déjà en production.

## État réel

| Composant | Statut |
|---|---|
| Roadmap ARTEON, 13 étapes | 4 terminées, 8 en attente, 1 rouge |
| Domaine, manifeste, slogan, charte | Terminés — étapes 1 à 4 |
| WildLens | Relance engagée ; six fichiers d'édition présents |
| Ghost | En pause après diagnostic et contact du support |
| Instagram | Authentification et préparation validées ; aucune publication |
| Shopify / WhiteWall | À configurer |
| L'Instant Lu | Backend à construire |

## Prochaine étape

Reprendre la remise en service de Ghost après réponse du support et à la reprise décidée par JC. En parallèle, JC doit pouvoir allouer du temps créatif aux huit étapes non closes ; les anciennes échéances trimestrielles ne sont pas conservées comme engagements.

## Équipe

- **Jean-Claude Havaux** — photographie, zoologie, direction éditoriale et arbitrages.
- **PKA_JCH** — appui éditorial, IA spécialisée et infrastructure technique.

*Roadmap détaillée : `INDEX.md` et `strategy/arteon-etat-projet.md`. État courant et décisions : `thread-arteon.md` et `wildlens/INDEX.md`.*
