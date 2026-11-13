---
date: 2026-05-25
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-05-25 — vs-code-speech-timeout

## Session — 11:07 — vs-code-speech-timeout

### Contexte
- Modèle : [[Codex]]
- Projet : [[01_AI_IT_TOOLS]]

### Résumé
Updated VS Code Speech to avoid auto-submit on pause during voice dictation.

### Actions
Set accessibility.voice.speechTimeout=0 in VS Code user settings; verified JSON update.

### Décisions
Keep voice dictation from auto-submitting after pauses; continue troubleshooting MCP separately if needed.

### Prochaines étapes
Re-test voice dictation in VS Code; if the loop persists, disable Copilot Chat or its MCP server temporarily.
