---
date: 2026-05-29
type: architecture-evaluation
status: validated
owner: "[[Dobby]]"
author: "[[Atlas]]"
project: "[[01_AI_IT_TOOLS]]"
phase: "Phase 4 — Mémoire persistante"
source:
  - "[[Local_Infrastructure_Setup]]"
  - "[[AI_System_Blueprint]]"
  - "[[AI_Data_Governance]]"
  - "[[Runtime_Service_Register]]"
  - "[[Hermisation]]"
---

# Persistent Memory Architecture — PKA_JCH

## Position dans la [[Hermisation]]

Ce document est le livrable formel de la **Phase 4 — Mémoire persistante**.

Il évalue PostgreSQL, Redis et Qdrant au regard des besoins réels du système PKA_JCH, et définit l'architecture de mémoire à adopter.

> Règle de phase : aucune installation technique avant que ce document soit validé par JCH.

---

## 1. État de la mémoire actuelle

### Ce qui existe déjà

| Couche | Support | État |
|--------|---------|------|
| Mémoire session portable | `MEMORY.md` | Actif — chargé à chaque session |
| Mémoire relationnelle | `TEAM/team.db` (SQLite) | Actif — source de vérité |
| Mémoire connaissance | `team.db` → table `knowledge` (15 entrées) | Sous-utilisé |
| Liens entre connaissances | `team.db` → table `knowledge_links` (15 entrées) | Sous-utilisé |
| Mémoire procédurale | `team.db` → table `skills` (7 entrées) | Sous-utilisé |
| Mémoire événements | `team.db` → table `memory_log` | Existe, non alimenté |
| Index fichiers | `team.db` → table `file_index` (718 entrées) | Actif |
| Journal quotidien | `wiki/Daily/` | Actif via `/save` |
| Livrables équipe | `TEAM_Inbox/` | Actif |

### Ce qui manque

1. **La table `skills` est peu alimentée** (7 entrées) — `skill_write.py` existe mais n'est pas exécuté systématiquement après les tâches complexes.
2. **`memory_log` n'est pas utilisé** — la table existe, aucune écriture automatique.
3. **Aucune recherche sémantique** — trouver une décision passée ou une connaissance similaire exige de connaître les mots exacts.
4. **La sauvegarde de session** (`/save`) écrit dans `wiki/Daily/` mais le contenu n'est pas indexé ni requêtable.

---

## 2. Évaluation des technologies

### 2.1 PostgreSQL

**Besoin adressé :** base relationnelle robuste, concurrence, volumes élevés.

**Réalité PKA :**
- `TEAM/team.db` (SQLite) couvre l'intégralité des besoins relationnels actuels.
- Utilisateur unique, pas de concurrence d'écriture critique.
- Plane dispose déjà de son propre PostgreSQL interne Docker — à ne pas réutiliser (règle Phase 1).

**Verdict : ❌ Non justifié.**

SQLite est suffisant pour la taille et l'usage actuel. PostgreSQL n'apporterait aucun bénéfice concret et ajouterait un conteneur Docker supplémentaire à maintenir.

---

### 2.2 Redis

**Besoin adressé :** cache session, pub/sub entre agents, état partagé temps réel.

**Réalité PKA :**
- Pas d'agents concurrents en temps réel.
- Pas de besoin de pub/sub inter-processus.
- Plane dispose déjà de son propre Redis interne Docker — à ne pas réutiliser.
- Le problème que Redis résoudrait n'existe pas encore dans PKA.

**Verdict : ❌ Non justifié.**

À reconsidérer uniquement si des agents persistants multiples fonctionnent en parallèle (Phase 5+).

---

### 2.3 Qdrant (base vectorielle)

**Besoin adressé :** recherche sémantique sur les connaissances, décisions et notes — "trouve ce qui ressemble à X" sans connaître les mots exacts.

**Réalité PKA :**
- `knowledge` contient 15 entrées. La recherche vectorielle est pertinente à partir de ~100 entrées.
- Ollama est déjà actif en local sur `127.0.0.1:11434` — peut générer des embeddings sans API externe.
- Qdrant existe en version légère mono-conteneur Docker.
- Le projet `obsidian-knowledge-graph` travaille déjà sur l'indexation des notes — potentielle synergie.

