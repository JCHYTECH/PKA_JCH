# ARTEON — Index projet

Dernière mise à jour : 2026-07-02

## Description
Plateforme éditoriale photographique naturaliste.  
`arteon.be` | Stack : Shopify Basic · Ghost ([[WildLens]]) · WhiteWall

> **[[WildLens]] est le service prioritaire d'ARTEON.** C'est la tête du funnel d'acquisition — sans lecteurs WildLens, pas de conversion vers [[L'Instant Lu]].

---

## Structure

```
02_ARTEON/
├── wildlens/       ← SERVICE 1 — Journal naturaliste (PRIORITAIRE)
│   ├── INDEX.md            ← index WildLens dédié
│   ├── ref/                ← référentiel éditorial + prompt
│   ├── editions/           ← éditions publiées (#1, #2)
│   ├── weekly-reviews/     ← revues hebdomadaires insights
│   ├── research/           ← recherches, livres, sources
│   └── reports/            ← rapports de santé WildLens
├── instant-lu/     ← SERVICE 2 — Critique photo IA (L'Instant Lu)
│   └── exports/            ← wireframes + propositions
├── brand/          ← identité transverse (manifeste, charte, logo, exports visuels)
├── strategy/       ← pilotage (colonne vertébrale, état projet, plan action)
└── legal/          ← documents juridiques (CGU, contrats, RGPD)
```

## Services

| Service | Rôle | Statut | Détail |
|---------|------|--------|--------|
| **[[WildLens]]** | Journal hebdomadaire — acquisition et identité éditoriale | 🟡 Relance nécessaire | [INDEX dédié](wildlens/INDEX.md) |
| **L'Instant Lu** | Critique photo IA — €1,90/analyse, KPI €1000/mois | 🟠 Backend à construire | Voir `strategy/plan-action-critique-service.md` |

## Fichiers clés

| Fichier | Rôle |
|---------|------|
| `strategy/arteon-colonne-vertebrale.md` | **Point d'entrée** — pipeline technique + état Phase 0 + todo |
| `strategy/arteon-etat-projet.md` | Décisions de marque, domaine, stack, roadmap étapes 1-13 |
| `strategy/plan-action-critique-service.md` | Roadmap commerciale — KPI €1000/mois, tâches J0→J90 |
| `brand/arteon-architecture-charte.md` | Charte graphique, sitemap, URLs, composants UI |
| `brand/presentation-governance.md` | Règle de base pour tout deck, PowerPoint ou support |
| `brand/arteon-manifeste-{court,long}.md` | Textes éditoriaux finaux |
| `wildlens/ref/WildLens.md` | Transcript fondateur ChatGPT (28/03/2026) |
| `wildlens/ref/wildlens-prompt-weekly-review.md` | Prompt éditorial complet pour génération hebdomadaire |

## Règle de production visuelle

Tout support de présentation produit pour ARTEON doit partir de la charte graphique et des layouts déjà définis.  
Autrement dit : charte d'abord, système visuel existant ensuite, production du support seulement après.

## Roadmap

| # | Étape | État |
|---|-------|------|
| 1 | Réservation domaine | ✅ arteon.be enregistré |
| 2 | Manifeste Arteon | ✅ 2 versions livrées |
| 3 | Slogan | ✅ Validé |
| 4 | Charte graphique | ✅ Livrée dans `arteon-architecture-charte.md` |
| 5 | Template fiche artiste | ⏳ |
| 6 | Template fiche produit | ⏳ |
| 7 | Formulaire affiliation | ⏳ |
| 8 | Setup Shopify | ⏳ |
| 9 | Setup WhiteWall | ⏳ |
| 10 | Intégration WildLens ↔ Arteon | ⏳ |
| 11 | Préparation 10 photos JC | ⏳ |
| 12 | Retravail éditions WildLens | 🔴 Relance #2 |
| 13 | Lancement V1 | ⏳ |

## Statut

Phase 0 close — 58 photos JCH analysées, pipeline [[Argus]] opérationnel.  
Charte graphique livrée (étape 4 ✅).  
**Urgence : relancer la production WildLens** — 0 édition depuis 3 mois.

## Voir aussi

- [[WildLens]] — journal naturaliste (service prioritaire, [INDEX dédié](wildlens/INDEX.md))
- [[Argus]] / PHOTO_AI_JURY — pipeline IA critique photo (`../05_PHOTO_AI_JURY/`)
- PHOTO_NATURE — matière première terrain et technique (`../06_PHOTO_NATURE/`)
- `../05_PHOTO_AI_JURY/INDEX.md` — index du moteur IA
- `../06_PHOTO_NATURE/INDEX.md` — index du terrain

---

*Index mis à jour par [[Dobby]] 🦉 le 2026-07-02*
