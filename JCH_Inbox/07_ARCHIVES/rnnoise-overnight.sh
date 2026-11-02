#!/usr/bin/env bash
# rnnoise-overnight.sh — Sync RPi + RNNoise batch nocturne
# v6 — Dobby 🦉 + Forge 🦦 — 2026-06-05
#
# Usage: bash rnnoise-overnight.sh          (test manuel)
#        crontab: 0 3 * * * bash /Users/jchavauxm5/PKA_JCH/scripts/rnnoise-overnight.sh
#
# Pipeline nocturne :
#   1. rsync des WAV depuis le RPi BirdNET vers raw/
#   2. RNNoise (ffmpeg arnndn) sur les fichiers de la veille
#   3. Purge raw > 30 jours + clean orphelins
set -euo pipefail

# === Config ===
USER_HOME="/Users/jchavauxm5"
PKA_ROOT="$USER_HOME/PKA_JCH"
RAW_DIR="${RNNOISE_RAW_DIR:-$PKA_ROOT/_local/audio/raw}"
OUT_DIR="${RNNOISE_OUT_DIR:-$PKA_ROOT/_local/audio/clean}"
LOG_DIR="$PKA_ROOT/_local/audio"
LOG_FILE="$LOG_DIR/rnnoise-overnight.log"
LOCK_FILE="/tmp/rnnoise-overnight.lock"
RNN_MODEL="${RNN_MODEL:-$PKA_ROOT/_local/audio/rnnoise_model.rnn}"
PURGE_AFTER_DAYS="${RNNOISE_PURGE_DAYS:-30}"
EXTENSIONS=("wav" "flac" "WAV" "FLAC")

# === Config RPi ===
RPI_HOST="${RPI_HOST:-100.66.110.60}"
RPI_USER="${RPI_USER:-jchavaux}"
RPI_WAV_DIR="${RPI_WAV_DIR:-/home/jchavaux/BirdSongs/StreamData/}"
SSH_OPTS="-o StrictHostKeyChecking=no -o ConnectTimeout=10 -o BatchMode=yes"

# Fuseau : CEST (UTC+2) — BirdNET sur RPi est en UTC, décalage de 2h
export TZ="${TZ:-Europe/Brussels}"

# === Pré-vérifications ===
if ! command -v ffmpeg &>/dev/null; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') ✗ ffmpeg introuvable" >> "$LOG_FILE"
    exit 1
fi
if ! ffmpeg -hide_banner -filters 2>/dev/null | grep arnndn >/dev/null; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') ✗ ffmpeg n'a pas le filtre arnndn" >> "$LOG_FILE"
    exit 1
fi
if [[ ! -f "$RNN_MODEL" ]]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') ✗ Modèle RNNoise introuvable: $RNN_MODEL" >> "$LOG_FILE"
    exit 1
fi

# === Guard: single instance ===
if ! (set -o noclobber; echo "$$" > "$LOCK_FILE") 2>/dev/null; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') ⏭ Déjà en cours, sortie." >> "$LOG_FILE"
    exit 0
fi
trap 'rm -f "$LOCK_FILE"' EXIT

# === Init ===
mkdir -p "$RAW_DIR" "$OUT_DIR" "$LOG_DIR"
echo "" >> "$LOG_FILE"
echo "========================================" >> "$LOG_FILE"
echo "$(date '+%Y-%m-%d %H:%M:%S') — Batch RNNoise v6 start" >> "$LOG_FILE"

# ============================================
# PHASE 1: rsync depuis le RPi
# ============================================
echo "$(date '+%Y-%m-%d %H:%M:%S') — Phase 1: rsync $RPI_USER@$RPI_HOST:$RPI_WAV_DIR" >> "$LOG_FILE"
if rsync -avz --progress --include="*/" --include="*.wav" --include="*.flac" --include="*.WAV" --include="*.FLAC" --exclude="*" \
    -e "ssh $SSH_OPTS" \
    "$RPI_USER@$RPI_HOST:$RPI_WAV_DIR" \
    "$RAW_DIR/" 2>>"$LOG_FILE"; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') ✓ rsync terminé" >> "$LOG_FILE"
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') ✗ rsync échoué (RPi hors ligne ?) — continue avec fichiers présents" >> "$LOG_FILE"
fi

