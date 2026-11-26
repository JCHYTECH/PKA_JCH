# FTS5 Sessions — Design Spec
> Recherche full-text cross-session dans l'historique PKA.
> Inspiré de FTS5 + LLM summarization d'Hermes Agent.
> Version 0.1 — 2026-06-19

---

## Concept

Indexer les sessions JSON PKA dans une table SQLite FTS5 pour permettre
des recherches comme « qu'est-ce qu'on a décidé sur le budget WildNexus en mars ? »
ou « dans quelle session a-t-on parlé du M1 headless ? ».

Hermes utilise FTS5 sur ses session transcripts + LLM summarization pour
répondre à ce type de requêtes. PKA a déjà `pka_retrieve.py` (team.db + graphify +
wiki) mais pas de recherche full-text dans les transcripts bruts.

---

## Architecture

```
┌────────────────────────────────────────────┐
│           FTS5 Session Index               │
├────────────────────────────────────────────┤
│  1. Collecte                                │
│     └─ session_*.json dans PKA_JCH/        │
│  2. Indexation                              │
│     └─ pka_fts_index.py → session_fts      │
│  3. Recherche                               │
│     └─ pka_retrieve.py (étendu) + FTS5     │
│  4. Summarization                           │
│     └─ LLM résume les résultats FTS5       │
└────────────────────────────────────────────┘
```

---

## Table team.db : `session_fts`

```sql
CREATE VIRTUAL TABLE IF NOT EXISTS session_fts USING fts5(
    session_id,
    date,
    model,
    project,
    content
);
```

Index partiel : seules les 50 dernières sessions ou sessions < 100 000 tokens.

---

## Script : `pka_fts_index.py`

Usage :
```bash
python3 scripts/pka_fts_index.py --all            # indexer toutes les sessions
python3 scripts/pka_fts_index.py --recent 50      # 50 dernières
python3 scripts/pka_fts_index.py --session abc123 # une session spécifique
```

Workflow :
1. Scanner `PKA_JCH/session_*.json`
2. Pour chaque session : extraire `session_id`, date, modèle, contenu texte
3. Insérer dans `session_fts`
4. Éviter les doublons (vérifier `session_id` existant)

---

## Recherche : extension de `pka_retrieve.py`

Ajouter un mode `--fts` :
```bash
python3 scripts/pka_retrieve.py --fts "budget WildNexus mars 2026"
```

Combine :
1. FTS5 sur `session_fts` → sessions pertinentes
2. `pka_retrieve.py` existant (team.db + graphify + wiki) → connaissances structurées
3. LLM summarization des résultats combinés

---

## Estimation

| Métrique | Valeur |
|----------|--------|
| Sessions existantes | ~20 sessions JSON |
| Tokens totaux | ~18,7M tokens |
| Taille index FTS5 estimée | ~5-10 MB |
| Temps d'indexation initial | ~2-5 minutes |
| Temps de recherche | < 1 seconde |

---

## Statut

- [ ] Table `session_fts` créée dans team.db
- [ ] Script `pka_fts_index.py` écrit
- [ ] `pka_retrieve.py` étendu avec mode `--fts`
- [ ] Intégré dans SOUL.md (capacité de recherche historique)

*Priorité : P1 — ce trimestre.*
