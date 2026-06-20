# Launch Command

Mémo de lancement des runtimes [[Dobby]] / PKA_JCH.

## Commandes courtes

```bash
dobby "ta question"      # Dobby via Qwen 3.7 Plus / OpenRouter
dobby max "ta question"  # Dobby via Qwen 3.7 Max / OpenRouter
qwen "ta question"       # Qwen 3.7 Plus / OpenRouter
qwen max "ta question"   # Qwen 3.7 Max / OpenRouter
```

Sans question, les commandes ouvrent un mode interactif :

```bash
dobby
dobby max
qwen
qwen max
```

## Lanceur multi-modèles PKA

Depuis le dossier `PKA_JCH` :

```bash
bin/dobby.sh --model claude       # Claude Code
bin/dobby.sh --model codex        # Codex CLI
bin/dobby.sh --model gemini       # Gemini CLI
bin/dobby.sh --model deepseek     # DeepSeek chat
bin/dobby.sh --model deepseek-r1  # DeepSeek reasoner
bin/dobby.sh --model gemma4       # Gemma 4 local / Ollama
bin/dobby.sh --model qwen3        # Qwen 3.6 local / Ollama
```

## Commandes disponibles

| Commande | Chemin |
|---|---|
| `claude` | `/Users/jchavauxm5/.local/bin/claude` |
| `codex` | `/Users/jchavauxm5/.npm-global/bin/codex` |
| `gemini` | `/Users/jchavauxm5/.npm-global/bin/gemini` |
| `deepseek` | `/Library/Frameworks/Python.framework/Versions/3.13/bin/deepseek` |
| `deepseek-tui` | `/opt/homebrew/bin/deepseek-tui` |
| `qwen` | `/Users/jchavauxm5/.local/bin/qwen` |
| `dobby` | `/Users/jchavauxm5/.local/bin/dobby` |

## Notes

- `dobby` et `qwen` chargent automatiquement le bootstrap PKA : `QWEN.md`, `ADAPTER-PROMPT.md`, `MEMORY.md`, `TEAM/dobby.md`, `TEAM/ROSTER.md`, `wiki/index.md`, les deux dernières daily, le scan projets et le scan inbox.
- `dobby` est un wrapper vers `qwen` avec identité [[Dobby]] déjà injectée.
- `bin/dobby.sh` reste le lanceur multi-modèles historique.

## Voir aussi

- [[Dobby]]
- [[QWEN]]
- [[ADAPTER-PROMPT]]
- [[MEMORY]]
- [[TEAM/ROSTER|Roster]]
