---
date: 2026-05-25
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-05-25 — Skills common index

## Session — 10:00 — Skills common index

### Contexte
- Modèle : [[Codex]] CLI / GPT-5
- Projet : PKA

### Résumé
Creation of a shared PKA guideline for skill inventory and runtime mapping across [[Codex]], [[Claude]], and other local skill stores. The index records where skills live, which runtime can actually load them, and where no Gemini skill was found.

### Actions
- Added wiki/Guidelines/GL-002-skill-inventory.md.\n- Linked it from wiki/Guidelines/INDEX.md and wiki/index.md.\n- Cross-referenced it from internal-agent-governance/skills/README.md.\n- Updated wiki index stats and date.

### Décisions
Skills should be inventoried as runtime-scoped capabilities, not treated as globally available artifacts.

### Prochaines étapes
Keep the guideline updated whenever a new skill store appears or a runtime gains/loses discovery support.
