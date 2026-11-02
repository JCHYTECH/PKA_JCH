#!/bin/zsh
set -euo pipefail

echo "=== PKA Email — Installation complete ==="

# 1. Config Outlook
mkdir -p ~/.config/pka-jch
cp ~/PKA_JCH/docs/system/outlook_config.json ~/.config/pka-jch/outlook_config.json
echo "OK Config Outlook"

# 2. Email Digest (9h, 14h, 20h)
LABEL_DIGEST="com.jchytech.pka-email-digest"
SRC_DIGEST="$HOME/PKA_JCH/scripts/launchd/${LABEL_DIGEST}.plist"
DST_DIGEST="$HOME/Library/LaunchAgents/${LABEL_DIGEST}.plist"
launchctl bootout "gui/$(id -u)/$LABEL_DIGEST" 2>/dev/null || true
cp "$SRC_DIGEST" "$DST_DIGEST"
launchctl bootstrap "gui/$(id -u)" "$DST_DIGEST"
echo "OK Email Digest"

# 3. Outlook Gatekeeper (toutes les 15 min)
LABEL_OUTLOOK="com.jchytech.pka-outlook-gatekeeper"
SRC_OUTLOOK="$HOME/PKA_JCH/scripts/launchd/${LABEL_OUTLOOK}.plist"
DST_OUTLOOK="$HOME/Library/LaunchAgents/${LABEL_OUTLOOK}.plist"
launchctl bootout "gui/$(id -u)/$LABEL_OUTLOOK" 2>/dev/null || true
cp "$SRC_OUTLOOK" "$DST_OUTLOOK"
launchctl bootstrap "gui/$(id -u)" "$DST_OUTLOOK"
echo "OK Outlook Gatekeeper"

# 4. Dropbox Watch
LABEL_DBX="com.jchytech.pka-dropbox-watch"
if launchctl print "gui/$(id -u)/$LABEL_DBX" >/dev/null 2>&1; then
  echo "OK Dropbox Watch (deja la)"
else
  SRC_DBX="$HOME/PKA_JCH/scripts/launchd/${LABEL_DBX}.plist"
  DST_DBX="$HOME/Library/LaunchAgents/${LABEL_DBX}.plist"
  cp "$SRC_DBX" "$DST_DBX"
  launchctl bootstrap "gui/$(id -u)" "$DST_DBX"
  echo "OK Dropbox Watch"
fi

# 5. Gmail Gatekeeper (check)
LABEL_GMAIL="com.jchytech.pka-gmail-gatekeeper"
if launchctl print "gui/$(id -u)/$LABEL_GMAIL" >/dev/null 2>&1; then
  echo "OK Gmail Gatekeeper"
else
  echo "ATTENTION Gmail Gatekeeper manquant"
fi

echo ""
echo "=== Fini ==="
echo "Outlook : un code apparaitra dans ~/PKA_JCH/tmp/outlook-gatekeeper.log"
echo "          A entrer sur https://microsoft.com/devicelogin"
