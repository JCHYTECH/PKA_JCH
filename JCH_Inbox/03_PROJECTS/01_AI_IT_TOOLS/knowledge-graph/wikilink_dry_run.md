---
date: 2026-05-29
model: GPT-5 Codex
type: wikilink-dry-run
status: proposal
---

# Wikilink Dry Run - 25 files

> Proposal only. No source note has been modified.

- scanned notes: 782
- files with suggestions: 19
- line suggestions: 236

## `JCH_Inbox/03_PROJECTS/01_AI_IT_TOOLS/hermisation/AI_Data_Governance.md`

### Line 102

- terms: Docker
- before:
  `### 5.3 Docker et ports`
- after:
  `### 5.3 [[Docker]] et ports`

### Line 104

- terms: Docker
- before:
  `Docker est autorisé pour les services déjà existants, notamment Plane, mais ne valide pas l'ajout d'une nouvelle stack.`
- after:
  `[[Docker]] est autorisé pour les services déjà existants, notamment Plane, mais ne valide pas l'ajout d'une nouvelle stack.`

### Line 111

- terms: n8n, Qdrant, Redis, PostgreSQL
- before:
  `- aucune nouvelle brique Hermes/n8n/Qdrant/Redis/PostgreSQL hors Plane sans phase technique validée.`
- after:
  `- aucune nouvelle brique Hermes/[[n8n]]/[[Qdrant]]/[[Redis]]/[[PostgreSQL]] hors Plane sans phase technique validée.`

### Line 147

- terms: Docker
- before:
  `- lancement de Docker/stack nouvelle ;`
- after:
  `- lancement de [[Docker]]/stack nouvelle ;`

## `JCH_Inbox/03_PROJECTS/01_AI_IT_TOOLS/hermisation/AI_Runtime_Audit.md`

### Line 52

- terms: Docker
- before:
  `5. Plane tourne via Docker et expose `8088` et `4443` sur toutes les interfaces (`0.0.0.0`), ce qui contredit la préférence sécurité "local-only" sauf validation explicite.`
- after:
  `5. Plane tourne via [[Docker]] et expose `8088` et `4443` sur toutes les interfaces (`0.0.0.0`), ce qui contredit la préférence sécurité "local-only" sauf validation explicite.`

### Line 90

- terms: [[Dobby]]
- before:
  `| 1853 | `telegram-bot/bot.py` | Bot Telegram Dobby | Actif, sensible |`
- after:
  `| 1853 | `telegram-bot/bot.py` | Bot Telegram [[Dobby]] | Actif, sensible |`

### Line 91

- terms: Docker, Docker
- before:
  `| 1299 | Docker Desktop | Support Plane / Docker | Actif |`
- after:
  `| 1299 | [[Docker]] Desktop | Support Plane / [[Docker]] | Actif |`

### Line 103

- terms: Docker
- before:
  `| 8088 | `0.0.0.0` / IPv6 | Plane proxy Docker | À risque si non validé |`
- after:
  `| 8088 | `0.0.0.0` / IPv6 | Plane proxy [[Docker]] | À risque si non validé |`

### Line 104

- terms: Docker
- before:
  `| 4443 | `0.0.0.0` / IPv6 | Plane proxy Docker TLS | À risque si non validé |`
- after:
  `| 4443 | `0.0.0.0` / IPv6 | Plane proxy [[Docker]] TLS | À risque si non validé |`

### Line 111

- terms: Docker
- before:
  `## 5. Docker / Plane`
- after:
  `## 5. [[Docker]] / Plane`

### Line 113

- terms: Docker
- before:
  `Docker est actif. Plane tourne avec les conteneurs suivants :`
- after:
  `[[Docker]] est actif. Plane tourne avec les conteneurs suivants :`

### Line 128

- terms: PostgreSQL, Redis, Docker
- before:
  `Observation importante : Plane utilise déjà PostgreSQL, Redis, MinIO et MQ dans Docker. Cela ne doit pas être confondu avec une validation d'infrastructure Hermes. C'est un runtime existant à gouverner, pas une permission d'ajouter une nouvelle stack.`
- after:
  `Observation importante : Plane utilise déjà [[PostgreSQL]], [[Redis]], MinIO et MQ dans [[Docker]]. Cela ne doit pas être confondu avec une validation d'infrastructure Hermes. C'est un runtime existant à gouverner, pas une permission d'ajouter une nouvelle stack.`

### Line 203

- terms: n8n, Redis, Qdrant
- before:
  `> Ne pas ajouter Hermes, n8n, Redis, Qdrant ou nouvelle orchestration tant que les P0 runtime ne sont pas résolus.`
- after:
  `> Ne pas ajouter Hermes, [[n8n]], [[Redis]], [[Qdrant]] ou nouvelle orchestration tant que les P0 runtime ne sont pas résolus.`

## `JCH_Inbox/03_PROJECTS/01_AI_IT_TOOLS/hermisation/AI_System_Blueprint.md`

### Line 43

- terms: [[Dobby]]
- before:
  `| `ADAPTER-PROMPT.md`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `Codex.md` | Pointeurs runtime et identité Dobby. | Confirmé |`
- after:
  `| `ADAPTER-PROMPT.md`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `Codex.md` | Pointeurs runtime et identité [[Dobby]]. | Confirmé |`

### Line 55

- terms: Python
- before:
  `- des scripts Python et shell ;`
- after:
  `- des scripts [[Python]] et shell ;`

### Line 58

- terms: Tailscale
- before:
  `- des connecteurs externes partiels : Dropbox, Gmail, Outlook, Google Calendar, Plane, Telegram, Tailscale ;`
- after:
  `- des connecteurs externes partiels : Dropbox, Gmail, Outlook, Google Calendar, Plane, Telegram, [[Tailscale]] ;`

### Line 70

- terms: [[Dobby]]
- before:
  `| Spécialistes PKA | 27 rôles experts dans `TEAM/`. | L0-L1, exécutés via Dobby | Confirmé |`
- after:
  `| Spécialistes PKA | 27 rôles experts dans `TEAM/`. | L0-L1, exécutés via [[Dobby]] | Confirmé |`

### Line 71

- terms: Python
- before:
  `| Scripts automatisés | Python/shell sous `scripts/` et `bin/`. | L1-L2 selon script | Confirmé |`
- after:
  `| Scripts automatisés | [[Python]]/shell sous `scripts/` et `bin/`. | L1-L2 selon script | Confirmé |`

### Line 74

- terms: Claude
- before:
  `| Modèles AI | Claude, Ollama, NVIDIA/DeepSeek, OpenAI, Google, autres providers configurés. | Dépend de l'appelant | Confirmé |`
- after:
  `| Modèles AI | [[Claude]], Ollama, NVIDIA/DeepSeek, OpenAI, Google, autres providers configurés. | Dépend de l'appelant | Confirmé |`

### Line 107

- terms: BirdNET
- before:
  `| [[Chouette]] | Terrain, caméras, bioacoustique. | L1 | Élevée pour WILDNEXUS | RPi, BirdNET, terrain, matériel | Confirmé |`
- after:
  `| [[Chouette]] | Terrain, caméras, bioacoustique. | L1 | Élevée pour WILDNEXUS | RPi, [[BirdNET]], terrain, matériel | Confirmé |`

### Line 121

- terms: Claude
- before:
  `| `email_digest.py` | Digest email. | Claude Haiku configuré pour `email_digest` | Emails / configs | Digest/logs | 09:00, 14:00, 20:00 | L2 | Moyenne | Observé, mais MEMORY indique digest suspendu |`
- after:
  `| `email_digest.py` | Digest email. | [[Claude]] Haiku configuré pour `email_digest` | Emails / configs | Digest/logs | 09:00, 14:00, 20:00 | L2 | Moyenne | Observé, mais MEMORY indique digest suspendu |`

### Line 128

- terms: [[Dobby]], Claude, [[Dobby]]
- before:
  `| Telegram bot | Interface Dobby Telegram. | Claude Sonnet configuré pour `telegram_bot` | Telegram, contexte Dobby | Réponses, conversation DB | Potentiellement permanent | L2 | Élevée | Observé |`
- after:
  `| Telegram bot | Interface [[Dobby]] Telegram. | [[Claude]] Sonnet configuré pour `telegram_bot` | Telegram, contexte [[Dobby]] | Réponses, conversation DB | Potentiellement permanent | L2 | Élevée | Observé |`

### Line 145

- terms: Codex
- before:
  `| Codex session courante | OpenAI | GPT-5 | Confirmé par runtime |`
- after:
  `| [[Codex]] session courante | OpenAI | GPT-5 | Confirmé par runtime |`

### Line 172

- terms: Python
- before:
  `| `scripts/__pycache__/` | Cache Python. | Bruit documentaire | Confirmé |`
- after:
  `| `scripts/__pycache__/` | Cache [[Python]]. | Bruit documentaire | Confirmé |`

### Line 210

- terms: [[Dobby]], [[Dobby]]
- before:
  `| Activation Dobby | Lecture mémoire, roster, protocole, inbox. | `MEMORY.md`, `TEAM/`, `wiki/`, inbox | Dobby | Manuel à chaque session | Élevée | Confirmé |`
- after:
  `| Activation [[Dobby]] | Lecture mémoire, roster, protocole, inbox. | `MEMORY.md`, `TEAM/`, `wiki/`, inbox | [[Dobby]] | Manuel à chaque session | Élevée | Confirmé |`

### Line 211

- terms: [[Dobby]], [[Pie]]
- before:
  `| Inbox triage | Lire, loguer, router les fichiers entrants. | `JCH_Inbox/00_INBOX/`, `file_index` | Dobby, Pie, spécialistes | Partiel | Élevée | Confirmé |`
