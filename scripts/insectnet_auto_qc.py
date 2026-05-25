#!/usr/bin/env python3
"""Add conservative automatic QC suggestions to InsectNet segment QC rows."""

from __future__ import annotations

import argparse
import csv
import math
import statistics
import wave
import sys
from collections import defaultdict
from pathlib import Path

from PIL import Image
import numpy as np


ROOT = Path(__file__).resolve().parent.parent
BASE_DIR = (
    ROOT
    / "JCH_Inbox/03_PROJECTS/03_WILDNEXUS/06_COMPONENTS/BIOACOUSTIC/"
    / "INSECTNET/03_AUDIO_DOWNLOADS"
)
DEFAULT_QC = BASE_DIR / "segment_qc.csv"
DEFAULT_OUTPUT = BASE_DIR / "segment_qc_auto.csv"


AUTO_FIELDS = [
    "auto_qc",
    "auto_reason",
    "auto_score",
    "active_pixel_ratio",
    "contrast_stddev",
    "mean_luminance",
    "audio_band_tag",
    "audio_band_reason",
    "dominant_freq_hz",
    "low_band_ratio",
    "mid_band_ratio",
    "high_band_ratio",
]

SPECIES_AUDIO_FIELDS = [
    "species_audio_median_hz",
    "species_audio_mean_hz",
    "species_audio_min_hz",
    "species_audio_max_hz",
    "species_audio_count",
    "species_audio_status",
    "species_audio_threshold_hz",
]


def _round(value: float) -> float:
    return round(value, 4)


def analyze_spectrogram(path: Path) -> dict[str, float]:
    with Image.open(path) as image:
        image = image.convert("RGB")
        pixels = list(image.getdata())

    if not pixels:
        return {
            "active_pixel_ratio": 0.0,
            "contrast_stddev": 0.0,
            "mean_luminance": 0.0,
        }

    luminance = [
        0.2126 * red + 0.7152 * green + 0.0722 * blue
        for red, green, blue in pixels
    ]
    mean = sum(luminance) / len(luminance)
    variance = sum((value - mean) ** 2 for value in luminance) / len(luminance)
    stddev = math.sqrt(variance)

    active = 0
    for red, green, blue in pixels:
        bright = 0.2126 * red + 0.7152 * green + 0.0722 * blue
        green_signal = green > red + 20 and green > blue * 0.75
        if bright > mean + stddev and green_signal:
            active += 1

    return {
        "active_pixel_ratio": _round(active / len(pixels)),
        "contrast_stddev": _round(stddev),
        "mean_luminance": _round(mean),
    }


def classify_metrics(metrics: dict[str, float]) -> dict[str, str]:
    active = metrics["active_pixel_ratio"]
    contrast = metrics["contrast_stddev"]
    mean = metrics["mean_luminance"]
    score = min(1.0, (active / 0.08) * 0.65 + (contrast / 55.0) * 0.35)

    if active < 0.006 or contrast < 4.0:
        auto_qc = "auto_reject_candidate"
        reason = "low_signal"
    elif mean > 180 and contrast < 18:
        auto_qc = "auto_reject_candidate"
        reason = "uniform_noise"
    elif active >= 0.045 and contrast >= 16:
        auto_qc = "auto_keep_candidate"
        reason = "structured_signal"
    else:
        auto_qc = "human_review"
        reason = "ambiguous"

    return {
        "auto_qc": auto_qc,
        "auto_reason": reason,
        "auto_score": f"{score:.4f}",
    }


def _dtype_for_sample_width(sample_width: int):
    if sample_width == 1:
        return np.uint8, 128.0
    if sample_width == 2:
        return np.int16, 0.0
    if sample_width == 4:
        return np.int32, 0.0
    raise ValueError(f"unsupported sample width: {sample_width}")


def analyze_audio_band(path: Path, max_seconds: float = 2.0) -> dict[str, float]:
    with wave.open(str(path), "rb") as wav_file:
        sample_rate = wav_file.getframerate()
        channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()
        frame_limit = min(wav_file.getnframes(), int(sample_rate * max_seconds))
        raw = wav_file.readframes(frame_limit)

    dtype, offset = _dtype_for_sample_width(sample_width)
    audio = np.frombuffer(raw, dtype=dtype).astype(np.float64)
    if sample_width == 1:
        audio = audio - offset
    if channels > 1 and len(audio):
        audio = audio.reshape(-1, channels).mean(axis=1)
    audio = audio - audio.mean() if len(audio) else audio
    if not len(audio):
        return {
            "dominant_freq_hz": 0.0,
            "low_band_ratio": 0.0,
            "mid_band_ratio": 0.0,
            "high_band_ratio": 0.0,
        }

    window = np.hanning(len(audio))
    spectrum = np.abs(np.fft.rfft(audio * window)) ** 2
    freqs = np.fft.rfftfreq(len(audio), d=1.0 / sample_rate)
    total = float(spectrum.sum()) or 1.0

    low = float(spectrum[freqs < 8000].sum()) / total
    mid = float(spectrum[(freqs >= 8000) & (freqs < 12000)].sum()) / total
    high = float(spectrum[freqs >= 12000].sum()) / total
    dominant = float(freqs[int(np.argmax(spectrum))])

    return {
        "dominant_freq_hz": _round(dominant),
        "low_band_ratio": _round(low),
        "mid_band_ratio": _round(mid),
        "high_band_ratio": _round(high),
    }


