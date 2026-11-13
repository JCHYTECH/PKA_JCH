# EventNET Noise Index Implementation Plan

> **For agentic workers:** REQUIRED SUB-[[SKILL]]: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Extend EventNET on the current BirdNET-Pi Raspberry Pi to compute a wildlife-oriented anthropogenic noise index from YAMNet detections.

**Architecture:** Keep the existing single EventNET service and YAMNet model. Add a target taxonomy with `weather` and `anthropic` groups, migrate SQLite safely, compute a 0-100 noise index over fixed time windows, and display it in the PHP dashboard.

**Tech Stack:** Python 3, SQLite, YAMNet TFLite, pytest, PHP/SQLite3, systemd service unchanged unless deployment threshold changes.

---

## Files

- Modify: `scripts/eventnet_detect.py`
  - Add grouped taxonomy.
  - Make TFLite import lazy enough that unit tests can import pure helpers without model dependencies.
  - Add SQLite migration for `event_group` and `noise_index`.
  - Log grouped events.
  - Add noise-index computation and `--rebuild-index`.
  - Extend `--stats`.
- Modify: `scripts/eventnet.php`
  - Display current anthropogenic noise index.
  - Split weather and anthropic summaries.
  - Show recent index windows and recent grouped events.
- Create: `tests/test_eventnet_noise_index.py`
  - Unit tests for taxonomy selection, score levels, index formula, SQLite migration, and index rebuild.
- Optional verify only: `scripts/eventnet.service`
  - Confirm the existing `--threshold 0.15` remains suitable. Do not change unless field testing requires it.

## Task 1: Make EventNET Importable and Add Taxonomy Helpers

**Files:**
- Modify: `scripts/eventnet_detect.py`
- Create: `tests/test_eventnet_noise_index.py`

- [ ] **Step 1: Write failing tests for taxonomy helpers**

Create `tests/test_eventnet_noise_index.py` with:

```python
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
```

- [ ] **Step 2: Run the test and confirm it fails**

Run:

```bash
python3 -m pytest tests/test_eventnet_noise_index.py::test_target_indices_include_weather_and_anthropic_labels -q
```

Expected: FAIL because `build_target_indices` does not exist, or import fails because TFLite exits at import time.

- [ ] **Step 3: Implement lazy TFLite import and taxonomy helpers**

In `scripts/eventnet_detect.py`, replace the top-level TFLite import block with:

```python
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
```

Then update `load_model` to use it:

```python
def load_model(path):
    interpreter_cls = get_interpreter_class()
    interpreter = interpreter_cls(model_path=str(path))
    interpreter.allocate_tensors()
    return interpreter
```

Add the grouped taxonomy near `WEATHER_CLASSES`:

```python
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
```

- [ ] **Step 4: Run the taxonomy test and confirm it passes**

Run:

```bash
python3 -m pytest tests/test_eventnet_noise_index.py::test_target_indices_include_weather_and_anthropic_labels -q
```

Expected: PASS.

- [ ] **Step 5: Commit Task 1**

```bash
git add scripts/eventnet_detect.py tests/test_eventnet_noise_index.py
git commit -m "Add EventNET grouped target taxonomy"
```

## Task 2: Migrate SQLite and Log Event Groups

**Files:**
- Modify: `scripts/eventnet_detect.py`
- Modify: `tests/test_eventnet_noise_index.py`

- [ ] **Step 1: Write failing tests for SQLite migration**

Append:

```python
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
```

- [ ] **Step 2: Run the test and confirm it fails**

Run:

```bash
python3 -m pytest tests/test_eventnet_noise_index.py::test_init_db_migrates_event_group_and_creates_noise_index -q
```

Expected: FAIL because `event_group` and `noise_index` are not created.

- [ ] **Step 3: Implement migration and grouped logging**

Replace `init_db` with logic that creates/migrates both tables:

```python
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
```

Change `log_event` signature and insert:

