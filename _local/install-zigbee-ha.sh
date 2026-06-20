#!/bin/bash
# Installer le dongle Zigbee dans Home Assistant Docker — macOS
# Usage : bash _local/install-zigbee-ha.sh
# À exécuter APRÈS avoir branché le dongle Zigbee USB sur le M5

set -e

echo "🔍 Détection du dongle Zigbee..."
ZIGBEE_DEV=""
for dev in /dev/tty.usbserial* /dev/tty.usbmodem* /dev/ttyUSB* /dev/ttyACM*; do
    if [ -e "$dev" ]; then
        ZIGBEE_DEV="$dev"
        echo "   ✅ Trouvé : $ZIGBEE_DEV"
        break
    fi
done

if [ -z "$ZIGBEE_DEV" ]; then
    echo "   ❌ Aucun dongle Zigbee détecté."
    echo "   macOS : /dev/tty.usbserial* ou /dev/tty.usbmodem*"
    echo "   Linux : /dev/ttyUSB0 ou /dev/ttyACM0"
    exit 1
fi

ZIGBEE_TCP_PORT=6638

# Kill any existing socat bridge
pkill -f "socat.*${ZIGBEE_TCP_PORT}" 2>/dev/null || true

echo ""
echo "🌉 Bridge série → TCP (port $ZIGBEE_TCP_PORT)..."
if command -v socat &>/dev/null; then
    socat TCP-LISTEN:${ZIGBEE_TCP_PORT},reuseaddr,fork FILE:${ZIGBEE_DEV},b57600,raw,echo=0 &
    SOCAT_PID=$!
    echo "   ✅ Bridge actif (PID $SOCAT_PID) — $ZIGBEE_DEV → tcp:$ZIGBEE_TCP_PORT"
else
    echo "   ❌ socat non installé."
    echo "   Installe avec : brew install socat"
    exit 1
fi
sleep 1

echo ""
echo "🛑 Arrêt du container Home Assistant..."
docker stop homeassistant 2>/dev/null || true
docker rm homeassistant 2>/dev/null || true

echo ""
echo "🚀 Démarrage de Home Assistant..."
docker run -d \
  --name homeassistant \
  --restart unless-stopped \
  --add-host host.docker.internal:host-gateway \
  -v /Users/jchavauxm5/PKA_JCH/_local/homeassistant:/config \
  -p 8123:8123 \
  ghcr.io/home-assistant/home-assistant:stable

echo ""
echo "✅ Container démarré."
echo ""
echo "📋 Étapes suivantes dans Home Assistant (http://localhost:8123) :"
echo "   1. Paramètres → Appareils & services → Ajouter une intégration"
echo "   2. Chercher « ZHA »"
echo "   3. Type de port : « Entrez un port série manuellement »"
echo "   4. Saisir : socket://host.docker.internal:${ZIGBEE_TCP_PORT}"
echo "   5. Radio type : laisser auto-détection"
echo ""
echo "🔗 Appairage du AirGuard TH :"
echo "   1. ZHA → Ajouter un appareil"
echo "   2. Appui long 5s sur le bouton du capteur (LED clignote)"
echo "   3. Le capteur apparaît automatiquement"
echo ""
echo "ℹ️  Le bridge socat tourne en arrière-plan (PID $SOCAT_PID)."
echo "   Pour l'arrêter : kill $SOCAT_PID"
