#!/usr/bin/env python3
"""Triage OCR gratuit des screenshots SITES/ — dédup + détection de listes.

Usage: python3 triage_ocr.py
  - OCR brut -> _local/decouvertes-ocr/<stem>.txt
  - Résumé groupé sur stdout (doublons / listes / nouveaux)
"""
import json
import re
import subprocess
import unicodedata
from pathlib import Path

PKA_ROOT = Path(__file__).resolve().parents[2]
BASE = PKA_ROOT / "JCH_Inbox/03_PROJECTS/07_TRAVELS/pka-decouvertes"
SITES = PKA_ROOT / "JCH_Inbox/00_INBOX/SITES"
OCR_OUT = PKA_ROOT / "_local/decouvertes-ocr"
OCR_OUT.mkdir(parents=True, exist_ok=True)


def norm(s):
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", " ", s)
    return " ".join(s.split())


# 1. Index des lieux déjà traités
known = {}
for p in (BASE / "data").glob("*.json"):
    try:
        d = json.loads(p.read_text(encoding="utf-8"))
        nm = d.get("nom_lieu") or p.stem
        known[norm(nm)] = nm
    except Exception:
        pass
for p in (BASE / "validated_places").glob("*.md"):
    try:
        txt = p.read_text(encoding="utf-8")
        m = re.search(r"^nom_lieu:\s*(.+)$", txt, re.M)
        nm = m.group(1).strip() if m else p.stem
        known[norm(nm)] = nm
    except Exception:
        pass

# 2. OCR + classification
images = sorted(f for f in SITES.glob("*") if f.suffix.lower() in {".jpeg", ".jpg", ".png"})
rows = []
for img in images:
    try:
        out = subprocess.run(
            ["tesseract", str(img), "stdout", "-l", "eng"],
            capture_output=True, text=True, timeout=30,
        )
        text = out.stdout.strip()
    except Exception:
        text = ""
    (OCR_OUT / (img.stem + ".txt")).write_text(text, encoding="utf-8")
    t = norm(text)
    hits = [dn for kn, dn in known.items() if len(kn) >= 4 and kn in t]
    numbered = len(re.findall(r"\b\d{1,3}[.)]\s+", text))
    is_list = numbered >= 3
    snip = " ".join(text.split())[:110]
    rows.append((img.name, hits, is_list, snip))

dup = [r for r in rows if r[1]]
lst = [r for r in rows if not r[1] and r[2]]
new = [r for r in rows if not r[1] and not r[2]]

print(f"TOTAL {len(rows)} | doublons {len(dup)} | listes {len(lst)} | nouveaux {len(new)}")
print(f"index lieux connus: {len(known)}")
print()
print("=== DOUBLONS (match lieu connu) ===")
for name, hits, _, snip in dup:
    print(f"  {name}  ->  {', '.join(hits)}")
    print(f"      {snip}")
print()
print("=== LISTES (numérotation détectée) ===")
for name, _, _, snip in lst:
    print(f"  {name}")
    print(f"      {snip}")
print()
print("=== NOUVEAUX ===")
for name, _, _, snip in new:
    print(f"  {name}  ::  {snip}")
