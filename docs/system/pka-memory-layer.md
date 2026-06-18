# PKA Memory Layer — Architecture

> Inspiré par Databricks « Memory Scaling for AI Agents » (avril 2026)
> Dernière mise à jour : 2026-06-17 — v1

---

## Principe fondateur

**La mémoire est le différenciateur de PKA, pas le modèle.**

Un LLM plus petit avec une mémoire riche surpasse un LLM plus gros sans mémoire. Les connaissances du domaine, les préférences de JCH, les patterns opérationnels et les décisions accumulées ne se trouvent dans aucun modèle fondamental — ils sont uniques à ce déploiement.

**Memory Scaling** = les performances de [[Dobby]] s'améliorent avec la quantité d'expérience accumulée (sessions, feedback, décisions, contexte métier).

---

## Architecture actuelle (as-is)

```
┌─────────────────────────────────────────────────┐
│                  Dobby 🦉                        │
│         (lit manuellement les sources)           │
└──────────┬──────────┬──────────┬────────────────┘
           │          │          │
     ┌─────▼──┐  ┌────▼───┐  ┌──▼──────────┐
     │MEMORY.md│  │team.db │  │graphify-out/ │
     │ (191 ln)│  │(24 tbl)│  │ (JSON+HTML)  │
     └─────────┘  └────────┘  └──────────────┘
           │          │          │
     ┌─────▼──┐  ┌────▼───┐  ┌──▼──────────┐
     │ wiki/  │  │file_idx│  │   scripts/   │
     │(vault) │  │(DB tbl)│  │(outils_idx)  │
     └────────┘  └────────┘  └──────────────┘
```

**Problèmes :**
- MEMORY.md est un goulot manuel (191 lignes, curation humaine)
- Pas d'extraction automatique des sessions (les JSON sont jetés)
- Pas de feedback loop sur [[Dobby]] lui-même
- La recherche est non unifiée ([[Dobby]] lit les sources une par une)
- Pas de scoring de qualité/fraîcheur des entrées mémoire
- Pas de déduplication ni détection d'obsolescence

---

## Architecture cible (to-be)

```
┌──────────────────────────────────────────────────────────┐
│                     Dobby 🦉                              │
│            (consomme l'API mémoire unifiée)               │
└────────────────────┬─────────────────────────────────────┘
                     │
         ┌───────────▼───────────┐
         │   PKA Memory API      │  ← pka_retrieve.py
         │  (recherche unifiée)   │
         └──┬──────┬──────┬──────┘
            │      │      │
    ┌───────▼─┐ ┌──▼───┐ ┌▼────────┐
    │team.db  │ │graph │ │file_idx  │
    │(source) │ │-ify  │ │+ vault   │
    └────┬────┘ └──────┘ └──────────┘
         │
    ┌────▼──────────────────────────┐
    │     Pipeline mémoire          │
    │                               │
    │  ┌─────────────────────────┐  │
    │  │ Session Extractor       │  │  ← post-session hook
    │  │ (JSON → knowledge+)     │  │
    │  └─────────────────────────┘  │
    │  ┌─────────────────────────┐  │
    │  │ Feedback Collector      │  │  ← dobby_feedback table
    │  │ (corrections → patterns)│  │
    │  └─────────────────────────┘  │
    │  ┌─────────────────────────┐  │
    │  │ Memory Curator          │  │  ← Corbeau
    │  │ (score, dedup, stale)   │  │
    │  └─────────────────────────┘  │
    │  ┌─────────────────────────┐  │
    │  │ MEMORY.md Generator     │  │  ← régénération auto
    │  │ (DB → markdown lisible) │  │
    │  └─────────────────────────┘  │
    └───────────────────────────────┘
```

---

## Composants

### 1. Session Extractor — `scripts/pka_session_extract.py`
**Statut :** SPEC (à construire)

Extrait automatiquement d'un JSON de session DeepSeek TUI :
- **Décisions** prises → `knowledge` (type: decision)
- **Faits** appris → `knowledge` (type: fact)
- **Préférences** exprimées par JCH → `knowledge` (type: preference)
- **Échecs** / blocages → `retro_patterns` (type: blocker)
- **Briefs** émis vers spécialistes → `knowledge` (type: brief)

Fonctionne en mode post-session hook (appelé après `/save`) ou en batch.

### 2. Feedback Loop — `dobby_feedback` table
**Statut :** À créer (schéma ci-dessous)

Capture chaque correction/déviation de JCH :
- Quand JCH dit « non, fais plutôt X »
- Quand JCH ignore une suggestion
- Quand JCH valide explicitement (👍)

Alimente `retro_patterns` pour ajuster le comportement futur.

