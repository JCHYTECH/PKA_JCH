#!/usr/bin/env python3
"""Download InsectNet audio files listed in a manifest."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from datetime import datetime
from pathlib import Path
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parent.parent
BASE_DIR = (
    ROOT
    / "JCH_Inbox/03_PROJECTS/03_WILDNEXUS/06_COMPONENTS/BIOACOUSTIC/"
    / "INSECTNET/03_AUDIO_DOWNLOADS"
)
DEFAULT_MANIFEST = BASE_DIR / "audio-download-manifest.csv"
DEFAULT_AUDIO_DIR = BASE_DIR / "audio"
DEFAULT_LOG = BASE_DIR / "download-log.csv"


LOG_FIELDS = [
    "downloaded_at",
    "species_latin",
    "recording_id",
    "source_url",
    "download_url",
    "target_path",
    "status",
    "bytes",
    "message",
]


def slug(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "-", value.strip().lower()).strip("-")
    return cleaned or "unknown"


def safe_filename(row: dict[str, str]) -> str:
    raw = row.get("file_name") or f"XC{row.get('recording_id', 'unknown')}.wav"
    name = Path(raw).name
    if not name.startswith(f"XC{row.get('recording_id', '')}"):
        name = f"XC{row.get('recording_id', 'unknown')}-{name}"
    return re.sub(r"[^A-Za-z0-9._+ -]+", "_", name)


def target_path(row: dict[str, str], audio_dir: Path) -> Path:
    species_dir = audio_dir / slug(row.get("species_latin", "unknown"))
    return species_dir / safe_filename(row)


def load_manifest(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def download_file(url: str, destination: Path, overwrite: bool = False) -> int:
    if destination.exists() and not overwrite:
        return destination.stat().st_size

    destination.parent.mkdir(parents=True, exist_ok=True)
    tmp = destination.with_suffix(destination.suffix + ".part")
    with urlopen(url, timeout=90) as response, tmp.open("wb") as handle:
        total = 0
        while True:
            chunk = response.read(1024 * 256)
            if not chunk:
                break
            handle.write(chunk)
            total += len(chunk)
    tmp.replace(destination)
    return total


def build_log_row(
    row: dict[str, str],
    destination: Path,
    status: str,
    bytes_written: int | str,
    message: str = "",
) -> dict[str, str]:
    return {
        "downloaded_at": datetime.now().isoformat(timespec="seconds"),
        "species_latin": row.get("species_latin", ""),
        "recording_id": row.get("recording_id", ""),
        "source_url": row.get("source_url", ""),
        "download_url": row.get("download_url", ""),
        "target_path": str(destination),
        "status": status,
        "bytes": str(bytes_written),
        "message": message,
    }


def write_log(rows: list[dict[str, str]], log_path: Path) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with log_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=LOG_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def download_manifest(
    manifest_path: Path,
    audio_dir: Path,
    log_path: Path,
    limit: int | None,
    overwrite: bool,
    dry_run: bool,
) -> list[dict[str, str]]:
    rows = load_manifest(manifest_path)
    if limit is not None:
        rows = rows[:limit]

    log_rows: list[dict[str, str]] = []
    for row in rows:
        destination = target_path(row, audio_dir)
        if dry_run:
            log_rows.append(build_log_row(row, destination, "dry-run", 0))
            continue
        try:
            existed = destination.exists()
            bytes_written = download_file(row["download_url"], destination, overwrite)
            status = "skipped-existing" if existed and not overwrite else "downloaded"
            log_rows.append(build_log_row(row, destination, status, bytes_written))
        except Exception as exc:  # pragma: no cover - operational logging path
            log_rows.append(build_log_row(row, destination, "error", "", str(exc)))

    write_log(log_rows, log_path)
    return log_rows


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--audio-dir", type=Path, default=DEFAULT_AUDIO_DIR)
    parser.add_argument("--log", type=Path, default=DEFAULT_LOG)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    log_rows = download_manifest(
        args.manifest,
        args.audio_dir,
        args.log,
        args.limit,
        args.overwrite,
        args.dry_run,
    )
    statuses: dict[str, int] = {}
    for row in log_rows:
        statuses[row["status"]] = statuses.get(row["status"], 0) + 1
    summary = ", ".join(f"{key}={value}" for key, value in sorted(statuses.items()))
    print(f"Processed {len(log_rows)} rows: {summary}")
    print(f"Log: {args.log}")
    return 1 if statuses.get("error") else 0


if __name__ == "__main__":
    raise SystemExit(main())
