# AI_IT_TOOLS — Executive Summary

> Document interne — infrastructure PKA uniquement.
> Généré le 2026-07-03 par Dobby 🦉. Version 1.0.

---

## En une phrase

**Infrastructure IA multi-modèles qui fait fonctionner PKA_JCH — 31 agents spécialisés, hub OpenRouter, skills automatisés, mémoire persistante.**

---

## Ce que c'est

Le système nerveux de PKA_JCH. Pas un produit — la plateforme qui rend tous les autres projets possibles.

---

## Composants

| Composant | Rôle |
|-----------|------|
| **Dobby 🦉** | Orchestrateur central — route les demandes vers 30 spécialistes |
| **team.db** (SQLite) | Base de données relationnelle — membres, mémoire, skills, décisions |
| **MEMORY.md** | Journal chronologique des sessions |
| **Skills** (30+) | Automatismes spécialisés (photo, bioacoustique, IoT, finance, SEO…) |
| **Hub OpenRouter** | Accès unifié à 5 modèles (DeepSeek, Claude, Gemini, Qwen, Kimi) |
| **Graphify** | Knowledge graph extraction automatique |
| **Thread Files** | Living documents par projet |
| **Obsidian Vault** | Wiki interlinké — navigation knowledge graph |

---

## Architecture mémoire

```
Config (SOUL.md, USER.md)
    ↕
State (hardware-state.md, etat-projets.md, roadmap-90-jours.md)
    ↕
Log (MEMORY.md, team.db, TEAM_Inbox/)
    ↕
Knowledge (wiki/, graphify-out/, skills/)
```

Séparation stricte State/Log — les décisions et l'état ne sont jamais confondus avec l'historique.

---

## Modèles IA

| Modèle | Usage |
|--------|-------|
| DeepSeek V4 | Session principale (orchestration, analyse) |
| Claude | Code review, documents longs |
| Gemini | Vision, SEO, image generation |
| Qwen | Code, scripts Python |
| Ollama local (M5/M1) | Gemma4, Llama vision, Qwen coder |

---

*Document interne — ne pas partager en externe. Cette infrastructure est le socle technique de tous les projets PKA.*
