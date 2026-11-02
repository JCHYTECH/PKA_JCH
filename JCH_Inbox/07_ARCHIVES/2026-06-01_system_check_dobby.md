# PKA System Check

_Generated: 2026-06-01T21:01:38_
_Status: RED_

## Components

- Security audit: `RED`
- System improvement audit: `ORANGE`
- Pointer generation drift: `ORANGE`
- Instinct promotion: `GREEN`

## Security Findings

- `high` `permissions` _local/homeassistant/secrets.yaml: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/homeassistant/home-assistant_v2.db: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/homeassistant/home-assistant.log: mode 0644, expected 0600 or stricter
- `high` `backups` TEAM/backups/team_2026-05-30_0800.db: latest backup is 61.0 hours old

## Improvement Findings

- `medium` `pointer-generation` CLAUDE.md / AGENTS.md / GEMINI.md / DEEPSEEK.md: generated pointer surfaces are drifting from the canonical config

## Pointer Drift

- canonical pointer surfaces are drifting

