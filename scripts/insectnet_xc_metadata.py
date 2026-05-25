#!/usr/bin/env python3
"""Collect Xeno-canto API v3 metadata for InsectNet."""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = (
    ROOT
    / "JCH_Inbox/03_PROJECTS/03_WILDNEXUS/06_COMPONENTS/BIOACOUSTIC/"
    / "INSECTNET/02_DATASET/metadata.csv"
)
API_ENDPOINT = "https://xeno-canto.org/api/3/recordings"


FIELDNAMES = [
    "recording_id",
    "source",
    "source_url",
    "download_url",
    "file_name",
    "local_path",
    "genus",
    "species",
    "species_latin",
    "species_common_en",
    "group",
    "country",
    "location",
    "latitude",
    "longitude",
    "altitude_m",
    "date_recorded",
    "time_recorded",
    "uploaded_date",
    "recordist",
    "license_url",
    "license_class",
    "quality",
    "sound_type",
    "sex",
    "life_stage",
    "method",
    "animal_seen",
    "playback_used",
    "temperature_c",
    "device",
    "microphone",
    "sample_rate_hz",
    "duration_text",
    "duration_s",
    "remarks",
    "quality_flag",
    "usable_for_training",
    "usable_for_public_release",
    "split",
    "notes",
]


def parse_duration_seconds(value: str | None) -> float | str:
    if not value:
        return ""
    parts = value.split(":")
    try:
        if len(parts) == 2:
            return int(parts[0]) * 60 + float(parts[1])
        if len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
    except ValueError:
        return ""
    return ""


def as_int_or_empty(value: str | int | None) -> int | str:
    if value in (None, ""):
        return ""
    try:
        return int(value)
    except (TypeError, ValueError):
        return ""


def as_float_or_empty(value: str | int | float | None) -> float | str:
    if value in (None, ""):
        return ""
    try:
        return float(value)
    except (TypeError, ValueError):
        return ""


def classify_license(license_url: str | None) -> str:
    value = (license_url or "").lower()
    if "publicdomain/zero" in value or "cc0" in value:
        return "open"
    if "by-nc-nd" in value or "by-nd" in value:
        return "no_derivatives"
    if "by-nc" in value:
        return "non_commercial"
    if "creativecommons.org/licenses/by" in value:
        return "open"
    return "unknown"


def derive_quality_flag(recording: dict[str, object], license_class: str) -> str:
    quality = str(recording.get("q") or "").upper()
    playback = str(recording.get("playback-used") or "").lower()
    download_url = str(recording.get("file") or "")

    if not download_url or license_class == "unknown":
        return "reject"
    if quality not in {"A", "B"}:
        return "review"
    if playback == "yes":
        return "review"
    return "ok"


def map_recording(recording: dict[str, object]) -> dict[str, object]:
    genus = str(recording.get("gen") or "")
    species = str(recording.get("sp") or "")
    license_url = str(recording.get("lic") or "")
    license_class = classify_license(license_url)
    quality_flag = derive_quality_flag(recording, license_class)

    usable_for_training = quality_flag == "ok" and license_class in {
        "open",
        "non_commercial",
    }
    usable_for_public_release = quality_flag == "ok" and license_class == "open"

    return {
        "recording_id": recording.get("id") or "",
        "source": "xeno-canto",
        "source_url": recording.get("url") or "",
        "download_url": recording.get("file") or "",
        "file_name": recording.get("file-name") or "",
        "local_path": "",
        "genus": genus,
        "species": species,
        "species_latin": " ".join(part for part in (genus, species) if part),
        "species_common_en": recording.get("en") or "",
        "group": recording.get("grp") or "",
        "country": recording.get("cnt") or "",
        "location": recording.get("loc") or "",
        "latitude": as_float_or_empty(recording.get("lat")),
        "longitude": as_float_or_empty(recording.get("lon")),
        "altitude_m": as_int_or_empty(recording.get("alt")),
        "date_recorded": recording.get("date") or "",
        "time_recorded": recording.get("time") or "",
        "uploaded_date": recording.get("uploaded") or "",
        "recordist": recording.get("rec") or "",
        "license_url": license_url,
        "license_class": license_class,
        "quality": recording.get("q") or "",
        "sound_type": recording.get("type") or "",
        "sex": recording.get("sex") or "",
        "life_stage": recording.get("stage") or "",
        "method": recording.get("method") or "",
        "animal_seen": recording.get("animal-seen") or "",
        "playback_used": recording.get("playback-used") or "",
        "temperature_c": as_float_or_empty(recording.get("temp")),
        "device": recording.get("dvc") or "",
        "microphone": recording.get("mic") or "",
        "sample_rate_hz": as_int_or_empty(recording.get("smp")),
        "duration_text": recording.get("length") or "",
        "duration_s": parse_duration_seconds(str(recording.get("length") or "")),
        "remarks": recording.get("rmk") or "",
        "quality_flag": quality_flag,
        "usable_for_training": "yes" if usable_for_training else "no",
        "usable_for_public_release": "yes" if usable_for_public_release else "no",
        "split": "",
        "notes": "",
    }


def build_url(query: str, key: str, page: int, per_page: int) -> str:
    params = urlencode(
        {
            "query": query,
            "key": key,
            "page": page,
            "per_page": per_page,
        }
    )
    return f"{API_ENDPOINT}?{params}"


def fetch_json(url: str) -> dict[str, object]:
    with urlopen(url, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def collect_metadata(
    query: str,
    key: str,
    per_page: int,
    limit_pages: int | None,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    page = 1
    total_pages = 1

    while page <= total_pages:
        payload = fetch_json(build_url(query, key, page, per_page))
        if "error" in payload:
            message = payload.get("message") or payload.get("error")
            raise RuntimeError(f"Xeno-canto API error: {message}")

        total_pages = int(payload.get("numPages") or 1)
        for recording in payload.get("recordings") or []:
            if isinstance(recording, dict):
                rows.append(map_recording(recording))

        if limit_pages is not None and page >= limit_pages:
            break
        page += 1

    return rows


def write_csv(rows: list[dict[str, object]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--query",
        default="gen:Tettigonia sp:viridissima",
        help="Xeno-canto tagged search query.",
    )
    parser.add_argument(
        "--species-name",
        help="Optional species label used only for console output.",
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--per-page", type=int, default=100)
    parser.add_argument("--limit-pages", type=int)
    parser.add_argument(
        "--api-key-env",
        default="XC_API_KEY",
        help="Environment variable containing the Xeno-canto API key.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    key = os.environ.get(args.api_key_env)
    if not key:
        print(f"Missing API key environment variable: {args.api_key_env}", file=sys.stderr)
        return 2

    rows = collect_metadata(args.query, key, args.per_page, args.limit_pages)
    write_csv(rows, args.output)
    label = f" for {args.species_name}" if args.species_name else ""
    print(f"Wrote {len(rows)} rows{label} to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
