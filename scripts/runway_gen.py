#!/usr/bin/env python3
"""
runway_gen.py — Génération vidéo IA via Runway (mécanique réutilisable WildLens).

Deux modes, c'est la « mécanique » qu'on réutilisera :
  - texte → vidéo   : clips abstraits, métaphores visuelles (jamais de faune).
  - image → vidéo   : animer une photo réelle de JC (léger mouvement de caméra).

Usage :
  python3 scripts/runway_gen.py --text "..." --out clip.mp4 [--duration 5] [--ratio 16:9]
  python3 scripts/runway_gen.py --image photo.jpg --prompt "..." --out clip.mp4

Clé : RUNWAY_API_KEY (env) ou ~/.config/pka-jch/runway_api_key.txt
"""

from __future__ import annotations

import argparse
import base64
import os
import sys
import time
from pathlib import Path

import requests

API = "https://api.dev.runwayml.com/v1"
MODEL = "gen4.5"  # runway ; autres dispo : kling3.0_standard, seedance2, hailuo3
VERSION = "2024-11-06"  # en-tête X-Runway-Version requis (seule version valide)


def load_key() -> str:
    env = os.environ.get("RUNWAY_API_KEY", "").strip()
    if env:
        return env
    f = Path("~/.config/pka-jch/runway_api_key.txt").expanduser()
    if f.exists():
        val = f.read_text(encoding="utf-8").strip()
        if val:
            return val
    raise RuntimeError("RUNWAY_API_KEY introuvable")


def _headers() -> dict:
    return {"Authorization": f"Bearer {load_key()}", "Content-Type": "application/json", "X-Runway-Version": VERSION}


def _image_to_data_uri(path: Path) -> str:
    data = base64.b64encode(path.read_bytes()).decode()
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    return f"data:{mime};base64,{data}"


def _poll(task_id: str, timeout: int = 300) -> dict:
    t0 = time.time()
    while True:
        r = requests.get(f"{API}/tasks/{task_id}", headers=_headers(), timeout=30)
        r.raise_for_status()
        task = r.json()
        status = task.get("status", "")
        if status in ("SUCCEEDED", "FAILED", "CANCELLED"):
            return task
        if time.time() - t0 > timeout:
            raise TimeoutError(f"Génération trop longue (>{timeout}s)")
        time.sleep(5)


def _download(url: str, out: Path) -> None:
    r = requests.get(url, timeout=120)
    r.raise_for_status()
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(r.content)


def text_to_video(prompt: str, out: Path, duration: int = 5, ratio: str = "1280:720",
                  model: str = MODEL, timeout: int = 300) -> bool:
    payload = {"promptText": prompt, "model": model, "duration": duration, "ratio": ratio}
    r = requests.post(f"{API}/text_to_video", headers=_headers(), json=payload, timeout=60)
    if r.status_code >= 400:
        print(f"❌ HTTP {r.status_code}: {r.text[:300]}", file=sys.stderr)
        return False
    task = _poll(r.json().get("id") or r.json().get("task", {}).get("id"), timeout=timeout)
    if task.get("status") != "SUCCEEDED":
        print(f"❌ échec : {task.get('failure', task.get('status'))}", file=sys.stderr)
        return False
    outputs = task.get("output", [])
    if not outputs:
        print("❌ aucune sortie vidéo", file=sys.stderr)
        return False
    _download(outputs[0], out)
    print(f"✅ {out}")
    return True


def image_to_video(image: str, prompt: str, out: Path, duration: int = 5,
                   ratio: str = "1280:720", model: str = MODEL, timeout: int = 300) -> bool:
    # image = chemin local OU url http(s)
    img = image if image.startswith(("http://", "https://")) else _image_to_data_uri(Path(image))
    payload = {"promptImage": img, "promptText": prompt, "model": model,
               "duration": duration, "ratio": ratio}
    r = requests.post(f"{API}/image_to_video", headers=_headers(), json=payload, timeout=60)
    if r.status_code >= 400:
        print(f"❌ HTTP {r.status_code}: {r.text[:300]}", file=sys.stderr)
        return False
    task = _poll(r.json().get("id") or r.json().get("task", {}).get("id"), timeout=timeout)
    if task.get("status") != "SUCCEEDED":
        print(f"❌ échec : {task.get('failure', task.get('status'))}", file=sys.stderr)
        return False
    outputs = task.get("output", [])
    if not outputs:
        print("❌ aucune sortie vidéo", file=sys.stderr)
        return False
    _download(outputs[0], out)
    print(f"✅ {out}")
    return True


def main() -> int:
    ap = argparse.ArgumentParser(description="Runway — génération vidéo IA (WildLens)")
    ap.add_argument("--text", help="Prompt texte → vidéo")
    ap.add_argument("--image", help="Image source (chemin ou URL) → vidéo")
    ap.add_argument("--prompt", help="Prompt (pour --image)")
    ap.add_argument("--out", required=True, help="Fichier .mp4 de sortie")
    ap.add_argument("--duration", type=int, default=5, help="Durée (5 ou 10 s)")
    ap.add_argument("--ratio", default="1280:720", help="Format (1280:720 = 16:9 · 720:1280 = 9:16)")
    args = ap.parse_args()

    try:
        if args.text:
            ok = text_to_video(args.text, Path(args.out), args.duration, args.ratio)
        elif args.image:
            ok = image_to_video(args.image, args.prompt or "", Path(args.out), args.duration, args.ratio)
        else:
            ap.error("--text ou --image requis")
        return 0 if ok else 1
    except Exception as e:
        print(f"❌ {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
