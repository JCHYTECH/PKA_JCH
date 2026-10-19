#!/bin/bash
# install-bluetti-price-watch-launchd.sh — Installe le LaunchAgent de surveillance de prix Bluetti.
set -e

PLIST_SRC="$HOME/PKA_JCH/_local/launchd-plists/com.dobby.pka-watch-bluetti.plist"
PLIST_DST="$HOME/Library/LaunchAgents/com.dobby.pka-watch-bluetti.plist"
LABEL="com.dobby.pka-watch-bluetti"

echo "[Dobby] Installation de la surveillance de prix Bluetti..."

cp "$PLIST_SRC" "$PLIST_DST"
echo "  ✓ plist copié → $PLIST_DST"

launchctl bootout gui/$(id -u)/$LABEL 2>/dev/null || true
launchctl bootstrap gui/$(id -u) "$PLIST_DST"
echo "  ✓ LaunchAgent démarré"

sleep 1
if launchctl print gui/$(id -u)/$LABEL &>/dev/null; then
    echo "  ✓ Surveillance active (test quotidien à 08:00)"
else
    echo "  ⚠️ Vérification échouée — 'launchctl list $LABEL'"
fi

echo ""
echo "[Dobby] Test manuel  : bin/pka-watch-bluetti --check"
echo "[Dobby] Alerte test   : bin/pka-watch-bluetti --alert"
echo "[Dobby] Arrêt         : launchctl bootout gui/\$(id -u)/$LABEL"