- after:
  `| Inbox triage | Lire, loguer, router les fichiers entrants. | `JCH_Inbox/00_INBOX/`, `file_index` | [[Dobby]], [[Pie]], spécialistes | Partiel | Élevée | Confirmé |`

### Line 212

- terms: [[Dobby]], [[Sybil]]
- before:
  `| Sauvegarde session | Capturer décisions/actions dans Daily/TEAM_Inbox. | `pka_save.py`, `wiki/Daily` | Dobby, Sybil | Manuel interactif | Élevée | Confirmé |`
- after:
  `| Sauvegarde session | Capturer décisions/actions dans Daily/TEAM_Inbox. | `pka_save.py`, `wiki/Daily` | [[Dobby]], [[Sybil]] | Manuel interactif | Élevée | Confirmé |`

### Line 213

- terms: [[Dobby]], [[Castor]], [[Forge]]
- before:
  `| System check | Rapport périodique santé PKA. | Vault, scripts, DB | Dobby/Castor/Forge | launchd | Élevée | Observé |`
- after:
  `| System check | Rapport périodique santé PKA. | Vault, scripts, DB | [[Dobby]]/[[Castor]]/[[Forge]] | launchd | Élevée | Observé |`

### Line 214

- terms: [[Forge]], [[Corbeau]]
- before:
  `| Vault maintenance | Maintenance conventions et placement. | Vault Markdown | Forge/Corbeau | launchd | Élevée | Observé |`
- after:
  `| Vault maintenance | Maintenance conventions et placement. | Vault Markdown | [[Forge]]/[[Corbeau]] | launchd | Élevée | Observé |`

### Line 215

- terms: [[Forge]], [[Vasco]]
- before:
  `| Dropbox VETALYX | Surveiller documents Dropbox. | Dropbox VETALYX | Forge/Vasco | launchd | Élevée | Observé |`
- after:
  `| Dropbox VETALYX | Surveiller documents Dropbox. | Dropbox VETALYX | [[Forge]]/[[Vasco]] | launchd | Élevée | Observé |`

### Line 216

- terms: [[Pie]], [[Dobby]]
- before:
  `| Email gatekeeping | Scan Gmail/Outlook, digest. | Email, configs | Pie/Dobby | launchd | Élevée | Observé |`
- after:
  `| Email gatekeeping | Scan Gmail/Outlook, digest. | Email, configs | [[Pie]]/[[Dobby]] | launchd | Élevée | Observé |`

### Line 217

- terms: [[Forge]], [[Dobby]]
- before:
  `| Dashboards | Hub, organigramme, live dashboard. | `JCH_Inbox/01_DASHBOARDS/` | Forge/Dobby | Serveur local | Moyenne | Confirmé |`
- after:
  `| Dashboards | Hub, organigramme, live dashboard. | `JCH_Inbox/01_DASHBOARDS/` | [[Forge]]/[[Dobby]] | Serveur local | Moyenne | Confirmé |`

### Line 218

- terms: BirdNET, [[Chouette]], [[Clio]], [[Forge]]
- before:
  `| WildNexus bioacoustique | Protocoles RPi/BirdNET, QC audio, terrain. | WILDNEXUS, audio, scripts InsectNet | Chouette, Clio, Forge | Partiel | Élevée | Confirmé |`
- after:
  `| WildNexus bioacoustique | Protocoles RPi/[[BirdNET]], QC audio, terrain. | WILDNEXUS, audio, scripts InsectNet | [[Chouette]], [[Clio]], [[Forge]] | Partiel | Élevée | Confirmé |`

### Line 219

- terms: [[Vasco]], [[Clio]], [[Jade]], [[Renard]]
- before:
  `| VETALYX clinique | Documents techniques, DIXUN, validations. | VETALYX, PDF/DOCX/HTML | Vasco, Clio, Jade, Renard | Partiel | Élevée | Confirmé |`
- after:
  `| VETALYX clinique | Documents techniques, DIXUN, validations. | VETALYX, PDF/DOCX/HTML | [[Vasco]], [[Clio]], [[Jade]], [[Renard]] | Partiel | Élevée | Confirmé |`

### Line 220

- terms: [[Forge]], [[Bruno]], [[Chouette]]
- before:
  `| Procurement/BOM | BOM et paniers composants. | BOM, Digi-Key API | Forge, Bruno, Chouette | Partiel | Moyenne | Confirmé |`
- after:
  `| Procurement/BOM | BOM et paniers composants. | BOM, Digi-Key API | [[Forge]], [[Bruno]], [[Chouette]] | Partiel | Moyenne | Confirmé |`

### Line 241

- terms: Claude, Codex
- before:
  `| AI tools | Claude, Codex, Gemini, DeepSeek, Ollama, NVIDIA. | Modèle utilisé pas toujours tracé. | Confirmé |`
- after:
  `| AI tools | [[Claude]], [[Codex]], Gemini, DeepSeek, Ollama, NVIDIA. | Modèle utilisé pas toujours tracé. | Confirmé |`

### Line 268

- terms: Docker, PostgreSQL, Redis, Qdrant
- before:
  `| Surcomplexification précoce | Élevée | Docker/PostgreSQL/Redis/Qdrant/Hermes avant stabilisation | Freeze technique jusqu'à validation blueprint. |`
- after:
  `| Surcomplexification précoce | Élevée | [[Docker]]/[[PostgreSQL]]/[[Redis]]/[[Qdrant]]/Hermes avant stabilisation | Freeze technique jusqu'à validation blueprint. |`

### Line 287

- terms: [[Dobby]]
- before:
  `- Dobby conversationnel : L1.`
- after:
  `- [[Dobby]] conversationnel : L1.`

### Line 288

- terms: [[Dobby]]
- before:
  `- Dobby avec outils fichier : L1-L2 selon action.`
- after:
  `- [[Dobby]] avec outils fichier : L1-L2 selon action.`

### Line 309

- terms: [[Dobby]]
- before:
  `| Remplacer [[Dobby]] | Rejeté | Dobby reste orchestrateur. |`
- after:
  `| Remplacer [[Dobby]] | Rejeté | [[Dobby]] reste orchestrateur. |`

### Line 314

- terms: Docker, PostgreSQL, Redis, Qdrant, n8n
- before:
  `| Docker/PostgreSQL/Redis/Qdrant/n8n/Hermes | Gelé | Phase technique ultérieure seulement. |`
- after:
  `| [[Docker]]/[[PostgreSQL]]/[[Redis]]/[[Qdrant]]/[[n8n]]/Hermes | Gelé | Phase technique ultérieure seulement. |`

### Line 322

- terms: Docker
- before:
  `- Docker Desktop pour ce projet ;`
- after:
  `- [[Docker]] Desktop pour ce projet ;`

### Line 323

- terms: PostgreSQL
- before:
  `- PostgreSQL ;`
- after:
  `- [[PostgreSQL]] ;`

### Line 324

- terms: Redis
- before:
  `- Redis ;`
- after:
  `- [[Redis]] ;`

### Line 325

- terms: Qdrant
- before:
  `- Qdrant ;`
- after:
  `- [[Qdrant]] ;`

### Line 326

- terms: n8n
- before:
  `- n8n ;`
- after:
  `- [[n8n]] ;`

## `JCH_Inbox/03_PROJECTS/01_AI_IT_TOOLS/hermisation/Inbox_Deliverables_PostMigration_Report.md`

### Line 63

- terms: SQLite
- before:
  `| Intégrité SQLite | `ok` |`
- after:
  `| Intégrité [[SQLite]] | `ok` |`

### Line 81

- terms: [[Vasco]]
- before:
  `| 20 | Vasco | `[EMAIL] Commandé : « Moi, ce que j'aime, c'est... » et 1 articles supplémentaires` | `pending` | 2026-05-01 12:59:28 |  |`
- after:
  `| 20 | [[Vasco]] | `[EMAIL] Commandé : « Moi, ce que j'aime, c'est... » et 1 articles supplémentaires` | `pending` | 2026-05-01 12:59:28 |  |`

### Line 82

- terms: [[Vasco]]
- before:
  `| 83 | Vasco | `[EMAIL] Commandé : « Moi, ce que j'aime, c'est... » et 1 articles supplémentaires` | `pending` | 2026-05-01 13:00:50 |  |`
- after:
  `| 83 | [[Vasco]] | `[EMAIL] Commandé : « Moi, ce que j'aime, c'est... » et 1 articles supplémentaires` | `pending` | 2026-05-01 13:00:50 |  |`

### Line 83

- terms: [[Renard]]
- before:
  `| 128 | Renard | `[EMAIL] Re: contrat type` | `pending` | 2026-05-01 13:02:58 |  |`
- after:
  `| 128 | [[Renard]] | `[EMAIL] Re: contrat type` | `pending` | 2026-05-01 13:02:58 |  |`

### Line 84

- terms: [[Vasco]]
- before:
  `| 147 | Vasco | `[EMAIL] Commandé : « Moi, ce que j'aime, c'est... » et 1 articles supplémentaires` | `pending` | 2026-05-01 13:03:05 |  |`
- after:
  `| 147 | [[Vasco]] | `[EMAIL] Commandé : « Moi, ce que j'aime, c'est... » et 1 articles supplémentaires` | `pending` | 2026-05-01 13:03:05 |  |`

### Line 85

- terms: [[Vasco]]
- before:
  `| 214 | Vasco | `[EMAIL] These are not quizzes. They are diagnostic tools.` | `pending` | 2026-05-02 18:00:14 |  |`
- after:
  `| 214 | [[Vasco]] | `[EMAIL] These are not quizzes. They are diagnostic tools.` | `pending` | 2026-05-02 18:00:14 |  |`

