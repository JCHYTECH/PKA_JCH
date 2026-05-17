# PKA System Check

_Generated: 2026-05-16T22:41:24_
_Status: RED_

## Components

- Security audit: `RED`
- System improvement audit: `GREEN`
- Pointer generation drift: `GREEN`
- Instinct promotion: `GREEN`

## Security Findings

- `high` `permissions` TEAM/backups/team_2026-05-15_0800.db: mode 0644, expected 0600 or stricter
- `high` `db-drift` team.db: root team.db differs semantically from TEAM/team.db
- `high` `backups` TEAM/backups/team_2026-05-15_0800.db: latest backup is 38.7 hours old

