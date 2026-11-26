# ARTEON — Index projet

Dernière mise à jour : 2026-11-05 — navigation et état de relance.

## Description
Plateforme éditoriale photographique naturaliste.  
`arteon.be` | Stack : Shopify Basic · Ghost ([[WildLens]]) · WhiteWall

> **[[WildLens]] est le service prioritaire d'ARTEON.** C'est la tête du funnel d'acquisition — sans lecteurs WildLens, pas de conversion vers [[L'Instant Lu]].

## Point d'entrée

1. [thread-arteon.md](thread-arteon.md) — **état opérationnel courant, décisions et prochaines actions**.
2. [strategy/arteon-colonne-vertebrale.md](strategy/arteon-colonne-vertebrale.md) — architecture et pipeline technique.
3. [wildlens/INDEX.md](wildlens/INDEX.md) — index du service éditorial prioritaire.
4. [executive-summary.md](JCH_Inbox/03_PROJECTS/02_ARTEON/executive-summary.md) — synthèse du projet.

---

## Structure

```
02_ARTEON/
├── wildlens/       ← SERVICE 1 — Journal naturaliste (PRIORITAIRE)
│   ├── INDEX.md            ← index WildLens dédié
│   ├── ref/                ← référentiel éditorial + prompt
│   ├── editions/           ← fichiers d'édition, statuts de publication à vérifier
│   ├── weekly-reviews/     ← revues hebdomadaires insights
│   ├── research/           ← recherches, livres, sources
│   └── reports/            ← rapports de santé WildLens
├── instant-lu/     ← SERVICE 2 — Critique photo IA (L'Instant Lu)
│   └── exports/            ← wireframes + propositions
├── brand/          ← identité transverse (manifeste, charte, logo, exports visuels)
├── strategy/       ← pilotage (colonne vertébrale, état projet, plan action)
├── legal/          ← documents juridiques (CGU, contrats, RGPD)
└── passe-utile/    ← documents historiques encore utiles, pas l'état courant
```

## Services

| Service | Rôle | Statut | Détail |
|---------|------|--------|--------|
| **[[WildLens]]** | Journal hebdomadaire — acquisition et identité éditoriale | 🟠 Relance engagée ; Ghost en pause | [INDEX dédié](wildlens/INDEX.md) |
| **L'Instant Lu** | Critique photo IA — €1,90/analyse, KPI €1000/mois | 🟠 Backend à construire | Voir `strategy/plan-action-critique-service.md` |

## Fichiers clés

| Fichier | Rôle |
|---------|------|
| [strategy/arteon-colonne-vertebrale.md](strategy/arteon-colonne-vertebrale.md) | Pipeline technique, état Phase 0 et todo |
| [strategy/arteon-etat-projet.md](strategy/arteon-etat-projet.md) | Décisions de marque, domaine, stack et roadmap |
| [strategy/plan-action-critique-service.md](strategy/plan-action-critique-service.md) | Roadmap commerciale de L'Instant Lu |
| [brand/arteon-architecture-charte.md](brand/arteon-architecture-charte.md) | Charte graphique, sitemap, URLs et composants UI |
| [brand/presentation-governance.md](brand/presentation-governance.md) | Règles des decks et supports |
| Manifestes [court](brand/arteon-manifeste-court.md) et [long](brand/arteon-manifeste-long.md) | Textes éditoriaux finaux |
| [wildlens/ref/WildLens.md](wildlens/ref/WildLens.md) | Transcript fondateur du 28/03/2026 |
| [wildlens/ref/wildlens-prompt-weekly-review.md](wildlens/ref/wildlens-prompt-weekly-review.md) | Prompt éditorial de revue hebdomadaire |
| [wildlens/instagram-launch-kit.md](wildlens/instagram-launch-kit.md) | Préparation Instagram, sans autorisation de publication implicite |

## Règle de production visuelle

Tout support de présentation produit pour ARTEON doit partir de la charte graphique et des layouts déjà définis.  
Autrement dit : charte d'abord, système visuel existant ensuite, production du support seulement après.

## Roadmap

> Ce tableau est le cadre initial des 13 étapes. Leur suivi courant et les priorités réelles sont dans [thread-arteon.md](thread-arteon.md).

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

Relance engagée — quatre éditions WildLens présentes (28/03 → 31/10) ; leur présence ne prouve pas leur publication. Automatisation hebdomadaire réactivée selon le thread courant.
Instagram est préparé, mais **aucune publication n'est autorisée sans nouvelle demande explicite de JC**.
Ghost renvoie 404 ; le support a été contacté et ce chantier est **en pause**.
Les décisions et la prochaine étape sont suivies dans [thread-arteon.md](thread-arteon.md).

## Voir aussi

- [WildLens](wildlens/INDEX.md) — journal naturaliste, service prioritaire.
- [PHOTO_AI_JURY / Argus](../05_PHOTO_AI_JURY/INDEX.md) — moteur IA de critique photo.
- [PHOTO_NATURE](../06_PHOTO_NATURE/INDEX.md) — matière première terrain et technique.
- [Documents historiques ARTEON](passe-utile/) — à distinguer des documents opérationnels.

---

*Index créé par [[Dobby]] 🦉 le 2026-07-02 ; navigation révisée le 2026-11-05.*
