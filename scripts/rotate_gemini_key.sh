#!/usr/bin/env bash
set -euo pipefail

SECRETS_DIR="$HOME/.config/pka-jch"
API_KEYS="$SECRETS_DIR/api_keys"
STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP_DIR="$SECRETS_DIR/backups/$STAMP-gemini"

umask 077
mkdir -p "$BACKUP_DIR"

if [[ -f "$API_KEYS" ]]; then
  cp "$API_KEYS" "$BACKUP_DIR/api_keys.bak"
fi

printf "Paste NEW Gemini API key. Input is hidden: "
IFS= read -r -s NEW_GEMINI_KEY
printf "\n"

if [[ -z "$NEW_GEMINI_KEY" ]]; then
  echo "Aborted: empty key."
  exit 1
fi

tmp="$(mktemp "$SECRETS_DIR/api_keys.XXXXXX")"
chmod 600 "$tmp"
seen_gemini=0

if [[ -f "$API_KEYS" ]]; then
  while IFS= read -r line || [[ -n "$line" ]]; do
    case "$line" in
      GEMINI_API_KEY=*)
        printf 'GEMINI_API_KEY=%s\n' "$NEW_GEMINI_KEY" >> "$tmp"
        seen_gemini=1
        ;;
      *)
        printf '%s\n' "$line" >> "$tmp"
        ;;
    esac
  done < "$API_KEYS"
fi

if [[ "$seen_gemini" -eq 0 ]]; then
  printf 'GEMINI_API_KEY=%s\n' "$NEW_GEMINI_KEY" >> "$tmp"
fi

mv "$tmp" "$API_KEYS"
chmod 600 "$API_KEYS"
unset NEW_GEMINI_KEY

echo "Gemini key updated locally."
echo "Backup: $BACKUP_DIR"
stat -f '%Sp %N' "$API_KEYS"
awk -F= '/^[A-Za-z_][A-Za-z0-9_]*=/{print $1}' "$API_KEYS" | sort
