#!/usr/bin/env python3
"""Create per-species contact sheets for InsectNet spectrogram review."""

from __future__ import annotations

import argparse
import csv
import math
import re
import sys
from collections import defaultdict
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent.parent
BASE_DIR = (
    ROOT
    / "JCH_Inbox/03_PROJECTS/03_WILDNEXUS/06_COMPONENTS/BIOACOUSTIC/"
    / "INSECTNET/03_AUDIO_DOWNLOADS"
)
DEFAULT_SPECTROGRAM_MANIFEST = BASE_DIR / "spectrogram-manifest.csv"
DEFAULT_OUTPUT_DIR = BASE_DIR / "contact_sheets"


def slug(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9]+", "-", value.strip().lower()).strip("-")
    return cleaned or "unknown"


def group_rows_by_species(rows: list[dict[str, str]]) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        if row.get("status") in {"created", "skipped-existing"} and row.get(
            "spectrogram_path"
        ):
            grouped[row.get("species_latin", "unknown")].append(row)
    return dict(grouped)


def contact_sheet_path(species: str, output_dir: Path) -> Path:
    return output_dir / f"{slug(species)}-contact-sheet.png"


def label_for_row(row: dict[str, str]) -> str:
    return f"XC{row.get('recording_id', '?')} seg {row.get('segment_index', '?')}"


def create_contact_sheet(
    rows: list[dict[str, str]],
    output: Path,
    columns: int,
    thumb_width: int,
    label_height: int,
    max_images: int,
) -> None:
    selected = rows[:max_images]
    if not selected:
        return

    cells: list[tuple[Image.Image, str]] = []
    for row in selected:
        with Image.open(row["spectrogram_path"]) as image:
            image = image.convert("RGB")
            ratio = thumb_width / image.width
            thumb_height = max(1, int(image.height * ratio))
            image = image.resize((thumb_width, thumb_height))
            cells.append((image.copy(), label_for_row(row)))

    thumb_height = max(image.height for image, _label in cells)
    rows_count = math.ceil(len(cells) / columns)
    sheet = Image.new(
        "RGB",
        (columns * thumb_width, rows_count * (thumb_height + label_height)),
        color=(255, 255, 255),
    )
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.load_default()

    for index, (image, label) in enumerate(cells):
        col = index % columns
        row = index // columns
        x = col * thumb_width
        y = row * (thumb_height + label_height)
        sheet.paste(image, (x, y))
        draw.text((x + 4, y + thumb_height + 2), label[:28], fill=(0, 0, 0), font=font)

    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output)


def load_manifest(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def build_contact_sheets(
    manifest: Path,
    output_dir: Path,
    columns: int,
    thumb_width: int,
    label_height: int,
    max_images: int,
) -> list[Path]:
    written: list[Path] = []
    grouped = group_rows_by_species(load_manifest(manifest))
    for species, rows in sorted(grouped.items()):
        output = contact_sheet_path(species, output_dir)
        create_contact_sheet(rows, output, columns, thumb_width, label_height, max_images)
        written.append(output)
    return written


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_SPECTROGRAM_MANIFEST)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--columns", type=int, default=5)
    parser.add_argument("--thumb-width", type=int, default=320)
    parser.add_argument("--label-height", type=int, default=18)
    parser.add_argument("--max-images", type=int, default=25)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    paths = build_contact_sheets(
        args.manifest,
        args.output_dir,
        args.columns,
        args.thumb_width,
        args.label_height,
        args.max_images,
    )
    print(f"Wrote {len(paths)} contact sheets")
    for path in paths:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
