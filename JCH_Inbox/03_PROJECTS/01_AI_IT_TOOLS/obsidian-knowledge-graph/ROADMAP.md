---
date: 2026-05-25
model: GPT-5 Codex
type: roadmap
status: active
domain: obsidian
---

# Roadmap — Obsidian Knowledge Graph

## Phase 1 — Inventory

Scan PKA_JCH files and build initial indexes:

- `indexes/note_index.md`
- `indexes/project_index.md`
- `indexes/technology_index.md`
- `indexes/agent_index.md`

Output: a readable inventory with titles, aliases, tags, folders, and frequent concepts.

## Phase 2 — Knowledge Dictionary

Create `knowledge_dictionary.md` with:

- canonical name;
- aliases;
- category;
- source folder;
- ambiguity notes.

JCH validates this first dictionary before large-scale linking.

## Phase 3 — Controlled Linking

Apply wikilinks automatically only when:

- target exists;
- confidence is high;
- ambiguity is low;
- readability is preserved.

Ambiguous candidates go to `review_queue.md`.

## Phase 4 — Quality Control

Check for:

- broken links;
- duplicates;
- excessive links;
- useless circular links;
- YAML inconsistencies;
- unreadable notes.

## Phase 5 — Semantic Layer

Later only:

- embeddings;
- semantic search;
- clustering;
- relation scoring;
- generated dashboards.
