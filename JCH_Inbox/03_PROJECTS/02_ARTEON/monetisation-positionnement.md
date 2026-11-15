# ARTEON / WildLens — Positionnement & monétisation

> Dobby 🦉 — 2026-11-15 — issu du run des skills `competitive-framework` + prompts business (Groupe B) sur ARTEON/WildLens.
> Ancrage : `thread-arteon.md`, `executive-summary.md`, `brand/`, `wildlens/`.

---

## 1. Positionnement — competitive-framework

**Contre qui ?** L'adversaire réel n'est pas les autres photographes naturalistes, c'est **Instagram gratuit** + le **statu quo du lecteur** (consommer sans payer ni s'abonner). Les tirages d'art sont un marché de niche, pas une menace.

**Sur quoi ?** Le critère décisif n'est pas la technique, c'est la **singularité du regard** : JC est **zoologiste** (Master ULiège 1979), pas un photographe qui fait de jolies images. La crédibilité naturaliste est l'actif différenciant.

**Limites auto-imposées (3) :**
1. « La monétisation vient après l'audience » — on attend les lecteurs avant de vendre, alors que les presets sont **déjà faits**.
2. Perfectionnisme — 8 étapes de roadmap non closes, Instagram préparé mais non publié.
3. « Je n'ai pas le temps créatif » — vrai pour l'éditorial, mais **faux pour la monétisation** (elle ne demande aucun temps créatif).

**Rupture** : vendre d'abord ce qui est déjà produit, l'audience viendra ensuite.

---

## 2. Monétisation — prompts business

### 2.1 Les 4 leviers, classés

| Levier | Offre | Prix | Marge | Effort JC |
|---|---|---|---|---|
| **Presets** | Pack « Naturaliste » 11 presets Argus | 29 € | ~100 % | 0 (déjà faits) |
| **Critique IA** | L'Instant Lu | 1,90 €/analyse | 1,37 € | 0 (pipeline Argus rodé) |
| **Abonnement** | WildLens Premium | 5 €/mois | ~90 % | ~1 h/sem |
| **Tirages** | WhiteWall via Shopify | 60–300 € | 30–50 % | logistique |

Conseil papier : ponctuel (60–120 €/session), pas un pilier.
**Cible réaliste au 6ᵉ mois : 250–400 €/mois**, essentiellement numérique.

### 2.2 Priorité

**Presets immédiatement + L'Instant Lu.** Les presets génèrent le premier cash dès la semaine 1 (zéro temps créatif) et financent la suite. L'Instant Lu est le seul levier à la fois **récurrent** et à marge quasi totale (pipeline Argus déjà rodé : 58 analyses, score moyen 73,8/100 ; KPI 1 000 €/mois = 280 analyses + 2 clubs photo B2B à 200 €/mois).

### 2.3 Funnel automatisé

```
Instagram → WildLens (Ghost) → landing page → lead magnet (1 preset gratuit + 1 analyse gratuite)
    → séquence email 5 mails → checkout (Gumroad/Stripe, TVA UE gérée) → livraison automatique
```

### 2.4 Automatisation

Réutiliser l'existant : `com.dobby.wildlens-weekly` (launchd hebdo), pipeline Argus, `scripts/ghost_import.py`. Aucune nouvelle infra lourde — brancher le checkout sur ce qui tourne déjà.

---

## 3. Convergence (le message unique)

Les deux cadres disent la même chose : **JC a déjà les actifs monétisables (presets, pipeline Argus), mais ne les vend pas en attendant l'audience ou la perfection.** La rupture = **vendre maintenant**, l'éditorial (WildLens) construit l'audience en parallèle.

---

## 4. Prochaine action — le funnel minimal (détaillé)

**Objectif : premier cash en semaine 1, sans temps créatif.**

### Semaine 1 — Landing + checkout (le strict minimum)
1. **Checkout : Gumroad** (gère TVA UE + livraison digitale automatique ; plus simple que Stripe pour un solo). Produit = pack « Naturaliste » 11 presets à 29 €.
2. **Landing page une-page** : titre + 3 visuels + « 11 presets créés par un jury photo » + bouton acheter (Gumroad) + formulaire email (lead magnet).
3. **Lead magnet** : 1 preset gratuit en échange d'un email (pour amorcer la séquence).

### Semaine 2 — Séquence email (5 mails)
1. Bienvenue + le preset gratuit (livraison immédiate).
2. « Le regard naturaliste » — pourquoi ces presets (crédibilité zoologiste).
3. 1 analyse gratuite L'Instant Lu (teaser + CTA).
4. Upsell pack complet 29 € (rappel bénéfice + preuve).
5. Follow-up simple (« toujours là si besoin »).

### Semaine 3 — Connexion des canaux
- **Instagram** : bio → lien Ghost → landing.
- **WildLens** : CTA en fin de chaque édition → landing (lead magnet).
- **Ghost** : section « Ressources » avec le pack.

### Ce qui n'est PAS bloquant
- Shopify / WhiteWall (tirages) : plus tard, quand les presets tournent.
- Le multilingue EN/FR/IT : les presets sont agnostiques, pas besoin d'attendre.
- La perfection de la charte : une landing simple suffit pour vendre un produit déjà fini.

### Rôles PKA
- **Forge** — brancher Gumroad/landing + séquence email (automatisation).
- **Vega / Miel** — copy de la landing + des 5 mails (brand).
- **Dobby** — coordonner, tenir le funnel.
