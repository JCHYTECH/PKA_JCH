#!/bin/zsh
set -euo pipefail

LABEL="com.jchytech.pka-dropbox-watch"
SRC="/Users/jchavauxm5/PKA_JCH/scripts/launchd/${LABEL}.plist"
DST="$HOME/Library/LaunchAgents/${LABEL}.plist"

mkdir -p "$HOME/Library/LaunchAgents"

# Unload if already loaded
if launchctl print "gui/$(id -u)/$LABEL" >/dev/null 2>&1; then
  launchctl bootout "gui/$(id -u)/$LABEL" >/dev/null 2>&1 || true
fi

cp "$SRC" "$DST"
launchctl bootstrap "gui/$(id -u)" "$DST"
launchctl enable "gui/$(id -u)/$LABEL"

# Trigger immediate first run
launchctl kickstart -k "gui/$(id -u)/$LABEL"

echo "Installed $LABEL"
echo "Log: ~/PKA_JCH/TEAM_Inbox/dropbox_vetalyx_changes.log"
