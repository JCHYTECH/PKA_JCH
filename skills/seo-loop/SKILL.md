---
name: seo-loop
description: Boucle autonome d'optimisation SEO — Trace modifie page/contenu → seo-audit score → si < seuil → optimise → re-audit. Déclencher sur "seo loop", "optimise le SEO", "auto-optimize SEO", "boucle SEO". Inspiré de forge-loop, Grep Loop et AutoResearch.
---

# Skill — seo-loop

> Variante SEO de `forge-loop`. Le pattern AutoResearch (3 fichiers + budget temps fixe + eval immuable) appliqué à l'optimisation SEO : Lighthouse, Core Web Vitals, rankings, contenu EEAT.

## Architecture 3 fichiers adaptée au SEO

| Fichier AutoResearch | Rôle | Équivalent SEO PKA | Modifiable ? |
|---------------------|------|--------------------|-------------|
| `program.md` | Instructions de la boucle | Brief Trace + quality gate | ❌ Immuable |
| `train.py` | Code/contenu à optimiser | Page HTML, article, meta tags, contenu | ✅ Oui |
| `prepare.py` | Métrique d'évaluation | `seo-audit` (score /100) ou Lighthouse | ❌ Immuable |

## Déclencheurs

- "seo loop sur <url/page>"
- "optimise le SEO de <site>"
- "auto-optimize SEO", "boucle SEO"
- "passe ce contenu au seo-audit et améliore jusqu'au seuil"

## Métriques disponibles

| Métrique | Outil | Seuil cible | Risque si mauvaise métrique |
|----------|-------|------------|------------------------------|
| **Lighthouse Performance** | Lighthouse / PageSpeed | ≥ 90 | Optimiser pour 100 → site vide |
| **Lighthouse SEO score** | Lighthouse | ≥ 95 | Optimiser pour 100 → keyword stuffing |
| **Core Web Vitals (LCP)** | CrUX / Lighthouse | < 2.5s | Optimiser pour 0 → pas de contenu |
| **Core Web Vitals (INP)** | CrUX / Lighthouse | < 200ms | Optimiser pour 0 → pas d'interaction |
| **Core Web Vitals (CLS)** | CrUX / Lighthouse | < 0.1 | — |
| **Content EEAT score** | `content-quality-auditor` | ≥ 80/100 | Pousser à 100 → contenu artificiel |
| **Keyword rankings** | Search Console | Top 10 | Poursuivre un mot-clé mort |
| **Technical SEO** | `seo-technical` | 0 erreurs critiques | — |

> ⚠️ **Le « bad metric » warning s'applique.** Optimiser pour un Lighthouse 100 peut produire une page sans images, sans CSS, sans contenu. Toujours définir des bornes : un score minimum acceptable par métrique mais aussi un contenu minimum viable.

## Principe

```
Brief Trace → modifie page/contenu → déploie → seo-audit → score /100
                                                           │
                                              ≥ seuil ─────┤─── ✅ Dobby valide
                                              < seuil ─────┤─── 🔁 Trace optimise → redéploie
                                                                 (max 3 itérations)
```

## Procédure

### 1. Identifier la cible

- URL ou page spécifique → crawler cette page
- Site complet → `seo-audit` full scan (jusqu'à 500 pages)
- Contenu unique → `content-quality-auditor`
- Si rien n'est spécifié → demander

### 2. Audit initial

```bash
# Pour une page : Lighthouse + seo-technical
# Pour un site : seo-audit complet
# Pour un contenu : content-quality-auditor
```

Si le score est ≥ seuil → **terminé**. Reporter.

### 3. Boucle d'optimisation (si score < seuil)

```
ITÉRATION 1..3 :
  1. Lire le rapport d'audit
  2. Identifier les 3 issues les plus impactantes (pas toutes)
  3. Appliquer les fixes (meta tags, structure, contenu, images, vitesse)
  4. Redéployer / republier
  5. Relancer l'audit
  6. Si score ≥ seuil → SORTIR
```

### 4. Sortie de boucle

| Issue | Action |
|-------|--------|
| **Score ≥ seuil** | ✅ Reporter succès : score final, itérations, fixes appliqués |
| **3 itérations sans atteindre le seuil** | ⚠️ Escalader à Dobby avec le rapport détaillé |
| **Token budget dépassé** | 🛑 Arrêter. Reporter budget + dernier score |

## Règles

### Règles absolues

- **Max 3 itérations par cible.** Au-delà, le problème est structurel (refonte nécessaire).
- **Token budget : 100 000 tokens par loop.** Les audits SEO peuvent crawler 500 pages.
- **Time budget : 600 secondes par expérience.** Laisse le temps au crawler et au déploiement.
- **Ne jamais supprimer de contenu sans vérification.** Optimiser en supprimant = perte de valeur.
- **Ne jamais toucher l'outil d'audit.** `seo-audit` et `content-quality-auditor` sont immuables.
- **Prioriser les fixes à fort impact.** Pas de micro-optimisations (0.1 point Lighthouse).

### Portée des fixes

| Priorité | Action |
|----------|--------|
| **Critique** (404, noindex, canonical cassé) | Toujours fixer |
| **Haute** (LCP > 4s, CLS > 0.25, titre manquant) | Toujours fixer |
| **Moyenne** (meta description, alt text, h1 manquant) | Fixer si < 5 changements |
| **Basse** (minification CSS, cache headers) | Ignorer dans la loop |

## Intégration brief

```yaml
# Dans le brief Trace :
seo_loop: true
metric: "lighthouse_performance"
target: "≥ 90"
floor: "≥ 70"          # Contenu minimum viable
max_iterations: 3
time_budget: 600
```

## Exemple concret — Lighthouse Performance

```
Cible : https://wildlens.be
Métrique : Lighthouse Performance
Seuil : ≥ 90
Plancher : ≥ 70

Itération 1 :
  Baseline : 62/100
  Issues critiques : LCP 4.8s, images non optimisées, render-blocking CSS
  Fixes : compression images WebP, async CSS, lazy loading
  Résultat : 78/100 ✅ → commit

Itération 2 :
  Issues : INP 350ms, JavaScript non minifié
  Fixes : defer JS, minification
  Résultat : 91/100 ✅ → objectif atteint → SORTIE
```

## Skills liés

- **`seo-audit`** — Audit complet site (score /100)
- **`seo-technical`** — Scan technique (crawlability, indexability, Core Web Vitals)
- **`seo-content-writer`** — Rédaction SEO optimisée
- **`seo-content-brief`** — Brief éditorial SEO
- **`content-quality-auditor`** — Score EEAT /100 (80 items)
- **`seo-images`** — Optimisation images
- **`forge-loop`** — Pattern original (code review)
- **`brief`** — Génération de brief avec `seo_loop: true`

## Références

- **AutoResearch** (Karpathy, 2025) — Architecture 3 fichiers, eval immuable
- **Grep Loop** (Ross Mike, 2026) — Code review autonome avec quality gate
- **forge-loop** (PKA, 2026) — Adaptation PKA du pattern pour la code review
