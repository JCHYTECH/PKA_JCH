---
project: Future Invest
type: research-prompt
author: "[[Dobby]]"
created: 2026-06-04
status: à exécuter
outil_recommandé: Perplexity / Gemini avec recherche web / ChatGPT browsing / deep-research skill
---

# Prompt — Recherche DIY Trading Algorithmique Futures

> Coller ce prompt dans un LLM avec accès web activé.
> Résultats à sauvegarder dans `research/2026-06-04_resultats-recherche-diy.md`

---

```
Tu es un chercheur expert en trading algorithmique. Effectue une recherche 
approfondie et multi-sources sur les systèmes de trading automatisé DIY 
appliqués aux marchés Futures, tels qu'ils sont documentés par des praticiens 
indépendants (YouTube, Reddit, GitHub, blogs, forums).

## Angles de recherche à couvrir

1. ARCHITECTURE TECHNIQUE DIY
   - Quelles stacks techniques les développeurs indépendants utilisent-ils 
     réellement en production ? (Python, ib_insync, LEAN, NinjaTrader, etc.)
   - Quelles sont les erreurs d'architecture les plus fréquemment signalées ?
   - Quels patterns ont survécu à la mise en production vs ceux qui ont échoué ?

2. BROKERS & CONNEXIONS API
   - Retours d'expérience réels sur Interactive Brokers, Tradovate, NinjaTrader 
     en mode automatisé — fiabilité, déconnexions, limites API
   - Coûts cachés et pièges signalés par les praticiens
   - Alternatives low-cost recommandées par la communauté

3. GESTION DU RISQUE & CIRCUIT BREAKER
   - Comment les traders DIY implémentent-ils concrètement les protections 
     contre les runaway algorithms (boucles infinies d'ordres, etc.) ?
   - Incidents réels documentés et ce qui a été appris
   - Paramètres de risque typiques recommandés pour un débutant sur futures

4. SOURCES DE DONNÉES & INTELLIGENCE MARCHÉ
   - Quelles sources de données alternatives les praticiens DIY utilisent-ils 
     gratuitement ou à faible coût ?
   - Utilisation du COT report, sentiment, saisonnalité dans des systèmes réels
   - Intégration de LLM (GPT, Claude) dans des pipelines de trading — retours terrain

5. ERREURS CLASSIQUES & LEÇONS DES COMMUNAUTÉS
   - Top 10 des erreurs de débutants sur les forums Reddit (r/algotrading, 
     r/FuturesTrading) et YouTube
   - Ce que les tutorials ne disent pas (overfitting, slippage, données survivorship bias)
   - Différences réelles entre backtesting et performance live

## Sources à prioriser
- YouTube : chaînes de traders algorithmiques indépendants avec démonstrations live
- Reddit : r/algotrading, r/FuturesTrading, r/learnpython (posts avec upvotes élevés)
- GitHub : dépôts publics de systèmes de trading complets avec documentation
- Blogs : QuantStart, Algorithmic Trading Club, blogs personnels de traders
- Forums : NinjaTrader Community, Interactive Brokers API forum

## Format de sortie attendu
- Rapport structuré par angle de recherche
- Chaque affirmation sourcée (URL ou référence)
- Section "Consensus communautaire" : ce sur quoi tout le monde s'accorde
- Section "Points de débat" : là où les avis divergent
- Section "Pépites inattendues" : conseils peu connus mais fortement validés
- Conclusion : 10 recommandations concrètes applicables à notre système
```

## Voir aussi

- [[INDEX|Future Invest — Index projet]]
- [[2026-06-04_checklist-lancement|Checklist de lancement]]
