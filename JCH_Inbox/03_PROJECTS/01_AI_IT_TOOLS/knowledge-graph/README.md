---
date: 2026-05-25
model: GPT-5 [[Codex]]
type: project
status: active
domain: ai-it-tools
---

# [[Obsidian]] Knowledge Graph

## Mission

Connect PKA_JCH to [[Obsidian]] as a governed [[knowledge]] graph: readable by JCH, useful for [[Dobby]] and the specialists, and stable enough to support long-term memory.

## Role in PKA

This project owns the documentary graph layer:

- wikilinks;
- note indexes;
- controlled aliases;
- YAML conventions;
- review queues;
- quality checks;
- integration of non-Markdown assets into the documentary memory.

## Boundaries

This project does not own agent runtime, persistent databases, queues, or external orchestration. Those belong to `pka-hermisation/`.

## Initial Status

Scaffold created from 

## Key Files

- `PROJECT_BRIEF.md` — vision and scope.
- `ROADMAP.md` — implementation phases.
- `GOVERNANCE.md` — rules for wikilinking and metadata.
- `review_queue.md` — ambiguities requiring validation.
- `indexes/` — future generated indexes.
- `source/` — copied source documents from [[inbox]].
