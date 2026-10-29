# Thread — AI_IT_TOOLS

> Living document — mis à jour automatiquement par Dobby 🦉 en fin de session.
> **Dernière mise à jour** : 2026-10-22 — boucle mémoire autonome, gouvernance MCP, tracing coûts, banc mémoire, export portable
> **Statut** : 🟢 actif

---

## Vue d'ensemble

Infrastructure IA et outils PKA — maintenance du système Dobby, skills, mémoire, modèles, et architecture multi-modèles (DeepSeek, Claude, Gemini, Qwen). Hub OpenRouter structuré. Bootstrap mémoire v2 opérationnel.

---

## État actuel

| Axe | Statut | Détail |
|-----|--------|--------|
| Global | 🟢 | Système stable, P0-P2 terminés (19/06) |
| Skills | 🟢 | **34 skills** (comptage 22/10), shadow système |
| Memory Layer | 🟢 | MEMORY.md + team.db + FTS5 (67 sessions indexées) + boucle autonome |
| Boucle mémoire | 🟢 | **Nouveau 22/10** — `bin/pka-memory-review` (review LLM + auto-skill), launchd quotidien 09:15 |
| Gouvernance MCP | 🟢 | **Nouveau 22/10** — `pka_mcp_guard.py` (registre + scan tool poisoning) |
| Tracing coûts | 🟢 | **Nouveau 22/10** — `pka_llm_trace.py`, table `llm_calls` |
| Banc mémoire | 🟢 | **Nouveau 22/10** — `pka_memory_eval.py`, hit@5 66,7 %, MRR 0,556 |
| Export portable | 🟢 | **Nouveau 22/10** — `pka_memory_export.py`, 322 faits atomiques |
| OpenRouter Hub | 🟢 | Restructuré 01/07, multi-modèle opérationnel |
| Code base | 🟢 | **126 scripts Python**, 57 binaires `bin/`, 117 fichiers `.md` |

---

## Décisions clés

| Date | Décision | Contexte |
|------|----------|----------|
| 2026-10-22 | **Boucle mémoire autonome** | `pka-memory-review` : review LLM (deepseek-chat), auto-skill, FTS, apply. Launchd 09:15 quotidien |
| 2026-10-22 | **Gouvernance MCP** | `pka_mcp_guard` — registre versionné + scan tool poisoning (OWASP ASI01) |
| 2026-10-22 | **Banc mémoire** | LoCoMo-like : hit@5 66,7 %, MRR 0,556, 306 tokens/requête |
| 2026-10-22 | **Retriever corrigé** | tokenisation (phrases entières ne matchaient jamais), classement par score, source State ajoutée |
| 2026-07-03 | Création skill `pka-thread-file` | Analyse Threads Memory System (Ev Chapman) — gap identifié : pas de living thread files par projet |
| 2026-07-03 | Template thread-file deployé | Standard unique pour tous les projets PKA |
| 2026-06-19 | Split SOUL/USER/MEMORY | Pattern Hermes — séparation personnalité / profil / connaissances |
| 2026-06-19 | Memory Nudge synchrone | Mode batch inefficace → passage en synchrone post-réponse |

---

## Prochaine étape

**Action** : Maintenance — utiliser `pka-thread-file` à chaque fin de session projet
**Deadline** : Continu
**Responsable** : Dobby 🦉

---

## Historique sessions

| Date | Résumé session | Livrable |
|------|---------------|----------|
| 2026-10-22 | Loop mémoire autonome + gouvernance MCP + tracing + banc + export portable ; retriever corrigé | `bin/pka-memory-review`, `scripts/pka_mcp_guard.py`, `pka_llm_trace.py`, `pka_memory_eval.py`, `pka_memory_export.py` |
| 2026-10-22 | Re-vérification des 8 projets (correction de 5 notes) | `2026-10-22_dobby_reverification-projets.md` |
| 2026-07-03 | Analyse Threads Memory System → skill pka-thread-file créé, template deployé, skill enregistré dans outils-index.md | `TEAM_Inbox/2026-07-03_dobby_analyse-threads-memory-system.md` |
| 2026-07-01 | Hub OpenRouter restructuré | — |
| 2026-06-19 | Split SOUL/USER/MEMORY, P0-P2 terminés | — |

---

## Liens

- INDEX : `03_PROJECTS/01_AI_IT_TOOLS/INDEX.md`
- Skills : `skills/` (30+ skills)
- Outils index : `docs/system/outils-index.md`
- Memory bootstrap : `docs/system/dobby-memory-bootstrap.md`

---

*Fichier maintenu par Dobby 🦉 via le skill `pka-thread-file`. Ne pas éditer manuellement.*
