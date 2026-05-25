from pathlib import Path

from scripts import insectnet_audio_inventory as inv


def manifest_row(**overrides):
    row = {
        "species_latin": "Tettigonia viridissima",
        "recording_id": "123",
        "source_url": "https://xeno-canto.org/123",
        "download_url": "https://xeno-canto.org/123/download",
        "file_name": "XC123-clean.wav",
        "quality": "A",
        "sample_rate_hz": "96000",
    }
    row.update(overrides)
    return row


def test_audio_path_groups_manifest_rows_by_species():
    path = inv.audio_path(manifest_row(), Path("/tmp/audio"))

    assert path == Path("/tmp/audio/tettigonia-viridissima/XC123-clean.wav")


def test_parse_ffprobe_result_extracts_audio_stream_and_format():
    payload = {
        "streams": [
            {"codec_type": "video", "codec_name": "png"},
            {
                "codec_type": "audio",
                "codec_name": "pcm_s16le",
                "sample_rate": "48000",
                "channels": 2,
            },
        ],
        "format": {"duration": "12.345", "size": "98765", "format_name": "wav"},
    }

    result = inv.parse_ffprobe_result(payload)

    assert result["probe_status"] == "ok"
    assert result["codec_name"] == "pcm_s16le"
    assert result["actual_sample_rate_hz"] == "48000"
    assert result["channels"] == "2"
    assert result["actual_duration_s"] == "12.345"
    assert result["bytes"] == "98765"
    assert result["format_name"] == "wav"


def test_inventory_row_marks_missing_local_file(tmp_path):
    row = manifest_row()

    output = inv.inventory_row(row, tmp_path / "audio")

    assert output["probe_status"] == "missing"
    assert output["species_latin"] == "Tettigonia viridissima"
    assert output["recording_id"] == "123"
    assert output["local_path"].endswith("tettigonia-viridissima/XC123-clean.wav")
