---
date: 2026-05-25
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-05-25 — vs-code-disable-ai-features

## Session — 11:11 — vs-code-disable-ai-features

### Contexte
- Modèle : codex
- Projet : 01_AI_IT_TOOLS

### Résumé
Disabled VS Code built-in AI features after voice and MCP guardrails did not stop the activation loop.

### Actions
Set chat.disableAIFeatures=true in VS Code user settings; kept speech timeout and MCP guards in place.

### Décisions
Treat the loop as coming from VS Code AI/Copilot integration, not the speech extension.

### Prochaines étapes
Restart VS Code and retest dictation; if the loop is gone, re-enable only the features actually needed.