**Verdict : 🟡 Pertinent, mais prématuré.**

Qdrant devient justifié quand `knowledge` dépasse 100 entrées **et** qu'une requête sémantique concrète ne peut pas être satisfaite par SQLite `LIKE` ou `FTS5`. Déclencher l'évaluation à ce seuil.

---

## 3. Architecture retenue — Phase 4a (maintenant)

### Principe

> Aucune nouvelle infrastructure. Renforcer ce qui existe.

La mémoire persistante de PKA repose déjà sur SQLite + fichiers Markdown. Le travail de Phase 4a consiste à **alimenter systématiquement les tables existantes** et à **rendre la mémoire procédurale active**.

### Actions Phase 4a

| Action | Support | Responsable |
|--------|---------|-------------|
| Alimenter `skills` après chaque tâche complexe (>3 étapes ou procédure réutilisable) | `team.db` → `skills` via `skill_write.py` | [[Dobby]] (automatique) |
| Activer `memory_log` — écrire les décisions structurelles, mandats importants, erreurs | `team.db` → `memory_log` | [[Dobby]] (systématique) |
| Enrichir `knowledge` — chaque livrable spécialiste contenant un fait réutilisable → [[Corbeau]] extrait et indexe | `team.db` → `knowledge` | [[Corbeau]] |
| Relier les entrées `knowledge` via `knowledge_links` | `team.db` → `knowledge_links` | [[Corbeau]] |
| Brancher `/save` sur `memory_log` — chaque sauvegarde de session écrit une entrée horodatée | `team.db` → `memory_log` | [[Forge]] (script) |

### Critère de passage Phase 4b

| Seuil | Condition |
|-------|-----------|
| `knowledge` ≥ 100 entrées | Évaluer Qdrant light |
| Besoin sémantique concret identifié | Justifier l'installation |
| `skills` ≥ 30 procédures actives | Évaluer un moteur de recommandation de skills |

---

## 4. Architecture Phase 4b (conditionnelle — Qdrant)

> À ne déployer que si les seuils ci-dessus sont atteints.

### Composants

| Composant | Rôle | Infrastructure |
|-----------|------|---------------|
| Qdrant light | Stockage et recherche vectorielle sur `knowledge` | 1 conteneur Docker isolé, port `127.0.0.1:6333` |
| Ollama (existant) | Génération des embeddings (ex. `nomic-embed-text`) | Déjà actif `127.0.0.1:11434` |
| Script d'indexation | Lit `knowledge` depuis SQLite, envoie embeddings à Qdrant | Python, [[Forge]] |

### Règles

- Qdrant est **read-only depuis les agents** — seul le script d'indexation écrit.
- `TEAM/team.db` reste la source de vérité — Qdrant est un index dérivé, reconstituable.
- Données vectorielles stockées localement, pas en cloud.
- Rollback : `docker stop qdrant && docker rm qdrant` — aucun effet sur `team.db`.

---

## 5. Ce que cette architecture ne fait pas

- Elle ne déploie pas d'agents persistants autonomes.
- Elle ne relie pas Hermes, n8n ou tout framework d'orchestration externe.
- Elle ne duplique pas les composants internes de Plane.
- Elle n'introduit pas de nouvelle couche réseau ou d'API publique.

---

## 6. Conditions d'entrée en Phase 5

1. Phase 4a complète : `skills` ≥ 15 entrées actives, `memory_log` alimenté, `knowledge` en croissance régulière.
2. `/save` branché sur `memory_log`.
3. Ce document validé par JCH.
4. `python3 scripts/pka_security_audit.py` GREEN.

---

## Voir aussi

- [[Local_Infrastructure_Setup]]
- [[AI_System_Blueprint]]
- [[AI_Data_Governance]]
- [[Runtime_Service_Register]]
- [[RUNBOOK_PKA_MACBOOK]]
- [[Hermisation]]
- [[Dobby]]
- [[Forge]]
- [[Castor]]
- [[Corbeau]]
- [[Atlas]]