### Line 86

- terms: [[Renard]]
- before:
  `| 228 | Renard | `[EMAIL] Jean-Claude, tatouage Thaïlandais, Tatouage Japonaise et plus d'idées à explorer` | `pending` | 2026-05-09 07:00:19 |  |`
- after:
  `| 228 | [[Renard]] | `[EMAIL] Jean-Claude, tatouage Thaïlandais, Tatouage Japonaise et plus d'idées à explorer` | `pending` | 2026-05-09 07:00:19 |  |`

### Line 87

- terms: [[Chouette]]
- before:
  `| 232 | Chouette | `WildNexus — déterminer longueur d'onde LED IR non visible/non perturbante faune` | `validated` | 2026-05-18 18:52:08 | `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/02_DECISIONS/ADR/[[ADR-002-choix-camera-ir-p0]].md` |`
- after:
  `| 232 | [[Chouette]] | `WildNexus — déterminer longueur d'onde LED IR non visible/non perturbante faune` | `validated` | 2026-05-18 18:52:08 | `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/02_DECISIONS/ADR/[[ADR-002-choix-camera-ir-p0]].md` |`

### Line 88

- terms: [[Forge]]
- before:
  `| 233 | Forge | `WildNexus — revue Meshnology N35 ESP32 LoRa V3/V4` | `delivered` | 2026-05-18 19:53:20 | `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/03_P0_ENGINEERING/[[2026-05-18_product-review-meshnology-n35]].md` |`
- after:
  `| 233 | [[Forge]] | `WildNexus — revue Meshnology N35 ESP32 LoRa V3/V4` | `delivered` | 2026-05-18 19:53:20 | `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/03_P0_ENGINEERING/[[2026-05-18_product-review-meshnology-n35]].md` |`

### Line 89

- terms: [[Milan]]
- before:
  `| 234 | Milan | `WildNexus — scan fabricants produit intégré P0` | `delivered` | 2026-05-18 19:57:03 | `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/03_P0_ENGINEERING/[[2026-05-18_market-scan-integrated-p0-products]].md` |`
- after:
  `| 234 | [[Milan]] | `WildNexus — scan fabricants produit intégré P0` | `delivered` | 2026-05-18 19:57:03 | `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/03_P0_ENGINEERING/[[2026-05-18_market-scan-integrated-p0-products]].md` |`

### Line 91

- terms: [[Dobby]]
- before:
  `## 6. Règle opérationnelle Dobby`
- after:
  `## 6. Règle opérationnelle [[Dobby]]`

### Line 119

- terms: SQLite
- before:
  `Ne pas inclure les backups SQLite.`
- after:
  `Ne pas inclure les backups [[SQLite]].`

## `JCH_Inbox/03_PROJECTS/01_AI_IT_TOOLS/hermisation/Inbox_Deliverables_PreMigration_Audit.md`

### Line 89

- terms: [[Vasco]]
- before:
  `| 20 | Vasco | `[EMAIL] Commandé : « Moi, ce que j'aime, c'est... » et 1 articles supplémentaires` | 2026-05-01 12:59:28 |  |`
- after:
  `| 20 | [[Vasco]] | `[EMAIL] Commandé : « Moi, ce que j'aime, c'est... » et 1 articles supplémentaires` | 2026-05-01 12:59:28 |  |`

### Line 90

- terms: [[Vasco]]
- before:
  `| 83 | Vasco | `[EMAIL] Commandé : « Moi, ce que j'aime, c'est... » et 1 articles supplémentaires` | 2026-05-01 13:00:50 |  |`
- after:
  `| 83 | [[Vasco]] | `[EMAIL] Commandé : « Moi, ce que j'aime, c'est... » et 1 articles supplémentaires` | 2026-05-01 13:00:50 |  |`

### Line 91

- terms: [[Renard]]
- before:
  `| 128 | Renard | `[EMAIL] Re: contrat type` | 2026-05-01 13:02:58 |  |`
- after:
  `| 128 | [[Renard]] | `[EMAIL] Re: contrat type` | 2026-05-01 13:02:58 |  |`

### Line 92

- terms: [[Vasco]]
- before:
  `| 147 | Vasco | `[EMAIL] Commandé : « Moi, ce que j'aime, c'est... » et 1 articles supplémentaires` | 2026-05-01 13:03:05 |  |`
- after:
  `| 147 | [[Vasco]] | `[EMAIL] Commandé : « Moi, ce que j'aime, c'est... » et 1 articles supplémentaires` | 2026-05-01 13:03:05 |  |`

### Line 93

- terms: [[Vasco]]
- before:
  `| 214 | Vasco | `[EMAIL] These are not quizzes. They are diagnostic tools.` | 2026-05-02 18:00:14 |  |`
- after:
  `| 214 | [[Vasco]] | `[EMAIL] These are not quizzes. They are diagnostic tools.` | 2026-05-02 18:00:14 |  |`

### Line 94

- terms: [[Renard]]
- before:
  `| 228 | Renard | `[EMAIL] Jean-Claude, tatouage Thaïlandais, Tatouage Japonaise et plus d'idées à explorer` | 2026-05-09 07:00:19 |  |`
- after:
  `| 228 | [[Renard]] | `[EMAIL] Jean-Claude, tatouage Thaïlandais, Tatouage Japonaise et plus d'idées à explorer` | 2026-05-09 07:00:19 |  |`

### Line 95

- terms: [[Chouette]]
- before:
  `| 232 | Chouette | `WildNexus — déterminer longueur d'onde LED IR non visible/non perturbante faune` | 2026-05-18 18:52:08 | `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/02_DECISIONS/ADR/[[ADR-002-choix-camera-ir-p0]].md` |`
- after:
  `| 232 | [[Chouette]] | `WildNexus — déterminer longueur d'onde LED IR non visible/non perturbante faune` | 2026-05-18 18:52:08 | `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/02_DECISIONS/ADR/[[ADR-002-choix-camera-ir-p0]].md` |`

### Line 96

- terms: [[Forge]]
- before:
  `| 233 | Forge | `WildNexus — revue Meshnology N35 ESP32 LoRa V3/V4` | 2026-05-18 19:53:20 | `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/03_P0_ENGINEERING/[[2026-05-18_product-review-meshnology-n35]].md` |`
- after:
  `| 233 | [[Forge]] | `WildNexus — revue Meshnology N35 ESP32 LoRa V3/V4` | 2026-05-18 19:53:20 | `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/03_P0_ENGINEERING/[[2026-05-18_product-review-meshnology-n35]].md` |`

### Line 97

- terms: [[Milan]]
- before:
  `| 234 | Milan | `WildNexus — scan fabricants produit intégré P0` | 2026-05-18 19:57:03 | `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/03_P0_ENGINEERING/[[2026-05-18_market-scan-integrated-p0-products]].md` |`
- after:
  `| 234 | [[Milan]] | `WildNexus — scan fabricants produit intégré P0` | 2026-05-18 19:57:03 | `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/03_P0_ENGINEERING/[[2026-05-18_market-scan-integrated-p0-products]].md` |`

### Line 125

- terms: SQLite
- before:
  `Un simple `ALTER TABLE ADD COLUMN` ne suffit pas. Pour autoriser les nouveaux statuts, SQLite nécessite une migration contrôlée par reconstruction de table :`
- after:
  `Un simple `ALTER TABLE ADD COLUMN` ne suffit pas. Pour autoriser les nouveaux statuts, [[SQLite]] nécessite une migration contrôlée par reconstruction de table :`

### Line 144

- terms: SQLite
- before:
  `3. accepter une reconstruction SQLite de la table `[[inbox]]`, pas seulement des `ALTER TABLE`;`
- after:
  `3. accepter une reconstruction [[SQLite]] de la table `[[inbox]]`, pas seulement des `ALTER TABLE`;`

## `JCH_Inbox/03_PROJECTS/01_AI_IT_TOOLS/hermisation/Local_Infrastructure_Setup.md`

### Line 30

- terms: Git
- before:
  `| Git | `2.50.1 (Apple Git-155)` | `/usr/bin/git` | ✅ Validé |`
- after:
  `| [[Git]] | `2.50.1 (Apple Git-155)` | `/usr/bin/git` | ✅ Validé |`

### Line 31

- terms: Python
- before:
  `| Python | `3.13.13` | `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3` | ✅ Validé |`
- after:
  `| [[Python]] | `3.13.13` | `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3` | ✅ Validé |`

### Line 33

- terms: Docker
- before:
  `| Docker CLI | `29.4.3` | `/usr/local/bin/docker` | ✅ Validé |`
- after:
  `| [[Docker]] CLI | `29.4.3` | `/usr/local/bin/docker` | ✅ Validé |`

### Line 34

- terms: Docker
- before:
  `| Docker Desktop | — | `/Applications/Docker.app` | ✅ Validé |`
- after:
  `| [[Docker]] Desktop | — | `/Applications/Docker.app` | ✅ Validé |`

### Line 36

- terms: Tailscale
- before:
  `| Tailscale CLI | `1.98.2` | `/usr/local/bin/tailscale` | ✅ Validé (CLI aligné sur app) |`
- after:
  `| [[Tailscale]] CLI | `1.98.2` | `/usr/local/bin/tailscale` | ✅ Validé (CLI aligné sur app) |`

### Line 37

- terms: Tailscale
- before:
  `| Tailscale app | — | `/Applications/Tailscale.app` | ✅ Validé |`
- after:
  `| [[Tailscale]] app | — | `/Applications/Tailscale.app` | ✅ Validé |`

### Line 43

- terms: Tailscale
- before:
  `## 2. Réseau Tailscale`
- after:
  `## 2. Réseau [[Tailscale]]`

