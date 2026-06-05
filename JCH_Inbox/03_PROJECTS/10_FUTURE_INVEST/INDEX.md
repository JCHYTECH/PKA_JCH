---
project: Future Invest
created: 2026-06-04
status: phase-0-en-cours
owner: JCH
orchestrator: "[[Dobby]]"
team:
  - "[[Bruno]]"
  - "[[Forge]]"
---

# Future Invest — Projet de Trading Automatisé sur Futures

## Objectif
Concevoir et déployer un système de trading algorithmique sur les marchés Futures, avec une approche Human-in-the-Loop : co-création humain/IA pour les décisions, exécution automatique, circuit-breaker supervisé par l'IA.

## Structure du projet

| Dossier | Contenu |
|---------|---------|
| `strategy/` | Profil investisseur, stratégies sélectionnées, règles de risque |
| `architecture/` | Schémas techniques, choix de stack, documentation système |
| `docs/` | Guides didactiques, glossaire Futures, ressources formation |
| `research/` | Analyses de marché, notes de veille, benchmarks |
| `logs/` | Journal de bord des sessions de trading, événements circuit-breaker |

## Documents clés

| Document | Emplacement | Statut |
|----------|------------|--------|
| [[2026-06-04_bruno_profil-investisseur\|Profil investisseur — Bruno]] | `strategy/` | 🟡 À remplir |
| [[2026-06-04_event-analyzer-architecture\|Event Analyzer — Architecture v1]] | `architecture/` | ✅ Draft |
| [[2026-06-04_checklist-lancement\|Checklist de lancement]] | `docs/` | 🟡 En cours |
| [[2026-06-04_prompt-recherche-diy\|Prompt recherche DIY communities]] | `research/` | ⬜ À exécuter |
| Résultats recherche DIY | `research/` | ⬜ À créer après exécution |

## Modules du système

| Module | Rôle | Statut |
|--------|------|--------|
| **Event Analyzer** | Analyse macro événementielle — OSINT + chaîne causale + opinions | 🟡 Architecture draft |
| **Decision Layer** | Co-création humain/IA — validation des thèses | ⬜ À concevoir |
| **Execution Layer** | Passage automatique des ordres via IBKR | ⬜ À concevoir |
| **Risk Supervisor** | Circuit-breaker + pré-freinage IA | ✅ Architecture draft |
| **Notification Layer** | Telegram Bot + Dashboard Streamlit | ✅ Architecture draft |

## Voir aussi

- [[Dobby]] — orchestrateur
- [[Bruno]] — analyste finance & investissement
- [[Forge]] — développeur système

## Statut des phases

| Phase | Description | Statut |
|-------|-------------|--------|
| 0 | Profil investisseur (questionnaire [[Bruno]]) | 🟡 À compléter |
| 0 | Recherche communautés DIY (prompt prêt) | ⬜ À exécuter |
| 0 | Formation personnelle minimale (Futures) | ⬜ À planifier |
| 1 | Architecture système globale | ✅ Draft |
| 1b | Event Analyzer — architecture | ✅ Draft |
| 1c | Améliorations équipe (COT, Kelly, vectorDB…) | ✅ Documenté |
| 2 | Environnement technique (IBKR Paper + Python) | ⬜ À venir |
| 3 | Bibliothèque rétrospective (10 événements) | ⬜ À venir |
| 4 | Backtesting règles de risque | ⬜ À venir |
| 5 | Paper trading — rodage 4 semaines | ⬜ À venir |
| 6 | Go Live — capital réel | ⬜ À venir |

## Prochain item bloquant

> **Remplir le questionnaire [[Bruno]]** (`strategy/2026-06-04_bruno_profil-investisseur.md`)  
> Sans le profil investisseur, on ne peut pas choisir les marchés cibles  
> ni calibrer les paramètres de risque.
