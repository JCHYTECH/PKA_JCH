#!/usr/bin/env python3
"""Build a technical inventory for downloaded InsectNet audio files."""

from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
BASE_DIR = (
    ROOT
    / "JCH_Inbox/03_PROJECTS/03_WILDNEXUS/06_COMPONENTS/BIOACOUSTIC/"
    / "INSECTNET/03_AUDIO_DOWNLOADS"
)
DEFAULT_MANIFEST = BASE_DIR / "audio-download-manifest.csv"
DEFAULT_AUDIO_DIR = BASE_DIR / "audio"
DEFAULT_OUTPUT = BASE_DIR / "audio-inventory.csv"


OUTPUT_FIELDS = [
    "species_latin",
    "recording_id",
    "source_url",
    "download_url",
    "file_name",
    "local_path",
    "probe_status",
    "format_name",
    "codec_name",
    "actual_sample_rate_hz",
    "manifest_sample_rate_hz",
    "channels",
    "actual_duration_s",
    "manifest_duration_s",
    "bytes",
    "quality",
    "message",
]


def slug(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "-", value.strip().lower()).strip("-")
    return cleaned or "unknown"


def safe_filename(row: dict[str, str]) -> str:
    raw = row.get("file_name") or f"XC{row.get('recording_id', 'unknown')}.wav"
    return re.sub(r"[^A-Za-z0-9._+ -]+", "_", Path(raw).name)


def audio_path(row: dict[str, str], audio_dir: Path) -> Path:
    return audio_dir / slug(row.get("species_latin", "unknown")) / safe_filename(row)


def _string_number(value: object, decimals: int = 3) -> str:
    if value in (None, ""):
        return ""
    try:
        return f"{float(value):.{decimals}f}"
    except (TypeError, ValueError):
        return str(value)


def parse_ffprobe_result(payload: dict[str, object]) -> dict[str, str]:
    streams = payload.get("streams")
    if not isinstance(streams, list):
        streams = []
    audio_stream = next(
        (
            stream
            for stream in streams
            if isinstance(stream, dict) and stream.get("codec_type") == "audio"
        ),
        None,
    )
    if audio_stream is None:
        return {
            "probe_status": "error",
            "format_name": "",
            "codec_name": "",
            "actual_sample_rate_hz": "",
            "channels": "",
            "actual_duration_s": "",
            "bytes": "",
            "message": "no audio stream",
        }

    fmt = payload.get("format") if isinstance(payload.get("format"), dict) else {}
    return {
        "probe_status": "ok",
        "format_name": str(fmt.get("format_name") or ""),
        "codec_name": str(audio_stream.get("codec_name") or ""),
        "actual_sample_rate_hz": str(audio_stream.get("sample_rate") or ""),
        "channels": str(audio_stream.get("channels") or ""),
        "actual_duration_s": _string_number(fmt.get("duration")),
        "bytes": str(fmt.get("size") or ""),
        "message": "",
    }


def probe_audio(path: Path) -> dict[str, str]:
    command = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=format_name,duration,size:stream=codec_type,codec_name,sample_rate,channels",
        "-of",
        "json",
        str(path),
    ]
    result = subprocess.run(command, check=False, capture_output=True, text=True)
    if result.returncode != 0:
        return {
            "probe_status": "error",
            "format_name": "",
            "codec_name": "",
            "actual_sample_rate_hz": "",
            "channels": "",
            "actual_duration_s": "",
            "bytes": "",
            "message": result.stderr.strip() or f"ffprobe exited {result.returncode}",
        }
    try:
        return parse_ffprobe_result(json.loads(result.stdout))
    except json.JSONDecodeError as exc:
        return {
            "probe_status": "error",
            "format_name": "",
            "codec_name": "",
            "actual_sample_rate_hz": "",
            "channels": "",
            "actual_duration_s": "",
            "bytes": "",
            "message": f"invalid ffprobe json: {exc}",
        }


def inventory_row(row: dict[str, str], audio_dir: Path) -> dict[str, str]:
    path = audio_path(row, audio_dir)
    output = {
        "species_latin": row.get("species_latin", ""),
        "recording_id": row.get("recording_id", ""),
        "source_url": row.get("source_url", ""),
        "download_url": row.get("download_url", ""),
        "file_name": row.get("file_name", ""),
        "local_path": str(path),
        "manifest_sample_rate_hz": row.get("sample_rate_hz", ""),
        "manifest_duration_s": row.get("duration_s", ""),
        "quality": row.get("quality", ""),
    }
    if not path.exists():
        output.update(
            {
                "probe_status": "missing",
                "format_name": "",
                "codec_name": "",
                "actual_sample_rate_hz": "",
                "channels": "",
                "actual_duration_s": "",
                "bytes": "",
                "message": "file not found",
            }
        )
        return output

    output.update(probe_audio(path))
    return output


def load_manifest(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_inventory(rows: list[dict[str, str]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def build_inventory(
    manifest: Path, audio_dir: Path, output: Path, limit: int | None
) -> list[dict[str, str]]:
    rows = load_manifest(manifest)
    if limit is not None:
        rows = rows[:limit]
    inventory = [inventory_row(row, audio_dir) for row in rows]
    write_inventory(inventory, output)
    return inventory


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--audio-dir", type=Path, default=DEFAULT_AUDIO_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--limit", type=int)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    rows = build_inventory(args.manifest, args.audio_dir, args.output, args.limit)
    statuses: dict[str, int] = {}
    for row in rows:
        statuses[row["probe_status"]] = statuses.get(row["probe_status"], 0) + 1
    summary = ", ".join(f"{key}={value}" for key, value in sorted(statuses.items()))
    print(f"Processed {len(rows)} rows: {summary}")
    print(f"Inventory: {args.output}")
    return 1 if statuses.get("error") or statuses.get("missing") else 0


if __name__ == "__main__":
    raise SystemExit(main())