```python
def log_event(db_path, ts, cid, name_fr, name_en, score, src, dur, event_group):
    with sqlite3.connect(str(db_path)) as conn:
        conn.execute(
            """INSERT INTO events
               (timestamp, class_id, class_name_fr, class_name_en, score, source_file, duration_s, event_group)
               VALUES (?,?,?,?,?,?,?,?)""",
            (ts, cid, name_fr, name_en, round(score, 4), src, round(dur, 2), event_group),
        )
        conn.commit()
```

Update `process_file` to iterate `targets` instead of `weather_idx`:

```python
def process_file(wav_path, interpreter, targets):
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
            print(f"  -> {target['group']} / {target['name_fr']}: {score:.3f}", flush=True)
```

Update `main_loop` and `--once` branches to call:

```python
targets = build_target_indices(labels)
print(f"[EventNET] {len(targets)} target classes loaded", flush=True)
```

- [ ] **Step 4: Run migration tests**

Run:

```bash
python3 -m pytest tests/test_eventnet_noise_index.py -q
```

Expected: PASS for the tests added so far.

- [ ] **Step 5: Commit Task 2**

```bash
git add scripts/eventnet_detect.py tests/test_eventnet_noise_index.py
git commit -m "Migrate EventNET events for grouped logging"
```

## Task 3: Add Noise Index Computation

**Files:**
- Modify: `scripts/eventnet_detect.py`
- Modify: `tests/test_eventnet_noise_index.py`

- [ ] **Step 1: Write failing tests for score levels and window aggregation**

Append:

```python
def test_noise_level_boundaries():
    assert eventnet.noise_level(0) == "none"
    assert eventnet.noise_level(1) == "low"
    assert eventnet.noise_level(29) == "low"
    assert eventnet.noise_level(30) == "moderate"
    assert eventnet.noise_level(59) == "moderate"
    assert eventnet.noise_level(60) == "high"
    assert eventnet.noise_level(100) == "high"


def test_compute_noise_score_uses_max_score_and_recurrence():
    assert eventnet.compute_noise_score(0.0, 0) == 0
    assert eventnet.compute_noise_score(0.2, 1) == 19
    assert eventnet.compute_noise_score(0.8, 1) == 61
    assert eventnet.compute_noise_score(1.0, 20) == 100


def test_rebuild_noise_index_writes_expected_window(tmp_path):
    db_path = tmp_path / "events.db"
    eventnet.init_db(db_path)
    with sqlite3.connect(db_path) as conn:
        conn.executemany(
            """INSERT INTO events
               (timestamp, class_id, class_name_fr, class_name_en, score, source_file, duration_s, event_group)
               VALUES (?,?,?,?,?,?,?,?)""",
            [
                ("2026-06-03T10:00:01", "/m/air", "Avion", "Aircraft", 0.8, "a.wav", 3.0, "anthropic"),
                ("2026-06-03T10:05:00", "/m/dog", "Chien / aboiement", "Bark", 0.4, "b.wav", 3.0, "anthropic"),
                ("2026-06-03T10:06:00", "/m/rain", "Pluie", "Rain", 0.7, "c.wav", 3.0, "weather"),
            ],
        )
        conn.commit()

    written = eventnet.rebuild_noise_index(db_path, window_minutes=15)

    assert written == 1
    with sqlite3.connect(db_path) as conn:
        row = conn.execute(
            """SELECT window_start, window_end, anthropic_noise_score, anthropic_noise_level,
                      dominant_anthropic_source, anthropic_event_count, max_anthropic_score,
                      weather_event_count, sample_count
               FROM noise_index"""
        ).fetchone()

    assert row == (
        "2026-06-03T10:00:00",
        "2026-06-03T10:15:00",
        66.0,
        "high",
        "Avion",
        2,
        0.8,
        1,
        3,
    )
```

- [ ] **Step 2: Run the tests and confirm failure**

Run:

