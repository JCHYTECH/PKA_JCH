# Launch Command

Mémo de lancement des runtimes [[Dobby]] / PKA_JCH.

## Lanceur multi-modèles

Depuis le dossier `PKA_JCH` :

```bash
bin/dobby.sh --model deepseek    # DeepSeek V4 (TUI, outils) — défaut
bin/dobby.sh --model openai      # GPT-6.1 Sol (via OpenRouter)
bin/dobby.sh --model anthropic   # Claude Opus 5.5 (via OpenRouter)
bin/dobby.sh --model kimi        # Kimi K3.1 Pro (via OpenRouter)
bin/dobby.sh --model gemini      # Gemini (CLI Google, direct)
bin/dobby.sh --model local       # Local sur M1 32 Go (Ollama)
```

Sans argument : lance `deepseek` (TUI).

## Bootstrap unique

Tous les lanceurs chargent le **même bootstrap Dobby** — `AGENTS.md` est la source canonique :

- `deepseek` (TUI) → lit `AGENTS.md` automatiquement.
- `openai` / `anthropic` / `kimi` → `openrouter_chat.py` injecte `AGENTS.md` en system prompt.
- `gemini` → lit `GEMINI.md` (stub → `AGENTS.md`).
- `local` → `ollama_chat.py --system-file AGENTS.md`.

## Modèles par défaut (derniers)

| Société | Modèle | Accès |
|---|---|---|
| DeepSeek | V4 (TUI) | direct |
| OpenAI | GPT-6.1 Sol | OpenRouter |
| Anthropic | Claude Opus 5.5 | OpenRouter |
| Kimi | Kimi K3.1 Pro | OpenRouter |
| Google | Gemini 4 Argon | Gemini CLI direct |
| Local M1 | gemma3:27b (défaut) | Ollama M1 |

## Grok 4.7 (prototype validé)

`bin/lancer-grok.command` lance `x-ai/grok-4.7` via Codex CLI et OpenRouter. Sans argument, il injecte le bootstrap forcé ; avec `exec`, les options de configuration sont placées après la sous-commande Codex. Le lanceur Dobby par défaut reste inchangé.

Capacités vérifiées le 5 novembre 2026 :

- lecture et écriture contrôlée de fichiers avec les outils Codex ;
- capture et recherche explicites de mémoire entre deux sessions, sur copies isolées de `TEAM/team.db` et `MEMORY.md` ;
- appels réels aux MCP `pka_filesystem` et `pka_sqlite` en lecture ;
- délégation native à un spécialiste distinct, avec `wait` sans `timeout_ms` ;
- `graphify update .` et `graphify explain` pilotés par Grok.

Le lanceur active le multi-agent, rend les deux MCP obligatoires et limite SQLite MCP à `list_tables`, `describe_table` et `read_query`. Cette configuration propre à Grok est distincte du `.mcp.json` général.

Limites :

- l’inférence dépend d’OpenRouter, du réseau et des crédits : ce n’est pas un Dobby autonome hors ligne ;
- le serveur MCP filesystem peut écrire dans `PKA_JCH` ; les tests MCP ont uniquement porté sur la lecture ;
- les appels `exec` sont validés, mais le double-clic et le TUI interactif n’ont pas été testés ;
- la mémoire automatique post-session, Plane, l’e-mail et les publications ne sont pas certifiés ;
- les fichiers `.command`, dont `lancer-grok.command`, ne sont pas nécessairement indexés par graphify.

## Changer de modèle en cours de session

Depuis un chat, la commande `/model <slug>` change de modèle sans quitter
(`/models` pour lister). L'historique est conservé.

**OpenRouter** (openai / anthropic / kimi — dans `openrouter_chat.py`) :

```
/model anthropic/claude-sonnet-5-5    # moins cher chez Anthropic
/model openai/gpt-6-astra             # top OpenAI
/model moonshotai/kimi-k3.1-pro
/models
```

**Local M1** (dans `ollama_chat.py`) :

```
/model qwen2.5-coder:32b
/model gemma3:27b
/models
```

**Gemini** : CLI natif — le modèle se gère via les options du CLI Gemini (pas de `/model` PKA).

## Commandes disponibles

| Commande | Chemin |
|---|---|
| `deepseek-tui` | `/opt/homebrew/bin/deepseek-tui` |
| `gemini` | `/Users/jchavauxm5/.npm-global/bin/gemini` |
| `dobby` | `bin/dobby.sh` (lanceur multi-modèles) |

## Local (M1 32 Go)

Le lanceur `local` ouvre un tunnel SSH vers le M1 et appelle `ollama_chat.py`.
Modèle par défaut : `gemma3:27b`. Pour changer :

```bash
OLLAMA_MODEL=qwen2.5-coder:32b ./bin/dobby.sh --model local
```

Voir `docs/system/MODE_EMPLOI_M1_LLM.md` pour l'accès M1 détaillé.

## Notes

- `bin/dobby.sh` est le lanceur unifié ; les `bin/lancer-*.command` sont les raccourcis double-clic (6 modèles).
- Clés : OpenRouter dans `~/.config/pka-jch/openrouter_key.txt`, Gemini géré par le CLI.

## Voir aussi

- [[Dobby]]
- [[M1_LLM_ACCESS]]
- [[ADAPTER-PROMPT]]
- [[MEMORY]]