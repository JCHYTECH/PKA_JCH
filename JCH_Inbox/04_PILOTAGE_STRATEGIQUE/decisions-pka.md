# Registre des décisions PKA
> Décisions structurelles transverses — hors ADR projet (WildNexus, etc.).
> Dernière mise à jour : 2026-06-19 par Dobby 🦉
> 
> **Lecture :** une ligne = une décision qui a changé l'architecture du système.
> Les décisions projet-spécifiques sont dans leurs ADR respectives.

---

## 2026

| Date | Décision | Contexte | Impact | Fichiers modifiés |
|------|----------|----------|--------|-------------------|
| 2026-06-19 | **Split SOUL.md / USER.md / MEMORY.md** | Pattern Hermes (soul/user/memory) — séparation claire personnalité / profil utilisateur / connaissances | Architecture mémoire 3 fichiers, lecture ordonnée au démarrage, 6 pointeurs synchronisés | `SOUL.md` (nouveau), `USER.md` (nouveau), `MEMORY.md` (révisé), `AGENTS.md`, `DEEPSEEK.md`, `CLAUDE.md`, `GEMINI.md`, `QWEN.md`, `ADAPTER-PROMPT.md` |
| 2026-06-19 | **Skill system-improvement-ingest** | Besoin d'une grille systématique pour extraire des améliorations de tout document | Toute analyse de document externe passe par la grille 6 axes standard | `skills/system-improvement-ingest/SKILL.md`, `outils-index.md` |
| 2026-06-19 | **Tableau instructions-systeme.md** | Consolidation de 42 instructions dispersées en 1 tableau | Vue unique de tous les prompts, skills, loops, règles, outils, pilotage | `JCH_Inbox/04_PILOTAGE_STRATEGIQUE/instructions-systeme.md` |
| 2026-06-19 | **Memory Nudge — extraction post-réponse** | Pattern Hermes — analyser le transcript toutes les ~10 réponses | Mémoire continue, pas seulement post-session | `scripts/pka_memory_nudge.py`, `SOUL.md` |
| 2026-06-19 | **Alerte compression contexte** | Pattern Hermes — alerter à 50% du context window | Plus jamais de session qui atteint le plafond en silence | `SOUL.md` (règle) |
| 2026-06-19 | **Tableaux de pilotage (×3)** | One-pager projets, matrice modèles, registre décisions PKA | Vue consolidée remplaçant la lecture dispersée | `etat-projets.md`, `matrice-modeles.md`, `decisions-pka.md` |
| 2026-06-19 | **Design specs Honcho + FTS5** | Spécifications pour user modeling évolutif et recherche full-text historique | Roadmap P1 documentée, prête à implémenter | `docs/system/honcho-pka-design.md`, `docs/system/fts5-sessions-design.md` |
| 2026-06-19 | **Roadmap P2** | Skills auto-générées + Gateway unifiée | Vision long terme documentée | `JCH_Inbox/04_PILOTAGE_STRATEGIQUE/roadmap-p2.md` |
| 2026-06-19 | **Pivot Honcho synchrone** | Mode batch (cron) inefficace — memory_log trop court. Passage en synchrone post-session. | Dobby exécute Honcho en direct, insights → user_model + diff USER.md automatique si confiance ≥0.8 | `SOUL.md`, `docs/system/honcho-pka-design.md` (v0.2), `scripts/pka_honcho_analyze.py` |
| 2026-06-19 | **Pivot Memory Nudge synchrone** | Même problème que Honcho — heuristiques insuffisantes. Passage en synchrone, cohérent avec Honcho. | Dobby exécute Memory Nudge en direct toutes les ~10 réponses | `SOUL.md`, `scripts/pka_memory_nudge.py` |
| 2026-06-19 | **Honcho — 1ère exécution synchrone** | Session 19 juin — 4 insights détectés, 3 appliqués à USER.md (validation JC) | USER.md enrichi de 3 préférences, table user_model active | `USER.md`, `team.db` (user_model) |
| 2026-06-19 | **Gateway unifiée pka_gateway.py** | 6 connecteurs fragmentés → 1 point d'entrée unique. Telegram down → gateway assure la continuité. | 4 canaux actifs, table gateway_messages, launchd watch | `scripts/pka_gateway.py`, `team.db` (gateway_messages), `com.dobby.pka-gateway.plist` |
| 2026-06-17 | **Memory Layer v2 — Procédural + Zettelkasten** | ≥3 feedbacks JC partagés → procédure auto. Jaccard similarité entre entrées | Mémoire procédurale dynamique + linking automatique entre connaissances | `pka_session_extract.py` (étendu), `team.db` (knowledge_links) |
| 2026-06-17 | **pka_pointer_sync.py — synchro automatique** | Détection de dérive entre 6 fichiers pointeurs et team.db | Plus jamais de désynchronisation manuelle des pointers | `scripts/pka_pointer_sync.py`, 6 fichiers pointeurs |
| 2026-06-17 | **pka_conflict_checker.py — détection contradictions** | Inspiré OctoChains — heuristique + LLM | Détection de conflits numériques, recommandations opposées entre spécialistes | `scripts/pka_conflict_checker.py` |
| 2026-06-15 | **pka_prompt_guard.py — sécurité inbox** | Scanner prompt injection 3 niveaux (OWASP LLM01) | Protection automatique de tous les fichiers entrants dans l'inbox | `scripts/pka_prompt_guard.py`, pipeline ingest |
| 2026-06-14 | **Wokwi adopté comme smoke test CI** | WildNexus P0 — logique firmware sans hardware | CI possible avant d'avoir le matériel physique | `03_WILDNEXUS/03_P0_ENGINEERING/05_SIMULATION/wokwi/` |
| 2026-06-13 | **Architecture IoT distribuée — 3 HA locaux** | Belgique (M5 Docker), Italie (RPi 5), Van (RPi 5) — autonomes | Pas de serveur central, supervision unifiée via iPhone + Tailscale | `docs/system/station-domotique-plan-rpi5.md` |
| 2026-06-12 | **Skills — politique de shadow** | Skills locaux `skills/` > skills fondation runtime | Priorité aux versions PKA améliorées, shadow systématique | `skills/` (ingest, capture, brief, status → shadowés) |
| 2026-06-09 | **DuckDuckGo comme moteur de recherche** | Bing indisponible dans DeepSeek TUI | Toute recherche web PKA passe par DuckDuckGo | `SOUL.md`, `CLAUDE.md`, `AGENTS.md` |
| 2026-06-06 | **Onboarding Araignée (#30) + Fourmi (#31)** | Gaps IoT + électronique/protocoles | Couverture complète hardware WildNexus | `TEAM/araignee.md`, `TEAM/fourmi.md`, `team.db`, `TEAM/ROSTER.md` |
| 2026-06-05 | **Pipeline LoRA fine-tuning via MLX** | Entraînement `dobby-prompt` sur M1 (32 GB) | Capacité de fine-tuning local sans cloud | `scripts/dobby_train.py`, modèle Ollama `dobby-prompt` |
| 2026-06-04 | **Allègement MEMORY.md — historique → wiki** | MEMORY.md trop lourd, split historique | MEMORY.md passe de ~400 à ~200 lignes | `wiki/archives/memory-history-2026-05.md` |

---

## Format d'une nouvelle entrée

```markdown
| YYYY-MM-DD | **Titre** | Pourquoi cette décision | Ce qui a changé concrètement | Fichiers impactés |
```

---

## Lien avec les ADR projet

Les décisions techniques spécifiques à un projet sont dans leurs ADR :
- **WildNexus** : `03_WILDNEXUS/02_DECISIONS/ADR/`
- **Vetalyx** : `08_VETALYX/`
- **ARTEON** : `02_ARTEON/`

Ce registre couvre uniquement les décisions qui traversent les projets ou changent l'architecture de PKA elle-même.

---

*Mise à jour automatique par Dobby après chaque décision structurelle.
Toute décision qui modifie ≥2 fichiers canoniques ou introduit un nouveau pattern doit être enregistrée ici.*
