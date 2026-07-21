#!/usr/bin/env python3
"""check_state_freshness.py — Vérifie la fraîcheur des fichiers State PKA_JCH.

Usage:
    python3 scripts/check_state_freshness.py          # Vérifie tout, sortie console
    python3 scripts/check_state_freshness.py --json   # Sortie JSON pour automation

Règles:
    - Tout fichier State > 7 jours depuis last_updated → WARNING
    - Tout fichier State > 14 jours → CRITICAL
    - Sortie formatée pour intégration dans system_check
"""

import os
import re
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

WORKSPACE = Path(os.environ.get("PKA_WORKSPACE", os.path.expanduser("~/PKA_JCH")))

# Fichiers State à vérifier — chemins relatifs au workspace
STATE_FILES = [
    "JCH_Inbox/04_PILOTAGE_STRATEGIQUE/hardware-state.md",
    "JCH_Inbox/04_PILOTAGE_STRATEGIQUE/etat-projets.md",
    "JCH_Inbox/04_PILOTAGE_STRATEGIQUE/decisions-actives.md",
    "JCH_Inbox/04_PILOTAGE_STRATEGIQUE/priorites-actives.md",
    "JCH_Inbox/04_PILOTAGE_STRATEGIQUE/risques-et-frottements.md",
    "JCH_Inbox/04_PILOTAGE_STRATEGIQUE/roadmap-90-jours.md",
    "JCH_Inbox/04_PILOTAGE_STRATEGIQUE/matrice-modeles.md",
    "docs/system/registre-achats.md",
]

# Registres procurement — glob dynamique (comme dans dobby-memory-bootstrap.md)
PROCUREMENT_PATTERNS = ["*procurement*.md", "*BOM*.md", "*shortlist*.md"]
PROCUREMENT_DIRS = ["JCH_Inbox/03_PROJECTS"]

# Registres procurement historiques — archivés, pas des State actifs
# Les fichiers datant de plus de PROCUREMENT_ARCHIVE_DAYS sans mise à jour sont exclus
PROCUREMENT_ARCHIVE_DAYS = 60

# Patterns d'exclusion pour les fichiers procurement historiques
PROCUREMENT_EXCLUDE_PATTERNS = [
    "*procurement-policy*",    # Politiques d'achat (doc de référence, pas State)
    "*procurement-pass*",      # Passes d'achat historiques
]

# Patterns pour extraire la date de dernière mise à jour
DATE_PATTERNS = [
    re.compile(r"Dernière mise à jour\s*:\s*(\d{4}-\d{2}-\d{2})"),
    re.compile(r"Dernière mise à jour\s*:\s*(\d{4}-\d{2}-\d{2})"),
    re.compile(r"last.updated[:\s]+(\d{4}-\d{2}-\d{2})", re.IGNORECASE),
    re.compile(r"Mis à jour le\s*:\s*(\d{4}-\d{2}-\d{2})"),
]


def extract_date(filepath: Path) -> datetime | None:
    """Extrait la date de dernière mise à jour d'un fichier."""
    try:
        content = filepath.read_text(encoding="utf-8")
    except (UnicodeDecodeError, FileNotFoundError, OSError):
        # Fallback: date de modification du fichier
        try:
            mtime = os.path.getmtime(filepath)
            return datetime.fromtimestamp(mtime)
        except (FileNotFoundError, OSError):
            return None

    try:
        for pattern in DATE_PATTERNS:
            match = pattern.search(content)
            if match:
                return datetime.strptime(match.group(1), "%Y-%m-%d")
        # Fallback: date de modification du fichier
        mtime = os.path.getmtime(filepath)
        return datetime.fromtimestamp(mtime)
    except (FileNotFoundError, OSError):
        return None


def check_freshness(json_output: bool = False) -> dict:
    """Vérifie la fraîcheur de tous les fichiers State + registres procurement."""
    now = datetime.now()
    results = {"ok": [], "warning": [], "critical": [], "missing": []}

    # Collecter tous les fichiers à vérifier : State statiques + procurement dynamiques
    all_files = list(STATE_FILES)

    for base_dir in PROCUREMENT_DIRS:
        base = WORKSPACE / base_dir
        if base.exists():
            for pattern in PROCUREMENT_PATTERNS:
                for f in base.rglob(pattern):
                    rel = f.relative_to(WORKSPACE)
                    rel_str = str(rel)

                    # Skip excluded patterns
                    excluded = False
                    for excl in PROCUREMENT_EXCLUDE_PATTERNS:
                        if f.match(excl):
                            excluded = True
                            break

                    # Skip procurement files older than archive threshold
                    if not excluded:
                        try:
                            mtime = os.path.getmtime(f)
                            age_days = (datetime.now() - datetime.fromtimestamp(mtime)).days
                            if age_days > PROCUREMENT_ARCHIVE_DAYS:
                                excluded = True
                        except OSError:
                            pass

                    if not excluded:
                        all_files.append(rel_str)

    for rel_path in all_files:
        filepath = WORKSPACE / rel_path
        date = extract_date(filepath)

        if date is None:
            results["missing"].append({"file": rel_path, "reason": "not found or unreadable"})
            continue

        age_days = (now - date).days

        entry = {
            "file": rel_path,
            "last_updated": date.strftime("%Y-%m-%d"),
            "age_days": age_days,
        }

        if age_days > 14:
            entry["level"] = "CRITICAL"
            results["critical"].append(entry)
        elif age_days > 7:
            entry["level"] = "WARNING"
            results["warning"].append(entry)
        else:
            entry["level"] = "OK"
            results["ok"].append(entry)

    return results


def print_console(results: dict):
    """Affiche les résultats en console."""
    total = sum(len(v) for v in results.values())
    critical = len(results["critical"])
    warning = len(results["warning"])
    ok_count = len(results["ok"])
    missing = len(results["missing"])

    print(f"State Freshness Check — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Files checked: {total} | OK: {ok_count} | WARNING: {warning} | CRITICAL: {critical} | MISSING: {missing}")
    print()

    if results["critical"]:
        print("🔴 CRITICAL (>14 days stale):")
        for e in results["critical"]:
            print(f"  {e['file']} — last updated {e['last_updated']} ({e['age_days']} days ago)")
        print()

    if results["warning"]:
        print("🟡 WARNING (>7 days stale):")
        for e in results["warning"]:
            print(f"  {e['file']} — last updated {e['last_updated']} ({e['age_days']} days ago)")
        print()

    if results["missing"]:
        print("⚪ MISSING:")
        for e in results["missing"]:
            print(f"  {e['file']} — {e['reason']}")
        print()

    if results["ok"]:
        print(f"✅ OK: {ok_count} files up to date")

    # Score global
    if critical > 0:
        print("\nStatus: RED")
    elif warning > 0:
        print("\nStatus: ORANGE")
    else:
        print("\nStatus: GREEN")


def main():
    json_output = "--json" in sys.argv
    results = check_freshness(json_output)

    if json_output:
        print(json.dumps(results, indent=2, default=str))
    else:
        print_console(results)

    # Exit code pour CI/automation
    if results["critical"]:
        sys.exit(2)
    elif results["warning"]:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
