#!/usr/bin/env python3
"""Create fixed-length WAV segments from the InsectNet audio inventory."""

from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BASE_DIR = (
    ROOT
    / "JCH_Inbox/03_PROJECTS/03_WILDNEXUS/06_COMPONENTS/BIOACOUSTIC/"
    / "INSECTNET/03_AUDIO_DOWNLOADS"
)
DEFAULT_INVENTORY = BASE_DIR / "audio-inventory.csv"
DEFAULT_SEGMENTS_DIR = BASE_DIR / "segments"
DEFAULT_OUTPUT = BASE_DIR / "segments-manifest.csv"


OUTPUT_FIELDS = [
    "created_at",
    "species_latin",
    "recording_id",
    "source_path",
    "target_path",
    "segment_index",
    "start_s",
    "duration_s",
    "target_sample_rate_hz",
    "status",
    "message",
]


def slug(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "-", value.strip().lower()).strip("-")
    return cleaned or "unknown"


def as_float(value: str | float | int | None) -> float:
    if value in (None, ""):
        return 0.0
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


def segment_count(duration_s: float, segment_length_s: float) -> int:
    if segment_length_s <= 0:
        raise ValueError("segment_length_s must be positive")
    return int(duration_s // segment_length_s)


def segment_path(
    row: dict[str, str],
    segments_dir: Path,
    segment_index: int,
    segment_length_s: float,
) -> Path:
    start_s = segment_index * segment_length_s
    recording_id = row.get("recording_id") or "unknown"
    filename = f"XC{recording_id}_seg{segment_index:03d}_start{start_s:07.3f}s.wav"
    return segments_dir / slug(row.get("species_latin", "unknown")) / filename


def is_usable_inventory_row(row: dict[str, str], segment_length_s: float) -> bool:
    return (
        row.get("probe_status") == "ok"
        and row.get("local_path")
        and segment_count(as_float(row.get("actual_duration_s")), segment_length_s) > 0
    )


def run_ffmpeg_segment(
    source: Path,
    destination: Path,
    start_s: float,
    duration_s: float,
    sample_rate_hz: int,
    overwrite: bool,
) -> tuple[str, str]:
    if destination.exists() and not overwrite:
        return "skipped-existing", ""

    destination.parent.mkdir(parents=True, exist_ok=True)
    command = [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y" if overwrite else "-n",
        "-ss",
        f"{start_s:.3f}",
        "-i",
        str(source),
        "-t",
        f"{duration_s:.3f}",
        "-ac",
        "1",
        "-ar",
        str(sample_rate_hz),
        "-vn",
        str(destination),
    ]
    result = subprocess.run(command, check=False, capture_output=True, text=True)
    if result.returncode != 0:
        return "error", result.stderr.strip() or f"ffmpeg exited {result.returncode}"
    return "created", ""


def build_segment_row(
    row: dict[str, str],
    destination: Path,
    segment_index: int,
    start_s: float,
    segment_length_s: float,
    sample_rate_hz: int,
    status: str,
    message: str,
) -> dict[str, str]:
    return {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "species_latin": row.get("species_latin", ""),
        "recording_id": row.get("recording_id", ""),
        "source_path": row.get("local_path", ""),
        "target_path": str(destination),
        "segment_index": str(segment_index),
        "start_s": f"{start_s:.3f}",
        "duration_s": f"{segment_length_s:.3f}",
        "target_sample_rate_hz": str(sample_rate_hz),
        "status": status,
        "message": message,
    }


def build_segment_rows(
    inventory_rows: list[dict[str, str]],
    segments_dir: Path,
    segment_length_s: float,
    sample_rate_hz: int,
    dry_run: bool,
    overwrite: bool,
    per_file_limit: int | None,
) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    for row in inventory_rows:
        if not is_usable_inventory_row(row, segment_length_s):
            continue

        count = segment_count(as_float(row.get("actual_duration_s")), segment_length_s)
        if per_file_limit is not None:
            count = min(count, per_file_limit)

        source = Path(row["local_path"])
        for segment_index in range(count):
            start_s = segment_index * segment_length_s
            destination = segment_path(row, segments_dir, segment_index, segment_length_s)
            if dry_run:
                status, message = "dry-run", ""
            else:
                status, message = run_ffmpeg_segment(
                    source,
                    destination,
                    start_s,
                    segment_length_s,
                    sample_rate_hz,
                    overwrite,
                )
            output.append(
                build_segment_row(
                    row,
                    destination,
                    segment_index,
                    start_s,
                    segment_length_s,
                    sample_rate_hz,
                    status,
                    message,
                )
            )
    return output


def load_inventory(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_manifest(rows: list[dict[str, str]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def segment_inventory(
    inventory: Path,
    segments_dir: Path,
    output: Path,
    segment_length_s: float,
    sample_rate_hz: int,
    dry_run: bool,
    overwrite: bool,
    per_file_limit: int | None,
) -> list[dict[str, str]]:
    rows = build_segment_rows(
        load_inventory(inventory),
        segments_dir,
        segment_length_s,
        sample_rate_hz,
        dry_run,
        overwrite,
        per_file_limit,
    )
    write_manifest(rows, output)
    return rows


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inventory", type=Path, default=DEFAULT_INVENTORY)
    parser.add_argument("--segments-dir", type=Path, default=DEFAULT_SEGMENTS_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--segment-length-s", type=float, default=3.0)
    parser.add_argument("--sample-rate-hz", type=int, default=48000)
    parser.add_argument("--per-file-limit", type=int)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    rows = segment_inventory(
        args.inventory,
        args.segments_dir,
        args.output,
        args.segment_length_s,
        args.sample_rate_hz,
        args.dry_run,
        args.overwrite,
        args.per_file_limit,
    )
    statuses: dict[str, int] = {}
    for row in rows:
        statuses[row["status"]] = statuses.get(row["status"], 0) + 1
    summary = ", ".join(f"{key}={value}" for key, value in sorted(statuses.items()))
    print(f"Processed {len(rows)} segments: {summary}")
    print(f"Manifest: {args.output}")
    return 1 if statuses.get("error") else 0


if __name__ == "__main__":
    raise SystemExit(main())
