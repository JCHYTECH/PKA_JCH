#!/usr/bin/env zsh
PKA_DIR="/Users/jchavauxm5/PKA_JCH"
MODEL="openrouter"
TITLE="Dobby - OpenRouter"
BG="#1a1a2e"
FG="#e8e2da"
CURSOR="#c9a43e"

osascript <<APPLESCRIPT
tell application "Terminal"
  activate
  do script "printf '\\033]0;$TITLE\\007'; printf '\\033]10;$FG\\007'; printf '\\033]11;$BG\\007'; printf '\\033]12;$CURSOR\\007'; cd " & quoted form of "$PKA_DIR" & " && ./bin/dobby.sh --model $MODEL"
end tell
APPLESCRIPT
