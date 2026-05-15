---
date: 2026-05-11
tags: [daily, PKA, architecture, modèles, skills]
type: daily
status: active
---

# 2026-05-11 — Hermes Agent & Multi-Model Routing

## Actions

- Analyse Hermes Agent (Nous Research) — évaluation intérêt pour PKA via Furet + Forge + Castor
- Décision : Hermes utile uniquement comme runtime pour modèles locaux (Gemma4, Qwen3)
- Création table `skills` dans `TEAM/team.db` (Castor)
- Création `scripts/skill_write.py` — enregistrement automatique de skill post-tâche (Forge)
- Création `scripts/skill_search.py` — recherche de skill pré-tâche (Forge)
- Ajout section *Skill Memory System* dans `CLAUDE.md` (comportement auto Dobby)
- Premier skill capturé (id=1) : procédure d'analyse outil externe pour intégration PKA
- Création fichiers-pointeurs : `AGENTS.md`, `GEMINI.md`, `GEMMA.md`, `QWEN.md`
- Création `scripts/model_config.json` — routing tâche → modèle (anthropic / ollama / google / openai)
- Création `scripts/model_client.py` — client unifié tous providers
- Création `dobby.sh` — launcher unifié (`--model claude|codex|gemini|gemma4|qwen3`)

## Décisions

- **Hermes mis de côté** sauf pour modèles locaux (Gemma4/Qwen3 sans agent CLI natif)
- **Gemma4 et Qwen3.6 déjà installés** dans Ollama — routing opérationnel via `model_config.json`
- **Gemini CLI** a une commande native `gemini gemma` pour routing local (setup requis)
- **Architecture model routing** : une tâche = un modèle configuré dans JSON, sans toucher au code
- **Routing scripts** : journal/retro → Qwen3.6 local ; weekly_report/bot → Claude Sonnet

## Prochaine étape

- Capturer l'idée d'interface web de gestion (sélecteur modèle + chat + vue team.db) → brief Forge + Vega quand JCH prêt
- `gemini gemma setup` si on veut Gemma4 avec accès filesystem via Gemini CLI
- Mettre à jour les scripts existants (`sybil_journal.py`, `dobby_retro.py`) pour utiliser `model_client.py` au lieu de l'Anthropic SDK direct

---

## Actions (session 2 — ARTEON Phase 0 + Chouette)

- Batch Argus Phase 0 : 52/52 photos analysées — PDF + XMP générés pour chaque
- Table `analyses` créée dans `PHOTO/argus_critique.db` — logging tokens opérationnel
- `scripts/argus_batch.py` créé — wrapper batch avec `--limit` et `--bypass-ethics`
- Flag `--bypass-ethics` ajouté dans `run_analysis.py` et `argus_batch.py`
- Coût réel mesuré : ~0,17$/photo · ~10$ pour 52 photos · Claude Opus 4.7
- Analyse de pattern portfolio par Argus : signature aquatique + portrait serré + axe exposition faible
- Brief pré-shooting Argus décliné pour Canon R10 et Canon 90D (4 situations terrain)
- Matos complet JCH lu : R10 + 90D + RF 200-800 + Tamron 150-600 + Laowa + Godox + LED
- Hiring pipeline #9 ouvert puis fermé : Chouette 🦉 recrutée (membre #25)
- `TEAM/chouette.md` créé — 5 responsabilités dans `team.db`

## Décisions (session 2)

- **Bypass ethics** = flag interne uniquement, filtre client intact
- **Scope ARTEON** : trancher entre wildlife strict ou nature élargie (architecture, sculptures incluses ?)
- **Chouette** : spécialiste terrain #25 — reçoit les scores Argus, produit fiches setup boîtier
- **Phase 0.3** : JCH évalue les 52 PDFs — go/no-go avant backend

## Prochaine étape (session 2)

- JCH évalue les rapports PDF Phase 0 (étape 0.3 du plan ARTEON)
- Décider le scope ARTEON : wildlife strict ou nature élargie
- Chouette produit les fiches setup C1/C2/C3 complètes pour R10 et 90D
- Interface web Dobby (sélecteur modèle + chat) → brief Forge + Vega

---

## Actions (session 3 — Héron + Chouette + ARTEON structure + modèles)

- `scripts/heron_paper.py` créé — recommandation papier Epson ET8550 (6 papiers, profils ICC)
- `scripts/chouette_diagnostic.py` créé — diagnostic matériel EXIF vs scores (4 diagnostics)
- `scripts/backfill_exif.py` créé — backfill EXIF sur 58 analyses existantes (focal, aperture, ISO, shutter)
- `run_analysis.py` mis à jour — extraction EXIF automatique + appel Héron intégré (Step 7)
- Backfill EXIF exécuté : 58/58 analyses mises à jour
- Diagnostic Chouette JCH : 0 problème matériel détecté — axe faible Exposition relève de la technique
- `arteon-colonne-vertebrale.md` créé dans `docs/` — point d'entrée pipeline complet + todo priorisé
- Nettoyage `docs/` ARTEON : 6 fichiers redondants supprimés (chats exports, doublons, stub)
- `todo-jch.html` déplacé vers `JCH_Inbox/` (racine)
- Réorganisation complète `02_ARTEON/` : `brand/` · `strategy/` · `legal/` · `wildlens/` · `instant-lu/`
- `INDEX.md` ARTEON mis à jour selon nouvelle structure
- Codex CLI : authentifié via `auth.json` — prêt
- Gemini CLI : clé API configurée dans `~/.zshrc` + `GEMINI_CLI_TRUST_WORKSPACE=true` dans `dobby.sh` — testé ✅
- DeepSeek : `scripts/deepseek_chat.py` créé + `DEEPSEEK.md` + clé API dans `~/.zshrc` — testé ✅
- `dobby.sh` mis à jour : `--model deepseek` et `--model deepseek-r1` ajoutés
- `model_config.json` mis à jour : provider `deepseek` ajouté
- PKA Digest cron suspendu — mémorisé (à améliorer avant relance)
- Ollama confirmé gratuit pour usage local (cloud payant, local toujours free)

## Décisions (session 3)

- **Héron intégré au pipeline** : chaque analyse génère automatiquement un `_papier.md`
- **Chouette** requiert des données EXIF en DB — backfill fait, nouvelles analyses les capturent nativement
- **Structure ARTEON** : reorganisée par nature (brand/strategy/legal) + par service (wildlens/instant-lu)
- **DeepSeek** : deux modes — `deepseek` (chat) et `deepseek-r1` (reasoner)
- **PKA Digest** : suspendu, ne pas relancer sans amélioration et accord JCH

## Prochaine étape (session 3)

- Tester `./dobby.sh --model gemini|codex|deepseek` en session réelle
- JCH évalue les 58 rapports PDF Phase 0 (étape 0.3)
- Chouette : fiches setup C1/C2/C3 pour R10 et 90D
- Interface web Dobby (Forge + Vega)
