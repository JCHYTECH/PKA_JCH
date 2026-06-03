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
