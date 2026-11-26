#!/bin/bash
# install-overpass-backfill-launchd.sh — Installe le LaunchAgent de backfill Overpass.
set -e

PLIST_SRC="$HOME/PKA_JCH/_local/launchd-plists/com.dobby.overpass-backfill.plist"
PLIST_DST="$HOME/Library/LaunchAgents/com.dobby.overpass-backfill.plist"
LABEL="com.dobby.overpass-backfill"

echo "[Dobby] Installation du backfill Overpass..."

cp "$PLIST_SRC" "$PLIST_DST"
echo "  ✓ plist copié → $PLIST_DST"

launchctl bootout gui/$(id -u)/$LABEL 2>/dev/null || true
launchctl bootstrap gui/$(id -u) "$PLIST_DST"
echo "  ✓ LaunchAgent démarré"

sleep 1
if launchctl print gui/$(id -u)/$LABEL &>/dev/null; then
    echo "  ✓ Backfill Overpass actif (test toutes les heures)"
else
    echo "  ⚠️ Vérification échouée — 'launchctl list $LABEL'"
fi

echo ""
echo "[Dobby] Test manuel : bash bin/overpass-backfill"
echo "[Dobby] Arrêt      : launchctl bootout gui/\$(id -u)/$LABEL"
