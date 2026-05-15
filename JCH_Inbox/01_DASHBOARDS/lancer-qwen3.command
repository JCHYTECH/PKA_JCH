#!/usr/bin/env zsh
PKA_DIR="/Users/jchavauxm5/PKA_JCH"
MODEL="qwen3"
TITLE="Dobby - Qwen 3.6"
BG="#3a3937"
FG="#0d0b09"
CURSOR="#e8e2da"

osascript <<APPLESCRIPT
tell application "Terminal"
  activate
  do script "printf '\\033]0;$TITLE\\007'; printf '\\033]10;$FG\\007'; printf '\\033]11;$BG\\007'; printf '\\033]12;$CURSOR\\007'; cd " & quoted form of "$PKA_DIR" & " && ./dobby.sh --model $MODEL"
end tell
APPLESCRIPT
