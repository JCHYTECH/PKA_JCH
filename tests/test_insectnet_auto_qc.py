import math
import struct
import wave
from pathlib import Path

from pathlib import Path

from PIL import Image, ImageDraw

from scripts import insectnet_auto_qc as auto


def qc_row(path: Path, **overrides):
    row = {
        "species_latin": "Gryllus campestris",
        "recording_id": "123",
        "segment_index": "0",
        "spectrogram_path": str(path),
        "visual_qc": "review",
        "qc_reason": "unreviewed",
    }
    row.update(overrides)
    return row


def write_tone_wav(path: Path, sample_rate: int, frequency: float) -> None:
    duration_s = 1.0
    frames = int(sample_rate * duration_s)
    amplitude = 0.6
    with wave.open(str(path), "wb") as wav_file:
      wav_file.setnchannels(1)
      wav_file.setsampwidth(2)
      wav_file.setframerate(sample_rate)
      payload = bytearray()
      for index in range(frames):
          sample = int(
              amplitude
              * 32767
              * math.sin(2.0 * math.pi * frequency * (index / sample_rate))
          )
          payload.extend(struct.pack("<h", sample))
      wav_file.writeframes(bytes(payload))


def test_analyze_spectrogram_detects_empty_image(tmp_path):
    path = tmp_path / "empty.png"
    Image.new("RGB", (64, 32), color=(0, 0, 0)).save(path)

    metrics = auto.analyze_spectrogram(path)

    assert metrics["active_pixel_ratio"] == 0.0
    assert metrics["contrast_stddev"] == 0.0


def test_classify_auto_qc_rejects_low_signal():
    result = auto.classify_metrics(
        {
            "active_pixel_ratio": 0.0,
            "contrast_stddev": 0.0,
            "mean_luminance": 0.0,
        }
    )

    assert result["auto_qc"] == "auto_reject_candidate"
    assert result["auto_reason"] == "low_signal"


def test_classify_auto_qc_marks_pattern_as_keep_candidate(tmp_path):
    path = tmp_path / "pattern.png"
    image = Image.new("RGB", (120, 64), color=(25, 20, 65))
    draw = ImageDraw.Draw(image)
    for x in range(8, 120, 14):
        draw.rectangle((x, 8, x + 4, 56), fill=(40, 210, 130))
    image.save(path)

    result = auto.classify_metrics(auto.analyze_spectrogram(path))

    assert result["auto_qc"] == "auto_keep_candidate"
    assert result["auto_reason"] == "structured_signal"


def test_build_auto_qc_row_preserves_human_fields(tmp_path):
    path = tmp_path / "empty.png"
    Image.new("RGB", (64, 32), color=(0, 0, 0)).save(path)

    row = auto.build_auto_qc_row(qc_row(path, visual_qc="keep", notes="manual"))

    assert row["visual_qc"] == "keep"
    assert row["notes"] == "manual"
    assert row["auto_qc"] == "auto_reject_candidate"
    assert "auto_score" in row


def test_analyze_audio_band_detects_ultrasonic_tone(tmp_path):
    path = tmp_path / "ultrasonic.wav"
    write_tone_wav(path, sample_rate=96000, frequency=30000)

    metrics = auto.analyze_audio_band(path)
    classification = auto.classify_audio_band(metrics)

    assert classification["audio_band_tag"] == "ultrasonic"
    assert classification["audio_band_reason"] == "high_frequency_dominant"
    assert metrics["dominant_freq_hz"] > 20000


def test_analyze_audio_band_detects_audible_tone(tmp_path):
    path = tmp_path / "audible.wav"
    write_tone_wav(path, sample_rate=48000, frequency=1000)

    metrics = auto.analyze_audio_band(path)
    classification = auto.classify_audio_band(metrics)

    assert classification["audio_band_tag"] == "audible"
    assert classification["audio_band_reason"] == "low_frequency_dominant"
    assert metrics["dominant_freq_hz"] < 2000


def test_compute_species_audio_profiles_marks_high_frequency_species():
    rows = [
        {
            "species_latin": "Audible species",
            "dominant_freq_hz": "12000.0",
        },
        {
            "species_latin": "Audible species",
            "dominant_freq_hz": "14000.0",
        },
        {
            "species_latin": "Ultrasonic species",
            "dominant_freq_hz": "30000.0",
        },
        {
            "species_latin": "Ultrasonic species",
            "dominant_freq_hz": "32000.0",
        },
    ]

    profiles = auto.compute_species_audio_profiles(rows, threshold_hz=28000)

    assert profiles["Audible species"]["species_audio_status"] == "audible_list_keep"
    assert profiles["Audible species"]["species_audio_median_hz"] == "13000.0000"
    assert profiles["Ultrasonic species"]["species_audio_status"] == "audible_list_exclude"
    assert profiles["Ultrasonic species"]["species_audio_median_hz"] == "31000.0000"
