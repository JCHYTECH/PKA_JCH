# Index central des outils PKA_JCH

> Dernière mise à jour : 2026-07-16 — Ajout principes-architecturaux, securite-sauvegardes, roadmap-long-terme
> Source : `docs/system/outils-index.md`
> Charger ce fichier au début de chaque session pour connaître tous les outils disponibles.

---

## Navigation rapide

| Section | Contenu |
|---------|---------|
| **Architecture** | Memory Layer, gouvernance, décisions |
| **Memory Pipeline** | Session extractor, unified retrieval, MEMORY.md generator |
| Orchestration | Sauvegarde, system check, mémoire |
| Sécurité | Rotation clés, audit, isolation secrets |
| Infrastructure | Backup, sync, maintenance |
| **Navigation Web** | FlareSolverr (Cloudflare bypass), Playwright MCP |
| IA & LLM | Clients modèles, providers, config |
| [[Dobby]] | Rétro, training, rapports |
| Dashboard | Serveur, contrôle, launchd |
| Email | Gatekeepers, digest, auth |
| Fichiers & Inbox | Tool pointers, todo, dropbox |
| Kanban & Plane | Kanban service, Plane adapter |
| Lanceurs | .command pour chaque LLM |
| Skills PKA | Skills internes (vault, ADR, BOM, onboarding) |
| Projets | Scripts par projet (WildNexus, Vetalyx, Photo, InsectNet...) |

---

## Orchestration

- bin/pka — Commande universelle de sauvegarde multi-modèle
- bin/pka-save — Sauvegarde explicite de session
- scripts/pka_save.py — Backend Python de pka-save
- scripts/pka_system_check.py — Health-check auto du système PKA
- scripts/pka_memory_log.py — Log mémoire automatique dans SYBIL_JOURNAL
- scripts/pka_context_profile.py — Génère un profil de contexte pour LLM
- scripts/pka_vigilance.py — Détection de dérive entre DB et fichiers
- scripts/pka_vault_maintenance.py — Maintenance vault Obsidian
- scripts/pka_structure_check.py — Vérifie la structure du workspace

## Memory Pipeline

- scripts/pka_memory_capture.py — **Capture mémoire unifiée v0.2** — API `{fact, category, importance, trust}` avec déduplication, auto-reconcile (override intelligent), memory guard (pre-write injection scan), routage (team.db, MEMORY.md, knowledge, USER.md). Niveaux de confiance : `--trust internal|external|untrusted`. Auto-extract : `--auto-extract` via Gemma3 12B (Ollama M1) ou DeepSeek V3 (fallback).
- scripts/pka_session_extract.py — Extraction post-session : décisions, faits, feedback → `knowledge` + `retro_patterns` + `dobby_feedback`
- scripts/pka_retrieve.py — Recherche unifiée multi-sources (team.db, graphify, file_index, MEMORY.md, wiki) + FTS5 sessions (--fts) + recherche sémantique par embedding (--embed, Ollama M1)
- scripts/pka_memory_prune.py — **Nettoyage automatique MEMORY.md** — Archive les entrées > 90 jours vers wiki/archives/ avec résumé une ligne. Implémente le maillon « Forget » de la boucle CoALA. `--dry-run`, `--days N`, `--force`.
- scripts/pka_generate_memory.py — Régénération automatique de MEMORY.md depuis team.db
- scripts/pka_conflict_checker.py — Détection de contradictions entre rapports de spécialistes (inspiré OctoChains)
- scripts/pka_pointer_sync.py — Synchronisation automatique des 6 fichiers pointeurs PKA
- docs/system/[[pka-memory-layer]].md — Architecture complète du Memory Layer PKA
- scripts/pka_memory_nudge.py — Extraction mémoire post-réponse (pattern Hermes)
- docs/system/honcho-pka-design.md — Design spec Honcho PKA (user modeling évolutif)
- docs/system/fts5-sessions-design.md — Design spec FTS5 sur sessions JSON
- scripts/pka_date_scanner.py — **Nouveau (2026-07-13)** — Scan auto de dates (deadlines, expirations) dans les fichiers → création follow_ups dans team.db. Patterns FR + EN, mots-clés déclencheurs, vacuum des expirés. `--dry-run`, `--all-projects`, `--vacuum`.
- scripts/pka_quick_capture.py — **Nouveau (2026-07-13)** — Capture rapide d'une pensée brute → inbox avec auto-détection du projet. Zéro friction : `pka_quick_capture.py "pensée"`. Option `--urgent`. Pattern inspiré de Sanja (Obsidian+AI).

