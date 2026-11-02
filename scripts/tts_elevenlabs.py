#!/usr/bin/env python3
"""
tts_elevenlabs.py — Synthèse vocale ElevenLabs (voix off WildLens, qualité documentaire).

Modèle multilingue (FR supporté) + paramètre de débit natif (pas besoin de ffmpeg).

Usage :
  python3 scripts/tts_elevenlabs.py --list                          # lister les voix
  python3 scripts/tts_elevenlabs.py --text "..." --voice <id> --out f.wav --speed 0.9

Clé : ELEVENLABS_API_KEY (env) ou ~/.config/pka-jch/elevenlabs_api_key.txt
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import requests

API = "https://api.elevenlabs.io/v1"
MODEL = "eleven_multilingual_v2"  # FR ok ; autres : eleven_flash_v2_5, eleven_v3

# Quelques voix préenregistrées utiles (masculines chaudes)
PRESETS = {
    "Antoni": "ErXwobaYiN019PkySvjV",
    "Adam": "pNInz6obpgDQGcFmaLgI",
    "Domi": "AZnzlk1XvdvUeBnXmlld",
    "Josh": "TxGEqnHWrfWFTfGW9XjX",
    "Rachel": "21m00Tcm4TlvDq8ikWAM",
    "Bella": "EXAVITQu4vr4xnSDxMaL",
}


def load_key() -> str:
    env = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if env:
        return env
    f = Path("~/.config/pka-jch/elevenlabs_api_key.txt").expanduser()
    if f.exists():
        val = f.read_text(encoding="utf-8").strip()
        if val:
            return val
    raise RuntimeError("ELEVENLABS_API_KEY introuvable")


def _headers() -> dict:
    return {"xi-api-key": load_key(), "Content-Type": "application/json"}


def list_voices() -> None:
    r = requests.get(f"{API}/voices", headers=_headers(), timeout=30)
    r.raise_for_status()
    for v in r.json().get("voices", []):
        print(f"{v['name']:30} {v['voice_id']}")


def synth(text: str, voice_id: str, out: Path, speed: float = 0.9,
          stability: float = 0.55, similarity: float = 0.75) -> bool:
    data = {
        "text": text,
        "model_id": MODEL,
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity,
            "style": 0.0,
            "use_speaker_boost": True,
            "speed": speed,
        },
    }
    r = requests.post(f"{API}/text-to-speech/{voice_id}", headers=_headers(), json=data, timeout=120)
    if r.status_code != 200:
        print(f"❌ HTTP {r.status_code}: {r.text[:300]}", file=sys.stderr)
        return False
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(r.content)
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description="ElevenLabs TTS — voix off WildLens")
    ap.add_argument("--list", action="store_true", help="Lister les voix")
    ap.add_argument("--text", help="Texte à synthétiser")
    ap.add_argument("--voice", help="voice_id ou nom de PRESETS")
    ap.add_argument("--out", help="Fichier de sortie (.mp3)")
    ap.add_argument("--speed", type=float, default=0.9, help="Débit (1.0 = normal, <1 = plus lent)")
    args = ap.parse_args()

    if args.list:
        try:
            list_voices()
            return 0
        except Exception as e:
            print(f"❌ {e}", file=sys.stderr)
            return 1

    if not args.text or not args.voice:
        ap.error("--text et --voice requis (ou --list)")
    voice_id = PRESETS.get(args.voice, args.voice)
    out = Path(args.out) if args.out else Path("voix-off.mp3")
    try:
        if synth(args.text, voice_id, out, speed=args.speed):
            print(f"✅ {out} (voix {voice_id}, speed {args.speed})")
            return 0
        return 1
    except Exception as e:
        print(f"❌ {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
