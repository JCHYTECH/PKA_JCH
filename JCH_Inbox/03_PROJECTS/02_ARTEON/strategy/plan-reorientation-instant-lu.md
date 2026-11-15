---
date: 2026-11-15
source: dobby
domain: arteon/wildlens
type: strategy
status: actif
lang: fr
---

# Plan de réorientation — ARTEON (post-conseil L'Instant Lu)

> Issu du conseil du 2026-11-15 (`TEAM_Inbox/2026-11-15_dobby_conseil_instant-lu.md`).
> Remplace la trajectoire du `plan-action-critique-service.md` (2026-05-02) pour la partie L'Instant Lu.

---

## Décision (rappel du conseil)

- **NO-GO** sur la critique à l'acte €1,90 (unanimité).
- **Gel du badge « Vérifié »** (sans condition).
- **Prioriser** presets + WildLens (actifs prêts, sans promesse impossible).
- **Préserver** le corpus Argus comme actif stratégique (pivot possible).

---

## Principe directeur

Vendre d'abord ce qui est **déjà produit et vrai** (le look signature + le journal), construire l'audience en parallèle, et ne relancer L'Instant Lu que sur des **fondations validées** (espèce + score), jamais sur une promesse de certification.

---

## Phase 1 — Semaine 1-2 · Presets (cash immédiat)

- **Produit :** pack « Naturaliste — signature Fin Art Cinématique » (voir Annexe A).
- **Checkout :** Gumroad (TVA UE auto, livraison digitale) — plus simple que Stripe pour un solo.
- **Landing une-page** : titre + 3 visuels + « le regard d'un zoologiste sur vos images » + bouton acheter + lead magnet.
- **Lead magnet :** 1 preset gratuit contre email (amorce la séquence).
- **KPI :** premier cash, ~10-30 ventes × €29, zéro temps créatif.

## Phase 2 — Semaine 2-6 · WildLens + Ghost (acquisition)

- Finaliser le self-host Ghost (DNS A `wildlens` → 2.25.8.208 → SSL → Mailgun → migration 6 éditions) — runbook en cours.
- WildLens = moteur d'acquisition ; CTA presets en fin de chaque édition.

## Phase 3 — Conditionnelle (J+60) · Relance L'Instant Lu en B recadré

**Gates bloquantes (ne pas lancer avant) :**
1. **Espèce** : benchmark ≥200 images vérité terrain, top-1 ≥95 % — ou brancher un classifieur (BirdNET/Spécio) au lieu de l'ID LLM.
2. **Score** : panel ≥100 images, 3 juges humains, ICC ≥0,70, ancres pour étaler l'échelle sur 40-95 (aujourd'hui compressée 57-86).
3. **Positionnement** : « conseil éditorial », **pas** de note « niveau jury », **pas** de badge.
4. **Pricing** : coût API réel ($0,174) + temps de validation valorisé → ≥€4-5/analyse, OU automatisation sans validation humaine (et baisse de la promesse).

## Phase 4 — Optionnelle · Pivot corpus (Expansionniste)

- Le corpus Argus (5 axes × espèce × EXIF × corrections) → **référentiel licenciable** : clubs photo, festivals (Montier, Namur), fabricants (évaluation AF animalier).
- **Présélection de concours** (API de curation : tri 8 000 images, le jury humain garde la souveraineté) comme offre B2B.

---

## Réconciliation des incohérences (à corriger dans les docs)

| Sujet | Actuel (faux) | Corrigé |
|-------|---------------|---------|
| Prix analyse | €2,90 dans projections §7 | **€1,90** décidé (et le service est suspendu) |
| Coût API | €0,02/analyse (projection) | **$0,174** réel |
| Funnel | 6 clients/mois vs KPI 280 analyses | KPI €1 000/mois **suspendu** avec la critique à l'acte |
| Presets | « 11 presets » | **1 signature** distillée + variantes (pas 11 XMP bruts) |

---

## Rôles PKA

- **Forge** — Gumroad/landing + séquence email + extraction du preset signature.
- **Argus** — distillation des presets depuis `lr_params.md` + benchmark espèce (gate Phase 3).
- **Vega / Miel** — copy landing + emails (brand).
- **Bruno** — pricing recalculé (Phase 3).
- **Dobby** — coordination, tenue des gates.

---

## Annexe A — Package presets « Naturaliste »

### Ce qui existe réellement (constat vérifié)

`03_PROJECTS/06_PHOTO_NATURE/tech/presets-argus/` contient **11 fichiers XMP**, tous **du même look** : le `dc:title` de chaque fichier est « … — Fin Art Cinématique Wildlife ». Ce ne sont pas 11 presets distincts, mais **1 signature démontrée sur 11 photos réelles** (chaque XMP est calibré par image).

Contenu type d'un XMP (lu) : WB custom ~5400-5800 K, teinte +4/5 · exposition +0.15 · contraste +25 · hautes lumières -35/-40 · ombres +35/+40 · courbe S cinématique · TSL (orange sat +18, bleu sat -15) · color grading ombres indigo 220° + hautes lumières chaudes 38° · clarté +22 · vibrance +8/15 · saturation -8 · grain 12 · vignette -20.

### Ce qu'on vend (honnête, pas 11 faux presets)

**Pack « Naturaliste — signature Fin Art Cinématique »**

1. **1 preset signature** (Fin Art Cinématique Wildlife) — XMP importable LrC + LR CC.
2. **3 variantes scénario** (à construire depuis `lr_params.md`) : Plumage sombre · Plumage clair · Golden hour.
3. **11 édits réels avant/après** — preuve + pédagogie (pas « 11 presets »).
4. **PDF guide** « poser et ajuster » (réutilise les instructions XMP du skill).

**Prix :** €29 (€19 en lancement). **Positionnement :** « le regard d'un zoologiste sur vos images — un seul look, exigeant, pas une pile de filtres. »

### Travail à faire (~2-3 h, Forge/Argus)

Extraire le preset signature unique + générer les 3 variantes scénario depuis `lr_params.md`. Les 11 XMP bruts ne sont **pas vendables tels quels** (nommés par photo, calibrés par image).
