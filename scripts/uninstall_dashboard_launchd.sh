#!/usr/bin/env zsh
# Removes the PKA dashboard launchd service for the current macOS user.

set -euo pipefail

LABEL="com.jchytech.pka-dashboard"
DST="$HOME/Library/LaunchAgents/${LABEL}.plist"

if launchctl print "gui/$(id -u)/$LABEL" >/dev/null 2>&1; then
  launchctl bootout "gui/$(id -u)/$LABEL" >/dev/null 2>&1 || true
fi

rm -f "$DST"

echo "Uninstalled $LABEL"