```bash
python3 -m pytest tests/test_eventnet_noise_index.py::test_noise_level_boundaries tests/test_eventnet_noise_index.py::test_compute_noise_score_uses_max_score_and_recurrence tests/test_eventnet_noise_index.py::test_rebuild_noise_index_writes_expected_window -q
```

Expected: FAIL because index helpers do not exist.

- [ ] **Step 3: Implement index helpers**

Add to `scripts/eventnet_detect.py`:

```python
from collections import Counter, defaultdict
from datetime import timedelta
```

Add helper functions:

```python
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
```

- [ ] **Step 4: Add CLI option**

In `main()`, add:

```python
parser.add_argument("--rebuild-index", action="store_true")
parser.add_argument("--index-window-minutes", type=int, default=15)
```

Before the `--once` branch, add:

```python
if args.rebuild_index:
    written = rebuild_noise_index(DB_PATH, args.index_window_minutes)
    print(f"Noise index windows written: {written}")
    return
```

- [ ] **Step 5: Run all EventNET tests**

Run:

```bash
python3 -m pytest tests/test_eventnet_noise_index.py -q
```

Expected: PASS.

- [ ] **Step 6: Commit Task 3**

```bash
git add scripts/eventnet_detect.py tests/test_eventnet_noise_index.py
git commit -m "Add EventNET anthropic noise index"
```

## Task 4: Rebuild Index After Each Processed WAV

**Files:**
- Modify: `scripts/eventnet_detect.py`
- Modify: `tests/test_eventnet_noise_index.py`

- [ ] **Step 1: Write failing test for process hook**

Append:

```python
def test_process_file_rebuilds_index_after_logging(monkeypatch, tmp_path):
    calls = []
    monkeypatch.setattr(eventnet, "DB_PATH", tmp_path / "events.db")
    monkeypatch.setattr(eventnet, "read_wav_mono_16k", lambda path: [0.1] * eventnet.TARGET_SR)
    monkeypatch.setattr(eventnet, "run_yamnet", lambda interpreter, audio: [0.9])
    monkeypatch.setattr(eventnet, "rebuild_noise_index", lambda db_path: calls.append(db_path) or 1)
    eventnet.init_db(eventnet.DB_PATH)

    targets = {
        0: {
            "mid": "/m/air",
            "name_fr": "Avion",
            "name_en": "Aircraft",
            "group": "anthropic",
        }
    }

    eventnet.process_file(Path("sample.wav"), object(), targets)

    assert calls == [eventnet.DB_PATH]
```

- [ ] **Step 2: Run and confirm failure**

Run:

```bash
python3 -m pytest tests/test_eventnet_noise_index.py::test_process_file_rebuilds_index_after_logging -q
```

Expected: FAIL because `process_file` does not call `rebuild_noise_index`.

- [ ] **Step 3: Update `process_file`**

Track whether at least one event was logged:

```python
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
```

Keep the rest of `process_file` unchanged from Task 2.

- [ ] **Step 4: Run tests**

Run:

```bash
python3 -m pytest tests/test_eventnet_noise_index.py -q
```

Expected: PASS.

- [ ] **Step 5: Commit Task 4**

```bash
git add scripts/eventnet_detect.py tests/test_eventnet_noise_index.py
git commit -m "Refresh EventNET noise index after detections"
```

## Task 5: Extend CLI Stats

**Files:**
- Modify: `scripts/eventnet_detect.py`

- [ ] **Step 1: Update `--stats` query**

Replace the existing stats output with two sections:

```python
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
```

- [ ] **Step 2: Run focused tests and smoke stats**

Run:

```bash
python3 -m pytest tests/test_eventnet_noise_index.py -q
python3 scripts/eventnet_detect.py --stats
```

Expected:
- Tests PASS.
- `--stats` prints grouped event stats or empty sections. If it fails locally because `/home/jchavaux/BirdNET-Pi/eventnet/events.db` does not exist, note that final smoke must be run on the RPi.

- [ ] **Step 3: Commit Task 5**

```bash
git add scripts/eventnet_detect.py
git commit -m "Show EventNET noise index in stats"
```

