#!/usr/bin/env python3
"""
eventnet_detect.py — EventNET: détection acoustique d'événements météo
via YAMNet (AudioSet) en parallèle de BirdNET-Pi.

Surveille les fichiers WAV produits par BirdNET dans StreamData/,
passe chaque segment dans YAMNet TFLite, et loggue les événements
météo (pluie, orage, vent) dans events.db.
"""

from __future__ import annotations

import argparse
import csv
import os
import sqlite3
import sys
import time
import wave
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np

Interpreter = None


def get_interpreter_class():
    global Interpreter
    if Interpreter is not None:
        return Interpreter
    try:
        from tflite_runtime.interpreter import Interpreter as RuntimeInterpreter
    except ImportError:
        try:
            from tensorflow.lite.python.interpreter import Interpreter as RuntimeInterpreter
        except ImportError as exc:
            raise RuntimeError("tflite_runtime or tensorflow.lite is required for YAMNet inference") from exc
    Interpreter = RuntimeInterpreter
    return Interpreter

BASE_DIR = Path("/home/jchavaux/BirdNET-Pi")
EVENTNET_DIR = BASE_DIR / "eventnet"
MODEL_PATH = EVENTNET_DIR / "yamnet.tflite"
LABELS_PATH = EVENTNET_DIR / "yamnet_class_map.csv"
STREAM_DIR = Path("/home/jchavaux/BirdSongs/StreamData")
DB_PATH = EVENTNET_DIR / "events.db"
PROCESSED_LOG = EVENTNET_DIR / "processed_files.txt"
POLL_INTERVAL = 5
TARGET_SR = 16000
SCORE_THRESHOLD = 0.25

WEATHER_CLASSES = {
    "/m/0ngt1": "Tonnerre",
    "/m/0jbk": "Orage",
    "/m/06mb1": "Pluie",
    "/t/dd00129": "Pluie (surface)",
    "/m/03m9d0h": "Vent",
    "/m/0cj0r": "Vent (micro)",
}

ANTHROPIC_LABELS = {
    "aircraft": "Avion",
    "aeroplane": "Avion",
    "airplane": "Avion",
    "jet engine": "Avion",
    "motor vehicle (road)": "Voiture / moteur",
    "car": "Voiture / moteur",
    "engine": "Voiture / moteur",
    "engine idling": "Voiture / moteur",
    "human voice": "Voix humaine",
    "speech": "Voix humaine",
    "conversation": "Voix humaine",
    "shout": "Voix humaine",
    "shouting": "Voix humaine",
    "dog": "Chien / aboiement",
    "bark": "Chien / aboiement",
    "chainsaw": "Tronconneuse",
}


def normalize_label(label):
    return label.strip().lower()


def build_target_indices(labels):
    targets = {}
    for idx, (mid, display_name) in labels.items():
        if mid in WEATHER_CLASSES:
            targets[idx] = {
                "mid": mid,
                "name_fr": WEATHER_CLASSES[mid],
                "name_en": display_name,
                "group": "weather",
            }
            continue

        normalized = normalize_label(display_name)
        if normalized in ANTHROPIC_LABELS:
            targets[idx] = {
                "mid": mid,
                "name_fr": ANTHROPIC_LABELS[normalized],
                "name_en": display_name,
                "group": "anthropic",
            }
    return targets


def load_labels(path):
    labels = {}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            labels[int(row["index"])] = (row["mid"], row["display_name"])
    return labels


def load_model(path):
    interpreter_cls = get_interpreter_class()
    interpreter = interpreter_cls(model_path=str(path))
    interpreter.allocate_tensors()
    return interpreter


def read_wav_mono_16k(path):
    try:
        with wave.open(str(path), "rb") as wf:
            nch = wf.getnchannels()
            sw = wf.getsampwidth()
            sr = wf.getframerate()
            raw = wf.readframes(wf.getnframes())
    except Exception:
        return None

    dtype_map = {2: np.int16, 4: np.int32}
    if sw not in dtype_map:
        return None
    audio = np.frombuffer(raw, dtype=dtype_map[sw]).astype(np.float32)
    if nch > 1:
        audio = audio.reshape(-1, nch).mean(axis=1)
    audio /= float(np.iinfo(dtype_map[sw]).max)
    if sr != TARGET_SR:
        ratio = TARGET_SR / sr
        new_len = int(len(audio) * ratio)
        audio = np.interp(np.linspace(0, len(audio) - 1, new_len), np.arange(len(audio)), audio).astype(np.float32)
    return audio


YAMNET_INPUT_SIZE = 15600  # échantillons à 16kHz (~0.975s)


