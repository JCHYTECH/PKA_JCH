---
date: 2026-11-03
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-11-03 — consolidation-routing-automatique

## Session — 15:41 — consolidation-routing-automatique

### Contexte
- Modèle : deepseek
- Projet : AI_IT_TOOLS

### Résumé
Consolidation du routing automatique : slugs Anthropic mis a jour (sonnet-5-5, haiku-5-5, opus-5-5) dans 13 scripts, model_config.json cree (etait manquant, model_client.py lisait un fichier inexistant), modeles.html corrige.

### Actions
13 scripts corriges (analyzer, identify_skips, generate_van_fiches, analyzer_archive_vision, inject_notes, dobby_weekly_report, dobby_retro, email_digest, sybil_journal, outlook_imap, outlook_gatekeeper, procurement/config, migrate_instincts) ; scripts/model_config.json cree (remplace le snapshot orphelin logs/model_config.json supprime) ; slugs Ollama qwen3.6/gemma4 -> gemma3:27b ; table routing modeles.html corrigee.

### Décisions
Slugs Anthropic API exacts verifies via l'API : claude-sonnet-5-5, claude-haiku-5-5, claude-opus-5-5 ; cascade haiku/sonnet/opus preservee ; Ollama local = gemma3:27b (M1).

### Prochaines étapes
Relancer ollama serve sur M1 pour --model local et les taches ollama ; verifier le pipeline DECOUVERTES au prochain run (analyzer).
