#!/usr/bin/env python3
"""Auto-validation systématique des fiches DÉCOUVERTES.

Déplace toutes les drafts vers validated_places/ (idempotent, no-clobber).
Le status du frontmatter est conservé — `needs_review` reste une étiquette
informative, plus de relecture manuelle systématique (décision JC 2026-09-21).

Usage :
  python3 auto_validate.py            # tout valider
  python3 auto_validate.py --dry-run  # aperçu sans déplacement
"""
import argparse
import re
import shutil
from collections import Counter
from pathlib import Path

PKA_ROOT = Path(__file__).resolve().parents[2]
BASE = PKA_ROOT / "JCH_Inbox/03_PROJECTS/07_TRAVELS/pka-decouvertes"
DRAFTS = BASE / "drafts"
VALIDATED = BASE / "validated_places"

VALIDATED.mkdir(parents=True, exist_ok=True)


def status_of(path: Path) -> str:
    m = re.search(r"^status:\s*(.+)$", path.read_text(), re.M)
    return m.group(1).strip().strip('"\'') if m else "(none)"


def main() -> None:
    ap = argparse.ArgumentParser(description="Auto-validate DÉCOUVERTES drafts")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    files = sorted(DRAFTS.glob("*.md"))
    moved = 0
    skipped = []
    by_status = Counter()

    for f in files:
        st = status_of(f)
        by_status[st] += 1
        dst = VALIDATED / f.name
        if dst.exists():
            skipped.append(f.name)
            continue
        if not args.dry_run:
            shutil.move(str(f), str(dst))
        moved += 1

    verb = "seraient validées" if args.dry_run else "validées"
    print(f"drafts: {len(files)}")
    print(f"{verb}: {moved}")
    print(f"déjà présentes (skip): {len(skipped)}")
    print("breakdown par status:", dict(by_status))
    if skipped:
        print("skip (déjà en validated_places):")
        for s in skipped:
            print("  ", s)


if __name__ == "__main__":
    main()
