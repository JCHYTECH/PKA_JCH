---
name: bioacoustics-qc-playbook
description: Curate insect and bioacoustic datasets, review spectrogram/audio segments, build species-level audio profiles, and decide whether species stay in the audible review list. Use when working on bioacoustic QC, segment triage, spectrogram review, ultrasonic-vs-audible classification, or dataset curation for insect/call recordings.
---

# Bioacoustics QC Playbook

## Overview

Use this skill to turn a raw bioacoustic lot into a reviewable, auditable dataset. Keep the workflow conservative: automate prefiltering, preserve human QC, and write down species-level audio decisions.

## Workflow

1. Build or load manifests for recordings, segments, and spectrograms.
2. Run conservative auto-QC first.
3. Compute species audio profiles from `dominant_freq_hz`.
4. Apply the audible-list rule:
   - if the species median `dominant_freq_hz` is above `28000 Hz`, mark it `audible_list_exclude`
   - otherwise mark it `audible_list_keep`
5. Keep `auto_qc` separate from human QC. Never let the prefilter override a human `keep`/`reject`.
6. Group train/test splits by `recording_id`, not by segment.
7. Save the result in a machine-readable CSV and a short pipeline log.

## Review Priorities

- Prefer species-level review over segment-level intuition.
- For difficult species, use a slow preview mode before judging by ear.
- Use the spectrogram when audio is ultrasonic or compressed by playback rate.
- Treat low-signal segments as candidates for rejection, not automatic truth.

## Output Conventions

- `auto_qc`: `auto_keep_candidate`, `auto_reject_candidate`, `human_review`
- `audio_band_tag`: `audible`, `mixed`, `ultrasonic`, `unknown`
- `species_audio_status`: `audible_list_keep`, `audible_list_exclude`, `unknown`
- QC logs should mention the threshold used and the species count covered.

## References

Load [Bioacoustics QC Reference](references/bioacoustics-qc-reference.md) when you need the concrete InsectNet conventions, threshold rationale, or field examples.
