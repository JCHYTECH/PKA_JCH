---
tags:
  - type/project
  - status/active
  - wildlens
  - arteon
  - editorial
owner: "[[Dobby]]"
last_updated: 2026-11-24
---
# [[WildLens]] — Journal naturaliste de photographie wildlife

> **Service prioritaire [[ARTEON]]** — tête du funnel d'acquisition.
> Sans WildLens, pas de traffic, pas de conversion vers [[L'Instant Lu]], pas de revenu.
> wildlens-journal.ghost.io · EN uniquement
>
> **État courant :** Ghost self-host en ligne (`https://wildlens.arteon.be`) — #1 publiée 18/11, #3 programmée 28/11, #2 programmée 05/12, #4 (pigeon ramier) en brouillon 22/11. Instagram : 1ᵉʳ post publié 17/11. **Restructuration 24/11 : 3 sections par numéro (décision panel lecteurs).** Voir [thread-arteon.md](../thread-arteon.md).

---

## Identité

WildLens est un **journal hebdomadaire** analysant les avancées en photographie naturaliste — techniques, science, équipement, concours. Il se positionne à l'intersection de **l'éthologie et de l'image-making**, un territoire quasi inexploré dans la presse photo.

| Élément | Définition |
|---------|------------|
| **Ambition** | Devenir le magazine wildlife de référence pour les photographes naturalistes exigeants |
| **Ton** | Rotatif : militant · investigatif · lyrique (rotation hebdomadaire) |
| **Profondeur technique** | Intermédiaire — assume camera fluency |
| **Différenciateur** | The Frame — une photo de JC qui porte le propos militant |
| **Langue** | Anglais (pivot FR actif depuis le 19/11) |
| **Plateforme** | Ghost (wildlens-journal.ghost.io) + vitrine sur arteon.be/wildlens |
| **Cadence** | Hebdomadaire — samedi |

## Architecture éditoriale v3 — 3 sections

> Validée par JC le 2026-11-24 — décision panel lecteurs. Remplace la v2 (4 sections).
> Voir `ref/architecture-editoriale-v2.md` pour le document complet.

| # | Section | Contenu | Longueur |
|---|---------|---------|----------|
| ① | **Le Cadre** (The Frame) | Une photo de JC + analyse éditoriale. Ton militant. L'image porte le propos. | 400-600 mots |
| ② | **Le Constat** (The Record) | Une dérive de destruction du vivant, factuelle et sourcée. Sobre, sans polémique. | 100-200 mots |
| ③ | **L'actualité technique** | Le développement technique/scientifique de la semaine — fusion Le Virage + L'Objectif. | 300-500 mots |

**Total visé :** 900-1300 mots — 5-7 minutes de lecture.
**Mots-clés :** en fin de numéro (après la section ③), plus en tête.

## Section essai / philosophie (en cours)

> Nouvelle section expérimentale « philosophie/essai » — lancée le 2026-11-03.
> Premier sujet : le langage animal. Deux essais + la source originale, regroupés dans `essai/`.
> Pas encore intégrée à l'architecture éditoriale (3 sections) — en maturation.

| Fichier | Type | Contenu |
|---------|------|---------|
| `essai/AI-Will-Never-Speak-the-Language-of-the-Living.pdf` | source | Article original (PDF) |
| `essai/article-ai-never-speak-language-living.md` | essai | AI et langage animal — patterns vs sens (draft 01/11) |
| `essai/article-ia-voynich-langage-animal.md` | essai | Manuscrit Voynich et langage animal |
| `essai/article-le-miroir-a-refuser-v6.md` | essai | « Le miroir à refuser » — version courante (v6, 24/11 — faits bioacoustiques + sources) |
| `essai/article-le-miroir-a-refuser-v4.md` | essai | « Le miroir à refuser » — v4 (17/11), remplacée par v6 |
| `essai/article-le-miroir-a-refuser-ado.md` | essai | « Le miroir à refuser » — version adolescents |
| `essai/source-parler-aux-animaux-ia.md` | source/réflexion | Vidéo « Parler aux animaux grâce à l'IA » — faits bioacoustiques 2021-2024 reliés à l'essai (24/11) |

## Charte visuelle WildLens

| Élément | Valeur |
|---------|--------|
| Accent | Vert Terrain `#3D5A3E` |
| Base | Palette [[ARTEON]] (Noir Terrain, Ivoire, Ocre Lumière) |
| Typo | Identique ARTEON (Space Grotesk + Lora + IBM Plex Mono) |

→ Voir [la charte ARTEON](../brand/arteon-architecture-charte.md) §3

## Funnel de conversion

```
WildLens (lecteurs ~500) → arteon.be/wildlens → CTA "L'Instant Lu" → 1ère analyse gratuite → Payant
```

WildLens est le canal éditorial d'acquisition prévu. Instagram sert de couche de découverte ; aucune publication Instagram ne peut être faite sans nouvelle demande explicite de JC.

## Structure

```
wildlens/
├── INDEX.md                  ← ce fichier
├── instagram-launch-kit.md   ← préparation Instagram, publication soumise à accord explicite
├── manifeste.md · theme-semaine.md
├── ref/                      ← référentiel éditorial et prompts
├── editions/                 ← fichiers des éditions datées
├── essai/                    ← philosophie et essais
├── deck/                     ← présentation et assets du deck
├── video/                    ← production vidéo et storyboards
├── Pierre de Rosette/        ← dossier de production associé
├── suggestions/              ← suggestions datées
├── research/                 ← recherches, livres et sources
└── reports/                  ← rapports de santé WildLens
```

## Éditions

| # | Sujet | Fichier (FR) | Statut Ghost |
|---|-------|--------------|--------------|
| 1 | Rouge-gorge « Look it in the face » | [wildlens-edition-1-rouge-gorge.md](editions/fr/wildlens-edition-1-rouge-gorge.md) | publiée 18/11 |
| 2 | Gannet (nid en filet de pêche) | [wildlens-edition-2-gannet.md](editions/fr/wildlens-edition-2-gannet.md) | programmée 05/12 |
| 3 | AI autofocus + NewtCam | [wildlens-edition-3-ai-autofocus.md](editions/fr/wildlens-edition-3-ai-autofocus.md) | programmée 28/11 |
| 4 | Pigeon ramier « À hauteur d'yeux — ou pas » | [wildlens-edition-4-pigeon-ramier.md](editions/fr/wildlens-edition-4-pigeon-ramier.md) | draft (brouillon 22/11) |

> **Renumérotation 15/11** (`tmp/renumber_wildlens.py`) : ancienne #4 (rouge-gorge) → #1 ; ancienne #1 (AI autofocus) → #3 ; ancienne #2 (gannet) → #2 ; ancienne #3 (provenance « Was this real? ») → supprimée.
> **Restructuration 24/11 (panel lecteurs)** : 3 sections par numéro — ① Le Cadre, ② Le Constat, ③ L'actualité technique ; mots-clés en fin. Anciennes versions (EN `final/`, FR 4 sections, voix-jc) archivées dans `editions/_archive/2026-11-24_avant-restructuration-3-sections/`.
> *Fichiers datés d'origine archivés dans `editions/_archive/`.*

Le statut de rédaction ou de publication ne doit pas être déduit du seul nom de fichier ; voir [thread-arteon.md](../thread-arteon.md).

## Statut

Relance opérationnelle — Ghost self-host en ligne depuis le 17/11, 3 éditions en place (#1 publiée, #2 et #3 programmées). Cadence hebdo : 28/11 puis 05/12.
Instagram : 1ᵉʳ post publié le 17/11 ; **aucune publication supplémentaire sans nouvelle demande explicite de JC**.

## Actions prioritaires

Les actions courantes sont centralisées dans [thread-arteon.md](../thread-arteon.md). À la date de cette révision : traduire les éditions FR/IT (Jade/Forge), finaliser le thème + abonnement, combler la compétence impression photo avant « ARTEON Éditions ». Ne publier sur Instagram que sur nouvelle demande explicite de JC.

## Voir aussi

- [[ARTEON]] — projet parent (shop, marque, L'Instant Lu)
- [[Argus]] — pipeline IA critique photo (05_PHOTO_AI_JURY)
- PHOTO_NATURE — matière première terrain et technique (06_PHOTO_NATURE)
- [Plan d'action L'Instant Lu](../strategy/plan-action-critique-service.md) — funnel de conversion.

---

*Index mis à jour par [[Dobby]] 🦉 le 2026-11-24 ; restructuration 3 sections (décision panel lecteurs), éditions 1-4 adaptées, anciennes versions archivées.*
