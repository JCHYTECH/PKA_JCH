# MEMORY — PKA_JCH
> Connaissances accumulées, décisions, chronologie des événements.
> Dernière mise à jour : 2026-06-20 — Kimi routing direct Moonshot + split Hermes
> 
> **SOUL.md** → personnalité et règles de comportement de Dobby
> **USER.md** → profil de JCH, setup technique, projets actifs
> **MEMORY.md** → ce fichier — connaissances, décisions, historique

---

## État équipe

- **31 membres actifs** (source : `team.db`) — 30 spécialistes + Dobby. Derniers ajouts : Araignée #30, Fourmi #31.
- **Recrutement gelé** levé ponctuellement pour besoin opérationnel avéré — re-gelé après intégration.
- **Graphify onboardé** — attribué à Corbeau (#5). Outil de knowledge graph extraction (v0.4.29), doc `docs/system/graphify.md`.

---

## Session 2026-06-19 — Photo Keyworder

- **photo_keyworder.py** — Auto-tagging photos nature par vision model local (Ollama). 100% autonome, zéro API Google.
- **Taxonomie** : 62 catégories (faune 80+ espèces, flore 40+, comportements, saisons, lumières, compositions, habitats, techniques).
- **Modèle** : gemma4 (M5 local, ~18s/image) ou llama3.2-vision:11b (M1). Testé et fonctionnel.
- **Sortie** : IPTC + XMP + HierarchicalSubject → directement lisible par Lightroom (Metadata → Read from Files).
- **Cache** : évite de re-traiter les images déjà tagguées.
- Fichiers : `scripts/photo_keyworder.py`, `06_PHOTO_NATURE/keyword_taxonomy.json`, `keyword_prompt.md`, `keyword_cache.json`.
- Usage : `python3 scripts/photo_keyworder.py --input ~/Desktop/Photos/ --m1 --dry-run`

---

## Session 2026-06-19 — Réorganisation WildNexus

- **Extraction NEXUS_ACOUSTIC** (projet #11) — tout le bioacoustique (100+ fichiers, projet « Faune Autour — Radar de Biodiversité Acoustique ») extrait de `06_COMPONENTS/BIOACOUSTIC/` → `03_PROJECTS/12_NEXUS_ACOUSTIC/`. Spécialistes : Clio, Chouette, Musaraigne.
- **Extraction FAUNE_AUTOUR** (projet #12) — code source PWA extrait de `06_COMPONENTS/FAUNE_AUTOUR_APP/` → `03_PROJECTS/FAUNE_AUTOUR/`. Projet gelé.
- **Renommage** `06_COMPONENTS` → `06_ADJACENT` — le nom « COMPONENTS » suggérait à tort des sous-composants du projet, alors que ce sont des projets adjacents.
- **Nettoyage** `08_TECH_NOTES` reclassé (bioacoustique → NEXUS_ACOUSTIC, hardware → 99_REFERENCES, veille → veille/). PPK2 CSV déplacés de `05_VISUALS` vers `03_ENERGIE_AUTONOMIE/mesures/`.
- **Création** `03_P0_ENGINEERING/99_REFERENCES/` pour ESP-DIVE, PPK2, datasheets, veille.
- Analyse complète dans `TEAM_Inbox/2026-06-19_dobby_analyse-reorganisation-wildnexus.md`.
- Projets actifs : 10 → 12 (NEXUS_ACOUSTIC + FAUNE_AUTOUR extraits).

---

## Échecs récents

<!-- Dobby log automatiquement les échecs ici — Format : [YYYY-MM-DD] [Agent] : [Description] [Statut : résolu/ouvert] -->
- [2026-06-07] [M1] : M1 headless (100.73.212.110) régulièrement inaccessible — sleep/standby actif malgré `sleep 0`. Cause : `standby 1` + `hibernatemode 3` par défaut. Résolu par `sudo pmset -a standby 0 hibernatemode 0`. Vérifié : p2p direct, SSH, Ollama OK. [Statut : résolu]

---

## Décisions structurelles (juin 2026)

- [2026-06-04] [Optimisation] : MEMORY.md allégé — historique déplacé vers `wiki/archives/memory-history-2026-05.md`. Skills communautaires inutilisées retirées de `skills-lock.json`. Pointer files regénérés. System check auto-healing ajouté.
- [2026-06-04] [Pointer] : Tool pointers régénérés — 10 projets, 2 inbox. Permissions HA corrigées (0600).
- [2026-06-03] [Onboarding] : Graphify attribué à Corbeau par extension de responsabilités — pas de nouveau membre.
- [2026-06-05] [Auto-training] : `dobby_retro.py` réécrit — multi-source (DeepSeek TUI, Claude, composer_history), extraction locale patterns, provider OpenRouter. Tables `retro_patterns` + `retro_sessions` dans team.db.
- [2026-06-05] [Fine-tuning] : Pipeline LoRA via MLX — `dobby_train.py`. Modèle fine-tuné `Qwen2.5-7B-Instruct` + LoRA sur M1 (32GB RAM, 14.6GB peak). Ollama model `dobby-prompt` créé.
- [2026-06-05] [Infra] : Python 3.12.4 + MLX 0.31.2 installés sur M1 via pyenv. Cron 23h actif sur M1 pour rétro quotidienne. Launchd plist sur M5 (installer via `bin/install-dobby-retro.sh`).
- [2026-06-06] [HA] : iPad ajouté comme tableau de bord HA via Tailscale — `http://100.108.55.44:8123`
- [2026-06-06] [NotebookLM] : 5 notebooks préparés — WildNexus (25), Vetalyx (25), PhotoNature (25), Travels (25), PhotoAIJury (12). Correction budget WildNexus v0.3 (pivot AA). 7 livrables notebook_sources/.
- [2026-06-07] [Infra] : M1 — pmset corrigé (standby 0, hibernatemode 0). Maintenance session : permissions logs 0600, pointers regénérés, todo HTML resynchronisé. Modèles Ollama mis à jour : remplacement phi4 + mistral-nemo par gemma3:12b-it-qat (gain ~16 Go).
- [2026-06-07] [Domotique v1] : Première ébauche avec **N100 + HA OS** (Beelink S12 Pro). Budget vérifié ~387€. Plan dans `docs/system/station-domotique-plan.md`.
- [2026-06-06] [Onboarding] : Araignée #30 onboardée — IoT & Embedded Systems Specialist. Recrutement suite mandat Furet.
- [2026-06-07] [Domotique v2] : Pivot vers **RPi5 4GB + SSD USB** après analyse budget. Budget vérifié ~234-260€. Même coordonateur Zigbee (Sonoff ZBDongle-P). Plans disponibles : `docs/system/station-domotique-plan.md` (N100) et `docs/system/station-domotique-plan-rpi5.md` (RPi5).
- [2026-06-08] [Onboarding] : Fourmi #31 onboardée — Bench Technician Électronique & Protocoles. Recrutement suite gap opérationnel M-02 WildNexus. Profil : exécution protocoles, câblage, mesures PPK2, diagnostic 1er niveau.
- [2026-06-09] [Sécurité] : Secrets pka-decouvertes isolés dans `JCH_PRIVATE/decouvertes.env`. Token Telegram renouvelé. TokenMaskFilter + RotatingFileHandler sur collector.py. Log purgé (88K lignes → 0 token). `.gitignore` renforcé.
- [2026-06-09] [Convention] : Attribution modèle désormais documentée dans chaque script via champ `Model:` en docstring. Format : `Model: <modèle> (date, contexte)`. Objectif : affiner les choix de modèle par type de tâche.
- [2026-06-09] [Cleanup] : Artefacts NotebookLM supprimés — 6 × `NOTEBOOKLM_SOURCES.md` + 5 × `notebook_sources/` (~100 fichiers copies) éliminés des projets. Doublons, plus besoin.
- [2026-06-12] [Skills] : 25 skills SEO (claude-seo) installées depuis AgriciDaniel/claude-seo → `.claude/skills/seo*`. Trace #20 activé. Couverture : technique, contenu, schema, local, backlinks, ecommerce, GEO, programmatique.
- [2026-06-12] [Knowledge] : Glossaire IA 50 termes extrait de sAIpien (MIT Media Lab) → `wiki/AI-Tools/glossary-ai.md`. Cadre 6 piliers (Ideas, Data, Products, Experiences, Empowerment, Readiness).
- [2026-06-12] [Auto-apprentissage] : `pka_skill_generator.py` créé — boucle fermée retro_patterns → LLM → SKILL.md. Cron hebdo dimanche 22h via launchd.
- [2026-06-12] [Procurement] : Pipeline achat Mouser/DigiKey. Chaque ligne BOM → réf Mouser + DigiKey. Indispo → fallback auto, jamais de ligne vide. CSV prêts import. Fourmi exécute, Bruno valide budget. BOM v0.3 §11 = index canonique.
- [2026-06-18] [Procurement — Compétence autonome] : Session Arbor complète — 3 cycles de recherche exécutés. Agent `scripts/procurement/` étendu avec DigiKey Search v4, basket optimizer (seuils 50€ gratuité), validation MPN (score confiance ✅⚠️🔴), cache supply SQLite (team.db). Testé sur BOM WildNexus 11 composants : dual search 60s vs 2h manuel, facteur ~120×. Passe 2 : 100% cache, 0 appel API. Rapport dans `TEAM_Inbox/`. Farnell API confirmée (partner.element14.com — REST + SOAP, en attente de compte JCH). Octopart évalué : API payante (~$100-500/mois) non justifiée pour prototypage ponctuel. Alternatives chinoises sérieuses : LCSC (endpoint non documenté), TME (API XML documentée). Arbre Arbor dans `.arbor/research/procurement-electronique/`.
- [2026-06-18] [Pointer — Règle d'adresse] : Règle d'adresse ABSENTE des pointers AGENTS.md et DEEPSEEK.md — uniquement dans MEMORY.md et ADAPTER-PROMPT.md. Corrigé : ajoutée en #1 dans la section Behavioral rules (MANDATORY) des deux fichiers. Root cause : `generate_tool_pointers.py` n'incluait pas la règle d'adresse dans le template. À corriger côté générateur si les pointers sont regénérés.
- [2026-06-12] [Procurement — Prix réels] : ⚠️ PIR EKMB estimé 5€ → réel 22,30€ (×4.5). Règle : tout prix BOM vérifié sur site fournisseur avant présentation. Ne jamais estimer de mémoire. Écart >2× fausse les priorités CoG.
- [2026-06-19] [Honcho PKA] : Pivot asynchrone → synchrone. Dobby exécute Honcho en direct après chaque session significative (≥5 échanges, /save, décision). Insights stockés dans `user_model` (team.db), confiance ≥0.8 → proposition USER.md automatique. Design spec v0.2 : `docs/system/honcho-pka-design.md`.
- [2026-06-19] [Memory Nudge] : Pivot batch → synchrone. Dobby exécute Memory Nudge en direct toutes les ~10 réponses — extrait faits JC, décisions, patterns. Cohérent avec Honcho synchrone. Script `pka_memory_nudge.py` reste en fallback batch.
- [2026-06-19] [Skill Generator] : Ajout sources Honcho (`user_model`) et Memory Nudge (`dobby_feedback`) en priorité sur `retro_patterns`. Poids : Honcho ×3, Nudge ×2, retro ×1. Dry-run OK — les 3 top candidats sont maintenant des insights Honcho structurés au lieu de fragments bruités. En accumulation — point dans quelques semaines.
- [2026-06-19] [Gateway unifiée] : `pka_gateway.py` (480+ lignes) — point d'entrée unique multi-canal remplaçant les connecteurs fragmentés. 5 canaux actifs (local_inbox, dropbox_inbox, apple_notes, telegram, git_commits). Table `gateway_messages` dans team.db, state file `_local/gateway_state.json`, launchd plist `com.dobby.pka-gateway.plist`. Premier scan : 164 messages détectés.
- [2026-06-19] [Telegram — remise en route] : Bot out depuis le 19 juin. Diagnostic : clés API Anthropic + OpenAI périmées dans `.env` (différentes des clés centrales `~/.config/pka-jch/api_keys`). Bug Markdown entities : `parse_mode="Markdown"` causait `BadRequest` sur les réponses Claude. Corrigé : `.env` mis à jour depuis clés centrales, 5 parse_mode Markdown → None, conflit launchd résolu (ancien `com.pka.dobby.plist` désactivé, nouveau `com.dobby.telegram-bot.plist`). Bot actif, canal Telegram intégré dans gateway.
- [2026-06-12] [Skills — Analyse] : 59 skills audités, classés par fréquence (5 niveaux). 25 skills SEO = 42% du catalogue, <5% des activations. Cœur opérationnel = 15 skills.
- [2026-06-12] [Skills — Amélioration] : Top 12 skills analysés — 4 corrigés (session-start, file-versioning, obsidian-kg, wildnexus-adr), 4 shadowés (ingest, capture, brief, status), 2 créés (system-check, weekly-report). Décision : les skills locaux `skills/` prennent priorité sur les skills fondation du runtime. Politique de shadow pour toute amélioration future.
- [2026-06-12] [Pipeline ESP32] : Arduino CLI 1.5.1 + ESPHome 2026.5.3 installés sur M5. Core ESP32 3.3.9. En attente d'un ESP32 branché pour test blink. Pipeline prêt pour prototypage firmware WildNexus conversationnel.
- [2026-06-13] [InsectNet — Alpes] : Query Xeno-Canto API v3 → 132 espèces d'orthoptères dans l'arc alpin (box:44,5,48,13), 2 868 enregistrements. Nos 5 espèces V0.1 = 6.1% du potentiel. Inventaire complet dans `INSECTNET/02_DATASET/alpine-species-inventory.md`. Genres clés : Chorthippus (700+), Pholidoptera (260+), Anonconotus endémique (140+).
- [2026-06-13] [Qualité — Vérification] : Règle « Données chiffrées vérifiées » élargie en « Vérification avant affirmation » dans AGENTS.md + MEMORY.md. Registre `docs/system/sources-verite.md` créé — 40+ domaines avec source autoritaire et outil. Protocole 3 temps : fichier projet → outil externe → dire « non vérifié ».
- [2026-06-13] [Architecture — LLM Wiki] : Pattern Karpathy adopté. 3 couches formalisées dans `AGENTS.md` (Raw=JCH_Inbox/PRIVATE, Wiki=wiki/, Schema=AGENTS.md+skills). `wiki/index.md` réécrit — catalogue auto-maintenu. `wiki/log.md` formaté `## [DATE] op | description` — grep-parseable. Document fondateur archivé dans `wiki/Knowledge/AI-Tools/LLM Wiki — Karpathy pattern.md`.
- [2026-06-13] [InsectNet — xcapi] : Package `xenocanto-api` (xcapi 0.3.1) adopté → remplace 3 scripts de collecte par 1 commande. Wrapper `bin/xcapi` + `scripts/insectnet_xcapi_ingest.py` (enrichissement metadata). Scripts `insectnet_xc_metadata.py`, `insectnet_select_audio_candidates.py`, `insectnet_download_audio.py` marqués DEPRECATED. Pipeline segmentation/QC/split conservé. Venv dans `.venv/`. Document Xeno-Canto routé vers `INSECTNET/01_SOURCES/`.
- [2026-06-13] [WildNexus — NLM] : NotebookLM a interprété les 12 SOPs M-02 en PPTX 14 slides (`2026-06-13_NLM_SOP-M02-Metrology_Protocol.pptx`). Analyse Dobby : capture fidèle des seuils et workflow 6 phases, mais gaps critiques — code firmware absent, règles de sécurité incomplètes (SOP-03, SOP-10), lien ADR-010 R4 manquant, grilles GO/ORANGE/NO-GO absentes. Verdict : aide-mémoire visuel uniquement, pas un remplacement des SOPs Markdown. Routé vers `03_WILDNEXUS/05_VISUALS_DASHBOARDS/` avec PNG exemple SOP-01.
- [2026-06-13] [Système — Recovery] : Gap de 7 jours dans les daily notes (08→12 juin) comblé. 5 daily notes régénérées depuis retros + sybil-auto + system checks. Diagnostic : `com.dobby.retro.plist` est opérationnel. Vraie cause : Dobby n'a pas fait de `/save`.
- [2026-06-13] [HA — Zigbee] : Préparation intégration Sonoff AirGuard TH (SNZB-02DR2, Zigbee). Script `_local/install-zigbee-ha.sh` prêt + mode d'emploi `docs/manuels/sonoff-zigbee-ha-guide.md`. Reste à faire : acheter un Sonoff ZBDongle-E (~25€), le brancher, lancer le script, puis ZHA → appairage. Pas besoin de HACS pour ce capteur Zigbee.
- [2026-06-13] [Architecture IoT — Décision] : Architecture distribuée validée. 3 HA locaux autonomes — Belgique (M5 Docker), Italie (RPi 5 + HA OS), Van (RPi 5 + HA OS). Chaque site = ZBDongle-E. Supervision unifiée via iPhone (app HA multi-serveurs + Tailscale). Le van doit fonctionner offline (alarme portes, frigo). Pas de serveur central.
- [2026-06-14] [InsectNet — xcapi validé] : Clé API XC v3 testée, ingestion xcapi fonctionnelle. Cicada orni absent de XC — remplacé par **Conocephalus fuscus** (30 enregistrements, qualité A, licence CC BY-SA, 24 min → ~479 segments). Métadonnées enrichies dans `02_DATASET/conocephalus-fuscus-metadata.csv`.
- [2026-06-14] [ARTEON — Phase 0.3] : Évaluation JCH des rapports Argus — 16/58 analyses évaluées. Résultat : 81% d'acceptation (2👍 + 11👌), 19% de rejet (3👎). Points faibles : identification d'espèces ambiguës, scènes complexes. Prompt mis à jour dans `run_analysis.py` (+ règles géographiques, + règles scènes complexes). Dashboard dans `02_ARTEON/phase03-evaluation-argus.html`.
- [2026-06-15] [Backup] : Backup chiffré PKA → Dropbox (`scripts/backup_pka_to_dropbox.py`). AES-256-CBC via Keychain. team.db + JCH_PRIVATE chiffrés, MEMORY.md + docs/system/ en miroir. Launchd quotidien 08:15. Rotation 7j.
- [2026-06-15] [Sécurité] : Scanner prompt injection `pka_prompt_guard.py` déployé. Architecture airlock 3 niveaux : pré-traitement HTML/Unicode → détection patterns/heuristiques → scoring 0-100 + quarantaine. Pipelines inbox (ingest, Pie) intégrés. 5 familles d'attaques couvertes : zero-width binaire, Unicode tags, bidi override, homoglyphes, payload splitting. Recherche OWASP LLM01 + promptfoo + ctx-guard + cyberdesserts. Brief Pie (`TEAM_Inbox/2026-06-15_dobby_brief-pie_prompt-injection-security.md`).
- [2026-06-14] [InsectNet — M1] : Plan de migration du pipeline InsectNet (segmentation, spectrogrammes, training CNN) du M5 (16 Go) vers le M1 headless (32 Go, MLX 0.31.2, Python 3.12.4). Gains : RAM ×2, délestage M5, jobs longs 24/7 sans impacter le bureau. À exécuter plus tard — nécessite accès M1 au dépôt PKA (rsync ou partage réseau).
- [2026-06-20] [Kimi — Routing] : Kimi K2.7 basculé d'OpenRouter → API Moonshot directe (`api.moonshot.ai/v1` — `.cn` → `.ai` corrigé après 401). Clé `~/.config/pka-jch/kimi_key.txt`. Modèle `kimi-k2.7-code`. `KIMI.md` créé (pointer file dédié). `deepseek_chat.py` rendu générique via `PKA_POINTER` + `PKA_PROVIDER`. `dobby.sh` : case `kimi|kimik2|moonshot`, extrait du bloc OpenRouter ; détection auto `.venv/bin/python3` (évite conflit pydantic Python 3.13 système). `model_config.json` + `dobby-doctor.py` endpoint corrigés.
- [2026-06-20] [Siri — CarPlay] : Guide complet `docs/manuels/dobby-siri-carplay.md` — Raccourci iOS « Dobby » permettant de parler à Dobby via Siri + API Kimi en mains libres (voiture, CarPlay). Pipeline : dictée vocale → API Moonshot → réponse lue par Siri. ~$0.02/interaction.
- [2026-06-20] [Agent — Outils] : `deepseek_chat.py` upgadé en agent avec tool calling (OpenAI-compatible). 5 outils : `read_file`, `list_dir`, `grep_files`, `exec_shell`, `write_file`. Workspace isolé dans PKA_DIR. Tous les modèles (DeepSeek, Kimi, OpenRouter) bénéficient des outils automatiquement. Kimi K2.7 confirmé compatible tool calling natif.
- [2026-06-20] [Gateway — Intégration] : Gateway (`pka_gateway.py`) intégrée au protocole de démarrage Dobby. 128 messages historiques acquittés. À chaque « dobby », Dobby interroge `gateway_messages` pour les nouveaux messages depuis la dernière session. 5 canaux : Telegram, Dropbox, Apple Notes, inbox local, git commits. Piste d'audit complète.
- [2026-06-20] [P1 — Nettoyage] : 16 launchd zombies désactivés (→ `.disabled`), 22 MB de logs purgés. `.claude/skills/` supprimé (doublon de `.agents/skills/`). 3 venvs → 1 (`.venv` unique, 210 MB libérés). `requirements.txt` unifié racine. `pka_security_audit.py` exclut `node_modules`, `.venv`, `*.d.ts` — 12 faux positifs → 0. 8 `.DS_Store` + `.bak` supprimés.

---

## Suivi des modèles par script

| Script | Modèle | Date | Tâche |
|--------|--------|------|-------|
| `scripts/decouvertes-collector/collector.py` | unknown | ~2026-06-02 | Bot Telegram collecteur |
| `scripts/decouvertes-collector/analyzer.py` | unknown | ~2026-06-02 | Analyse lieux + fiches Obsidian |
| `scripts/decouvertes-collector/collector.py` (fix) | deepseek-v4 | 2026-06-09 | TokenMaskFilter, rotation logs, isolation secrets |
| `scripts/insectnet_xcapi_ingest.py` | deepseek-v4 | 2026-06-13 | Ingest Xeno-Canto via xcapi + enrichissement metadata |

---

## Session 2026-06-19 — Amélioration système Hermes → PKA

### Contexte
Analyse du transcript Hermes Agent (NousResearch, 197k★, v0.15.2) et recherche web (docs officielles, Hermes Atlas, Honcho, Dev.to « 5 layers of memory ») + 3 spécialistes (Forge, Corbeau, Furet). Objectif : extraire les patterns applicables à PKA.

### Décisions
- **Split SOUL.md / USER.md / MEMORY.md** — pattern Hermes soul/user/memory. Architecture mémoire 3 fichiers distincts.
- **Memory Nudge** — script `pka_memory_nudge.py` (225 lignes) pour extraction mémoire post-réponse (toutes les ~10 réponses ou /save)
- **Alerte compression contexte** — règle SOUL.md : Dobby alerte à 50% du context window
- **Skill system-improvement-ingest** — grille 6 axes pour tout document d'amélioration
- **Tableaux de pilotage (×3)** — etat-projets.md, matrice-modeles.md, decisions-pka.md
- **Design specs** — Honcho PKA (user modeling évolutif) + FTS5 sessions (recherche historique)
- **Instructions système consolidées** — 42 instructions dans un tableau unique

### Fichiers créés (10)
SOUL.md, USER.md, etat-projets.md, matrice-modeles.md, decisions-pka.md, instructions-systeme.md, roadmap-p2.md, pka_memory_nudge.py, honcho-pka-design.md, fts5-sessions-design.md

### Fichiers modifiés (10)
MEMORY.md, AGENTS.md, DEEPSEEK.md, GEMINI.md, QWEN.md, CLAUDE.md, ADAPTER-PROMPT.md, SOUL.md, outils-index.md, INDEX.md (04_PILOTAGE)

### Prochaines étapes
- ✅ P0 : Memory Nudge — testé et pivoté synchrone, règle dans SOUL.md
- ✅ P0 : Alerte contexte 50% — activée dans SOUL.md
- ✅ P1 : Honcho PKA — pivoté synchrone, 4 insights, USER.md mis à jour
- ✅ P1 : FTS5 — 6 sessions indexées, pka_retrieve.py --fts opérationnel
- ✅ P1 : Memory Nudge — pivoté synchrone, cohérent avec Honcho
- ✅ Clôture : /save exécuté le 2026-06-20 — daily note + log.md
- 🔧 P2.1 : Skill generator — amélioré (sources Honcho + Nudge), en accumulation
- ⏳ P2.2 : Gateway unifiée — audit connecteurs nécessaire

### Procurement potentiel
- [2026-06-19] [Bioacoustique] : Zoom F3 (220€) + LOM MikroUši Pro (180€) = setup bioacoustique ~400€ pour InsectNet. 32-bit float, 192 kHz, stéréo séparable. À envisager pour remplacer iPhone sur le terrain. Fiche : `TEAM_Inbox/2026-06-19_dobby_recherche-zoom-f3-micro-bioacoustique.md`

---

## Session 2026-06-14 — Wokwi + Test Harness Caméra

### Décisions
- **Wokwi adopté** pour smoke tests CI WildNexus P0. Wokwi CLI v0.26.1 installé sur M5.
- **Périmètre Wokwi** : logique firmware (GPIO, SPI/SD, deep sleep, WiFi). Hors scope : caméra OV5640, LoRa SX1262, mesures conso.
- **Test Harness Caméra** : approche découplée — lire images SD → inference → benchmark, sans attendre la caméra physique. Débloque ADR-010 R4.
- Brief Forge+Nova créé (`TEAM_Inbox/2026-06-14_dobby_brief-forge-nova_test-harness-camera.md`)

### Artefacts créés
- `03_P0_ENGINEERING/05_SIMULATION/wokwi/` — projet Wokwi complet (diagram.json, wokwi.toml, firmware smoke test)
- Simulation validée : BOOT → LED → SD → LOG → deep sleep → TEST PASSED
- Leçon critique : `diagram.json` doit connecter `$serialMonitor` pour capturer le output série

### Outils installés
- `wokwi-cli` v0.26.1 (`~/.wokwi/bin/wokwi-cli`, PATH via ~/.zshrc)
- Token WOKWI_CLI_TOKEN dans ~/.zshrc
- Dépendances : arduino-cli (ESP32-S3), idf-wokwi

### À retenir
- Wokwi = smoke test logique rapide, PAS un remplacement du banc PPK2+Fourmi
- Pour caméra et LoRa : aucun simulateur n'existe. Hardware obligatoire.
- Prochaine étape : Forge+Nova livrent le test harness caméra (deadline 21 juin)

### Décision caméra (2026-06-14)
- Camemake OV5640 rejeté (MOQ 10)
- Acheté : ESP32-CAM OV2640 (~10€) comme outil dév DVP
- Commandé en parallèle : OV5640 DVP M12 24-pin NoIR sur AliExpress (~30€, délai 15-25j)
- BOM v0.2c mis à jour

### Session 2026-06-16 — Redémarrage M5 + Docker restart policy
- Vérifié redémarrage HA après shutdown M5 : OK, reparti automatiquement.
- Corrigé : zigbee2mqtt et mosquitto n'avaient pas `--restart unless-stopped` → crash au shutdown (perte dongle USB → ASH_ERROR_TIMEOUTS).
- Appliqué `docker update --restart unless-stopped mosquitto zigbee2mqtt` → les 3 conteneurs (HA, mosquitto, z2m) repartent maintenant automatiquement.
- Dongle Sonoff ZBDongle-E sur `/dev/cu.usbserial-10`, capteur SNZB-02DR2 (Temphumid) opérationnel.
- ⚠️ **RPI — Projet IoT** : reproduire cette config sur le RPi. Tout conteneur Docker (HA, mosquitto, zigbee2mqtt, etc.) devra avoir `--restart unless-stopped`. Anticiper le même scénario : shutdown → dongle USB disparaît → conteneur perd le port série → sans restart policy, mort définitif. À intégrer dans la procédure de déploiement RPi.
- [2026-06-16] [WildNexus — BOM] : A19 (NULA DeepSleep ESP32-S3, ~25€, 7µA deep sleep) et A20 (Freenove Breakout nu, ~15€) ajoutés au WP02 v0.2c. Objectif : mesurer le vrai deep sleep ESP32-S3 sans overhead DevKit (AMS1117 + CP210x + LEDs = ~1 mA). Budget : +40€, réserve restante ~131€.
- [2026-06-16] [WildNexus — Production] : MCU recommandé = ESP32-S3-WROOM-1-N8R8 (~3.50-4.00 $/u en bulk, ~7-15 µA deep sleep). PCB : JLCPCB assembly pour prototypes (50-60 $ pour 5 PCB soudés). Fourmi QC. Décision JCH : attendre la fin des SOPs M-02 avant de lancer le PCB. A20 (Freenove) à supprimer — redondant avec NULA.
- [2026-06-16] [Permissions — Corrigé 17/06] : 22 fichiers `_local/` (HA DB, zigbee2mqtt logs/DB, zigbee-bridge.log, collector.log) → 0600. 66 faux positifs ignorés (node_modules/ tokenizers, .venv public certs).
- [2026-06-16] [Argus — MCP] : `lightroom-mcp` (github.com/Automaat/lightroom-mcp) et `photoshop-mcp` (github.com/alisaitteke/photoshop-mcp) découverts. Ces MCP servers permettent à un LLM de contrôler Lightroom Classic et Photoshop sans intervention humaine. Argus génère déjà des `lr_params` (JSON) dans `argus_critique.db` → le chaînon manquant est l'application automatique de ces paramètres dans LR via `set_develop_settings`. Roadmap détaillée dans `05_PHOTO_AI_JURY/roadmap-mcp-integration.md`.
- [2026-06-17] [InsectNet — Stratégie test ASAP] : Pipeline audio fonctionnel, dataset Conocephalus fuscus prêt (~479 segments). 3 découvertes DDG : **InsectSet459** (Nature, 26k fichiers, 459 espèces Orthoptères), **PULSE** (arXiv juin 2026, framework semi-supervisé), **BirdNET transfer learning pour insectes** (chirpkit, 37%→55%). Plan 3 phases : baseline BirdNET → fine-tuning → PULSE. Brief Clio pour évaluation scientifique. JCH va enregistrer des chants d'insectes en Italie (longues séquences WAV recommandées).
- [2026-06-17] [IoT RPi — Pré-déploiement] : Stratégie simulation/préparation pour le RPi. **PI-CI** (émulateur RPi5 Docker) pour tester la stack HA+Mosquitto+Zigbee2MQTT avant flashage SD. **QEMU ARM64 Docker** pour validation bare-metal. Briefs Forge (docker-compose ARM64 + test PI-CI + script install + van offline) et Chouette (assemblage hardware + migration capteur SNZB-02DR2 + spécification hardware van). Deadline 28 juin.
- [2026-06-17] [WildNexus — Simulation pré-réception] : Recherche DDG → 6 outils de simulation identifiés. **Cirkit Designer** (ESP32-S3 instruction-accurate, Rust/WASM, WiFi réel), **IoT Virtual Lab** (LoRaWAN), **QEMU ESP-IDF**, **CupCarbon** (Digital Twin), **Velxio** (SPICE open-source). Briefs Araignée (smoke test Cirkit + LoRaWAN simulé) et Forge (firmware MQTT + test harness caméra). Deadline 28 juin. Stratégie : tout ce qui peut être codé/testé sans hardware l'est maintenant.
- [2026-06-17] [Pointer Sync — script + DB corrigés] : `scripts/pka_pointer_sync.py` créé — détection automatique de dérive entre les 6 fichiers pointeurs et `team.db`. Trouvé : Fourmi (#31) absente de `team.db` → corrigé (INSERT). Araignée + Fourmi absentes du roster CLAUDE.md → ajoutées. Tous les compteurs (specialist count, team count, RÈGLE D'ADRESSE) synchronisés → 0 dérive. Le script s'exécute en `--fix` automatique.
- [2026-06-17] [Pointer Sync — CLAUDE.md corrigé] : 6 incohérences détectées et corrigées : (1) team count : 29 → 31 dans 2 endroits, (2) inbox count : 4 → 2, (3) tables DB manquantes ajoutées (dobby_feedback, retro_*, memory_log, email_senders, instincts), (4) doublon file_index supprimé, (5) RÈGLE D'ADRESSE absente du bloc canonique. Propagé vers AGENTS.md, GEMINI.md, DEEPSEEK.md, QWEN.md (30→31 membres, 4→2 inbox). Leçon : les fichiers pointeurs dérivent. Prochaine étape : `pka_pointer_sync.py`.
- [2026-06-17] [Conflict Checker] : `scripts/pka_conflict_checker.py` — détection de contradictions entre spécialistes inspirée de OctoChains ConflictChecker. Deux modes : heuristique (regex + Jaccard, local) et LLM (prompt matrix, via API). Détecte les conflits numériques (ratio >2x), recommandations opposées, et incohérences. Sortie structurée JSON avec sévérité (critical/high/moderate/minor). Testé sur cas réel : 3 conflits détectés entre rapports simulés (deep sleep ESP32, budget, recommandation d'achat).
- [2026-06-17] [Leçon — Mémoire transversale] : La règle d'adresse « commencer par JC » n'existait dans **aucun** fichier canonique (AGENTS.md, MEMORY.md, DEEPSEEK.md, ADAPTER-PROMPT.md). Elle était implicite, portée par les sessions Qwen/Claude mais jamais persistée. **Un système multi-modèles sans mémoire partagée perd les préférences utilisateur.** Corrigé : règle ajoutée dans AGENTS.md + MEMORY.md. Le pipeline `dobby_feedback → knowledge.type='procedure'` est précisément conçu pour éviter que ce scénario ne se reproduise. Prochaine étape : un « pointer sync » automatique qui propage les règles comportementales découvertes vers tous les fichiers pointeurs (AGENTS.md, CLAUDE.md, DEEPSEEK.md, GEMINI.md, QWEN.md).
- [2026-06-17] [Memory Layer v2 — Procédural + Zettelkasten] : `pka_session_extract.py` étendu avec 2 nouvelles passes post-extraction : (1) **mémoire procédurale dynamique** — quand ≥3 feedbacks JCH partagent des mots-clés → génération automatique `knowledge.type='procedure'`, (2) **Zettelkasten linking** — similarité Jaccard entre nouvelles et anciennes entrées → `knowledge_links` automatiques. Inspiré de A-MEM (NeurIPS 2025), Red Hat « From context to dreams », Zylos.ai memory survey. Pipeline complet testé sur session active.
- [2026-06-17] [Memory Layer — Pipeline complet livré] : Architecture mémoire unifiée inspirée de Databricks « Memory Scaling » — spec dans `docs/system/pka-memory-layer.md`. **3 scripts créés et testés :** `pka_session_extract.py` (extraction post-session JSON → `knowledge` + `dobby_feedback` + `retro_patterns`), `pka_retrieve.py` (recherche unifiée multi-sources : team.db + graphify + file_index + MEMORY.md + wiki), `pka_generate_memory.py` (régénération MEMORY.md depuis team.db). Table `dobby_feedback` créée dans team.db. [[Corbeau]] promu Memory Curator (scoring, déduplication, détection obsolescence).
- [2026-06-17] [Purge système] : 34 session JSONs supprimés (20 MB), 46 `.DS_Store` éliminés, artifacts GitHub Actions (`build/`, `report-build-status/`) supprimés, 12 backups team.db mai-début juin supprimés (gardé 11 backups récents), 18 dossiers vides nettoyés, fichiers obsolètes (`MEMORY.md.bak`, `TTD_MASTER`, `.code-workspace`) supprimés. Routage : 3 PPK2 → WildNexus `06_COMPONENTS/PPK2/`, `argus_critique.db` → `05_PHOTO_AI_JURY/`, 16 fichiers WildNexus classés en sous-dossiers, 2 transcripts YouTube routés, Order Mouser #39492997 archivé. Inbox restante : `email_imports/` (1 audio) + `notes_apple/` (54 notes) — à traiter via ingest.
- [2026-06-19] [Architecture — Hermes] : Split SOUL.md / USER.md / MEMORY.md (pattern Hermes). Memory Nudge activé (extraction mémoire synchrone post-réponse). Alerte compression contexte 50% activée. Skill system-improvement-ingest créé (grille 6 axes). 3 tableaux de pilotage (etat-projets, matrice-modeles, decisions-pka). 42 instructions système consolidées dans instructions-systeme.md.
- [2026-06-19] [Honcho PKA + FTS5] : Table user_model + session_fts créées dans team.db. Scripts pka_honcho_analyze.py + pka_fts_index.py. Extension pka_retrieve.py --fts opérationnelle. 4 sessions indexées FTS5. Profil cognitif JC ajouté dans USER.md.
- [2026-06-19] [InsectNet — Pipeline] : 10 fichiers M4A iPhone → 1 441 segments WAV classifiés (Gryllus campestris, Tettigonia viridissima, Gryllus bimaculatus). Manifold 3D UMAP interactif. Arbor Loop densité acoustique (0.2–5 ind/ha). Recherche Lucio Arese (3D/4D sonogram). Recherche Zoom F3 + LOM MikroUši Pro (~400€).
- [2026-06-19] [WildNexus — Test Harness] : Dataset 51 images 224×224 extraites de Lightroom. Contact sheet HTML interactive. Deadline repoussée au 30 juin (attente IR Belgique). Note dropout voltage AMS1117 ajoutée à SOP-10.
- [2026-06-19] [Réorganisation — Projets] : NEXUS_ACOUSTIC (projet #11) + FAUNE_AUTOUR (projet #12) extraits de WildNexus. 06_COMPONENTS → 06_ADJACENT. Nettoyage 08_TECH_NOTES, PPK2, datasheets. Projets actifs : 10 → 12. Analyse complète dans TEAM_Inbox/2026-06-19_dobby_analyse-reorganisation-wildnexus.md.
- [2026-06-20] [Memory Nudge — Activé] : Première exécution live du Memory Nudge. Détection gap MEMORY.md (session 19 juin non capturée). Mode synchrone validé — les gaps mémoire sont détectés et comblés sans script externe.