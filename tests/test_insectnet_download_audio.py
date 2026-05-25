from pathlib import Path

from scripts import insectnet_download_audio as dl


def test_slug_normalizes_species_name():
    assert dl.slug("Tettigonia viridissima") == "tettigonia-viridissima"
    assert dl.slug(" Roeseliana / roeselii ") == "roeseliana-roeselii"


def test_safe_filename_prefixes_recording_id_when_needed():
    row = {"recording_id": "123", "file_name": "clean.wav"}
    assert dl.safe_filename(row) == "XC123-clean.wav"


def test_target_path_groups_by_species():
    row = {
        "species_latin": "Gryllus campestris",
        "recording_id": "456",
        "file_name": "XC456.wav",
    }

    path = dl.target_path(row, Path("/tmp/audio"))

    assert path == Path("/tmp/audio/gryllus-campestris/XC456.wav")


def test_dry_run_writes_log_without_downloading(tmp_path):
    manifest = tmp_path / "manifest.csv"
    manifest.write_text(
        "species_latin,recording_id,source_url,download_url,file_name\n"
        "Tettigonia viridissima,1,https://xeno-canto.org/1,https://example.test/1,one.wav\n",
        encoding="utf-8",
    )

    log_rows = dl.download_manifest(
        manifest,
        tmp_path / "audio",
        tmp_path / "download-log.csv",
        limit=None,
        overwrite=False,
        dry_run=True,
    )

    assert log_rows[0]["status"] == "dry-run"
    assert (tmp_path / "download-log.csv").exists()
    assert not (tmp_path / "audio").exists()
