#!/usr/bin/env python3
"""Create a grouped train/test split for InsectNet segments."""

from __future__ import annotations

import argparse
import csv
import math
import sys
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BASE_DIR = (
    ROOT
    / "JCH_Inbox/03_PROJECTS/03_WILDNEXUS/06_COMPONENTS/BIOACOUSTIC/"
    / "INSECTNET/03_AUDIO_DOWNLOADS"
)
DEFAULT_QC = BASE_DIR / "segment_qc.csv"
DEFAULT_OUTPUT = BASE_DIR / "train-test-split.csv"


OUTPUT_FIELDS = [
    "species_latin",
    "recording_id",
    "segment_index",
    "segment_path",
    "spectrogram_path",
    "visual_qc",
    "qc_reason",
    "split",
]


def is_split_eligible(row: dict[str, str]) -> bool:
    return (
        row.get("visual_qc") != "reject"
        and bool(row.get("recording_id"))
        and bool(row.get("segment_path"))
        and bool(row.get("spectrogram_path"))
    )


def group_rows(
    rows: list[dict[str, str]],
) -> dict[str, dict[str, list[dict[str, str]]]]:
    grouped: dict[str, dict[str, list[dict[str, str]]]] = defaultdict(
        lambda: defaultdict(list)
    )
    for row in rows:
        if is_split_eligible(row):
            grouped[row.get("species_latin", "")][row.get("recording_id", "")].append(
                row
            )
    return {species: dict(recordings) for species, recordings in grouped.items()}


def assign_recordings(
    recording_ids: list[str],
    test_fraction: float = 0.2,
    recording_counts: dict[str, int] | None = None,
) -> dict[str, str]:
    if not 0 < test_fraction < 1:
        raise ValueError("test_fraction must be between 0 and 1")
    ordered = sorted(recording_ids)
    if not ordered:
        return {}

    counts = recording_counts or {recording_id: 1 for recording_id in ordered}
    total_segments = sum(counts.get(recording_id, 0) for recording_id in ordered)
    target_segments = max(1, round(total_segments * test_fraction))
    candidates = sorted(ordered, key=lambda recording_id: (counts[recording_id], recording_id))
    test_ids: set[str] = set()
    test_segments = 0
    for recording_id in candidates:
        if len(test_ids) >= len(ordered) - 1:
            break
        next_count = counts[recording_id]
        if test_segments >= target_segments and test_ids:
            break
        test_ids.add(recording_id)
        test_segments += next_count
    return {
        recording_id: "test" if recording_id in test_ids else "train"
        for recording_id in ordered
    }


def build_split_rows(
    qc_rows: list[dict[str, str]], test_fraction: float = 0.2
) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    grouped = group_rows(qc_rows)
    for species, recordings in sorted(grouped.items()):
        recording_counts = {
            recording_id: len(rows) for recording_id, rows in recordings.items()
        }
        assignments = assign_recordings(
            list(recordings), test_fraction, recording_counts=recording_counts
        )
        for recording_id, rows in sorted(recordings.items()):
            split = assignments[recording_id]
            for row in sorted(rows, key=lambda item: int(item.get("segment_index") or 0)):
                output.append(
                    {
                        "species_latin": species,
                        "recording_id": recording_id,
                        "segment_index": row.get("segment_index", ""),
                        "segment_path": row.get("segment_path", ""),
                        "spectrogram_path": row.get("spectrogram_path", ""),
                        "visual_qc": row.get("visual_qc", ""),
                        "qc_reason": row.get("qc_reason", ""),
                        "split": split,
                    }
                )
    return output


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_split(rows: list[dict[str, str]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def create_split(qc: Path, output: Path, test_fraction: float) -> list[dict[str, str]]:
    rows = build_split_rows(load_csv(qc), test_fraction)
    write_split(rows, output)
    return rows


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--qc", type=Path, default=DEFAULT_QC)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--test-fraction", type=float, default=0.2)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    rows = create_split(args.qc, args.output, args.test_fraction)
    train = sum(1 for row in rows if row["split"] == "train")
    test = sum(1 for row in rows if row["split"] == "test")
    print(f"Wrote {len(rows)} split rows to {args.output}")
    print(f"train={train} test={test}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
