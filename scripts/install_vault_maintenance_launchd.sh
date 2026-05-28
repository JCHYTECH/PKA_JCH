#!/bin/zsh
set -euo pipefail

LABEL="com.jchytech.pka-vault-maintenance"
SRC="/Users/jchavauxm5/PKA_JCH/scripts/launchd/${LABEL}.plist"
DST="$HOME/Library/LaunchAgents/${LABEL}.plist"

mkdir -p "$HOME/Library/LaunchAgents"
mkdir -p "/Users/jchavauxm5/PKA_JCH/scripts/logs"
cp "$SRC" "$DST"

if launchctl print "gui/$(id -u)/$LABEL" >/dev/null 2>&1; then
  launchctl bootout "gui/$(id -u)/$LABEL" >/dev/null 2>&1 || true
fi

launchctl bootstrap "gui/$(id -u)" "$DST"
launchctl enable "gui/$(id -u)/$LABEL"

echo "Installed $LABEL — lancé quotidiennement à 02:00"
