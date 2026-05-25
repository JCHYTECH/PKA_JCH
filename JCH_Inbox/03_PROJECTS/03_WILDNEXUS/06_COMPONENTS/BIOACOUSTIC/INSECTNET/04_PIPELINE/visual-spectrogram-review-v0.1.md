# InsectNet - Visual Spectrogram Review V0.1

**Date:** 2026-05-24  
**Input:** `INSECTNET/03_AUDIO_DOWNLOADS/contact_sheets/`  
**Review scope:** first 25 spectrogram segments per species, generated from 3-second WAV segments.  
**Reviewer:** Dobby orchestration, with Chouette field-signal reading and Clio scientific caution.

## Summary

The V0.1 dataset is visually usable for a first baseline, but it should not go directly into training without filtering.

Best immediate candidates:

1. `Gryllus campestris`
2. `Tettigonia viridissima`
3. `Roeseliana roeselii`

Use with filtering:

4. `Pholidoptera griseoaptera`
5. `Leptophyes punctatissima`

## Species Review

### Gryllus campestris

**Visual quality:** strong.

Observed pattern:

- clear repeated pulse columns;
- high contrast against background;
- consistent structure across segments;
- good candidate for first classifier positive class.

Decision:

```text
Keep as V0.1 core species.
```

Recommended action:

- keep most segments;
- remove only visibly silent or corrupted outliers if found in full review.

### Leptophyes punctatissima

**Visual quality:** mixed to weak.

Observed pattern:

- some visible insect activity;
- many low-signal or diffuse segments;
- some segments show broadband noise or weak horizontal bands rather than clean species structure.

Decision:

```text
Keep, but require stricter segment-level QC before training.
```

Recommended action:

- flag low-signal segments;
- listen to representative weak segments before inclusion;
- consider this species a stress test for the pipeline rather than a clean early class.

### Pholidoptera griseoaptera

**Visual quality:** heterogeneous.

Observed pattern:

- several segments have strong vertical pulse events;
- several early segments look sparse or nearly empty;
- strong variation between recordings.

Decision:

```text
Keep, but filter heavily.
```

Recommended action:

- reject segments with no clear visible event;
- stratify by recording ID to avoid the classifier learning recordist/site artifacts;
- inspect whether strong segments come from too few recordings.

### Roeseliana roeselii

**Visual quality:** usable, dense.

Observed pattern:

- broad continuous high-frequency bands;
- repeated fine vertical modulation;
- some segments look very intense and may risk recording/site bias;
- strong species signature but less discrete than Gryllus.

Decision:

```text
Keep as V0.1 core species, with recording-ID split discipline.
```

Recommended action:

- split train/test by recording ID, not by segment;
- check for saturation or excessive background continuity.

### Tettigonia viridissima

**Visual quality:** strong.

Observed pattern:

- regular vertical pulse trains;
- high consistency across reviewed segments;
- clearly visible species-level structure.

Decision:

```text
Keep as V0.1 core species.
```

Recommended action:

- use as one of the anchor classes;
- ensure train/test split is by recording ID to avoid leakage from adjacent segments.

## Cross-Cutting Risks

### Segment Leakage

Many adjacent 3-second segments come from the same original recording. A random segment split would create leakage.

Decision:

```text
Train/test split must be grouped by recording_id.
```

### Overrepresentation

`Gryllus campestris` has 210 segments while `Pholidoptera griseoaptera` has only 62. A classifier trained naively will see class imbalance.

Decision:

```text
Baseline training must use balanced sampling or capped segments per class.
```

### Weak Segments

Some species include visibly weak or empty segments, especially `Leptophyes punctatissima` and parts of `Pholidoptera griseoaptera`.

Decision:

```text
Create a segment QC layer before training.
```

## Recommended Next Step

Create a segment review manifest:

```text
segment_qc.csv
```

Suggested fields:

| Field | Values |
|---|---|
| `segment_path` | path from `segments-manifest.csv` |
| `spectrogram_path` | path from `spectrogram-manifest.csv` |
| `species_latin` | species |
| `recording_id` | XC recording ID |
| `visual_qc` | keep, review, reject |
| `qc_reason` | low_signal, silence, noise, saturation, good_pattern |
| `reviewed_by` | Dobby/JCH/manual |

Initial rule-based bootstrap:

- mark all `Gryllus campestris`, `Tettigonia viridissima`, `Roeseliana roeselii` as `review`;
- mark all `Leptophyes punctatissima`, `Pholidoptera griseoaptera` as `review`;
- manually promote obvious clean examples to `keep`;
- reject visibly empty or noise-dominated segments.

## Baseline Readiness

Do not train yet.

Minimum before baseline:

1. Create `segment_qc.csv`.
2. Review at least 20 clean segments per species.
3. Build grouped train/test split by `recording_id`.
4. Cap or balance segment counts per species.
5. Then train a small CNN spectrogram baseline.
