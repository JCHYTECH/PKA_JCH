#!/usr/bin/env python3
"""
pka_quick_capture.py — Capture rapide d'une pensée brute dans l'inbox PKA.

Pattern inspiré de « I Replaced Apple Notes With AI » (Sanja, 2026) :
une pensée → inbox → Dobby la classe plus tard. Zéro friction.

Usage:
    pka_quick_capture.py "Penser à vérifier le prix du WiCAN Pro"
    pka_quick_capture.py "Idée WildLens : article sur les chants d'orthoptères"
    pka_quick_capture.py --project IOT "Commander silentblocs M3"
    pka_quick_capture.py --urgent "Lupo deadline 7 août — vérifier SD reçue"
    echo "une pensée" | pka_quick_capture.py --stdin

Le script :
1. Crée un fichier Markdown daté dans 00_INBOX/
2. Détecte automatiquement le projet si --project n'est pas spécifié
3. Ajoute le frontmatter minimal (date, type: quick-capture)
4. Option --urgent ajoute un flag priorité
"""

from __future__ import annotations

import argparse
import os
import sys
import re
from datetime import datetime
from pathlib import Path

PKABASE = Path(os.path.expanduser("~/PKA_JCH"))
INBOX_DIR = PKABASE / "JCH_Inbox" / "00_INBOX"

# Mots-clés → projet (détection automatique)
PROJECT_KEYWORDS = {
    "IOT": ["lupo", "rpi", "raspberry", "van", "vanlife", "zigbee", "home assistant", "ha ", "obd",
            "silentbloc", "can bus", "wican", "serre", "solaire", "batterie", "domotique"],
    "WILDNEXUS": ["wildnexus", "esp32", "fomo", "tinyml", "capteur", "mems", "lora", "bioacoustique",
                  "camera esp", "firmware", "bench loop", "sop", "ppk2"],
    "NEXUS_ACOUSTIC": ["acoustique", "orthoptère", "birdnet", "tweetybert", "insectset", "soundplot",
                       "spectrogram", "audio", "microphone", "enregistreur"],
    "PHOTO_NATURE": ["photo", "canon", "objectif", "raw", "rafale", "affût", "faune", "macro",
                     "trépied", "filtre", "sd card photo"],
    "PHOTO_AI_JURY": ["argus", "jury", "critique", "preset", "xmp", "lightroom"],
    "ARTEON": ["arteon", "wildlens", "boutique", "print", "tirage", "vente", "shop", "marque"],
    "AI_IT_TOOLS": ["script", "skill", "prompt", "automatis", "llm", "claude", "deepseek",
                    "modèle ia", "agent", "pka ", "dobby"],
    "VETALYX": ["vetalyx", "diagnostic", "vétérinaire", "ige", "allergie", "test rapide",
                "marque", "wipo", "dépôt"],
    "TRAVELS": ["voyage", "roadtrip", "camping", "bivouac", "kelsey", "westfalia", "ford",
                "park4night", "carte", "itinéraire"],
    "LEAFNET": ["leafnet", "ad623", "sonification", "plante", "xiao"],
    "InsectNet": ["insectnet", "insecte", "classification"],
}


def detect_project(text):
    """Détecte le projet le plus probable par mots-clés."""
    text_lower = text.lower()
    scores = {}
    for project, keywords in PROJECT_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        if score > 0:
            scores[project] = score

    if not scores:
        return "INBOX"  # fallback

    return max(scores, key=scores.get)


def create_capture_note(text, project=None, urgent=False):
    """Crée une note de capture rapide dans l'inbox."""
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d_%H%M%S")

    if project is None:
        project = detect_project(text)

    # Slug du contenu pour le nom de fichier
    slug = re.sub(r'[^a-z0-9]+', '-', text.lower()[:60].strip())
    slug = slug.strip('-')
    filename = f"quick-{timestamp}-{slug}.md" if slug else f"quick-{timestamp}.md"

    priority_header = "\npriority: urgent" if urgent else ""
    content = f"""---
date: {now.strftime('%Y-%m-%d')}
time: {now.strftime('%H:%M')}
type: quick-capture
project: {project}{priority_header}
---

# {text.strip()}

> Captured {now.strftime('%Y-%m-%d %H:%M')} — to be processed.
"""

    filepath = INBOX_DIR / filename
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return filepath, project


def main():
    parser = argparse.ArgumentParser(description="pka_quick_capture — Capture rapide d'une pensée")
    parser.add_argument("thought", nargs="?", help="La pensée à capturer")
    parser.add_argument("--project", "-p", help="Projet cible (auto-détecté si absent)")
    parser.add_argument("--urgent", "-u", action="store_true", help="Marquer comme urgent")
    parser.add_argument("--stdin", action="store_true", help="Lire depuis stdin")
    args = parser.parse_args()

    text = args.thought
    if args.stdin:
        text = sys.stdin.read().strip()
        if not text:
            print("❌ stdin vide.")
            return 1

    if not text:
        parser.print_help()
        return 1

    INBOX_DIR.mkdir(parents=True, exist_ok=True)

    filepath, project = create_capture_note(text, args.project, args.urgent)

    urgent_tag = "🔴 " if args.urgent else ""
    print(f"{urgent_tag}✅ Quick-capture → {project}")
    print(f"   {filepath}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
