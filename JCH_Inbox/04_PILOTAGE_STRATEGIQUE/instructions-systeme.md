# Instructions Système PKA-JCH — Tableau Consolidé
> Tous les mécanismes d'instruction, d'amélioration et de pilotage du système.
> Généré le 2026-06-19 par Dobby 🦉
> 
> **Lecture :** une ligne = une instruction. Activable par Dobby ou par JC.

---

## 1. Prompts d'amélioration systémique

| # | Nom | Fichier | Activation | Rôle |
|---|-----|---------|------------|------|
| P1 | Prompt Hermes → PKA | `04_PILOTAGE_STRATEGIQUE/prompt-hermes-amelioration-pka.md` | Donner le prompt à un LLM | Analyse ciblée de l'architecture Hermes pour PKA (5 axes, livrables P0/P1/P2) |
| P2 | Prompt ingestion universel | `04_PILOTAGE_STRATEGIQUE/prompt-ingestion-amelioration-systemique.md` | Remplacer `{{FICHIER}}` + donner au LLM | Grille 6 axes pour tout document d'amélioration — transcript, papier, URL, audio |

---

## 2. Skills d'amélioration système (skills/)

| # | Nom | Fichier | Déclencheur | Rôle |
|---|-----|---------|-------------|------|
| S1 | system-improvement-ingest | `skills/system-improvement-ingest/SKILL.md` | `/system-improvement-ingest`, « analyse ce document pour PKA » | Grille 6 axes — version skill du prompt P2 |
| S2 | arbor-research | `skills/arbor-research/SKILL.md` | « arbor loop », « recherche autonome », « hypothesis tree » | Protocole hypothèse → expérience → insight → décision |
| S3 | pka-system-check | `skills/pka-system-check/SKILL.md` | « check pka », « system check », « vérifie l'état du système » | Health-check automatique (permissions, backups, pointers, todo drift) |
| S4 | pka-session-start | `skills/pka-session-start/SKILL.md` | Automatique en début de session | Protocole démarrage : identité, mémoire, inbox, activation |
| S5 | pka-pointer-sync | `skills/pka-pointer-sync/SKILL.md` | « mets à jour les pointers », « synchronise les fichiers système » | Synchro 6 fichiers pointeurs après changement équipe/structure |
| S6 | pka-file-versioning | `skills/pka-file-versioning/SKILL.md` | Automatique avant modif BOM/ADR/registre/budget | Backup pré-édition fichiers itératifs |
---

## 3. Loop patterns (skills/)

| # | Nom | Fichier | Déclencheur | Rôle |
|---|-----|---------|-------------|------|
| L1 | forge-loop | `skills/forge-loop/SKILL.md` | « forge loop », « code loop », « auto-fix » | Code → review → score < 4/5 → auto-fix → repush |
| L2 | bench-loop | `skills/bench-loop/SKILL.md` | « bench loop », « test loop », « SOP loop » | Exécution autonome SOPs hardware → mesure → commit |
| L3 | edge-ai-loop | `skills/edge-ai-loop/SKILL.md` | « edge ai loop », « TinyML loop », « FOMO loop » | Optimisation modèles TinyML → benchmark → commit si meilleur |
| L4 | sigma-loop | `skills/sigma-loop/SKILL.md` | « sigma loop », « backtest loop » | Validation données financières → backtesting → ajustement modèle |
| L5 | seo-loop | `skills/seo-loop/SKILL.md` | « seo loop », « auto-optimize SEO » | Modification page → audit score → optimisation → re-audit |

---

## 4. Fichiers canoniques de règles comportementales

| # | Nom | Fichier | Chargement | Rôle |
|---|-----|---------|------------|------|
| R1 | SOUL.md | `SOUL.md` (racine) | Chaque session — lu en premier | Personnalité Dobby, règles de comportement, responsabilités |
| R2 | USER.md | `USER.md` (racine) | Chaque session — lu en deuxième | Profil JCH, setup technique, projets, préférences |
| R3 | MEMORY.md | `MEMORY.md` (racine) | Chaque session — lu en troisième | Connaissances accumulées, décisions, chronologie |
| R4 | ADAPTER-PROMPT.md | `ADAPTER-PROMPT.md` (racine) | Bootstrap LLM externe | Protocole d'activation PKA pour tout LLM, compliance check |
| R5 | AGENTS.md | `AGENTS.md` (racine) | Codex CLI — automatique | Pointer Codex : identité Dobby, source of truth, règles |
| R6 | CLAUDE.md | `CLAUDE.md` (racine) | Claude Code — automatique | Pointer Claude : overlay canonique + graphify + DuckDuckGo |
| R7 | DEEPSEEK.md | `DEEPSEEK.md` (racine) | DeepSeek — automatique | Pointer DeepSeek : identité, source of truth, règles |
| R8 | GEMINI.md | `GEMINI.md` (racine) | Gemini CLI — automatique | Pointer Gemini : identité, source of truth, règles |
| R9 | QWEN.md | `QWEN.md` (racine) | Qwen — automatique | Pointer Qwen : identité, source of truth, règles |
| R10 | TEAM/dobby.md | `TEAM/dobby.md` | Référence | Persona complet Dobby, responsabilités, DB stewardship |

