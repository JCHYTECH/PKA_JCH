#!/usr/bin/env python3
"""
photo_keyworder.py — Auto-tagging nature photos via local vision model (Ollama).
Analyzes images and writes IPTC keywords + structured XMP metadata.
100% local — no Google API, no cloud dependency.

Usage:
  python3 photo_keyworder.py --input ~/Desktop/Photos_to_tag/
  python3 photo_keyworder.py --input ~/Pictures/batch/ --model llama3.2-vision:11b --endpoint http://100.73.212.110:11434
  python3 photo_keyworder.py --input img.jpg --dry-run   (preview only, no write)

Dependencies: exiftool, requests, Pillow
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

try:
    import requests
except ImportError:
    sys.exit("Missing 'requests'. Install: pip3 install requests")

# ── Config ────────────────────────────────────────────────────────────────────
DEFAULT_OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
DEFAULT_MODEL      = "llama3.2-vision:11b"
DEFAULT_M1_URL     = "http://100.73.212.110:11434/api/generate"
SUPPORTED_EXTS     = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".dng", ".webp"}
SCRIPT_DIR         = Path(__file__).resolve().parent
REPO_ROOT          = SCRIPT_DIR.parent
PROMPT_FILE        = REPO_ROOT / "JCH_Inbox/03_PROJECTS/06_PHOTO_NATURE/keyword_prompt.md"
TAXONOMY_FILE      = REPO_ROOT / "JCH_Inbox/03_PROJECTS/06_PHOTO_NATURE/keyword_taxonomy.json"
CACHE_FILE         = REPO_ROOT / "JCH_Inbox/03_PROJECTS/06_PHOTO_NATURE/keyword_cache.json"
TEMPLATES_FILE     = REPO_ROOT / "JCH_Inbox/03_PROJECTS/06_PHOTO_NATURE/prompt_templates.json"

# ── Helpers ────────────────────────────────────────────────────────────────────
def load_prompt() -> str:
    if PROMPT_FILE.exists():
        return PROMPT_FILE.read_text(encoding="utf-8")
    print(f"⚠️  Prompt file not found: {PROMPT_FILE}")
    return "Describe this wildlife photograph in detail."

def load_template(name: str) -> Optional[dict]:
    if not TEMPLATES_FILE.exists():
        return None
    templates = json.loads(TEMPLATES_FILE.read_text())
    return templates.get(name)

def build_template_prompt(template: dict) -> str:
    system = template.get("system", "")
    prompt = template.get("prompt", "")
    return f"{system}\n\n{prompt}"

def load_cache() -> dict:
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text())
        except json.JSONDecodeError:
            return {}
    return {}

def save_cache(cache: dict) -> None:
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps(cache, indent=2, ensure_ascii=False))

def file_fingerprint(path: Path) -> str:
    """Quick fingerprint: size + mtime (avoids full hash on large files)."""
    stat = path.stat()
    return f"{path.name}_{stat.st_size}_{int(stat.st_mtime)}"

def encode_image(path: Path) -> str:
    """Read image file and return base64 data URI."""
    ext = path.suffix.lower()
    mime_map = {".jpg": "image/jpeg", ".jpeg": "image/jpeg",
                ".png": "image/png", ".webp": "image/webp",
                ".tif": "image/tiff", ".tiff": "image/tiff"}
    mime = mime_map.get(ext, "image/jpeg")
    data = path.read_bytes()
    return f"data:{mime};base64,{base64.b64encode(data).decode('ascii')}"

# ── Ollama Vision ─────────────────────────────────────────────────────────────
def ollama_vision(image_b64: str, prompt: str, model: str, endpoint: str,
                  timeout: int = 120) -> Optional[dict]:
    """Send image + prompt to Ollama vision model, return parsed JSON."""
    payload = {
        "model": model,
        "prompt": prompt,
        "images": [image_b64.split(",", 1)[1]],  # strip data URI header
        "stream": False,
        "format": "json",
        "options": {"temperature": 0.3, "num_predict": 1024}
    }
    try:
        resp = requests.post(endpoint, json=payload, timeout=timeout)
        resp.raise_for_status()
        body = resp.json()
        raw = body.get("response", "").strip()

        # Try to extract JSON from the response
        # Sometimes the model wraps JSON in markdown fences
        if raw.startswith("```"):
            lines = raw.split("\n")
            raw = "\n".join(lines[1:-1]) if len(lines) > 2 else raw

        # Find first { and last }
        start = raw.find("{")
        end = raw.rfind("}")
        if start >= 0 and end > start:
            raw = raw[start:end+1]

        return json.loads(raw)
    except (requests.RequestException, json.JSONDecodeError, KeyError) as e:
        print(f"  ⚠️  Model error: {e}")
        return None

# ── EXIF / IPTC writing ───────────────────────────────────────────────────────
def write_keywords(image_path: Path, keywords: list[str], dry_run: bool = False) -> bool:
    """Write keywords individually to IPTC/XMP (avoids semicolon parsing issues)."""
    if not keywords:
        return False

    cmd = ["exiftool", "-overwrite_original", "-preserve"]
    for kw in keywords:
        cmd.append(f"-IPTC:Keywords+={kw}")
        cmd.append(f"-XMP:Subject+={kw}")
        cmd.append(f"-XMP:HierarchicalSubject+={kw}")
    cmd.append(str(image_path))

    if dry_run:
        print(f"  [DRY-RUN] Would write {len(keywords)} keywords")
        return True

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if result.returncode != 0 and "image files updated" not in result.stdout:
            print(f"  ⚠️  exiftool warning: {result.stderr.strip()}")
            return False
        return True
    except subprocess.TimeoutExpired:
        print("  ⚠️  exiftool timed out")
        return False
    except Exception as e:
        print(f"  ⚠️  exiftool error: {e}")
        return False

def write_metadata(image_path: Path, headline: str, description: str,
                   keywords: list[str], dry_run: bool = False) -> bool:
    """Write headline, description, and keywords individually to IPTC/XMP."""
    cmd = ["exiftool", "-overwrite_original", "-preserve"]
    if headline:
        cmd.append(f"-IPTC:Headline={headline}")
        cmd.append(f"-XMP:Headline={headline}")
    if description:
        cmd.append(f"-IPTC:Caption-Abstract={description}")
        cmd.append(f"-XMP:Description={description}")
    for kw in (keywords or []):
        cmd.append(f"-IPTC:Keywords+={kw}")
        cmd.append(f"-XMP:Subject+={kw}")
        cmd.append(f"-XMP:HierarchicalSubject+={kw}")
    cmd.append(str(image_path))

    if dry_run:
        print(f"  [DRY-RUN] Headline: {headline[:80] if headline else '—'}")
        print(f"  [DRY-RUN] Description: {(description[:150] + '...') if description else '—'}")
        print(f"  [DRY-RUN] Keywords: {len(keywords) if keywords else 0} keywords")
        return True

    try:
        subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return True
    except Exception as e:
        print(f"  ⚠️  exiftool error: {e}")
        return False

def get_gps_keywords(image_path: Path) -> list[str]:
    """Extract GPS coordinates from EXIF and return keyword + Google Maps link."""
    try:
        r = subprocess.run(
            ['exiftool', '-GPSLatitude', '-GPSLongitude', '-n', '-s3', str(image_path)],
            capture_output=True, text=True, timeout=10
        )
        lines = [l.strip() for l in r.stdout.strip().splitlines() if l.strip()]
        if len(lines) >= 2 and lines[0] and lines[1]:
            lat = float(lines[0])
            lon = float(lines[1])
            # Format with 5 decimal places (~1m precision)
            lat_s = f"{lat:.5f}"
            lon_s = f"{lon:.5f}"
            maps_url = f"https://www.google.com/maps?q={lat_s},{lon_s}"
            return [
                f"GPS|{lat_s},{lon_s}",
                f"GPS|Google Maps|{maps_url}"
            ]
    except (ValueError, subprocess.TimeoutExpired, Exception):
        pass
    return []

# ── Response normalization ────────────────────────────────────────────────────
def load_taxonomy() -> set:
    """Load known species from taxonomy for validation."""
    if not TAXONOMY_FILE.exists():
        return set()
    try:
        tax = json.loads(TAXONOMY_FILE.read_text())
        known = set()
        for kingdom in tax.get("subjects", {}).values():
            for family, species_list in kingdom.items():
                known.update(species_list)
        return known
    except Exception:
        return set()

KNOWN_SPECIES = load_taxonomy()

def validate_subject(subject: str, confidence: float) -> str:
    """Validate a subject against taxonomy. Downgrade invented species."""
    parts = subject.split(".")
    if len(parts) < 3:
        return subject  # already at family level, keep it

    # Extract species name
    species = parts[-1]
    if species == "indéterminé":
        return subject  # model already said it's unsure

    # Check if species is in our taxonomy
    if species not in KNOWN_SPECIES:
        # Downgrade: keep kingdom.family but mark as indéterminé
        return f"{parts[0]}.{parts[1]}.indéterminé"

    # If confidence is low, downgrade too
    if confidence < 0.5:
        return f"{parts[0]}.{parts[1]}.indéterminé"

    return subject


def flatten_keywords(data: dict) -> list[str]:
    """Convert structured model output to flat IPTC keyword list with validation."""
    kws = []
    conf = data.get("confidence", 0.5)

    # Subjects — validate against taxonomy
    for s in data.get("subjects", []):
        validated = validate_subject(s, conf)
        if validated.startswith("faune."):
            kws.append(f"Faune|{validated.replace('faune.', '').replace('.', '|')}")
        elif validated.startswith("flore."):
            kws.append(f"Flore|{validated.replace('flore.', '').replace('.', '|')}")
        else:
            kws.append(validated)

    # Behavior
    for b in data.get("behavior", []):
        kws.append(f"Comportement|{b.replace('.', '|')}")

    # Season
    s = data.get("season")
    if s:
        val = s[0] if isinstance(s, list) else s
        kws.append(f"Saison|{str(val).capitalize()}")

    # Time
    t = data.get("time")
    if t:
        val = t[0] if isinstance(t, list) else t
        kws.append(f"Moment|{str(val).capitalize()}")

    # Lighting
    for l in data.get("lighting", []):
        kws.append(f"Lumière|{l.replace('_', ' ').capitalize()}")

    # Composition
    for c in data.get("composition", []):
        kws.append(f"Composition|{c.replace('_', ' ').capitalize()}")

    # Habitat
    h = data.get("habitat")
    if h:
        if isinstance(h, list):
            for hi in h:
                kws.append(f"Habitat|{str(hi).capitalize()}")
        else:
            kws.append(f"Habitat|{str(h).capitalize()}")

    # Technique
    for t in data.get("technique", []):
        kws.append(f"Technique|{t.replace('_', ' ').capitalize()}")

    # Mood
    m = data.get("mood")
    if m:
        val = m[0] if isinstance(m, list) else m
        kws.append(f"Ambiance|{val}")

    # Confidence tag
    if conf := data.get("confidence"):
        level = "Haute" if conf >= 0.7 else "Moyenne" if conf >= 0.4 else "Basse"
        kws.append(f"Auto|Confiance_{level}")

    return kws

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Auto-tag wildlife photos with local vision model (Ollama)")
    parser.add_argument("--input", required=True, help="Image file or directory")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help=f"Ollama vision model (default: {DEFAULT_MODEL})")
    parser.add_argument("--endpoint", default=DEFAULT_OLLAMA_URL,
                        help=f"Ollama API URL (default: {DEFAULT_OLLAMA_URL})")
    parser.add_argument("--m1", action="store_true",
                        help=f"Use M1 endpoint ({DEFAULT_M1_URL})")
    parser.add_argument("--dry-run", action="store_true",
                        help="Analyze but don't write keywords")
    parser.add_argument("--no-cache", action="store_true",
                        help="Ignore cache, re-analyze all images")
    parser.add_argument("--max-images", type=int, default=0,
                        help="Process at most N images (0 = all)")
    parser.add_argument("--verbose", "-v", action="store_true")
    parser.add_argument("--template", "-t", default=None,
                        help="Prompt template: classify, species, describe, print, arteon, stock, caption, full")
    parser.add_argument("--species-api", default=None,
                        help="External API for species ID: gemini (uses gemini-3.1-flash-lite, near-free)")
    args = parser.parse_args()

    # Resolve endpoint
    endpoint = DEFAULT_M1_URL if args.m1 else args.endpoint
    model = args.model

    print(f"🦉 Photo Keyworder — {model} @ {endpoint}")
    
    # Load template if specified
    template = None
    prompt = load_prompt()
    if args.template:
        template = load_template(args.template)
        if template:
            prompt = build_template_prompt(template)
            print(f"   📋 Template: {template['name']} ({args.template})")
        else:
            print(f"   ⚠️  Template '{args.template}' not found, using default")
    
    if not args.template:
        print(f"   {'DRY RUN — no changes' if args.dry_run else 'Writing IPTC + XMP keywords'}")

    # Gather images
    input_path = Path(args.input).expanduser().resolve()
    images = []
    if input_path.is_file():
        if input_path.suffix.lower() in SUPPORTED_EXTS:
            images.append(input_path)
    elif input_path.is_dir():
        for ext in SUPPORTED_EXTS:
            images.extend(sorted(input_path.rglob(f"*{ext}")))
        images.sort()
    else:
        sys.exit(f"❌ Input not found: {input_path}")

    if not images:
        sys.exit("❌ No supported images found.")

    print(f"   Found {len(images)} image(s)")

    if args.max_images > 0:
        images = images[:args.max_images]
        print(f"   Limited to {len(images)} image(s)")

    # Load cache & prompt
    cache = load_cache() if not args.no_cache else {}

    # Auto-enable full template when species-api is active (for richer metadata)
    use_full_metadata = args.species_api == "gemini"
    if use_full_metadata and not args.template:
        template = load_template("full")
        if template:
            prompt = build_template_prompt(template)
            print(f"   📋 Template: {template['name']} (auto pour species-api)")

    processed = 0
    tagged = 0
    errors = 0
    skipped_cached = 0

    t_start = time.monotonic()

    for img in images:
        fingerprint = file_fingerprint(img)

        # Check cache
        if not args.no_cache and fingerprint in cache:
            if args.verbose:
                print(f"  ⏭️  {img.name} (cached)")
            skipped_cached += 1
            processed += 1
            continue

        print(f"  🔍 {img.name} ... ", end="", flush=True)

        try:
            # Encode
            img_b64 = encode_image(img)

            # Send to model
            result = ollama_vision(img_b64, prompt, model, endpoint)
            if result is None:
                errors += 1
                print("❌ model error")
                continue

            if args.template:
                # Template mode: display result as-is
                display = json.dumps(result, ensure_ascii=False)
                if args.verbose:
                    print(f"\n     → {display[:300]}")
                print(f"✅ {display[:120]}")
                tagged += 1
                cache[fingerprint] = {
                    "file": img.name,
                    "template": args.template,
                    "result": result,
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
                }
            else:
                # Flatten to keywords
                keywords = [] if use_full_metadata else flatten_keywords(result)
                description = ""

                # Two-pass: species identification via Gemini
                species_info = None
                if args.species_api == "gemini":
                    try:
                        from inat_species import identify_species
                        species_info = identify_species(str(img))
                        if species_info and species_info.get("latin"):
                            latin = species_info["latin"]
                            sp_name = species_info.get("species", "")
                            sp_conf = species_info.get("confidence", 0)
                            # Inject Latin name + species into keywords
                            if sp_name and sp_name != "indéterminé":
                                keywords.insert(0, f"Faune|Espèce|{latin}")
                                keywords.insert(0, f"Faune|Espèce|{sp_name}")
                                print(f" 🧬 {sp_name} ({latin}) {sp_conf:.0%}", end="")
                    except Exception as e:
                        print(f" ⚠️ species API: {e}", end="")

                # Full metadata mode: extract headline + description + enrich keywords
                if use_full_metadata and not args.template:
                    headline = result.get("headline", "")
                    description = result.get("description", "")
                    # Add labels as keywords
                    for lb in result.get("labels", []):
                        label = lb.get("label", "")
                        conf_lb = lb.get("confidence", 0)
                        if conf_lb >= 0.7 and label:
                            keywords.append(f"Label|{label}")
                    # Add stock keywords
                    for kw in result.get("keywords", []):
                        if kw not in keywords:
                            keywords.append(kw)
                    # Add print recommendation
                    pr = result.get("print") or {}
                    if pr.get("paper"):
                        keywords.append(f"Print|{pr['paper']}")
                    # Add composition, lighting, habitat, technique, mood
                    comp = result.get("composition") or {}
                    for k, v in comp.items():
                        if v:
                            keywords.append(f"Composition|{str(v).replace('_',' ').capitalize()}")
                    light = result.get("lighting") or {}
                    for k, v in light.items():
                        if v:
                            keywords.append(f"Lumière|{str(v).replace('_',' ').capitalize()}")
                    if result.get("habitat"):
                        keywords.append(f"Habitat|{result['habitat'].capitalize()}")
                    for t in result.get("technique", []):
                        keywords.append(f"Technique|{str(t).replace('_',' ').capitalize()}")
                    if result.get("mood"):
                        keywords.append(f"Ambiance|{result['mood']}")
                    # Behavior
                    for b in result.get("behavior", []):
                        keywords.append(f"Comportement|{str(b).replace('.','|')}")
                    # ARTEON
                    ar = result.get("arteon") or {}
                    if ar.get("verdict"):
                        keywords.append(f"ARTEON|{ar['verdict'].upper()}|{ar.get('score','?')}/10")

                # GPS from EXIF
                gps_kws = get_gps_keywords(img)
                if gps_kws:
                    keywords.extend(gps_kws)
                    # Also add GPS to headline context
                    if use_full_metadata and gps_kws:
                        headline = result.get("headline", "")

                conf = result.get("confidence", 0)
                if args.verbose:
                    print(f"\n     → {json.dumps(result, ensure_ascii=False)[:200]}")

                if use_full_metadata and (headline or description):
                    ok = write_metadata(img, headline, description, keywords, dry_run=args.dry_run)
                else:
                    ok = write_keywords(img, keywords, dry_run=args.dry_run)

                if ok:
                    tagged += 1
                    meta = f" +headline +desc" if (headline or description) else ""
                    cache[fingerprint] = {
                        "file": img.name,
                        "keywords": keywords,
                        "confidence": conf,
                        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
                    }
                    print(f"✅ {len(keywords)} keywords (conf {conf:.0%})")
                if not ok:
                    errors += 1
                    print("❌ write error")

        except Exception as e:
            errors += 1
            print(f"❌ {e}")

        processed += 1

    elapsed = time.monotonic() - t_start

    # Save cache
    if not args.dry_run:
        save_cache(cache)

    # Summary
    print(f"\n{'─'*50}")
    print(f"  Images:    {len(images)}")
    print(f"  Tagged:    {tagged}")
    print(f"  Cached:    {skipped_cached}")
    print(f"  Errors:    {errors}")
    print(f"  Time:      {elapsed:.1f}s ({elapsed/max(processed,1):.1f}s/img)")
    if not args.dry_run and tagged > 0:
        print(f"  Keywords written to IPTC + XMP + HierarchicalSubject")
        print(f"  → Import into Lightroom: Metadata → Read Metadata from Files")
    print(f"{'─'*50}")


if __name__ == "__main__":
    main()