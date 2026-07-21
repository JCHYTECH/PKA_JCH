#!/bin/bash
# ============================================================
# Lupo Planner 🐺 — Deploy script
# ============================================================
# Options:
#   1. Local dev:        ./deploy.sh dev
#   2. Home Assistant:   ./deploy.sh ha          (serves via HA www/)
#   3. RPi standalone:   ./deploy.sh rpi         (serves via python http.server)
# ============================================================
set -e

DIR="$(cd "$(dirname "$0")" && pwd)"
MODE="${1:-dev}"
PORT="${2:-8088}"

case "$MODE" in
  dev)
    echo "🐺 Lupo Planner — dev mode on http://localhost:${PORT}"
    echo "   Open in browser. Ctrl+C to stop."
    cd "$DIR" && python3 -m http.server "$PORT"
    ;;

  ha)
    # Copy to Home Assistant www folder
    HA_WWW="/Users/jchavauxm5/PKA_JCH/_local/homeassistant/www/lupo-planner"
    echo "🐺 Deploying to HA www/ ($HA_WWW)..."
    mkdir -p "$HA_WWW"
    cp "$DIR/index.html" "$DIR/manifest.json" "$DIR/sw.js" "$HA_WWW/"
    echo "✅ Deployed to HA."
    echo "   Access: http://homeassistant.local:8123/local/lupo-planner/"
    echo "   Or via Tailscale: http://<ha-tailscale-ip>:8123/local/lupo-planner/"
    ;;

  rpi)
    echo "🐺 Lupo Planner — starting server on 0.0.0.0:${PORT}"
    echo "   [M5] cd $DIR && python3 -m http.server ${PORT} --bind 0.0.0.0"
    cd "$DIR" && python3 -m http.server "$PORT" --bind 0.0.0.0
    ;;

  *)
    echo "Usage: ./deploy.sh [dev|ha|rpi] [port]"
    ;;
esac
