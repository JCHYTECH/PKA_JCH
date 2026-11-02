---
name: sigma-loop
description: Boucle autonome de validation de données financières — Sigma analyse données → backtesting → écart prévision/réel → ajuste modèle. Déclencher sur "sigma loop", "valide les données", "backtest loop", "optimise le modèle financier". Inspiré de forge-loop et AutoResearch.
---

# Skill — sigma-loop

> Variante finance de `forge-loop`. Le pattern AutoResearch appliqué à la validation et l'optimisation de modèles financiers : données de marché, projections, backtesting.

## Architecture 3 fichiers adaptée à la finance

| Fichier AutoResearch | Rôle | Équivalent Finance | Modifiable ? |
|---------------------|------|--------------------|-------------|
| `program.md` | Instructions de la boucle | Brief Sigma + quality gate | ❌ Immuable |
| `train.py` | Code/data à optimiser | Modèle financier, paramètres, hypothèses | ✅ Oui |
| `prepare.py` | Métrique d'évaluation | Backtesting, validation croisée | ❌ Immuable |

## Déclencheurs

- "sigma loop", "valide les données"
- "backtest loop", "optimise le modèle financier"
- "vérifie les projections"
- "audite les données financières"

## Métriques disponibles

| Métrique | Calcul | Seuil cible | Risque si mauvaise métrique |
|----------|--------|------------|------------------------------|
| **RMSE projections** | Écart quadratique moyen prévision/réel | < 5% | Optimiser pour 0 → overfitting |
| **MAPE** | Mean Absolute Percentage Error | < 10% | Ignorer les outliers → modèle trop lisse |
| **R² ajusté** | Coefficient de détermination | > 0.85 | Pousser à 1.0 → surapprentissage |
| **Sharpe ratio (backtest)** | Rendement / volatilité | > 1.0 | Optimiser pour max → risque caché |
| **Max drawdown (backtest)** | Perte max historique | < 20% | Optimiser pour 0 → pas investi |
| **Data completeness** | % valeurs non-nulles | > 95% | — |
| **Outlier rate** | % valeurs > 3σ | < 2% | — |
| **Data freshness** | Âge max des données | < 7 jours | — |

> ⚠️ **Le « bad metric » warning est particulièrement dangereux en finance.** Un modèle optimisé pour le Sharpe ratio peut cacher un risque de ruine. Un modèle optimisé pour un R² parfait est inutilisable en conditions réelles. Toujours coupler risque + rendement.

## Principe

```
Brief Sigma → analyse données → modèle → backtesting → métriques
                                                         │
                                              OK ────────┤─── ✅ commit
                                              sous seuil ─┤─── 🔁 ajuste modèle
                                              (max 3 itérations)
```

## Procédure

### 1. Définir les contraintes couplées

```yaml
metrics:
  - name: "mape"
    target: "< 10%"
    ceiling: "< 20%"
  - name: "sharpe_ratio"
    target: "> 1.0"
    floor: "> 0.5"
  - name: "max_drawdown"
    target: "< 15%"
    ceiling: "< 25%"
max_iterations: 3
time_budget: 300
```

### 2. Boucle de validation

```
ITÉRATION 1..3 :
  1. Charger les données (marché, portefeuille, historique)
  2. Valider la qualité des données (complétude, outliers, fraîcheur)
  3. Exécuter le modèle / les projections
  4. Backtesting contre données historiques
  5. Calculer les métriques couplées
  6. Toutes les métriques dans les bornes → commit
     Une métrique hors bornes → ajuster paramètres / hypothèses
```

### 3. Sortie de boucle

| Issue | Action |
|-------|--------|
| **Toutes les métriques OK** | ✅ Commit. Mettre à jour le rapport financier |
| **3 itérations sans convergence** | ⚠️ Escalader à Dobby + Bruno. Les hypothèses de marché sont peut-être caduques |
| **Données de mauvaise qualité** | 🛑 Arrêter. Pas de modèle fiable sur des données pourries |
| **Overfitting détecté** (R² train ≫ test) | 🛑 Arrêter. Simplifier le modèle |

## Règles absolues

- **Jamais de métrique unique.** Toujours coupler performance + risque.
- **Ne jamais backtester sur les données d'entraînement.** Split temporel obligatoire (ex: train 2020-2024, test 2025-2026).
- **Ne jamais modifier les données sources.** Les données de marché sont immuables.
- **Documenter chaque hypothèse.** « J'ai supposé un taux d'inflation à 2% » → traçable.
- **Alerter sur les outliers, ne pas les supprimer.** Un outlier peut être un signal, pas du bruit.
- **Budget temps fixe.** Même temps de calcul par itération.

## Intégration brief

```yaml
# Dans le brief Sigma :
sigma_loop: true
metrics:
  - name: "mape"
    target: "< 10%"
  - name: "sharpe_ratio"
    target: "> 1.0"
  - name: "max_drawdown"
    target: "< 15%"
max_iterations: 3
time_budget: 300
```

## Exemple concret — Validation projections portefeuille

```
Métriques couplées :
  MAPE : < 10%
  Sharpe : > 1.0
  Max drawdown : < 15%

Itération 1 :
  Baseline : MAPE 14%, Sharpe 0.8, drawdown 18%
  Hypothèse : fenêtre de calcul trop courte (6 mois → 24 mois)
  Modification : fenêtre glissante 24 mois
  Résultat : MAPE 11% (+3), Sharpe 0.9 (+0.1), drawdown 16% (+2)
  ✅ Amélioration sur toutes les métriques → commit

Itération 2 :
  Hypothèse : pondération égale → risk parity
  Modification : ajustement volatilité par actif
  Résultat : MAPE 9%, Sharpe 1.1, drawdown 13%
  ✅ Toutes les métriques dans les bornes → SORTIE
```

## Skills liés

- **`forge-loop`** — Pattern code review original
- **`modele`** — Estimation coût avant lancement
- **`brief`** — Génération de brief avec `sigma_loop: true`
- **Bruno** 🐻 — Validation humaine finale des projections financières (stakes élevés)

## Références

- **AutoResearch** (Karpathy, 2025) — Architecture 3 fichiers, budget temps fixe
- **forge-loop** (PKA, 2026) — Adaptation PKA du pattern
- **argus_batch.py** — Script d'analyse financière batch PKA
