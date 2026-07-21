#!/bin/bash
# Serveur HTTP minimal pour l'outil Assiette Lupo
# Accessible depuis l'iPhone sur le même réseau WiFi
# Usage: bash _local/serve-assiette.sh [port]

PORT=${1:-8080}
DIR="$(cd "$(dirname "$0")/../JCH_Inbox/03_PROJECTS/11_IOT/iot-van/specs" && pwd)"

echo "🚐 Assiette Lupo — http://$(ipconfig getifaddr en0 2>/dev/null || hostname):${PORT}"
echo "   Ouvre cette URL sur ton iPhone, puis Ajouter à l'écran d'accueil"
echo "   Ctrl+C pour arrêter"
echo ""

python3 -m http.server ${PORT} --directory "${DIR}" 2>&1 | grep -v "^::"
