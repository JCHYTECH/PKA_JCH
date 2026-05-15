#!/usr/bin/env zsh
# Lance le serveur local des dashboards PKA.

PKA_DIR="$(cd "$(dirname "$0")" && pwd)"
PORT="${PKA_DASHBOARD_PORT:-8787}"

cd "$PKA_DIR"

echo "Dobby — dashboards PKA"
echo "URL : http://127.0.0.1:$PORT"
echo ""

exec python3 "$PKA_DIR/scripts/dashboard_server.py" --host 127.0.0.1 --port "$PORT"