def classify_audio_band(metrics: dict[str, float]) -> dict[str, str]:
    dominant = metrics["dominant_freq_hz"]
    low = metrics["low_band_ratio"]
    high = metrics["high_band_ratio"]

    if dominant >= 12000 or high >= 0.55:
        return {
            "audio_band_tag": "ultrasonic",
            "audio_band_reason": "high_frequency_dominant",
        }
    if dominant < 8000 and low >= 0.55:
        return {
            "audio_band_tag": "audible",
            "audio_band_reason": "low_frequency_dominant",
        }
    return {
        "audio_band_tag": "mixed",
        "audio_band_reason": "mixed_band",
    }


def compute_species_audio_profiles(
    rows: list[dict[str, str]],
    threshold_hz: float = 28000.0,
) -> dict[str, dict[str, str]]:
    grouped: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        species = row.get("species_latin", "").strip()
        if not species:
            continue
        try:
            value = float(row.get("dominant_freq_hz", "") or 0.0)
        except ValueError:
            continue
        if value > 0.0:
            grouped[species].append(value)

    profiles: dict[str, dict[str, str]] = {}
    for species, values in grouped.items():
        median = statistics.median(values)
        mean = sum(values) / len(values)
        status = "audible_list_exclude" if median > threshold_hz else "audible_list_keep"
        profiles[species] = {
            "species_latin": species,
            "species_audio_median_hz": f"{median:.4f}",
            "species_audio_mean_hz": f"{mean:.4f}",
            "species_audio_min_hz": f"{min(values):.4f}",
            "species_audio_max_hz": f"{max(values):.4f}",
            "species_audio_count": str(len(values)),
            "species_audio_status": status,
            "species_audio_threshold_hz": f"{threshold_hz:.1f}",
        }
    return profiles


def annotate_species_audio_policy(
    rows: list[dict[str, str]],
    threshold_hz: float = 28000.0,
) -> list[dict[str, str]]:
    profiles = compute_species_audio_profiles(rows, threshold_hz=threshold_hz)
    annotated: list[dict[str, str]] = []
    for row in rows:
        output = dict(row)
        species = row.get("species_latin", "").strip()
        profile = profiles.get(species)
        if profile:
            output.update({field: profile[field] for field in SPECIES_AUDIO_FIELDS})
        else:
            output.update({
                "species_audio_median_hz": "",
                "species_audio_mean_hz": "",
                "species_audio_min_hz": "",
                "species_audio_max_hz": "",
                "species_audio_count": "0",
                "species_audio_status": "unknown",
                "species_audio_threshold_hz": f"{threshold_hz:.1f}",
            })
        annotated.append(output)
    return annotated


def build_auto_qc_row(row: dict[str, str]) -> dict[str, str]:
    output = dict(row)
    path = Path(row.get("spectrogram_path", ""))
    if not path.exists():
        metrics = {
            "active_pixel_ratio": 0.0,
            "contrast_stddev": 0.0,
            "mean_luminance": 0.0,
        }
        classification = {
            "auto_qc": "human_review",
            "auto_reason": "missing_spectrogram",
            "auto_score": "0.0000",
        }
    else:
        metrics = analyze_spectrogram(path)
        classification = classify_metrics(metrics)

    audio_metrics = {
        "dominant_freq_hz": 0.0,
        "low_band_ratio": 0.0,
        "mid_band_ratio": 0.0,
        "high_band_ratio": 0.0,
    }
    audio_classification = {
        "audio_band_tag": "unknown",
        "audio_band_reason": "missing_audio",
    }
    audio_path = Path(row.get("segment_path", ""))
    if audio_path.exists():
        try:
            audio_metrics = analyze_audio_band(audio_path)
            audio_classification = classify_audio_band(audio_metrics)
        except Exception:
            audio_classification = {
                "audio_band_tag": "unknown",
                "audio_band_reason": "analysis_error",
            }

    output.update(classification)
    output.update({key: f"{value:.4f}" for key, value in metrics.items()})
    output.update(audio_classification)
    output.update({key: f"{value:.4f}" for key, value in audio_metrics.items()})
    return output


def load_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def write_csv(fieldnames: list[str], rows: list[dict[str, str]], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def add_auto_qc(
    qc_path: Path,
    output: Path,
    profile_output: Path | None = None,
) -> list[dict[str, str]]:
    fields, rows = load_csv(qc_path)
    output_fields = fields + [field for field in AUTO_FIELDS if field not in fields]
    output_fields += [field for field in SPECIES_AUDIO_FIELDS if field not in output_fields]
    scored = [build_auto_qc_row(row) for row in rows]
    scored = annotate_species_audio_policy(scored)
    write_csv(output_fields, scored, output)
    if profile_output is None:
        profile_output = output.with_name("species_audio_profile.csv")
    profiles = compute_species_audio_profiles(scored)
    profile_rows = [profiles[species] for species in sorted(profiles)]
    write_csv(
        [
            "species_latin",
            "species_audio_status",
            "species_audio_threshold_hz",
            "species_audio_median_hz",
            "species_audio_mean_hz",
            "species_audio_min_hz",
            "species_audio_max_hz",
            "species_audio_count",
        ],
        profile_rows,
        profile_output,
    )
    return scored


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--qc", type=Path, default=DEFAULT_QC)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--profile-output", type=Path, default=None)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    rows = add_auto_qc(args.qc, args.output, args.profile_output)
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["auto_qc"]] = counts.get(row["auto_qc"], 0) + 1
    summary = ", ".join(f"{key}={value}" for key, value in sorted(counts.items()))
    print(f"Wrote {len(rows)} auto-QC rows to {args.output}")
    print(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
