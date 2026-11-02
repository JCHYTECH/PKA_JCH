#!/usr/bin/env python3
"""
pka_state_snapshot.py — Snapshot d'état + détection de dérive
Dobby 🦉 — 2026-10-04 — Amélioration agentique #2

Deux fonctions :
1. Fraîcheur + dérive : scanne les State files et docs dérivées, flag les fichiers
   périmés (> 7 j) et les contradictions de statut (un même sujet « bloqué » dans
   un fichier vs « résolu » dans un autre).
2. Snapshot : génère une page d'état consolidée (projets, host, inbox, follow-ups)
   → `04_PILOTAGE_STRATEGIQUE/etat-snapshot.md`

Usage :
  python3 scripts/pka_state_snapshot.py --check    fraîcheur + dérive (stdout)
  python3 scripts/pka_state_snapshot.py --actions  top-3 prochaines actions
  python3 scripts/pka_state_snapshot.py --write    génère et écrit etat-snapshot.md
"""

import os
import re
import subprocess
import sys
from datetime import datetime

PKA_ROOT = os.path.expanduser("~/PKA_JCH")
STRAT = os.path.join(PKA_ROOT, "JCH_Inbox", "04_PILOTAGE_STRATEGIQUE")
SNAPSHOT_PATH = os.path.join(STRAT, "etat-snapshot.md")

STATE_FILES = [
    "etat-projets.md", "hardware-state.md", "decisions-actives.md",
    "priorites-actives.md", "risques-et-frottements.md",
    "roadmap-90-jours.md", "roadmap-long-terme.md",
]

DERIVED = [
    ("INDEX (TRAVELS)", os.path.join(PKA_ROOT, "JCH_Inbox/03_PROJECTS/07_TRAVELS/INDEX.md")),
    ("PREFERENCES (vanlife)", os.path.join(PKA_ROOT, "JCH_Inbox/03_PROJECTS/07_TRAVELS/vanlife/PREFERENCES.md")),
]

# Termes obsolètes qui ne devraient plus apparaître (dérive de modèle / ancien nom)
OBSOLETE = [
    ("Stylevan", "remplacé par Westfalia Kelsey (30/06/2026)"),
    ("Equinox", "ancien van — remplacé par Kelsey"),
]

NEG = ["bloqué", "bloquee", "en panne", "échec", "interrompu",
       "perdu", "deadlock", "failed", "crash"]
POS = ["résolu", "résolue", "réparé", "healthy", "boot ok", "fonctionne"]

TOPICS = ["rpi", "boot", "nvme", "haos", "zigbee", "wican", "lupo",
          "wildnexus", "arteon", "vetalyx", "iot", "nexus", "insectnet"]


def sh(cmd, timeout=20):
    try:
        return subprocess.run(cmd, shell=True, capture_output=True, text=True,
                              timeout=timeout).stdout.strip()
    except Exception:
        return ""


