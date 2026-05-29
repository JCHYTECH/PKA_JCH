# InsectNet QC + Segmentation Implementation Plan

> **For agentic workers:** REQUIRED SUB-[[SKILL]]: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a reproducible QC and segmentation pipeline for the InsectNet V0.1 audio lot.

**Architecture:** Add two focused [[Python]] scripts. The inventory script maps manifest rows to downloaded files and probes technical metadata with 

**Tech Stack:** [[Python]] standard library, 

---

### Task 1: Audio Inventory

**Files:**
- Create: `scripts/insectnet_audio_inventory.py`
- Create: `tests/test_insectnet_audio_inventory.py`

- [ ] Write failing tests for manifest path mapping, `ffprobe` JSON parsing, and missing-file status.
- [ ] Run `python3 -m pytest tests/test_insectnet_audio_inventory.py -q` and confirm failure because the module does not exist.
- [ ] Implement the inventory script with CSV input/output and CLI defaults.
- [ ] Run `python3 -m pytest tests/test_insectnet_audio_inventory.py -q` and confirm pass.

### Task 2: Audio Segmentation

**Files:**
- Create: `scripts/insectnet_segment_audio.py`
- Create: `tests/test_insectnet_segment_audio.py`

- [ ] Write failing tests for segment count planning, output path creation, and dry-run log rows.
- [ ] Run `python3 -m pytest tests/test_insectnet_segment_audio.py -q` and confirm failure because the module does not exist.
- [ ] Implement the segmentation script with CSV input/output and CLI defaults.
- [ ] Run `python3 -m pytest tests/test_insectnet_segment_audio.py -q` and confirm pass.

### Task 3: Operational Run

**Files:**
- Modify: `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/06_COMPONENTS/BIOACOUSTIC/INSECTNET/04_PIPELINE/audio-qc-segmentation-log.md`

- [ ] Run the full InsectNet test subset.
- [ ] Generate `audio-inventory.csv`.
- [ ] Generate 3-second segments and `segments-manifest.csv`.
- [ ] Record counts, failures, and next step in the pipeline log.
