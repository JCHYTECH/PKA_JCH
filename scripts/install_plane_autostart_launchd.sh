#!/usr/bin/env zsh
# Installs the PKA Plane autostart launchd service for the current macOS user.

set -euo pipefail

LABEL="com.jchytech.pka-plane-autostart"
SRC="/Users/jchavauxm5/PKA_JCH/scripts/launchd/${LABEL}.plist"
DST="$HOME/Library/LaunchAgents/${LABEL}.plist"

mkdir -p "$HOME/Library/LaunchAgents"
chmod +x "/Users/jchavauxm5/PKA_JCH/bin/plane-autostart.sh"
cp "$SRC" "$DST"

if launchctl print "gui/$(id -u)/$LABEL" >/dev/null 2>&1; then
  launchctl bootout "gui/$(id -u)/$LABEL" >/dev/null 2>&1 || true
fi

launchctl bootstrap "gui/$(id -u)" "$DST"
launchctl enable "gui/$(id -u)/$LABEL"
launchctl kickstart -k "gui/$(id -u)/$LABEL"

echo "Installed and started $LABEL"
echo "Log: /Users/jchavauxm5/PKA_JCH/tmp/plane-autostart.log"
