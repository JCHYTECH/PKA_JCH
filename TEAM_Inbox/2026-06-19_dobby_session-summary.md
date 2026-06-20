# Résumé de session — 2026-06-19
> Dobby 🦉 — DeepSeek TUI v0.8.39
> Projet principal : AI_IT_TOOLS (amélioration système)
> Projets touchés : WildNexus, InsectNet, ARTEON

---

## Ce qui a été accompli

### 🏗️ Architecture système (Hermes → PKA)
- Split SOUL.md / USER.md / MEMORY.md (pattern Hermes)
- Memory Nudge — extraction mémoire post-réponse
- Alerte compression contexte automatique
- Skill system-improvement-ingest (grille 6 axes)
- 3 tableaux de pilotage : etat-projets, matrice-modeles, decisions-pka
- Consolidation 42 instructions système (instructions-systeme.md)

### 🧠 P1 — Honcho PKA + FTS5
- Table `user_model` dans team.db
- Table `session_fts` dans team.db
- Script `pka_honcho_analyze.py`
- Script `pka_fts_index.py`
- Extension `pka_retrieve.py --fts`
- 4 sessions indexées FTS5

### 📸 WildNexus — Test Harness Caméra
- Dataset 51 images 224×224 extraites de Lightroom
- Contact sheet HTML interactive
- Deadline repoussée au 30 juin (attente IR Belgique)
- Note dropout voltage AMS1117 ajoutée à SOP-10

### 🦗 InsectNet — Pipeline complet
- 10 fichiers M4A iPhone → 1 441 segments WAV
- Classification : Gryllus campestris (7 fichiers), Tettigonia viridissima (2), Gryllus bimaculatus (1)
- Manifold 3D UMAP interactif
- Analyse individus : fréquence + pulse rate + stéréo spatiale
- Arbor Loop densité acoustique (0.2–5 ind/ha)
- Recherche Lucio Arese (3D/4D sonogram)
- Recherche Zoom F3 + LOM MikroUši Pro (~400€)

### 🧹 Inbox
- 4 transcripts NoteGPT analysés → .processed
- 10 fichiers M4A traités → .processed
- 2 guides diffuseur supprimés
- Reste : email_imports, notes_apple, procurement questions

### 📊 Nouveaux fichiers
- **Créés :** SOUL.md, USER.md, 3 tableaux pilotage, 2 design specs, 1 roadmap P2, 4 scripts, 1 skill
- **Modifiés :** MEMORY.md, 5 pointeurs, ADAPTER-PROMPT.md, outils-index.md, SOP-10, 2 briefs
- **TEAM_Inbox :** 8 analyses livrées
- **team.db :** 2 nouvelles tables (user_model, session_fts)

---

## Fiches de travail — Prochaines actions

### 🔴 P0 — À faire maintenant
| Action | Qui | Fichier |
|--------|-----|---------|
| Tester Memory Nudge sur session active | Dobby | `scripts/pka_memory_nudge.py` |
| Activer alerte contexte 50% | Dobby | Règle SOUL.md |

### 🟡 P1 — Ce trimestre
| Action | Qui | Fichier |
|--------|-----|---------|
| Configurer cron Honcho hebdomadaire | Dobby | `scripts/pka_honcho_analyze.py` |
| Indexer toutes les sessions FTS5 | Dobby | `scripts/pka_fts_index.py --all` |
| Finaliser dataset test harness (IR Belgique) | Nova | `test_harness/test_images/` |
| Protocole triangulation 3 iPhones | Chouette | `TEAM_Inbox/2026-06-19_dobby_arbor-densite-acoustique-orthopteres.md` |
| Calibrer iPhone (dBFS→dB SPL) | Chouette | App NIOSH SLM |

### ⚪ P2 — Vision
| Action | Qui | Fichier |
|--------|-----|---------|
| Skills auto-générées | Dobby | Roadmap P2 |
| Gateway unifiée | Forge | Roadmap P2 |
| BOM health check auto | Forge | Extension procurement |
| Acquisition Zoom F3 + LOM | JCH | Procurement potentiel |

### 📋 En attente
| Action | Qui | Blocage |
|--------|-----|---------|
| Test harness caméra | Forge+Nova | Images IR Belgique |
| Config Docker RPi | Forge+Araignée | RPi disponible ? |
| Migration InsectNet M5→M1 | Clio+Musaraigne | Accès rsync M1 |
| Traitement notes_apple (54) | Dobby | Session dédiée |
| Traitement email_imports | Pie | Session dédiée |
