# PKA System Check

_Generated: 2026-05-17T17:41:51_
_Status: RED_

## Components

- Security audit: `RED`
- System improvement audit: `ORANGE`
- Pointer generation drift: `ORANGE`
- Instinct promotion: `GREEN`

## Security Findings

- `high` `permissions` TEAM/backups/team_2026-05-15_0800.db: mode 0644, expected 0600 or stricter
- `high` `db-drift` team.db: root team.db differs semantically from TEAM/team.db
- `high` `backups` TEAM/backups/team_2026-05-15_0800.db: latest backup is 57.7 hours old
- `medium` `roster-drift` AGENTS.md: does not mention current active count 28
- `medium` `roster-drift` GEMINI.md: does not mention current active count 28
- `medium` `roster-drift` ADAPTER-PROMPT.md: does not mention current active count 28

## Improvement Findings

- `medium` `instruction-surface` CLAUDE.md: overlay does not mention active roster count 28
- `medium` `instruction-surface` AGENTS.md: overlay does not mention active roster count 28
- `medium` `instruction-surface` GEMINI.md: overlay does not mention active roster count 28
- `medium` `instruction-surface` DEEPSEEK.md: overlay does not mention active roster count 28
- `medium` `instruction-surface` ADAPTER-PROMPT.md: overlay does not mention active roster count 28
- `medium` `pointer-generation` CLAUDE.md / AGENTS.md / GEMINI.md / DEEPSEEK.md: generated pointer surfaces are drifting from the canonical config

## Pointer Drift

- canonical pointer surfaces are drifting

