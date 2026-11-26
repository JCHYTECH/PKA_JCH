#!/bin/bash
# install-ollama-system.sh — Installe Ollama en daemon SYSTEME (loopback) sur le M1.
# Exécuter sur le M1 (demande le mot de passe sudo M1 UNE fois) :
#   ssh -t m1@100.73.212.110 'bash /Users/m1/.local/launchd/install-ollama-system.sh'
set -euo pipefail

SRC_PLIST="/Users/m1/.local/launchd/com.pka.ollama.plist"
DST_PLIST="/Library/LaunchDaemons/com.pka.ollama.plist"

echo "=== 1/6 backup ancien plist système ==="
if sudo cp -a "$DST_PLIST" "${DST_PLIST}.bak-20261115" 2>/dev/null; then
  echo "backup OK -> ${DST_PLIST}.bak-20261115"
else
  echo "(pas d'ancien plist à backuper)"
fi

echo "=== 2/6 arrêt + désactivation agent utilisateur (gui/501) ==="
launchctl bootout gui/501/com.pka.ollama 2>/dev/null || echo "(agent gui déjà arrêté)"
launchctl disable gui/501/com.pka.ollama 2>/dev/null || echo "(disable gui : ok/absent)"

echo "=== 3/6 copie nouveau plist système (loopback 127.0.0.1) ==="
sudo cp "$SRC_PLIST" "$DST_PLIST"
sudo chown root:wheel "$DST_PLIST"
sudo chmod 644 "$DST_PLIST"

echo "=== 4/6 activation + rechargement daemon système ==="
sudo launchctl enable system/com.pka.ollama
sudo launchctl bootout system/com.pka.ollama 2>/dev/null || echo "(bootout : rien à arrêter)"
sudo launchctl bootstrap system "$DST_PLIST"

echo "=== 5/6 attente ==="
sleep 4

echo "=== 6/6 vérification ==="
echo -n "version loopback : "; curl -s --max-time 5 http://127.0.0.1:11434/api/version; echo
echo -n "Tailscale 11434   : "; curl -s --max-time 3 http://100.73.212.110:11434/api/version >/dev/null 2>&1 && echo "⚠️ ENCORE ACCESSIBLE" || echo "✅ refusé (loopback seul)"
sudo launchctl list | grep -i ollama
lsof -iTCP:11434 -sTCP:LISTEN -n -P
echo "=== TERMINÉ ==="
