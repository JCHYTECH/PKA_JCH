#!/bin/bash
# install-loop-watcher.sh — Installe le LaunchAgent loop-watcher
set -e

PLIST_SRC="$HOME/PKA_JCH/_local/com.dobby.loop-watcher.plist"
PLIST_DST="$HOME/Library/LaunchAgents/com.dobby.loop-watcher.plist"

echo "[Dobby] Installation du Loop Watcher..."

# Copier le plist
cp "$PLIST_SRC" "$PLIST_DST"
echo "  ✓ plist copié → $PLIST_DST"

# Décharger si déjà actif
launchctl bootout gui/$(id -u)/com.dobby.loop-watcher 2>/dev/null || true

# Charger
launchctl bootstrap gui/$(id -u) "$PLIST_DST"
echo "  ✓ LaunchAgent démarré"

# Vérifier
sleep 1
if launchctl print gui/$(id -u)/com.dobby.loop-watcher &>/dev/null; then
    echo "  ✓ Loop Watcher actif (scan toutes les 5 minutes)"
else
    echo "  ⚠️ Vérification échouée — lance 'launchctl list com.dobby.loop-watcher'"
fi

echo ""
echo "[Dobby] Pour tester : python3 scripts/dobby_loop_watcher.py"
echo "[Dobby] Pour arrêter : launchctl bootout gui/\$(id -u)/com.dobby.loop-watcher"