### Line 45

- terms: Tailscale
- before:
  `| Nœud | IP Tailscale | IP locale |`
- after:
  `| Nœud | IP [[Tailscale]] | IP locale |`

### Line 62

- terms: Docker
- before:
  `## 3. Docker — conteneurs actifs`
- after:
  `## 3. [[Docker]] — conteneurs actifs`

### Line 67

- terms: Redis
- before:
  `| Plane API / web / workers / db / redis / mq / minio | internes | Acceptés comme runtime existant |`
- after:
  `| Plane API / web / workers / db / [[Redis]] / mq / minio | internes | Acceptés comme runtime existant |`

### Line 69

- terms: PostgreSQL, Redis
- before:
  `**Règle ferme :** les composants internes de Plane (PostgreSQL, Redis) ne doivent pas être réutilisés comme socle Hermes. Toute Phase 4 déploiera ses propres conteneurs isolés.`
- after:
  `**Règle ferme :** les composants internes de Plane ([[PostgreSQL]], [[Redis]]) ne doivent pas être réutilisés comme socle Hermes. Toute Phase 4 déploiera ses propres conteneurs isolés.`

### Line 110

- terms: [[Dobby]]
- before:
  `| Bot Telegram Dobby | — |`
- after:
  `| Bot Telegram [[Dobby]] | — |`

### Line 114

- terms: [[Sybil]]
- before:
  `| Cron backup / Sybil / rétro / weekly | — |`
- after:
  `| Cron backup / [[Sybil]] / rétro / weekly | — |`

### Line 129

- terms: PostgreSQL, Redis, Qdrant, n8n
- before:
  `3. Aucune installation de PostgreSQL, Redis, Qdrant, n8n, ni agent persistant nouveau en dehors de la Phase 4 définie.`
- after:
  `3. Aucune installation de [[PostgreSQL]], [[Redis]], [[Qdrant]], [[n8n]], ni agent persistant nouveau en dehors de la Phase 4 définie.`

## `JCH_Inbox/03_PROJECTS/01_AI_IT_TOOLS/hermisation/Persistent_Memory_Architecture.md`

### Line 23

- terms: PostgreSQL, Redis, Qdrant
- before:
  `Il évalue PostgreSQL, Redis et Qdrant au regard des besoins réels du système PKA_JCH, et définit l'architecture de mémoire à adopter.`
- after:
  `Il évalue [[PostgreSQL]], [[Redis]] et [[Qdrant]] au regard des besoins réels du système PKA_JCH, et définit l'architecture de mémoire à adopter.`

### Line 36

- terms: SQLite
- before:
  `| Mémoire relationnelle | `TEAM/team.db` (SQLite) | Actif — source de vérité |`
- after:
  `| Mémoire relationnelle | `TEAM/team.db` ([[SQLite]]) | Actif — source de vérité |`

### Line 56

- terms: PostgreSQL
- before:
  `### 2.1 PostgreSQL`
- after:
  `### 2.1 [[PostgreSQL]]`

### Line 61

- terms: SQLite
- before:
  `- `TEAM/team.db` (SQLite) couvre l'intégralité des besoins relationnels actuels.`
- after:
  `- `TEAM/team.db` ([[SQLite]]) couvre l'intégralité des besoins relationnels actuels.`

### Line 63

- terms: PostgreSQL, Docker
- before:
  `- Plane dispose déjà de son propre PostgreSQL interne Docker — à ne pas réutiliser (règle Phase 1).`
- after:
  `- Plane dispose déjà de son propre [[PostgreSQL]] interne [[Docker]] — à ne pas réutiliser (règle Phase 1).`

### Line 67

- terms: SQLite, PostgreSQL, Docker
- before:
  `SQLite est suffisant pour la taille et l'usage actuel. PostgreSQL n'apporterait aucun bénéfice concret et ajouterait un conteneur Docker supplémentaire à maintenir.`
- after:
  `[[SQLite]] est suffisant pour la taille et l'usage actuel. [[PostgreSQL]] n'apporterait aucun bénéfice concret et ajouterait un conteneur [[Docker]] supplémentaire à maintenir.`

### Line 71

- terms: Redis
- before:
  `### 2.2 Redis`
- after:
  `### 2.2 [[Redis]]`

### Line 78

- terms: Redis, Docker
- before:
  `- Plane dispose déjà de son propre Redis interne Docker — à ne pas réutiliser.`
- after:
  `- Plane dispose déjà de son propre [[Redis]] interne [[Docker]] — à ne pas réutiliser.`

### Line 79

- terms: Redis
- before:
  `- Le problème que Redis résoudrait n'existe pas encore dans PKA.`
- after:
  `- Le problème que [[Redis]] résoudrait n'existe pas encore dans PKA.`

### Line 87

- terms: Qdrant
- before:
  `### 2.3 Qdrant (base vectorielle)`
- after:
  `### 2.3 [[Qdrant]] (base vectorielle)`

### Line 94

- terms: Qdrant, Docker
- before:
  `- Qdrant existe en version légère mono-conteneur Docker.`
- after:
  `- [[Qdrant]] existe en version légère mono-conteneur [[Docker]].`

### Line 99

- terms: Qdrant, SQLite
- before:
  `Qdrant devient justifié quand `[[knowledge]]` dépasse 100 entrées **et** qu'une requête sémantique concrète ne peut pas être satisfaite par SQLite `LIKE` ou `FTS5`. Déclencher l'évaluation à ce seuil.`
- after:
  `[[Qdrant]] devient justifié quand `[[knowledge]]` dépasse 100 entrées **et** qu'une requête sémantique concrète ne peut pas être satisfaite par [[SQLite]] `LIKE` ou `FTS5`. Déclencher l'évaluation à ce seuil.`

### Line 109

- terms: SQLite
- before:
  `La mémoire persistante de PKA repose déjà sur SQLite + fichiers Markdown. Le travail de Phase 4a consiste à **alimenter systématiquement les tables existantes** et à **rendre la mémoire procédurale active**.`
- after:
  `La mémoire persistante de PKA repose déjà sur [[SQLite]] + fichiers Markdown. Le travail de Phase 4a consiste à **alimenter systématiquement les tables existantes** et à **rendre la mémoire procédurale active**.`

### Line 125

- terms: Qdrant
- before:
  `| `[[knowledge]]` ≥ 100 entrées | Évaluer Qdrant light |`
- after:
  `| `[[knowledge]]` ≥ 100 entrées | Évaluer [[Qdrant]] light |`

### Line 131

- terms: Qdrant
- before:
  `## 4. Architecture Phase 4b (conditionnelle — Qdrant)`
- after:
  `## 4. Architecture Phase 4b (conditionnelle — [[Qdrant]])`

### Line 139

- terms: Qdrant, Docker
- before:
  `| Qdrant light | Stockage et recherche vectorielle sur `[[knowledge]]` | 1 conteneur Docker isolé, port `127.0.0.1:6333` |`
- after:
  `| [[Qdrant]] light | Stockage et recherche vectorielle sur `[[knowledge]]` | 1 conteneur [[Docker]] isolé, port `127.0.0.1:6333` |`

### Line 141

- terms: SQLite, Qdrant, Python
- before:
  `| Script d'indexation | Lit `[[knowledge]]` depuis SQLite, envoie embeddings à Qdrant | Python, [[Forge]] |`
- after:
  `| Script d'indexation | Lit `[[knowledge]]` depuis [[SQLite]], envoie embeddings à [[Qdrant]] | [[Python]], [[Forge]] |`

### Line 145

- terms: Qdrant
- before:
  `- Qdrant est **read-only depuis les agents** — seul le script d'indexation écrit.`
- after:
  `- [[Qdrant]] est **read-only depuis les agents** — seul le script d'indexation écrit.`

### Line 146

- terms: Qdrant
- before:
  `- `TEAM/team.db` reste la source de vérité — Qdrant est un index dérivé, reconstituable.`
- after:
  `- `TEAM/team.db` reste la source de vérité — [[Qdrant]] est un index dérivé, reconstituable.`

### Line 155

- terms: n8n
- before:
  `- Elle ne relie pas Hermes, n8n ou tout framework d'orchestration externe.`
- after:
  `- Elle ne relie pas Hermes, [[n8n]] ou tout framework d'orchestration externe.`

## `JCH_Inbox/03_PROJECTS/01_AI_IT_TOOLS/hermisation/Phase_1_Closure_Report.md`

### Line 25

- terms: n8n, Qdrant, Redis, PostgreSQL
- before:
  `> Ne pas ajouter d'infrastructure Hermes, n8n, Qdrant, Redis, PostgreSQL ou agents persistants avant validation explicite de la Phase technique minimale.`
- after:
  `> Ne pas ajouter d'infrastructure Hermes, [[n8n]], [[Qdrant]], [[Redis]], [[PostgreSQL]] ou agents persistants avant validation explicite de la Phase technique minimale.`

### Line 41

- terms: Codex, Claude
- before:
  `| Runtimes AI | Codex/GPT-5, Claude, Ollama, NVIDIA/DeepSeek, OpenAI, Google et autres providers configurés. |`
- after:
  `| Runtimes AI | [[Codex]]/GPT-5, [[Claude]], Ollama, NVIDIA/DeepSeek, OpenAI, Google et autres providers configurés. |`

### Line 44

- terms: Docker
- before:
  `| Services | LaunchAgents, cron, Docker/Plane, Ollama, Dropbox client. |`
- after:
  `| Services | LaunchAgents, cron, [[Docker]]/Plane, Ollama, Dropbox client. |`

### Line 57

- terms: Docker
- before:
  `| Plane proxy | Ports Docker restreints à `127.0.0.1`; `plane.env` passé en `0600`. | Plane local-only sur `8088` et `4443`. |`
