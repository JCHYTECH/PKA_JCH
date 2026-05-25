# PKA Vault Worktree Stabilization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Stabilize the PKA_JCH vault and Git worktree before expanding Obsidian and Hermisation automation.

**Architecture:** Use a non-destructive audit-first workflow. Separate unrelated changes into reviewable batches, then commit or ignore each batch only after classification.

**Tech Stack:** Git, shell inventory commands, Markdown reports, PKA vault conventions.

---

### Task 1: Freeze and Inventory

**Files:**
- Create: `TEAM_Inbox/2026-05-25_dobby_vault_worktree_stabilization_report.md`
- Read: `git status --short`
- Read: `git diff --stat`

- [ ] **Step 1: Record current status counts**

Run:

```bash
git ls-files --deleted | wc -l
git ls-files --others --exclude-standard | wc -l
git diff --name-only --diff-filter=M | wc -l
```

Expected current baseline:

```text
80 deleted tracked files
1425 untracked files
25 modified tracked files
```

- [ ] **Step 2: Record high-risk large data**

Run:

```bash
du -sh JCH_Inbox/03_PROJECTS/03_WILDNEXUS/06_COMPONENTS/BIOACOUSTIC/INSECTNET
git ls-files --others --exclude-standard JCH_Inbox/03_PROJECTS/03_WILDNEXUS/06_COMPONENTS/BIOACOUSTIC/INSECTNET | awk '
  function ext(path){n=split(path,a,"/"); f=a[n]; if (f !~ /\./) return "[no-ext]"; sub(/^.*\./,"",f); return "." f}
  {count[ext($0)]++}
  END{for (e in count) print count[e], e}' | sort -nr
```

Expected current baseline:

```text
1.7G InsectNet
659 .wav
564 .png
16 .csv
13 .md
2 .html
```

### Task 2: Classify Commit Batches

**Files:**
- Modify: `TEAM_Inbox/2026-05-25_dobby_vault_worktree_stabilization_report.md`

- [ ] **Step 1: Classify batch A — PKA system pointers and skills**

Scope:

```text
AGENTS.md
CLAUDE.md
DEEPSEEK.md
GEMINI.md
skills/
wiki/Guidelines/GL-002-skill-inventory.md
wiki/Guidelines/INDEX.md
```

Action: review diffs, then commit as a system-pointer/skills batch if coherent.

- [ ] **Step 2: Classify batch B — save tooling**

Scope:

```text
bin/pka
bin/pka-save
scripts/pka_save.py
tests/test_pka_save.py
tests/test_pka_save_shortcut.py
```

Action: run the focused tests before commit.

Run:

```bash
pytest tests/test_pka_save.py tests/test_pka_save_shortcut.py
```

- [ ] **Step 3: Classify batch C — WildNexus reorganization**

Scope:

```text
JCH_Inbox/03_PROJECTS/03_WILDNEXUS/
```

Action: inspect deleted files against new locations. Do not restore or delete anything blindly.

Run:

```bash
git ls-files --deleted JCH_Inbox/03_PROJECTS/03_WILDNEXUS | wc -l
git ls-files --others --exclude-standard JCH_Inbox/03_PROJECTS/03_WILDNEXUS | wc -l
```

- [ ] **Step 4: Classify batch D — Nuances archive**

Scope:

```text
JCH_Inbox/03_PROJECTS/04_NUANCES/
JCH_Inbox/03_PROJECTS/archive/reanimable/04_NUANCES/
```

Action: treat as a likely project archival move. Verify matching basenames, then commit deletion plus archive addition together if confirmed.

- [ ] **Step 5: Classify batch E — InsectNet generated data**

Scope:

```text
JCH_Inbox/03_PROJECTS/03_WILDNEXUS/06_COMPONENTS/BIOACOUSTIC/INSECTNET/
```

Action: decide whether `.wav` and generated `.png` spectrograms belong in Git, Git LFS, NAS, or `.gitignore`. Do not add 1.7 GB of data by default.