def read(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except Exception:
        return None


def file_age(path):
    """Extrait la date de dernière mise à jour du header, retourne (date_str, jours)."""
    txt = read(path)
    if txt is None:
        return None, None
    head = "\n".join(txt.splitlines()[:15])
    patterns = [
        r"[Dd]erni[èe]re mise [àa] jour[^:]*[:：][^0-9]*(\d{4}-\d{2}-\d{2})",
        r"last_updated\s*[:：]\s*(\d{4}-\d{2}-\d{2})",
        r"(\d{4}-\d{2}-\d{2})",
    ]
    for pat in patterns:
        m = re.search(pat, head)
        if m:
            d = datetime.strptime(m.group(1), "%Y-%m-%d")
            return m.group(1), (datetime.now() - d).days
    return None, None


def check_freshness():
    """Retourne [(source, path, date, age, niveau)] pour State + dérivés."""
    rows = []
    for name in STATE_FILES:
        p = os.path.join(STRAT, name)
        date, age = file_age(p)
        if date is None:
            rows.append((name, "date inconnue", None, "WARN"))
        else:
            lvl = "CRIT" if age > 30 else ("WARN" if age > 7 else "OK")
            rows.append((name, date, age, lvl))
    for name, p in DERIVED:
        date, age = file_age(p)
        if date is None:
            rows.append((name, "date inconnue", None, "WARN"))
        else:
            lvl = "CRIT" if age > 30 else ("WARN" if age > 7 else "OK")
            rows.append((name, date, age, lvl))
    return rows


def check_obsolete():
    """Détecte les références obsolètes dans State + dérivés."""
    hits = []
    paths = [(os.path.join(STRAT, n)) for n in STATE_FILES] + [p for _, p in DERIVED]
    for path in paths:
        txt = read(path)
        if not txt:
            continue
        for term, note in OBSOLETE:
            if re.search(term, txt, re.IGNORECASE):
                hits.append((os.path.basename(path), term, note))
    return hits


def check_contradictions():
    """Détecte un même sujet avec statut négatif ET positif (mot-clé sur la même ligne)."""
    flags = []
    paths = [(os.path.join(STRAT, n)) for n in STATE_FILES]
    for topic in TOPICS:
        neg_files = set()
        pos_files = set()
        for p in paths:
            txt = read(p)
            if not txt:
                continue
            for line in txt.splitlines():
                low = line.lower()
                if topic not in low:
                    continue
                for w in NEG:
                    if re.search(rf"\b{re.escape(w)}\b", low):
                        neg_files.add(os.path.basename(p))
                        break
                for w in POS:
                    if re.search(rf"\b{re.escape(w)}\b", low):
                        pos_files.add(os.path.basename(p))
                        break
        if neg_files and pos_files:
            flags.append((topic, sorted(neg_files), sorted(pos_files)))
    return flags


def check_host():
    """Réutilise pka_host_watch pour l'état hôte."""
    try:
        from pka_host_watch import check_disks, check_tm, check_cpu
        return check_disks() + check_tm() + check_cpu()
    except Exception:
        out = sh(f"python3 {os.path.join(PKA_ROOT, 'scripts/pka_host_watch.py')} --check")
        return [("host", "via subprocess", out, "OK")]


def check_inbox():
    inbox = os.path.join(PKA_ROOT, "JCH_Inbox", "00_INBOX")
    items = []
    if os.path.isdir(inbox):
        for f in sorted(os.listdir(inbox)):
            if f == ".DS_Store":
                continue
            full = os.path.join(inbox, f)
            items.append(f + ("/" if os.path.isdir(full) else ""))
    return items


def check_followups():
    db = os.path.join(PKA_ROOT, "TEAM", "team.db")
    if not os.path.exists(db):
        return []
    out = sh(f"sqlite3 '{db}' \"SELECT subject, due_date FROM follow_ups "
             f"WHERE due_date < date('now') AND status != 'done' ORDER BY due_date;\"")
    return [ln for ln in out.splitlines() if ln.strip()]


def check_next_actions():
    """Extrait les prochaines étapes de etat-projets.md, triées par priorité."""
    txt = read(os.path.join(STRAT, "etat-projets.md"))
    if not txt:
        return []
    actions = []
    for line in txt.splitlines():
        if not line.startswith("|"):
            continue
        parts = [p.strip() for p in line.split("|")][1:-1]
        if len(parts) < 5 or "Projet" in line or all(set(p) <= set("- ") for p in parts):
            continue
        projet = parts[1].replace("**", "").strip()
        statut = parts[2]
        next_step = parts[4]
        if "🔴" in statut:
            prio = 0
        elif "🔶" in statut:
            prio = 1
        elif "🟢" in statut:
            prio = 2
        else:
            prio = 3
        if prio < 3:
            actions.append((prio, projet, next_step, statut))
    actions.sort(key=lambda x: x[0])
    return actions


def snapshot_markdown(freshness, obsolete, contradictions, host, inbox, followups, actions):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [f"# État consolidé — {now}", ""]

    lines.append("## Prochaines actions (top)")
    if actions:
        for i, (prio, projet, next_step, statut) in enumerate(actions[:3], 1):
            lines.append(f"{i}. **{projet}** — {next_step}")
    else:
        lines.append("- (aucune extraite)")
    lines.append("")

    lines.append("## ⚠️ À surveiller")
    watch = []
    for kind, name, val, lvl in host:
        if lvl == "CRIT":
            watch.append(f"🔴 {name}: {val}")
    for name, date, age, lvl in freshness:
        if lvl == "CRIT":
            watch.append(f"🔴 State périmé : {name} ({age} j)")
    if obsolete:
        watch.append(f"🟡 {len(obsolete)} référence(s) obsolète(s)")
    if contradictions:
        watch.append(f"🔴 {len(contradictions)} contradiction(s) de statut")
    lines += [f"- {w}" for w in watch] if watch else ["- ✅ rien de critique"]
    lines.append("")

    lines.append("## Host (disque / Time Machine / CPU)")
    for kind, name, val, lvl in host:
        icon = {"OK": "✅", "WARN": "🟡", "CRIT": "🔴"}[lvl]
        lines.append(f"- {icon} {name}: {val}")
    lines.append("")

    lines.append("## Fraîcheur des State files")
    for name, date, age, lvl in freshness:
        icon = {"OK": "✅", "WARN": "🟡", "CRIT": "🔴"}[lvl]
        age_s = f"{age} j" if age is not None else date
        lines.append(f"- {icon} {name} — {date} ({age_s})")
    lines.append("")

    if obsolete or contradictions:
        lines.append("## ⚠️ Dérives détectées")
        for fname, term, note in obsolete:
            lines.append(f"- 🟡 Référence obsolète « {term} » dans {fname} ({note})")
        for topic, neg, pos in contradictions:
            lines.append(f"- 🔴 Contradiction « {topic} » : négatif dans {neg} vs positif dans {pos}")
        lines.append("")

    lines.append("## Inbox en attente")
    lines.append("- " + (", ".join(inbox) if inbox else "(vide)"))
    lines.append("")

    lines.append("## Follow-ups en retard")
    if followups:
        for fu in followups:
            lines.append(f"- {fu}")
    else:
        lines.append("- (aucun)")
    lines.append("")

    lines.append("> Généré par `pka_state_snapshot.py`. Lire ce fichier au lieu des 18 fichiers State.")
    return "\n".join(lines)


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--check"

    freshness = check_freshness()
    obsolete = check_obsolete()
    contradictions = check_contradictions()
    actions = check_next_actions()

    if mode == "--actions":
        print("=== Prochaines actions (top) ===")
        for i, (prio, projet, next_step, statut) in enumerate(actions[:3], 1):
            print(f"{i}. [{statut.strip()}] {projet} — {next_step}")
        return 0

    if mode == "--write":
        host = check_host()
        inbox = check_inbox()
        followups = check_followups()
        md = snapshot_markdown(freshness, obsolete, contradictions, host, inbox, followups, actions)
        with open(SNAPSHOT_PATH, "w", encoding="utf-8") as f:
            f.write(md)
        print(f"✅ Snapshot écrit : {SNAPSHOT_PATH}")
        print()
        print(md)
        return 0

    # --check (défaut) : fraîcheur + dérive seulement
    print("=== Fraîcheur State files ===")
    for name, date, age, lvl in freshness:
        icon = {"OK": "✅", "WARN": "🟡", "CRIT": "🔴"}[lvl]
        age_s = f"{age} j" if age is not None else date
        print(f"{icon} {name} — {date} ({age_s})")
    print()
    print("=== Références obsolètes ===")
    if obsolete:
        for fname, term, note in obsolete:
            print(f"🟡 « {term} » dans {fname} — {note}")
    else:
        print("✅ aucune")
    print()
    print("=== Contradictions de statut ===")
    if contradictions:
        for topic, neg, pos in contradictions:
            print(f"🔴 « {topic} » — négatif dans {neg} vs positif dans {pos}")
    else:
        print("✅ aucune")
    return 0


if __name__ == "__main__":
    sys.exit(main())
