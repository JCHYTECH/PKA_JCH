#!/usr/bin/env python3
"""
pka_date_scanner.py — Scan de dates dans les fichiers PKA et création auto de follow_ups.

Pattern inspiré de « I Replaced Apple Notes With AI » (Sanja, 2026) :
détecte automatiquement les dates d'expiration, deadlines, due dates
dans les fichiers texte et crée des follow_ups dans team.db.

Usage:
    pka_date_scanner.py --path JCH_Inbox/00_INBOX/       # scan un dossier
    pka_date_scanner.py --path TEAM_Inbox/ --dry-run     # preview sans écrire
    pka_date_scanner.py --all-projects                   # scan tous les projets actifs
    pka_date_scanner.py --file MEMORY.md                 # scan un fichier unique
    pka_date_scanner.py --vacuum                         # nettoie les follow_ups expirés
"""

from __future__ import annotations

import argparse
import re
import sqlite3
import sys
import os
from datetime import date, datetime, timedelta
from pathlib import Path

PKABASE = Path(os.path.expanduser("~/PKA_JCH"))
DB_PATH = PKABASE / "TEAM" / "team.db"

# Patterns de dates à scanner (FR + EN)
DATE_PATTERNS = [
    # Dates explicites ISO: 2026-07-13, 2026/07/13
    (re.compile(r'\b(20\d{2})[-/](0[1-9]|1[0-2])[-/](0[1-9]|[12]\d|3[01])\b'), "iso"),
    # Dates FR: 13 juillet 2026, 1er août 2026
    (re.compile(r'\b(\d{1,2})(?:er)?\s+(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s+(20\d{2})\b', re.IGNORECASE), "fr_long"),
    # Dates EN: July 13, 2026, Aug 1st 2026
    (re.compile(r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2})(?:st|nd|rd|th)?,?\s+(20\d{2})\b', re.IGNORECASE), "en_long"),
    # Dates FR compact: 13/07/2026, 13-07-2026
    (re.compile(r'\b(0[1-9]|[12]\d|3[01])[/-](0[1-9]|1[0-2])[/-](20\d{2})\b'), "fr_compact"),
]

# Mots-clés déclencheurs + fenêtre
TRIGGER_KEYWORDS = [
    (re.compile(r'\b(deadline|date\s+limite|échéance|due\s+date|expir(?:es|ation|y|e[ds]?)|à\s+faire\s+avant|à\s+commander\s+avant|livraison\s+(?:estimée|prévue)|arrivée\s+(?:prévue|estimée)|ETA)\b', re.IGNORECASE), "deadline"),
    (re.compile(r'\b(rapp?el|suivi|follow.?up|relance|check.?up|vérifier|review)\b', re.IGNORECASE), "followup"),
    (re.compile(r'\b(commande|order|achat|paiement|facture|invoice)\b', re.IGNORECASE), "order"),
]

FR_MONTHS = {
    "janvier": 1, "février": 2, "mars": 3, "avril": 4, "mai": 5, "juin": 6,
    "juillet": 7, "août": 8, "septembre": 9, "octobre": 10, "novembre": 11, "décembre": 12
}

EN_MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12
}


def parse_date(match, pattern_type):
    """Parse une date depuis un match regex selon le type de pattern."""
    try:
        if pattern_type == "iso":
            y, m, d = int(match.group(1)), int(match.group(2)), int(match.group(3))
            return date(y, m, d)
        elif pattern_type == "fr_long":
            d = int(match.group(1))
            m = FR_MONTHS.get(match.group(2).lower(), 0)
            y = int(match.group(3))
            return date(y, m, d) if m else None
        elif pattern_type == "en_long":
            m = EN_MONTHS.get(match.group(1).lower(), 0)
            d = int(match.group(2))
            y = int(match.group(3))
            return date(y, m, d) if m else None
        elif pattern_type == "fr_compact":
            d, m, y = int(match.group(1)), int(match.group(2)), int(match.group(3))
            return date(y, m, d)
    except (ValueError, IndexError):
        return None
    return None


def find_trigger_context(line, date_pos, window=80):
    """Cherche un mot-clé déclencheur dans la fenêtre autour d'une date."""
    start = max(0, date_pos - window)
    end = min(len(line), date_pos + window)
    context = line[start:end]
    for pattern, trigger_type in TRIGGER_KEYWORDS:
        if pattern.search(context):
            return trigger_type
    return None


def scan_file(filepath):
    """Scan un fichier pour les dates avec contexte déclencheur."""
    results = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
    except (IOError, OSError):
        return results

    for lineno, line in enumerate(lines, 1):
        for pattern, ptype in DATE_PATTERNS:
            for match in pattern.finditer(line):
                parsed = parse_date(match, ptype)
                if parsed and parsed >= date.today():
                    trigger = find_trigger_context(line, match.start())
                    if trigger or parsed <= date.today() + timedelta(days=90):
                        results.append({
                            "file": str(filepath),
                            "line": lineno,
                            "date": parsed.isoformat(),
                            "trigger": trigger or "date_only",
                            "snippet": line.strip()[:120],
                        })
    return results


