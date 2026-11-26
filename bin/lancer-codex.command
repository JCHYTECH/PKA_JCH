#!/usr/bin/env zsh
export PKA_DIR="/Users/jchavauxm5/PKA_JCH"
export PKA_TITLE="Dobby — Codex (OpenRouter)"
export PKA_BG="#1a1a2e"
export PKA_FG="#f8f5f0"
export PKA_CURSOR="#7c3aed"

osascript <<'APPLESCRIPT'
tell application "Terminal"
  activate
  set pka_dir to system attribute "PKA_DIR"
  set pka_title to system attribute "PKA_TITLE"
  set pka_bg to system attribute "PKA_BG"
  set pka_fg to system attribute "PKA_FG"
  set pka_cursor to system attribute "PKA_CURSOR"
  do script "printf '\\033]0;" & pka_title & "\\007'; printf '\\033]10;" & pka_fg & "\\007'; printf '\\033]11;" & pka_bg & "\\007'; printf '\\033]12;" & pka_cursor & "\\007'; cd " & quoted form of pka_dir & " && export OPENROUTER_API_KEY=\"$(cat ~/.config/pka-jch/openrouter_key.txt)\" && codex --profile openrouter \"$(cat docs/system/bootstrap-forced.md)\""
end tell
APPLESCRIPT
