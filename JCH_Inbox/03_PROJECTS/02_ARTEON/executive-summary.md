# ARTEON & WildLens — Executive Summary

> Document externe — partenaires et prestataires.
> Version 1.2 — état consolidé le 2026-11-17 ; source opérationnelle : `thread-arteon.md`.
> Pilotage interne (chantiers / ordre / gardes-fous) : `strategy/arteon-executive-summary.md`.

## En une phrase

**ARTEON est la marque de photographie naturaliste éditoriale de Jean-Claude Havaux — un éditeur de tirages documentés. WildLens est son journal d'acquisition, avant les éditions numérotées et le futur service L'Instant Lu.**

## Positionnement

ARTEON associe beauté visuelle, contexte naturaliste, éthique de prise de vue et narration. L'objectif est de proposer un canal plus durable que le seul flux des réseaux sociaux.

Le produit n'est pas la photo ni l'impression : c'est la **provenance** — le choix de l'image, la preuve (édition numérotée, certificat anti-IA, récit de terrain). L'impression est un support, jamais la valeur.

Trois services complémentaires structurent le projet :

1. **WildLens** — journal naturaliste hebdomadaire en anglais, destiné à l'acquisition et à l'identité éditoriale.
2. **ARTEON Éditions** — tirages documentés, édition numérotée à provenance anti-IA (positionnement acté le 17/11 ; déploiement conditionnel après preuve d'audience).
3. **L'Instant Lu** — futur service de conseil éditorial photo (recadré, backend à construire).

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
    → L'Instant Lu puis ARTEON Éditions
```

Instagram est techniquement préparé, mais **aucune publication ne peut être effectuée sans nouvelle demande explicite de JC**. WildLens est en cours de migration vers un VPS Hostinger (Ghost installé le 15/11) ; le domaine final est `wildlens.arteon.be`.

## Chaîne de production photo

```text
PHOTO_NATURE → PHOTO_AI_JURY / Argus → ARTEON / WildLens
   terrain       critique et presets       édition et services
```

Cette chaîne documente un flux de travail ; elle ne signifie pas que les éditions, les ventes ou les automatisations Lightroom sont déjà en production.

## État réel

| Composant | Statut |
|---|---|
| Roadmap ARTEON, 13 étapes | 4 terminées, 8 en attente, 1 rouge |
| Domaine, manifeste, slogan, charte | Terminés — étapes 1 à 4 |
| WildLens | Migration VPS Hostinger en cours ; six éditions présentes |
| Ghost | Installé sur VPS (15/11) ; reste DNS/SSL/Mailgun/migration |
| Instagram | Authentification et préparation validées ; aucune publication |
| Presets Naturaliste | 36 XMP livrés ; checkout/landing à brancher |
| ARTEON Éditions | Repositionné — tirages documentés, déploiement conditionnel |
| L'Instant Lu | Recadré ; backend à construire |

## Prochaine étape

Brancher le checkout des presets Naturaliste (premier cash, semaine 1) pendant que la migration Ghost (DNS/SSL) se termine. Les éditions numérotées ne se déploient qu'après preuve d'audience — pas de galerie avant audience prouvée.

## Équipe

- **Jean-Claude Havaux** — photographie, zoologie, direction éditoriale et arbitrages.
- **PKA_JCH** — appui éditorial, IA spécialisée et infrastructure technique.
- **Partenaire impression (à sélectionner)** — tireur d'art white-label, sous contrat (association capitalistique seulement après la première édition écoulée et apport d'un marché B2B).

*Roadmap détaillée : `INDEX.md` et `strategy/arteon-etat-projet.md`. État courant et décisions : `thread-arteon.md` et `wildlens/INDEX.md`. Chantiers / ordre / gardes-fous : `strategy/arteon-executive-summary.md`.*
