#!/usr/bin/env python3
"""Lightweight PreToolUse guidance for Claude-local PKA sessions.

This script stays quiet most of the time. It emits a reminder only at
strategic intervals so Dobby gets gentle pressure toward compaction and
system hygiene without adding noise to every edit.
"""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = ROOT / "scripts" / ".pretool_guidance_state.json"
INITIAL_THRESHOLD = 50
REMINDER_INTERVAL = 25


def load_state() -> dict:
    if STATE_PATH.is_file():
        try:
            return json.loads(STATE_PATH.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def save_state(state: dict) -> None:
    STATE_PATH.write_text(json.dumps(state, indent=2), encoding="utf-8")


def next_message(count: int) -> str | None:
    if count < INITIAL_THRESHOLD:
        return None
    if count == INITIAL_THRESHOLD or (count - INITIAL_THRESHOLD) % REMINDER_INTERVAL == 0:
        return (
            "PKA guidance — point de contrôle utile: si tu changes de phase "
            "(recherche -> implémentation, debug -> suite, milestone terminé), "
            "pense à compacter le contexte ou à capturer la procédure avant de continuer."
        )
    return None


def main() -> int:
    state = load_state()
    count = int(state.get("count", 0)) + 1
    state["count"] = count
    save_state(state)

    message = next_message(count)
    if message:
        print(json.dumps({"systemMessage": message}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
