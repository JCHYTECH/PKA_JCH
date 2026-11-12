#!/bin/bash
# install-box-watch-launchd.sh — Installe le LaunchAgent de surveillance de la box Proximus.
set -e

PLIST_SRC="$HOME/PKA_JCH/_local/launchd-plists/com.dobby.pka-watch-box.plist"
PLIST_DST="$HOME/Library/LaunchAgents/com.dobby.pka-watch-box.plist"
LABEL="com.dobby.pka-watch-box"

echo "[Dobby] Installation de la surveillance box Proximus..."

cp "$PLIST_SRC" "$PLIST_DST"
echo "  ✓ plist copié → $PLIST_DST"

launchctl bootout gui/$(id -u)/$LABEL 2>/dev/null || true
launchctl bootstrap gui/$(id -u) "$PLIST_DST"
echo "  ✓ LaunchAgent démarré"

sleep 1
if launchctl print gui/$(id -u)/$LABEL &>/dev/null; then
    echo "  ✓ Surveillance active (08:00 et 11:00, 15 min — mail si anomalie)"
else
    echo "  ⚠️ Vérification échouée — 'launchctl list $LABEL'"
fi

echo ""
echo "[Dobby] Test manuel  : BOX_WATCH_DURATION=30 bin/pka-watch-box --check"
echo "[Dobby] Test mail    : BOX_WATCH_DURATION=30 bin/pka-watch-box --alert"
echo "[Dobby] Arrêt        : launchctl bootout gui/\$(id -u)/$LABEL"