def create_follow_up(conn, result, dry_run=False):
    """Crée un follow_up dans team.db."""
    due_date = result["date"]
    note = f"[auto] {result['trigger']}: {result['snippet'][:100]}"
    source = f"{Path(result['file']).name}:L{result['line']}"

    if dry_run:
        return True

    try:
        conn.execute(
            "INSERT INTO follow_ups (note, due_date, status, source, created_at) VALUES (?, ?, 'pending', ?, ?)",
            (note, due_date, source, datetime.now().isoformat())
        )
        conn.commit()
        return True
    except sqlite3.Error:
        return False


def scan_path(path, conn, dry_run=False, recursive=True):
    """Scan un fichier ou dossier."""
    total = 0
    created = 0
    path = Path(path)

    if path.is_file():
        results = scan_file(path)
        total = len(results)
        for r in results:
            if create_follow_up(conn, r, dry_run):
                created += 1
                if dry_run:
                    print(f"  📅 {r['date']} [{r['trigger']}] — {r['file']}:L{r['line']}")
                    print(f"     {r['snippet']}")
    elif path.is_dir():
        for f in sorted(path.rglob("*.md") if recursive else path.glob("*.md")):
            file_results = scan_file(f)
            for r in file_results:
                total += 1
                if create_follow_up(conn, r, dry_run):
                    created += 1
                    if dry_run:
                        print(f"  📅 {r['date']} [{r['trigger']}] — {r['file']}:L{r['line']}")
                        print(f"     {r['snippet']}")

    return total, created


def vacuum_follow_ups(conn, dry_run=False):
    """Supprime les follow_ups expirés (>30 jours après due_date)."""
    cutoff = (date.today() - timedelta(days=30)).isoformat()
    if dry_run:
        cur = conn.execute(
            "SELECT id, note, due_date FROM follow_ups WHERE due_date < ? AND status != 'done'",
            (cutoff,)
        )
        expired = cur.fetchall()
        print(f"  🧹 {len(expired)} follow_ups expirés:")
        for row in expired:
            print(f"     #{row[0]} {row[2]}: {row[1][:80]}")
        return len(expired), 0
    else:
        cur = conn.execute(
            "DELETE FROM follow_ups WHERE due_date < ? AND status != 'done'",
            (cutoff,)
        )
        conn.commit()
        return cur.rowcount, cur.rowcount


def init_db(conn):
    """Crée la table follow_ups si elle n'existe pas."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS follow_ups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            note TEXT,
            due_date TEXT,
            status TEXT DEFAULT 'pending',
            source TEXT,
            created_at TEXT
        )
    """)
    conn.commit()


def main():
    parser = argparse.ArgumentParser(description="pka_date_scanner — Auto-détection de dates → follow_ups")
    parser.add_argument("--path", help="Fichier ou dossier à scanner")
    parser.add_argument("--file", help="Fichier unique à scanner")
    parser.add_argument("--all-projects", action="store_true", help="Scanner tous les projets actifs")
    parser.add_argument("--dry-run", action="store_true", help="Preview sans écrire dans team.db")
    parser.add_argument("--vacuum", action="store_true", help="Nettoyer les follow_ups expirés")
    args = parser.parse_args()

    conn = sqlite3.connect(str(DB_PATH))
    init_db(conn)

    if args.vacuum:
        total, cleaned = vacuum_follow_ups(conn, dry_run=args.dry_run)
        action = "seraient nettoyés" if args.dry_run else "nettoyés"
        print(f"🧹 Vacuum terminé — {cleaned}/{total} follow_ups {action}")
        conn.close()
        return 0

    scan_targets = []
    if args.path:
        scan_targets.append(Path(args.path))
    if args.file:
        scan_targets.append(Path(args.file))
    if args.all_projects:
        projects_dir = PKABASE / "JCH_Inbox" / "03_PROJECTS"
        if projects_dir.exists():
            scan_targets.append(projects_dir)

    if not scan_targets:
        print("❌ Aucune cible spécifiée. Utiliser --path, --file ou --all-projects.")
        conn.close()
        return 1

    total = 0
    created = 0
    for target in scan_targets:
        if not target.exists():
            print(f"⚠️  Cible introuvable: {target}")
            continue
        t, c = scan_path(target, conn, dry_run=args.dry_run)
        total += t
        created += c

    if args.dry_run:
        print(f"\n📋 Dry run — {total} dates détectées, {created} follow_ups seraient créés.")
    else:
        print(f"\n✅ {created}/{total} follow_ups créés dans team.db.")

    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
