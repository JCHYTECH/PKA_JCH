# PKA System Check

_Generated: 2026-06-16T19:55:04_
_Status: RED_

## Components

- Security audit: `RED`
- System improvement audit: `ORANGE`
- Pointer generation drift: `ORANGE`
- File placement drift: `GREEN`
- Instinct promotion: `GREEN`

## Security Findings

- `high` `permissions` _local/zigbee-bridge.log: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/homeassistant/zigbee.db: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/homeassistant/home-assistant.log: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/zigbee2mqtt/data/migration-2-to-3.log: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/zigbee2mqtt/data/migration-3-to-4.log: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/zigbee2mqtt/data/migration-4-to-5.log: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/zigbee2mqtt/data/migration-1-to-2.log: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/zigbee2mqtt/data/database.db: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/zigbee2mqtt/data/log/2026-06-15.19-43-43/log.log: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/zigbee2mqtt/data/log/2026-06-16.10-12-43/log.log: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/zigbee2mqtt/data/log/2026-06-15.19-55-39/log.log: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/zigbee2mqtt/data/log/2026-06-15.19-55-39/log2.log: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/zigbee2mqtt/data/log/2026-06-15.19-55-39/log1.log: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/zigbee2mqtt/data/log/2026-06-15.19-46-33/log.log: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/zigbee2mqtt/data/log/2026-06-15.19-47-41/log.log: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/zigbee2mqtt/data/log/2026-06-15.19-11-05/log.log: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/zigbee2mqtt/data/log/2026-06-15.19-43-12/log.log: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/zigbee2mqtt/data/log/2026-06-15.19-10-20/log.log: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/zigbee2mqtt/data/log/2026-06-16.13-59-31/log.log: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/zigbee2mqtt/data/log/2026-06-15.19-55-11/log.log: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/dist/token.d.ts: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/dist/token.d.ts.map: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/dist/token.js: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/dist/token.js.map: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/tests/token.test.ts: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/src/token.ts: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/node_modules/js-tokens/LICENSE: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/node_modules/js-tokens/CHANGELOG.md: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/node_modules/js-tokens/index.js: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/node_modules/js-tokens/[[README]].md: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/node_modules/js-tokens/package.json: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/node_modules/eslint/lib/languages/js/source-code/token-store/cursors.js: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/node_modules/eslint/lib/languages/js/source-code/token-store/backward-token-cursor.js: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/node_modules/eslint/lib/languages/js/source-code/token-store/backward-token-comment-cursor.js: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/node_modules/eslint/lib/languages/js/source-code/token-store/filter-cursor.js: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/node_modules/eslint/lib/languages/js/source-code/token-store/index.js: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/node_modules/eslint/lib/languages/js/source-code/token-store/forward-token-comment-cursor.js: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/node_modules/eslint/lib/languages/js/source-code/token-store/padded-token-cursor.js: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/node_modules/eslint/lib/languages/js/source-code/token-store/forward-token-cursor.js: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/node_modules/eslint/lib/languages/js/source-code/token-store/cursor.js: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/node_modules/eslint/lib/languages/js/source-code/token-store/utils.js: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/node_modules/eslint/lib/languages/js/source-code/token-store/skip-cursor.js: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/node_modules/eslint/lib/languages/js/source-code/token-store/decorative-cursor.js: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/node_modules/eslint/lib/languages/js/source-code/token-store/limit-cursor.js: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/node_modules/espree/lib/token-translator.js: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/node_modules/@babel/generator/lib/token-map.js.map: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/node_modules/@babel/generator/lib/token-map.js: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/node_modules/@sinclair/typebox/build/cjs/parser/runtime/token.d.ts: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/node_modules/@sinclair/typebox/build/cjs/parser/runtime/token.js: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/node_modules/@sinclair/typebox/build/cjs/parser/static/token.d.ts: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/node_modules/@sinclair/typebox/build/cjs/parser/static/token.js: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/node_modules/@sinclair/typebox/build/esm/parser/runtime/token.d.mts: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/node_modules/@sinclair/typebox/build/esm/parser/runtime/token.mjs: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/node_modules/@sinclair/typebox/build/esm/parser/static/token.d.mts: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/node_modules/@sinclair/typebox/build/esm/parser/static/token.mjs: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/node_modules/@modelcontextprotocol/sdk/dist/cjs/server/auth/handlers/token.d.ts: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/node_modules/@modelcontextprotocol/sdk/dist/cjs/server/auth/handlers/token.d.ts.map: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/node_modules/@modelcontextprotocol/sdk/dist/cjs/server/auth/handlers/token.js: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/node_modules/@modelcontextprotocol/sdk/dist/cjs/server/auth/handlers/token.js.map: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/node_modules/@modelcontextprotocol/sdk/dist/esm/server/auth/handlers/token.d.ts: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/node_modules/@modelcontextprotocol/sdk/dist/esm/server/auth/handlers/token.d.ts.map: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/node_modules/@modelcontextprotocol/sdk/dist/esm/server/auth/handlers/token.js: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/node_modules/@modelcontextprotocol/sdk/dist/esm/server/auth/handlers/token.js.map: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/node_modules/jose/dist/webapi/key/generate_secret.js: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/node_modules/jose/dist/types/key/generate_secret.d.ts: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/lightroom-mcp/server/node_modules/yargs-parser/build/lib/tokenize-arg-string.js: mode 0644, expected 0600 or stricter
- `high` `permissions` .venv/lib/python3.13/site-packages/certifi/cacert.pem: mode 0644, expected 0600 or stricter
- `high` `permissions` .venv/lib/python3.13/site-packages/pip/_vendor/packaging/_tokenizer.py: mode 0644, expected 0600 or stricter
- `high` `permissions` .venv/lib/python3.13/site-packages/pip/_vendor/pygments/token.py: mode 0644, expected 0600 or stricter
- `high` `permissions` .venv/lib/python3.13/site-packages/pip/_vendor/certifi/cacert.pem: mode 0644, expected 0600 or stricter
- `high` `permissions` JCH_Inbox/03_PROJECTS/07_TRAVELS/pka-decouvertes/logs/collector.log: mode 0644, expected 0600 or stricter

## Improvement Findings

- `medium` `pointer-generation` CLAUDE.md / AGENTS.md / GEMINI.md / DEEPSEEK.md: generated pointer surfaces are drifting from the canonical config
- `low` `todo-drift` JCH_Inbox/todo-jch.html vs todo-jch.json: generated HTML is out of sync with JSON task data

## Pointer Drift

- canonical pointer surfaces are drifting

