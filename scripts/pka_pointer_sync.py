#!/usr/bin/env python3
"""
PKA Pointer Sync — synchronise les fichiers pointeurs PKA entre eux.

Détecte les dérives entre :
  - AGENTS.md, CLAUDE.md, DEEPSEEK.md, GEMINI.md, QWEN.md, ADAPTER-PROMPT.md
  - team.db (source de vérité pour le roster)
  - JCH_Inbox/00_INBOX/ (source de vérité pour l'inbox)

Usage:
  python3 scripts/pka_pointer_sync.py          # détecte les dérives (dry-run)
  python3 scripts/pka_pointer_sync.py --fix    # corrige automatiquement
  python3 scripts/pka_pointer_sync.py --diff   # montre les diffs

Part of PKA Memory Layer — docs/system/pka-memory-layer.md
"""

import os
import re
import sqlite3
import sys
from datetime import datetime

# ─── Configuration ───────────────────────────────────────────────

PKA_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(PKA_ROOT, "TEAM", "team.db")
INBOX_PATH = os.path.join(PKA_ROOT, "JCH_Inbox", "00_INBOX")
PROJECTS_PATH = os.path.join(PKA_ROOT, "JCH_Inbox", "03_PROJECTS")

POINTER_FILES = [
    "AGENTS.md",
    "CLAUDE.md",
    "DEEPSEEK.md",
    "GEMINI.md",
    "QWEN.md",
    "ADAPTER-PROMPT.md",
]

# ─── Sources de vérité ───────────────────────────────────────────

def get_actual_team_count():
    """Lit le nombre réel de membres depuis team.db."""
    conn = sqlite3.connect(DB_PATH)
    count = conn.execute(
        "SELECT COUNT(*) FROM members WHERE status = 'active'"
    ).fetchone()[0]
    conn.close()
    return count  # inclut Dobby


def get_actual_specialist_names():
    """Lit la liste des spécialistes actifs (hors Dobby)."""
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT name FROM members WHERE status = 'active' AND name != 'Dobby' ORDER BY id"
    ).fetchall()
    conn.close()
    return [r[0] for r in rows]


def get_actual_inbox_count():
    """Compte les éléments dans l'inbox."""
    if not os.path.isdir(INBOX_PATH):
        return 0
    items = [f for f in os.listdir(INBOX_PATH)
             if not f.startswith('.') and f != '.DS_Store']
    return len(items)


def get_actual_projects():
    """Liste les projets actifs."""
    if not os.path.isdir(PROJECTS_PATH):
        return []
    dirs = [d for d in os.listdir(PROJECTS_PATH)
            if os.path.isdir(os.path.join(PROJECTS_PATH, d))
            and not d.startswith('.') and not d.startswith('_')]
    return sorted(dirs)


# ─── Détection de dérive ─────────────────────────────────────────

def check_specialist_count(filepath, total_count):
    """Vérifie le nombre de membres/spécialistes dans le fichier.
    
    Args:
        total_count: nombre total de membres (incluant Dobby)
    """
    with open(filepath) as f:
        content = f.read()

    issues = []
    specialist_count = total_count - 1  # hors Dobby

    # Pattern 1: "The N specialists"
    match = re.search(r'The (\d+) specialists', content)
    if match and int(match.group(1)) != specialist_count:
        issues.append({
            "file": os.path.basename(filepath),
            "field": "specialist_list_count",
            "expected": specialist_count,
            "found": int(match.group(1)),
            "line": content[:match.start()].count('\n') + 1
        })

    # Pattern 2: "N membres actifs — M spécialistes + Dobby"
    expected_text = f"{total_count} membres actifs — {specialist_count} spécialistes + Dobby"
    for m in re.finditer(r'(\d+) membres actifs — (\d+) spécialistes \+ Dobby', content):
        if m.group(0) != expected_text:
            issues.append({
                "file": os.path.basename(filepath),
                "field": "team_count",
                "expected": expected_text,
                "found": m.group(0),
                "line": content[:m.start()].count('\n') + 1
            })

    return issues


