#!/usr/bin/env zsh
# dobby.sh — Lanceur unifié PKA
# Usage : ./dobby.sh [--model claude|codex|gemini|gemma4|qwen3]
# Sans argument : lance Claude Code (défaut)

PKA_DIR="$(cd "$(dirname "$0")" && pwd)"
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
    export DEEPSEEK_MODEL="${DEEPSEEK_MODEL:-deepseek-chat}"
    exec python3 "$PKA_DIR/scripts/deepseek_chat.py"
    ;;

  deepseek-r1)
    if [[ -z "$DEEPSEEK_API_KEY" ]]; then
      echo "❌ DEEPSEEK_API_KEY non définie — ajouter dans ~/.zshrc"
      exit 1
    fi
    export DEEPSEEK_MODEL="deepseek-reasoner"
    exec python3 "$PKA_DIR/scripts/deepseek_chat.py"
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
    exec python3 "$PKA_DIR/scripts/ollama_chat.py" \
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
    exec python3 "$PKA_DIR/scripts/ollama_chat.py" \
      --model "qwen3.6:latest" \
      --system-file "$PKA_DIR/QWEN.md" \
      --verbose

    ;;

  *)
    echo "❌ Modèle inconnu : $MODEL"
    echo ""
    echo "Modèles disponibles :"
    echo "  --model claude    Claude Code (Anthropic) — défaut"
    echo "  --model codex     Codex CLI (OpenAI)"
    echo "  --model gemini    Gemini CLI (Google)"
    echo "  --model gemma4    Gemma 4 local (Ollama)"
    echo "  --model qwen3     Qwen 3.6 local (Ollama)"
    exit 1
    ;;

esac
