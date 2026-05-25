from scripts import insectnet_grouped_split as split


def qc_row(species, recording_id, segment_index, visual_qc="review"):
    return {
        "species_latin": species,
        "recording_id": recording_id,
        "segment_index": str(segment_index),
        "segment_path": f"/tmp/{species}/{recording_id}-{segment_index}.wav",
        "spectrogram_path": f"/tmp/{species}/{recording_id}-{segment_index}.png",
        "visual_qc": visual_qc,
        "qc_reason": "unreviewed",
    }


def test_group_rows_by_species_and_recording_id():
    grouped = split.group_rows(
        [
            qc_row("A", "r1", 0),
            qc_row("A", "r1", 1),
            qc_row("A", "r2", 0),
            qc_row("B", "r3", 0),
        ]
    )

    assert len(grouped["A"]["r1"]) == 2
    assert len(grouped["A"]["r2"]) == 1
    assert len(grouped["B"]["r3"]) == 1


def test_assign_recordings_keeps_groups_intact():
    assignments = split.assign_recordings(["r1", "r2", "r3", "r4"], test_fraction=0.25)

    assert set(assignments) == {"r1", "r2", "r3", "r4"}
    assert list(assignments.values()).count("test") == 1
    assert list(assignments.values()).count("train") == 3


def test_build_split_rows_does_not_split_recording_ids():
    rows = [
        qc_row("A", "r1", 0),
        qc_row("A", "r1", 1),
        qc_row("A", "r2", 0),
        qc_row("A", "r3", 0),
        qc_row("A", "r4", 0),
    ]

    output = split.build_split_rows(rows, test_fraction=0.25)

    by_recording = {}
    for row in output:
        by_recording.setdefault(row["recording_id"], set()).add(row["split"])
    assert all(len(splits) == 1 for splits in by_recording.values())
    assert {row["split"] for row in output} == {"train", "test"}


def test_build_split_rows_filters_rejected_segments():
    rows = [
        qc_row("A", "r1", 0, visual_qc="reject"),
        qc_row("A", "r2", 0, visual_qc="review"),
    ]

    output = split.build_split_rows(rows, test_fraction=0.5)

    assert len(output) == 1
    assert output[0]["recording_id"] == "r2"


def test_build_split_rows_targets_segment_balance_not_last_recording_ids():
    rows = []
    rows.extend(qc_row("A", "big", i) for i in range(23))
    rows.extend(qc_row("A", "small1", i) for i in range(2))
    rows.extend(qc_row("A", "small2", i) for i in range(2))
    rows.extend(qc_row("A", "small3", i) for i in range(2))
    rows.extend(qc_row("A", "small4", i) for i in range(2))

    output = split.build_split_rows(rows, test_fraction=0.2)

    test_count = sum(1 for row in output if row["split"] == "test")
    assert test_count == 6
    assert all(
        row["split"] == "train" for row in output if row["recording_id"] == "big"
    )
