#!/usr/bin/env python3
"""
inat_species.py — Species identification via Gemini 2.0 Flash (free tier).
Returns species name, Latin binomial, confidence, and alternatives.
Used as the species pass in PKA Vision's two-pass architecture.

Usage:
  python3 scripts/inat_species.py --image photo.jpg
  python3 scripts/inat_species.py --image photo.jpg --json  (raw JSON output)
"""

import argparse, base64, json, sys, os
from pathlib import Path

GEMINI_KEY_FILE = Path.home() / ".config/pka-jch/api_keys"

def load_gemini_key() -> str:
    if not GEMINI_KEY_FILE.exists():
        sys.exit(f"❌ API key file not found: {GEMINI_KEY_FILE}")
    for line in GEMINI_KEY_FILE.read_text().splitlines():
        if line.startswith("GEMINI_API_KEY="):
            return line.split("=", 1)[1].strip()
    sys.exit("❌ GEMINI_API_KEY not found in api_keys")

def identify_species(image_path: str, model: str = "gemini-3.1-flash-lite") -> dict:
    """Send image to Gemini, return species identification with Latin name."""
    import requests

    key = load_gemini_key()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={key}"

    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("ascii")

    prompt = """You are a wildlife biologist. Identify the animal species in this photograph. 
Return ONLY a JSON object, no markdown, no explanations.

{
  "species": "Mésange charbonnière",
  "latin": "Parus major",
  "family": "Paridae",
  "order": "Passeriformes",
  "confidence": 0.92,
  "alternatives": [
    {"species": "Mésange bleue", "latin": "Cyanistes caeruleus", "confidence": 0.05}
  ],
  "behavior": "perché, repos",
  "count": 1,
  "notes": "Plumage caractéristique, bavette noire, dessus olive"
}

RULES:
- species: most likely species in French common name
- latin: binomial scientific name (Genus species)
- confidence: your certainty (0-1). Be honest. Use 0.3-0.5 if unsure.
- If NO animal is visible, set species to null and confidence to 0.
- If you see an animal but cannot identify beyond family, set species to "indéterminé" and latin to null.
- NEVER invent a species you don't see.
- alternatives: up to 3 alternative species with lower confidence."""

    payload = {
        "contents": [{
            "parts": [
                {"text": prompt},
                {"inline_data": {"mime_type": "image/jpeg", "data": img_b64}}
            ]
        }],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 512}
    }

    resp = requests.post(url, json=payload, timeout=30)
    resp.raise_for_status()
    body = resp.json()

    try:
        text = body["candidates"][0]["content"]["parts"][0]["text"]
        # Extract JSON
        start = text.find("{")
        end = text.rfind("}")
        if start >= 0 and end > start:
            return json.loads(text[start:end+1])
    except (KeyError, IndexError, json.JSONDecodeError):
        pass
    return {"species": None, "latin": None, "confidence": 0, "error": "parse_failed"}

def main():
    p = argparse.ArgumentParser(description="Species ID via Gemini")
    p.add_argument("--image", required=True)
    p.add_argument("--json", action="store_true")
    p.add_argument("--model", default="gemini-2.0-flash")
    args = p.parse_args()

    result = identify_species(args.image, args.model)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        sp = result.get("species")
        latin = result.get("latin")
        conf = result.get("confidence", 0)
        if sp and latin:
            print(f"{sp} ({latin}) — {conf:.0%}")
        elif sp == "indéterminé":
            print(f"Animal présent — espèce indéterminée")
        elif sp is None:
            print("Aucun animal détecté")
        else:
            print(json.dumps(result, ensure_ascii=False))

if __name__ == "__main__":
    main()
