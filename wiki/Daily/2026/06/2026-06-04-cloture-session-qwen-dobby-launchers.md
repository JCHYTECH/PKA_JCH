---
date: 2026-06-04
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-06-04 — Cloture session Qwen Dobby launchers

## Session — 23:11 — Cloture session Qwen Dobby launchers

### Contexte
- Modèle : codex
- Projet : AI_IT_TOOLS

### Résumé
Session de configuration des lanceurs IA PKA. DeepSeek TUI a ete resynchronise avec sa cle, Qwen 3.7 Plus/Max via OpenRouter ont ete valides, Continue VS Code a ete corrige pour lire la cle OpenRouter depuis le fichier local, et les commandes courtes dobby/qwen ont ete creees avec bootstrap PKA complet.

### Actions
Correction DeepSeek TUI via deepseek-tui login; ajout Qwen 3.7 Plus et Max dans ~/.continue/config.ts; remplacement qwen/qwen-max par qwen/qwen3.7-max dans .qwen/settings.json; creation/refonte de bin/qwen, scripts/qwen.py et bin/dobby; creation des liens ~/.local/bin/qwen et ~/.local/bin/dobby; creation de launch command.md; mises a jour docs/termius-mac-ipad.md et wiki/Daily/2026-06-04.md; graphify update execute apres modifications code.

### Décisions
dobby et qwen chargent automatiquement QWEN.md, ADAPTER-PROMPT.md, MEMORY.md, TEAM/dobby.md, TEAM/ROSTER.md, wiki/index.md, les deux dernieres daily, le scan projets et le scan inbox; dobby utilise Qwen 3.7 Plus par defaut et dobby max utilise Qwen 3.7 Max; bin/dobby.sh reste le lanceur multi-modeles historique.

### Prochaines étapes
Utiliser dobby "question" ou dobby max "question" pour des questions simples sans outils; utiliser Codex/Claude/Gemini quand une tache exige filesystem, shell, navigateur ou edition de fichiers.
