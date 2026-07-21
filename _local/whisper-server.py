#!/usr/bin/env python3
"""Whisper local server — OpenAI-compatible /v1/audio/transcriptions endpoint.
Uses faster-whisper (CTranslate2) for CPU-optimized transcription.
Designed for VS Code Whisper Assistant extension (martinopensky.whisper-assistant).

Supports both simple ({"text": "..."}) and verbose_json response formats.
The extension v1.2.4 sends response_format=verbose_json.
"""

import os
import tempfile
import argparse
import logging
from flask import Flask, request, jsonify

MODEL_SIZE = os.environ.get("WHISPER_MODEL", "base")
PORT = int(os.environ.get("WHISPER_PORT", "4444"))
API_KEY = os.environ.get("WHISPER_API_KEY", "localhost-key-must-be-set")
DEFAULT_LANGUAGE = os.environ.get("WHISPER_LANGUAGE", "fr")

app = Flask(__name__)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("whisper-server")

# Lazy-load model on first request
_model = None


def get_model():
    global _model
    if _model is None:
        from faster_whisper import WhisperModel
        log.info(f"Loading model '{MODEL_SIZE}' (cpu, int8)...")
        _model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")
        log.info(f"Model '{MODEL_SIZE}' loaded.")
    return _model


@app.route("/v1/audio/transcriptions", methods=["POST"])
def transcribe():
    # Auth check
    auth_header = request.headers.get("Authorization", "")
    if auth_header != f"Bearer {API_KEY}":
        log.warning(f"Unauthorized request: {auth_header[:30]}...")
        return jsonify({"error": "Unauthorized"}), 401

    if "file" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["file"]
    # Extension v1.2.4 hardcodes language='en' — always override with DEFAULT_LANGUAGE (fr)
    language = DEFAULT_LANGUAGE
    # Extension sends response_format=verbose_json
    response_format = request.form.get("response_format", "json")

    # Save to temp file
    suffix = os.path.splitext(audio_file.filename or "audio.wav")[1] or ".wav"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        audio_file.save(tmp.name)
        tmp_path = tmp.name

    try:
        model = get_model()
        log.info(f"Transcribing (lang={language}, fmt={response_format}, file={os.path.basename(tmp_path)})...")

        segments, info = model.transcribe(tmp_path, language=language, beam_size=5)

        # Collect segments (generator → list)
        segment_list = list(segments)
        text = " ".join(segment.text for segment in segment_list).strip()

        log.info(f"Transcription: {text[:100]}{'...' if len(text)>100 else ''}")

        if response_format == "verbose_json":
            # Full OpenAI-compatible verbose_json format
            return jsonify({
                "task": "transcribe",
                "language": language,
                "duration": info.duration,
                "text": text,
                "segments": [
                    {
                        "id": seg.id,
                        "seek": getattr(seg, "seek", 0),
                        "start": seg.start,
                        "end": seg.end,
                        "text": seg.text,
                        "tokens": getattr(seg, "tokens", []),
                        "temperature": getattr(seg, "temperature", 0.0),
                        "avg_logprob": getattr(seg, "avg_logprob", 0.0),
                        "compression_ratio": getattr(seg, "compression_ratio", 0.0),
                        "no_speech_prob": getattr(seg, "no_speech_prob", 0.0),
                    }
                    for seg in segment_list
                ],
            })
        else:
            # Simple format
            return jsonify({"text": text})

    except Exception as e:
        log.error(f"Transcription error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500
    finally:
        os.unlink(tmp_path)


@app.route("/v1/models", methods=["GET"])
def models():
    return jsonify({
        "object": "list",
        "data": [{"id": f"whisper-{MODEL_SIZE}", "object": "model"}]
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "model": MODEL_SIZE, "language": DEFAULT_LANGUAGE})


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Local Whisper Server")
    parser.add_argument("--model", default=MODEL_SIZE, help=f"Model size (default: {MODEL_SIZE})")
    parser.add_argument("--port", type=int, default=PORT, help=f"Port (default: {PORT})")
    parser.add_argument("--language", default=DEFAULT_LANGUAGE, help=f"Default language (default: {DEFAULT_LANGUAGE})")
    args = parser.parse_args()

    MODEL_SIZE = args.model
    DEFAULT_LANGUAGE = args.language

    log.info(f"Starting on port {args.port}, model={MODEL_SIZE}, language={DEFAULT_LANGUAGE}")
    app.run(host="127.0.0.1", port=args.port, debug=False)