## Gouvernance & Architecture

- `docs/system/principes-architecturaux.md` — **Nouveau (2026-07-16)** — Les 6 principes fondateurs de PKA (simplicité, modularité, maintenabilité, automatisation, documentation, indépendance fournisseur). Toute décision doit y être conforme.
- `docs/system/securite-sauvegardes.md` — **Nouveau (2026-07-16)** — Niveaux de confidentialité (🔴🟡🟢), plan de sauvegarde, règles agent.
- `JCH_Inbox/04_PILOTAGE_STRATEGIQUE/roadmap-long-terme.md` — **Nouveau (2026-07-16)** — Vision 1 an / 3 ans / 5 ans PKA.
- `JCH_Inbox/04_PILOTAGE_STRATEGIQUE/roadmap-90-jours.md` — Roadmap court terme (juillet→octobre 2026)

## Sécurité

- scripts/pka_security_audit.py — Audit de sécurité du workspace
- scripts/pka_prompt_guard.py — Scanner prompt injection (airlock [[inbox]]) — score 0-100 + quarantaine
- scripts/pka_system_improvement_audit.py — Audit d'amélioration continue
- scripts/rotate_deepseek_key.sh — Rotation clé DeepSeek
- scripts/rotate_gemini_key.sh — Rotation clé Gemini
- scripts/rotate_openrouter_key.sh — Rotation clé OpenRouter
- scripts/rotate_openai_anthropic_keys.sh — Rotation clés OpenAI/Anthropic
- JCH_PRIVATE/decouvertes.env — Secrets isolés du collector Découvertes
- scripts/rpi_security_hardening.sh — Hardening sécurité RPi

## Infrastructure

- scripts/backup_team_db.py — Backup team.db vers TEAM/backups/
- scripts/backup_pka_m1.sh — Backup complet PKA_JCH vers M1
- scripts/backup_vault_to_m1.sh — Backup vault vers M1 (ssh)
- scripts/migration_v4_consolidation.py — Consolidation v4
- scripts/rebuild_file_index.py — Reconstruit l'index des fichiers dans team.db
- bin/sync-to-m1 — Rsync workspace vers M1
- scripts/install_vault_maintenance_launchd.sh — Install cron vault maintenance
- scripts/pka_vault_maintenance.py — **Étendu (2026-07-13)** — Maintenance nocturne 6 étapes : wikilink patcher, file placement checker, git nightly commit, **dedup detector (nouveau)**, **broken link scanner (nouveau)**, **orphan detector (nouveau)**

## Navigation Web (Cloudflare bypass)

> Suite à la session du 2026-06-21 — les outils `fetch_url` et `web.run` sont bloqués par Cloudflare.
> Stack à 2 niveaux : FlareSolverr (proxy anti-Cloudflare, Docker) + Playwright MCP (navigateur complet pilotable).

- **FlareSolverr** (Docker, port 8191) — Proxy anti-Cloudflare JS Challenge. `POST http://localhost:8191/v1`. Usage : curl → FlareSolverr → site protégé.
- **@playwright/mcp** (Node.js, npm global) — Navigateur Chromium headless pilotable via MCP. Contourne Cloudflare + interactions AJAX (dropdowns, formulaires). Configuré dans `~/.deepseek/config.toml`.
- Docker: `docker run -d --name flaresolverr --restart unless-stopped -p 8191:8191 flaresolverr/flaresolverr:latest`
- MCP: `npx -y @playwright/mcp --browser chromium --headless --isolated`
- Brief: `TEAM_Inbox/2026-06-21_dobby_brief-forge_cloudflare-bypass-tools.md`

## IA & LLM

