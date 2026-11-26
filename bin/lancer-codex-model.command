#!/usr/bin/env zsh
# Lanceur Codex CLI générique — choisir un modèle OpenRouter (agent local, YOLO)
cd /Users/jchavauxm5/PKA_JCH || exit 1

echo "🐶 Dobby — Codex / OpenRouter (abonnement OpenRouter)"
echo ""
echo "Choisir le modèle :"
echo "  1) openai/gpt-6.1-sol           (GPT-6.1 Sol)"
echo "  2) anthropic/claude-opus-5.5    (Claude Opus 5.5)"
echo "  3) deepseek/deepseek-v4.1-flash (DeepSeek V4.1 Flash)"
echo "  4) moonshotai/kimi-k3.1-pro     (Kimi K3.1 Pro)"
echo "  5) google/gemini-4-argon        (Gemini 4 Argon)"
echo "  6) autre (saisir l'ID OpenRouter)"
echo ""
read "?Choix [1-6, défaut 1] : " n

case "$n" in
  1|"") M="openai/gpt-6.1-sol" ;;
  2)    M="anthropic/claude-opus-5.5" ;;
  3)    M="deepseek/deepseek-v4.1-flash" ;;
  4)    M="moonshotai/kimi-k3.1-pro" ;;
  5)    M="google/gemini-4-argon" ;;
  6)    read "?ID OpenRouter : " M ;;
  *)    M="openai/gpt-6.1-sol" ;;
esac

if [[ -z "$M" ]]; then
  echo "Aucun modèle sélectionné. Abandon."
  exit 1
fi

export OPENROUTER_API_KEY="$(cat ~/.config/pka-jch/openrouter_key.txt)"
echo ""
echo "→ codex --profile openrouter -m $M"
echo ""
exec codex --profile openrouter -m "$M"
