# AI_IT_TOOLS — Executive Summary

> Document interne — infrastructure PKA uniquement.
> Version 1.1 — état consolidé le 2026-11-05 ; source opérationnelle : `thread-ai-it-tools.md`.

## En une phrase

**AI_IT_TOOLS est l'infrastructure multi-modèles qui fait fonctionner PKA_JCH : Dobby, 31 spécialistes, mémoire persistante, skills, outils locaux et routage entre modèles.**

## Ce que c'est

Le système nerveux de PKA_JCH, et non un produit commercial. L'équipe compte **32 membres : 31 spécialistes + Dobby**, sans confondre les spécialistes délégués avec l'orchestrateur.

## Composants

| Composant | Rôle et état |
|---|---|
| **Dobby** | Orchestration, routage et maintien de la mémoire PKA |
| **team.db + MEMORY.md** | Données structurées et journal chronologique ; recherche FTS5 et export portable disponibles |
| **State / Log** | Séparation entre état courant (`hardware-state.md`, `etat-projets.md`) et historique |
| **Skills** | 34 au comptage du 22/10 ; ce chiffre daté n'est pas présenté comme un inventaire temps réel |
| **Boucle mémoire** | `bin/pka-memory-review`, revue LLM et launchd quotidien documentés |
| **OpenRouter** | Hub d'accès multi-modèles ; les modèles disponibles dépendent de la configuration de chaque outil |
| **Graphify** | Graphe de connaissances et de relations du workspace |
| **Gouvernance et coûts** | Registre/scan MCP, tracing des appels LLM et banc d'évaluation mémoire |
| **Thread files** | État vivant, décisions et prochaines actions par projet |
| **Obsidian / wiki** | Navigation et capitalisation documentaire |

## Architecture mémoire

```text
Config (SOUL.md, USER.md)
    ↕
State (hardware-state.md, etat-projets.md, decisions-actives.md)
    ↕
Log (MEMORY.md, team.db, TEAM_Inbox/)
    ↕
Knowledge (wiki/, graphify-out/, skills/)
```

Les décisions et l'état courant ne sont pas déduits de l'ancien journal sans vérification des sources actives.

## Modèles et limites d'intégration

| Famille | Usage documenté |
|---|---|
| DeepSeek / Kimi | Orchestration et analyse selon les sessions |
| Claude | Code et documents longs selon l'outil configuré |
| Gemini | Vision, recherche et génération selon les intégrations disponibles |
| Qwen | Code et scripts selon l'outil configuré |
| Grok | Prototype Dobby validé en `exec` : mémoire isolée, MCP, délégation et Graphify |
| Ollama local | Modèles locaux sur M5/M1 selon les workflows |

**Limites explicites :** le TUI Grok et ses intégrations externes ne sont pas certifiés. Le skill Kimi `/save` a été créé et chargé en dry-run, mais son invocation utilisateur dans le TUI reste à essayer. Aucun de ces essais ne remplace le Dobby complet existant.

## Prochaine étape

Essayer le TUI/double-clic Grok et l'invocation utilisateur `/save` dans Kimi, tout en poursuivant la maintenance des thread files et de la boucle mémoire.

*Document interne — ne pas partager en externe. Les résultats chiffrés du banc mémoire et les comptages datés restent consultables dans `thread-ai-it-tools.md`.*
