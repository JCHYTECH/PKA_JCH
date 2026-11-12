#!/usr/bin/env zsh
# dobby.sh — Lanceur unifié PKA (v2)
# Usage : ./dobby.sh [--model deepseek|openai|anthropic|kimi|gemini|local]
# Défaut : deepseek (TUI riche en outils)

PKA_DIR="$(cd "$(dirname "$0")/.." && pwd)"
MODEL="deepseek"

# Parse arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    --model|-m)
      MODEL="$2"
      shift 2
      ;;
    *)
      shift
      ;;
  esac
done

export PKA_DIR
export PKA_MODEL="$MODEL"

cd "$PKA_DIR"

# Python : priorité au venv local
if [[ -x "$PKA_DIR/.venv/bin/python3" ]]; then
  PYTHON="$PKA_DIR/.venv/bin/python3"
else
  PYTHON="python3"
fi

# Bootstrap Dobby : source canonique unique pour tous les runtimes
BOOTSTRAP="$PKA_DIR/AGENTS.md"

echo "🐶 Dobby — PKA_JCH"
echo "   Modèle  : $MODEL"
echo "   Dossier : $PKA_DIR"
echo ""

case "$MODEL" in

  deepseek|ds)
    if ! command -v deepseek-tui &>/dev/null; then
      echo "❌ deepseek-tui non trouvé. Installer : brew install deepseek-tui"
      exit 1
    fi
    # deepseek-tui lit AGENTS.md automatiquement dans le répertoire de travail
    exec deepseek-tui --yolo
    ;;

  openai|gpt)
    exec $PYTHON "$PKA_DIR/scripts/openrouter_chat.py" \
      --model "openai/gpt-6.1-sol" \
      --system-file "$BOOTSTRAP"
    ;;

  anthropic|claude)
    exec $PYTHON "$PKA_DIR/scripts/openrouter_chat.py" \
      --model "anthropic/claude-opus-5.5" \
      --system-file "$BOOTSTRAP"
    ;;

  kimi)
    exec $PYTHON "$PKA_DIR/scripts/openrouter_chat.py" \
      --model "moonshotai/kimi-k3.1-pro" \
      --system-file "$BOOTSTRAP"
    ;;

  gemini)
    if ! command -v gemini &>/dev/null; then
      echo "❌ Gemini CLI non trouvé."
      exit 1
    fi
    export GEMINI_CLI_TRUST_WORKSPACE=true
    # Gemini lit GEMINI.md (stub → AGENTS.md) automatiquement
    exec gemini
    ;;

  local|ollama|m1)
    # Ollama tourne sur le M1 (32 Go). Tunnel SSH + ollama_chat.py local.
    M1_HOST="m1@100.73.212.110"
    OLLAMA_REMOTE_PORT=11434
    OLLAMA_TUNNEL_PORT=11435
    LOCAL_MODEL="${OLLAMA_MODEL:-gemma3:27b}"

    if ! command -v ssh &>/dev/null; then
      echo "❌ ssh requis pour accéder au M1."
      exit 1
    fi

    # Ouvre le tunnel SSH si pas déjà actif
    if ! nc -z 127.0.0.1 "$OLLAMA_TUNNEL_PORT" 2>/dev/null; then
      echo "ℹ️  Ouverture du tunnel SSH vers le M1 (Ollama)..."
      ssh -f -N -L "${OLLAMA_TUNNEL_PORT}:127.0.0.1:${OLLAMA_REMOTE_PORT}" "$M1_HOST" 2>/dev/null || {
        echo "❌ Impossible d'ouvrir le tunnel vers $M1_HOST."
        echo "   Vérifier que le M1 est allumé et que le serveur Ollama y tourne (ollama serve)."
        exit 1
      }
    fi

    export OLLAMA_URL="http://127.0.0.1:${OLLAMA_TUNNEL_PORT}/api/chat"
    echo "ℹ️  Modèle local : $LOCAL_MODEL (via M1 32 Go)"
    echo "   Changer de modèle : OLLAMA_MODEL=qwen2.5-coder:32b ./bin/dobby.sh --model local"
    echo ""
    exec $PYTHON "$PKA_DIR/scripts/ollama_chat.py" \
      --model "$LOCAL_MODEL" \
      --system-file "$BOOTSTRAP"
    ;;

  codex|codex-openrouter|or)
    if ! command -v codex &>/dev/null; then
      echo "❌ codex CLI non trouvé. Installer : npm i -g @openai/codex"
      exit 1
    fi
    export OPENROUTER_API_KEY="$(cat ~/.config/pka-jch/openrouter_key.txt 2>/dev/null)"
    echo "ℹ️  Codex CLI — agent local, backend OpenRouter (profil YOLO)"
    exec codex --profile openrouter "$(cat "$PKA_DIR/docs/system/bootstrap-forced.md")"
    ;;

  kimi-code|kc)
    export OPENROUTER_API_KEY="$(cat ~/.config/pka-jch/openrouter_key.txt 2>/dev/null)"
    if command -v kimi &>/dev/null; then
      echo "ℹ️  Kimi Code CLI — agent local, backend OpenRouter (YOLO)"
      exec kimi -m kimi-k3-or -y
    elif [[ -x "$HOME/.kimi-code/bin/kimi" ]]; then
      echo "ℹ️  Kimi Code CLI — agent local, backend OpenRouter (YOLO)"
      exec "$HOME/.kimi-code/bin/kimi" -m kimi-k3-or -y
    else
      echo "❌ Kimi Code CLI non trouvé."
      exit 1
    fi
    ;;

  *)
    echo "❌ Modèle inconnu : $MODEL"
    echo ""
    echo "Modèles disponibles :"
    echo "  --model deepseek    DeepSeek V4 (TUI, outils) — défaut"
    echo "  --model openai      GPT-6.1 Sol (via OpenRouter)"
    echo "  --model anthropic   Claude Opus 5.5 (via OpenRouter)"
    echo "  --model kimi        Kimi K3.1 Pro (via OpenRouter)"
    echo "  --model codex       Codex CLI agent (OpenRouter, YOLO)"
    echo "  --model kimi-code   Kimi Code CLI agent (OpenRouter, YOLO)"
    echo "  --model gemini      Gemini (CLI Google, direct)"
    echo "  --model local       Local sur M1 32 Go (Ollama)"
    exit 1
    ;;

esac
