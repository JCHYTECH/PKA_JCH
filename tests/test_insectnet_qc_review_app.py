from pathlib import Path

from scripts import insectnet_qc_review_app as app


def qc_row(**overrides):
    row = {
        "species_latin": "Gryllus campestris",
        "recording_id": "123",
        "segment_index": "4",
        "start_s": "12.000",
        "duration_s": "3.000",
        "segment_path": "/tmp/insectnet/segments/XC123_seg004.wav",
        "spectrogram_path": "/tmp/insectnet/spectrograms/XC123_seg004.png",
        "visual_qc": "review",
        "qc_reason": "unreviewed",
        "reviewed_by": "",
        "notes": "",
        "auto_qc": "auto_keep_candidate",
        "auto_reason": "structured_signal",
        "auto_score": "0.8500",
        "audio_band_tag": "ultrasonic",
        "audio_band_reason": "high_frequency_dominant",
        "dominant_freq_hz": "30000.0000",
        "low_band_ratio": "0.0500",
        "mid_band_ratio": "0.1000",
        "high_band_ratio": "0.8500",
        "species_audio_status": "audible_list_keep",
        "species_audio_median_hz": "13000.0000",
        "species_audio_threshold_hz": "28000.0000",
    }
    row.update(overrides)
    return row


def test_file_uri_encodes_absolute_paths():
    uri = app.file_uri("/tmp/insectnet/some file.wav")

    assert uri == "file:///tmp/insectnet/some%20file.wav"


def test_prepare_records_adds_media_uris_without_replacing_csv_paths():
    record = app.prepare_records([qc_row()])[0]

    assert record["segment_path"] == "/tmp/insectnet/segments/XC123_seg004.wav"
    assert record["audio_uri"] == "file:///tmp/insectnet/segments/XC123_seg004.wav"
    assert record["spectrogram_uri"] == (
        "file:///tmp/insectnet/spectrograms/XC123_seg004.png"
    )


def test_species_options_are_sorted_unique():
    species = app.species_options(
        [qc_row(species_latin="B species"), qc_row(species_latin="A species")]
    )

    assert species == ["A species", "B species"]


def test_render_html_embeds_records_and_export_function():
    html = app.render_html([qc_row()], title="InsectNet QC")

    assert "InsectNet QC" in html
    assert "const QC_RECORDS =" in html
    assert "downloadCsv" in html
    assert "Gryllus campestris" in html
    assert "data-action=\"keep\"" in html
    assert "Auto suggestion" in html
    assert "auto_keep_candidate" in html
    assert "autoFilter" in html
    assert "Auto rejects" in html
    assert "audioBandFilter" in html
    assert "Preview mode" in html
    assert "ultrasonic" in html
    assert "Species audio" in html
    assert "audible_list_keep" in html


def test_prepare_view_rows_filters_species_and_sorts_for_review():
    rows = [
        qc_row(
            species_latin="Leptophyes punctatissima",
            recording_id="200",
            auto_qc="human_review",
            audio_band_tag="ultrasonic",
            dominant_freq_hz="22000.0000",
        ),
        qc_row(
            species_latin="Leptophyes punctatissima",
            recording_id="100",
            auto_qc="auto_keep_candidate",
            audio_band_tag="audible",
            dominant_freq_hz="7000.0000",
        ),
        qc_row(
            species_latin="Gryllus campestris",
            recording_id="300",
            auto_qc="auto_keep_candidate",
            audio_band_tag="ultrasonic",
            dominant_freq_hz="16000.0000",
        ),
    ]

    prepared = app.prepare_view_rows(rows, species="Leptophyes punctatissima")

    assert [row["recording_id"] for row in prepared] == ["100", "200"]
    assert all(row["species_latin"] == "Leptophyes punctatissima" for row in prepared)


def test_render_html_supports_default_preview_rate():
    html = app.render_html([qc_row()], title="Leptophyes QC", default_preview_rate="0.25")

    assert 'option value="0.25" selected' in html
