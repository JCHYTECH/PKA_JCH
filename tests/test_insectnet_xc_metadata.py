from scripts import insectnet_xc_metadata as xc


def test_map_recording_derives_training_flags_for_open_clean_recording():
    row = xc.map_recording(
        {
            "id": "1060773",
            "gen": "Tettigonia",
            "sp": "viridissima",
            "en": "Great Green Bush-cricket",
            "grp": "grasshoppers",
            "cnt": "France",
            "loc": "Montcenis",
            "lat": "46.8042",
            "lon": "4.3926",
            "alt": "500",
            "date": "2025-07-02",
            "time": "22:00",
            "uploaded": "2025-11-30",
            "rec": "Lionel Triboulin",
            "lic": "https://creativecommons.org/publicdomain/zero/1.0/",
            "q": "A",
            "type": "calling song",
            "method": "field recording",
            "animal-seen": "yes",
            "playback-used": "no",
            "temp": None,
            "dvc": "ZOOM H5",
            "mic": "Dodotronic",
            "smp": "44100",
            "length": "0:15",
            "url": "https://xeno-canto.org/1060773",
            "file": "https://xeno-canto.org/1060773/download",
            "file-name": "XC1060773.wav",
            "rmk": "",
        }
    )

    assert row["recording_id"] == "1060773"
    assert row["species_latin"] == "Tettigonia viridissima"
    assert row["latitude"] == 46.8042
    assert row["altitude_m"] == 500
    assert row["sample_rate_hz"] == 44100
    assert row["duration_s"] == 15.0
    assert row["license_class"] == "open"
    assert row["quality_flag"] == "ok"
    assert row["usable_for_training"] == "yes"
    assert row["usable_for_public_release"] == "yes"


def test_map_recording_marks_playback_or_no_derivatives_for_review():
    row = xc.map_recording(
        {
            "id": "1086751",
            "gen": "Tettigonia",
            "sp": "viridissima",
            "lic": "https://creativecommons.org/licenses/by-nc-nd/4.0/",
            "q": "A",
            "playback-used": "yes",
            "file": "https://xeno-canto.org/1086751/download",
            "length": "3:01",
        }
    )

    assert row["duration_s"] == 181.0
    assert row["license_class"] == "no_derivatives"
    assert row["quality_flag"] == "review"
    assert row["usable_for_training"] == "no"
    assert row["usable_for_public_release"] == "no"


def test_build_url_encodes_tagged_query_without_leaking_key_structure():
    url = xc.build_url("gen:Tettigonia sp:viridissima", "secret", page=2, per_page=50)

    assert url.startswith("https://xeno-canto.org/api/3/recordings?")
    assert "query=gen%3ATettigonia+sp%3Aviridissima" in url
    assert "key=secret" in url
    assert "page=2" in url
    assert "per_page=50" in url
