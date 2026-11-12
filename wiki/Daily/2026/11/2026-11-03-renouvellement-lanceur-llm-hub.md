---
date: 2026-11-03
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-11-03 — renouvellement-lanceur-llm-hub

## Session — 15:32 — renouvellement-lanceur-llm-hub

### Contexte
- Modèle : deepseek
- Projet : AI_IT_TOOLS

### Résumé
Renouvellement du lanceur LLM et du hub JCH : dobby.sh reecrit (6 modeles), openrouter_chat.py cree, deepseek_chat.py supprime, 6 lanceurs .command recrees, dashboards et dashboard_server.py mis a jour.

### Actions
dobby.sh reecrit (deepseek TUI / openai / anthropic / kimi / gemini / local M1) ; openrouter_chat.py cree (chat OpenRouter + bootstrap AGENTS.md) ; deepseek_chat.py + bootstrap-deepseek-chat.md supprimes ; 10 lanceurs obsoletes supprimes, 6 recrees ; GEMINI.md + CLAUDE.md crees ; ollama_chat.py (OLLAMA_URL env) ; dashboard_server.py (MODELS) ; launch-command.md + hub.html + modeles.html mis a jour.

### Décisions
Bootstrap unique = AGENTS.md pour tous les runtimes ; DeepSeek = TUI (deepseek-tui --yolo) ; OpenAI/Anthropic/Kimi via OpenRouter (gpt-6.1-sol, claude-opus-5.5, kimi-k3.1-pro) ; Gemini via CLI direct ; local = Ollama M1 32 Go (tunnel SSH).

### Prochaines étapes
Mettre a jour le routing automatique (or_route.py + table modeles.html) ; relancer ollama serve sur M1 pour --model local.
