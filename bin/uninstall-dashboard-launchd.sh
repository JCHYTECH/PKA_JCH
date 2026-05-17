#!/usr/bin/env zsh

set -euo pipefail

LABEL="com.jchytech.pka-dashboard"
PLIST_DST="$HOME/Library/LaunchAgents/$LABEL.plist"

if launchctl print "gui/$(id -u)/$LABEL" >/dev/null 2>&1; then
  launchctl bootout "gui/$(id -u)/$LABEL" >/dev/null 2>&1 || true
fi

rm -f "$PLIST_DST"

echo "LaunchAgent supprime: $PLIST_DST"
