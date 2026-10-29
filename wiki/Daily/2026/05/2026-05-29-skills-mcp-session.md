---
date: 2026-05-29
tags: [daily, PKA, skills, MCP, session]
type: daily
status: active
---

# 2026-05-29 — Skills capitalisation + MCP setup

## Actions

- Corrigé system check RED : permissions `vault_maintenance.log` (0644→0600) + pointer drift régénéré via `generate_tool_pointers.py`
- Traité 3 fichiers inbox → `08_VETALYX/clinical/` (2 PDFs usability + 1 MD artefact supprimé)
- Audit efficacité hermisation : skills 11→32 entrées, DB integrity OK, skill_search opérationnel
- Capitalisé 21 nouveaux skills dans `team.db` couvrant : ingest, CRM, system check, Vetalyx, WildNexus (ADR/BOM/milestone/Plane/glossaire), photo (import/print), WildLens, KOL screening, logigrammes cliniques, design tree interview, to-prd, to-issues, revue architecture
- Corrigé ids 18-19 (ADR/BOM) : pointeurs Claude supprimés → procédures complètes auto-suffisantes (règle transversalité tous modèles)
- Étudié source aihero.dev/5-agent-skills : intégré `/grill-me` (id=29), `/to-prd` (id=30), `/to-issues` (id=31), `/improve-codebase-architecture` (id=32)
- Configuré 3 MCP dans `.mcp.json` : `pka-sqlite` (uvx mcp-server-sqlite → team.db), `pka-filesystem` (npx → vault), `pka-plane` (custom Python)
- Écrit `scripts/mcp_plane_server.py` : 5 outils (list_projects, list_issues, create_issue, update_issue_status, list_cycles)
- Configuré compte Plane local (`jc_havaux@yahoo.com`) + token API `PKA_PLANE_API_TOKEN` testé et validé sur 8 projets

## Décisions

- Règle skills : toutes les entrées `team.db/skills` doivent être auto-suffisantes, sans dépendance à un outil ou modèle spécifique (transversalité Claude/Gemini/DeepSeek/Codex)
- `.mcp.json` gitignored (chemins absolus locaux)
- Plane owner = `jc.havaux@gmail.com` — compte `jc_havaux@yahoo.com` ajouté comme Admin via Django shell

## Prochaines étapes

- Ajouter `export PKA_PLANE_API_TOKEN="plane_api_e509d3131e984ce5813c80d1c48a78e7"` dans `~/.zshrc`
- Redémarrer Claude Code → vérifier `/mcp` (3 serveurs actifs)
- Alimenter `knowledge` vers 100 entrées (seuil Qdrant)
- Câble USB-C PD pour undervoltage RPi5 → protocole 24h BirdNET

## Voir aussi

- [[RUNBOOK_PKA_MACBOOK]]
- [[Persistent_Memory_Architecture]]
- [[mcp_plane_server]]
