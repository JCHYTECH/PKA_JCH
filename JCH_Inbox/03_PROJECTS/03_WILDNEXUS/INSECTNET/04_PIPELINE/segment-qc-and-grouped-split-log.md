# InsectNet - Segment QC and Grouped Split Log

## 2026-05-24 - Segment QC + grouped train/test split

**Objective:** Prepare InsectNet V0.1 for baseline modelling without leakage between train and test.

**Scripts added:**

- `scripts/insectnet_segment_qc.py`
- `scripts/insectnet_grouped_split.py`

**Tests:**

```text
python3 -m pytest tests/test_insectnet_audio_inventory.py tests/test_insectnet_segment_audio.py tests/test_insectnet_spectrograms.py tests/test_insectnet_contact_sheets.py tests/test_insectnet_segment_qc.py tests/test_insectnet_grouped_split.py tests/test_insectnet_download_audio.py tests/test_insectnet_select_audio_candidates.py tests/test_insectnet_xc_metadata.py -q
32 passed
```

## Segment QC

**Command:**

```bash
python3 scripts/insectnet_segment_qc.py
```

**Output:**

```text
Wrote 559 QC rows
missing_spectrogram=0
```

**File produced:**

```text
INSECTNET/03_AUDIO_DOWNLOADS/segment_qc.csv
```

Initial QC state:

```text
visual_qc = review    : 559
qc_reason = unreviewed : 559
```

Decision:

```text
No segment is auto-promoted to keep.
```

## Grouped Split

**Command:**

```bash
python3 scripts/insectnet_grouped_split.py
```

**File produced:**

```text
INSECTNET/03_AUDIO_DOWNLOADS/train-test-split.csv
```

Split result:

```text
train : 434
test  : 125
```

By species:

```text
Gryllus campestris        train 168 / test 42
Leptophyes punctatissima  train 72  / test 21
Pholidoptera griseoaptera train 49  / test 13
Roeseliana roeselii       train 82  / test 24
Tettigonia viridissima    train 63  / test 25
```

Leakage verification:

```text
recording_id groups checked : 82
leaks train/test            : 0
```

## Split Method

The split is grouped by `recording_id`. A recording and all its derived 3-second segments are assigned either to train or to test, never both.

The test set selection is segment-count-aware: it prefers small recording groups until reaching approximately 20% test segments per species. This avoids the earlier failure mode where one large recording could dominate the test set and leave too few train segments.

## Next Step

Manual or assisted review should update `segment_qc.csv`:

- `visual_qc=keep` for clean, species-representative segments;
- `visual_qc=reject` for silence, low signal, saturation, or obvious noise;
- `visual_qc=review` for uncertain cases.

After QC edits, regenerate `train-test-split.csv` so [[rejected]] segments are excluded.
