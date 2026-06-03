#!/usr/bin/env zsh
PKA_DIR="/Users/jchavauxm5/PKA_JCH"
MODEL="gemini"
TITLE="Dobby - Gemini CLI"
BG="#0f1710"
FG="#f8f5f0"
CURSOR="#3d5a3e"

osascript <<APPLESCRIPT
tell application "Terminal"
  activate
  do script "printf '\\033]0;$TITLE\\007'; printf '\\033]10;$FG\\007'; printf '\\033]11;$BG\\007'; printf '\\033]12;$CURSOR\\007'; cd " & quoted form of "$PKA_DIR" & " && ./dobby.sh --model $MODEL"
end tell
APPLESCRIPT
