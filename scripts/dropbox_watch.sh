#!/bin/bash
# dropbox-watch.sh — Surveille ~/Dropbox/VETALYX/ et logue les changements
# Exécuté par launchd en continu. Log dans TEAM_Inbox/

LOG_DIR="$HOME/PKA_JCH/TEAM_Inbox"
LOG_FILE="$LOG_DIR/dropbox_vetalyx_changes.log"
WATCH_DIR="$HOME/Dropbox/VETALYX"

mkdir -p "$LOG_DIR"

fswatch -0 \
  --exclude '\.DS_Store' \
  --exclude '~\$' \
  --exclude '\.tmp$' \
  "$WATCH_DIR" | while IFS= read -r -d '' file; do
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $file" >> "$LOG_FILE"
done
