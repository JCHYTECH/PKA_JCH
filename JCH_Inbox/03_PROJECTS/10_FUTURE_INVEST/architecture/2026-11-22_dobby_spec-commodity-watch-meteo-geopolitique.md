---
project: Future Invest
type: spec
module: Commodity Watch (surveillant météo + géopolitique)
author: "[[Dobby]]" (lens [[Forge]] / [[Araignée]])
created: 2026-11-22
status: v1 — opérationnel (script + LaunchAgent)
trigger: demande JC — surveiller en continu la météo et la géopolitique pour le volet futures
---

# Spec — Commodity Watch (météo + géopolitique, continu)

## Objectif

Alimenter le volet **futures** (agricole : blé/maïs/riz/soja ; transition : argent,
lithium, carbone) par un **surveillant continu** qui détecte en amont :
1. Les **chocs météo** (sécheresse, gel, El Niño/La Niña, mousson indienne).
2. Les **chocs géopolitiques** (embargos, restrictions d'export, sanctions, conflits).

Ces signaux sont les déclencheurs de l'Event Analyzer (Agents #1 Agricole + #2 Géopolitique) —
le surveillant ne trade pas, il **collecte, score et journalise** en continu pour bâtir
l'historique de signaux (Phase 2) et déclencher l'analyse quand un seuil est franchi.

## Sources

| Domaine | Source | Signal | Accès |
|---------|--------|--------|-------|
| Géopolitique | GDELT DOC 2.0 | comptage d'articles (30 j) sur requêtes ciblées | API gratuite |
| Météo (sécheresse US) | US Drought Monitor | % superficie en D1-D4 (maïs/soja/blé US) | JSON gratuit |
| Météo (ENSO) | NOAA CPC | statut El Niño / La Niña / neutre | à brancher (v2) |
| Mousson Inde (riz) | IMD | avancée/intensité de la mousson | à brancher (v2) |

## Requêtes géopolitiques (v1)

`export ban grain` · `export restriction rice` · `india rice export` · `wheat export
russia ukraine` · `drought` · `sanction fertilizer` — couvrent les 4 grains + les
risques clés (Inde/riz, mer Noire/blé, engrais).

## Seuils d'alerte (v1, à calibrer)

- Géopolitique : ≥ 100 articles / 30 j sur une requête → ⚠️ alerte dans le journal.
- Météo : hausse de la superficie D1-D4 (sécheresse) d'une semaine à l'autre → ⚠️.

## Sortie

- Journal quotidien : `10_FUTURE_INVEST/logs/watch/YYYY-MM-DD.md`.
- État JSON : `_local/futureinvest_watch_state.json` (pour le delta semaine à semaine).
- `--dry-run` par défaut ; `--apply` pour écrire.

## Cadence

LaunchAgent `com.dobby.futureinvest-commodity-watch` — quotidien **08:15** (après les
marchés de nuit, avant l'ouverture US). Installation :
`launchctl load ~/Library/LaunchAgents/com.dobby.futureinvest-commodity-watch.plist`.

## Limites (honnêteté)

- La sécheresse US (Drought Monitor) est un proxy ; elle ne couvre pas l'Inde/la mer
  Noire directement (mousson/ENSO à brancher en v2).
- Les comptages GDELT sont un signal de **flux d'information**, pas de fondamentaux —
  à croiser avec les prix (Agent #4).
- Premier run à tester (réseau) avant de considérer le pipeline fiable.

## Évolution (v2)

- ENSO (NOAA CPC ONI) + mousson indienne (IMD) + gel/températures (NOAA) pour le riz.
- Alertes Telegram quand un seuil est franchi (au lieu du seul journal).
