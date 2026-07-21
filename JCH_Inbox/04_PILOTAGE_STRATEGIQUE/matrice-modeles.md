# Matrice des modèles — PKA_JCH
> Quel modèle utiliser pour quel type de tâche, et comment.
> Dernière mise à jour : 2026-07-06 par Dobby 🦉
> 
> **Lecture :** une ligne = un modèle disponible. Choisir selon la tâche.

---

## Modèles cloud (API)

| Modèle | Runtime | Accès | Usage recommandé | Coût estimé | Forces | Limites |
|--------|---------|-------|-----------------|-------------|--------|---------|
| **DeepSeek V4** | Codex CLI (local) | Direct | Tâches complexes, code, architecture, recherche, loops | ~$0.14/M input | Raisonnement profond, 1M contexte, tools riches | Bing indisponible → DuckDuckGo |
| **Claude Sonnet 4.6** | Claude Code | API Anthropic | Raisonnement stratégique, analyse juridique, décisions nuancées | Payant | Pensée structurée, sécurité, nuance | Contexte plus limité que DeepSeek |
| **Qwen 2.5 / 3.5** | OpenRouter | `~/.config/pka-jch/openrouter_key.txt` | Tâches équilibrées, backup DeepSeek | Variable (OpenRouter) | Bon rapport qualité/prix | Dépend du modèle spécifique |
| **Gemini 2.5 Pro** | Gemini CLI | API Google | Multimodal, analyse d'images, recherche web Google | Payant | Intégration Google, vision, 1M+ contexte | Prompting différent des autres |
| **Nous Portal** | Hermes Agent | Portal OAuth | Agent autonome avec learning loop | Abonnement | Skills auto-générées, gateway multi-canal | Mono-runtime, non intégré PKA |

---

## Modèles locaux — Ollama sur M1 (headless)

| Modèle | Taille | Usage recommandé | Forces | Limites |
|--------|--------|-----------------|--------|---------|
| **qwen3:30b-a3b** | 30B (MoE) | Tâches complexes locales, code, analyse | Plus puissant du lineup local | Lent, ~16 Go RAM |
| **qwen2.5-coder:14b** | 14B | Code, scripts, debug | Spécialisé code, bonne qualité | Pas multimodal |
| **deepseek-r1:14b** | 14B | Raisonnement, math, logique | Chaîne de pensée explicite | Lent (reasoning tokens) |
| **gemma3:12b-it-qat** | 12B (quantifié) | Chat rapide, prototypage, tâches légères | Rapide, bon français | Moins puissant que Qwen |
| **llama3.2-vision:11b** | 11B | Analyse d'images, OCR, photo | Multimodal local | Vision seulement, pas audio |
| **dobby-prompt** | 7B (fine-tuné) | Tâches PKA spécifiques | Fine-tuné sur patterns Dobby | Modèle étroit, expérimental |
| **llama3.2:3b** | 3B | Tâches triviales, tests rapides | Ultra-rapide, léger | Très limité |
| **mxbai-embed-large** | 335M | Embeddings, recherche sémantique | Spécialisé embeddings | Pas de génération texte |

---

## Guide de choix rapide

| Tu veux... | Utilise... |
|------------|-----------|
| Coder un script complexe | DeepSeek V4 (Codex) |
| Écrire un brief stratégique | Claude Sonnet 4.6 |
| Analyser une photo | llama3.2-vision:11b (local) ou Gemini 2.5 Pro |
| Faire une recherche web | DeepSeek V4 → DuckDuckGo |
| Du code hors-ligne / gratuit | qwen2.5-coder:14b (Ollama M1) |
| Un agent autonome longue durée | DeepSeek V4 (1M contexte) |
| Raisonner sur un problème logique | deepseek-r1:14b (local) |
| Prototyper rapidement | gemma3:12b (local) |
| Intégrer PKA sans payer d'API | qwen3:30b (local, lent) ou gemma3:12b (local, rapide) |
| Faire une recherche sémantique | mxbai-embed-large → team.db |

---

## Coûts mensuels estimés (ordre de grandeur)

| Modèle | Usage typique | Coût/mois estimé |
|--------|---------------|-----------------|
| DeepSeek V4 | Sessions quotidiennes | ~$5-15 |
| Claude Sonnet | Sessions stratégiques | ~$10-30 |
| Ollama M1 (tous) | Local uniquement | ~$0 (électricité M1) |
| Gemini | Occasionnel | ~$0-5 |
| OpenRouter (Qwen) | Backup | ~$0-5 |

---

*Mise à jour automatique par Dobby quand un modèle est ajouté, remplacé, ou que ses performances changent.*
