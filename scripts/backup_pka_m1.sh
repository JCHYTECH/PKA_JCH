#!/bin/bash
# Backup PKA_JCH → M1 via Thunderbolt (10.0.0.2)

SOURCE="/Users/jchavauxm5/PKA_JCH/"
DEST="m1@10.0.0.2:/Users/m1/Backups/PKA_JCH/"
LOG="/Users/jchavauxm5/PKA_JCH/_local/backup_pka_m1.log"

# Vérifier que M1 est joignable
if ! ssh -o ConnectTimeout=5 -o BatchMode=yes m1@10.0.0.2 exit 2>/dev/null; then
    echo "$(date '+%Y-%m-%d %H:%M') — M1 non joignable, backup ignoré" >> "$LOG"
    exit 0
fi

echo "$(date '+%Y-%m-%d %H:%M') — Début backup PKA_JCH → M1" >> "$LOG"

rsync -az --delete \
    --exclude='.git/' \
    --exclude='_local/' \
    --exclude='*.tmp' \
    --exclude='.DS_Store' \
    "$SOURCE" "$DEST" >> "$LOG" 2>&1

echo "$(date '+%Y-%m-%d %H:%M') — Fin backup (exit $?)" >> "$LOG"
