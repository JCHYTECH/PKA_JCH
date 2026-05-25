#!/usr/bin/env python3
"""Generate PNG spectrograms for InsectNet audio segments with ffmpeg."""

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
DEFAULT_SEGMENTS_MANIFEST = BASE_DIR / "segments-manifest.csv"
DEFAULT_SPECTROGRAMS_DIR = BASE_DIR / "spectrograms"
DEFAULT_OUTPUT = BASE_DIR / "spectrogram-manifest.csv"


OUTPUT_FIELDS = [
    "created_at",
    "species_latin",
    "recording_id",
    "segment_index",
    "start_s",
    "duration_s",
    "segment_path",
    "spectrogram_path",
    "size",
    "color",
    "status",
    "message",
]


def slug(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "-", value.strip().lower()).strip("-")
    return cleaned or "unknown"


def spectrogram_path(row: dict[str, str], spectrograms_dir: Path) -> Path:
    source = Path(row.get("target_path", "segment.wav"))
    return (
        spectrograms_dir
        / slug(row.get("species_latin", "unknown"))
        / f"{source.stem}.png"
    )


def is_usable_segment_row(row: dict[str, str]) -> bool:
    return row.get("status") in {"created", "skipped-existing"} and bool(
        row.get("target_path")
    )


def ffmpeg_command(
    source: Path,
    destination: Path,
    size: str,
    color: str,
    overwrite: bool,
) -> list[str]:
    return [
        "ffmpeg",
        "-hide_banner",
        "-loglevel",
        "error",
        "-y" if overwrite else "-n",
        "-i",
        str(source),
        "-lavfi",
        f"showspectrumpic=s={size}:mode=combined:color={color}:legend=disabled",
        str(destination),
    ]


def run_ffmpeg_spectrogram(
    source: Path,
    destination: Path,
    size: str,
    color: str,
    overwrite: bool,
) -> tuple[str, str]:
    if destination.exists() and not overwrite:
        return "skipped-existing", ""

    destination.parent.mkdir(parents=True, exist_ok=True)
    result = subprocess.run(
        ffmpeg_command(source, destination, size, color, overwrite),
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return "error", result.stderr.strip() or f"ffmpeg exited {result.returncode}"
    return "created", ""


def build_spectrogram_row(
    row: dict[str, str],
    destination: Path,
    size: str,
    color: str,
    status: str,
    message: str,
) -> dict[str, str]:
    return {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "species_latin": row.get("species_latin", ""),
        "recording_id": row.get("recording_id", ""),
        "segment_index": row.get("segment_index", ""),
        "start_s": row.get("start_s", ""),
        "duration_s": row.get("duration_s", ""),
        "segment_path": row.get("target_path", ""),
        "spectrogram_path": str(destination),
        "size": size,
        "color": color,
        "status": status,
        "message": message,
    }


def build_spectrogram_rows(
    segment_rows: list[dict[str, str]],
    spectrograms_dir: Path,
    size: str,
    color: str,
    dry_run: bool,
    overwrite: bool,
) -> list[dict[str, str]]:
    output: list[dict[str, str]] = []
    for row in segment_rows:
        if not is_usable_segment_row(row):
            continue
        source = Path(row["target_path"])
        destination = spectrogram_path(row, spectrograms_dir)
        if dry_run:
            status, message = "dry-run", ""
        else:
            status, message = run_ffmpeg_spectrogram(
                source, destination, size, color, overwrite
            )
        output.append(
            build_spectrogram_row(row, destination, size, color, status, message)
        )
    return output


def load_segments(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_manifest(rows: list[dict[str, str]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def generate_spectrograms(
    segments_manifest: Path,
    spectrograms_dir: Path,
    output: Path,
    size: str,
    color: str,
    dry_run: bool,
    overwrite: bool,
) -> list[dict[str, str]]:
    rows = build_spectrogram_rows(
        load_segments(segments_manifest),
        spectrograms_dir,
        size,
        color,
        dry_run,
        overwrite,
    )
    write_manifest(rows, output)
    return rows


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--segments-manifest", type=Path, default=DEFAULT_SEGMENTS_MANIFEST)
    parser.add_argument("--spectrograms-dir", type=Path, default=DEFAULT_SPECTROGRAMS_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--size", default="1024x512")
    parser.add_argument("--color", default="viridis")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    rows = generate_spectrograms(
        args.segments_manifest,
        args.spectrograms_dir,
        args.output,
        args.size,
        args.color,
        args.dry_run,
        args.overwrite,
    )
    statuses: dict[str, int] = {}
    for row in rows:
        statuses[row["status"]] = statuses.get(row["status"], 0) + 1
    summary = ", ".join(f"{key}={value}" for key, value in sorted(statuses.items()))
    print(f"Processed {len(rows)} spectrograms: {summary}")
    print(f"Manifest: {args.output}")
    return 1 if statuses.get("error") else 0


if __name__ == "__main__":
    raise SystemExit(main())
