from scripts import insectnet_segment_qc as qc


def segment_row(**overrides):
    row = {
        "species_latin": "Tettigonia viridissima",
        "recording_id": "969762",
        "target_path": "/tmp/segments/tettigonia.wav",
        "segment_index": "3",
        "start_s": "9.000",
        "duration_s": "3.000",
        "status": "created",
    }
    row.update(overrides)
    return row


def spectrogram_row(**overrides):
    row = {
        "species_latin": "Tettigonia viridissima",
        "recording_id": "969762",
        "segment_index": "3",
        "segment_path": "/tmp/segments/tettigonia.wav",
        "spectrogram_path": "/tmp/spectrograms/tettigonia.png",
        "status": "created",
    }
    row.update(overrides)
    return row


def test_segment_key_uses_recording_id_segment_index_and_path():
    row = segment_row()

    assert qc.segment_key(row) == (
        "969762",
        "3",
        "/tmp/segments/tettigonia.wav",
    )


def test_default_visual_qc_is_review_not_keep():
    assert qc.default_visual_qc("Gryllus campestris") == "review"
    assert qc.default_visual_qc("Leptophyes punctatissima") == "review"


def test_build_qc_rows_joins_spectrogram_paths():
    rows = qc.build_qc_rows([segment_row()], [spectrogram_row()])

    assert len(rows) == 1
    row = rows[0]
    assert row["visual_qc"] == "review"
    assert row["qc_reason"] == "unreviewed"
    assert row["spectrogram_path"] == "/tmp/spectrograms/tettigonia.png"
    assert row["species_latin"] == "Tettigonia viridissima"


def test_build_qc_rows_marks_missing_spectrogram_for_review():
    rows = qc.build_qc_rows([segment_row()], [])

    assert rows[0]["spectrogram_path"] == ""
    assert rows[0]["visual_qc"] == "review"
    assert rows[0]["qc_reason"] == "missing_spectrogram"