# ============================================
# PHASE 2: RNNoise (veille uniquement)
# ============================================
YESTERDAY_START="$(date -v-1d '+%Y-%m-%d') 00:00:00"
TODAY_START="$(date '+%Y-%m-%d') 00:00:00"

echo "$(date '+%Y-%m-%d %H:%M:%S') — Phase 2: RNNoise $YESTERDAY_START → $TODAY_START" >> "$LOG_FILE"

processed=0; skipped=0; failed=0; in_use=0
is_file_open() { lsof "$1" &>/dev/null; }

for ext in "${EXTENSIONS[@]}"; do
    while IFS= read -r -d '' file; do
        basename="$(basename "$file")"
        stem="${basename%.*}"
        out="$OUT_DIR/${stem}_clean.wav"

        [[ -f "$out" ]] && { skipped=$((skipped + 1)); continue; }
        is_file_open "$file" && { in_use=$((in_use + 1)); echo "$(date '+%Y-%m-%d %H:%M:%S') ⏳ En cours: $basename" >> "$LOG_FILE"; continue; }

        if nice -n 10 ffmpeg -y -hide_banner -loglevel error \
            -i "$file" \
            -af "arnndn=m='$RNN_MODEL'" \
            -ar 48000 -ac 1 -sample_fmt s16 \
            "$out" 2>>"$LOG_FILE"; then
            processed=$((processed + 1))
            echo "$(date '+%Y-%m-%d %H:%M:%S') ✓ $basename" >> "$LOG_FILE"
        else
            failed=$((failed + 1))
            echo "$(date '+%Y-%m-%d %H:%M:%S') ✗ ÉCHEC: $basename" >> "$LOG_FILE"
            rm -f "$out"
        fi
    done < <(find "$RAW_DIR" -type f -name "*.$ext" \
        -newermt "$YESTERDAY_START" \
        ! -newermt "$TODAY_START" \
        -print0 2>/dev/null)
done

# ============================================
# PHASE 3: Purge raw > N jours
# ============================================
purged=0
while IFS= read -r -d '' old_file; do
    is_file_open "$old_file" && { echo "$(date '+%Y-%m-%d %H:%M:%S') ⏳ Purge skip: $(basename "$old_file")" >> "$LOG_FILE"; continue; }
    rm -f "$old_file" && purged=$((purged + 1))
done < <(find "$RAW_DIR" -type f \( -name "*.wav" -o -name "*.flac" -o -name "*.WAV" -o -name "*.FLAC" \) -mtime +${PURGE_AFTER_DAYS} -print0 2>/dev/null)

# === Orphelins ===
orphans=0
shopt -s nullglob
for clean in "$OUT_DIR"/*_clean.wav; do
    raw_stem="${clean%.wav}"; raw_stem="${raw_stem%_clean}"
    found=0
    for ext in wav flac WAV FLAC; do
        [[ -f "$RAW_DIR/$(basename "$raw_stem").$ext" ]] && { found=1; break; }
    done
    [[ "$found" -eq 0 ]] && rm -f "$clean" && orphans=$((orphans + 1))
done

# === Summary ===
echo "$(date '+%Y-%m-%d %H:%M:%S') — Batch done: $processed traités, $skipped skip, $in_use en cours, $failed échecs, $purged purgés, $orphans orphelins" >> "$LOG_FILE"

# === Notification desktop ===
[[ "$failed" -gt 0 ]] && osascript -e "display notification \"$processed traités, $failed échecs — voir log\" with title \"RNNoise batch — $failed échec(s)\"" 2>/dev/null || true
