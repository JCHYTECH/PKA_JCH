from pathlib import Path

from scripts import insectnet_segment_audio as seg


def inventory_row(**overrides):
    row = {
        "species_latin": "Gryllus campestris",
        "recording_id": "456",
        "local_path": "/tmp/audio/gryllus-campestris/XC456.wav",
        "probe_status": "ok",
        "actual_sample_rate_hz": "96000",
        "actual_duration_s": "10.2",
        "channels": "1",
        "quality": "A",
    }
    row.update(overrides)
    return row


def test_segment_count_uses_only_complete_segments():
    assert seg.segment_count(10.2, 3.0) == 3
    assert seg.segment_count(2.9, 3.0) == 0


def test_segment_path_groups_by_species_and_recording_id():
    path = seg.segment_path(
        inventory_row(),
        Path("/tmp/segments"),
        segment_index=2,
        segment_length_s=3.0,
    )

    assert path == Path(
        "/tmp/segments/gryllus-campestris/XC456_seg002_start006.000s.wav"
    )


def test_build_segment_rows_dry_run_without_ffmpeg(tmp_path):
    rows = seg.build_segment_rows(
        [inventory_row(actual_duration_s="7.1")],
        tmp_path / "segments",
        segment_length_s=3.0,
        sample_rate_hz=48000,
        dry_run=True,
        overwrite=False,
        per_file_limit=None,
    )

    assert len(rows) == 2
    assert rows[0]["status"] == "dry-run"
    assert rows[0]["start_s"] == "0.000"
    assert rows[1]["start_s"] == "3.000"
    assert rows[0]["target_path"].endswith("XC456_seg000_start000.000s.wav")


def test_build_segment_rows_skips_unusable_inventory_rows(tmp_path):
    rows = seg.build_segment_rows(
        [inventory_row(probe_status="missing"), inventory_row(actual_duration_s="2.0")],
        tmp_path / "segments",
        segment_length_s=3.0,
        sample_rate_hz=48000,
        dry_run=True,
        overwrite=False,
        per_file_limit=None,
    )

    assert rows == []
