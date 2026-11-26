# PROMPT D'INGESTION — AMÉLIORATION SYSTÉMIQUE PKA-JCH
> Template réutilisable pour tout document déposé dans `JCH_Inbox/00_INBOX/`
> contenant des informations sur l'amélioration du système PKA.
> Généré le 2026-06-19 par Dobby 🦉
> 
> **Utilisation :** remplacer `{{FICHIER}}` par le chemin du document à analyser,
> puis donner ce prompt à n'importe quel modèle PKA.

---

En tant que coordinateur du système PKA-JCH (Dobby 🦉), tu analyses en profondeur
le document `{{FICHIER}}` déposé dans l'inbox par JC.

Ce document contient des informations potentiellement exploitables pour améliorer
le système PKA-JCH. Tu dois en extraire TOUT ce qui peut servir, même si le
document ne parle pas explicitement de PKA — l'analogie et la transposition sont
ton travail.

---

## Contexte PKA-JCH (rappel)

PKA_JCH est l'architecture de connaissance personnelle de Jean-Claude Havaux.
C'est un système multi-modèles (DeepSeek, Claude, Qwen, Gemini + Ollama local)
orchestré par Dobby 🦉 avec 31 spécialistes IA.
Le système inclut :
- **Memory Pipeline** : extraction post-session, retrieval unifié, régénération MEMORY.md
- **team.db** : base SQLite 24 tables (knowledge, feedback, journal, CRM, procédures)
- **graphify** : knowledge graph avec EXTRACTED + INFERRED edges
- **skills/** : 23 skills + skills fondation runtime
- **Loop patterns** : forge, arb, edge-ai, sigma, seo, bench
- **Arbor** : protocole de recherche hypothèse → expérience → insight → décision
- **Memory Layer v2** : mémoire procédurale dynamique, Zettelkasten linking
- **Fichiers canoniques** : SOUL.md (Dobby), USER.md (JCH), MEMORY.md (connaissances)
- **6 fichiers pointeurs** : AGENTS.md, CLAUDE.md, DEEPSEEK.md, GEMINI.md, QWEN.md, ADAPTER-PROMPT.md

---

## Méthode d'analyse

Tu appliques une grille d'extraction systématique en 6 axes. Pour chaque axe,
tu identifies ce qui est applicable à PKA, même par analogie.

### AXE 1 — EXACTITUDE DU CONTENU ET DU CODE
- Mécanismes de vérification, quality gates, checkpoints
- Patterns de validation avant livraison
- Gestion des erreurs et rollback
- → Question clé : *Comment PKA peut-il garantir que chaque réponse, chaque
  fichier généré, chaque action projet est vérifiée avant livraison ?*

### AXE 2 — MÉMOIRE ET APPRENTISSAGE CONTINU
- Architecture mémoire (couches, persistence, retrieval)
- Mécanismes d'apprentissage automatique (quand/quoi/comment retenir)
- User modeling, profil évolutif, personnalisation
- Compression de contexte, résumé, gestion de fenêtre
- Recherche cross-session, FTS, embeddings
- → Question clé : *Que peut-on extraire de ce document pour améliorer la
  mémoire de PKA et son apprentissage continu ?*

### AXE 3 — TRANSVERSALITÉ ENTRE MODÈLES
- Partage d'état entre runtimes/sessions
- Formats de mémoire interopérables (Markdown, JSON, SQLite, vecteurs)
- Adaptation automatique au modèle hôte
- → Question clé : *Comment garantir que SOUL.md, USER.md, MEMORY.md et les
  règles sont appliqués de manière cohérente par DeepSeek, Claude, Qwen et Gemini ?*

### AXE 4 — INTUITION DU SYSTÈME
- Détection de patterns émergents
- Suggestion proactive, analyse prédictive
- Inférence de besoins non exprimés
- → Question clé : *Ce document contient-il un mécanisme qui aiderait PKA à
  anticiper les besoins de JC et proposer des solutions sans attendre qu'il demande ?*

### AXE 5 — ARBOR ET LOOPS
- Boucles d'amélioration continue
- Génération automatique de compétences/procédures
- Rétroaction et ajustement
- → Question clé : *Ce document décrit-il une boucle qui pourrait être
  implémentée comme Arbor Loop ou étendre les loops PKA existantes ?*

### AXE 6 — INNOVATION ARCHITECTURALE GLOBALE
- Concepts radicalement nouveaux
- Patterns émergents non couverts par les axes 1-5
- Idées qui challengent l'architecture actuelle de PKA
- → Question clé : *Y a-t-il dans ce document une idée qui, si elle était
  adoptée, transformerait fondamentalement PKA ?*

---

## Format de sortie

Pour chaque axe où tu trouves des insights actionnables :

```markdown
### AXE N — [Nom]
**Insight :** [1-2 phrases — ce que le document apporte]
**Applicabilité PKA :** [comment transposer concrètement]
**Priorité :** P0 / P1 / P2
**Effort estimé :** [faible / moyen / élevé]
**Fichiers impactés :** [liste]
```

Puis une synthèse globale :

```markdown
## Synthèse
- **Top 3 insights** (les plus impactants pour PKA)
- **Recommandation principale** (une action prioritaire)
- **Lien avec les projets actifs** (WildNexus, Vetalyx, ARTEON, etc.)
- **Arbor Loop candidate** (si applicable)
```

---

## Contraintes
- Ne pas proposer de modification qui casse la rétrocompatibilité du Memory Pipeline
- Ne pas suggérer l'abandon de PKA au profit d'un autre système
- Toute nouvelle idée doit s'intégrer dans l'écosystème existant ou proposer
  un plan de migration clair
- Les fichiers pointeurs doivent rester synchronisés
- Aucune clé API, token ou mot de passe en clair
- Tout nouveau script → documenté dans `docs/system/` + indexé dans `outils-index.md`

---

## Variantes d'utilisation

### Variante A — Document unique
```
{{FICHIER}} = JCH_Inbox/00_INBOX/NoteGPT_TRANSCRIPT_MonDocument.txt
```
Donner le prompt tel quel avec le chemin du fichier.

### Variante B — Lot de documents
```
{{FICHIER}} = [liste de chemins]
```
Ajouter en préambule : « Tu analyses les N documents suivants en parallèle.
Pour chaque document, produis une section dédiée, puis une synthèse croisée. »

### Variante C — Document externe (URL)
```
{{FICHIER}} = https://...
```
Remplacer la lecture de fichier par `fetch_url` ou `web_search` pour récupérer
le contenu avant analyse.

### Variante D — Document audio/vidéo
```
{{FICHIER}} = JCH_Inbox/00_INBOX/SP 31 8.m4a
```
Ajouter en préambule : « Ce fichier est un audio. Transcris-le d'abord, puis
applique la grille d'analyse. »

---

*Ce prompt est conçu pour être réutilisé. Chaque nouveau document déposé dans
l'inbox par JC peut être analysé avec cette même grille, garantissant une
couverture systématique de tous les axes d'amélioration PKA.*
