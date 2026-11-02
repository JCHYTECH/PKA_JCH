#!/bin/bash
# PKA Vault Backup → M1 (via Tailscale SSH)
# Exclut les fichiers lourds inutiles : .git, node_modules, _local, outputs, tmp

set -e

SRC="$HOME/PKA_JCH"
DST="m1@100.73.212.110:backups/PKA_JCH"
LOG="$HOME/PKA_JCH/scripts/logs/vault_backup.log"

mkdir -p "$(dirname "$LOG")"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Backup start" >> "$LOG"

rsync -avz --delete \
    --exclude '.git/' \
    --exclude 'node_modules/' \
    --exclude '_local/' \
    --exclude 'outputs/' \
    --exclude 'tmp/' \
    --exclude '.DS_Store' \
    --exclude '*.log' \
    -e "ssh -o ConnectTimeout=10" \
    "$SRC/" "$DST/" >> "$LOG" 2>&1

echo "[$(date '+%Y-%m-%d %H:%M:%S')] Backup OK" >> "$LOG"
