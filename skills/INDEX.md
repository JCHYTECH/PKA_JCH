# PKA Skills — Index transversal

**Emplacement canonique :** `PKA_JCH/skills/`  
**Dernière mise à jour :** 2026-06-17  
**Plateformes :** DeepSeek TUI, Codex CLI, Claude Code  
**Politique :** Les skills locaux (`skills/`) prennent priorité sur les skills fondation du runtime. Toute amélioration d'un skill fondation se fait via shadow local.

---

## Skills disponibles

| Skill | Trigger(s) | Description courte |
|-------|-----------|-------------------|
| **Orchestration** | | |
| [pka-session-start](pka-session-start/SKILL.md) | Automatique — début de session | Protocole démarrage Dobby : modèle, mémoire, inbox, confirmation |
| [pka-system-check](pka-system-check/SKILL.md) | "check pka", "system check", "nettoie les scories" | Health-check automatique : permissions, backups, pointers, drift |
| [pka-weekly-report](pka-weekly-report/SKILL.md) | "rapport hebdo", "weekly report", "bilan de la semaine" | Rapport hebdomadaire consolidé : équipe, projets, inbox, rétro |
| [pka-pointer-sync](pka-pointer-sync/SKILL.md) | "mets à jour les pointers", "l'équipe a changé" | Resynchroniser CLAUDE.md, AGENTS.md, GEMINI.md, DEEPSEEK.md |
| [pka-file-versioning](pka-file-versioning/SKILL.md) | Automatique — avant toute modif BOM/ADR/registre | Sauvegarder version précédente (cp ou git tag) |
| **Loops** | | |
| [forge-loop](forge-loop/SKILL.md) | "forge loop", "code loop", "auto-fix" | Boucle autonome code review avec quality gate ≥ 4/5 (Grep Loop + AutoResearch) |
| [wildnexus-benchmark-loop](wildnexus-benchmark-loop/SKILL.md) | "benchmark loop", "PPK2 loop", "optimise le firmware" | Boucle autonome firmware WildNexus contre benchmarks hardware (AutoResearch) |
| [edge-ai-loop](edge-ai-loop/SKILL.md) | "edge ai loop", "TinyML loop", "FOMO loop" | Boucle autonome TinyML — Musaraigne modèle → benchmark (AutoResearch) |
| [seo-loop](seo-loop/SKILL.md) | "seo loop", "optimise le SEO", "auto-optimize SEO" | Boucle autonome SEO — Trace contenu → audit → optimise (AutoResearch) |
| [sigma-loop](sigma-loop/SKILL.md) | "sigma loop", "backtest loop" | Boucle autonome validation financière — Sigma données → backtesting (AutoResearch) |
| [bench-loop](bench-loop/SKILL.md) | "bench loop", "test loop", "SOP loop" | Boucle autonome SOPs hardware — Fourmi suit SOP → mesure → commit |
| **Opérations** | | |
| [ingest](ingest/SKILL.md) | `/ingest`, traite automatiquement 00_INBOX | Router fichiers inbox → dossier projet, indexer dans file_index |
| [capture](capture/SKILL.md) | `/capture <texte>` | Transformer input en entrée knowledge structurée (team.db) |
| [brief](brief/SKILL.md) | `/brief <membre> <tâche>` | Générer brief de délégation avec PRIORITY et DEADLINE |
| [status](status/SKILL.md) | `/status`, `/status <membre>` | Tableau de bord des livrables en attente, détection tâches bloquées |
| **WildNexus** | | |
| [wildnexus-adr](wildnexus-adr/SKILL.md) | "crée un ADR", "passe l'ADR en accepté", "documente la décision" | Créer, mettre à jour ou valider un ADR WildNexus |
| [wildnexus-bom](wildnexus-bom/SKILL.md) | "génère le BOM", "mets à jour le budget", "shortlist achat" | Générer/mettre à jour le BOM WildNexus P0 en Excel multi-onglets |
| **Spécialistes** | | |
| [onboarding-specialiste](onboarding-specialiste/SKILL.md) | "recrute", "gap de compétence", "nouvel agent", "embauche" | Pipeline complet recrutement d'un spécialiste PKA |
| **Connaissances** | | |
| [obsidian-knowledge-graph](obsidian-knowledge-graph/SKILL.md) | "wikilink le vault", "dry-run Obsidian" | Inventaire Obsidian, dictionnaire, wikilinks |
| **Spécialisés** | | |
| [bioacoustics-qc-playbook](bioacoustics-qc-playbook/SKILL.md) | "bioacoustics QC", "segment triage", "spectrogram review" | Curation datasets bioacoustiques, QC spectrogrammes |
| [chronophotography-workflow](chronophotography-workflow.md) | "chronophotographie", "action overlay" | Images composites à partir de rafales (Action Overlay) |

---

## Skills externes (runtime — non modifiables)

Ces skills sont fournis par le runtime et ne peuvent pas être modifiés directement. Des shadows locaux existent pour les plus critiques. Voir `CACHE_SKILLS_IMPROVEMENTS.md` pour les améliorations documentées.

| Skill | Shadow local | Statut |
|-------|-------------|--------|
| `graphify` | — | Cross-ref documenté |
| `delegate` | — | Note modèle-agnostique documentée |
| `crm-update` | — | Acceptable en l'état |
| `find-skills` | — | Utilitaire runtime |
| `triage` | — | Usage rare |

---

## Ajouter un skill

1. Créer `skills/<nom>/SKILL.md` avec frontmatter `name`, `description`
2. Ajouter la ligne dans ce tableau
3. Le skill est automatiquement découvert par le runtime (priorité locale > fondation)
