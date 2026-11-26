---
date: 2026-06-19
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-06-19 — amelioration-systeme-hermes-pka

## Session — 09:12 — amelioration-systeme-hermes-pka

### Contexte
- Modèle : deepseek
- Projet : AI_IT_TOOLS

### Résumé
Analyse approfondie de l'architecture Hermes Agent (NousResearch, 197k★) et transposition vers PKA-JCH. Livrables : split SOUL.md/USER.md/MEMORY.md, Memory Nudge (pka_memory_nudge.py), alerte compression contexte, skill system-improvement-ingest (grille 6 axes), 3 tableaux de pilotage (etat-projets, matrice-modeles, decisions-pka), design specs Honcho PKA + FTS5 sessions, roadmap P2, instructions-systeme.md (42 instructions consolidees).

### Décisions
Split SOUL/USER/MEMORY (pattern Hermes), Memory Nudge post-reponse, alerte compression contexte 50%, skill system-improvement-ingest, tableaux de pilotage x3

### Prochaines étapes
Implementer pka_honcho_analyze.py (P1), creer table user_model dans team.db, coder pka_fts_index.py, etendre pka_retrieve.py avec mode --fts