- scripts/deepseek_chat.py — Client DeepSeek API
- scripts/claude_openrouter.py — Appel LLM one-shot via OpenRouter (Claude par défaut, `-m` pour changer)
- scripts/or_route.py — Routeur auto de modèles OpenRouter (type de tâche → modèle)
- scripts/or_image.py — Génération d'image via OpenRouter (Gemini nano-banana, sauvegarde fichier)
- scripts/ollama_chat.py — Client Ollama local (M1)
- scripts/qwen.py — Client Qwen
- scripts/nvidia_chat.py — Client Nvidia API
- scripts/model_client.py — Client modèle unifié
- scripts/provider_balance.py — Équilibrage et monitoring des coûts API
- scripts/model_config.json — Configuration des modèles
- scripts/setup_ollama_m1.sh — Setup et config Ollama sur M1
- scripts/m1_cleanup.sh — Nettoyage modèles Ollama (swap, espace)
- docs/system/[[models-reference]].md — Référence complète des modèles

## [[Dobby]]

- scripts/dobby_retro.py — Rétrospective multi-source
- scripts/dobby_train.py — Pipeline LoRA fine-tuning via MLX (M1)
- scripts/dobby_codex_bridge.py — Pont Codex CLI et [[Dobby]]
- scripts/dobby_weekly_report.py — Rapport hebdomadaire consolidé
- scripts/pka_skill_generator.py — Générateur de skills auto-apprenant (retro_patterns → LLM → [[SKILL]].md)
- scripts/cron-skill-generator.sh — Cron hebdomadaire skill generator (dimanche 22h)
- bin/install-skill-generator-launchd.sh — Installation du launchd skill generator
- scripts/cron-retro-local.sh — Cron rétro quotidienne (M1, 23h)
- bin/install-[[dobby]]-retro.sh — Installation du launchd retro
- bin/[[dobby]] — Commande [[Dobby]]
- bin/[[dobby]].sh — Script [[Dobby]]

## Dashboard

- bin/dashboard.sh — Lance le dashboard
- bin/dashboardctl.sh — Contrôle start/stop/status
- scripts/dashboard_server.py — Serveur Flask du dashboard
- bin/install-dashboard-launchd.sh — Install launchd (auto-start)
- bin/uninstall-dashboard-launchd.sh — Désinstall launchd

## Email

- scripts/[[gmail_gatekeeper]].py — Veille et filtrage Gmail
- scripts/outlook_gatekeeper.py — Veille et filtrage Outlook
- scripts/outlook_auth.py — Auth Outlook (Microsoft Graph)
- scripts/outlook_imap.py — Client IMAP Outlook
- scripts/email_digest.py — Résumé quotidien des emails
- scripts/google_auth.py — Auth Google (OAuth)
- scripts/google_calendar_bridge.py — Pont Agenda Google vers notes
- scripts/install_gmail_gatekeeper_launchd.sh — Install launchd Gmail
- scripts/install_email_pipeline.sh — Install pipeline [[email]] complet

## Fichiers & Inbox

- scripts/generate_tool_pointers.py — Génère les pointers multi-modèles
- scripts/generate_todo.py — Génère todo-jch.html et todo-jch.json
- scripts/migrate_inbox_deliverables.py — Migration format livrables
- scripts/dropbox_watch.py — Veille sur les nouveaux fichiers Dropbox
- scripts/dropbox_watch.sh — Wrapper bash
- scripts/install_dropbox_watch_launchd.sh — Install launchd dropbox
- scripts/migrate_skills_metadata.py — Migration métadonnées skills (legacy)
- scripts/rebuild_file_index.py — Reconstruit l'index des fichiers

## Kanban & Plane

- scripts/pka_kanban_bootstrap.py — Initialisation Kanban
- scripts/pka_kanban_schema.py — Schéma et validation Kanban
- scripts/pka_kanban_service.py — Service Kanban (CRUD)
- scripts/pka_plane_adapter.py — Adaptateur Plane
- scripts/seed_wildnexus_plane.py — Seed WildNexus dans Plane
- scripts/mcp_plane_server.py — Serveur MCP Plane

## Lanceurs