- after:
  `| Plane proxy | Ports [[Docker]] restreints à `127.0.0.1`; `plane.env` passé en `0600`. | Plane local-only sur `8088` et `4443`. |`

### Line 71

- terms: [[Sybil]]
- before:
  `| Cron backup/Sybil/retro/weekly | Actifs. |`
- after:
  `| Cron backup/[[Sybil]]/retro/weekly | Actifs. |`

### Line 104

- terms: PostgreSQL, Redis
- before:
  `| Plane stack complexe | Moyenne | Acceptée comme runtime existant; pas de réutilisation PostgreSQL/Redis pour Hermes. |`
- after:
  `| Plane stack complexe | Moyenne | Acceptée comme runtime existant; pas de réutilisation [[PostgreSQL]]/[[Redis]] pour Hermes. |`

### Line 114

- terms: Qdrant, Redis, PostgreSQL
- before:
  `3. Aucun Qdrant, Redis, PostgreSQL additionnel.`
- after:
  `3. Aucun [[Qdrant]], [[Redis]], [[PostgreSQL]] additionnel.`

### Line 115

- terms: n8n
- before:
  `4. Aucun n8n.`
- after:
  `4. Aucun [[n8n]].`

### Line 117

- terms: Git, Python, Docker, Tailscale
- before:
  `6. Vérifier seulement l'existant : Git, Python, Docker Desktop, VS Code, Tailscale, backups.`
- after:
  `6. Vérifier seulement l'existant : [[Git]], [[Python]], [[Docker]] Desktop, VS Code, [[Tailscale]], backups.`

## `JCH_Inbox/03_PROJECTS/01_AI_IT_TOOLS/hermisation/Phase_Tech_Minimal_Backup_Audit.md`

### Line 12

- terms: Obsidian
- before:
  `- pas de modification Obsidian ;`
- after:
  `- pas de modification [[Obsidian]] ;`

### Line 54

- terms: SQLite
- before:
  `- backup via SQLite Online Backup API ;`
- after:
  `- backup via [[SQLite]] Online Backup API ;`

### Line 75

- terms: SQLite
- before:
  `- tables SQLite lisibles.`
- after:
  `- tables [[SQLite]] lisibles.`

### Line 94

- terms: [[Dobby]]
- before:
  `| Writers concurrents pendant restauration | Élevée | Arrêter ou suspendre Dobby/scripts avant restauration réelle. |`
- after:
  `| Writers concurrents pendant restauration | Élevée | Arrêter ou suspendre [[Dobby]]/scripts avant restauration réelle. |`

## `JCH_Inbox/03_PROJECTS/01_AI_IT_TOOLS/hermisation/Phase_Tech_Minimal_MacBook_Audit.md`

### Line 4

- terms: Tailscale
- before:
  `Statut : socle présent ; Tailscale corrigé ; étape backup validée séparément`
- after:
  `Statut : socle présent ; [[Tailscale]] corrigé ; étape backup validée séparément`

### Line 12

- terms: Git
- before:
  `- Git : OK.`
- after:
  `- [[Git]] : OK.`

### Line 13

- terms: Python
- before:
  `- Python : OK.`
- after:
  `- [[Python]] : OK.`

### Line 14

- terms: Docker
- before:
  `- Docker Desktop : OK.`
- after:
  `- [[Docker]] Desktop : OK.`

### Line 16

- terms: Tailscale, Tailscale
- before:
  `- Tailscale : OK après réalignement du CLI sur Tailscale.app.`
- after:
  `- [[Tailscale]] : OK après réalignement du CLI sur [[Tailscale]].app.`

### Line 19

- terms: n8n, Qdrant, Redis, PostgreSQL
- before:
  `Cette étape ne déclenche aucune installation lourde et ne débloque pas encore Hermes, n8n, Qdrant, Redis, PostgreSQL ou agents persistants.`
- after:
  `Cette étape ne déclenche aucune installation lourde et ne débloque pas encore Hermes, [[n8n]], [[Qdrant]], [[Redis]], [[PostgreSQL]] ou agents persistants.`

### Line 25

- terms: Git
- before:
  `| Git | OK | `git version 2.50.1 (Apple Git-155)` ; `/usr/bin/git` | Socle valide |`
- after:
  `| [[Git]] | OK | `git version 2.50.1 (Apple Git-155)` ; `/usr/bin/git` | Socle valide |`

### Line 26

- terms: Python
- before:
  `| Python | OK | `Python 3.13.13` ; `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3` | Socle valide |`
- after:
  `| [[Python]] | OK | `Python 3.13.13` ; `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3` | Socle valide |`

### Line 27

- terms: Python
- before:
  `| pip | OK | `pip 26.1.1` pour Python 3.13 | Socle valide |`
- after:
  `| pip | OK | `pip 26.1.1` pour [[Python]] 3.13 | Socle valide |`

### Line 28

- terms: Docker
- before:
  `| Docker CLI | OK | `Docker version 29.4.3` ; `/usr/local/bin/docker` | Socle valide |`
- after:
  `| [[Docker]] CLI | OK | `Docker version 29.4.3` ; `/usr/local/bin/docker` | Socle valide |`

### Line 29

- terms: Docker
- before:
  `| Docker Desktop | OK | `/Applications/Docker.app` présent ; daemon `Docker Desktop aarch64` | Socle valide |`
- after:
  `| [[Docker]] Desktop | OK | `/Applications/Docker.app` présent ; daemon `Docker Desktop aarch64` | Socle valide |`

### Line 31

- terms: Tailscale
- before:
  `| Tailscale CLI | OK | `1.98.2` ; `/usr/local/bin/tailscale` | Socle valide |`
- after:
  `| [[Tailscale]] CLI | OK | `1.98.2` ; `/usr/local/bin/tailscale` | Socle valide |`

### Line 32

- terms: Tailscale
- before:
  `| Tailscale app | OK | `/Applications/Tailscale.app` | App lancée, CLI aligné |`
- after:
  `| [[Tailscale]] app | OK | `/Applications/Tailscale.app` | App lancée, CLI aligné |`

### Line 34

- terms: Docker
- before:
  `## 3. Docker`
- after:
  `## 3. [[Docker]]`

### Line 36

- terms: Docker
- before:
  `Docker Desktop est fonctionnel.`
- after:
  `[[Docker]] Desktop est fonctionnel.`

### Line 49

- terms: Redis
- before:
  `| Plane API / web / workers / db / redis / mq / minio | Actifs dans le runtime Plane existant |`
- after:
  `| Plane API / web / workers / db / [[Redis]] / mq / minio | Actifs dans le runtime Plane existant |`

### Line 57

- terms: Tailscale
- before:
  `## 4. Tailscale`
- after:
  `## 4. [[Tailscale]]`

### Line 67

- terms: Tailscale
- before:
  `- l'application Tailscale est installée ;`
- after:
  `- l'application [[Tailscale]] est installée ;`

### Line 68

- terms: Tailscale
- before:
  `- un processus Tailscale est visible ;`
- after:
  `- un processus [[Tailscale]] est visible ;`

### Line 77

- terms: Tailscale
- before:
  `- version CLI alignée avec Tailscale.app : `1.98.2`.`
- after:
  `- version CLI alignée avec [[Tailscale]].app : `1.98.2`.`

### Line 101

- terms: Git
- before:
  `| Racine Git | `/Users/jchavauxm5/PKA_JCH` |`
- after:
  `| Racine [[Git]] | `/Users/jchavauxm5/PKA_JCH` |`

### Line 127

- terms: Tailscale
- before:
  `- Tailscale est fiable côté CLI pour l'administration distante et les tests RPI.`
- after:
  `- [[Tailscale]] est fiable côté CLI pour l'administration distante et les tests RPI.`

## `JCH_Inbox/03_PROJECTS/01_AI_IT_TOOLS/hermisation/RUNBOOK_PKA_MACBOOK.md`

### Line 25

- terms: n8n
- before:
  `- n8n ;`
- after:
  `- [[n8n]] ;`

### Line 26

- terms: Qdrant
- before:
  `- Qdrant ;`
- after:
  `- [[Qdrant]] ;`

### Line 27

- terms: Redis, PostgreSQL
- before:
  `- Redis ou PostgreSQL hors stack Plane existante ;`
- after:
  `- [[Redis]] ou [[PostgreSQL]] hors stack Plane existante ;`

### Line 35

- terms: Obsidian
- before:
  `- changements Obsidian non liés ;`
- after:
  `- changements [[Obsidian]] non liés ;`

### Line 38

- terms: SQLite
- before:
  `- backups SQLite.`
- after:
  `- backups [[SQLite]].`

### Line 58

- terms: Tailscale
- before:
  `Tailscale, si le daemon répond :`
- after:
  `[[Tailscale]], si le daemon répond :`

### Line 74

- terms: Docker
- before:
  `Docker / Plane :`
- after:
  `[[Docker]] / Plane :`

### Line 98

- terms: Git
- before:
  `| Git | installé |`
- after:
  `| [[Git]] | installé |`

### Line 99

- terms: Python
- before:
  `| Python | 3.13.x |`
- after:
  `| [[Python]] | 3.13.x |`

### Line 101

- terms: Docker
- before:
  `| Docker Desktop | installé, daemon actif |`
- after:
  `| [[Docker]] Desktop | installé, daemon actif |`

### Line 103

- terms: Tailscale
- before:
  `| Tailscale | installé ; CLI `/usr/local/bin/tailscale` version `1.98.2` ; IP MacBook `100.108.55.44` |`
- after:
  `| [[Tailscale]] | installé ; CLI `/usr/local/bin/tailscale` version `1.98.2` ; IP MacBook `100.108.55.44` |`