```sql
CREATE TABLE dobby_feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT,
    feedback_type TEXT NOT NULL,  -- correction, preference, rejection, acceptance
    context TEXT,                  -- ce que Dobby était en train de faire
    dobby_action TEXT,            -- ce que Dobby a dit/fait
    user_response TEXT,           -- la réponse de JCH
    project_key TEXT,
    created_at TEXT DEFAULT (datetime('now')),
    incorporated INTEGER DEFAULT 0  -- 1 si intégré dans retro_patterns
);
```

### 3. Unified Retrieval — `scripts/pka_retrieve.py`
**Statut :** SPEC (à construire)

Point d'entrée unique pour la recherche PKA. Traduit une question en langage naturel en requêtes sur :
- `team.db` → SQL ([[knowledge]], journal, ideas, [[decisions]])
- `graphify-out/` → `graphify query` (traversal de graphe)
- `file_index` → recherche par nom de fichier
- `MEMORY.md` + `wiki/` → grep sémantique

Retourne un ensemble consolidé, dédupliqué, ranké par pertinence.

### 4. MEMORY.md Generator — `scripts/pka_generate_memory.py`
**Statut :** SPEC (à construire)

Régénère MEMORY.md à partir de `team.db` :
- Profil JCH → table `members` (JCH entry)
- Projets actifs → `knowledge` (type: project_status)
- Décisions → `knowledge` (type: decision, filtré 30 jours)
- Accès techniques → `knowledge` (type: access_info)
- Échecs → `retro_patterns` (type: blocker, status: ouvert)

Le fichier reste lisible par des humains et par des LLM non-PKA, mais sa source de vérité est la DB.

### 5. Memory Curator — attribué à [[Corbeau]]
**Statut :** Extension de rôle existant

[[Corbeau]] est déjà Knowledge Curator. Extension de ses responsabilités :
- **Scoring** : attribuer un score de qualité/fraîcheur aux entrées `knowledge`
- **Déduplication** : détecter les entrées redondantes
- **Obsolescence** : flagger les entrées périmées (>90 jours sans mise à jour)
- **Contradiction** : détecter les entrées qui se contredisent

### 6. Mémoire procédurale dynamique
**Statut :** ✅ Implémenté dans `pka_session_extract.py`

Quand `dobby_feedback` accumule ≥3 corrections de JCH partageant des mots-clés communs, le système génère automatiquement une entrée `knowledge.type='procedure'` et marque les feedbacks comme incorporés.

Exemple : si JCH corrige 3 fois des problèmes de permissions → règle « Toujours vérifier les permissions 0600 sur les fichiers _local/ ».

### 7. Zettelkasten Linking
**Statut :** ✅ Implémenté dans `pka_session_extract.py`

Après chaque extraction de session, les nouvelles entrées `knowledge` sont automatiquement reliées aux entrées existantes par similarité textuelle (Jaccard ≥3 mots communs). Les liens sont stockés dans `knowledge_links` avec une relation de type `related:mots-clés`.

Inspiré de A-MEM (NeurIPS 2025) — mémoire agentique avec linking dynamique et évolution continue.

---

## Roadmap

| Phase | Composant | Effort | Impact | Dépendances |
|-------|-----------|--------|--------|-------------|
| **P1** | `dobby_feedback` table | 30 min | Moyen | Aucune |
| **P1** | Memory Layer spec (ce document) | ✅ Fait | — | — |
| **P1** | Mémoire procédurale dynamique | ✅ Fait | Élevé | `dobby_feedback` |
| **P1** | Zettelkasten linking | ✅ Fait | Élevé | `knowledge_links` |
| **P2** | Session Extractor v0 | ✅ Fait | Élevé | Accès JSON sessions |
| **P2** | `pka_retrieve.py` v0 | ✅ Fait | Élevé | [[graphify]] CLI |
| **P3** | MEMORY.md Generator | ✅ Fait | Moyen | Session Extractor |
| **P3** | [[Corbeau]] Memory Curator | ✅ Fait | Moyen | Extension rôle |

---

## Métriques de succès

- **Couverture mémoire** : % des sessions qui produisent des extractions
- **Feedback incorporé** : % du feedback JCH intégré dans les patterns
- **Temps de recherche** : temps moyen pour répondre à une question cross-source
- **Fraîcheur MEMORY.md** : âge max des entrées dans MEMORY.md
- **Dédoublonnage** : nombre d'entrées [[knowledge]] sans doublon

---

## Références

- Databricks — « Mise à l'échelle de la mémoire pour les agents d'IA » (avril 2026)
- `MEMORY.md` — section « Règles de comportement [[Dobby]] »
- `scripts/dobby_retro.py` — extraction batch existante
- `TEAM/team.db` — tables `knowledge`, `retro_patterns`, `retro_sessions`, `memory_log`
- `TEAM/corbeau.md` — Knowledge Curator
