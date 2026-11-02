---
tags:
  - type/project
  - status/active
  - wildlens
  - arteon
  - editorial
owner: "[[Dobby]]"
last_updated: 2026-07-02
---
# [[WildLens]] — Journal naturaliste de photographie wildlife

> **Service prioritaire [[ARTEON]]** — tête du funnel d'acquisition.
> Sans WildLens, pas de traffic, pas de conversion vers [[L'Instant Lu]], pas de revenu.
> wildlens.ghost.io · EN uniquement

---

## Identité

WildLens est un **journal hebdomadaire** analysant les avancées en photographie naturaliste — techniques, science, équipement, concours. Il se positionne à l'intersection de **l'éthologie et de l'image-making**, un territoire quasi inexploré dans la presse photo.

| Élément | Définition |
|---------|------------|
| **Ambition** | Devenir le magazine wildlife de référence pour les photographes naturalistes exigeants |
| **Ton** | Rotatif : militant · investigatif · lyrique (rotation hebdomadaire) |
| **Profondeur technique** | Intermédiaire — assume camera fluency |
| **Différenciateur** | The Frame — une photo de JC qui porte le propos militant |
| **Langue** | Anglais |
| **Plateforme** | Ghost (wildlens.ghost.io) + vitrine sur arteon.be/wildlens |
| **Cadence** | Hebdomadaire — samedi |

## Architecture éditoriale v2 — 3 sections

> Validée par JC le 2026-07-02. Remplace la structure 5 sections de l'Édition #1.
> Voir `ref/architecture-editoriale-v2.md` pour le document complet.

| # | Section | Contenu | Longueur |
|---|---------|---------|----------|
| ① | **The Frame** | Une photo de JC + analyse éditoriale. Ton militant. L'image porte le propos. | 400-600 mots |
| ② | **The Shift** | Un développement technique, scientifique ou éthique de la semaine | 200-300 mots |
| ③ | **The Field** | Un exercice terrain concret dérivé de la photo ou du sujet | 100-150 mots |

**Total visé :** 900-1300 mots — 5-7 minutes de lecture.

## Charte visuelle WildLens

| Élément | Valeur |
|---------|--------|
| Accent | Vert Terrain `#3D5A3E` |
| Base | Palette [[ARTEON]] (Noir Terrain, Ivoire, Ocre Lumière) |
| Typo | Identique ARTEON (Space Grotesk + Lora + IBM Plex Mono) |

→ Voir `02_ARTEON/brand/arteon-architecture-charte.md` §3

## Funnel de conversion

```
WildLens (lecteurs ~500) → arteon.be/wildlens → CTA "L'Instant Lu" → 1ère analyse gratuite → Payant
```

WildLens est le **seul canal d'acquisition actif**. Sa santé éditoriale conditionne le CA de [[L'Instant Lu]].

## Structure

```
wildlens/
├── INDEX.md                              ← ce fichier
├── ref/
│   ├── WildLens.md                       ← transcript fondateur ChatGPT (28/03/2026)
│   ├── wildlens-prompt-weekly-review.md  ← prompt éditorial complet (v1)
│   └── architecture-editoriale-v2.md     ← architecture 3 sections (v2, 02/07/2026)
├── editions/
│   ├── WildLens-2026-03-28.md            ← Édition #1 — published (v1, 5 sections)
│   └── WildLens-2026-07-02.md            ← Édition #2 — draft (v2, 3 sections)
├── weekly-reviews/                       ← Revues hebdomadaires (format insights)
├── research/                             ← Recherches, livres, sources
└── reports/                              ← Rapports de santé WildLens (générés Dobby)
```

## Éditions

| # | Date | Format | Statut | Fichier |
|---|------|--------|--------|---------|
| 1 | 2026-03-28 | v1 (5 sections) | ✅ Published | `editions/WildLens-2026-03-28.md` |
| 2 | 2026-07-02 | v2 (3 sections) | 🟡 Draft — pending JC review | `editions/WildLens-2026-07-02.md` |

## Statut

🟡 **Relance en cours** — Édition #1 materialisée (28/03). Édition #2 draft générée (02/07) — format v2 3 sections, ton militant, photo fou de bassan. Cadence hebdomadaire à établir.

## Actions prioritaires

| Priorité | Action | Owner |
|----------|--------|-------|
| 🟡 | JC relire Édition #2 (draft) et valider pour publication Ghost | JC |
| 🔴 | Vérifier que wildlens.ghost.io est actif | [[Forge]] |
| 🟠 | Automatiser la cadence hebdomadaire (prompt → LLM → Ghost) | [[Forge]] |
| 🟠 | Configurer clé Ghost Admin API pour stats | [[Forge]] |
| 🟡 | Reprendre les weekly reviews à cadence régulière | [[Dobby]] |

## Voir aussi

- [[ARTEON]] — projet parent (shop, marque, L'Instant Lu)
- [[Argus]] — pipeline IA critique photo (05_PHOTO_AI_JURY)
- PHOTO_NATURE — matière première terrain et technique (06_PHOTO_NATURE)
- `02_ARTEON/strategy/plan-action-critique-service.md` — funnel de conversion

---

*Index mis à jour par [[Dobby]] 🦉 le 2026-07-02*