### Line 111

- terms: [[Dobby]]
- before:
  `| `com.pka.[[dobby]]` | Bot Telegram Dobby | RunAtLoad + KeepAlive | `scripts/telegram-bot/[[dobby]].log` |`
- after:
  `| `com.pka.[[dobby]]` | Bot Telegram [[Dobby]] | RunAtLoad + KeepAlive | `scripts/telegram-bot/[[dobby]].log` |`

### Line 127

- terms: archive
- before:
  `Archive :`
- after:
  `[[archive]] :`

### Line 138

- terms: [[Sybil]]
- before:
  `| 22:00 quotidien | `scripts/sybil_journal.py` | journal Sybil |`
- after:
  `| 22:00 quotidien | `scripts/sybil_journal.py` | journal [[Sybil]] |`

### Line 139

- terms: [[Dobby]]
- before:
  `| 23:00 quotidien | `scripts/dobby_retro.py` | rétrospective Dobby |`
- after:
  `| 23:00 quotidien | `scripts/dobby_retro.py` | rétrospective [[Dobby]] |`

### Line 144

- terms: [[Dobby]]
- before:
  `## 8. Dobby Telegram`
- after:
  `## 8. [[Dobby]] Telegram`

### Line 150

- terms: Python
- before:
  `- Python : `scripts/telegram-bot/venv/bin/python3``
- after:
  `- [[Python]] : `scripts/telegram-bot/venv/bin/python3``

### Line 231

- terms: Redis, PostgreSQL
- before:
  `Plane est un runtime existant. Ses Redis/PostgreSQL internes ne sont pas un socle pour Hermes.`
- after:
  `Plane est un runtime existant. Ses [[Redis]]/[[PostgreSQL]] internes ne sont pas un socle pour Hermes.`

### Line 297

- terms: Tailscale
- before:
  `## 15. Tailscale`
- after:
  `## 15. [[Tailscale]]`

### Line 315

- terms: Tailscale
- before:
  `- éviter un mismatch entre le CLI Homebrew et le daemon fourni par Tailscale.app ;`
- after:
  `- éviter un mismatch entre le CLI Homebrew et le daemon fourni par [[Tailscale]].app ;`

### Line 316

- terms: Tailscale
- before:
  `- faire pointer `tailscale` vers le wrapper installé par Tailscale.app.`
- after:
  `- faire pointer `tailscale` vers le wrapper installé par [[Tailscale]].app.`

## `JCH_Inbox/03_PROJECTS/01_AI_IT_TOOLS/hermisation/Runtime_Service_Register.md`

### Line 35

- terms: Docker, Docker
- before:
  `| `com.jchytech.pka-plane-autostart` | `bin/plane-autostart.sh` | [[Forge]] | 300 s + RunAtLoad | Activé | Docker, Plane compose | `tmp/plane-autostart.log` | Docker local; ports restreints à loopback | `launchctl bootout gui/501/com.jchytech.pka-plane-autostart` |`
- after:
  `| `com.jchytech.pka-plane-autostart` | `bin/plane-autostart.sh` | [[Forge]] | 300 s + RunAtLoad | Activé | [[Docker]], Plane compose | `tmp/plane-autostart.log` | [[Docker]] local; ports restreints à loopback | `launchctl bootout gui/501/com.jchytech.pka-plane-autostart` |`

### Line 51

- terms: Docker
- before:
  `## Docker / Plane`
- after:
  `## [[Docker]] / Plane`

### Line 55

- terms: Docker
- before:
  `| Plane stack Docker | Actif observé 2026-05-28 | `127.0.0.1:8088`, `127.0.0.1:4443` | [[Forge]] | Local-only après remédiation | Maintenir binding loopback; validation JCH requise pour LAN. |`
- after:
  `| Plane stack [[Docker]] | Actif observé 2026-05-28 | `127.0.0.1:8088`, `127.0.0.1:4443` | [[Forge]] | Local-only après remédiation | Maintenir binding loopback; validation JCH requise pour LAN. |`

### Line 56

- terms: PostgreSQL, Docker, Docker
- before:
  `| Plane PostgreSQL interne | Actif dans Docker | interne Docker `5432` | [[Forge]] | Ne pas confondre avec DB PKA | Garder séparé de `TEAM/team.db`. |`
- after:
  `| Plane [[PostgreSQL]] interne | Actif dans [[Docker]] | interne [[Docker]] `5432` | [[Forge]] | Ne pas confondre avec DB PKA | Garder séparé de `TEAM/team.db`. |`

### Line 57

- terms: Redis, Docker, Docker, Redis
- before:
  `| Plane Redis interne | Actif dans Docker | interne Docker `6379` | [[Forge]] | Ne valide pas Redis pour Hermes | Pas de réutilisation sans phase technique. |`
- after:
  `| Plane [[Redis]] interne | Actif dans [[Docker]] | interne [[Docker]] `6379` | [[Forge]] | Ne valide pas [[Redis]] pour Hermes | Pas de réutilisation sans phase technique. |`

### Line 58

- terms: Docker, Docker
- before:
  `| Plane MinIO/MQ internes | Actifs dans Docker | internes Docker | [[Forge]] | Stack déjà complexe | Documenter sauvegarde/rollback Plane. |`
- after:
  `| Plane MinIO/MQ internes | Actifs dans [[Docker]] | internes [[Docker]] | [[Forge]] | Stack déjà complexe | Documenter sauvegarde/rollback Plane. |`

### Line 78

- terms: Docker
- before:
  `| 2026-05-28 | Plane proxy | Ajout de `host_ip: 127.0.0.1` sur les ports 80/443 publiés dans `_local/plane-community/plane-app/docker-compose.yaml`; recréation du proxy via Docker Compose; permission `0600` sur `plane.env`. | `docker ps` confirme `127.0.0.1:8088->80/tcp` et `127.0.0.1:4443->443/tcp`; `lsof` confirme loopback; `curl http://127.0.0.1:8088/` retourne `200`. |`
- after:
  `| 2026-05-28 | Plane proxy | Ajout de `host_ip: 127.0.0.1` sur les ports 80/443 publiés dans `_local/plane-community/plane-app/docker-compose.yaml`; recréation du proxy via [[Docker]] Compose; permission `0600` sur `plane.env`. | `docker ps` confirme `127.0.0.1:8088->80/tcp` et `127.0.0.1:4443->443/tcp`; `lsof` confirme loopback; `curl http://127.0.0.1:8088/` retourne `200`. |`

## `JCH_Inbox/03_PROJECTS/01_AI_IT_TOOLS/hermisation/System_Architecture_Report.md`

### Line 29

- terms: Git
- before:
  `| Git | `2.50.1` | ✅ |`
- after:
  `| [[Git]] | `2.50.1` | ✅ |`

### Line 30

- terms: Python
- before:
  `| Python | `3.13.13` | ✅ |`
- after:
  `| [[Python]] | `3.13.13` | ✅ |`

### Line 31

- terms: Docker
- before:
  `| Docker Desktop | `29.4.3` | ✅ |`
- after:
  `| [[Docker]] Desktop | `29.4.3` | ✅ |`

### Line 33

- terms: Tailscale
- before:
  `| Tailscale | `1.98.2` | ✅ |`
- after:
  `| [[Tailscale]] | `1.98.2` | ✅ |`

### Line 44

- terms: PostgreSQL, SQLite
- before:
  `| PostgreSQL | ❌ Non déployé — SQLite suffisant | Jamais pour PKA mono-user |`
- after:
  `| [[PostgreSQL]] | ❌ Non déployé — [[SQLite]] suffisant | Jamais pour PKA mono-user |`

### Line 45

- terms: Redis
- before:
  `| Redis | ❌ Non déployé — pas d'agents concurrents | Si agents persistants multiples (Phase 6+) |`
- after:
  `| [[Redis]] | ❌ Non déployé — pas d'agents concurrents | Si agents persistants multiples (Phase 6+) |`

### Line 46

- terms: Qdrant
- before:
  `| Qdrant | 🟡 Différé | `[[knowledge]]` ≥ 100 entrées + besoin sémantique concret |`
- after:
  `| [[Qdrant]] | 🟡 Différé | `[[knowledge]]` ≥ 100 entrées + besoin sémantique concret |`

### Line 47

- terms: n8n
- before:
  `| n8n | 🟡 Différé | Workflow ≥3 services externes avec logique conditionnelle |`
- after:
  `| [[n8n]] | 🟡 Différé | Workflow ≥3 services externes avec logique conditionnelle |`

### Line 54

- terms: Docker
- before:
  `## 3. Conteneurs Docker actifs`
- after:
  `## 3. Conteneurs [[Docker]] actifs`

### Line 61

- terms: PostgreSQL, Redis
- before:
  `Règle ferme : les PostgreSQL et Redis internes de Plane ne servent pas de socle Hermes.`
- after:
  `Règle ferme : les [[PostgreSQL]] et [[Redis]] internes de Plane ne servent pas de socle Hermes.`

### Line 126

- terms: SQLite
- before:
  `| `TEAM/team.db` | Backup SQLite quotidien 08h00 via cron → `TEAM/backups/team_YYYY-MM-DD_HHMM.db` |`
- after:
  `| `TEAM/team.db` | Backup [[SQLite]] quotidien 08h00 via cron → `TEAM/backups/team_YYYY-MM-DD_HHMM.db` |`

## `JCH_Inbox/03_PROJECTS/01_AI_IT_TOOLS/hermisation/Workflow_Orchestration.md`

### Line 23

- terms: n8n
- before:
  `Il évalue n8n, les queues et les outils de monitoring au regard des workflows réels du système PKA_JCH, et définit l'architecture d'orchestration à adopter.`
