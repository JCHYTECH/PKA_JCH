# Wiki — Index

> Catalogue auto-maintenu du wiki PKA.  
> Dobby met à jour ce fichier à chaque session.  
> Dernière mise à jour : 2026-06-13  
> Pattern : LLM Wiki (Karpathy, 2026) — [[Knowledge/AI-Tools/LLM Wiki — Karpathy pattern|document source]]

---

## Architecture 3 couches

| Couche | Dossier | Rôle | Maintenance |
|--------|---------|------|-------------|
| **Raw** | `JCH_Inbox/`, `JCH_PRIVATE/` | Sources immuables — articles, PDFs, images | Manuelle (JCH) |
| **Wiki** | `wiki/` | Connaissances compilées, narratives, inter-connectées | LLM (Dobby) |
| **Schema** | `AGENTS.md`, `skills/`, `docs/system/` | Instructions pour le LLM — conventions, workflows | Dobby + JCH |

---

## Catégories du wiki

| # | Domaine | Chemin | Description | Pages |
|---|---------|--------|-------------|:-----:|
| 01 | 🤖 AI & Outils | `AI-Tools/` | Outils IA, glossaire, patterns LLM | 2 |
| 02 | 🗓️ Journal | `Daily/YYYY/MM/` | Notes quotidiennes — YYYY-MM-DD-slug.md | 121 |
| 03 | 📋 SOPs | `SOPs/` | Procédures pas-à-pas | 7 |
| 04 | 🔄 Workstreams | `Workstreams/` | Orchestrations récurrentes multi-spécialistes | 1 |
| 05 | 📐 Guidelines | `Guidelines/` | Référentiels statiques partagés | 4 |
| 06 | 📚 Knowledge | `Knowledge/` | Articles, références, documents fondateurs | 2 |
| — | 📋 Index | `index.md` | Ce fichier | 1 |
| — | 📝 Log | `log.md` | Journal opérationnel append-only | 1 |

---

## AI & Outils

- [[AI-Tools/glossary-ai|Glossaire IA — 50 termes]] — extrait de sAIpien (MIT Media Lab), cadre 6 piliers
- [[../Knowledge/AI-Tools/LLM Wiki — Karpathy pattern|LLM Wiki — Karpathy pattern]] — cadre fondateur pour bases de connaissance LLM

## SOPs

- [[SOPs/SOP-001-onboarding-nouveau-specialiste|SOP-001 — Onboarding nouveau spécialiste]]
- [[SOPs/SOP-005-checklist-terrain-bioacoustique|SOP-005 — Checklist Terrain Bioacoustique RPi 5]]
- [[SOPs/SOP-006-travail-obsidian-vscode-pka|SOP-006 — Travail Obsidian + VS Code dans PKA_JCH]]
- [[SOPs/SOP-007-test-terrain-birdnet-mobile-24h|SOP-007 — Test terrain BirdNET-Go mobile 24 h]]
- [[SOPs/SOP_OAUTH_ONBOARDING|SOP OAUTH — Onboarding OAuth]]
- [[SOPs/SOP_EMAIL_IMPORT_AND_CLASSIFICATION|SOP Email — Import et classification]]
- [[SOPs/pka-kanban-governance|PKA Kanban — Gouvernance]]

## Workstreams

- [[Workstreams/WS-001-journal-quotidien|WS-001 — Journal quotidien]]

## Guidelines

- [[Guidelines/GL-001-conventions-nommage|GL-001 — Conventions de nommage]]
- [[Guidelines/GL-002-skill-inventory|GL-002 — Skill Inventory and Runtime Map]]
- [[Guidelines/GL-003-obsidian-graph-project-view|GL-003 — Vue Graphe Obsidian projets uniquement]]
- [[Guidelines/GL-004-ergonomie-intervention-dobby|GL-004 — Ergonomie d'intervention Dobby]]

## Knowledge

- [[Knowledge/AI-Tools/LLM Wiki — Karpathy pattern|LLM Wiki — Karpathy pattern]] — cadre fondateur
- [[Knowledge/AI-Tools/glossary-ai|Glossaire IA — 50 termes]]

---

## Système & Infrastructure

- [[../JCH_Inbox/99_SYSTEM/thunderbolt-m1-m5-mode-emploi|Thunderbolt Bridge M1↔M5 — Mode d'emploi]] — réseau 40 Gb/s
- [[../docs/system/outils-index|Index central des outils PKA_JCH]] — scripts, skills, bin
- `AGENTS.md` — schema LLM (3 couches, identité, règles)
- `MEMORY.md` — mémoire accumulée, contexte JCH, décisions

---

## Navigation rapide

- **Dernières daily notes :** `Daily/2026/06/` (trié par date)
- **Log opérationnel :** `log.md` — `grep "^## \[" log.md | tail -10`
- **Sources brutes :** `JCH_Inbox/00_INBOX/` → `/ingest` pour traitement
- **Projets :** `JCH_Inbox/03_PROJECTS/`
- **Équipe :** `TEAM/ROSTER.md`
- **Santé du wiki :** `/lint` (contradictions, orphelins, pages périmées)

---

## Statistiques

- Daily notes : 128 (dernière : 2026-06-15 — intégration Zigbee ZBDongle-P V2 × HA Docker, bridge Python launchd)
- SOPs : 7 — Workstreams : 1 — Guidelines : 4
- Articles knowledge : 2 (AI-Tools)
- Log système : actif depuis 2026-05-03 (178+ entrées, format structuré depuis 2026-06-13)

*Mis à jour par Dobby à chaque session. Dernière mise à jour : 2026-06-15.*
