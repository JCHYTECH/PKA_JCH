---
project: Future Invest
type: research
author: "[[Dobby]]" (lens financier [[Bruno]])
created: 2026-11-22
status: livré
scope: Stratégies d'usage de l'IA en investissement + performances semaine du krach (17-21/11/2026)
sources: web (Tavily) — voir références en fin de doc
---

# Analyse — Stratégies d'usage de l'IA en investissement & performances de la semaine

## 1. Panorama des stratégies d'usage de l'IA

Le marché de l'IA en trading pèse **~27,9 Md$ en 2026** (→ 45,7 Md$ en 2030, +13,2 %/an).
L'IA intervient dans **~89 % du volume mondial** et 80 % des institutions. Sous ce
chiffre se cachent des approches très différentes — le point crucial est qu'elles
n'ont PAS la même exposition au risque.

### Taxonomie fonctionnelle (survey Springer, 34 études 2023-2026)

| Paradigme | Mécanisme | Risque dominant |
|-----------|-----------|-----------------|
| **Feature-based** | Le LLM extrait un score (sentiment, embedding) injecté dans un modèle ML/RL. LLM hors boucle d'optimisation. | Hérite du biais du signal injecté |
| **Auxiliary-based** | LLM comme assistant : génère features, labels, données synthétiques. | Qualité du labeling |
| **Policy-based** | LLM directement dans la décision (le modèle choisit l'action). | Hallucination / non-stationnarité |

### Familles concrètes sur le terrain

1. **Sentiment / NLP** — news + réseaux sociaux → score → position. (BlackRock Aladdin, Kensho ~50 k$/an.)
2. **Reinforcement Learning** — agent qui apprend par essai/erreur (PPO, LSTM/Transformer). Fonds autonomes type Aidyia.
3. **Hybride (RL + NLP + techniques + fondamentaux)** — la tendance dominante, « surperforme en régime changeant ».
4. **Copilote / recherche augmentée** — LLM pour lire rapports, filer l'actu ; gain de précision de prévision revendiqué ~+20 %.
5. **Fully autonomous** — RL de bout en bout, sans humain.

### Le constat clé de la littérature (à retenir)

> « Si ta stratégie "IA" n'est que du momentum déguisé, elle se fait prendre quand
> le trade se déboucle. La vraie IA devrait découvrir des signaux non-linéaires,
> complexes, que les modèles factoriels classiques ne voient pas — et être moins
> exposée à ces épisodes. » — J. Lee (Goldman PB), nov 2026.

Autre résultat récurrent : l'intégration du **sentiment LLM aide surtout les agents
LSTM** (les Transformer en profitent moins) ; et le **backtest perd 20-30 % en live**
(slippage, commissions, black swans) — à intégrer dès la conception.

---

## 2. Performances — semaine du krach (17-21/11/2026)

**Déclencheur :** l'IPO d'Anthropic (ANT) devait « confirmer » le trade IA, elle l'a
cassé. Prix $83, ouverture $111,50, clôture $97,17, levée **81,3 Md$ (record absolu)**,
valorisation ~1,5 T$ (2 T$ diluée) — puis repli vers le prix d'IPO. Les fonds ont vendu
leurs autres positions IA pour financer l'allocation IPO.

### Ce qui a perdu (le momentum)

| Indicateur | Performance |
|------------|-------------|
| S&P 500 (SPY) | **−8,6 %** (correction, −10 % sous record) |
| Nasdaq-100 (QQQ) | **−10,5 %** (bear intraday, −20 % du high) |
| Or (GLD) | **−9,2 %** (baisse avec les actions → cascade de liquidité) |
| Momentum factor (S&P) | **−18,3 %** depuis juin 2026 |
| Systematic long-short (Goldman PB) | **−2,1 %** semaine, pire 5 jours depuis déc 2023 |
| Tech funds | −2,0 % (jeudi) ; Asie −2,6 % ; stock-pickers −0,9 % ; multi-strat ~−1 % |
| Micron (MU) | −17 % en séance, −38 % sur un mois |

### Ce qui a tenu (les défensifs)

| Indicateur | Performance |
|------------|-------------|
| Low Volatility factor | **+7,8 %** depuis juin |
| Value / Quality | stables, favorisés (JPM, CME) |
| Growth factor | −8,4 % (moins mal que le momentum pur) |

### Lecture structurelle

- **C'est un « momentum crash »**, pas une remise en cause des fondamentaux. La
  rotation sort des gagnants IA bondés vers le reste du marché.
- Goldman : **6 séances de suite de ventes sur l'IA**, software = 75 % du net selling,
  exposition nette aux software à 2,6 % (ratio long/short 1,3 — plus bas historiques).
- BofA : **6ᵉ semaine de sorties record sur la tech**.
- JPMorgan avait prévenu : « Momentum Fragility Index » élevé, volatilité du momentum
  à des plus hauts de 6 ans → risque de crash de momentum.

**Conclusion performance :** les stratégies IA **à base de momentum** (RL entraîné sur
la persistance des prix, sentiment qui « surfe » les gagnants tech) ont été les plus
touchées. Les stratégies **événementielles/fondamentales et défensives** ont résisté.
« Vraie IA » ≠ « IA momentum déguisée » : c'est toute la différence cette semaine.

---

## 3. Implications pour Future Invest

1. **Notre architecture est du bon côté de la ligne.** L'Event Analyzer est
   fondamental/événementiel (offre/demande commodités), pas momentum. Il n'est pas
   structurellement long tech — donc moins exposé au débouclage qui a frappé la semaine.
2. **Mais deux leçons à intégrer maintenant :**
   - **Corrélation → 1 en crise.** L'or a baissé de −9,2 % avec les actions. La thèse
     « or = refuge » du Risk Supervisor doit être corrigée : en cascade de liquidité,
     tout se vend. Il faut un régime « liquidity cascade » distinct.
   - **Le risque de foule (crowding) est le vrai risque, pas la technologie.** Le
     circuit-breaker doit détecter le « momentum crash », pas seulement la perte.
3. **Pour le backtest (Phase 2) :** ajouter les épisodes de momentum crash à la
   bibliothèque des 10 événements (2009, 2020-03, 2026-11) — pas seulement les chocs
   d'offre agricoles. Le système doit être testé sur les DEUX régimes.
4. **Calibrage réaliste :** appliquer la décote 20-30 % backtest→live dès la grille de
   scoring ; ne pas croire un Sharpe de paper trading sans cette marge.

---

## Références (consultées 2026-11-22)

- lunefi.com/blog/ai-trading-strategies-2026-trends-stats-tips-risks (taille marché, 89 % volume, décote 20-30 %)
- link.springer.com/article/10.1007/s44163-026-02018-0 (taxonomie LLM+RL : feature/auxiliary/policy)
- arxiv.org/html/2510.19173v1 (LSTM+news > Transformer+news)
- linkedin.com/posts/justina-lee (Goldman PB : systematic long-short −2,1 %, momentum selloff, « vraie IA vs IA momentum »)
- finance.yahoo.com/markets/stocks/articles/ai-selloff-hammers-hedge-funds (jeudi : Asia −2,6 %, tech −2,0 %, 6 séances de ventes IA, software 75 %)
- hedgeweek.com/news/china-quant-hedge-funds-hit-by-ai-led-selloff (quants Chine, reversal momentum)
- cmegroup.com/articles/2026/short-term-changes-in-factor-correlations (factors juin→nov : LowVol +7,8 %, Growth −8,4 %, Momentum −18,3 %)
- am.jpmorgan.com (Momentum Fragility Index, volatilité momentum 6 ans)
- investing.com/news/stock-market-news/anthropic-ipo-triggers-ai-selloff (IPO ANT : $83/111,50/97,17, 81,3 Md$ levés)
- finance.yahoo.com (McElligott « They're shooting the generals », Micron −17 %/−38 %)
- in.investing.com (BofA : tech 6ᵉ semaine d'outflows records)