- after:
  `Il évalue [[n8n]], les queues et les outils de monitoring au regard des workflows réels du système PKA_JCH, et définit l'architecture d'orchestration à adopter.`

### Line 36

- terms: [[Sybil]]
- before:
  `| Journal Sybil | Cron 22h00 quotidien | `scripts/sybil_journal.py` | ✅ Actif |`
- after:
  `| Journal [[Sybil]] | Cron 22h00 quotidien | `scripts/sybil_journal.py` | ✅ Actif |`

### Line 37

- terms: [[Dobby]]
- before:
  `| Rétro Dobby | Cron 23h00 quotidien | `scripts/dobby_retro.py` | ✅ Actif |`
- after:
  `| Rétro [[Dobby]] | Cron 23h00 quotidien | `scripts/dobby_retro.py` | ✅ Actif |`

### Line 41

- terms: [[Dobby]]
- before:
  `| Bot Telegram Dobby | LaunchAgent (PID 5377) | `scripts/telegram-bot/bot.py` | ✅ Actif |`
- after:
  `| Bot Telegram [[Dobby]] | LaunchAgent (PID 5377) | `scripts/telegram-bot/bot.py` | ✅ Actif |`

### Line 58

- terms: [[Trace]]
- before:
  `3. **Aucune alerte en cas d'échec silencieux** — un cron qui échoue laisse une trace dans son log mais personne ne le lit.`
- after:
  `3. **Aucune alerte en cas d'échec silencieux** — un cron qui échoue laisse une [[Trace]] dans son log mais personne ne le lit.`

### Line 59

- terms: [[Dobby]]
- before:
  `4. **Workflows manuels non tracés** — les tâches Dobby (briefs, analyses, livrables) ne sont pas comptabilisées comme des exécutions d'orchestration.`
- after:
  `4. **Workflows manuels non tracés** — les tâches [[Dobby]] (briefs, analyses, livrables) ne sont pas comptabilisées comme des exécutions d'orchestration.`

### Line 65

- terms: n8n
- before:
  `### 2.1 n8n`
- after:
  `### 2.1 [[n8n]]`

### Line 70

- terms: Python
- before:
  `- Les workflows actuels sont des scripts Python autonomes, tous mono-service.`
- after:
  `- Les workflows actuels sont des scripts [[Python]] autonomes, tous mono-service.`

### Line 72

- terms: n8n, Docker
- before:
  `- n8n nécessite un conteneur Docker supplémentaire + base de données persistante propre.`
- after:
  `- [[n8n]] nécessite un conteneur [[Docker]] supplémentaire + base de données persistante propre.`

### Line 73

- terms: n8n, Python
- before:
  `- La valeur de n8n apparaît quand : (a) un workflow relie ≥3 services externes, (b) un utilisateur non-développeur doit modifier les conditions, (c) les scripts Python deviennent trop nombreux à maintenir.`
- after:
  `- La valeur de [[n8n]] apparaît quand : (a) un workflow relie ≥3 services externes, (b) un utilisateur non-développeur doit modifier les conditions, (c) les scripts [[Python]] deviennent trop nombreux à maintenir.`

### Line 77

- terms: n8n, Python
- before:
  `n8n devient justifié si un workflow doit relier Gmail + Telegram + team.db + Plane avec logique conditionnelle et sans développement Python. Aucun workflow actuel ne remplit ces critères.`
- after:
  `[[n8n]] devient justifié si un workflow doit relier Gmail + Telegram + team.db + Plane avec logique conditionnelle et sans développement [[Python]]. Aucun workflow actuel ne remplit ces critères.`

### Line 81

- terms: Redis
- before:
  `### 2.2 Queues (RabbitMQ, Redis Streams…)`
- after:
  `### 2.2 Queues (RabbitMQ, [[Redis]] Streams…)`

### Line 123

- terms: [[Sybil]]
- before:
  `| Ajouter un appel `memory_log` en fin de chaque script cron (backup, sybil, retro, weekly) | `team.db` → `memory_log` | [[Forge]] |`
- after:
  `| Ajouter un appel `memory_log` en fin de chaque script cron (backup, [[Sybil]], retro, weekly) | `team.db` → `memory_log` | [[Forge]] |`

### Line 133

- terms: n8n
- before:
  `| Workflow ≥3 services externes avec logique conditionnelle identifié | Évaluer n8n |`
- after:
  `| Workflow ≥3 services externes avec logique conditionnelle identifié | Évaluer [[n8n]] |`

### Line 139

- terms: n8n
- before:
  `## 4. Architecture Phase 5b — conditionnelle (n8n)`
- after:
  `## 4. Architecture Phase 5b — conditionnelle ([[n8n]])`

### Line 147

- terms: n8n, Docker
- before:
  `| n8n | Orchestration visuelle de workflows multi-services | 1 conteneur Docker, port `127.0.0.1:5678` |`
- after:
  `| [[n8n]] | Orchestration visuelle de workflows multi-services | 1 conteneur [[Docker]], port `127.0.0.1:5678` |`

### Line 148

- terms: SQLite
- before:
  `| SQLite (existant) | Persistence des états workflow via `memory_log` | Déjà actif |`
- after:
  `| [[SQLite]] (existant) | Persistence des états workflow via `memory_log` | Déjà actif |`

### Line 150

- terms: n8n
- before:
  `### Workflows candidats à migrer vers n8n`
- after:
  `### Workflows candidats à migrer vers [[n8n]]`

### Line 154

- terms: Python, SQLite
- before:
  `| Ingestion inbox → classification → team.db | Dropbox/filesystem + Python + SQLite | Haute |`
- after:
  `| Ingestion inbox → classification → team.db | Dropbox/filesystem + [[Python]] + [[SQLite]] | Haute |`

### Line 156

- terms: Python, Obsidian
- before:
  `| Digest email → résumé → daily note | Gmail + Python + Obsidian | Faible (suspendu) |`
- after:
  `| Digest email → résumé → daily note | Gmail + [[Python]] + [[Obsidian]] | Faible (suspendu) |`

### Line 160

- terms: n8n, Docker
- before:
  `- n8n stocke ses données dans un volume Docker isolé.`
- after:
  `- [[n8n]] stocke ses données dans un volume [[Docker]] isolé.`

### Line 161

- terms: PostgreSQL, Redis
- before:
  `- Aucune réutilisation du PostgreSQL ou Redis de Plane.`
- after:
  `- Aucune réutilisation du [[PostgreSQL]] ou [[Redis]] de Plane.`

### Line 179

- terms: [[Corbeau]], [[Forge]], Obsidian
- before:
  `- **Pilote 1** — Gouvernance documentaire (Corbeau + Forge) : classifier notes, valider YAML, maintenir index Obsidian.`
- after:
  `- **Pilote 1** — Gouvernance documentaire ([[Corbeau]] + [[Forge]]) : classifier notes, valider YAML, maintenir index [[Obsidian]].`

### Line 180

- terms: [[Forge]], [[Castor]]
- before:
  `- **Pilote 2** — Architecture système (Forge + Castor) : câbler concrètement les couches mémoire définies en Phase 4.`
- after:
  `- **Pilote 2** — Architecture système ([[Forge]] + [[Castor]]) : câbler concrètement les couches mémoire définies en Phase 4.`

### Line 181

- terms: [[Chouette]], [[Clio]], [[Forge]], [[Corbeau]], BirdNET, ESP32
- before:
  `- **Pilote 3** — Wildlife / Bioacoustique (Chouette + Clio + Forge + Corbeau) : connecter BirdNET, RPi, ESP32, datasets audio à la mémoire PKA.`
- after:
  `- **Pilote 3** — Wildlife / Bioacoustique ([[Chouette]] + [[Clio]] + [[Forge]] + [[Corbeau]]) : connecter [[BirdNET]], RPi, [[ESP32]], datasets audio à la mémoire PKA.`

## `JCH_Inbox/07_ARCHIVES/MODEL_HANDOFF_2026-05-28.md`

### Line 12

- terms: [[Dobby]]
- before:
  `- `ADAPTER-PROMPT.md` and `MEMORY.md` were updated with Dobby operating rules and memory protocol.`
- after:
  `- `ADAPTER-PROMPT.md` and `MEMORY.md` were updated with [[Dobby]] operating rules and memory protocol.`

### Line 19

- terms: n8n, Qdrant, Redis, PostgreSQL
- before:
  `- No Hermes / n8n / Qdrant / Redis / PostgreSQL rollout yet.`
- after:
  `- No Hermes / [[n8n]] / [[Qdrant]] / [[Redis]] / [[PostgreSQL]] rollout yet.`

### Line 20

- terms: Obsidian
- before:
  `- Obsidian is not part of the current runtime work.`
- after:
  `- [[Obsidian]] is not part of the current runtime work.`

### Line 27

- terms: Tailscale
- before:
  `- Tailscale is operational with CLI version `1.98.2`.`
- after:
  `- [[Tailscale]] is operational with CLI version `1.98.2`.`

### Line 50

- terms: SQLite
- before:
  `  - creates consistent SQLite snapshots`
- after:
  `  - creates consistent [[SQLite]] snapshots`

### Line 61

- terms: [[Dobby]]
- before:
  `### Dobby protocol / memory`
- after:
  `### [[Dobby]] protocol / memory`

### Line 114

- terms: [[Vasco]]
- before:
  `- `20` Vasco`
- after:
  `- `20` [[Vasco]]`

### Line 115

- terms: [[Vasco]]
- before:
  `- `83` Vasco`
- after:
  `- `83` [[Vasco]]`

### Line 116

- terms: [[Renard]]
- before:
  `- `128` Renard`
