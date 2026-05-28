# InsectNet QC + Segmentation Design

**Goal:** Prepare the 100-file InsectNet V0.1 audio lot for model work by producing a reproducible audio inventory and short analysis segments.

**Scope:** This step covers quality control and segmentation only. It does not train a model, generate spectrograms, or modify BirdNET-Pi.

## Architecture

Two small scripts keep responsibilities separate:

- `scripts/insectnet_audio_inventory.py` reads the download manifest, probes local audio files with `ffprobe`, and writes `audio-inventory.csv`.
- `scripts/insectnet_segment_audio.py` reads the inventory, keeps only usable audio rows, uses `ffmpeg` to extract fixed-length WAV segments, and writes `segments-manifest.csv`.

The implementation uses [[Python]] standard library plus the installed 

## Data Flow

```text
audio-download-manifest.csv
  + downloaded audio files
  -> audio-inventory.csv
  -> segmented WAV files
  -> segments-manifest.csv
```

## Defaults

- Segment length: 3 seconds.
- Output audio: WAV, mono, 48 kHz.
- Segment policy: skip clips shorter than one full segment.
- Per-file limit: optional CLI parameter, default unlimited.
- Existing segment files are skipped unless `--overwrite` is passed.

## Validation

Tests cover path mapping, `ffprobe` JSON parsing, status handling, segment planning, and dry-run segmentation. Operational runs produce CSV logs so the dataset state is inspectable without re-running the scripts.
