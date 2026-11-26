---
project: Future Invest
type: spec
module: Risk Supervisor
author: "[[Dobby]]" (relecture [[Bruno]] / [[Forge]])
created: 2026-11-22
status: draft v1 — seuils à calibrer en Phase 2 (backtest)
trigger: leçons du krach AI-led nov 2026
---

# Spec — Risk Supervisor : régimes « cascade de liquidité » & « momentum crash »

## Contexte

Le krach de nov 2026 a exposé deux angles morts du Risk Supervisor (v1, draft) :
1. L'hypothèse « or = refuge » ne tient pas en crise de liquidité (or −9,2 % **avec** les actions).
2. Le circuit-breaker ne voit que la **perte de portefeuille**, pas le « momentum crash » (débouclage de positions bondées) qui la précède.

Cette spec ajoute un **classificateur de régime** en amont du circuit-breaker. Il ne remplace pas les paramètres existants — il les conditionne.

## Principe général

Le Risk Supervisor passe de « réactif (perte) » à « anticipatif (régime) » : il détecte le régime de marché **avant** qu'il ne frappe le P&L, et ajuste les contraintes. Trois régimes :

| Régime | Signature | Corrélation |
|--------|-----------|-------------|
| NOMINAL | marché normal | diversifiée |
| **CASCADE DE LIQUIDITÉ** | vente forcée généralisée, refuge vendu aussi | **→ 1** |
| **MOMENTUM CRASH** | débouclage brutal d'un trade bondé | rotation extrême |

---

## Gradient de corrélation actions ↔ matières premières (régime-dépendant)

La corrélation n'est **pas uniforme**. Le krach de nov 2026 a mesuré un gradient net
(chute du jour, en ratio du SPY −8,6 %) :

| Catégorie | Instrument observé | Chute | Ratio / SPY | Corrélation actions (nominal) | Corrélation actions (cascade) |
|-----------|--------------------|-------|-------------|-------------------------------|-------------------------------|
| Métaux précieux | Argent (SLV) | −16,2 % | **1,9×** | faible / négative en stress normal | **très haute (~1)** |
| Métaux précieux | Or (GLD) | −9,2 % | 1,1× | faible / négative | haute (0,9–1) |
| Métaux industriels | Cuivre (CPER) | −9,9 % | 1,2× | modérée | haute (0,8–0,9) |
| Panier commo | DBC / GSG | −4,8 % / −4,5 % | 0,55× | modérée | modérée (0,5–0,6) |
| Énergie | Pétrole (USO) | −4,1 % | 0,5× | modérée | modérée (0,5) |
| Agricole | Blé (WEAT) | −1,9 % | 0,2× | faible | **faible (0,2–0,3)** |
| Agricole | Maïs (CORN) | −1,6 % | 0,2× | faible | faible (0,2) |

**Règle (remplace le R4 uniforme) :** en régime cascade, le coefficient de
corrélation est **par sous-catégorie**, pas global. Les métaux précieux sont des
« actifs financiers déguisés » (corrélation ≈ actions, voire pire) ; l'agricole
reste découplé (physique/météo). Conséquences pour le Risk Supervisor :
- En cascade : **réduire fortement précieux/industriels**, **conserver l'agricole**.
- Les « valeurs refuge » (or/argent) ne couvrent RIEN en cascade — elles amplifient.

*Valeurs mesurées sur le krach nov 2026 — à confirmer sur 2008 et 2020-03 en Phase 2.*

---

## Régime 1 — Cascade de liquidité

### Définition

Phase aiguë où les acteurs vendent **tout** pour lever du cash (margin calls, deleveraging). Signature : les actifs « refuge » (or, T-bonds) baissent **en même temps** que les actifs risqués. Documenté : 2008 (or −30 % mars→oct, Lehman), 2020-03 (or −12 % phase aiguë COVID), oct-nov 2026.

### Signaux de détection (vote pondéré — régime actif si score ≥ seuil)

