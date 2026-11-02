# Honcho PKA — Design Spec
> Modélisation utilisateur évolutive inspirée de Honcho (dialectic user modeling)
> et du pattern USER.md auto-apprenant d'Hermes Agent.
> Version 0.2 — 2026-06-19 — Pivot synchrone (décision JC)

---

## Concept

Honcho PKA est un protocole **synchrone** exécuté par Dobby en fin de session
significative. Dobby analyse le transcript de la session qui vient de se terminer,
détecte des patterns comportementaux, des préférences, et des angles morts, puis
met à jour `USER.md` automatiquement (avec validation Dobby → JC).

**Pourquoi synchrone plutôt qu'asynchrone :**
- Les résumés `memory_log` sont trop courts (100-200 chars) pour une analyse pertinente
- Dobby a le transcript complet en contexte — aucune perte d'information
- Plus simple, plus immédiat, pas de cron à maintenir
- Cohérent avec le pattern Hermes original (USER.md auto-apprenant)
- Décision JC : 2026-06-19 — choix B (synchrone)

---

## Architecture

```
┌──────────────────────────────────────────────────┐
│           Honcho PKA — Post-Session Protocol      │
├──────────────────────────────────────────────────┤
│  1. Détection                                      │
│     └─ Dobby identifie une session « significative »│
│        (≥ 5 échanges, décisions, ou /save)         │
│  2. Analyse                                        │
│     └─ Dobby analyse le transcript en contexte     │
│        → 5 catégories : preference, habit,         │
│        project_interest, technical, communication  │
│  3. Stockage                                       │
│     └─ INSERT dans user_model (team.db)            │
│  4. Proposition                                    │
│     └─ Dobby génère un diff USER.md si pertinent   │
│  5. Validation                                     │
│     └─ Dobby présente à JC → apply ou reject      │
│  6. Application                                    │
│     └─ Mise à jour USER.md + log décision          │
└──────────────────────────────────────────────────┘
```

---

## Déclencheurs

Honcho s'exécute automatiquement quand :
- `/save` est appelé (session explicitement sauvegardée)
- Une session atteint ≥ 8 échanges
- Une décision structurelle est prise (split de fichier, nouvelle règle, pivot)
- JC demande explicitement « honcho »

**Ne pas exécuter** sur les sessions triviales (1-2 échanges, lookup simple).

---

## Table team.db : `user_model`

```sql
CREATE TABLE IF NOT EXISTS user_model (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,        -- 'preference', 'habit', 'project_interest', 'technical', 'communication'
    insight TEXT NOT NULL,          -- le pattern détecté
    evidence TEXT,                  -- extraits de session qui supportent l'insight
    confidence REAL DEFAULT 0.5,   -- score 0-1
    source_session TEXT,            -- session_id ou NULL si multi-session
    status TEXT DEFAULT 'proposed', -- proposed | validated | rejected | applied
    validated_by TEXT,              -- 'dobby' ou 'jch'
    created_at TEXT DEFAULT (datetime('now')),
    updated_at TEXT DEFAULT (datetime('now'))
);
```

---

## Catégories d'analyse

| Catégorie | Exemples | Impact USER.md |
|-----------|----------|----------------|
| **preference** | « JC préfère les systèmes simples aux pipelines complexes » | Ajouté à « À retenir » |
| **habit** | « JC active Dobby par un simple 'dobby' et attend le résumé » | Ajouté à workflow |
| **project_interest** | « JC investit dans l'infrastructure PKA (AI_IT_TOOLS) » | Ajustement priorités |
| **technical** | « JC utilise maintenant DxO plus que Lightroom » | Mise à jour setup |
| **communication** | « JC est extrêmement concis, fait confiance à Dobby » | Ajustement ton Dobby |

---

## Seuils de confiance

| Confiance | Action |
|-----------|--------|
| ≥ 0.8 | Proposer diff USER.md automatiquement |
| 0.5–0.79 | Stocker dans `user_model`, proposer à JC seulement si récurrent |
| < 0.5 | Stocker mais ne pas proposer (attendre confirmation) |

---

## Script : `pka_honcho_analyze.py`

Le script existe en mode batch (analyse `memory_log` sur N jours) comme fallback
pour l'analyse rétrospective. Le mode principal est **synchrone** : Dobby analyse
en direct.

Usage batch (fallback) :
```bash
python3 scripts/pka_honcho_analyze.py --days 7 --dry-run
python3 scripts/pka_honcho_analyze.py --since 2026-06-12
```

---

## Exemple de sortie (mode synchrone)

```
=== Honcho PKA — Session 2026-06-19 ===

Insights détectés (4) :
  [communication] confidence 0.85 — JC extrêmement concis, répond par mots-clés
  [preference]    confidence 0.80 — JC préfère systèmes simples/synchrones
  [project_interest] confidence 0.75 — AI_IT_TOOLS toujours actif
  [habit]         confidence 0.90 — Activation par "dobby", attend résumé immédiat

USER.md diff proposé :
  + - Extrêmement concis — répond par mots-clés, fait confiance à Dobby pour décomposer
  + - Préfère les systèmes simples et synchrones aux pipelines asynchrones complexes
```

---

## État des lieux (2026-06-19)

| Composant | Statut |
|-----------|--------|
| Table `user_model` dans team.db | ✅ Créée, 4 insights stockés |
| Script `pka_honcho_analyze.py` | ✅ Batch OK, mode synchrone = Dobby direct |
| Protocole post-session dans SOUL.md | ✅ Règle ajoutée |
| Première exécution synchrone | ✅ 2026-06-19 — 4 insights |
| Intégration USER.md auto-update | ⏳ Proposition en attente validation JC |

*Priorité : P1 — actif.*
