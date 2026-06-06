#!/usr/bin/env bash
set -euo pipefail

SECRETS_DIR="$HOME/.config/pka-jch"
API_KEYS="$SECRETS_DIR/api_keys"
STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP_DIR="$SECRETS_DIR/backups/$STAMP-deepseek"

umask 077
mkdir -p "$BACKUP_DIR"

if [[ -f "$API_KEYS" ]]; then
  cp "$API_KEYS" "$BACKUP_DIR/api_keys.bak"
fi

printf "Paste NEW DeepSeek API key. Input is hidden: "
IFS= read -r -s NEW_DEEPSEEK_KEY
printf "\n"

if [[ -z "$NEW_DEEPSEEK_KEY" ]]; then
  echo "Aborted: empty key."
  exit 1
fi

tmp="$(mktemp "$SECRETS_DIR/api_keys.XXXXXX")"
chmod 600 "$tmp"
seen_deepseek=0

if [[ -f "$API_KEYS" ]]; then
  while IFS= read -r line || [[ -n "$line" ]]; do
    case "$line" in
      DEEPSEEK_API_KEY=*)
        printf 'DEEPSEEK_API_KEY=%s\n' "$NEW_DEEPSEEK_KEY" >> "$tmp"
        seen_deepseek=1
        ;;
      *)
        printf '%s\n' "$line" >> "$tmp"
        ;;
    esac
  done < "$API_KEYS"
fi

if [[ "$seen_deepseek" -eq 0 ]]; then
  printf 'DEEPSEEK_API_KEY=%s\n' "$NEW_DEEPSEEK_KEY" >> "$tmp"
fi

mv "$tmp" "$API_KEYS"
chmod 600 "$API_KEYS"
unset NEW_DEEPSEEK_KEY

echo "DeepSeek key updated locally."
echo "Backup: $BACKUP_DIR"
stat -f '%Sp %N' "$API_KEYS"
awk -F= '/^[A-Za-z_][A-Za-z0-9_]*=/{print $1}' "$API_KEYS" | sort
