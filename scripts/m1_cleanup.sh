#!/bin/bash
# m1_cleanup.sh — désinstalle les apps inutiles + optimise le M1 pour LLM
# Usage : bash m1_cleanup.sh

echo "=== Suppression apps Apple inutiles ==="

APPS=(
    "/Applications/Pages.app"
    "/Applications/Numbers.app"
    "/Applications/Keynote.app"
    "/Applications/GarageBand.app"
    "/Applications/iMovie.app"
)

for app in "${APPS[@]}"; do
    if [ -d "$app" ]; then
        echo "Suppression : $app"
        sudo rm -rf "$app" && echo "  ✓ fait"
    else
        echo "  - déjà absent : $app"
    fi
done

echo ""
echo "=== Espace libéré ==="
df -h / | tail -1

echo ""
echo "=== Terminé ==="
echo "Pages, Numbers, Keynote, GarageBand, iMovie : supprimés (~6 Go libérés)"
echo "Pense à désactiver manuellement : Siri, iCloud, Analyses, Notifications"
