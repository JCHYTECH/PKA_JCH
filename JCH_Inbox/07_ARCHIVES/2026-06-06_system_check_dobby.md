# PKA System Check

_Generated: 2026-06-06T03:02:17_
_Status: RED_

## Components

- Security audit: `RED`
- System improvement audit: `ORANGE`
- Pointer generation drift: `ORANGE`
- File placement drift: `GREEN`
- Instinct promotion: `GREEN`

## Security Findings

- `high` `permissions` _local/backup_pka_m1.log: mode 0644, expected 0600 or stricter
- `high` `permissions` _local/retro-launchd.log: mode 0644, expected 0600 or stricter

## Improvement Findings

- `medium` `pointer-generation` CLAUDE.md / AGENTS.md / GEMINI.md / DEEPSEEK.md: generated pointer surfaces are drifting from the canonical config
- `low` `todo-drift` JCH_Inbox/todo-jch.html vs todo-jch.json: generated HTML is out of sync with JSON task data

## Pointer Drift

- canonical pointer surfaces are drifting

