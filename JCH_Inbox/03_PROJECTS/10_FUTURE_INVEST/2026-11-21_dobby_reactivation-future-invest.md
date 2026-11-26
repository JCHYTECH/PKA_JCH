---
project: Future Invest
type: reactivation-memo
author: "[[Dobby]]"
team: ["[[Bruno]]", "[[Forge]]"]
created: 2026-11-21
status: réactivé — Phase 0 en cours
trigger: Krach actions (AI-led, nov 2026) — décision JC de réveiller le projet
---

# Future Invest — Remise en route (2026-11-21)

## Contexte de réactivation

Krach actions en cours (20-21/11/2026), déclencheur : dégonflage du trade IA
(IPO Anthropic, Nvidia −14 %), bascule risk-off généralisée. Chiffres vérifiés
live le 21/11 :

| Indicateur | Valeur |
|------------|--------|
| S&P 500 (SPY) | 689,81 → **−8,6 %** (correction, −10 % sous record) |
| Nasdaq-100 (QQQ) | 608,45 → **−10,5 %** (bear intraday, −20 % du high) |
| Or (GLD) | 322,87 → **−9,2 %** (baisse avec les actions) |
| Pétrole (USO) | 139,63 → −4,1 % |
| Blé (WEAT) | 21,44 → −1,9 % |

**Lecture clé :** l'or baisse en même temps que les actions → signature de
**cascade de liquidité** (tout est vendu pour lever du cash, corrélations → 1).
Ce n'est PAS le comportement « or = valeur refuge » supposé dans les contraintes
d'architecture. Point à intégrer au Risk Supervisor : en crise de liquidité,
la corrélation refuge s'effondre.

## Où on s'était arrêté (juin 2026)

Projet gelé en **Phase 0**, archivé le 2026-06-23. Documents validés et intacts :
- `architecture/2026-06-07_contraintes-style-trading.md` — swing event-driven ✅
- `architecture/2026-06-04_event-analyzer-architecture.md` — draft v1 (8 agents) ✅
- `docs/2026-06-04_checklist-lancement.md` — 6 phases ✅
- `docs/2026-06-07_grille-scoring-backtesting.md` — validé ✅
- `strategy/2026-06-04_bruno_profil-investisseur.md` — 🟡 4 questions ouvertes

## Point bloquant (à lever par JC — seule chose qui a gelé le projet)

4 questions de profil encore ouvertes :
- **A1** — montant alloué au projet (fourchette)
- **B2** — perte maximale acceptable sur une journée → `MAX_DAILY_LOSS`
- **E2** — broker existant (ou non)
- **E3** — exclusions éthiques / personnelles

Plus 3 paramètres de risque à fixer : `MAX_DAILY_LOSS`, `MAX_DRAWDOWN_PCT`,
`MAX_POSITION_SIZE`.

## Feuille de route (reprise ordonnée — ne pas sauter d'étape)

| Phase | Action | Statut |
|-------|--------|--------|
| 0.1 | Répondre aux 4 questions + fixer les 3 paramètres risque | ⏳ JC |
| 0.2 | Exécuter le prompt recherche DIY → résultats | ⬜ |
| 0.3 | Formation minimale Futures (contrat, marge, levier) | ⬜ |
| 2.1 | **Instrumenter le krach actuel = événement #1** bibliothèque rétrospective | ⬜ (maintenant) |
| 2.1 | Compléter à 10 événements historiques (Russie 2010, sécheresse 2012, COVID 2020, Suez 2021, Ukraine 2022, riz Inde 2023…) | ⬜ |
| 1 | IBKR paper + env Python (ib_insync) | ⬜ |
| 2.2-2.3 | Backtest Event Analyzer sur 10 événements + règles de risque | ⬜ |
| 3 | Paper trading 4 semaines (HITL strict, timeout 4h) | ⬜ |
| 4 | Go live — capital réduit 20-30 % | ⬜ |

## Conseil stratégique (Dobby + Bruno)

Le krach est un **catalyseur de reprise**, pas une raison de trader tout de suite :
1. Le système n'est pas construit pour shorter les indices — sa zone d'edge est
   les chocs offre/demande sur commodités (agricole, énergie). Un krach actions
   est un événement macro/liquidité, pas un choc d'offre.
2. La vraie valeur du krach pour nous : c'est un **cas d'étude live gratuit** —
   premier événement documenté de la bibliothèque rétrospective + scénario de
   stress pour le circuit-breaker (une journée à −8,5 % est exactement ce que le
   Risk Supervisor doit détecter).
3. Ne pas rediriger l'architecture vers de l'intraday « profiter du crash » —
   ce serait abandonner l'edge fondamental documenté et entrer sur le terrain où
   le système est le plus faible (timing court, données différées 10-15 min).
