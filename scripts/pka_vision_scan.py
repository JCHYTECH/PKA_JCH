#!/usr/bin/env python3
"""pka_vision_scan.py — Scanner un dossier d'images avec un modèle vision (OpenRouter).

Construit des planches-contact (grilles) et demande au modèle vision de
localiser une image répondant à une description.

Usage :
    python3 scripts/pka_vision_scan.py <dossier> "<description cible>"
"""
from __future__ import annotations

import base64
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "openai/gpt-4o-mini"
CELL = 320  # taille de cellule en px
COLS = 4
ROWS = 3
PER_SHEET = COLS * ROWS


def key() -> str:
    return Path(os.path.expanduser("~/.config/pka-jch/openrouter_key.txt")) \
        .read_text().strip()


def list_images(folder: Path) -> list[Path]:
    imgs = sorted(
        [p for p in folder.iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png"}],
        key=lambda p: int(re.findall(r"\d+", p.stem)[-1]) if re.findall(r"\d+", p.stem) else 0,
    )
    return imgs


def build_sheet(imgs: list[Path], start: int, sheet_idx: int) -> tuple[Path, dict]:
    """Construit une planche de PER_SHEET images numérotées. Retourne (chemin, mapping)."""
    n = min(PER_SHEET, len(imgs) - start)
    cols = COLS if n >= COLS else n
    rows = (n + cols - 1) // cols
    sheet = Image.new("RGB", (cols * CELL, rows * CELL), "white")
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 56)
    except Exception:
        font = ImageFont.load_default()
    mapping: dict[int, str] = {}
    for i in range(n):
        idx = start + i
        img = Image.open(imgs[idx]).convert("RGB")
        img.thumbnail((CELL - 8, CELL - 8))
        r, c = divmod(i, cols)
        x, y = c * CELL, r * CELL
        sheet.paste(img, (x + 4, y + 4))
        draw.rectangle([x, y, x + CELL - 1, y + CELL - 1], outline="black", width=3)
        draw.text((x + 6, y + 2), str(i + 1), fill="red", font=font, stroke_width=2)
        mapping[i + 1] = imgs[idx].name
    out = Path(f"/tmp/sheet_{sheet_idx}.jpg")
    sheet.save(out, quality=88)
    return out, mapping


def ask_vision(sheet: Path, prompt: str) -> str:
    b64 = base64.b64encode(sheet.read_bytes()).decode()
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": [
            {"type": "text", "text": prompt},
            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
        ]}],
        "max_tokens": 200,
    }
    body = json.dumps(payload)
    r = subprocess.run(
        ["curl", "-sS", "--max-time", "60", OPENROUTER_URL,
         "-H", f"Authorization: Bearer {key()}",
         "-H", "Content-Type: application/json", "-d", body],
        capture_output=True, text=True, timeout=70,
    )
    try:
        return json.loads(r.stdout)["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"[ERREUR] {e} :: {r.stdout[:300]}"


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 1
    folder = Path(sys.argv[1])
    target = sys.argv[2]
    imgs = list_images(folder)
    print(f"{len(imgs)} images trouvées dans {folder}")
    sheets = (len(imgs) + PER_SHEET - 1) // PER_SHEET
    for s in range(sheets):
        sheet, mapping = build_sheet(imgs, s * PER_SHEET, s)
        prompt = (f"Voici une planche de {len(mapping)} vignettes numérotées (1..{len(mapping)}), "
                  f"en lecture ligne par ligne. Objectif : {target}. "
                  f"Réponds UNIQUEMENT par les numéros des vignettes qui correspondent "
                  f"(ex: '3' ou '5,7'), ou 'aucune' si rien ne correspond. "
                  f"Sois bref, pas de phrase.")
        answer = ask_vision(sheet, prompt)
        print(f"\n=== Planche {s + 1}/{sheets} → {answer}")
        for num in re.findall(r"\d+", answer):
            n = int(num)
            if n in mapping:
                print(f"   → vignette {num} = {mapping[n]}")
    print("\nScan terminé.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
