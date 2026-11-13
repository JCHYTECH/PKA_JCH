#!/usr/bin/env python3
"""
insectnet.py — InsectNet V0.1 : classification bioacoustique d'orthoptères.
Prend un fichier WAV (ou un dossier), prédit l'espèce.

Usage:
  python3 scripts/insectnet.py --input grillon.wav
  python3 scripts/insectnet.py --input ./enregistrements/  # dossier
  python3 scripts/insectnet.py --input champ.wav --json     # sortie JSON

Dépendances : numpy, soundfile, librosa, onnxruntime
Modèle ONNX : tmp/insectnet_cnn.onnx (généré par la session Arbor 2026-06-19)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

import numpy as np
import soundfile as sf

try:
    import librosa
except ImportError:
    sys.exit("Missing 'librosa'. Install: pip3 install librosa")

try:
    import onnxruntime as ort
except ImportError:
    sys.exit("Missing 'onnxruntime'. Install: pip3 install onnxruntime")

# ── Config ────────────────────────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = REPO_ROOT / "tmp/insectnet_cnn.onnx"
SPECIES_PATH = REPO_ROOT / "tmp/insectnet_species.json"
N_MELS = 128
N_FFT = 1024
HOP_LEN = 512
FIXED_FRAMES = 256
TARGET_SR = 48000


def load_model():
    """Charge le modèle ONNX et la liste d'espèces."""
    if not MODEL_PATH.exists():
        sys.exit(f"Model not found: {MODEL_PATH}\nRun the training pipeline first.")
    if not SPECIES_PATH.exists():
        sys.exit(f"Species list not found: {SPECIES_PATH}")

    session = ort.InferenceSession(str(MODEL_PATH))
    species = json.loads(SPECIES_PATH.read_text())
    return session, species


def preprocess(audio: np.ndarray, sr: int) -> np.ndarray:
    """Convertit un signal audio en mel-spectrogramme normalisé (1, 1, 128, 256)."""
    if len(audio.shape) > 1:
        audio = audio.mean(axis=1)

    if sr != TARGET_SR:
        audio = librosa.resample(audio.astype(np.float64), orig_sr=sr, target_sr=TARGET_SR)

    spec = librosa.feature.melspectrogram(
        y=audio.astype(np.float32), sr=TARGET_SR,
        n_mels=N_MELS, n_fft=N_FFT, hop_length=HOP_LEN
    )
    log_spec = librosa.power_to_db(spec, ref=np.max)
    log_spec = (log_spec - log_spec.mean()) / max(log_spec.std(), 1e-6)

    if log_spec.shape[1] < FIXED_FRAMES:
        log_spec = np.pad(log_spec, ((0, 0), (0, FIXED_FRAMES - log_spec.shape[1])), mode='constant')
    else:
        log_spec = log_spec[:, :FIXED_FRAMES]

    return log_spec[np.newaxis, np.newaxis, :, :].astype(np.float32)


def predict(file_path: Path, session, species: list[str]) -> dict:
    """Prédit l'espèce pour un fichier audio."""
    audio, sr = sf.read(str(file_path))
    x = preprocess(audio, sr)

    inputs = {session.get_inputs()[0].name: x}
    logits = session.run(None, inputs)[0][0]

    # Softmax
    ex = np.exp(logits - logits.max())
    probs = ex / ex.sum()

    pred_idx = int(np.argmax(probs))
    return {
        "file": file_path.name,
        "species": species[pred_idx],
        "confidence": round(float(probs[pred_idx]), 4),
        "probabilities": {
            sp: round(float(p), 4)
            for sp, p in zip(species, probs.tolist())
        },
    }


def process_input(input_path: Path, session, species: list[str], as_json: bool = False):
    """Traite un fichier unique ou un dossier de WAV."""
    if input_path.is_file():
        results = [predict(input_path, session, species)]
    elif input_path.is_dir():
        wavs = sorted(input_path.glob("*.wav")) + sorted(input_path.glob("*.WAV"))
        if not wavs:
            sys.exit(f"No WAV files found in {input_path}")
        results = []
        for i, wav in enumerate(wavs):
            if not as_json and i % 50 == 0:
                print(f"  {i}/{len(wavs)}...", file=sys.stderr)
            results.append(predict(wav, session, species))
    else:
        sys.exit(f"Input not found: {input_path}")

    if as_json:
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        for r in results:
            conf = r["confidence"]
            bar = "█" * int(conf * 20) + "░" * (20 - int(conf * 20))
            print(f"{r['species']:30s} {bar} {conf:.1%}")
            if len(results) == 1:
                print()
                others = [(sp, p) for sp, p in r["probabilities"].items() if p > 0.01 and sp != r["species"]]
                if others:
                    print("  Autres:")
                    for sp, p in sorted(others, key=lambda x: -x[1]):
                        print(f"    {sp:30s} {p:.1%}")

    return results


# ── CLI ────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="InsectNet V0.1 — Classification bioacoustique d'orthoptères"
    )
    parser.add_argument("--input", "-i", required=True, help="Fichier WAV ou dossier")
    parser.add_argument("--json", "-j", action="store_true", help="Sortie JSON")
    args = parser.parse_args()

    session, species = load_model()
    input_path = Path(args.input).expanduser().resolve()
    process_input(input_path, session, species, as_json=args.json)


if __name__ == "__main__":
    main()
