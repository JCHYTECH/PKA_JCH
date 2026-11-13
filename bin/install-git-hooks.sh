#!/usr/bin/env bash
# install-git-hooks.sh — active le hook pre-commit versionné (scripts/hooks/pre-commit).
# Idempotent : à exécuter une fois par clone (M5, iMac, autre machine).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

git config core.hooksPath scripts/hooks

echo "core.hooksPath = $(git config core.hooksPath)"
if [ -x scripts/hooks/pre-commit ]; then
  echo "hook présent : OUI ($(git config core.hooksPath)/pre-commit)"
else
  echo "hook présent : NON — vérifier scripts/hooks/pre-commit" >&2
  exit 1
fi
