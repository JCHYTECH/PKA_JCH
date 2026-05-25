from pathlib import Path

from PIL import Image

from scripts import insectnet_contact_sheets as sheets


def spectrogram_row(**overrides):
    row = {
        "species_latin": "Roeseliana roeselii",
        "recording_id": "850126",
        "segment_index": "0",
        "spectrogram_path": "/tmp/spectrograms/roeseliana-roeselii/example.png",
        "status": "created",
    }
    row.update(overrides)
    return row


def test_group_created_rows_by_species_skips_errors():
    grouped = sheets.group_rows_by_species(
        [
            spectrogram_row(),
            spectrogram_row(status="error"),
            spectrogram_row(species_latin="Gryllus campestris"),
        ]
    )

    assert sorted(grouped) == ["Gryllus campestris", "Roeseliana roeselii"]
    assert len(grouped["Roeseliana roeselii"]) == 1


def test_contact_sheet_path_uses_species_slug():
    path = sheets.contact_sheet_path("Roeseliana roeselii", Path("/tmp/sheets"))

    assert path == Path("/tmp/sheets/roeseliana-roeselii-contact-sheet.png")


def test_create_contact_sheet_writes_png(tmp_path):
    image_path = tmp_path / "one.png"
    Image.new("RGB", (32, 16), color=(10, 20, 30)).save(image_path)

    output = tmp_path / "sheet.png"
    sheets.create_contact_sheet(
        [spectrogram_row(spectrogram_path=str(image_path))],
        output,
        columns=2,
        thumb_width=64,
        label_height=16,
        max_images=4,
    )

    assert output.exists()
    with Image.open(output) as image:
        assert image.size == (128, 48)
