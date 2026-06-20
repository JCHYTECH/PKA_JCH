#!/bin/bash
# mount M1 datasets via SSHFS (macFUSE)
# Tries Thunderbolt (10.0.0.2) first for speed, falls back to Tailscale IP
set -euo pipefail

M1_USER="m1"
M1_THUNDERBOLT="10.0.0.2"
M1_TAILSCALE="${M1_IP:-100.73.212.110}"
M1_REMOTE="/Users/m1/datasets"
MOUNT_POINT="/Users/jchavauxm5/mnt/m1-datasets"
SSHFS_OPTS="reconnect,ServerAliveInterval=15,ServerAliveCountMax=3,noatime,nobrowse,defer_permissions"

mkdir -p "$MOUNT_POINT"

# Détecter et nettoyer un montage FUSE stale (mount | grep ne suffit pas)
if mount | grep -q "$MOUNT_POINT"; then
    # Vérifier que le montage répond réellement (timeout 2s)
    if timeout 2 ls "$MOUNT_POINT" &>/dev/null 2>&1; then
        echo "✅ $MOUNT_POINT déjà monté et actif"
        exit 0
    else
        echo "⚠️  Montage stale détecté — nettoyage..."
        diskutil unmountDisk force "$MOUNT_POINT" 2>/dev/null || true
        umount -f "$MOUNT_POINT" 2>/dev/null || true
        # Tuer les processus mount_macfuse orphelins sur ce point de montage
        pkill -9 -f "mount_macfuse.*m1-datasets" 2>/dev/null || true
        sleep 1
    fi
fi

echo "🔗 Montage SSHFS M1:$M1_REMOTE → $MOUNT_POINT ..."

if ping -c 1 -W 500 "$M1_THUNDERBOLT" &>/dev/null; then
    TARGET="$M1_THUNDERBOLT"
    LABEL="Thunderbolt"
elif ping -c 1 -W 2000 "$M1_TAILSCALE" &>/dev/null; then
    TARGET="$M1_TAILSCALE"
    LABEL="Tailscale"
else
    echo "❌ M1 inaccessible (Thunderbolt + Tailscale) — montage annulé"
    exit 1
fi

if /usr/local/bin/sshfs "${M1_USER}@${TARGET}:${M1_REMOTE}" "$MOUNT_POINT" -o "$SSHFS_OPTS" 2>&1; then
    echo "✅ Monté via $LABEL ($TARGET)"
else
    echo "❌ Échec SSHFS — vérifier SSH et accès M1"
    exit 1
fi
