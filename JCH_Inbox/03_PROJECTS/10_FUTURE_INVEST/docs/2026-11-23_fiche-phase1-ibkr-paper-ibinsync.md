---
project: Future Invest
type: fiche-technique
author: "[[Dobby]]"
created: 2026-11-23
status: à exécuter (après crédit du dépôt)
---

# Phase 1 — Environnement IBKR Paper + Python (ib_insync)

## Objectif
Monter l'environnement technique pour piloter IBKR en **PAPER trading** (aucun fonds réel
consommé), en amont du backtest (Phase 4) et du go live.

## Prérequis
- Compte IBKR approuvé (fait le 23/11).
- Compte **Paper** activé (identifiants paper fournis par IBKR après approbation).
- Python 3.10+ sur M5 (orchestrateur).

## Étapes
1. **Activer l'API** : TWS ou IB Gateway → Global Configuration → API → Settings →
   cocher « Enable ActiveX and Socket Clients » + noter le port.
2. **Ports standards** :
   - TWS : live **7496**, paper **7497**
   - IB Gateway : live **4001**, paper **4002**
3. **Installer la lib** : `pip install ib_insync`
4. **Connexion paper** : `IB().connect(host='127.0.0.1', port=7497, clientId=1)`
5. **Smoke test** : récupérer le contrat d'un future agricole (ex. blé **ZW**) via
   `reqContractDetails`.

## Stack (à valider à l'exécution)
- `ib_insync` (wrapper asyncio, le plus répandu) — alternative : `ib_async` (fork maintenu).
- Orchestrateur = M5. Cette phase **ne dépend pas** des LLM locaux M1.

## À vérifier lors de l'exécution
- Identifiants Paper exacts (Portail → Settings → Paper Trading Account).
- Port réel selon TWS vs Gateway.
- **Market data** : les données futures CME en direct sont **payantes** chez IBKR ; en
  paper, données **différées par défaut**. À arbitrer avec l'Event Analyzer (qui peut
  fonctionner sur des données journalières plutôt que du tick temps réel).

## Prochaine étape après montage
- Phase 3 : bibliothèque rétrospective (10 événements historiques) + backtest des règles de risque.
