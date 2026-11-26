# Décisions PKA — Registre des décisions structurelles

last_updated: 2026-10-28

> **Fichier State** — registre des décisions structurelles **déjà tranchées** qui modifient ≥ 2 fichiers canoniques.
> Complément de `decisions-actives.md` (décisions **en attente** d'arbitrage JC).
> Mise à jour par Dobby après chaque décision structurelle (règle `SOUL.md` — maintenance des tableaux de pilotage).
> Backfill complet depuis `MEMORY.md` (Log) le 2026-10-28 — source : chronologie accumulée.

---

## Format

| Date | Décision | Périmètre | Fichiers canoniques touchés | Statut |
|------|----------|-----------|------------------------------|--------|

---

## Registre (ordre chronologique inversé)

| Date | Décision | Périmètre | Fichiers canoniques touchés | Statut |
|------|----------|-----------|------------------------------|--------|
| 2026-10-27 | **Garde-fou pré-action (decision-gate)** — questions fermées G1–G4, mode fantôme, pas de hook | Sécurité transverse | `skills/decision-gate/`, `bin/pka-gate`, `SOUL.md`, `skills/INDEX.md`, `securite-sauvegardes.md`, `instructions-systeme.md` | ✅ fantôme |
| 2026-10-27 | **M1 décommissionné** (MacBook Pro M1, panne écran + FileVault) | Infra | `docs/system/m1-decommission.md`, `bin/m1-wake`, `bin/m1-rearm`, 6 scripts Ollama → API | ✅ décidé — migration en cours |
| 2026-10-22 | **Journée infrastructure** — boucle mémoire autonome, gouvernance MCP, tracing coûts, banc mémoire, règles SOUL Flash | Système / mémoire | `bin/pka-memory-review`, `pka_mcp_guard.py`, `pka_llm_trace.py`, `pka_memory_eval.py`, `SOUL.md` | ✅ actif |
| 2026-10-20 | **Purge historique Git** 88 Go → 617 Mo (`filter-repo`) | Repo | `.git` (rewrite) + backup `.git.bak` | ✅ fait |
| 2026-10-04 | **Améliorations agentiques** — `bin/pka` CLI unifié, snapshot/dérive, host-watch, règle « spécialistes à la demande » | Système | `bin/pka`, `pka_state_snapshot.py`, `pka_host_watch.py`, `SOUL.md` | ✅ actif |
| 2026-08-31 | **Roster réaligné sur team.db** (31 spécialistes actifs) | Équipe | `team.db`, `ROSTER.md`, `SOUL.md`, pointers | ✅ actif |
| 2026-07-16 | **Gouvernance — 3 docs fondateurs** (principes architecturaux, sécurité/sauvegardes, roadmap long-terme) | Architecture | `docs/system/principes-architecturaux.md`, `securite-sauvegardes.md`, `roadmap-long-terme.md`, `AGENTS.md`, `outils-index.md` | ✅ actif |
| 2026-07-16 | **Recrutement Scarabée #34** (Conception 3D & fabrication) | Équipe | `team.db`, `ROSTER.md`, pointers | ✅ actif |
| 2026-07-07 | **Bootstrap GLM 5.2** (BOOTSTRAP.md + pointer GLM.md + deepseek_chat.py enrichi) | Modèles / pointers | `BOOTSTRAP.md`, `GLM.md`, `deepseek_chat.py`, `dobby.sh` | ✅ actif |
| 2026-07-05 | **CoALA Memory Layer v0.2** — 4 types de mémoire + auto-reconcile + memory guard (injection) | Mémoire | `pka_memory_capture.py`, `SOUL.md` | ✅ actif |
| 2026-07-03 | **Threads Memory System → `pka-thread-file`** (living thread par projet, 10 créés) | Mémoire | `skills/pka-thread-file/`, `thread-file-template.md`, 10 `thread-*.md` | ✅ actif |
| 2026-06-24 | **Distinction mémoire session ↔ long-terme (Mem0)** + auto-extract de faits | Mémoire | `SOUL.md`, `AGENTS.md`, `pka_memory_capture.py` | ✅ actif |
| 2026-06-22 | **Fusion Ariane #13 + Fourmi #31 → Forge / Araignée** ; Musaraigne #32 onboardée | Équipe | `team.db`, `ROSTER.md`, `SOUL.md` | ✅ actif |
| 2026-06-19 | **Split SOUL / USER / MEMORY (pattern Hermes)** + Memory Nudge + 3 tables de pilotage + 42 instructions consolidées | Architecture mémoire | `SOUL.md`, `USER.md`, `MEMORY.md`, `etat-projets.md`, `matrice-modeles.md`, `decisions-pka.md`, `instructions-systeme.md`, + 10 fichiers | ✅ actif |
| 2026-06-19 | **Honcho PKA + FTS5** (tables `user_model` + `session_fts`) | Mémoire / recherche | `team.db`, `pka_honcho_analyze.py`, `pka_fts_index.py`, `pka_retrieve.py` | ✅ actif |
| 2026-06-19 | **Gateway unifiée `pka_gateway.py`** (5 canaux d'ingestion) | Ingestion | `pka_gateway.py`, `team.db` (`gateway_messages`), launchd | ✅ actif |
| 2026-06-18 | **Règle d'adresse ajoutée aux pointers** (AGENTS.md, DEEPSEEK.md) | Règles | `AGENTS.md`, `DEEPSEEK.md`, `generate_tool_pointers.py` | ✅ actif |
| 2026-06-17 | **Memory Layer pipeline** (session_extract + retrieve + generate_memory ; Corbeau Memory Curator) | Mémoire | `pka_session_extract.py`, `pka_retrieve.py`, `pka_generate_memory.py`, `team.db` | ✅ actif |
| 2026-06-13 | **Règle « Vérification avant affirmation »** | Règles | `AGENTS.md`, `MEMORY.md` | ✅ actif |
| 2026-06-12 | **Skills audit + politique shadow** (59 skills, local `skills/` prioritaire sur fondation) | Skills | `skills/` (4 corrigés, 4 shadowés, 2 créés), `skills/INDEX.md` | ✅ actif |
| 2026-06-05 | **dobby_retro.py réécrit** (multi-source, tables `retro_patterns` + `retro_sessions`) | Auto-training | `dobby_retro.py`, `team.db` | ✅ actif |

---

## Détail — 2026-06-19 : Split SOUL / USER / MEMORY (fondation)

**Contexte.** Analyse du transcript Hermes Agent (NousResearch) + 3 spécialistes (Forge, Corbeau, Furet). Objectif : extraire les patterns applicables à PKA.

**Décision.**
1. **Split SOUL.md / USER.md / MEMORY.md** — architecture mémoire 3 fichiers distincts (pattern Hermes soul/user/memory).
2. **Memory Nudge** — extraction mémoire post-réponse (`pka_memory_nudge.py`).
3. **Alerte compression contexte 50 %** — règle SOUL.md.
4. **3 tables de pilotage** — `etat-projets.md`, `matrice-modeles.md`, `decisions-pka.md`.
5. **instructions-systeme.md** — 42 instructions consolidées en tableau unique.

**Fichiers.** 10 créés (`SOUL.md`, `USER.md`, `etat-projets.md`, `matrice-modeles.md`, `decisions-pka.md`, `instructions-systeme.md`, `roadmap-p2.md`, `pka_memory_nudge.py`, `honcho-pka-design.md`, `fts5-sessions-design.md`) ; 10 modifiés (`MEMORY.md`, `AGENTS.md`, `DEEPSEEK.md`, `GEMINI.md`, `QWEN.md`, `CLAUDE.md`, `ADAPTER-PROMPT.md`, `SOUL.md`, `outils-index.md`, `INDEX.md`).

> ⚠️ Note : `decisions-pka.md` a été créé nominalement le 2026-06-19 mais le fichier était absent du disque — recréé et backfillé le 2026-10-28 (ce fichier).

---

## Détail — 2026-10-27 : Garde-fou pré-action (decision-gate)

**Contexte.** Le système tourne en mode YOLO (auto-approve) sur 6 CLI d'agents ; personne n'est dans la boucle avant une action destructive, sortante ou touchant un secret.

**Décision.**
1. Introduire un garde-fou pré-action à **questions fermées** (G1 destructif, G2 sortant, G3 secret, G4 conformité), inspiré du pattern Jev/TypeSafe + Warden.
2. **Mode fantôme par défaut** : le garde-fou observe et logge (journal `_local/state/decision-gate.log`) sans rien bloquer, jusqu'à calibration (100–200 cas).
3. **Implicite, pas de hook matériel** pour l'instant — ancré en règle de comportement dans `SOUL.md` ; le pré-contrôle déterministe `bin/pka-gate check` couvre `rm -rf`, `git push --force`, `DROP TABLE`.
4. **Aucun envoi hors machine sans JC.**

**Trace.** Source : transcript vidéo « Obsidian, Claude et Jev : 5 usages pour votre second cerveau » (dans `Downloads/`). Délivrables : `skills/decision-gate/SKILL.md` + `bin/pka-gate`.

---

## Voir aussi

- `decisions-actives.md` — décisions en attente d'arbitrage JC (State complémentaire)
- `MEMORY.md` — chronologie complète (Log), source du backfill
- `SOUL.md` — règle « Maintenance des tableaux de pilotage » (critère : ≥ 2 fichiers canoniques)
