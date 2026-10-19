#!/bin/bash
# install-host-watch-launchd.sh — Installe le LaunchAgent de surveillance santé hôte.
set -e

PLIST_SRC="$HOME/PKA_JCH/_local/launchd-plists/com.dobby.pka-watch-host.plist"
PLIST_DST="$HOME/Library/LaunchAgents/com.dobby.pka-watch-host.plist"
LABEL="com.dobby.pka-watch-host"

echo "[Dobby] Installation de la surveillance santé hôte..."

cp "$PLIST_SRC" "$PLIST_DST"
echo "  ✓ plist copié → $PLIST_DST"

launchctl bootout gui/$(id -u)/$LABEL 2>/dev/null || true
launchctl bootstrap gui/$(id -u) "$PLIST_DST"
echo "  ✓ LaunchAgent démarré"

sleep 1
if launchctl print gui/$(id -u)/$LABEL &>/dev/null; then
    echo "  ✓ Surveillance active (test quotidien à 08:15)"
else
    echo "  ⚠️ Vérification échouée — 'launchctl list $LABEL'"
fi

echo ""
echo "[Dobby] Test manuel  : bin/pka-watch-host --check"
echo "[Dobby] Alerte test   : bin/pka-watch-host --alert"
echo "[Dobby] Arrêt         : launchctl bootout gui/\$(id -u)/$LABEL"
