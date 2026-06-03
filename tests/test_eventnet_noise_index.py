import sqlite3
from pathlib import Path

import pytest

from scripts import eventnet_detect as eventnet


def test_target_indices_include_weather_and_anthropic_labels():
    labels = {
        0: ("/m/06mb1", "Rain"),
        1: ("/m/test_aircraft", "Aircraft"),
        2: ("/m/test_speech", "Speech"),
        3: ("/m/test_chainsaw", "Chainsaw"),
        4: ("/m/irrelevant", "Violin"),
    }

    targets = eventnet.build_target_indices(labels)

    assert targets[0]["group"] == "weather"
    assert targets[0]["name_fr"] == "Pluie"
    assert targets[1]["group"] == "anthropic"
    assert targets[1]["name_fr"] == "Avion"
    assert targets[2]["name_fr"] == "Voix humaine"
    assert targets[3]["name_fr"] == "Tronconneuse"
    assert 4 not in targets


def columns_for(conn, table):
    return {row[1] for row in conn.execute(f"PRAGMA table_info({table})").fetchall()}


def test_init_db_migrates_event_group_and_creates_noise_index(tmp_path):
    db_path = tmp_path / "events.db"
    with sqlite3.connect(db_path) as conn:
        conn.execute("""CREATE TABLE events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            class_id TEXT NOT NULL,
            class_name_fr TEXT NOT NULL,
            class_name_en TEXT NOT NULL,
            score REAL NOT NULL,
            source_file TEXT,
            duration_s REAL)""")
        conn.execute(
            "INSERT INTO events VALUES (NULL,?,?,?,?,?,?,?)",
            ("2026-06-03T10:00:00", "/m/06mb1", "Pluie", "Rain", 0.4, "a.wav", 3.0),
        )

    eventnet.init_db(db_path)

    with sqlite3.connect(db_path) as conn:
        assert "event_group" in columns_for(conn, "events")
        assert "noise_index" in {
            row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        }
        row = conn.execute("SELECT event_group FROM events").fetchone()
        assert row[0] == "weather"
