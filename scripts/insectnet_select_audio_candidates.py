#!/usr/bin/env python3
"""Select clean audio download candidates for InsectNet."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DATASET_DIR = (
    ROOT
    / "JCH_Inbox/03_PROJECTS/03_WILDNEXUS/06_COMPONENTS/BIOACOUSTIC/"
    / "INSECTNET/02_DATASET"
)
DEFAULT_OUTPUT = (
    ROOT
    / "JCH_Inbox/03_PROJECTS/03_WILDNEXUS/06_COMPONENTS/BIOACOUSTIC/"
    / "INSECTNET/03_AUDIO_DOWNLOADS/audio-download-manifest.csv"
)


SPECIES_FILES = {
    "Tettigonia viridissima": DATASET_DIR / "metadata.csv",
    "Gryllus campestris": DATASET_DIR / "gryllus-campestris-metadata.csv",
    "Pholidoptera griseoaptera": DATASET_DIR / "pholidoptera-griseoaptera-metadata.csv",
    "Leptophyes punctatissima": DATASET_DIR / "leptophyes-punctatissima-metadata.csv",
    "Roeseliana roeselii": DATASET_DIR / "roeseliana-roeselii-metadata.csv",
}


OUTPUT_FIELDS = [
    "species_latin",
    "recording_id",
    "source",
    "source_url",
    "download_url",
    "file_name",
    "country",
    "quality",
    "quality_flag",
    "license_class",
    "license_url",
    "method",
    "playback_used",
    "animal_seen",
    "sample_rate_hz",
    "duration_s",
    "recordist",
    "selection_rank",
    "selection_reason",
]


QUALITY_SCORE = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "": 9}


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def sample_rate(row: dict[str, str]) -> int:
    try:
        return int(row.get("sample_rate_hz") or 0)
    except ValueError:
        return 0


def duration(row: dict[str, str]) -> float:
    try:
        return float(row.get("duration_s") or 0)
    except ValueError:
        return 0


def is_candidate(row: dict[str, str]) -> bool:
    return (
        row.get("download_url")
        and row.get("quality_flag") == "ok"
        and row.get("usable_for_public_release") == "yes"
        and row.get("playback_used") == "no"
        and row.get("method") == "field recording"
        and row.get("license_class") == "open"
        and row.get("quality") in {"A", "B"}
        and sample_rate(row) >= 44100
        and duration(row) > 0
    )


def sort_key(row: dict[str, str]) -> tuple[int, int, float, str]:
    return (
        QUALITY_SCORE.get(row.get("quality", ""), 9),
        -sample_rate(row),
        duration(row),
        row.get("recording_id", ""),
    )


def selection_reason(row: dict[str, str]) -> str:
    return (
        f"quality={row.get('quality')}; "
        f"license={row.get('license_class')}; "
        f"method={row.get('method')}; "
        f"playback={row.get('playback_used')}; "
        f"sample_rate={row.get('sample_rate_hz')}"
    )


def select_for_species(
    species: str, rows: list[dict[str, str]], per_species: int
) -> list[dict[str, str]]:
    selected: list[dict[str, str]] = []
    for rank, row in enumerate(sorted(filter(is_candidate, rows), key=sort_key), 1):
        output = {field: row.get(field, "") for field in OUTPUT_FIELDS}
        output["species_latin"] = species
        output["selection_rank"] = str(rank)
        output["selection_reason"] = selection_reason(row)
        selected.append(output)
        if len(selected) >= per_species:
            break
    return selected


def build_manifest(per_species: int) -> list[dict[str, str]]:
    manifest: list[dict[str, str]] = []
    for species, path in SPECIES_FILES.items():
        manifest.extend(select_for_species(species, load_rows(path), per_species))
    return manifest


def write_manifest(rows: list[dict[str, str]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--per-species", type=int, default=20)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    manifest = build_manifest(args.per_species)
    write_manifest(manifest, args.output)
    print(f"Wrote {len(manifest)} candidates to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
