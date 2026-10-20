# InsectNet - Audio QC and Segmentation Log

## 2026-05-24 - QC + 3 s segmentation

**Objective:** Convert the downloaded InsectNet V0.1 audio lot into a verified inventory and short fixed-length analysis segments.

**Scripts added:**

- `scripts/insectnet_audio_inventory.py`
- `scripts/insectnet_segment_audio.py`

**Tests:**

```text
python3 -m pytest tests/test_insectnet_audio_inventory.py tests/test_insectnet_segment_audio.py tests/test_insectnet_download_audio.py tests/test_insectnet_select_audio_candidates.py tests/test_insectnet_xc_metadata.py -q
17 passed
```

## Inventory

**Command:**

```bash
python3 scripts/insectnet_audio_inventory.py
```

**Output:**

```text
Processed 100 rows: ok=100
```

**File produced:**

```text
INSECTNET/03_AUDIO_DOWNLOADS/audio-inventory.csv
```

**By species:**

```text
Gryllus campestris        : 20
Leptophyes punctatissima  : 20
Pholidoptera griseoaptera : 20
Roeseliana roeselii       : 20
Tettigonia viridissima    : 20
```

## Segmentation

**Dry run:**

```bash
python3 scripts/insectnet_segment_audio.py --dry-run
```

**Dry-run output:**

```text
Processed 559 segments: dry-run=559
```

**Real run:**

```bash
python3 scripts/insectnet_segment_audio.py
```

**Output:**

```text
Processed 559 segments: created=559
```

**Files produced:**

```text
INSECTNET/03_AUDIO_DOWNLOADS/segments-manifest.csv
INSECTNET/03_AUDIO_DOWNLOADS/segments/
```

**Segment settings:**

```text
duration      : 3.000 s
format        : WAV
codec         : pcm_s16le
channels      : mono
sample rate   : 48000 Hz
```

**Segment count by species:**

```text
Gryllus campestris        : 210
Leptophyes punctatissima  : 93
Pholidoptera griseoaptera : 62
Roeseliana roeselii       : 106
Tettigonia viridissima    : 88
```

## Verification Sample

First segment checked with `ffprobe`:

```text
codec_name=pcm_s16le
codec_type=audio
sample_rate=48000
channels=1
duration=3.000000
```

## Interpretation

The V0.1 audio lot is technically usable:

- all 100 downloaded source files are readable;
- all planned 3-second segments were created;
- no source audio file was modified;
- the segment distribution is uneven because source recording durations differ strongly between species.

## Next Step

Generate spectrograms from `segments-manifest.csv`, then inspect a small contact sheet per species before training any classifier.

## 2026-05-24 - Spectrograms + contact sheets

**Objective:** Generate visual spectrograms for all 3-second InsectNet V0.1 segments and produce quick review sheets per species.

**Scripts added:**

- `scripts/insectnet_generate_spectrograms.py`
- `scripts/insectnet_contact_sheets.py`

**Tests:**

```text
python3 -m pytest tests/test_insectnet_audio_inventory.py tests/test_insectnet_segment_audio.py tests/test_insectnet_spectrograms.py tests/test_insectnet_contact_sheets.py tests/test_insectnet_download_audio.py tests/test_insectnet_select_audio_candidates.py tests/test_insectnet_xc_metadata.py -q
23 passed
```

### Spectrogram Generation

**Command:**

```bash
python3 scripts/insectnet_generate_spectrograms.py --overwrite
```

**Output:**

```text
Processed 559 spectrograms: created=559
```

**Files produced:**

```text
INSECTNET/03_AUDIO_DOWNLOADS/spectrogram-manifest.csv
INSECTNET/03_AUDIO_DOWNLOADS/spectrograms/
```

**Generation settings:**

```text
tool       : ffmpeg showspectrumpic
size       : 1024x512
color      : viridis
legend     : disabled
input      : 3 s WAV mono 48 kHz segments
```

**Counts by species:**

```text
Gryllus campestris        : 210
Leptophyes punctatissima  : 93
Pholidoptera griseoaptera : 62
Roeseliana roeselii       : 106
Tettigonia viridissima    : 88
```

### Contact Sheets

**Command:**

```bash
python3 scripts/insectnet_contact_sheets.py
```

**Output:**

```text
Wrote 5 contact sheets
```

**Files produced:**

```text
INSECTNET/03_AUDIO_DOWNLOADS/contact_sheets/
```

**Contact sheet settings:**

```text
max images per species : 25
columns                : 5
thumbnail width        : 320 px
sheet size             : 1600x890 px
```

### Interpretation

The dataset now has a visual inspection layer. The next scientific step is manual review of the five contact sheets to flag:

- low-signal segments;
- saturated or noisy recordings;
- species with overly repetitive or overly heterogeneous signatures;
- candidate examples for a first classifier train/test split.

No classifier has been trained yet.
