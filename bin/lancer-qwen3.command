#!/usr/bin/env zsh
export PKA_DIR="/Users/jchavauxm5/PKA_JCH"
export PKA_MODEL="qwen3"
export PKA_TITLE="Dobby - Qwen 3.6"
export PKA_BG="#3a3937"
export PKA_FG="#0d0b09"
export PKA_CURSOR="#e8e2da"

osascript <<'APPLESCRIPT'
tell application "Terminal"
  activate
  set pka_dir to system attribute "PKA_DIR"
  set pka_model to system attribute "PKA_MODEL"
  set pka_title to system attribute "PKA_TITLE"
  set pka_bg to system attribute "PKA_BG"
  set pka_fg to system attribute "PKA_FG"
  set pka_cursor to system attribute "PKA_CURSOR"
  do script "printf '\\033]0;" & pka_title & "\\007'; printf '\\033]10;" & pka_fg & "\\007'; printf '\\033]11;" & pka_bg & "\\007'; printf '\\033]12;" & pka_cursor & "\\007'; cd " & quoted form of pka_dir & " && ./bin/dobby.sh --model " & pka_model
end tell
APPLESCRIPT