def check_regle_adresse(filepath):
    """Vérifie la présence de la RÈGLE D'ADRESSE."""
    with open(filepath) as f:
        content = f.read()

    if "RÈGLE D'ADRESSE" not in content:
        return [{
            "file": os.path.basename(filepath),
            "field": "regle_adresse",
            "expected": "présente",
            "found": "ABSENTE",
            "line": 0
        }]
    return []


def check_specialist_names(filepath, actual_names):
    """Vérifie que tous les spécialistes sont listés."""
    with open(filepath) as f:
        content = f.read()

    missing = []
    for name in actual_names:
        if name not in content:
            missing.append(name)

    if missing:
        return [{
            "file": os.path.basename(filepath),
            "field": "specialist_names",
            "expected": f"tous les {len(actual_names)}",
            "found": f"manquants: {', '.join(missing)}",
            "line": 0
        }]
    return []


def check_graphify(filepath):
    """Vérifie la présence de la section graphify."""
    with open(filepath) as f:
        content = f.read()

    if "graphify" not in content.lower() and "ADAPTER" not in filepath:
        return [{
            "file": os.path.basename(filepath),
            "field": "graphify_section",
            "expected": "présente",
            "found": "ABSENTE",
            "line": 0
        }]
    return []


# ─── Correction ───────────────────────────────────────────────────

def fix_specialist_count(filepath, total_count):
    """Corrige le nombre de spécialistes.
    
    Args:
        total_count: nombre total de membres (incluant Dobby)
    """
    specialist_count = total_count - 1
    with open(filepath) as f:
        content = f.read()

    modified = False

    # Fix "The N specialists"
    new_content = re.sub(
        r'The \d+ specialists',
        f'The {specialist_count} specialists',
        content
    )
    if new_content != content:
        modified = True
        content = new_content

    # Fix "N membres actifs — M spécialistes + Dobby"
    expected = f"{total_count} membres actifs — {specialist_count} spécialistes + Dobby"
    new_content = re.sub(
        r'\d+ membres actifs — \d+ spécialistes \+ Dobby',
        expected,
        content
    )
    if new_content != content:
        modified = True
        content = new_content

    if modified:
        with open(filepath, 'w') as f:
            f.write(content)
        return True
    return False


def fix_specialist_names(filepath, actual_names):
    """Ajoute les spécialistes manquants dans la liste."""
    with open(filepath) as f:
        content = f.read()

    # Cherche la liste entre parenthèses
    pattern = r'\((Bouvier[^)]+)\)'
    match = re.search(pattern, content)
    if not match:
        return False

    old_list = match.group(1)
    # Reconstruit la liste dans l'ordre canonique
    new_list = ', '.join(actual_names)
    new_content = content.replace(old_list, new_list)
    new_content = re.sub(
        r'The \d+ specialists',
        f'The {len(actual_names)} specialists',
        new_content
    )

    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        return True
    return False


def add_regle_adresse(filepath):
    """Ajoute la RÈGLE D'ADRESSE si absente."""
    with open(filepath) as f:
        content = f.read()

    if "RÈGLE D'ADRESSE" in content:
        return False

    rule = '\n**RÈGLE D\'ADRESSE — Toute réponse commence par « JC, » ou « JC — »** — Dobby s\'adresse directement à Jean-Claude, pas de manière impersonnelle. Pas de réponse qui commence par un titre, un emoji seul, ou du texte sans interpellation. Cette règle s\'applique à tous les modèles (DeepSeek, Qwen, Claude, Gemini).\n'

    # Pour CLAUDE.md, ajoute dans la table des règles
    if "CLAUDE.md" in filepath:
        if "| **Adresse**" not in content:
            content = content.replace(
                "| **Language** | Match the language",
                "| **Adresse** | **RÈGLE D'ADRESSE — Toute réponse commence par « JC, » ou « JC — »** — Dobby s'adresse directement à Jean-Claude, pas de manière impersonnelle. |\n| **Language** | Match the language"
            )
    else:
        # Pour les autres fichiers, après "Match the language"
        content = content.replace(
            "Match the language JCH uses in each message (FR/EN).",
            f"Match the language JCH uses in each message (FR/EN).\n{rule}"
        )

    with open(filepath, 'w') as f:
        f.write(content)
    return True