- [ ] **Step 6: Classify batch F — Obsidian and Hermisation scaffolds**

Scope:

```text
JCH_Inbox/03_PROJECTS/01_AI_IT_TOOLS/obsidian-knowledge-graph/
JCH_Inbox/03_PROJECTS/01_AI_IT_TOOLS/pka-hermisation/
docs/superpowers/specs/2026-05-25-pka-system-evolution-two-projects-design.md
JCH_Inbox/03_PROJECTS/01_AI_IT_TOOLS/INDEX.md
```

Action: commit as its own docs scaffold after the vault stabilization policy is confirmed.

### Task 3: Establish Git Hygiene

**Files:**
- Possibly modify: `.gitignore`
- Possibly modify: `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/06_COMPONENTS/BIOACOUSTIC/INSECTNET/README.md`

- [ ] **Step 1: Decide generated-data policy**

Recommended policy:

```text
Track small source metadata and curated review sheets.
Do not track raw downloaded audio, generated segments, generated spectrogram PNGs, or transient review app outputs in normal Git.
Store heavy datasets on NAS or a dedicated data area, with manifest files in Git.
```

- [ ] **Step 2: Apply `.gitignore` only after approval**

Candidate patterns:

```gitignore
JCH_Inbox/03_PROJECTS/03_WILDNEXUS/06_COMPONENTS/BIOACOUSTIC/INSECTNET/03_AUDIO_DOWNLOADS/audio/
JCH_Inbox/03_PROJECTS/03_WILDNEXUS/06_COMPONENTS/BIOACOUSTIC/INSECTNET/03_AUDIO_DOWNLOADS/segments/
JCH_Inbox/03_PROJECTS/03_WILDNEXUS/06_COMPONENTS/BIOACOUSTIC/INSECTNET/03_AUDIO_DOWNLOADS/spectrograms/
```

### Task 4: Commit in Thematic Order

**Files:**
- Use Git staging only after each batch is verified.

- [ ] **Step 1: Commit system pointers**

Run:

```bash
git add AGENTS.md CLAUDE.md DEEPSEEK.md GEMINI.md skills wiki/Guidelines/GL-002-skill-inventory.md wiki/Guidelines/INDEX.md
git commit -m "chore: align PKA pointers and skills inventory"
```

- [ ] **Step 2: Commit save tooling**

Run:

```bash
pytest tests/test_pka_save.py tests/test_pka_save_shortcut.py
git add bin/pka bin/pka-save scripts/pka_save.py tests/test_pka_save.py tests/test_pka_save_shortcut.py
git commit -m "chore: update PKA save shortcuts"
```

- [ ] **Step 3: Commit AI_IT_TOOLS scaffolds**

Run:

```bash
git add JCH_Inbox/03_PROJECTS/01_AI_IT_TOOLS/INDEX.md JCH_Inbox/03_PROJECTS/01_AI_IT_TOOLS/obsidian-knowledge-graph JCH_Inbox/03_PROJECTS/01_AI_IT_TOOLS/pka-hermisation docs/superpowers/specs/2026-05-25-pka-system-evolution-two-projects-design.md
git commit -m "docs: scaffold PKA system evolution projects"
```

- [ ] **Step 4: Commit WildNexus and Nuances only after review**

Action: stage with path-specific `git add` after confirming archival/reorganization intent.

### Task 5: Final Verification

**Files:**
- Read: `git status --short`
- Modify: `TEAM_Inbox/2026-05-25_dobby_vault_worktree_stabilization_report.md`

- [ ] **Step 1: Verify status**

Run:

```bash
git status --short
```

Expected: either clean, or only intentionally deferred heavy/generated data remains.

- [ ] **Step 2: Write final status in report**

Record:

- committed batches;
- deferred batches;
- unresolved decisions;
- next safe step for Obsidian/Hermisation.
