#!/usr/bin/env bash
set -euo pipefail

SECRETS_DIR="$HOME/.config/pka-jch"
KEY_FILE="$SECRETS_DIR/openrouter_key.txt"
STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP_DIR="$SECRETS_DIR/backups/$STAMP-openrouter"

umask 077
mkdir -p "$BACKUP_DIR"

if [[ -f "$KEY_FILE" ]]; then
  cp "$KEY_FILE" "$BACKUP_DIR/openrouter_key.txt.bak"
fi

printf "Paste NEW OpenRouter API key. Input is hidden: "
IFS= read -r -s NEW_OPENROUTER_KEY
printf "\n"

if [[ -z "$NEW_OPENROUTER_KEY" ]]; then
  echo "Aborted: empty key."
  exit 1
fi

printf '%s\n' "$NEW_OPENROUTER_KEY" > "$KEY_FILE"
chmod 600 "$KEY_FILE"
unset NEW_OPENROUTER_KEY

echo "OpenRouter key updated locally."
echo "Backup: $BACKUP_DIR"
stat -f '%Sp %N' "$KEY_FILE"
