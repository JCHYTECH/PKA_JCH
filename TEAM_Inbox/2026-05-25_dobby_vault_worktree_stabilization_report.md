---
date: 2026-05-25
model: GPT-5 [[Codex]]
type: audit
status: draft
scope: vault-worktree-stabilization
---

# [[Dobby]] — Vault and Worktree Stabilization Report

## Objective

Stabilize PKA_JCH before deeper [[Obsidian]] and Hermisation work.

No destructive cleanup has been performed in this pass.

## Specialists Routed

- [[Dobby]]: orchestration and arbitration.
- [[Forge]]: [[Git]] hygiene, tooling, worktree structure.
- [[Corbeau]]: vault coherence and documentary governance.
- [[Castor]]: memory and database consistency.

## Current [[Git]] Baseline

Fresh inventory from 

| Category | Count / Signal |
|---|---:|
| Modified tracked files | 25 |
| Deleted tracked files | 80 |
| Untracked files | 1425 |
| Diff stat | 105 files changed, 331 insertions, 14551 deletions |

## Main Risk

The worktree is not ready for broad automation. The largest risk is not the new [[Obsidian]]/Hermisation scaffold; it is the combination of:

- 80 tracked deletions;
- a likely WildNexus reorganization;
- a likely Nuances archival move;
- 1.7 GB of untracked InsectNet data;
- system pointer and skill updates mixed with project content.

## Batch Classification

### Batch A — PKA Pointers and Skills

Files include:

- `AGENTS.md`
- `CLAUDE.md`
- `DEEPSEEK.md`
- `GEMINI.md`
- `skills/`
- `wiki/Guidelines/GL-002-skill-inventory.md`

Recommended action: review and commit as one system-alignment batch.

### Batch B — PKA Save Tooling

Files include:

- `bin/pka`
- `bin/pka-save`
- `scripts/pka_save.py`
- `tests/test_pka_save.py`
- `tests/test_pka_save_shortcut.py`

Recommended action: run focused pytest, then commit if passing.

### Batch C — WildNexus Reorganization

Scope:

- `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/`

Observed:

- many tracked files deleted;
- many new WildNexus folders and files untracked;
- 13 deleted WildNexus basenames appear elsewhere in the current WildNexus tree, suggesting partial reorganization rather than simple deletion.

Recommended action: inspect and commit as a reorganization batch only after confirming no important tracked content was lost.

### Batch D — Nuances [[archive]]

Scope:

- deleted tracked files under `JCH_Inbox/03_PROJECTS/04_NUANCES/`
- untracked files under `JCH_Inbox/03_PROJECTS/archive/reanimable/04_NUANCES/`

Observed:

- `04_NUANCES` has no current files at shallow scan.
- 33 files exist under `archive/reanimable/04_NUANCES`.
- 32 deleted Nuances basenames match files in the [[archive]] path.

Recommended action: treat as a likely intentional [[archive]] move. Commit deletion plus [[archive]] addition together if JCH confirms 

### Batch E — InsectNet Data

Scope:

- `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/06_COMPONENTS/BIOACOUSTIC/INSECTNET/`

Observed:

- 1.7 GB total.
- Untracked file types include 659 `.wav`, 564 `.png`, 16 `.csv`, 13 `.md`, 2 `.html`.

Recommended action: do not add all generated audio/spectrogram data to normal [[Git]]. Track metadata, manifests, scripts, and curated notes. Store heavy audio/spectrogram artifacts outside normal [[Git]] or ignore generated folders.

### Batch F — [[Obsidian]] and Hermisation Scaffolds

Scope:

- `JCH_Inbox/03_PROJECTS/01_AI_IT_TOOLS/obsidian-knowledge-graph/`
- `JCH_Inbox/03_PROJECTS/01_AI_IT_TOOLS/pka-hermisation/`
- `docs/superpowers/specs/2026-05-25-pka-system-evolution-two-projects-design.md`
- `JCH_Inbox/03_PROJECTS/01_AI_IT_TOOLS/INDEX.md`

Recommended action: commit as a small standalone docs scaffold after the cleanup policy is agreed.

## Proposed Commit Order

1. System pointers and skills.
2. Save tooling after tests.
3. AI_IT_TOOLS [[Obsidian]]/Hermisation scaffold.
4. Nuances [[archive]] move, if confirmed.
5. WildNexus reorganization, after targeted review.
6. InsectNet scripts/tests/metadata, excluding heavy generated data unless a dedicated data strategy is chosen.

## Immediate Decision Needed

The one decision that affects the next safe action:

Should the 1.7 GB InsectNet audio/spectrogram data be excluded from normal [[Git]] and represented by manifests plus curated metadata?

Recommended answer: yes.
