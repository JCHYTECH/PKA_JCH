# PKA System Check

_Generated: 2026-05-24T20:17:41_
_Status: RED_

## Components

- Security audit: `RED`
- System improvement audit: `ORANGE`
- Pointer generation drift: `ORANGE`
- Instinct promotion: `GREEN`

## Security Findings

- `high` `permissions` dashboard.log: mode 0644, expected 0600 or stricter
- `high` `permissions` scripts/sybil_journal.log: mode 0644, expected 0600 or stricter
- `high` `permissions` scripts/dobby_weekly.log: mode 0644, expected 0600 or stricter
- `high` `permissions` scripts/dobby_retro.log: mode 0644, expected 0600 or stricter
- `high` `permissions` scripts/email_digest.log: mode 0644, expected 0600 or stricter
- `high` `permissions` tmp/plane-autostart.launchd.log: mode 0644, expected 0600 or stricter
- `high` `permissions` tmp/plane-autostart.log: mode 0644, expected 0600 or stricter
- `high` `permissions` TEAM/backups/team_2026-05-15_0800.db: mode 0644, expected 0600 or stricter
- `high` `permissions` JCH_Inbox/99_SYSTEM/google_calendar_credentials.json: mode 0644, expected 0600 or stricter
- `high` `db-drift` team.db: root team.db differs semantically from TEAM/team.db
- `high` `backups` TEAM/backups/team_2026-05-15_0800.db: latest backup is 228.3 hours old

## Improvement Findings

- `medium` `pointer-generation` CLAUDE.md / AGENTS.md / GEMINI.md / DEEPSEEK.md: generated pointer surfaces are drifting from the canonical config

## Pointer Drift

- canonical pointer surfaces are drifting