- bin/lancer-claude.command — Lance Claude Code
- bin/lancer-codex.command — Lance Codex CLI
- bin/lancer-deepseek.command — Lance DeepSeek TUI
- bin/lancer-deepseek-r1.command — Lance DeepSeek R1 (14B)
- bin/lancer-gemini.command — Lance Gemini CLI
- bin/lancer-gemma4.command — Lance Gemma 4 (Ollama)
- bin/lancer-qwen3.command — Lance Qwen 3
- bin/lancer-dashboard.command — Lance le dashboard
- bin/activate-ssh — Active SSH (M1, RPi)
- bin/plane-autostart.sh — Autostart Plane

## Skills PKA — Système

- skills/pka-session-start — Protocole démarrage session [[Dobby]] (obligatoire)
- skills/pka-pointer-sync — Synchro pointers multi-modèles
- skills/pka-file-versioning — Backup pré-édition fichiers itératifs
- skills/pka-brand-identity — Charte graphique Arteon, [[WildLens]], L'Instant Lu
- skills/onboarding-specialiste — Pipeline recrutement spécialiste
- skills/wildnexus-governance — Règles architecturales WildNexus P0
- skills/wildnexus-adr — Création/mise à jour ADR WildNexus
- skills/wildnexus-bom — Génération BOM WildNexus Excel
- skills/obsidian-[[knowledge]]-graph — Inventaire, dictionnaire, wikilinks Obsidian
- skills/bioacoustics-qc-playbook — QC bioacoustique, spectrogrammes, tri segments
- skills/system-improvement-ingest — Analyse document → amélioration PKA (grille 6 axes)
- skills/pka-thread-file — Living document par projet (overview/statut/décisions), lecture auto + mise à jour session

## Skills home — Claude Code (~/.claude/skills)

> Emplacement réel : `~/.claude/skills` (home, hors workspace). Skills per-tool chargés par Claude Code.
> ⚠️ `[dup]` = existe aussi dans le workspace (`.agents/skills/` ou `skills/`) — le workspace est la source canonique. À réconcilier (symlink ou purge home).

- brief — Génération de brief structuré [dup: skills/brief]
- capture — Capture connaissance vers team.db [dup: skills/capture]
- code-review-pro — Revue de code [dup: .agents/skills/code-review-pro]
- content-gap-analysis — Gaps éditoriaux [dup]
- content-quality-auditor — Audit E-E-A-T [dup]
- crm-update — Log interaction contact (home only)
- deploy — Checklist mise en production Forge (home only)
- figma-generate-design — Maquettes Figma [dup]
- find-skills — Découverte/install skills [dup]
- graphify — Extraction knowledge graph (home only ; CLI `graphify` aussi dans workspace)
- ingest — Traitement inbox [dup: skills/ingest]
- insecure-defaults — Defaults insecure [dup]
- legal-check — Revue juridique (home only)
- modele — Enrichissement contexte modèle (home only)
- onboarding-specialiste — Recrutement spécialiste [dup: skills/onboarding-specialiste]
- photo-analyse-wildlife — Analyse photo naturaliste (home only) ⚠️ à promouvoir dans le workspace
- pka-file-versioning / pka-pointer-sync / pka-session-start — [dup: skills/]
- seo-content-writer — Rédaction SEO [dup]
- status — Dashboard livrables [dup: skills/status]
- supply-chain-risk-auditor — Audit supply chain [dup]
- triage — Classification mails ambigus (home only)
- wildnexus-adr / wildnexus-bom — [dup: skills/]

## Skills home — DeepSeek CLI (~/.deepseek/skills)

> Emplacement réel : `~/.deepseek/skills`. Skills per-tool chargés par DeepSeek CLI (hors TUI workspace). Aucun doublon avec le workspace.

- delegate — Délégation multi-step via sub-agents
- skill-creator — Création/amélioration de skills
- skill-installer — Installation de skills depuis GitHub
- plugin-creator — Scaffold plugins DeepSeek
- mcp-builder — Construction serveurs MCP (stdio, HTTP/SSE)
- documents — Création/édition DOCX
- spreadsheets — Création/analyse XLSX/CSV
- presentations — Création PPTX
- pdf — Manipulation PDF (split, merge, OCR, watermark)
- feishu — Intégration Feishu/Lark
- v4-best-practices — Bonnes pratiques DeepSeek V4

