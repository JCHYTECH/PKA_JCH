# PKA System Check

_Generated: 2026-06-08T15:01:28_
_Status: ORANGE_

## Components

- Security audit: `ORANGE`
- System improvement audit: `ORANGE`
- Pointer generation drift: `ORANGE`
- File placement drift: `GREEN`
- Instinct promotion: `GREEN`

## Security Findings

- `medium` `roster-drift` ADAPTER-PROMPT.md: does not mention current active count 30

## Improvement Findings

- `medium` `instruction-surface` ADAPTER-PROMPT.md: overlay does not mention active roster count 30
- `medium` `pointer-generation` CLAUDE.md / AGENTS.md / GEMINI.md / DEEPSEEK.md: generated pointer surfaces are drifting from the canonical config
- `low` `todo-drift` JCH_Inbox/todo-jch.html vs todo-jch.json: generated HTML is out of sync with JSON task data

## Pointer Drift

- canonical pointer surfaces are drifting

