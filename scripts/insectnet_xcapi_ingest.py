#!/usr/bin/env python3
"""Ingest Xeno-Canto recordings via xcapi and enrich with InsectNet metadata.

Replaces the three-step pipeline:
  insectnet_xc_metadata.py → insectnet_select_audio_candidates.py → insectnet_download_audio.py

Usage:
  export XC_API_KEY=<key>
  python3 scripts/insectnet_xcapi_ingest.py --genus Tettigonia --species viridissima --box 44,5,48,13 --min_quality B --max 20

  # Or multiple species from alpine-species-inventory
  python3 scripts/insectnet_xcapi_ingest.py --genus Chorthippus --species "biguttulus,brunneus,mollis" --box 44,5,48,13

Output:
  INSECTNET/03_AUDIO_DOWNLOADS/<Genus_species>/   — audio files (xcapi native)
  INSECTNET/02_DATASET/<species>-metadata.csv      — enriched metadata

Model: deepseek-v4 (2026-06-13, intégration xcapi pipeline InsectNet)
"""

from __future__ import annotations

import argparse
import csv
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parent.parent
INSECTNET_ROOT = (
    ROOT / "JCH_Inbox/03_PROJECTS/03_WILDNEXUS/06_COMPONENTS/BIOACOUSTIC/INSECTNET"
)
XCAPI_BIN = ROOT / "bin/xcapi"

# ── Enrichment columns (added to xcapi output) ──────────────────────
ENRICH_COLUMNS = [
    "quality_flag",
    "license_class",
    "usable_for_training",
    "usable_for_public_release",
]

# ── License classification (from insectnet_xc_metadata.py) ──────────

def classify_license(license_url: str) -> str:
    """Classify a Xeno-Canto license URL into open / non_commercial / no_derivatives / unknown."""
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


def derive_quality_flag(quality: str, license_class: str, playback_used: str, file_url: str) -> str:
    """Derive quality_flag from xcapi fields."""
    q = (quality or "").upper().strip()
    pb = (playback_used or "").lower().strip()

    if not file_url or license_class == "unknown":
        return "reject"
    if q not in {"A", "B"}:
        return "review"
    if pb == "yes":
        return "review"
    return "ok"


# ── Main ─────────────────────────────────────────────────────────────

def run_xcapi(
    genus: Optional[str],
    species: Optional[str],
    box: Optional[str],
    min_quality: str,
    max_results: int,
    output_dir: Path,
    api_key: str,
    extra_args: list[str],
) -> Path:
    """Run xcapi and return path to the output directory."""
    cmd = [str(XCAPI_BIN)]
    if genus:
        cmd += ["--gen", genus]
    if species:
        cmd += ["--sp", species]
    if box:
        cmd += ["--box", box]
    if min_quality:
        cmd += ["--q", f">{min_quality}"]
    if max_results:
        cmd += ["--max_results", str(max_results)]
    cmd += ["--output_dir", str(output_dir)]
    cmd += ["--api_key", api_key]
    cmd += ["--per_page", "50"]
    cmd += extra_args

    print(f"[xcapi] {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(result.stderr, file=sys.stderr)
        raise RuntimeError(f"xcapi failed with exit code {result.returncode}")

    print(result.stdout)
    return output_dir


def enrich_metadata(xcapi_metadata_csv: Path, output_csv: Path) -> int:
    """Read xcapi metadata, add enrichment columns, write back."""
    rows = []
    with open(xcapi_metadata_csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        xcapi_fields = reader.fieldnames or []
        for row in reader:
            lic_url = row.get("lic", "")
            quality_raw = row.get("q", "")
            playback = row.get("playback-used", "")
            file_url = row.get("file", "")

            lic_class = classify_license(lic_url)
            qflag = derive_quality_flag(quality_raw, lic_class, playback, file_url)

            row["license_class"] = lic_class
            row["quality_flag"] = qflag
            row["usable_for_training"] = (
                "yes" if qflag == "ok" and lic_class in {"open", "non_commercial"} else "no"
            )
            row["usable_for_public_release"] = (
                "yes" if qflag == "ok" and lic_class == "open" else "no"
            )
            rows.append(row)

    all_fields = list(xcapi_fields) + ENRICH_COLUMNS
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=all_fields)
        writer.writeheader()
        writer.writerows(rows)

    return len(rows)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--genus", help="Genus filter (e.g. Tettigonia)")
    parser.add_argument("--species", help="Species filter, comma-separated")
    parser.add_argument("--box", help="Bounding box lat_min,lon_min,lat_max,lon_max")
    parser.add_argument("--min_quality", default="B", help="Minimum quality grade")
    parser.add_argument("--max", type=int, default=50, dest="max_results")
    parser.add_argument("--api-key-env", default="XC_API_KEY")
    parser.add_argument("--output-dir", help="Override output directory")
    parser.add_argument("extra", nargs="*", help="Extra arguments passed to xcapi")
    return parser.parse_args(argv or sys.argv[1:])


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    api_key = os.environ.get(args.api_key_env)
    if not api_key:
        print(f"Missing API key: {args.api_key_env}", file=sys.stderr)
        return 2

    if not args.genus and not args.species:
        print("At least --genus or --species is required.", file=sys.stderr)
        return 1

    species_list = [s.strip() for s in (args.species or "").split(",") if s.strip()]
    if not species_list and args.genus:
        species_list = [""]

    all_rows = 0
    output_base = Path(args.output_dir) if args.output_dir else (INSECTNET_ROOT / "03_AUDIO_DOWNLOADS")

    for sp in species_list:
        safe_sp = sp.replace(" ", "_") if sp else ""
        run_output = (
            output_base / f"{args.genus}_{safe_sp}"
            if (args.genus and safe_sp)
            else output_base / (safe_sp or args.genus or "xcapi_output")
        )

        try:
            run_xcapi(
                genus=args.genus, species=sp if sp else None, box=args.box,
                min_quality=args.min_quality, max_results=args.max_results,
                output_dir=run_output, api_key=api_key, extra_args=args.extra,
            )
        except RuntimeError:
            return 3

        xcapi_csv = run_output / "metadata.csv"
        if xcapi_csv.exists():
            dataset_dir = INSECTNET_ROOT / "02_DATASET"
            if args.genus and sp:
                enriched_name = f"{args.genus.lower()}-{sp.lower().replace(' ','-')}-metadata.csv"
            elif sp:
                enriched_name = f"{sp.lower().replace(' ','-')}-metadata.csv"
            else:
                enriched_name = f"{args.genus.lower()}-metadata.csv"
            enriched_csv = dataset_dir / enriched_name
            n = enrich_metadata(xcapi_csv, enriched_csv)
            all_rows += n
            print(f"[enrich] {enriched_csv.name}: {n} rows enriched")

    print(f"\nDone. {all_rows} total recordings ingested.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