## Skills Codex (.agents/skills)

- code-review-pro — Revue de code complète
- seo-content-writer — Rédaction SEO
- content-quality-auditor — Audit E-E-A-T (80 items)
- content-gap-analysis — Analyse gaps éditoriaux
- supply-chain-risk-auditor — Audit risques supply chain
- insecure-defaults — Détection defaults insecure
- figma-generate-design — Génération maquettes Figma
- find-skills — Découverte et installation skills

## Projets — WildNexus

- scripts/seed_wildnexus_plane.py — Seed dans Plane
- scripts/ask-gemma-wildnexus-audit.sh — Audit via Gemma 3
- Skills : wildnexus-governance, wildnexus-adr, wildnexus-bom

## Projets — Vetalyx

- scripts/build_vetalyx_rapid_allergy_report.py — Rapport allergie rapide
- Dossiers : strategy/, legal/, regulatory/, clinical/, market/, investors/
- Procédure : `docs/system/procedure-traduction-jade.md` — traduction bilingue Jade (VETALYX/DIAHO)

## MCP Servers (ponts IA ↔ applications)

- lightroom-mcp — `_local/lightroom-mcp/` — Contrôle Lightroom Classic via MCP (plugin Lua + serveur Node). Configuré dans `~/.deepseek/config.toml`.
- photoshop-mcp — `github.com/alisaitteke/photoshop-mcp` — Contrôle Photoshop via MCP (50+ outils). À installer.

## Projets — Photo

- scripts/argus_batch.py — Traitement par lot critiques [[Argus]]
- scripts/argus_progression.py — Suivi progression critiques
- scripts/backfill_exif.py — Remplissage EXIF
- scripts/heron_paper.py — Préparation tirages papier
- scripts/chouette_diagnostic.py — Diagnostic pièges photo
- `05_PHOTO_AI_JURY/mcp_apply_lr.py` — Pont [[Argus]] → Lightroom MCP (mapping 51 clés SDK, commandes prepare/map/sdk-keys)
- Skill : bioacoustics-qc-playbook

## Projets — InsectNet

10 scripts dans scripts/insectnet_*
- audio_inventory, auto_qc, contact_sheets, download_audio
- generate_spectrograms, grouped_split, qc_review_app
- segment_audio, segment_qc, select_audio_candidates, xc_metadata

## Projets — Découvertes

- scripts/decouvertes-collector/collector.py — Bot Telegram collecteur
- scripts/decouvertes-collector/analyzer.py — Analyse lieux + fiches Obsidian

## Projets — Camping / Vanlife

- scripts/camping_scout.py — Scout de campings
- scripts/camping_server.py — Serveur app camping

## Projets — Instincts

- scripts/instinct_search.py — Recherche instincts
- scripts/instinct_promote.py — Promotion instinct vers connaissance
- scripts/instinct_write.py — Écriture instinct
- scripts/instinct_migrate.py — Migration format instincts

## Projets — EventNet

- scripts/eventnet.php — Backend PHP EventNet
- scripts/eventnet_detect.py — Détection événements

## Fichiers de config système

- JCH_Inbox/99_SYSTEM/tool_pointer_config.json — Config pointers
- JCH_Inbox/99_SYSTEM/pka_kanban_schema.json — Schéma Kanban
- JCH_Inbox/99_SYSTEM/pka_kanban_governance.json — Règles Kanban
- JCH_Inbox/99_SYSTEM/pka_plane_config.json — Config Plane
- JCH_Inbox/99_SYSTEM/instinct_promotion_config.json — Config instincts
- JCH_Inbox/99_SYSTEM/context_profiles.json — Profils de contexte
- JCH_Inbox/99_SYSTEM/[[routing_rules]].md — Règles de routage [[inbox]]
- JCH_Inbox/99_SYSTEM/[[diagramming-standard]].md — Standard diagrammes
