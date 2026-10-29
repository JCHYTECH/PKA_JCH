#!/usr/bin/env python3
"""
gemini_voice.py — conversation vocale native avec Gemini 3.1 Flash Live (voix Ursa).

Audio natif : pas de Whisper, pas de TTS séparé, pas de boucle micro/haut-parleur.
- Entrée  : PCM 16 bits / 16 kHz (micro)
- Sortie  : PCM 16 bits / 24 kHz (voix Ursa)

Usage : python3 scripts/gemini_voice.py
Arrêt : Ctrl+C.

Réglages (variables d'env) :
  GEMINI_VOICE  (défaut "Ursa")
  MIC_DEVICE    (défaut ":1" — micro interne)
"""
import asyncio
import base64
import json
import os
import re
import subprocess
import sys

import websockets

MODEL = "models/gemini-3.1-flash-live-preview"
WS_URL = ("wss://generativelanguage.googleapis.com/ws/"
          "google.ai.generativelanguage.v1beta.GenerativeService.BidiGenerateContent?key={key}")
VOICE = os.environ.get("GEMINI_VOICE", "Ursa")
MIC = os.environ.get("MIC_DEVICE", ":1")

SYSTEM_INSTRUCTION = (
    "Tu es Dobby, l'assistant personnel de Jean-Claude. "
    "Réponds TOUJOURS en français, de façon naturelle et concise (2-3 phrases). "
    "Sois chaleureux et efficace."
)


def load_key():
    path = os.path.expanduser("~/.config/pka-jch/api_keys")
    try:
        with open(path) as f:
            for line in f:
                m = re.match(r'(?:export\s+)?GEMINI_API_KEY\s*=\s*["\']?([^"\'#\s]+)', line)
                if m:
                    return m.group(1)
    except OSError:
        pass
    return os.environ.get("GEMINI_API_KEY")


def setup_message():
    return {
        "setup": {
            "model": MODEL,
            "generationConfig": {
                "responseModalities": ["AUDIO"],
                "speechConfig": {
                    "voiceConfig": {"prebuiltVoiceConfig": {"voiceName": VOICE}},
                },
            },
            "systemInstruction": {"parts": [{"text": SYSTEM_INSTRUCTION}]},
        }
    }


async def start_mic():
    return await asyncio.create_subprocess_exec(
        "ffmpeg", "-f", "avfoundation", "-i", MIC,
        "-ar", "16000", "-ac", "1", "-f", "s16le", "-loglevel", "error", "pipe:1",
        stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.DEVNULL)


def audio_chunks(msg):
    """Extrait les chunks audio PCM (bytes) d'un message serverContent."""
    out = []
    turn = msg.get("serverContent", {}).get("modelTurn", {})
    for part in turn.get("parts", []):
        data = part.get("inlineData", {}).get("data")
        if data:
            out.append(base64.b64decode(data))
    return out


async def send_audio(ws, mic, ready):
    await ready.wait()
    print("🎤 Micro ouvert — parle naturellement (Ctrl+C pour quitter).", flush=True)
    while True:
        chunk = await mic.stdout.read(3200)  # ~100 ms à 16 kHz
        if not chunk:
            break
        await ws.send(json.dumps({
            "realtimeInput": {
                "audio": {
                    "mimeType": "audio/pcm;rate=16000",
                    "data": base64.b64encode(chunk).decode(),
                }
            }
        }))


async def receive_audio(ws, ready):
    play = None
    try:
        while True:
            msg = json.loads(await ws.recv())
            if "setupComplete" in msg:
                ready.set()
                continue
            for pcm in audio_chunks(msg):
                if play is None or play.poll() is not None:
                    play = subprocess.Popen(
                        ["play", "-q", "-t", "raw", "-r", "24000",
                         "-e", "signed-integer", "-b", "16", "-c", "1", "-"],
                        stdin=subprocess.PIPE)
                play.stdin.write(pcm)
            if msg.get("serverContent", {}).get("turnComplete"):
                if play:
                    play.stdin.close()
                    play.wait()
                    play = None
    except websockets.exceptions.ConnectionClosed:
        pass


async def main():
    key = load_key()
    if not key:
        print("❌ GEMINI_API_KEY introuvable (vérifie ~/.config/pka-jch/api_keys).")
        return 1
    mic = await start_mic()
    ready = asyncio.Event()
    print(f"🐶 Dobby vocal — Gemini Live · voix {VOICE} · connexion…", flush=True)
    try:
        async with websockets.connect(WS_URL.format(key=key), max_size=10_000_000) as ws:
            await ws.send(json.dumps(setup_message()))
            await asyncio.gather(send_audio(ws, mic, ready), receive_audio(ws, ready))
    except websockets.exceptions.InvalidStatus as e:
        print(f"❌ Connexion refusée (clé ou modèle invalide) : {e}")
        return 1
    except Exception as e:
        print(f"❌ Erreur : {e}")
        return 1
    finally:
        mic.terminate()
    return 0


if __name__ == "__main__":
    try:
        sys.exit(asyncio.run(main()))
    except KeyboardInterrupt:
        print("\n👋 À bientôt.")