# ─── Main ─────────────────────────────────────────────────────────

def audit():
    """Audit complet — retourne toutes les dérives."""
    actual_count = get_actual_team_count()
    actual_names = get_actual_specialist_names()
    actual_inbox = get_actual_inbox_count()
    actual_projects = get_actual_projects()

    all_issues = []

    print(f"📊 État réel : {actual_count} membres ({len(actual_names)} spécialistes + Dobby)")
    print(f"📥 Inbox : {actual_inbox} éléments")
    print(f"📁 Projets : {', '.join(actual_projects[:5])}...")
    print()

    for fname in POINTER_FILES:
        fpath = os.path.join(PKA_ROOT, fname)
        if not os.path.exists(fpath):
            all_issues.append({
                "file": fname, "field": "existence",
                "expected": "présent", "found": "FICHIER MANQUANT", "line": 0
            })
            continue

        all_issues.extend(check_specialist_count(fpath, actual_count))  # total incluant Dobby
        all_issues.extend(check_specialist_names(fpath, actual_names))
        all_issues.extend(check_regle_adresse(fpath))
        if "ADAPTER" not in fname:
            all_issues.extend(check_graphify(fpath))

    return all_issues, actual_count, actual_names


def fix_all(actual_count, actual_names):
    """Corrige toutes les dérives."""
    fixed = 0
    for fname in POINTER_FILES:
        fpath = os.path.join(PKA_ROOT, fname)
        if not os.path.exists(fpath):
            print(f"⚠️  {fname} introuvable — ignoré")
            continue

        if fix_specialist_count(fpath, actual_count):  # total incluant Dobby
            print(f"🔧 {fname} : specialist count corrigé")
            fixed += 1
        if fix_specialist_names(fpath, actual_names):
            print(f"🔧 {fname} : liste spécialistes mise à jour")
            fixed += 1
        if add_regle_adresse(fpath):
            print(f"🔧 {fname} : RÈGLE D'ADRESSE ajoutée")
            fixed += 1

    return fixed


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="PKA Pointer Sync")
    parser.add_argument("--fix", action="store_true", help="Corriger automatiquement")
    parser.add_argument("--diff", action="store_true", help="Mode diff (équivalent à dry-run)")
    args = parser.parse_args()

    issues, actual_count, actual_names = audit()

    if not issues:
        print("✅ Tous les pointeurs sont synchronisés.")
        sys.exit(0)

    print(f"🔍 {len(issues)} dérive(s) détectée(s) :\n")
    for i, issue in enumerate(issues, 1):
        icon = "🔴" if issue["field"] in ("specialist_list_count", "team_count", "regle_adresse") else "🟡"
        print(f"  {i}. {icon} [{issue['file']}] {issue['field']}")
        print(f"     Attendu : {issue['expected']}")
        print(f"     Trouvé  : {issue['found']}")
        if issue.get("line"):
            print(f"     Ligne    : {issue['line']}")
        print()

    if args.fix:
        print("🔧 Correction en cours...\n")
        fixed = fix_all(actual_count, actual_names)
        print(f"\n✅ {fixed} correction(s) appliquée(s).")

        # Re-vérifie
        remaining, _, _ = audit()
        if remaining:
            print(f"⚠️  {len(remaining)} dérive(s) persistante(s) — vérification manuelle nécessaire.")
        else:
            print("✅ Tous les pointeurs sont maintenant synchronisés.")
    else:
        print("💡 Pour corriger : python3 scripts/pka_pointer_sync.py --fix")
