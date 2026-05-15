#!/usr/bin/env zsh

set -euo pipefail

PKA_DIR="$(cd "$(dirname "$0")" && pwd)"
LABEL="com.jchytech.pka-dashboard"
PLIST_SRC="$PKA_DIR/scripts/launchd/$LABEL.plist"
LAUNCH_AGENTS_DIR="$HOME/Library/LaunchAgents"
PLIST_DST="$LAUNCH_AGENTS_DIR/$LABEL.plist"
RUNTIME_DIR="$PKA_DIR/tmp"

mkdir -p "$LAUNCH_AGENTS_DIR" "$RUNTIME_DIR"

cp "$PLIST_SRC" "$PLIST_DST"

if launchctl print "gui/$(id -u)/$LABEL" >/dev/null 2>&1; then
  launchctl bootout "gui/$(id -u)/$LABEL" >/dev/null 2>&1 || true
fi

existing_pid="$(lsof -tiTCP:8787 -sTCP:LISTEN 2>/dev/null | head -n 1 || true)"
if [[ -n "${existing_pid:-}" ]]; then
  existing_command="$(ps -p "$existing_pid" -o command= 2>/dev/null || true)"
  if [[ "$existing_command" == *"dashboard_server.py"* ]]; then
    kill "$existing_pid" 2>/dev/null || true
    sleep 0.5
  fi
fi

launchctl bootstrap "gui/$(id -u)" "$PLIST_DST"
launchctl enable "gui/$(id -u)/$LABEL"
launchctl kickstart -k "gui/$(id -u)/$LABEL"

echo "LaunchAgent installe: $PLIST_DST"
echo "Dashboard: http://127.0.0.1:8787/hub.html"
