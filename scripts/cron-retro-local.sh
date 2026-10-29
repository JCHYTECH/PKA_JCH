#!/bin/bash
# Dobby retro quotidienne — M5 local
# Lance à 23h via launchd (com.dobby.retro)
cd ~/PKA_JCH || { echo "PKA_JCH introuvable"; exit 1; }

PYTHON="/Library/Frameworks/Python.framework/Versions/3.13/bin/python3"

echo "[$(date)] Dobby retro start"
$PYTHON scripts/dobby_retro.py --provider openrouter 2>&1
RETRO_EXIT=$?
echo "[$(date)] Dobby retro done (exit=$RETRO_EXIT)"

# Bridge Dobby -> Codex (silencieux si absent)
if [ -f scripts/dobby_codex_bridge.py ]; then
    $PYTHON scripts/dobby_codex_bridge.py 2>&1 || true
fi