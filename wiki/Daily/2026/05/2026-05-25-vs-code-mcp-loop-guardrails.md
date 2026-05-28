---
date: 2026-05-25
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-05-25 — vs-code-mcp-loop-guardrails

## Session — 11:09 — vs-code-mcp-loop-guardrails

### Contexte
- Modèle : [[Codex]]
- Projet : [[01_AI_IT_TOOLS]]

### Résumé
Disabled VS Code MCP discovery, autostart, and apps after voice auto-submit fix did not stop the activation loop.

### Actions
Set chat.mcp.discovery.enabled=false, chat.mcp.autostart=false, chat.mcp.apps.enabled=false in VS Code user settings.

### Décisions
Treat the remaining loop as chat/MCP-side rather than speech-side.

### Prochaines étapes
Retest dictation; if the loop persists, disable GitHub Copilot Chat or Azure MCP server extension next.
