# PKA System Check

_Generated: 2026-05-31T20:13:42_
_Status: RED_

## Components

- Security audit: `RED`
- System improvement audit: `GREEN`
- Pointer generation drift: `GREEN`
- Instinct promotion: `GREEN`

## Security Findings

- `high` `permissions` _local/homeassistant/secrets.yaml: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/homeassistant/home-assistant_v2.db: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/homeassistant/home-assistant.log: mode 0644, expected 0600 or stricter
- `high` `backups` TEAM/backups/team_2026-05-30_0800.db: latest backup is 36.2 hours old

