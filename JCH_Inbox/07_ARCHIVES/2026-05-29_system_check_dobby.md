# PKA System Check

_Generated: 2026-05-29T23:49:23_
_Status: ORANGE_

## Components

- Security audit: `ORANGE`
- System improvement audit: `ORANGE`
- Pointer generation drift: `ORANGE`
- Instinct promotion: `GREEN`

## Security Findings

- `medium` `roster-drift` ADAPTER-PROMPT.md: does not mention current active count 29

## Improvement Findings

- `medium` `instruction-surface` ADAPTER-PROMPT.md: overlay does not mention active roster count 29
- `medium` `pointer-generation` CLAUDE.md / AGENTS.md / GEMINI.md / DEEPSEEK.md: generated pointer surfaces are drifting from the canonical config

## Pointer Drift

- canonical pointer surfaces are drifting

