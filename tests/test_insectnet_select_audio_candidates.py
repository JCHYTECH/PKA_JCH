from scripts import insectnet_select_audio_candidates as select


def base_row(**overrides):
    row = {
        "species_latin": "Tettigonia viridissima",
        "recording_id": "1",
        "source": "xeno-canto",
        "source_url": "https://xeno-canto.org/1",
        "download_url": "https://xeno-canto.org/1/download",
        "file_name": "one.wav",
        "country": "France",
        "quality": "A",
        "quality_flag": "ok",
        "license_class": "open",
        "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
        "method": "field recording",
        "playback_used": "no",
        "animal_seen": "yes",
        "sample_rate_hz": "96000",
        "duration_s": "12",
        "recordist": "Recordist",
        "usable_for_public_release": "yes",
    }
    row.update(overrides)
    return row


def test_is_candidate_accepts_clean_open_field_recording():
    assert select.is_candidate(base_row())


def test_is_candidate_rejects_playback_or_non_public_license():
    assert not select.is_candidate(base_row(playback_used="yes"))
    assert not select.is_candidate(
        base_row(license_class="non_commercial", usable_for_public_release="no")
    )


def test_select_for_species_prefers_quality_then_sample_rate():
    rows = [
        base_row(recording_id="b-low", quality="B", sample_rate_hz="384000"),
        base_row(recording_id="a-low", quality="A", sample_rate_hz="48000"),
        base_row(recording_id="a-high", quality="A", sample_rate_hz="192000"),
    ]

    selected = select.select_for_species("Tettigonia viridissima", rows, per_species=2)

    assert [row["recording_id"] for row in selected] == ["a-high", "a-low"]
    assert selected[0]["selection_rank"] == "1"
    assert "sample_rate=192000" in selected[0]["selection_reason"]
