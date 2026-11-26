#!/bin/bash
# One-off (2026-11-23) : pull 5 modèles LLM sur M1 (tunnel 11435), retry 3x, puis mail à JC.
set -u
PKA="/Users/jchavauxm5/PKA_JCH"
LOG="$PKA/_local/llm-pull.log"
OLLAMA="http://127.0.0.1:11435"
: > "$LOG"

models=(qwen3-coder:30b gemma4:26b phi4:14b devstral:24b deepseek-r1:32b)
ok=""; ko=""

for m in "${models[@]}"; do
  done_flag=0
  for attempt in 1 2 3; do
    echo "=== PULL $m (essai $attempt) $(date '+%F %H:%M:%S') ===" >> "$LOG"
    curl -sN -X POST "$OLLAMA/api/pull" -H "Content-Type: application/json" -d "{\"model\":\"$m\"}" >> "$LOG" 2>&1
    if curl -s "$OLLAMA/api/tags" | grep -q "\"$m\""; then
      ok="${ok}\n  ✓ $m"
      echo "=== DONE $m OK ===" >> "$LOG"
      done_flag=1
      break
    fi
    echo "=== $m échec essai $attempt ===" >> "$LOG"
    [ "$attempt" != "3" ] && sleep 30
  done
  [ "$done_flag" = "0" ] && ko="${ko}\n  ✗ $m"
done
echo "=== ALL_DONE $(date '+%F %H:%M:%S') ===" >> "$LOG"

[ -z "$ok" ] && ok="\n  (aucun)"
[ -z "$ko" ] && ko="\n  (aucun)"
body="Bonsoir JC,\n\nTéléchargement des modèles LLM sur M1 terminé.\n\nRéussis:$ok\n\nÉchecs:$ko\n\nBanc promptfoo prêt à rejouer : JCH_Inbox/03_PROJECTS/01_AI_IT_TOOLS/llm-eval/\n\n— Dobby 🦉"
printf "%b" "$body" | python3 "$PKA/scripts/dobby_notify_email.py" --subject "M1 · modèles LLM téléchargés" --body - >> "$LOG" 2>&1
echo "=== NOTIF_MAIL $(date '+%F %H:%M:%S') ===" >> "$LOG"