## Task 6: Update Dashboard

**Files:**
- Modify: `scripts/eventnet.php`

- [ ] **Step 1: Add CSS classes**

Add badge/card classes for anthropic and index levels:

```css
.section-title{font-size:1.05em;margin:20px 0 10px;color:#cbd5e1}
.badge.anthropic{background:#581c87;color:#e9d5ff}
.badge.weather{background:#164e63;color:#a5f3fc}
.level-none{color:#94a3b8}
.level-low{color:#bef264}
.level-moderate{color:#fde68a}
.level-high{color:#fca5a5}
```

- [ ] **Step 2: Query latest index and grouped summaries**

Replace the current `$stats` block with:

```php
$db = new SQLite3('/home/jchavaux/BirdNET-Pi/eventnet/events.db');

$latestIndex = $db->querySingle("SELECT window_start, window_end, anthropic_noise_score, anthropic_noise_level, dominant_anthropic_source, anthropic_event_count, max_anthropic_score FROM noise_index ORDER BY window_start DESC LIMIT 1", true);

$stats = $db->query("SELECT event_group, class_name_fr, COUNT(*) as cnt, ROUND(AVG(score),3) as avg, ROUND(MAX(score),3) as max FROM events GROUP BY event_group, class_name_fr ORDER BY event_group, cnt DESC");
$counts = ['weather' => [], 'anthropic' => []];
$total = 0;
while ($row = $stats->fetchArray(SQLITE3_ASSOC)) {
    $group = $row['event_group'] ?: 'weather';
    if (!isset($counts[$group])) $counts[$group] = [];
    $counts[$group][$row['class_name_fr']] = $row;
    $total += $row['cnt'];
}
```

- [ ] **Step 3: Render index card**

After the subtitle, add:

```php
<?php if ($latestIndex): ?>
<div class="card">
<div class="label">Indice pollution sonore anthropique</div>
<div class="count level-<?= htmlspecialchars($latestIndex['anthropic_noise_level']) ?>"><?= number_format($latestIndex['anthropic_noise_score'], 0) ?></div>
<div class="label"><?= htmlspecialchars($latestIndex['anthropic_noise_level']) ?> — <?= htmlspecialchars($latestIndex['dominant_anthropic_source'] ?? 'aucune source dominante') ?></div>
<div class="max">fenetre: <?= htmlspecialchars($latestIndex['window_start']) ?> → <?= htmlspecialchars($latestIndex['window_end']) ?> · evenements: <?= intval($latestIndex['anthropic_event_count']) ?></div>
</div>
<?php else: ?>
<div class="card"><div class="label">Indice pollution sonore anthropique</div><div class="count level-none">0</div><div class="label">en attente de donnees</div></div>
<?php endif; ?>
```

- [ ] **Step 4: Render grouped cards**

Render weather and anthropic sections separately:

```php
<?php foreach (['weather' => 'Meteo acoustique', 'anthropic' => 'Bruit anthropique'] as $group => $title): ?>
<h2 class="section-title"><?= $title ?></h2>
<div class="grid">
<?php foreach (($counts[$group] ?? []) as $name => $row): ?>
<div class="card">
<div class="count"><?= $row['cnt'] ?></div>
<div class="label"><?= htmlspecialchars($name) ?></div>
<div class="max">max: <?= $row['max'] ?></div>
</div>
<?php endforeach; ?>
<?php if (empty($counts[$group])): ?>
<div class="card"><div class="count">0</div><div class="label">Aucun evenement</div></div>
<?php endif; ?>
</div>
<?php endforeach; ?>
```

- [ ] **Step 5: Update latest event table**

Change latest query to include `event_group`:

```php
$latest = $db->query("SELECT timestamp, event_group, class_name_fr, score FROM events ORDER BY id DESC LIMIT 30");
```

Render group badge:

```php
<td><span class="badge <?= htmlspecialchars($r['event_group'] ?: 'weather') ?>"><?= htmlspecialchars($r['event_group'] ?: 'weather') ?></span></td>
<td><?= htmlspecialchars($r['class_name_fr']) ?></td>
```

