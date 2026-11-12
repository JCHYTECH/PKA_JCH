#!/usr/bin/env zsh

PKA_DIR="/Users/jchavauxm5/PKA_JCH"
cd "$PKA_DIR" || exit 1

for TOOL in codex npx uvx; do
  if ! command -v "$TOOL" >/dev/null 2>&1; then
    echo "$TOOL est introuvable."
    exit 1
  fi
done

CODEX_BIN="$(command -v codex)"
NPX_BIN="$(command -v npx)"
UVX_BIN="$(command -v uvx)"

if [[ -z "${OPENROUTER_API_KEY:-}" ]]; then
  KEY_FILE="$HOME/.config/pka-jch/openrouter_key.txt"
  if [[ ! -r "$KEY_FILE" ]]; then
    echo "Définir OPENROUTER_API_KEY ou rendre $KEY_FILE lisible."
    exit 1
  fi
  export OPENROUTER_API_KEY="$(<"$KEY_FILE")"
fi

GROK_CONFIG=(
  --enable multi_agent
  -c 'mcp_optional_startup_grace_ms=0'
  -c "mcp_servers.pka_filesystem.command=\"$NPX_BIN\""
  -c "mcp_servers.pka_filesystem.args=[\"--offline\",\"-y\",\"@modelcontextprotocol/server-filesystem\",\"$PKA_DIR\"]"
  -c 'mcp_servers.pka_filesystem.required=true'
  -c 'mcp_servers.pka_filesystem.default_tools_approval_mode="approve"'
  -c "mcp_servers.pka_sqlite.command=\"$UVX_BIN\""
  -c "mcp_servers.pka_sqlite.args=[\"--offline\",\"--with\",\"mcp<2\",\"mcp-server-sqlite\",\"--db-path\",\"$PKA_DIR/TEAM/team.db\"]"
  -c 'mcp_servers.pka_sqlite.required=true'
  -c 'mcp_servers.pka_sqlite.enabled_tools=["list_tables","describe_table","read_query"]'
  -c 'mcp_servers.pka_sqlite.default_tools_approval_mode="approve"'
)

if [[ $# -eq 0 ]]; then
  set -- "$(<"$PKA_DIR/docs/system/bootstrap-forced.md")"$'\n\n## Règles runtime Grok/Codex\n- Pour les délégations natives, appelle `wait` sans `timeout_ms` : la sérialisation décimale des entiers est incompatible avec Codex.\n- Les serveurs MCP `pka_filesystem` et `pka_sqlite` sont requis. SQLite MCP expose uniquement les outils de lecture.'
fi

if [[ "${1:-}" == "exec" ]]; then
  shift
  exec "$CODEX_BIN" --profile openrouter --model x-ai/grok-4.7 exec "${GROK_CONFIG[@]}" "$@"
fi

exec "$CODEX_BIN" --profile openrouter --model x-ai/grok-4.7 "${GROK_CONFIG[@]}" "$@"