| # | Signal | Source | Sens |
|---|--------|--------|------|
| R1 | Corrélation signée or/actions **> 0** pendant un drawdown (or baisse AVEC le SPY) | Yahoo/CME | cascade |
| R2 | DXY (dollar) en hausse ≥ **X %** sur 5 j | FRED/DXY | cascade |
| R3 | VIX en spike ≥ **Y** (ex. doublement en 5 j) | CBOE | cascade |
| R4 | Corrélation moyenne cross-asset (commo + equity) → ≥ **0,8** | calcul interne | cascade |
| R5 | Rendements US en hausse pendant que les actions baissent (re-pricing de taux) | FRED | cascade |

### Comportement quand le régime est actif

1. **Modèle de corrélation** : basculer en « corrélation = 1 » (aucune diversification supposée).
2. **Hedges désactivés** : l'or / les T-bonds ne sont PLUS traités comme couvertures.
3. **Gel des nouvelles entrées** : pas d'ouverture, sauf validation JCH explicite.
4. **Dé-risquage** : réduire la taille max des positions (facteur à calibrer).
5. **Notification** : alerte Telegram « RÉGIME CASCADE » + le signal déclencheur + date.

### Sortie du régime

Ré-évaluer quand : le VIX se détend, le dollar cesse de monter, et l'or/actions **re-découplent** (corrélation signée < 0 à nouveau) — la phase 2 documentée (2008/2020) où le refuge rebondit après l'assouplissement des banques centrales.

---

## Régime 2 — Momentum crash

### Définition

Débouclage d'un trade bondé (crowded) : les anciens gagnants chutent brutalement **par rotation**, pas par détérioration fondamentale. Nov 2026 : momentum factor −18,3 %, systematic long-short −2,1 % (pire 5 j depuis déc 2023).

### Signaux de détection

| # | Signal | Source | Sens |
|---|--------|--------|------|
| M1 | Drawdown du facteur momentum (S&P) ≤ **−10 % sur 5 j** | CME/S&P | crash |
| M2 | Rotation extrême : leaders antérieurs en chute + low-vol en hausse | CME factor | crash |
| M3 | Crowding : net exposure / ratio long-short aux records (Goldman PB) | Goldman PB | fragilité |
| M4 | « Momentum Fragility Index » élevé (JPM) | JPM | fragilité |
| M5 | Dispersion factorielle en spike | calcul interne | crash |

### Comportement

1. **Circuit-breaker factoriel** : déclencher sur le signal de régime, pas seulement sur la perte de portefeuille.
2. **Réduire l'exposition aux thèmes bondés** (si le système détient des positions alignées au momentum).
3. **Ne pas chasser le rebond** — les débouclages sont violents ET réversibles : rester flat/observateur.
4. **Notification** : alerte « RÉGIME MOMENTUM CRASH ».

---

## Intégration avec les paramètres existants

| Paramètre existant | Ajustement en régime actif |
|--------------------|----------------------------|
| `MAX_DAILY_LOSS` | Réduire (ex. ×0,5) — à calibrer |
| `MAX_POSITION_SIZE` | Réduire (ex. ×0,5) — à calibrer |
| `MAX_DRAWDOWN_PCT` | Seuil de gel abaissé — à calibrer |
| `ATR_SPIKE_FACTOR` | Inchangé (vol) mais couplé au régime |
| Timeout HITL 4 h | **Maintenu** — aucune exécution auto, quel que soit le régime |

## À calibrer (Phase 2 backtest — obligatoire)

Tous les seuils numériques (R2 %, R3, R4, M1, M3…) doivent être fixés sur les
épisodes historiques de la bibliothèque rétrospective : **2008 (Lehman), 2020-03
(COVID), 2026-11 (krach AI)** — jamais sur une intuition. Appliquer la décote
backtest→live de 20-30 %.

## Sources de données à connecter (Agent #4 Marchés + Agent #5 Macro)

- **DXY** (dollar index), **VIX** (CBOE), **rendements US** (FRED), **facteurs S&P** (CME).
- **Prix or/argent/commodités** (Yahoo/CME) pour la corrélation signée R1.
