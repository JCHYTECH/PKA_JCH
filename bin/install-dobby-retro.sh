#!/bin/bash
# Installer la rétro quotidienne Dobby dans launchd
# Usage : bash bin/install-dobby-retro.sh

PLIST_SRC="$HOME/PKA_JCH/_local/com.dobby.retro.plist"
PLIST_DST="$HOME/Library/LaunchAgents/com.dobby.retro.plist"

cp "$PLIST_SRC" "$PLIST_DST" 2>/dev/null || {
    echo "❌ Copie impossible — essaie avec sudo :"
    echo "sudo cp $PLIST_SRC $PLIST_DST"
    echo "sudo chown $USER $PLIST_DST"
    exit 1
}

chmod 644 "$PLIST_DST"
launchctl load "$PLIST_DST" 2>&1 && echo "✅ Rétro programmée à 23h (launchd)" || echo "⚠️ launchctl load a échoué"

echo ""
echo "Vérification : launchctl list | grep dobby.retro"
launchctl list | grep dobby.retro
