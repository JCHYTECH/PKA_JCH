# PKA System Check

_Generated: 2026-06-09T14:38:29_
_Status: RED_

## Components

- Security audit: `RED`
- System improvement audit: `ORANGE`
- Pointer generation drift: `ORANGE`
- File placement drift: `GREEN`
- Instinct promotion: `GREEN`

## Security Findings

- `high` `permissions` _local/homeassistant/home-assistant.log: mode 0644, expected 0600 or stricter

## Improvement Findings

- `medium` `instruction-surface` ADAPTER-PROMPT.md: overlay does not mention active roster count 30
- `medium` `pointer-generation` CLAUDE.md / AGENTS.md / GEMINI.md / DEEPSEEK.md: generated pointer surfaces are drifting from the canonical config
- `low` `todo-drift` JCH_Inbox/todo-jch.html vs todo-jch.json: generated HTML is out of sync with JSON task data

## Pointer Drift

- canonical pointer surfaces are drifting

