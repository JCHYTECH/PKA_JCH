---
date: 2026-05-25
model: GPT-5 Codex
type: design
status: approved
project: AI_IT_TOOLS
---

# PKA System Evolution — Two Project Design

## Decision

Create two sibling projects in `JCH_Inbox/03_PROJECTS/01_AI_IT_TOOLS/`:

- `obsidian-knowledge-graph/`
- `pka-hermisation/`

The two projects are linked but independent. Obsidian is the governed documentary graph layer. Hermisation is the progressive adaptation of useful Hermes Agent concepts into PKA_JCH.

## Project 1 — Obsidian Knowledge Graph

Mission: connect PKA_JCH to Obsidian as a governed, human-readable, AI-usable knowledge graph.

Initial scope:

- inventory Markdown and non-Markdown files;
- create central indexes;
- create a controlled knowledge dictionary;
- add wikilinks only when confidence is high;
- route ambiguities to a review queue;
- preserve readability and reversibility.

Initial deliverables:

- `README.md`
- `PROJECT_BRIEF.md`
- `ROADMAP.md`
- `GOVERNANCE.md`
- `review_queue.md`
- `indexes/README.md`
- `source/`

## Project 2 — PKA Hermisation

Mission: adapt useful Hermes Agent concepts into a PKA-native architecture without replacing Dobby, multiplying agents blindly, or adding opaque framework complexity.

Initial scope:

- extract useful Hermes concepts;
- define what must not be copied;
- define a limited pilot scope;
- keep Dobby as central orchestrator;
- preserve human validation for critical actions;
- progress one technical layer at a time.

Initial deliverables:

- `README.md`
- `PROJECT_BRIEF.md`
- `ROADMAP.md`
- `HERMES_CONCEPTS_TO_ADAPT.md`
- `DO_NOT_COPY.md`
- `PILOT_SCOPE.md`
- `source/`

## Source Handling

The inbox files are copied into each project's `source/` folder and left untouched in `JCH_Inbox/00_INBOX/` until JCH validates that the project scaffolds are correct.

## Governance

No mass rename, delete, move, or automatic rewrite is allowed without explicit human validation.

No secret, password, or token may be written in project notes.

All automation must remain reversible, inspectable, and documented.
