from pathlib import Path

from scripts import insectnet_generate_spectrograms as spec


def segment_row(**overrides):
    row = {
        "species_latin": "Tettigonia viridissima",
        "recording_id": "969762",
        "target_path": "/tmp/segments/tettigonia-viridissima/XC969762_seg001_start003.000s.wav",
        "segment_index": "1",
        "start_s": "3.000",
        "duration_s": "3.000",
        "status": "created",
    }
    row.update(overrides)
    return row


def test_spectrogram_path_groups_by_species_and_uses_segment_stem():
    path = spec.spectrogram_path(segment_row(), Path("/tmp/spectrograms"))

    assert path == Path(
        "/tmp/spectrograms/tettigonia-viridissima/"
        "XC969762_seg001_start003.000s.png"
    )


def test_ffmpeg_command_uses_showspectrumpic_filter():
    command = spec.ffmpeg_command(
        Path("/tmp/source.wav"),
        Path("/tmp/out.png"),
        size="1024x512",
        color="viridis",
        overwrite=False,
    )

    assert command[:4] == ["ffmpeg", "-hide_banner", "-loglevel", "error"]
    assert "-n" in command
    assert str(Path("/tmp/source.wav")) in command
    assert (
        "showspectrumpic=s=1024x512:mode=combined:color=viridis:legend=disabled"
        in command
    )
    assert str(Path("/tmp/out.png")) == command[-1]


def test_build_spectrogram_rows_dry_run_skips_unusable_segments(tmp_path):
    rows = spec.build_spectrogram_rows(
        [
            segment_row(),
            segment_row(status="error"),
            segment_row(target_path=""),
        ],
        tmp_path / "spectrograms",
        size="1024x512",
        color="viridis",
        dry_run=True,
        overwrite=False,
    )

    assert len(rows) == 1
    assert rows[0]["status"] == "dry-run"
    assert rows[0]["spectrogram_path"].endswith(
        "tettigonia-viridissima/XC969762_seg001_start003.000s.png"
    )
