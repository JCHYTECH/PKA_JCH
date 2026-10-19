#!/usr/bin/env python3
"""Passe vision forcée sur les items 'skipped' de la file DÉCOUVERTES (MODE A SITES).

L'analyzer text-only échoue sur les screenshots Instagram où l'OCR ne sort que du
bruit (« Translation », « ADIMNIG »…). Ce script envoie l'IMAGE elle-même à Claude
(vision), puis géolocalise via Nominatim et écrit une fiche dans drafts/.

Usage :
  python3 identify_skips.py [--dry-run]
"""
import base64
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import anthropic
import requests
from dotenv import load_dotenv

PKA_ROOT = Path(os.getenv("PKA_ROOT", Path(__file__).resolve().parents[2]))
_env = PKA_ROOT / "JCH_PRIVATE" / "decouvertes.env"
load_dotenv(_env)

BASE = PKA_ROOT / "JCH_Inbox/03_PROJECTS/07_TRAVELS/pka-decouvertes"
QUEUE = BASE / "queue"
DRAFTS = BASE / "drafts"
DRAFTS.mkdir(parents=True, exist_ok=True)

MODEL = "claude-sonnet-4-6"
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

VISION_PROMPT = """Tu identifies des lieux à partir de captures d'écran Instagram.
Regarde l'IMAGE et identifie le lieu précis représenté (village, monument, lac,
château, église, panorama, gorge, etc.). Ignore le texte d'interface (boutons
« Translation », « Follow », « See translation », usernames, hashtags, likes).
Réponds UNIQUEMENT en JSON, sans texte autour, exactement ce format :
{"is_place": true, "nom_lieu": "Nom du lieu", "pays": "...", "region": "...", "ville": "...", "type_lieu": "...", "description": "une phrase", "confidence": 0.9}
Si le lieu n'est pas identifiable, réponds : {"is_place": false, "confidence": 0.0}"""


def _extract_json(raw: str):
    raw = raw.strip()
    # Retirer d'éventuels ```json ... ``` autour
    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.lower().startswith("json"):
            raw = raw[4:]
    start = raw.find("{")
    end = raw.rfind("}")
    if start == -1 or end == -1 or end <= start:
        return None
    try:
        return json.loads(raw[start : end + 1])
    except json.JSONDecodeError:
        return None


def geocode(nom: str):
    try:
        r = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": nom, "format": "json", "limit": 1},
            headers={"User-Agent": "PKA_DECOUVERTES/1.0"},
            timeout=15,
        )
        data = r.json()
        if data:
            return float(data[0]["lat"]), float(data[0]["lon"])
    except Exception as e:
        print(f"    [geocode] erreur sur '{nom}': {e}")
    return None


def slugify(name: str) -> str:
    """Slug sûr pour URL/nom de fichier : [A-Za-z0-9._-], sans accents, tronqué à 40."""
    import unicodedata
    s = unicodedata.normalize("NFKD", name or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^A-Za-z0-9._-]+", "-", s).strip("-")
    return s[:40] or "lieu"


def write_note(meta, analysis, gps, image_rel):
    nom = analysis.get("nom_lieu", "Lieu inconnu")
    pays = analysis.get("pays", "")
    region = analysis.get("region", "")
    ville = analysis.get("ville", "")
    descr = analysis.get("description", "")
    conf = analysis.get("confidence", 0)
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    slug = slugify(nom)

    gps_line = f"{gps[0]}, {gps[1]}" if gps else ""
    front = [
        "---",
        "type: lieu_a_visiter",
        "status: validated",
        "source: sites",
        "source_group: SITES",
        f"date_capture: {meta.get('datetime', today)[:10]}",
        f"date_analyse: {today}",
        "auteur: JCH",
        f"pays: {pays}",
        f"region: {region}",
        f"ville: {ville}",
        f"nom_lieu: {nom}",
        f'gps: "{gps_line}"',
        f"confidence: {conf}",
        "tags:",
        "  - decouvertes",
        "  - lieu_a_visiter",
        "---",
        "",
        f"# {nom}",
        "",
        "## Résumé",
        descr,
        "",
    ]
    body = front
    if gps:
        body += [
            "## Localisation",
            f"- GPS : `{gps[0]}, {gps[1]}`",
            f"- [Ouvrir dans Google Maps](https://www.google.com/maps/search/{gps[0]},{gps[1]})",
            f"- Pays : {pays} | Région : {region} | Ville : {ville}",
            "",
        ]
    body += [
        "## Source",
        "- Groupe : SITES",
        f"- Image source : {meta.get('source_file', '?')}",
        "",
        f"## Score de confiance",
        f"**{int(conf*100)}%** — identification vision",
        "",
    ]
    path = DRAFTS / f"{today}_{slug}.md"
    path.write_text("\n".join(body), encoding="utf-8")
    return path


def main():
    dry = "--dry-run" in sys.argv
    targets = []  # list of (Path, dict)
    for p in QUEUE.glob("*.json"):
        slug = p.stem
        if not slug.startswith("20260830_214841_"):
            continue
        d = json.loads(p.read_text())
        if d.get("analysis_status") == "skipped":
            targets.append((p, d))

    print(f"Items skipped à re-analyser (vision) : {len(targets)}")
    if dry:
        for p, d in sorted(targets, key=lambda x: x[0].name):
            print("  ", p.name, "<-", d.get("source_file"))
        return

    ok = 0
    for p, d in sorted(targets, key=lambda x: x[0].name):
        slug = p.stem
        mf = (d.get("media_files") or [{}])[0]
        img = PKA_ROOT / mf.get("file_path", "")
        print(f"\n[{slug}] <- {d.get('source_file')}")
        if not img.exists():
            print("   image introuvable")
            continue
        b64 = base64.standard_b64encode(img.read_bytes()).decode()
        try:
            resp = client.messages.create(
                model=MODEL,
                max_tokens=1024,
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": b64}},
                        {"type": "text", "text": VISION_PROMPT},
                    ],
                }],
            )
            raw = resp.content[0].text
            analysis = _extract_json(raw)
        except Exception as e:
            print(f"   vision erreur: {e}")
            continue

        if not analysis or not analysis.get("is_place"):
            print(f"   vision → pas un lieu (reste skipped)")
            d["analysis_status"] = "skipped"
            p.write_text(json.dumps(d, ensure_ascii=False, indent=2))
            continue

        nom = analysis.get("nom_lieu", "")
        conf = analysis.get("confidence", 0)
        print(f"   vision → {nom} ({int(conf*100)}%)")
        gps = geocode(nom)
        if gps:
            print(f"   GPS : {gps[0]:.4f}, {gps[1]:.4f}")

        note_path = write_note(d, analysis, gps, img)
        # Ré-écrire le JSON de file : analysé + infos
        d["analysis_status"] = "analysed"
        d["place_candidates"] = [nom]
        d["confidence"] = conf
        d["draft_path"] = str(note_path.relative_to(PKA_ROOT))
        d["note"] = "identifié par vision (identify_skips.py)"
        p.write_text(json.dumps(d, ensure_ascii=False, indent=2))
        ok += 1

    print(f"\nTerminé — {ok}/{len(targets)} fiches générées (vision).")


if __name__ == "__main__":
    main()
