#!/usr/bin/env bash
set -euo pipefail

SECRETS_DIR="$HOME/.config/pka-jch"
API_KEYS="$SECRETS_DIR/api_keys"
ANTHROPIC_FILE="$SECRETS_DIR/anthropic_key.txt"
STAMP="$(date +%Y%m%d-%H%M%S)"
BACKUP_DIR="$SECRETS_DIR/backups/$STAMP"

umask 077
mkdir -p "$BACKUP_DIR"

if [[ -f "$API_KEYS" ]]; then
  cp "$API_KEYS" "$BACKUP_DIR/api_keys.bak"
fi
if [[ -f "$ANTHROPIC_FILE" ]]; then
  cp "$ANTHROPIC_FILE" "$BACKUP_DIR/anthropic_key.txt.bak"
fi

printf "Paste NEW OpenAI API key. Input is hidden: "
IFS= read -r -s NEW_OPENAI_KEY
printf "\nPaste NEW Anthropic API key. Input is hidden: "
IFS= read -r -s NEW_ANTHROPIC_KEY
printf "\n"

if [[ -z "$NEW_OPENAI_KEY" || -z "$NEW_ANTHROPIC_KEY" ]]; then
  echo "Aborted: one of the keys was empty."
  exit 1
fi

tmp="$(mktemp "$SECRETS_DIR/api_keys.XXXXXX")"
chmod 600 "$tmp"

seen_openai=0
seen_claude=0
seen_anthropic=0

if [[ -f "$API_KEYS" ]]; then
  while IFS= read -r line || [[ -n "$line" ]]; do
    case "$line" in
      OPENAI_API_KEY=*)
        printf 'OPENAI_API_KEY=%s\n' "$NEW_OPENAI_KEY" >> "$tmp"
        seen_openai=1
        ;;
      CLAUDE_API_KEY=*)
        printf 'CLAUDE_API_KEY=%s\n' "$NEW_ANTHROPIC_KEY" >> "$tmp"
        seen_claude=1
        ;;
      ANTHROPIC_API_KEY=*)
        printf 'ANTHROPIC_API_KEY=%s\n' "$NEW_ANTHROPIC_KEY" >> "$tmp"
        seen_anthropic=1
        ;;
      *)
        printf '%s\n' "$line" >> "$tmp"
        ;;
    esac
  done < "$API_KEYS"
fi

if [[ "$seen_openai" -eq 0 ]]; then
  printf 'OPENAI_API_KEY=%s\n' "$NEW_OPENAI_KEY" >> "$tmp"
fi
if [[ "$seen_claude" -eq 0 ]]; then
  printf 'CLAUDE_API_KEY=%s\n' "$NEW_ANTHROPIC_KEY" >> "$tmp"
fi
if [[ "$seen_anthropic" -eq 0 ]]; then
  printf 'ANTHROPIC_API_KEY=%s\n' "$NEW_ANTHROPIC_KEY" >> "$tmp"
fi

mv "$tmp" "$API_KEYS"
chmod 600 "$API_KEYS"
printf '%s\n' "$NEW_ANTHROPIC_KEY" > "$ANTHROPIC_FILE"
chmod 600 "$ANTHROPIC_FILE"

unset NEW_OPENAI_KEY NEW_ANTHROPIC_KEY

echo "Rotation written locally."
echo "Backups: $BACKUP_DIR"
stat -f '%Sp %N' "$API_KEYS" "$ANTHROPIC_FILE"
awk -F= '/^[A-Za-z_][A-Za-z0-9_]*=/{print $1}' "$API_KEYS" | sort
