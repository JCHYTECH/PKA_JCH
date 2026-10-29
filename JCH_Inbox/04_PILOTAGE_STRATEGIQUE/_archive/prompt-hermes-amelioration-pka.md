# PROMPT D'AMÉLIORATION SYSTÉMIQUE PKA-JCH
> Inspiré par l'analyse de l'architecture Hermes Agent (NousResearch)
> Généré le 2026-06-19 par Dobby 🦉 — DeepSeek TUI v0.8.39
> Sources : transcript vidéo + docs hermes-agent.nousresearch.com + repo GitHub (197k★, v0.15.2)

---

En tant que coordinateur du système PKA-JCH (Dobby 🦉), tu analyses en profondeur l'architecture d'Hermes Agent — transcript complet fourni — et tu détermines les informations exploitables pour améliorer notre système sur 5 axes :

## 1. EXACTITUDE DU CONTENU ET DU CODE
- Comment garantir que chaque réponse, chaque fichier généré, chaque action projet est vérifiée avant livraison ?
- Quels mécanismes de quality gate manquent à PKA ?
- Comment Hermes gère-t-il ses checkpoints automatiques avant modification de fichier — et comment adapter ce pattern à PKA ?

## 2. MÉMOIRE ET APPRENTISSAGE CONTINU
- Analyser les 5 couches mémoire d'Hermes (session transcripts FTS5, MEMORY.md, USER.md auto-apprenant, SOUL.md, Honcho dialectique)
- Comparer avec PKA : team.db (24 tables), Memory Pipeline (session_extract, retrieve, generate_memory, conflict_checker, pointer_sync), graphify, wiki, MEMORY.md monolithique
- Proposer une migration de MEMORY.md monolithique → architecture SOUL.md / USER.md / MEMORY.md séparée
- Implémenter un « memory nudge » périodique (post-réponse) qui complète l'extraction post-session actuelle
- Ajouter FTS5 sur les transcripts de session JSON pour recherche cross-session avec LLM summarization

## 3. TRANSVERSALITÉ ENTRE MODÈLES LOCAUX ET EXTERNES
- PKA utilise 4+ runtimes (DeepSeek, Claude, Qwen, Gemini) + Ollama
- Hermes est mono-runtime mais multi-provider (OpenRouter 200+ modèles, Nous Portal, NVIDIA NIM, etc.)
- Comment garantir que la mémoire, les règles comportementales, les skills et les préférences utilisateur sont partagées de manière cohérente entre tous les modèles PKA ?
- La compression de contexte automatique d'Hermes (char/4 puis usage.tokens, seuil 50% configurable) est-elle adaptable au contexte multi-modèle de PKA ?
- Faut-il un « adapter prompt » unique (ADAPTER-PROMPT.md) enrichi avec les patterns de soul.md Hermes ?

## 4. INTUITION DU SYSTÈME — PROPOSER DES SOLUTIONS À JC
- Hermes utilise Honcho (dialectic user modeling) pour raisonner sur les conversations et construire un modèle évolutif de l'utilisateur
- PKA a un profil JCH statique dans MEMORY.md
- Concevoir un « Honcho PKA » : processus asynchrone qui analyse les conversations récentes de JC → déduit patterns, préférences, angles morts → propose proactivement des pistes d'action
- Activer le mécanisme de mémoire procédurale dynamique existant (≥3 feedbacks partagés → procédure) pour détecter des patterns émergents dans les demandes de JC
- Utiliser graphify (EXTRACTED + INFERRED edges) pour identifier des connexions non évidentes entre projets et suggérer des synergies

## 5. INCORPORATION D'ARBOR ET DES LOOPS
- La boucle d'apprentissage d'Hermes (créer skills depuis expérience) est structurellement un cas d'Arbor Loop : hypothèse → expérience → insight → décision
- Activer une Arbor Loop « Memory Learning » permanente :
  - Hypothèse : « les N derniers patterns conversationnels méritent une procédure ou une skill »
  - Expérience : génération automatique + test sur sessions suivantes
  - Insight : la procédure a-t-elle réduit les erreurs ou accéléré les tâches ?
  - Décision : publier dans skills/ ou rejeter
- Étendre les loops existantes (forge, edge-ai, sigma, bench, seo) avec le pattern « memory update » d'Hermes — chaque loop devrait terminer par une extraction de leçons apprises
- La gateway unifiée d'Hermes (Telegram/Discord/Slack/WhatsApp/Signal/Email depuis un seul processus) est-elle un modèle pour consolider les connecteurs PKA (Telegram bot, scripts email, loop_watcher, codex_bridge) ?

---

## LIVRABLES ATTENDUS
- Une matrice de décision P0/P1/P2 avec coût estimé (complexité, temps) et impact
- Pour chaque P0 : un plan d'implémentation concret (fichiers à créer ou modifier, scripts à écrire, schéma DB si nécessaire)
- Un prototype de la séparation SOUL.md / USER.md / MEMORY.md
- Un design pour le « memory nudge » périodique (fréquence, trigger, format de sortie)
- Une analyse de la faisabilité FTS5 sur les sessions JSON existantes
- Un plan d'activation de l'Arbor Loop « Memory Learning »

## CONTRAINTES
- Toute modification doit préserver la rétrocompatibilité avec les outils existants (pka_session_extract.py, pka_retrieve.py, pka_generate_memory.py)
- Les fichiers pointeurs (AGENTS.md, CLAUDE.md, DEEPSEEK.md, GEMINI.md, QWEN.md, ADAPTER-PROMPT.md) doivent rester synchronisés
- Aucune clé API, token ou mot de passe en clair
- Tout nouveau script doit être documenté dans docs/system/ et indexé dans outils-index.md

---

Ceci est un mandat de recherche-action. Tu as accès à l'équipe complète (32 spécialistes), aux tools PKA, au web, et aux patterns Arbor + Loop. Commence par l'analyse du transcript Hermes, puis produis le plan.
