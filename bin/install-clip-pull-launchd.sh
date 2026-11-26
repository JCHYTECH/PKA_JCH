#!/bin/bash
# install-clip-pull-launchd.sh — Installe le LaunchAgent du pull auto des clips iPad.
set -e

PLIST_SRC="$HOME/PKA_JCH/_local/launchd-plists/com.dobby.pka-clip-pull.plist"
PLIST_DST="$HOME/Library/LaunchAgents/com.dobby.pka-clip-pull.plist"
LABEL="com.dobby.pka-clip-pull"

echo "[Dobby] Installation du pull auto des clips iPad (toutes les 15 min)..."

cp "$PLIST_SRC" "$PLIST_DST"
echo "  ✓ plist copié → $PLIST_DST"

launchctl bootout gui/$(id -u)/$LABEL 2>/dev/null || true
launchctl bootstrap gui/$(id -u) "$PLIST_DST"
echo "  ✓ LaunchAgent démarré"

sleep 1
if launchctl print gui/$(id -u)/$LABEL &>/dev/null; then
    echo "  ✓ Pull auto actif (toutes les 15 min)"
else
    echo "  ⚠️ Vérification échouée — 'launchctl list $LABEL'"
fi

echo ""
echo "[Dobby] Test manuel  : bin/pka-clip-pull --list"
echo "[Dobby] Pull immédiat : bin/pka-clip-pull --apply"
echo "[Dobby] Arrêt         : launchctl bootout gui/\$(id -u)/$LABEL"
