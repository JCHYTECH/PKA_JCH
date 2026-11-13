# Bioacoustics QC Reference

## Current InsectNet conventions

Use these conventions when curating insect bioacoustic datasets:

- Segment length: 3 seconds
- Split discipline: group by `recording_id`
- Human QC states: `keep`, `reject`, `review`
- Auto-QC states: `auto_keep_candidate`, `auto_reject_candidate`, `human_review`
- Audio-band tags: `audible`, `mixed`, `ultrasonic`, `unknown`
- Species audio policy:
  - compute `dominant_freq_hz` for each segment
  - compute a species median
  - if the median is above `28000 Hz`, mark the species `audible_list_exclude`
  - otherwise mark it `audible_list_keep`

## Recommended review order

1. Review the strongest audible species first.
2. Then review species with mixed or ambiguous band tags.
3. Leave clear `auto_reject_candidate` rows for the end unless you need to inspect a failure mode.

## Files produced by the InsectNet pipeline

- `segment_qc.csv`
- `segment_qc_auto.csv`
- `species_audio_profile.csv`
- `train-test-split.csv`
- `insectnet-qc-review.html`
- `insectnet-qc-review-leptophyes.html`

## Practical rule

If the species-level median is above the threshold, do not spend manual review time trying to build an audible-only class from it. Keep the raw data for scientific completeness, but remove it from the audible worklist.
