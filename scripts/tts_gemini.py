#!/usr/bin/env python3
"""
tts_gemini.py — Synthèse vocale Gemini TTS (voix off WildLens).

Réutilise le modèle déjà branché sur le bot Telegram :
  modèle : gemini-2.5-flash-preview-tts
  voix   : prebuilt_voice_config (défaut Zephyr)

Usage :
  python3 scripts/tts_gemini.py --text "..." --voice Zephyr --out fichier.wav
  python3 scripts/tts_gemini.py --test           # échantillons multi-voix dans video/

Clé : GEMINI_API_KEY (env) ou ~/.config/pka-jch/api_keys
"""

from __future__ import annotations

import argparse
import os
import struct
import sys
from pathlib import Path

from google import genai

TTS_MODEL = "gemini-2.5-flash-preview-tts"
VIDEO_DIR = Path(__file__).resolve().parent.parent / "JCH_Inbox" / "03_PROJECTS" / "02_ARTEON" / "wildlens" / "video"

CANDIDATE_VOICES = ["Zephyr", "Puck", "Charon", "Orion", "Ursa", "Kore", "Leda"]

TEST_TEXT = (
    "Ce rêve de comprendre les animaux n'est pas nouveau. "
    "Le Coran dit que Salomon fut instruit du langage des oiseaux. "
    "En Chine, Gongye Chang passait pour les comprendre. "
    "Et au Mozambique, un oiseau sauvage mène encore les hommes au miel."
)


def load_key() -> str:
    env = os.environ.get("GEMINI_API_KEY", "").strip()
    if env:
        return env
    f = Path("~/.config/pka-jch/api_keys").expanduser()
    if f.exists():
        for line in f.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("GEMINI_API_KEY"):
                # accepte `=` ou `:` comme séparateur
                for sep in ("=", ":"):
                    if sep in line:
                        val = line.split(sep, 1)[1].strip().strip('"').strip("'")
                        if val:
                            return val
    raise RuntimeError("GEMINI_API_KEY introuvable")


def pcm_to_wav(pcm: bytes, sample_rate: int = 24000) -> bytes:
    """PCM brut → WAV (header 44 bytes)."""
    byte_rate = sample_rate * 2
    data_size = len(pcm)
    header = struct.pack(
        "<4sI4s4sIHHIIHH4sI",
        b"RIFF", 36 + data_size, b"WAVE", b"fmt ", 16,
        1, 1, sample_rate, byte_rate, 2, 16,
        b"data", data_size,
    )
    return header + pcm


def synth(text: str, voice: str, out_path: Path) -> bool:
    client = genai.Client(api_key=load_key())
    resp = client.models.generate_content(
        model=TTS_MODEL,
        contents=[{"role": "user", "parts": [{"text": text}]}],
        config={
            "response_modalities": ["AUDIO"],
            "speech_config": {
                "voice_config": {
                    "prebuilt_voice_config": {"voice_name": voice}
                }
            },
        },
    )
    for part in resp.candidates[0].content.parts:
        if hasattr(part, "inline_data") and part.inline_data and "audio" in part.inline_data.mime_type:
            out_path.write_bytes(pcm_to_wav(part.inline_data.data))
            return True
    return False


def main() -> int:
    ap = argparse.ArgumentParser(description="Gemini TTS — voix off WildLens")
    ap.add_argument("--text", help="Texte à synthétiser")
    ap.add_argument("--voice", default="Zephyr", help="Nom de la voix préenregistrée")
    ap.add_argument("--out", help="Fichier WAV de sortie")
    ap.add_argument("--test", action="store_true", help="Générer les échantillons multi-voix")
    args = ap.parse_args()

    if args.test:
        VIDEO_DIR.mkdir(parents=True, exist_ok=True)
        for v in CANDIDATE_VOICES:
            out = VIDEO_DIR / f"voix-{v}.wav"
            try:
                if synth(TEST_TEXT, v, out):
                    print(f"✅ {v:8} → {out.name}")
                else:
                    print(f"⚠️  {v:8} → pas d'audio")
            except Exception as e:
                print(f"❌ {v:8} → {e}")
        return 0

    if not args.text:
        ap.error("--text requis (ou --test)")
    out = Path(args.out) if args.out else VIDEO_DIR / f"voix-{args.voice}.wav"
    out.parent.mkdir(parents=True, exist_ok=True)
    try:
        if synth(args.text, args.voice, out):
            print(f"✅ WAV → {out}")
            return 0
        print("⚠️ pas d'audio dans la réponse", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"❌ {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
