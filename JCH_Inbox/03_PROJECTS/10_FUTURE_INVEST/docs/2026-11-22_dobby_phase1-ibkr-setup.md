---
project: Future Invest
type: checklist
author: "[[Dobby]]" (lens [[Forge]])
created: 2026-11-22
status: Phase 1 — actions manuelles JC + automatisations Dobby
---

# Phase 1 — Kickoff IBKR (actions JC + Dobby)

> Seul JC peut ouvrir le compte. Dobby automatise tout ce qui est en aval.

## À faire par JC (manuel, ~30 min)

1. **Ouvrir un compte Interactive Brokers** — ibkr.com → « Open Account ».
   - Type : **Individual** + **Margin Account**.
   - Activer les **permissions Futures** ET **US Equities** (pour le volet equity) dès l'ouverture.
   - Résidence fiscale : Belgique (Liège). Point Renard : implications fiscales des
     Futures en Belgique (taxe comptes-titres, plus-values dérivés) à vérifier.
2. **Activer le Paper Trading** (simulation) — TWS : File → Paper Trading Account.
   - On démarre en paper exclusivement (Phase 3), capital réel seulement en Phase 4.
3. **Installer TWS Gateway** (version légère, sans interface graphique) — la laisser
   tourner en arrière-plan sur le M5.
4. **Tester la connexion API** — port 7497 (paper) / 7496 (live).

## À faire par Dobby (automatisé, dès que le compte existe)

1. Créer l'env Python dédié + dépendances (ib_insync, pandas, fastapi, streamlit, redis).
2. Créer le fichier `.env` (jamais committé) :
   ```
   IBKR_HOST=127.0.0.1
   IBKR_PORT=7497
   MAX_DAILY_LOSS_USD=650        # 1,3 % de 50 000 €
   MAX_DRAWDOWN_PCT=10
   MAX_POSITION_SIZE_PCT=5
   TELEGRAM_BOT_TOKEN=...
   TELEGRAM_CHAT_ID=...
   ```
3. Créer le bot Telegram (@BotFather) pour les notifications (règle HITL).
4. Monter le Risk Supervisor **avant** toute exécution (circuit-breaker + régimes).

## Ordre strict (ne pas inverser)

1. Compte IBKR paper → 2. Risk Supervisor déployé → 3. Event Analyzer connecté au
   Decision Layer → 4. Premier run paper (1 event → analyse → décision → exécution simulée).
4. Période de rodage 4 semaines minimum (Phase 3) avant tout capital réel (Phase 4).

## Voir aussi

- `docs/2026-06-04_checklist-lancement.md` (phases complètes)
- `strategy/2026-11-22_dobby_these-consolidee-future-invest.md` (thèse 4 jambes)
