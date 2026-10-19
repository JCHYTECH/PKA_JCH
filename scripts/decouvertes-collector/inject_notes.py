#!/usr/bin/env python3
"""Injecte des notes / fichiers texte (JCH_Inbox/00_INBOX/NOTES/) dans la file DÉCOUVERTES.

Pour chaque fichier .txt/.md : détecte les lieux via Claude (un seul ou une liste),
et injecte UNE entrée texte par lieu dans queue/. Le pipeline analyzer.py (inchangé)
génère ensuite une fiche par entrée.

Gère le mixte : une note = un lieu OU une liste de lieux.

Usage :
  python3 inject_notes.py             # tous les .txt/.md de 00_INBOX/NOTES/
  python3 inject_notes.py --dry-run   # aperçu (lieux détectés) sans injecter
  python3 inject_notes.py --no-split  # injecte la note telle quelle (1 entrée = 1 note)
  python3 inject_notes.py --limit 3   # traite seulement les 3 premiers fichiers
"""
import argparse
import datetime
import json
import os
import re
import sys
from pathlib import Path

from dotenv import load_dotenv

PKA_ROOT = Path(os.getenv("PKA_ROOT", Path(__file__).resolve().parents[2]))
BASE = PKA_ROOT / "JCH_Inbox/03_PROJECTS/07_TRAVELS/pka-decouvertes"
QUEUE = BASE / "queue"
NOTES_DIR = PKA_ROOT / "JCH_Inbox/00_INBOX/NOTES"

MODEL = "claude-haiku-4-5-20251001"

SPLIT_PROMPT = """Tu es l'agent PKA_DECOUVERTES. Ce texte peut mentionner un ou plusieurs lieux touristiques à visiter (villes, villages, monuments, réserves naturelles, parcs, lacs, plages, montagnes, gorges, cascades...).

Texte : {text}

Identifie TOUS les lieux mentionnés. Pour chaque lieu, donne une formulation claire et désambiguïsée (ajoute la ville/région/pays si le texte la mentionne, sinon laisse juste le nom).

Retourne UNIQUEMENT un JSON valide :
{{"places": ["lieu 1", "lieu 2", ...]}}

Si le texte ne mentionne AUCUN lieu : {{"places": []}}
"""


def _extract_json(raw: str):
    raw = raw.strip()
    if "```" in raw:
        for part in raw.split("```"):
            part = part.strip()
            if part.startswith("json"):
                part = part[4:]
            try:
                return json.loads(part)
            except json.JSONDecodeError:
                continue
    start, end = raw.find("{"), raw.rfind("}")
    if start != -1 and end != -1:
        try:
            return json.loads(raw[start:end + 1])
        except json.JSONDecodeError:
            pass
    return json.loads(raw)


def call_claude(prompt: str) -> str:
    import anthropic
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    resp = client.messages.create(
        model=MODEL, max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text


def split_places(text: str) -> list[str]:
    raw = call_claude(SPLIT_PROMPT.format(text=text[:4000]))
    data = _extract_json(raw)
    places = data.get("places", []) if isinstance(data, dict) else []
    return [p.strip() for p in places if isinstance(p, str) and p.strip()]


def injected_sources() -> set:
    seen = set()
    for q in QUEUE.glob("*.json"):
        try:
            sf = json.loads(q.read_text()).get("source_file")
            if sf:
                seen.add(sf)
        except Exception:
            pass
    return seen


def inject(text: str, source_file: str, ts: str, n: int) -> str:
    slug = f"{ts}_{n}"
    payload = {
        "telegram_message_id": "0",
        "telegram_group": "NOTES",
        "author": "JCH",
        "datetime": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "content_type": "text",
        "text": text,
        "links": [],
        "media_files": [],
        "analysis_status": "pending",
        "place_candidates": [],
        "confidence": None,
        "source_file": source_file,
    }
    (QUEUE / f"{slug}.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2))
    return slug


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-split", action="store_true", help="1 entrée = 1 note (sans détection de liste)")
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args()

    _env = PKA_ROOT / "JCH_PRIVATE" / "decouvertes.env"
    if _env.exists():
        load_dotenv(_env)

    NOTES_DIR.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)

    files = sorted(f for f in NOTES_DIR.glob("*")
                   if f.suffix.lower() in {".txt", ".md", ".text"})
    if args.limit:
        files = files[: args.limit]
    if not files:
        print(f"Aucun .txt/.md dans {NOTES_DIR.relative_to(PKA_ROOT)}/")
        return 0

    seen = injected_sources()
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    n = 0
    total_places = 0

    for f in files:
        if f.name in seen:
            print(f"skip (déjà en file) : {f.name}")
            continue
        text = f.read_text(encoding="utf-8", errors="replace").strip()
        if not text:
            print(f"skip (vide)         : {f.name}")
            continue

        if args.no_split:
            places = [text]
        else:
            if not os.getenv("ANTHROPIC_API_KEY"):
                print("✗ ANTHROPIC_API_KEY introuvable (JCH_PRIVATE/decouvertes.env).")
                return 1
            print(f"analyse {f.name} ...")
            places = split_places(text)

        if not places:
            print(f"  ↦ aucun lieu détecté — {f.name} (ignoré)")
            continue

        total_places += len(places)
        for p in places:
            n += 1
            label = p if len(p) <= 50 else p[:50] + "…"
            if args.dry_run:
                print(f"  ↦ (dry-run) {label}")
            else:
                slug = inject(p, f.name, ts, n)
                print(f"  ↦ {slug}  <- {label}")

    print(f"\n{total_places} lieu(x) injecté(s) depuis {len(files)} note(s).")
    if total_places and not args.dry_run:
        print("Lance ensuite :  python3 scripts/decouvertes-collector/analyzer.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
