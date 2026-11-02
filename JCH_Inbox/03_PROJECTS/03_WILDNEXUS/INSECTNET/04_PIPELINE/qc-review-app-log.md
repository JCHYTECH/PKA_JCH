# InsectNet - QC Review App Log

## 2026-05-24 - Standalone HTML QC app

**Objective:** Make manual segment QC easy enough for practical use without editing `segment_qc.csv` directly.

**Script added:**

```text
scripts/insectnet_qc_review_app.py
```

**Test command:**

```bash
python3 -m pytest tests/test_insectnet_audio_inventory.py tests/test_insectnet_segment_audio.py tests/test_insectnet_spectrograms.py tests/test_insectnet_contact_sheets.py tests/test_insectnet_segment_qc.py tests/test_insectnet_grouped_split.py tests/test_insectnet_qc_review_app.py tests/test_insectnet_download_audio.py tests/test_insectnet_select_audio_candidates.py tests/test_insectnet_xc_metadata.py -q
```

**Result:**

```text
36 passed
```

**Generated app:**

```text
INSECTNET/04_PIPELINE/insectnet-qc-review.html
```

## Features

- standalone HTML file;
- no server required;
- embeds all `segment_qc.csv` records;
- displays spectrogram PNG;
- provides 3-second audio player;
- filters by species;
- filters by QC status;
- searches by recording ID;
- buttons: `Keep`, `Reject`, `Review`;
- reason selector:
  - `unreviewed`
  - `good_pattern`
  - `low_signal`
  - `noise`
  - `silence`
  - `saturation`
  - `ambiguous`
- notes field;
- exports updated CSV as `segment_qc_reviewed.csv`.

## Operating Rule

The app does not overwrite `segment_qc.csv` automatically. After review, the exported `segment_qc_reviewed.csv` should be inspected and then copied over `segment_qc.csv` intentionally.

After replacement, rerun:

```bash
python3 scripts/insectnet_grouped_split.py
```

This regenerates `train-test-split.csv` while excluding `visual_qc=reject` rows.

## Next Step

[[Start]] review with the strongest species:

1. `Gryllus campestris`
2. `Tettigonia viridissima`
3. `Roeseliana roeselii`

Goal for first baseline:

```text
20-40 keep segments per species
no rejected segments in train/test
split still grouped by recording_id
```
