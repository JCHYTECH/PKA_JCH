#!/bin/bash
set -euo pipefail

curl --ipv6 --noproxy '*' --silent --show-error --fail --max-time 5 \
  -g 'http://[::1]:8123/.well-known/oauth-authorization-server' | \
  python3 -c 'import json, sys; metadata = json.load(sys.stdin); assert metadata.get("issuer") == "http://localhost:8123", "Unexpected Home Assistant relay identity"'

export NODE_OPTIONS="${NODE_OPTIONS:+$NODE_OPTIONS }--dns-result-order=ipv6first"
exec npx -y -p mcp-remote@0.16.1 mcp-remote \
  http://localhost:8123/api/mcp 1455 \
  --host 127.0.0.1 \
  --static-oauth-client-info '{"client_id":"http://127.0.0.1:1455"}' \
  --static-oauth-client-metadata '{"scope":"openid"}' \
  --transport http-only \
  --protocol auto \
  --ignore-tool todo__get_items \
  --auth-timeout 180 \
  --silent
