#!/usr/bin/env zsh
# Lupo Planner 🐺 — lanceur double-clic
# Démarre un serveur local et ouvre le navigateur.
# Sans ça, OSM renvoie « 403 access blocked » (file:// → referer invalide).

PLANNER_DIR="/Users/jchavauxm5/PKA_JCH/JCH_Inbox/03_PROJECTS/07_TRAVELS/lupo-planner"
PORT=8088
URL="http://localhost:${PORT}"

cd "$PLANNER_DIR" || { echo "Dossier introuvable : $PLANNER_DIR"; read -k1; exit 1; }

# Un serveur tourne déjà sur ce port ? Alors on ouvre juste le navigateur.
if lsof -i "tcp:${PORT}" -sTCP:LISTEN >/dev/null 2>&1; then
  open "$URL"
  exit 0
fi

osascript <<APPLESCRIPT
tell application "Terminal"
  activate
  do script "printf '\\\\033]0;Lupo Planner 🐺\\\\007'; cd " & quoted form of "$PLANNER_DIR" & " && python3 -m http.server $PORT --bind 127.0.0.1"
end tell
APPLESCRIPT

# Laisser le temps au serveur de démarrer, puis ouvrir le navigateur.
sleep 1
open "$URL"
