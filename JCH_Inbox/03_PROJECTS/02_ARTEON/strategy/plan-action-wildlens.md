# Plan d'action — WildLens

> Dobby 🦉 — 2026-11-22 (màj) · Journal hebdomadaire wildlife, tête de funnel ARTEON → L'Instant Lu
> Cadence : samedi · Architecture v2 : ① Le Cadre · ② Le Virage · ③ L'Objectif · ④ Le Constat
> Pivot « tout en français » (19/11) : FR first, EN en réserve, IT plus tard

## Objectif

Devenir le magazine wildlife de référence des photographes naturalistes exigeants, et convertir les lecteurs vers L'Instant Lu (1ère analyse gratuite → payant).

## Baseline (état 2026-11-22)

- Ghost self-host en ligne (`wildlens.arteon.be`) depuis le 17/11.
- **#1** rouge-gorge — publiée 18/11 · **#3** ai-autofocus — programmée 28/11 · **#2** gannet — programmée 05/12 · **#4** pigeon ramier — brouillon 22/11.
- Procédure de rédaction + double-check Ghost/Markdown inscrits (`wildlens/ref/procedure-redaction-edition.md`).
- Script hebdo `wildlens_weekly.py` corrigé (plus de fausse alerte).
- Instagram : 1ᵉʳ post publié 17/11 — aucune publication sans demande explicite de JC.

## Phase 1 — Infrastructure · ✅ terminée

1. ✅ VPS Hostinger KVM 1 + Ghost self-host (datacenter UE).
2. ✅ DNS `wildlens.arteon.be` + Mailgun.
3. ✅ Import des éditions + thème custom (charte ARTEON, vert terrain #3D5A3E).
4. ✅ Journal en ligne.

## Phase 2 — Éditorial (continu, hebdo) · JC + Dobby

1. ✅ #1 publiée (18/11) ; #2 et #3 programmées (05/12 et 28/11).
2. ⏳ #4 (pigeon ramier) : validation JC → `draft → scheduled` (cible 12/12) ; poser la photo en *feature image* Ghost.
3. Reprendre la cadence hebdo (samedi), structure v2 : Le Cadre (400–600) · Le Virage (200–300) · L'Objectif (300–400) · Le Constat (100–150, **systématique**).
4. Maturation « essai/philosophie » (langage animal) — intégrer quand mûre.

## Phase 3 — Multilingue · Jade + Forge (réorientée par le pivot FR)

1. ✅ Pivot « tout en français » (19/11) : éditions FR en production.
2. ⏳ EN en réserve, IT plus tard (après traction francophone).
3. ⏳ Changeur de langue EN/FR/IT + détection géoloc IP (réactivé quand le multilingue reviendra).

## Phase 4 — Distribution + monétisation · Dobby + Forge + Vega/Miel

1. Instagram : couche de découverte (publication sur demande explicite JC uniquement).
2. Funnel de conversion : WildLens → arteon.be/wildlens → CTA L'Instant Lu → 1ère analyse gratuite → payant.
3. Monétisation (`monetisation-positionnement.md`) : presets 29 € + L'Instant Lu 1,90 €.

## Jalons

- ✅ S2 — Ghost self-host en ligne (17/11).
- 🔶 S3 — cadence hebdo : #1 publiée, #2/#3 programmées, #4 en brouillon (reprendre le rythme samedi).
- 🔶 S4 — multilingue : pivot FR réalisé, EN/IT en attente de traction.
- ⬜ S6 — funnel connecté à la monétisation.

## Rôles

- **JC** — éditorial créatif (Le Cadre), feu vert publications.
- **Forge** — infra Ghost, changeur langue, landing.
- **Jade** — traductions (FR prioritaire, IT plus tard).
- **Vega / Miel** — copy landing + mails.
- **Dobby** — coordination, cadence hebdo, procédure de rédaction.

## Décisions clés de la session (22/11)

- **Le Constat (④) devient systématique** (angle pro-nature / anti-spécisme), plus optionnel.
- **L'édition #3 (ai-autofocus) reste sur l'ancienne structure 5 sections** — assumée telle quelle.
- **Template** : la photo en tête est une *feature image* Ghost, le sommaire cliquable une TOC générée par le thème — **ni l'un ni l'autre ne sont dans le Markdown**. Double-check Ghost/Markdown obligatoire.
- Rôles des sections réconciliés : Le Virage = innovation technologique · L'Objectif = sujet technique.
