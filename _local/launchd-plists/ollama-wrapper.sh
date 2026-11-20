#!/bin/bash
# Wrapper Dobby 🦉 (2026-11-15) — force le loopback + relaie vers Ollama 0.40.16.
# Le LaunchDaemon système com.pka.ollama pointe vers ce chemin ; le plist root
# contient encore OLLAMA_HOST=100.73.212.110, on le surcharge ici en 127.0.0.1.
export OLLAMA_HOST="127.0.0.1:11434"
exec /Users/m1/.local/ollama/ollama "$@"
