#!/usr/bin/env python3
"""
pka_memory_prune.py — Nettoyage automatique de MEMORY.md

Archive les entrées > 90 jours vers wiki/archives/ avec résumé d'une ligne.
Implémente le maillon « Forget » de la boucle mémoire CoALA.

Usage:
    python3 scripts/pka_memory_prune.py --dry-run          # Simuler sans écrire
    python3 scripts/pka_memory_prune.py --days 60           # Seuil personnalisé (défaut: 90)
    python3 scripts/pka_memory_prune.py --force             # Exécuter sans confirmation
    python3 scripts/pka_memory_prune.py --json              # Sortie JSON pour automation
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path

PKA_ROOT = Path(__file__).resolve().parents[1]
MEMORY_PATH = PKA_ROOT / "MEMORY.md"
ARCHIVE_DIR = PKA_ROOT / "wiki" / "archives"

# Pattern: - [YYYY-MM-DD][tag] : fact
ENTRY_PATTERN = re.compile(
    r'^- \[(\d{4}-\d{2}-\d{2})\](\[[^\]]+\])?\s*:\s*(.+)$',
    re.MULTILINE
)

# Session header pattern
SESSION_HEADER = re.compile(r'^## Session (\d{4}-\d{2}-\d{2})')


def parse_memory_entries(content: str) -> list[dict]:
    """Parse MEMORY.md into structured entries with line numbers."""
    entries = []
    lines = content.split('\n')
    current_session = None

    for i, line in enumerate(lines):
        # Track session headers
        session_match = SESSION_HEADER.match(line.strip())
        if session_match:
            current_session = session_match.group(1)

        # Parse entries
        entry_match = ENTRY_PATTERN.match(line)
        if entry_match:
            entries.append({
                'date': entry_match.group(1),
                'tag': (entry_match.group(2) or '').strip('[]'),
                'fact': entry_match.group(3).strip(),
                'line': i,
                'raw': line,
                'session': current_session
            })

    return entries, lines


def is_stale(entry_date: str, threshold_days: int, reference_date: datetime = None) -> bool:
    """Check if an entry is older than threshold_days."""
    if reference_date is None:
        reference_date = datetime.now()

    try:
        entry_dt = datetime.strptime(entry_date, "%Y-%m-%d")
        age = (reference_date - entry_dt).days
        return age > threshold_days
    except ValueError:
        return False


def generate_summary(entries: list[dict]) -> str:
    """Generate a one-line-per-fact summary for the archive."""
    today = datetime.now().strftime("%Y-%m-%d")
    lines = [
        f"# Memory Archive — Generated {today}",
        f"",
        f"Summary of {len(entries)} pruned entries.",
        f"",
    ]

    # Group by session
    by_session = {}
    for e in entries:
        session = e.get('session') or e['date']
        if session not in by_session:
            by_session[session] = []
        by_session[session].append(e)

    for session in sorted(by_session.keys()):
        lines.append(f"## {session}")
        for e in by_session[session]:
            tag_str = f" [{e['tag']}]" if e['tag'] else ""
            lines.append(f"- [{e['date']}]{tag_str} : {e['fact']}")
        lines.append("")

    return '\n'.join(lines)


def prune_memory(content: str, stale_entries: list[dict], lines: list[str]) -> str:
    """Remove stale entries from MEMORY.md content."""
    stale_line_indices = {e['line'] for e in stale_entries}

    new_lines = []
    skip_next_blank = False

    for i, line in enumerate(lines):
        if i in stale_line_indices:
            skip_next_blank = True
            continue

        # If we just skipped a line and current is blank, skip it too
        if skip_next_blank and line.strip() == '':
            skip_next_blank = False
            continue
        skip_next_blank = False

        # Remove orphaned session headers (no entries remaining)
        if SESSION_HEADER.match(line.strip()):
            # Check if any non-stale entries remain for this session
            session_date = SESSION_HEADER.match(line.strip()).group(1)
            has_remaining = any(
                e for e in parse_memory_entries('\n'.join(lines))[0]
                if e.get('session') == session_date and e['line'] not in stale_line_indices
            )
            if not has_remaining:
                # Skip header and its following blank line
                if i + 1 < len(lines) and lines[i + 1].strip() == '':
                    skip_next_blank = True
                continue

        new_lines.append(line)

    # Clean up multiple consecutive blank lines
    result = []
    prev_blank = False
    for line in new_lines:
        is_blank = line.strip() == ''
        if is_blank and prev_blank:
            continue
        result.append(line)
        prev_blank = is_blank

    return '\n'.join(result)


def main():
    parser = argparse.ArgumentParser(
        description="pka_memory_prune — Archive les entrées MEMORY.md > 90 jours"
    )
    parser.add_argument("--days", type=int, default=90,
                        help="Seuil de rétention en jours (défaut: 90)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Simuler sans écrire")
    parser.add_argument("--force", action="store_true",
                        help="Exécuter sans confirmation")
    parser.add_argument("--json", action="store_true",
                        help="Sortie JSON")
    args = parser.parse_args()

    if not MEMORY_PATH.exists():
        print(f"❌ MEMORY.md introuvable à {MEMORY_PATH}", file=sys.stderr)
        sys.exit(1)

    content = MEMORY_PATH.read_text(encoding='utf-8')
    entries, lines = parse_memory_entries(content)

    if not entries:
        result = {"status": "empty", "message": "Aucune entrée trouvée dans MEMORY.md"}
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print("ℹ️  Aucune entrée trouvée dans MEMORY.md.")
        return

    stale = [e for e in entries if is_stale(e['date'], args.days)]

    if not stale:
        result = {
            "status": "clean",
            "total_entries": len(entries),
            "stale_entries": 0,
            "threshold_days": args.days,
            "oldest_entry": min(e['date'] for e in entries),
            "newest_entry": max(e['date'] for e in entries),
        }
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print(f"✅ Aucune entrée à archiver.")
            print(f"   {len(entries)} entrées totales — "
                  f"plus ancienne: {result['oldest_entry']}, "
                  f"plus récente: {result['newest_entry']}")
        return

    # Generate archive content
    archive_content = generate_summary(stale)
    archive_month = stale[0]['date'][:7]  # YYYY-MM
    archive_path = ARCHIVE_DIR / f"memory-archive-{archive_month}.md"

    # Prune
    pruned_content = prune_memory(content, stale, lines)

    # Stats
    dates = sorted(set(e['date'] for e in stale))
    result = {
        "status": "prune_ready",
        "total_entries": len(entries),
        "stale_entries": len(stale),
        "threshold_days": args.days,
        "stale_date_range": f"{dates[0]} → {dates[-1]}",
        "archive_path": str(archive_path.relative_to(PKA_ROOT)),
        "memory_size_before": len(content),
        "memory_size_after": len(pruned_content),
        "reduction_pct": round((1 - len(pruned_content) / max(len(content), 1)) * 100, 1),
    }

    if args.json:
        print(json.dumps(result, indent=2))
        if args.dry_run:
            return
    else:
        print(f"\n🧹 PRUNE — {len(stale)} entrées à archiver (>{args.days} jours)")
        print(f"   Période      : {result['stale_date_range']}")
        print(f"   Archive      : {result['archive_path']}")
        print(f"   MEMORY.md    : {result['memory_size_before']} → "
              f"{result['memory_size_after']} chars "
              f"(-{result['reduction_pct']}%)")
        print()

        if args.dry_run:
            print("🧪 DRY RUN — aucune modification effectuée.")
            return

    # Confirmation
    if not args.force and not args.json:
        response = input("Confirmer l'archivage ? [y/N] ").strip().lower()
        if response not in ('y', 'yes', 'oui'):
            print("Annulé.")
            return

    # Write archive
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    archive_path.write_text(archive_content, encoding='utf-8')

    # Write pruned MEMORY.md
    MEMORY_PATH.write_text(pruned_content, encoding='utf-8')

    if not args.json:
        print(f"\n✅ {len(stale)} entrées archivées → {result['archive_path']}")
        print(f"   MEMORY.md mis à jour ({result['memory_size_after']} chars)")


if __name__ == "__main__":
    main()
