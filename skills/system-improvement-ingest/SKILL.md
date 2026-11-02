---
name: system-improvement-ingest
description: Analyse tout document (transcript, papier, article, URL, audio) pour en extraire des améliorations actionnables du système PKA-JCH. Grille systématique 6 axes : exactitude, mémoire, transversalité, intuition, Arbor/Loops, innovation globale. Déclencher sur "analyse ce document pour PKA", "que peut-on tirer de ce papier", "améliore le système avec", "applique la grille d'ingestion", "system improvement ingest".
---

# /system-improvement-ingest — Analyse de document pour amélioration PKA

Analyse en profondeur un document déposé par JC dans l'inbox et en extrait
tout insight exploitable pour améliorer le système PKA-JCH — même si le
document ne parle pas explicitement de PKA. L'analogie et la transposition
sont le cœur de cette skill.

> **Prompt externe :** une version statique de cette skill existe dans
> `JCH_Inbox/04_PILOTAGE_STRATEGIQUE/prompt-ingestion-amelioration-systemique.md`
> pour usage hors PKA (copier-coller dans un autre outil).

## Usage

```
/system-improvement-ingest <fichier>     # analyse un fichier de l'inbox
/system-improvement-ingest <url>         # fetch + analyse une URL
/system-improvement-ingest --batch f1 f2 # analyse parallèle de N fichiers
```

## Prérequis

Avant analyse, le fichier doit être scanné avec `pka_prompt_guard.py` :

```bash
python3 scripts/pka_prompt_guard.py scan <fichier> --json
```

Si le score est ≥ 70 → quarantaine. Sinon → analyse.

---

## Grille d'analyse — 6 axes

Pour chaque axe, Dobby identifie ce qui est applicable à PKA, même par analogie.
Un insight peut être extrait même si le document ne mentionne jamais PKA.

### AXE 1 — EXACTITUDE DU CONTENU ET DU CODE
- Mécanismes de vérification, quality gates, checkpoints, rollback
- Patterns de validation avant livraison
- Gestion des erreurs et fiabilité
- **Question clé :** *Comment PKA peut-il garantir que chaque réponse, chaque
  fichier généré, chaque action projet est vérifiée avant livraison ?*

### AXE 2 — MÉMOIRE ET APPRENTISSAGE CONTINU
- Architecture mémoire (couches, persistence, retrieval)
- Apprentissage automatique (quand/quoi/comment retenir)
- User modeling, profil évolutif, personnalisation
- Compression de contexte, résumé, gestion de fenêtre
- Recherche cross-session, FTS, embeddings
- **Question clé :** *Que peut-on extraire pour améliorer la mémoire de PKA
  et son apprentissage continu ?*

### AXE 3 — TRANSVERSALITÉ ENTRE MODÈLES
- Partage d'état entre runtimes/sessions
- Formats de mémoire interopérables (Markdown, JSON, SQLite, vecteurs)
- Adaptation automatique au modèle hôte (DeepSeek, Claude, Qwen, Gemini)
- **Question clé :** *Comment garantir que SOUL.md, USER.md, MEMORY.md et les
  règles sont appliqués de manière cohérente par tous les modèles ?*

### AXE 4 — INTUITION DU SYSTÈME
- Détection de patterns émergents dans les demandes de JC
- Suggestion proactive, analyse prédictive
- Inférence de besoins non exprimés
- **Question clé :** *Ce document contient-il un mécanisme qui aiderait PKA à
  anticiper les besoins de JC et proposer des solutions sans qu'il demande ?*

### AXE 5 — ARBOR ET LOOPS
- Boucles d'amélioration continue (forge, edge-ai, sigma, seo, bench)
- Génération automatique de compétences/procédures
- Rétroaction et ajustement
- **Question clé :** *Ce document décrit-il une boucle qui pourrait être
  implémentée comme Arbor Loop ou étendre les loops PKA existantes ?*

### AXE 6 — INNOVATION ARCHITECTURALE GLOBALE
- Concepts radicalement nouveaux, patterns émergents
- Idées qui challengent l'architecture actuelle de PKA
- Synergies inattendues entre projets (WildNexus, Vetalyx, ARTEON, etc.)
- **Question clé :** *Y a-t-il une idée qui transformerait fondamentalement PKA ?*

---

## Format de sortie

Pour chaque axe avec insights actionnables :

```markdown
### AXE N — [Nom]
**Insight :** [1-2 phrases]
**Applicabilité PKA :** [transposition concrète]
**Priorité :** P0 / P1 / P2
**Effort estimé :** faible / moyen / élevé
**Fichiers impactés :** [liste]
```

Puis une synthèse :

```markdown
## Synthèse
- **Top 3 insights**
- **Recommandation principale** (action prioritaire)
- **Lien avec les projets actifs**
- **Arbor Loop candidate** (si applicable)
- **Fichier de synthèse :** TEAM_Inbox/YYYY-MM-DD_dobby_system-improvement_[sujet].md
```

---

## Workflow

1. **Scan sécurité** — `pka_prompt_guard.py scan <fichier>`
2. **Charger contexte PKA** — relire SOUL.md, USER.md, MEMORY.md (aperçu)
3. **Analyser le document** — appliquer la grille 6 axes
4. **Déléguer si nécessaire** — axe 1→Forge, axe 2→Corbeau, axe 5→Arbor skill, etc.
5. **Produire la synthèse** — format standard ci-dessus
6. **Sauvegarder** — `TEAM_Inbox/YYYY-MM-DD_dobby_system-improvement_[sujet].md`
7. **Mettre à jour MEMORY.md** — ajouter une entrée dans la chronologie
8. **Proposer les P0** — si des actions P0 émergent, les ajouter au kanban

---

## Contraintes

- Ne pas casser la rétrocompatibilité du Memory Pipeline
- Ne pas suggérer l'abandon de PKA au profit d'un autre système
- Toute nouvelle idée doit s'intégrer dans l'écosystème existant
- Les fichiers pointeurs (6 fichiers) doivent rester synchronisés
- Aucune clé API, token ou mot de passe en clair
- Nouveau script → `docs/system/` + `outils-index.md`

---

## Variantes

| Variante | Déclencheur | Particularité |
|----------|-------------|---------------|
| **Document unique** | `/system-improvement-ingest f.txt` | Grille standard |
| **Batch** | `/system-improvement-ingest --batch f1 f2 f3` | Analyse parallèle + synthèse croisée |
| **URL** | `/system-improvement-ingest https://...` | Fetch d'abord, puis grille |
| **Audio** | `/system-improvement-ingest audio.m4a` | Transcription d'abord, puis grille |

---

*Skill inspirée du pattern Hermes (soul.md/user.md/memory.md) et de la boucle
Arbor (hypothèse → expérience → insight → décision). Conçue pour être le point
d'entrée unique de tout document d'amélioration système déposé par JC.*
