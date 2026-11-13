#!/usr/bin/env python3
"""
generate_vo.py — Génère la voix off complète du storyboard FR (ElevenLabs).

Lit les lignes « - **VO :** … » de storyboard-FR.md et produit un MP3 par scène
dans video/vo/scene-NN.mp3 (pour caler chaque scène dans le montage).

Usage :
  python3 scripts/generate_vo.py                 # voix Brian, débit 0.9
  python3 scripts/generate_vo.py --voice <id> --speed 0.85
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tts_elevenlabs import synth  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
STORY = ROOT / "JCH_Inbox" / "03_PROJECTS" / "02_ARTEON" / "wildlens" / "video" / "storyboard-FR.md"
OUT_DIR = ROOT / "JCH_Inbox" / "03_PROJECTS" / "02_ARTEON" / "wildlens" / "video" / "vo"

# Voix retenue par JC : Brian — grave, chaleureux, rassurant
DEFAULT_VOICE = "nPczCjzI2devNBz1zQrb"
DEFAULT_SPEED = 0.9


def extract_vos(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return re.findall(r"^- \*\*VO :\*\*\s*(.*)$", text, re.M)


def main() -> int:
    ap = argparse.ArgumentParser(description="Voix off WildLens (ElevenLabs) depuis le storyboard FR")
    ap.add_argument("--voice", default=DEFAULT_VOICE, help="voice_id ElevenLabs")
    ap.add_argument("--speed", type=float, default=DEFAULT_SPEED, help="Débit (1.0 normal, <1 plus lent)")
    args = ap.parse_args()

    vos = extract_vos(STORY)
    if not vos:
        print("❌ Aucune ligne VO trouvée dans le storyboard.", file=sys.stderr)
        return 1
    print(f"{len(vos)} scènes détectées · débit {args.speed}")

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ok = 0
    for i, vo in enumerate(vos, 1):
        out = OUT_DIR / f"scene-{i:02d}.mp3"
        try:
            if synth(vo, args.voice, out, speed=args.speed):
                print(f"✅ scene-{i:02d}.mp3  ({len(vo.split())} mots)")
                ok += 1
            else:
                print(f"⚠️  scene-{i:02d} — échec")
        except Exception as e:
            print(f"❌ scene-{i:02d} — {e}")

    print(f"\n{ok}/{len(vos)} scènes générées → {OUT_DIR}")
    return 0 if ok == len(vos) else 1


if __name__ == "__main__":
    raise SystemExit(main())
