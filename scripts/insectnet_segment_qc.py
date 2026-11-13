#!/usr/bin/env python3
"""Create an initial segment QC manifest for InsectNet."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BASE_DIR = (
    ROOT
    / "JCH_Inbox/03_PROJECTS/03_WILDNEXUS/06_COMPONENTS/BIOACOUSTIC/"
    / "INSECTNET/03_AUDIO_DOWNLOADS"
)
DEFAULT_SEGMENTS = BASE_DIR / "segments-manifest.csv"
DEFAULT_SPECTROGRAMS = BASE_DIR / "spectrogram-manifest.csv"
DEFAULT_OUTPUT = BASE_DIR / "segment_qc.csv"


OUTPUT_FIELDS = [
    "species_latin",
    "recording_id",
    "segment_index",
    "start_s",
    "duration_s",
    "segment_path",
    "spectrogram_path",
    "visual_qc",
    "qc_reason",
    "reviewed_by",
    "notes",
]


def segment_key(row: dict[str, str]) -> tuple[str, str, str]:
    return (
        row.get("recording_id", ""),
        row.get("segment_index", ""),
        row.get("segment_path") or row.get("target_path", ""),
    )


def default_visual_qc(_species_latin: str) -> str:
    return "review"


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def build_qc_rows(
    segment_rows: list[dict[str, str]],
    spectrogram_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    spectrogram_index = {segment_key(row): row for row in spectrogram_rows}
    output: list[dict[str, str]] = []
    for segment in segment_rows:
        if segment.get("status") not in {"created", "skipped-existing"}:
            continue

        spec = spectrogram_index.get(segment_key(segment))
        spectrogram_path = spec.get("spectrogram_path", "") if spec else ""
        reason = "unreviewed" if spectrogram_path else "missing_spectrogram"
        species = segment.get("species_latin", "")
        output.append(
            {
                "species_latin": species,
                "recording_id": segment.get("recording_id", ""),
                "segment_index": segment.get("segment_index", ""),
                "start_s": segment.get("start_s", ""),
                "duration_s": segment.get("duration_s", ""),
                "segment_path": segment.get("target_path", ""),
                "spectrogram_path": spectrogram_path,
                "visual_qc": default_visual_qc(species),
                "qc_reason": reason,
                "reviewed_by": "",
                "notes": "",
            }
        )
    return output


def write_qc(rows: list[dict[str, str]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def create_segment_qc(segments: Path, spectrograms: Path, output: Path) -> list[dict[str, str]]:
    rows = build_qc_rows(load_csv(segments), load_csv(spectrograms))
    write_qc(rows, output)
    return rows


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--segments", type=Path, default=DEFAULT_SEGMENTS)
    parser.add_argument("--spectrograms", type=Path, default=DEFAULT_SPECTROGRAMS)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    rows = create_segment_qc(args.segments, args.spectrograms, args.output)
    missing = sum(1 for row in rows if row["qc_reason"] == "missing_spectrogram")
    print(f"Wrote {len(rows)} QC rows to {args.output}")
    print(f"missing_spectrogram={missing}")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