def run_yamnet(interpreter, audio):
    """Exécute YAMNet par chunks de YAMNET_INPUT_SIZE avec 50% de chevauchement.
    Retourne les scores moyens sur l'ensemble du segment."""
    inp = interpreter.get_input_details()
    out = interpreter.get_output_details()

    step = YAMNET_INPUT_SIZE // 2
    all_scores = []

    for start in range(0, len(audio) - YAMNET_INPUT_SIZE + 1, step):
        chunk = audio[start:start + YAMNET_INPUT_SIZE].astype(np.float32)
        interpreter.set_tensor(inp[0]["index"], chunk)
        interpreter.invoke()
        scores = interpreter.get_tensor(out[0]["index"])  # [1, 521]
        all_scores.append(scores[0])

    if not all_scores:
        return np.zeros(521, dtype=np.float32)
    return np.array(all_scores).mean(axis=0)


def ensure_column(conn, table, column, definition):
    columns = {row[1] for row in conn.execute(f"PRAGMA table_info({table})")}
    if column not in columns:
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")


def init_db(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(str(path)) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            class_id TEXT NOT NULL,
            class_name_fr TEXT NOT NULL,
            class_name_en TEXT NOT NULL,
            score REAL NOT NULL,
            source_file TEXT,
            duration_s REAL,
            event_group TEXT NOT NULL DEFAULT 'weather')""")
        ensure_column(conn, "events", "event_group", "TEXT NOT NULL DEFAULT 'weather'")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_events_ts ON events(timestamp)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_events_group_ts ON events(event_group, timestamp)")
        conn.execute("""CREATE TABLE IF NOT EXISTS noise_index (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            window_start TEXT NOT NULL,
            window_end TEXT NOT NULL,
            anthropic_noise_score REAL NOT NULL,
            anthropic_noise_level TEXT NOT NULL,
            dominant_anthropic_source TEXT,
            anthropic_event_count INTEGER NOT NULL,
            max_anthropic_score REAL NOT NULL,
            weather_event_count INTEGER NOT NULL,
            sample_count INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            UNIQUE(window_start, window_end))""")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_noise_index_window ON noise_index(window_start, window_end)")
        conn.commit()


def log_event(db_path, ts, cid, name_fr, name_en, score, src, dur, event_group):
    with sqlite3.connect(str(db_path)) as conn:
        conn.execute(
            """INSERT INTO events
               (timestamp, class_id, class_name_fr, class_name_en, score, source_file, duration_s, event_group)
               VALUES (?,?,?,?,?,?,?,?)""",
            (ts, cid, name_fr, name_en, round(score, 4), src, round(dur, 2), event_group),
        )
        conn.commit()


def parse_event_time(value):
    return datetime.fromisoformat(value)


def floor_time(dt, window_minutes):
    discard = timedelta(
        minutes=dt.minute % window_minutes,
        seconds=dt.second,
        microseconds=dt.microsecond,
    )
    return dt - discard


def compute_noise_score(max_anthropic_score, anthropic_event_count):
    if anthropic_event_count <= 0 or max_anthropic_score <= 0:
        return 0
    raw = (max_anthropic_score * 70) + min(anthropic_event_count, 6) * 5
    return min(100, round(raw))


def noise_level(score):
    if score <= 0:
        return "none"
    if score < 30:
        return "low"
    if score < 60:
        return "moderate"
    return "high"


def rebuild_noise_index(db_path, window_minutes=15):
    init_db(db_path)
    windows = defaultdict(list)
    with sqlite3.connect(str(db_path)) as conn:
        rows = conn.execute(
            """SELECT timestamp, class_name_fr, score, event_group
               FROM events
               ORDER BY timestamp"""
        ).fetchall()

        for timestamp, class_name_fr, score, event_group in rows:
            start = floor_time(parse_event_time(timestamp), window_minutes)
            windows[start].append(
                {
                    "class_name_fr": class_name_fr,
                    "score": float(score),
                    "event_group": event_group,
                }
            )

        now = datetime.now().isoformat(timespec="seconds")
        written = 0
        for start, events in sorted(windows.items()):
            end = start + timedelta(minutes=window_minutes)
            anthropic = [event for event in events if event["event_group"] == "anthropic"]
            weather = [event for event in events if event["event_group"] == "weather"]
            max_score = max((event["score"] for event in anthropic), default=0.0)
            count = len(anthropic)
            score = float(compute_noise_score(max_score, count))
            level = noise_level(score)
            dominant = None
            if anthropic:
                by_name = Counter(event["class_name_fr"] for event in anthropic)
                dominant = by_name.most_common(1)[0][0]
            conn.execute(
                """INSERT OR REPLACE INTO noise_index
                   (window_start, window_end, anthropic_noise_score, anthropic_noise_level,
                    dominant_anthropic_source, anthropic_event_count, max_anthropic_score,
                    weather_event_count, sample_count, created_at)
                   VALUES (?,?,?,?,?,?,?,?,?,?)""",
                (
                    start.isoformat(timespec="seconds"),
                    end.isoformat(timespec="seconds"),
                    score,
                    level,
                    dominant,
                    count,
                    round(max_score, 4),
                    len(weather),
                    len(events),
                    now,
                ),
            )
            written += 1
        conn.commit()
        return written


def load_processed(path):
    if not path.exists():
        return set()
    return set(path.read_text(encoding="utf-8").strip().splitlines())


def mark_processed(path, name):
    with open(path, "a", encoding="utf-8") as f:
        f.write(name + "\n")


def process_file(wav_path, interpreter, targets):
    """Analyse un fichier WAV et loggue les événements cibles."""
    print(f"[EventNET] {wav_path.name}", flush=True)
    audio = read_wav_mono_16k(wav_path)
    if audio is None or len(audio) < TARGET_SR:
        return

    try:
        scores = run_yamnet(interpreter, audio)
    except Exception as e:
        print(f"  Inference error: {e}", file=sys.stderr)
        return

    dur = len(audio) / TARGET_SR
    ts = datetime.now().isoformat(timespec="seconds")

    logged_any = False
    for idx, target in targets.items():
        score = float(scores[idx])
        if score >= SCORE_THRESHOLD:
            log_event(
                DB_PATH,
                ts,
                target["mid"],
                target["name_fr"],
                target["name_en"],
                score,
                wav_path.name,
                dur,
                target["group"],
            )
            logged_any = True
            print(f"  -> {target['group']} / {target['name_fr']}: {score:.3f}", flush=True)

    if logged_any:
        rebuild_noise_index(DB_PATH)


def main_loop():
    """Surveille StreamData/ via inotifywait pour capture immédiate des WAV."""
    import subprocess

    print("[EventNET] Loading model...", flush=True)
    labels = load_labels(LABELS_PATH)
    interpreter = load_model(MODEL_PATH)
    init_db(DB_PATH)

    targets = build_target_indices(labels)

    print(f"[EventNET] {len(targets)} target classes loaded", flush=True)
    print(f"[EventNET] Watching {STREAM_DIR}", flush=True)

    cmd = [
        "inotifywait", "-m", "-e", "close_write",
        "--format", "%f", str(STREAM_DIR),
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)

    try:
        for line in proc.stdout:
            fname = line.strip()
            if not fname.endswith(".wav"):
                continue
            wav_path = STREAM_DIR / fname
            if wav_path.exists():
                process_file(wav_path, interpreter, targets)
    except KeyboardInterrupt:
        pass
    finally:
        proc.terminate()
        proc.wait()


def main():
    parser = argparse.ArgumentParser(description="EventNET")
    parser.add_argument("--once", help="Analyze single WAV file")
    parser.add_argument("--threshold", type=float, default=0.25)
    parser.add_argument("--stats", action="store_true")
    parser.add_argument("--rebuild-index", action="store_true")
    parser.add_argument("--index-window-minutes", type=int, default=15)
    args = parser.parse_args()

    global SCORE_THRESHOLD
    SCORE_THRESHOLD = args.threshold

    if args.rebuild_index:
        written = rebuild_noise_index(DB_PATH, args.index_window_minutes)
        print(f"Noise index windows written: {written}")
        return

    if args.once:
        labels = load_labels(LABELS_PATH)
        interpreter = load_model(MODEL_PATH)
        init_db(DB_PATH)
        targets = build_target_indices(labels)
        process_file(Path(args.once), interpreter, targets)
        return

    if args.stats:
        init_db(DB_PATH)
        with sqlite3.connect(str(DB_PATH)) as conn:
            print("Events by group")
            print("===============")
            rows = conn.execute(
                """SELECT event_group, class_name_fr, COUNT(*), ROUND(AVG(score),3), MAX(score)
                   FROM events
                   GROUP BY event_group, class_name_fr
                   ORDER BY event_group, COUNT(*) DESC"""
            ).fetchall()
            for event_group, class_name_fr, count, avg_score, max_score in rows:
                print(f"{event_group:<10s} {class_name_fr:<24s} {count:>6d} {avg_score:>8.3f} {max_score:>8.3f}")

            print("\nRecent noise index")
            print("==================")
            rows = conn.execute(
                """SELECT window_start, anthropic_noise_score, anthropic_noise_level,
                          dominant_anthropic_source, anthropic_event_count
                   FROM noise_index
                   ORDER BY window_start DESC
                   LIMIT 10"""
            ).fetchall()
            for window_start, score, level, dominant, count in rows:
                print(f"{window_start} {score:>5.1f} {level:<8s} {dominant or '-':<24s} events={count}")

            total = conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]
            print(f"\nTotal: {total}")
        return

    main_loop()


if __name__ == "__main__":
    main()
