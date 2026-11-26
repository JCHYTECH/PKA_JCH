#!/bin/bash
# Installe le launchd pour le skill generator hebdomadaire
# Usage : bash bin/install-skill-generator-launchd.sh

set -e

PLIST_SRC="$HOME/PKA_JCH/_local/com.dobby.skill-generator.plist"
PLIST_DST="$HOME/Library/LaunchAgents/com.dobby.skill-generator.plist"

if [ ! -f "$PLIST_SRC" ]; then
    echo "❌ Plist source introuvable : $PLIST_SRC"
    exit 1
fi

# Vérifier que le script cron est exécutable
chmod +x "$HOME/PKA_JCH/scripts/cron-skill-generator.sh"

# Copier le plist
cp "$PLIST_SRC" "$PLIST_DST"
echo "✅ Plist installé dans $PLIST_DST"

# Charger
launchctl unload "$PLIST_DST" 2>/dev/null || true
launchctl load "$PLIST_DST"
echo "✅ Launchd chargé — exécution chaque dimanche à 22h"

# Vérifier
echo ""
echo "📋 Statut :"
launchctl list com.dobby.skill-generator
