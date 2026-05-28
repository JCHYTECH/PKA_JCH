# PKA System Check

_Generated: 2026-05-28T20:34:07_
_Status: RED_

## Components

- Security audit: `RED`
- System improvement audit: `ORANGE`
- Pointer generation drift: `ORANGE`
- Instinct promotion: `GREEN`

## Security Findings

- `high` `permissions` TEAM_Inbox/dropbox_vetalyx_changes.log: mode 0644, expected 0600 or stricter
- `high` `permissions` tmp/dropbox-watch.log: mode 0644, expected 0600 or stricter
- `high` `permissions` tmp/outlook-gatekeeper.log: mode 0644, expected 0600 or stricter
- `high` `permissions` tmp/email-digest.log: mode 0644, expected 0600 or stricter
- `high` `permissions` TEAM/backups/team_2026-05-26_0800.db: mode 0644, expected 0600 or stricter
- `high` `permissions` TEAM/backups/team_2026-05-25_0800.db: mode 0644, expected 0600 or stricter
- `high` `backups` TEAM/backups/team_2026-05-26_0800.db: latest backup is 60.6 hours old
- `medium` `roster-drift` TEAM/ROSTER.md: does not mention current active count 28

## Improvement Findings

- `medium` `pointer-generation` [[Claude]].md / AGENTS.md / GEMINI.md / DEEPSEEK.md: generated pointer surfaces are drifting from the canonical config

## Pointer Drift

- canonical pointer surfaces are drifting

