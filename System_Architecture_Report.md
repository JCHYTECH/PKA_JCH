---
date: 2026-05-29
type: architecture-report
status: validated
owner: "[[Dobby]]"
authors: "[[Castor]], [[Forge]]"
project: "[[01_AI_IT_TOOLS]]"
phase: "Pilote 2 — Architecture système"
source:
  - "[[Local_Infrastructure_Setup]]"
  - "[[Persistent_Memory_Architecture]]"
  - "[[Workflow_Orchestration]]"
---

# System Architecture Report — PKA_JCH

## Position

Ce document est le livrable formel du **Pilote 2 — Architecture système**.

Il consolide les décisions d'infrastructure prises lors des Phases 3-5 et documente l'état réel du système au 2026-05-29.

---

## 1. Infrastructure locale — état validé

| Composant | Version | État |
|-----------|---------|------|
| Git | `2.50.1` | ✅ |
| Python | `3.13.13` | ✅ |
| Docker Desktop | `29.4.3` | ✅ |
| VS Code | `1.121.0 arm64` | ✅ |
| Tailscale | `1.98.2` | ✅ |
| Ollama | `127.0.0.1:11434` | ✅ actif local |

Référence complète : [[Local_Infrastructure_Setup]]

---

## 2. Décisions d'infrastructure — définitives

| Technologie | Décision | Condition de réouverture |
|-------------|----------|--------------------------|
| PostgreSQL | ❌ Non déployé — SQLite suffisant | Jamais pour PKA mono-user |
| Redis | ❌ Non déployé — pas d'agents concurrents | Si agents persistants multiples (Phase 6+) |
| Qdrant | 🟡 Différé | `knowledge` ≥ 100 entrées + besoin sémantique concret |
| n8n | 🟡 Différé | Workflow ≥3 services externes avec logique conditionnelle |
| VPS | 🟡 Non adressé | Si besoin de disponibilité 24/7 ou collaboration externe |

Références : [[Persistent_Memory_Architecture]], [[Workflow_Orchestration]]

---

## 3. Conteneurs Docker actifs

| Service | Ports | Règle |
|---------|-------|-------|
| Plane (proxy, API, web, workers) | `127.0.0.1:8088`, `127.0.0.1:4443` | Local-only — composants internes non réutilisables |
| Ollama | `127.0.0.1:11434` | Local-only |

Règle ferme : les PostgreSQL et Redis internes de Plane ne servent pas de socle Hermes.

---

## 4. Base de données — `TEAM/team.db`

### État du schéma

| Version | Date | Description |
|---------|------|-------------|
| v1 | 2026-04-29 | Initial : members, responsibilities, hiring_pipeline, inbox |
| v2 | 2026-04-29 | Journal, contacts, file_index |
| v3 | 2026-04-29 | Knowledge, knowledge_links, ideas, bookmarks, goals, interactions, follow_ups |
| v4 | 2026-04-29 | Consolidation : CHECK constraints, indexes, tables_owned |
| v5 | 2026-05-28 | Migration inbox : deliverable_path, delivered_at, validated_at, statuts étendus |
| v6 | 2026-05-29 | Extension memory_log + skills : event_type, body, confidence, scope, model… |
| v7 | 2026-05-29 | Drop table vide `file_index_legacy_2026_05_16` ; 5 nouveaux indexes |

### Comptages au 2026-05-29

| Table | Lignes |
|-------|--------|
| `members` | 28 |
| `file_index` | 718 |
| `inbox` | 238 |
| `contacts` | 334 |
| `knowledge` | 19 |
| `knowledge_links` | 15 |
| `skills` | 10 |
| `memory_log` | 16 |
| `journal` | 13 |
| `ideas` | 3 |

### Intégrité

- Orphelins `knowledge_links` : **0**
- Foreign keys déclarées sur `knowledge_links` (from_id, to_id → knowledge.id)
- FK enforcement activé sur : `pka_memory_log.py`, `skill_write.py`
- FK enforcement à activer sur les autres scripts au fil des modifications

### Tables à surveiller

| Table | Statut |
|-------|--------|
| `file_index_legacy_2026_05_16_scope2` | 3272 lignes — backup 2026-05-16, à valider pour suppression par JCH |
| `bookmarks` | 0 lignes — table présente, non alimentée |
| `goals` | 0 lignes — table présente, non alimentée |

---

## 5. Indexes actifs

24 indexes sur les tables principales. Ajouts v7 :
- `idx_knowledge_tags` — recherche par tags
- `idx_skills_trigger` — lookup skills par pattern
- `idx_memory_log_event` — filtrage par type d'événement
- `idx_inbox_created` — tri chronologique inbox
- `idx_inbox_to` — filtrage par destinataire + statut

---

## 6. Règles de backup

| Élément | Règle |
|---------|-------|
| `TEAM/team.db` | Backup SQLite quotidien 08h00 via cron → `TEAM/backups/team_YYYY-MM-DD_HHMM.db` |
| Permissions | `0600` sur chaque backup |
| Rétention | 30 jours |
| Intégrité | `PRAGMA integrity_check` à chaque backup |
| Restauration | Validation humaine obligatoire — cf. [[TEAM/RESTORE_TEAM_DB]] |
| Hors-machine | Non encore adressé — à traiter en Phase 6 |

---

## 7. Monitoring

- Toutes les exécutions automatisées (cron, /save) écrivent dans `memory_log`
- Endpoint `/api/automation` expose les 20 dernières entrées
- Dashboard `hub.html` affiche le bloc "Dernières exécutions"
- Alertes Telegram sur échec : différées (seuil Phase 5b non atteint)

---

## 8. Points ouverts

| Sujet | Priorité | Décision |
|-------|----------|----------|
| Suppression `file_index_legacy_2026_05_16_scope2` | Basse | Validation JCH requise |
| FK enforcement sur les 24 autres scripts | Basse | Au fil des modifications, pas en masse |
| Backup hors-machine | Moyenne | Phase 6 ou maintenance runtime |
| VPS | Basse | Non justifié à ce stade |

---

## Voir aussi

- [[Local_Infrastructure_Setup]]
- [[Persistent_Memory_Architecture]]
- [[Workflow_Orchestration]]
- [[TEAM/RESTORE_TEAM_DB]]
- [[RUNBOOK_PKA_MACBOOK]]
- [[Dobby]]
- [[Castor]]
- [[Forge]]