---

## 5. Outils d'audit et d'amélioration (scripts/)

| # | Nom | Fichier | Usage | Rôle |
|---|-----|---------|-------|------|
| T1 | pka_system_check.py | `scripts/pka_system_check.py` | `python3 scripts/pka_system_check.py` | Health-check automatique : permissions, backups, pointers, structure |
| T2 | pka_session_extract.py | `scripts/pka_session_extract.py` | Post-session | Extraction décisions, faits, feedback → team.db |
| T3 | pka_retrieve.py | `scripts/pka_retrieve.py` | Recherche | Recherche unifiée multi-sources (DB, graph, wiki, MEMORY.md) |
| T4 | pka_generate_memory.py | `scripts/pka_generate_memory.py` | Régénération | Régénère MEMORY.md depuis team.db |
| T5 | pka_conflict_checker.py | `scripts/pka_conflict_checker.py` | Détection | Détecte contradictions entre spécialistes (OctoChains) |
| T6 | pka_pointer_sync.py | `scripts/pka_pointer_sync.py` | Synchronisation | Synchronise 6 fichiers pointeurs avec team.db |
| T7 | pka_vigilance.py | `scripts/pka_vigilance.py` | Surveillance | Détection de dérive entre DB et fichiers |
| T8 | pka_structure_check.py | `scripts/pka_structure_check.py` | Vérification | Vérifie la structure du workspace |
| T9 | pka_prompt_guard.py | `scripts/pka_prompt_guard.py` | Sécurité | Scanner prompt injection (score 0-100 + quarantaine) |
| T10 | pka_memory_log.py | `scripts/pka_memory_log.py` | Log | Log mémoire automatique dans SYBIL_JOURNAL |

---

## 6. Fichiers de pilotage stratégique (04_PILOTAGE_STRATEGIQUE/)

| # | Nom | Fichier | Rôle |
|---|-----|---------|------|
| D1 | Priorités actives | `priorites-actives.md` | Vue courte des priorités en cours |
| D2 | Roadmap 90 jours | `roadmap-90-jours.md` | Horizon tactique portefeuille |
| D3 | Arbitrages & décisions | `arbitrages-decisions.md` | Décisions de focus, stop, report |
| D4 | KPI portefeuille | `kpi-portefeuille.md` | Indicateurs transverses |
| D5 | Opportunités à suivre | `opportunites-a-suivre.md` | Pistes à surveiller |
| D6 | Risques & frottements | `risques-et-frottements.md` | Points de tension, obstacles |
| D7 | **État des projets** | `etat-projets.md` | Tableau de bord projets — statuts, blocages, échéances |
| D8 | **Matrice des modèles** | `matrice-modeles.md` | Quel modèle pour quelle tâche, coûts |
| D9 | **Décisions PKA** | `decisions-pka.md` | Registre des décisions structurelles transverses |

---

## Résumé — Tableau de bord unique

### Nouvelles capacités (Hermes → PKA, 2026-06-19)

| # | Capacité | Statut | Fichier |
|---|----------|--------|---------|
| N1 | Memory Nudge | ✅ Actif | `scripts/pka_memory_nudge.py` + règle SOUL.md |
| N2 | Alerte compression contexte | ✅ Actif | Règle SOUL.md |

| Catégorie | Nombre | Activation |
|-----------|--------|------------|
| **Prompts** | 2 | Manuel (donner au LLM) |
| **Skills système** | 6 | `/skill` ou mot-clé |
| **Loops** | 5 | `/skill` ou mot-clé |
| **Règles canoniques** | 10 | Automatique (session start) |
| **Outils audit** | 10 | `python3 scripts/...` |
| **Pilotage** | 9 | Lecture par Dobby |

**Total : 42 instructions système actives.**

---

*Ce tableau est le point d'entrée unique pour comprendre tous les mécanismes
d'instruction du système PKA-JCH. Toute nouvelle instruction (prompt, skill,
loop, règle, outil) doit être ajoutée ici.*