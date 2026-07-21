#!/usr/bin/env bash
# whisper-dictate.sh — Dictée vocale Whisper dans le terminal macOS
# Démarre l'enregistrement, attend Ctrl+C pour stopper, transcrit, colle le texte.
# Usage : whisper-dictate.sh [--print]
#   --print  : afficher le texte au lieu de le coller
# Nécessite : ffmpeg, curl, jq, le serveur whisper-server.py sur localhost:4444

set -euo pipefail

PORT=4444
API_KEY="localhost-key-must-be-set"
TMP_WAV="/tmp/whisper-dictate-$$.wav"
PRINT_ONLY="${1:-}"

# Vérifier que le serveur tourne
if ! curl -s --max-time 2 "http://localhost:${PORT}/health" >/dev/null 2>&1; then
    echo "❌ Serveur Whisper non disponible sur localhost:${PORT}" >&2
    echo "   Démarrer : launchctl load ~/Library/LaunchAgents/com.dobby.whisper-server.plist" >&2
    exit 1
fi

# Enregistrement — :1 = MacBook Pro Microphone
echo "🎤 Enregistrement... (Ctrl+C pour stopper)"
ffmpeg -y -f avfoundation -i ":1" -ac 1 -ar 16000 -sample_fmt s16 "${TMP_WAV}" >/dev/null 2>&1 &
FFPID=$!

# Attendre Ctrl+C
trap 'kill -INT $FFPID 2>/dev/null' INT
wait $FFPID 2>/dev/null || true

echo "⏳ Transcription..."

# Transcription
RESPONSE=$(curl -s --max-time 30 -X POST "http://localhost:${PORT}/v1/audio/transcriptions" \
    -H "Authorization: Bearer ${API_KEY}" \
    -F "file=@${TMP_WAV}" \
    -F "response_format=verbose_json" 2>/dev/null)

# Nettoyer
rm -f "${TMP_WAV}"

# Extraire le texte
TEXT=$(echo "${RESPONSE}" | jq -r '.text // empty' 2>/dev/null)

if [ -z "${TEXT}" ]; then
    echo "❌ Transcription vide ou erreur" >&2
    echo "   Réponse : ${RESPONSE}" >&2
    exit 1
fi

if [ "${PRINT_ONLY}" = "--print" ]; then
    echo "${TEXT}"
else
    # Copier dans le clipboard et simuler Cmd+V
    echo -n "${TEXT}" | pbcopy
    # Coller via AppleScript
    osascript -e 'tell application "System Events" to keystroke "v" using command down' 2>/dev/null
    echo "✅ Collé : ${TEXT}" >&2
fi