Update header to:

```html
<tr><th>Heure</th><th>Groupe</th><th>Evenement</th><th>Score</th></tr>
```

- [ ] **Step 6: PHP syntax check**

Run:

```bash
php -l scripts/eventnet.php
```

Expected: `No syntax errors detected in scripts/eventnet.php`.

- [ ] **Step 7: Commit Task 6**

```bash
git add scripts/eventnet.php
git commit -m "Display EventNET anthropic noise index"
```

## Task 7: Local Verification and RPi Deployment Notes

**Files:**
- Modify: `wiki/Daily/2026/06/2026-06-03-eventnet-noise-index.md`

- [ ] **Step 1: Run tests**

Run:

```bash
python3 -m pytest tests/test_eventnet_noise_index.py -q
php -l scripts/eventnet.php
```

Expected:
- EventNET tests PASS.
- PHP syntax check PASS.

- [ ] **Step 2: Create [[daily]] note**

Create `wiki/Daily/2026/06/2026-06-03-eventnet-noise-index.md`:

```markdown
---
date: 2026-06-03
tags: [daily, WILDNEXUS, EventNET, bioacoustics]
type: daily
status: active
---

# 2026-06-03 — EventNET noise index

## Session

### Contexte
- Projet : [[WildNexus]] / [[EventNET]]
- Objectif : transformer la detection de bruit anthropique en indice de pollution sonore wildlife sur le [[Raspberry Pi]] BirdNET-Pi.

### Actions
- Ajout taxonomie YAMNet groupee `weather` / `anthropic`.
- Ajout migration SQLite `event_group` et table `noise_index`.
- Ajout indice 0-100 par fenetre de 15 minutes.
- Dashboard PHP enrichi avec indice courant et groupes.

### Decisions
- L'indice est un proxy non calibre, pas une mesure dB SPL ou LAeq.
- L'ESP32 / Satellite Lite P0 n'est pas modifie.
- Les detections BirdNET ne sont pas invalidees automatiquement en V1.

### Verification
- `python3 -m pytest tests/test_eventnet_noise_index.py -q`
- `php -l scripts/eventnet.php`

## Voir aussi

- [[WILDNEXUS_P0_SCOPE_LOCK]]
- [[ADR-007-detection-evenementielle-p0]]
- [[2026-05-30-session-deepseek-eventnet-wildnexus]]
```

- [ ] **Step 3: Commit Task 7**

```bash
git add wiki/Daily/2026/06/2026-06-03-eventnet-noise-index.md
git commit -m "Document EventNET noise index update"
```

- [ ] **Step 4: Prepare RPi deployment commands for [[Dobby]] execution**

Use these only after local tests pass:

```bash
scp scripts/eventnet_detect.py scripts/eventnet.php jchavaux@100.84.45.93:/tmp/
ssh jchavaux@100.84.45.93 'sudo cp /tmp/eventnet_detect.py /home/jchavaux/BirdNET-Pi/eventnet/eventnet_detect.py && sudo cp /tmp/eventnet.php /var/www/html/eventnet.php && sudo systemctl restart eventnet.service && /home/jchavaux/BirdNET-Pi/birdnet/bin/python3 /home/jchavaux/BirdNET-Pi/eventnet/eventnet_detect.py --rebuild-index --threshold 0.15 && systemctl status eventnet.service --no-pager'
```

Expected:
- Service restarts.
- `Noise index windows written: N`.
- `systemctl status` shows active/running.

## Final Verification

- [ ] `python3 -m pytest tests/test_eventnet_noise_index.py -q` passes locally.
- [ ] `php -l scripts/eventnet.php` passes locally.
- [ ] `git log --oneline -5` shows the implementation commits.
- [ ] RPi deployment succeeds or is explicitly deferred.
- [ ] Dashboard loads over Tailscale and shows the current index, even if the index is `0 / none`.
