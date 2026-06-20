#!/usr/bin/env zsh
# dobby.sh — Lanceur unifié PKA
# Usage : ./dobby.sh [--model claude|codex|gemini|gemma4|qwen3]
# Sans argument : lance Claude Code (défaut)

PKA_DIR="$(cd "$(dirname "$0")/.." && pwd)"
MODEL="claude"

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

export PKA_MODEL="$MODEL"
export PKA_DIR

cd "$PKA_DIR"

# Python : priorité au venv local (évite conflits pydantic/openai du Python système)
if [[ -x "$PKA_DIR/.venv/bin/python3" ]]; then
  PYTHON="$PKA_DIR/.venv/bin/python3"
else
  PYTHON="python3"
fi

SECRETS_FILE="$HOME/.config/pka-jch/api_keys"
if [[ -f "$SECRETS_FILE" ]]; then
  set -a
  source "$SECRETS_FILE"
  set +a
fi

stop_ollama_model() {
  local model_name="$1"
  if command -v ollama &>/dev/null; then
    ollama stop "$model_name" >/dev/null 2>&1 || true
  fi
}

echo "🐶 Dobby — PKA_JCH"
echo "   Modèle  : $MODEL"
echo "   Dossier : $PKA_DIR"
echo ""

case "$MODEL" in

  claude|sonnet|opus)
    if ! command -v claude &>/dev/null; then
      echo "❌ Claude Code non trouvé. Installer : https://claude.ai/code"
      exit 1
    fi
    export PKA_MODEL="claude"
    exec claude

    ;;

  codex)
    if ! command -v codex &>/dev/null; then
      echo "❌ Codex CLI non trouvé."
      exit 1
    fi
    # Codex lit AGENTS.md automatiquement dans le répertoire de travail
    exec codex

    ;;

  gemini)
    if ! command -v gemini &>/dev/null; then
      echo "❌ Gemini CLI non trouvé."
      exit 1
    fi
    export GEMINI_CLI_TRUST_WORKSPACE=true
    # Gemini lit GEMINI.md automatiquement dans le répertoire de travail
    exec gemini

    ;;

  deepseek)
    if [[ -z "$DEEPSEEK_API_KEY" ]]; then
      echo "❌ DEEPSEEK_API_KEY non définie — ajouter dans ~/.zshrc"
      exit 1
    fi
    export DEEPSEEK_MODEL="${DEEPSEEK_MODEL:-deepseek-v4-flash}"
    exec $PYTHON "$PKA_DIR/scripts/deepseek_chat.py"
    ;;

  deepseek-r1)
    if [[ -z "$DEEPSEEK_API_KEY" ]]; then
      echo "❌ DEEPSEEK_API_KEY non définie — ajouter dans ~/.zshrc"
      exit 1
    fi
    export DEEPSEEK_MODEL="deepseek-reasoner"
    exec $PYTHON "$PKA_DIR/scripts/deepseek_chat.py"
    ;;

  openrouter|or)
    OPENROUTER_KEY_FILE="$HOME/.config/pka-jch/openrouter_key.txt"
    if [[ ! -f "$OPENROUTER_KEY_FILE" ]]; then
      echo "❌ Clé OpenRouter introuvable : $OPENROUTER_KEY_FILE"
      exit 1
    fi
    export DEEPSEEK_API_KEY="$(cat "$OPENROUTER_KEY_FILE")"
    export DEEPSEEK_BASE_URL="https://openrouter.ai/api/v1"

    export DEEPSEEK_MODEL="${DEEPSEEK_MODEL:-deepseek/deepseek-v4-flash}"
    echo "ℹ️  OpenRouter — multi-provider (DeepSeek, Anthropic, Qwen...)"

    echo "   Modèle : $DEEPSEEK_MODEL"
    echo "   Crédits : ~10 USD (pré-payé)"
    echo ""
    exec $PYTHON "$PKA_DIR/scripts/deepseek_chat.py"
    ;;

  kimi|kimik2|moonshot)
    KIMI_KEY_FILE="$HOME/.config/pka-jch/kimi_key.txt"
    if [[ ! -f "$KIMI_KEY_FILE" ]]; then
      echo "❌ Clé Kimi introuvable : $KIMI_KEY_FILE"
      echo "   À créer avec ta clé API Moonshot (https://platform.moonshot.ai)"
      exit 1
    fi
    export DEEPSEEK_API_KEY="$(cat "$KIMI_KEY_FILE")"
    export DEEPSEEK_BASE_URL="https://api.moonshot.ai/v1"
    export DEEPSEEK_MODEL="${DEEPSEEK_MODEL:-kimi-k2.7-code}"
    export PKA_POINTER="KIMI.md"
    export PKA_PROVIDER="Kimi K2.7"
    echo "ℹ️  Kimi K2.7 — API Moonshot directe"
    echo "   Modèle : $DEEPSEEK_MODEL"
    echo ""
    exec $PYTHON "$PKA_DIR/scripts/deepseek_chat.py"
    ;;

  gemma4|gemma)
    if ! command -v ollama &>/dev/null; then
      echo "❌ Ollama non trouvé. Installer : https://ollama.ai"
      exit 1
    fi
    # Vérifie que le modèle est disponible
    if ! ollama list 2>/dev/null | grep -q "gemma4"; then
      echo "⚠️  Gemma 4 non trouvé dans Ollama."
      echo "   Installer : ollama pull gemma4"
      exit 1
    fi
    stop_ollama_model "qwen3.6:latest"
    echo "ℹ️  Mode local Gemma 4 — accès filesystem limité au chat Ollama"
    echo "ℹ️  Préflight perf : arrêt de Qwen 3.6 pour libérer la RAM/VRAM"
    echo "   Pour un agent complet avec outils, lancer : gemini gemma setup"
    echo ""
    exec $PYTHON "$PKA_DIR/scripts/ollama_chat.py" \
      --model "gemma4:latest" \
      --system-file "$PKA_DIR/GEMMA.md" \
      --verbose

    ;;

  qwen3|qwen)
    if ! command -v ollama &>/dev/null; then
      echo "❌ Ollama non trouvé."
      exit 1
    fi
    if ! ollama list 2>/dev/null | grep -q "qwen3.6"; then
      echo "⚠️  Qwen 3.6 non trouvé dans Ollama."
      echo "   Installer : ollama pull qwen3.6"
      exit 1
    fi
    stop_ollama_model "gemma4:latest"
    echo "ℹ️  Mode local Qwen 3.6 — accès filesystem limité au chat Ollama"
    echo "ℹ️  Préflight perf : arrêt de Gemma 4 pour libérer la RAM/VRAM"
    echo ""
    exec $PYTHON "$PKA_DIR/scripts/ollama_chat.py" \
      --model "qwen3.6:latest" \
      --system-file "$PKA_DIR/QWEN.md" \
      --verbose

    ;;

  *)
    echo "❌ Modèle inconnu : $MODEL"
    echo ""
    echo "Modèles disponibles :"
    echo "  --model claude      Claude Code (Anthropic) — défaut"
    echo "  --model codex       Codex CLI (OpenAI)"
    echo "  --model gemini      Gemini CLI (Google)"
    echo "  --model deepseek    DeepSeek Chat (API)"
    echo "  --model deepseek-r1 DeepSeek Reasoner (API)"
    echo "  --model openrouter  OpenRouter (multi-provider, pré-payé)"
    echo "  --model kimi        Kimi K2.7 (API Moonshot directe)"
    echo "  --model gemma4      Gemma 4 local (Ollama)"
    echo "  --model qwen3       Qwen 3.6 local (Ollama)"
    exit 1
    ;;

esac
