# InsectNet - Auto-QC Prefilter Log

## 2026-05-24 - Spectrogram-based conservative prefilter

**Objective:** Add non-human filtering assistance before manual QC, without replacing human decisions.

**Script added:**

```text
scripts/insectnet_auto_qc.py
```

**Output file:**

```text
INSECTNET/03_AUDIO_DOWNLOADS/segment_qc_auto.csv
```

**Review app updated:**

```text
INSECTNET/04_PIPELINE/insectnet-qc-review.html
```

The app now displays:

- `auto_qc`
- `auto_reason`
- `auto_score`

## Method

The prefilter analyzes each spectrogram PNG and computes:

- `active_pixel_ratio`
- `contrast_stddev`
- `mean_luminance`

It then assigns one of:

```text
auto_keep_candidate
auto_reject_candidate
human_review
```

Important rule:

```text
The script never writes visual_qc=keep.
```

Human review remains authoritative.

## Run Result

**Command:**

```bash
python3 scripts/insectnet_auto_qc.py
```

**Output:**

```text
Wrote 559 auto-QC rows
auto_keep_candidate=494
auto_reject_candidate=21
human_review=44
```

By species:

```text
Gryllus campestris        auto_keep_candidate 204 / human_review 6
Leptophyes punctatissima  auto_keep_candidate 58  / auto_reject_candidate 20 / human_review 15
Pholidoptera griseoaptera auto_keep_candidate 54  / human_review 8
Roeseliana roeselii       auto_keep_candidate 97  / auto_reject_candidate 1  / human_review 8
Tettigonia viridissima    auto_keep_candidate 81  / human_review 7
```

Reject candidates:

```text
low_signal : 21
```

## Verification

```text
python3 -m pytest tests/test_insectnet_auto_qc.py tests/test_insectnet_qc_review_app.py tests/test_insectnet_audio_inventory.py tests/test_insectnet_segment_audio.py tests/test_insectnet_spectrograms.py tests/test_insectnet_contact_sheets.py tests/test_insectnet_segment_qc.py tests/test_insectnet_grouped_split.py tests/test_insectnet_download_audio.py tests/test_insectnet_select_audio_candidates.py tests/test_insectnet_xc_metadata.py -q
40 passed
```

## Interpretation

The filter is intentionally permissive. It is most useful for:

- surfacing likely weak `Leptophyes punctatissima` segments;
- prioritizing human review;
- reducing attention spent on obvious low-signal cases;
- later learning from JCH's manual `keep/reject` decisions.

## Next Step

JCH should continue reviewing in the HTML app using the auto suggestions as hints:

- trust `auto_reject_candidate` only after visual/audio check;
- use `auto_keep_candidate` as a queue priority, not as a final label;
- export `segment_qc_reviewed.csv` when a first batch is reviewed.
