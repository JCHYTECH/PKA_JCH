---
date: 2026-05-25
model: GPT-5 [[Codex]]
type: governance
status: active
domain: [[Obsidian]]
---

# Governance — [[Obsidian]] Knowledge Graph

## Hard Rules

[[Dobby]] may add wikilinks, aliases, YAML metadata, suggestions, and quality reports.

[[Dobby]] may not:

- create links to nonexistent notes;
- create thousands of blind links;
- rename critical notes without validation;
- move notes globally without validation;
- delete content;
- reduce human readability.

## YAML Minimum

New important notes should include:

```yaml
---
type:
status:
dateCreated:
dateModified:
tags:
---
```

## Wikilinking Rules

- Link the first meaningful occurrence of a concept in a paragraph.
- Avoid repeated visual noise.
- Prefer explicit stable names, for example `[[Raspberry Pi 5]]`, not `[[Pi]]`.
- Do not link ambiguous terms automatically.
- Use `review_queue.md` for ambiguity.

## Priority Order

1. Stability.
2. Human readability.
3. Governance.
4. Coherence.
5. Prudently automated enrichment.
6. Long-term [[knowledge]] capitalization.
