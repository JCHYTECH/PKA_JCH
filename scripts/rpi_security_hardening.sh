#!/usr/bin/env bash
set -euo pipefail

STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP_DIR="$HOME/pka-security-backups/$STAMP"

echo "[1/5] Creating backup directory: $BACKUP_DIR"
mkdir -p "$BACKUP_DIR"

echo "[2/5] Backing up x11vnc systemd unit if present"
if systemctl list-unit-files x11vnc.service >/dev/null 2>&1; then
  systemctl cat x11vnc.service > "$BACKUP_DIR/x11vnc.service.txt" || true
fi

echo "[3/5] Disabling unauthenticated x11vnc service"
if systemctl is-active --quiet x11vnc.service; then
  sudo systemctl stop x11vnc.service
fi
if systemctl is-enabled --quiet x11vnc.service; then
  sudo systemctl disable x11vnc.service
fi

echo "[4/5] Applying available package updates"
sudo apt-get update
sudo apt-get upgrade -y

echo "[5/5] Verification"
echo "x11vnc active:"
systemctl is-active x11vnc.service || true
echo "x11vnc enabled:"
systemctl is-enabled x11vnc.service || true
echo "Listening TCP ports:"
ss -tulpen | sed -n '1,80p'

echo "Backup written to: $BACKUP_DIR"
