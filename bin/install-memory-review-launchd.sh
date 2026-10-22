#!/bin/bash
# install-memory-review-launchd.sh — Installe le LaunchAgent de la boucle mémoire
set -e

PLIST_SRC="$HOME/PKA_JCH/_local/launchd-plists/com.dobby.pka-memory-review.plist"
PLIST_DST="$HOME/Library/LaunchAgents/com.dobby.pka-memory-review.plist"

echo "[Dobby] Installation de la boucle mémoire autonome (review + skills)..."

cp "$PLIST_SRC" "$PLIST_DST"
echo "  ✓ plist copié → $PLIST_DST"

launchctl bootout gui/$(id -u)/com.dobby.pka-memory-review 2>/dev/null || true
launchctl bootstrap gui/$(id -u) "$PLIST_DST"
echo "  ✓ LaunchAgent démarré"

sleep 1
if launchctl print gui/$(id -u)/com.dobby.pka-memory-review &>/dev/null; then
    echo "  ✓ Boucle mémoire active (quotidien 09:15)"
else
    echo "  ⚠️ Vérification échouée — lance 'launchctl list com.dobby.pka-memory-review'"
fi

echo ""
echo "[Dobby] Pour tester : bin/pka-memory-loop"
echo "[Dobby] Pour arrêter : launchctl bootout gui/\$(id -u)/com.dobby.pka-memory-review"