- after:
  `- `128` [[Renard]]`

### Line 117

- terms: [[Vasco]]
- before:
  `- `147` Vasco`
- after:
  `- `147` [[Vasco]]`

### Line 118

- terms: [[Vasco]]
- before:
  `- `214` Vasco`
- after:
  `- `214` [[Vasco]]`

### Line 119

- terms: [[Renard]]
- before:
  `- `228` Renard`
- after:
  `- `228` [[Renard]]`

### Line 137

- terms: SQLite, Git
- before:
  `- Do not include SQLite backups in Git.`
- after:
  `- Do not include [[SQLite]] backups in [[Git]].`

## `JCH_Inbox/99_SYSTEM/tool-pointers/GEMMA.md`

### Line 5

- terms: [[Dobby]]
- before:
  `You are Dobby 🦉, the team orchestrator of PKA_JCH.`
- after:
  `You are [[Dobby]] 🦉, the team orchestrator of PKA_JCH.`

### Line 6

- terms: [[Dobby]]
- before:
  `Dobby is your operating identity inside this folder — not a persona you switch into.`
- after:
  `[[Dobby]] is your operating identity inside this folder — not a persona you switch into.`

### Line 10

- terms: [[Bouvier]], [[Furet]], [[Castor]], [[Corbeau]], [[Delphi]], [[Héron]], [[Lynx]], [[Jade]]
- before:
  `The 24 specialists (Bouvier, Furet, Castor, Corbeau, Delphi, Héron, Lynx, Jade,`
- after:
  `The 24 specialists ([[Bouvier]], [[Furet]], [[Castor]], [[Corbeau]], [[Delphi]], [[Héron]], [[Lynx]], [[Jade]],`

### Line 11

- terms: [[Renard]], [[Iris]], [[Forge]], [[Ariane]], [[Bruno]], [[Sybil]], [[Clio]], [[Sigma]], [[Vega]], [[Trace]], [[Miel]], [[Vasco]]
- before:
  `Renard, Iris, Forge, Ariane, Bruno, Sybil, Clio, Sigma, Vega, Trace, Miel, Vasco,`
- after:
  `[[Renard]], [[Iris]], [[Forge]], [[Ariane]], [[Bruno]], [[Sybil]], [[Clio]], [[Sigma]], [[Vega]], [[Trace]], [[Miel]], [[Vasco]],`

### Line 12

- terms: [[Nova]], [[Argus]], [[Pie]]
- before:
  `Nova, Argus, Pie) are distinct identities you delegate to — you do NOT become them.`
- after:
  `[[Nova]], [[Argus]], [[Pie]]) are distinct identities you delegate to — you do NOT become them.`

### Line 18

- terms: SQLite
- before:
  `- `TEAM/team.db` — authoritative roster and all PKA data (SQLite)`
- after:
  `- `TEAM/team.db` — authoritative roster and all PKA data ([[SQLite]])`

### Line 33

- terms: Claude
- before:
  `- Capacités d'orchestration réduites par rapport à Claude Sonnet — préférer les tâches structurées`
- after:
  `- Capacités d'orchestration réduites par rapport à [[Claude]] Sonnet — préférer les tâches structurées`

### Line 37

- terms: [[Dobby]]
- before:
  `Reply to JCH as Dobby with:`
- after:
  `Reply to JCH as [[Dobby]] with:`

## `JCH_Inbox/99_SYSTEM/tool-pointers/QWEN.md`

### Line 5

- terms: [[Dobby]]
- before:
  `You are Dobby 🦉, the team orchestrator of PKA_JCH.`
- after:
  `You are [[Dobby]] 🦉, the team orchestrator of PKA_JCH.`

### Line 6

- terms: [[Dobby]]
- before:
  `Dobby is your operating identity inside this folder — not a persona you switch into.`
- after:
  `[[Dobby]] is your operating identity inside this folder — not a persona you switch into.`

### Line 10

- terms: [[Bouvier]], [[Furet]], [[Castor]], [[Corbeau]], [[Delphi]], [[Héron]], [[Lynx]], [[Jade]]
- before:
  `The 24 specialists (Bouvier, Furet, Castor, Corbeau, Delphi, Héron, Lynx, Jade,`
- after:
  `The 24 specialists ([[Bouvier]], [[Furet]], [[Castor]], [[Corbeau]], [[Delphi]], [[Héron]], [[Lynx]], [[Jade]],`

### Line 11

- terms: [[Renard]], [[Iris]], [[Forge]], [[Ariane]], [[Bruno]], [[Sybil]], [[Clio]], [[Sigma]], [[Vega]], [[Trace]], [[Miel]], [[Vasco]]
- before:
  `Renard, Iris, Forge, Ariane, Bruno, Sybil, Clio, Sigma, Vega, Trace, Miel, Vasco,`
- after:
  `[[Renard]], [[Iris]], [[Forge]], [[Ariane]], [[Bruno]], [[Sybil]], [[Clio]], [[Sigma]], [[Vega]], [[Trace]], [[Miel]], [[Vasco]],`

### Line 12

- terms: [[Nova]], [[Argus]], [[Pie]]
- before:
  `Nova, Argus, Pie) are distinct identities you delegate to — you do NOT become them.`
- after:
  `[[Nova]], [[Argus]], [[Pie]]) are distinct identities you delegate to — you do NOT become them.`

### Line 18

- terms: SQLite
- before:
  `- `TEAM/team.db` — authoritative roster and all PKA data (SQLite)`
- after:
  `- `TEAM/team.db` — authoritative roster and all PKA data ([[SQLite]])`

### Line 34

- terms: [[Jade]]
- before:
  `- Capacités multilingues fortes (FR/EN/ZH) — pertinent pour les tâches Jade`
- after:
  `- Capacités multilingues fortes (FR/EN/ZH) — pertinent pour les tâches [[Jade]]`

### Line 38

- terms: [[Dobby]]
- before:
  `Reply to JCH as Dobby with:`
- after:
  `Reply to JCH as [[Dobby]] with:`

## `wiki/Daily/2026/05/2026-05-29-hermisation-complete.md`

### Line 14

- terms: 01_AI_IT_TOOLS
- before:
  `- Projet : 01_AI_IT_TOOLS`
- after:
  `- Projet : [[01_AI_IT_TOOLS]]`

### Line 20

- terms: [[Chouette]], [[Clio]], [[Corbeau]]
- before:
  `Phase 3 Local_Infrastructure_Setup.md. Phase 4 Persistent_Memory_Architecture.md + 4a active. Phase 5 Workflow_Orchestration.md + 5a active. Pilote 1 wikilinks appliqués. Pilote 2 System_Architecture_Report.md + schema v8. Pilote 3 wildlife knowledge indexé (Chouette+Clio+Corbeau). Inbox triée, 5 livrables Vetalyx validés JCH. /save branché sur memory_log.`
- after:
  `Phase 3 Local_Infrastructure_Setup.md. Phase 4 Persistent_Memory_Architecture.md + 4a active. Phase 5 Workflow_Orchestration.md + 5a active. Pilote 1 wikilinks appliqués. Pilote 2 System_Architecture_Report.md + schema v8. Pilote 3 wildlife knowledge indexé ([[Chouette]]+[[Clio]]+[[Corbeau]]). Inbox triée, 5 livrables Vetalyx validés JCH. /save branché sur memory_log.`

### Line 23

- terms: PostgreSQL, Redis, Qdrant, n8n, Claude, ChatGPT, Python, Apple, Pi, Heron
- before:
  `PostgreSQL/Redis non justifiés. Qdrant différé knowledge>=100 (actuellement 28). n8n différé workflow>=3 services. Claude/ChatGPT/Python/Apple/Pi exclus wikilinks. Heron canonique sans accent. file_index_legacy_scope2 supprimée (−57% DB).`
- after:
  `[[PostgreSQL]]/[[Redis]] non justifiés. [[Qdrant]] différé knowledge>=100 (actuellement 28). [[n8n]] différé workflow>=3 services. [[Claude]]/[[ChatGPT]]/[[Python]]/[[Apple]]/[[Pi]] exclus wikilinks. [[Heron]] canonique sans accent. file_index_legacy_scope2 supprimée (−57% DB).`

### Line 26

- terms: BirdNET, Qdrant, n8n
- before:
  `Câble USB-C PD pour undervoltage RPi5 → protocole 24h BirdNET. Alimenter knowledge vers 100 entrées. Qdrant et n8n sur seuils mesurables.`
- after:
  `Câble USB-C PD pour undervoltage RPi5 → protocole 24h [[BirdNET]]. Alimenter knowledge vers 100 entrées. [[Qdrant]] et [[n8n]] sur seuils mesurables.`

## `wiki/log.md`

### Line 112

- terms: Codex, 01_AI_IT_TOOLS
- before:
  `2026-05-29 01:45 — Save Codex [model=claude-sonnet-4-6 ; project=01_AI_IT_TOOLS] : hermisation-complete (Hermisation PKA_JCH complète. 5 phases + 3 pilotes livrés. Infrastructure opérationnelle : memory_log, skills, knowledge, audit log dashboard, wikilinks vault appliqués (356 sur...) — `wiki/Daily/2026/05/2026-05-29-hermisation-complete.md``
- after:
  `2026-05-29 01:45 — Save [[Codex]] [model=claude-sonnet-4-6 ; project=[[01_AI_IT_TOOLS]]] : hermisation-complete (Hermisation PKA_JCH complète. 5 phases + 3 pilotes livrés. Infrastructure opérationnelle : memory_log, skills, knowledge, audit log dashboard, wikilinks vault appliqués (356 sur...) — `wiki/Daily/2026/05/2026-05-29-hermisation-complete.md``
