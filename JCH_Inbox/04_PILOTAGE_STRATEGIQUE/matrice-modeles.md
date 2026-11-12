# Matrice des modèles — PKA_JCH
> Quel modèle utiliser pour quel type de tâche, et comment.
> Dernière mise à jour : 2026-11-07 par Dobby 🦉
> 
> **Lecture :** une ligne = un modèle disponible. Choisir selon la tâche.

---

## Modèles cloud (API)

| Modèle | Runtime | Accès | Usage recommandé | Coût estimé | Forces | Limites |
|--------|---------|-------|-----------------|-------------|--------|---------|
| **DeepSeek V4 Pro** | Codex CLI / DeepSeek TUI | Direct | Orchestration, raisonnement profond, architecture, loops, traduction | Payant | 1,6 T params / 49 Md actifs, 1M contexte, agentique fort | — |
| **DeepSeek V4 Flash** | DeepSeek TUI / API | Direct | Sous-agents spécialistes (31), tâches à fort volume, sub-agent | ~$0.14/M input | Rapide, bon marché, 1M contexte | Raisonnement plus léger que Pro |
| **Claude Sonnet 4.6** | Claude Code | API Anthropic | Raisonnement stratégique, analyse juridique, décisions nuancées | Payant | Pensée structurée, sécurité, nuance | Contexte plus limité que DeepSeek |
| **Qwen 3.6 Plus** | OpenRouter | `~/.config/pka-jch/openrouter_key.txt` | Agentique open-source fort, backup DeepSeek | Variable (OpenRouter) | 1M contexte, tool-use fiable | Concurrence GLM 5.1 / Kimi K2.6 |
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
| Coder un script complexe | DeepSeek V4 Pro (Codex) |
| Écrire un brief stratégique | Claude Sonnet 4.6 |
| Analyser une photo | llama3.2-vision:11b (local) ou Gemini 2.5 Pro |
| Faire une recherche web | DeepSeek natif (Search/Fetch, $0.75/1k) → Tavily en secours |
| Du code hors-ligne / gratuit | qwen2.5-coder:14b (Ollama M1) |
| Un agent autonome longue durée | DeepSeek V4 Pro (1M contexte) |
| Raisonner sur un problème logique | deepseek-r1:14b (local) |
| Prototyper rapidement | gemma3:12b (local) |
| Intégrer PKA sans payer d'API | qwen3:30b (local, lent) ou gemma3:12b (local, rapide) |
| Faire une recherche sémantique | mxbai-embed-large → team.db |

---

## Coûts mensuels estimés (ordre de grandeur)

| Modèle | Usage typique | Coût/mois estimé |
|--------|---------------|-----------------|
| DeepSeek V4 (Pro+Flash) | Sessions quotidiennes | ~$5-15 |
| Claude Sonnet | Sessions stratégiques | ~$10-30 |
| Ollama M1 (tous) | Local uniquement | ~$0 (électricité M1) |
| Gemini | Occasionnel | ~$0-5 |
| OpenRouter (Qwen) | Backup | ~$0-5 |

---

## Notes 2026-11-07 (veille DeepSeek)

- **IDs explicites V4** : `deepseek-v4-pro` (flagship) et `deepseek-v4-flash` (rapide/économique). Les alias `deepseek-chat` / `deepseek-reasoner` **prennent fin le 24/07/2026** → utiliser les IDs explicites.
- **Recherche native** : endpoints DeepSeek `search` + `fetch` à **$0.75 / 1 000 requêtes réussies** (par requête, pas par token), opérateurs riches (`site:`, `lang:`, `after:`, `before:`, `OR`, `-`, `"…"`). Alternative à Tavily.
- **Tarif off-peak** : jusqu'à -75 % hors heures de pointe (pointe ≈ 11:30–19:30 ET). Programmer les jobs batch lourds (memory-review, loops) hors pointe.
- **Concurrence open-source** : Qwen 3.6 Plus (agentique fort), GLM 5.1, Kimi K2.6. DeepSeek V4 = meilleur en self-host MoE (souveraineté).
- **Routing recommandé** : orchestrateur → V4 Pro ; 31 sous-agents spécialistes → V4 Flash.

---

*Mise à jour automatique par Dobby quand un modèle est ajouté, remplacé, ou que ses performances changent.*
