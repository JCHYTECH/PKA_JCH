#!/usr/bin/env python3
"""
pka_host_watch.py — Surveillance santé de la machine hôte (M5)
Dobby 🦉 — 2026-10-04 — Amélioration agentique #1 (host-watch)

Contrôles :
1. Espace disque des volumes clés (Data, PKA_TimeMachine, JCH_SMALL)
2. Time Machine : dernière sauvegarde, sauvegardes interrompues, backupd bloqué
3. Processus anormalement gourmands en CPU (> 90 %)

Usage :
  python3 scripts/pka_host_watch.py --check   (défaut) affiche le rapport
  python3 scripts/pka_host_watch.py --alert   alerte si CRIT (fichier + notification)

Dépendances : stdlib uniquement (subprocess, shutil, os).
"""

import os
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone

PKA_ROOT = os.path.expanduser("~/PKA_JCH")
LOG = os.path.join(PKA_ROOT, "_local", "logs", "pka-host-watch.log")

VOLUMES = [
    ("Data (système)", "/System/Volumes/Data"),
    ("PKA_TimeMachine", "/Volumes/PKA_TimeMachine"),
    ("JCH_SMALL", "/Volumes/JCH_SMALL"),
]


def sh(cmd, timeout=25):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
        return r.stdout.strip()
    except Exception as e:
        return f"ERR:{e}"


def check_disks():
    rows = []
    for name, path in VOLUMES:
        try:
            u = shutil.disk_usage(path)
        except OSError:
            continue  # non monté
        pct = u.used / u.total * 100
        free_gb = u.free / (1024 ** 3)
        if pct > 95 or free_gb < 5:
            lvl = "CRIT"
        elif pct > 90 or free_gb < 10:
            lvl = "WARN"
        else:
            lvl = "OK"
        rows.append(("disque", name, f"{pct:.0f}% utilisés ({free_gb:.0f} Go libres)", lvl))
    return rows


def check_tm():
    rows = []
    latest = sh("tmutil latestbackup")
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})-\d{6}\.backup", latest)
    if m:
        d = datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        age = (datetime.now() - d).days
        lvl = "CRIT" if age > 14 else ("WARN" if age > 7 else "OK")
        rows.append(("tm", "Dernière sauvegarde",
                     f"{m.group(1)}-{m.group(2)}-{m.group(3)} ({age} j)", lvl))
    else:
        rows.append(("tm", "Dernière sauvegarde", "inconnue / inaccessible", "WARN"))

    dest = "/Volumes/PKA_TimeMachine"
    if os.path.isdir(dest):
        intr = [f for f in os.listdir(dest) if f.endswith(".interrupted")]
        if intr:
            rows.append(("tm", "Sauvegardes interrompues", str(len(intr)), "WARN"))

    for line in sh("ps -Ao pid=,pcpu=,comm= | grep backupd | grep -v grep").splitlines():
        parts = line.split(None, 2)
        if len(parts) >= 2:
            try:
                pcpu = float(parts[1])
            except ValueError:
                continue
            if pcpu > 90:
                rows.append(("tm", "backupd bloqué", f"PID {parts[0]} à {pcpu:.0f}% CPU", "CRIT"))
    return rows


def check_cpu():
    rows = []
    for line in sh("ps -Ao pid=,pcpu=,comm=").splitlines():
        parts = line.split(None, 2)
        if len(parts) < 3:
            continue
        try:
            pcpu = float(parts[1])
        except ValueError:
            continue
        if pcpu > 90:
            rows.append(("cpu", f"Processus {parts[2]}", f"PID {parts[0]} à {pcpu:.0f}%", "CRIT"))
    return rows


def log(msg):
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG, "a") as f:
        f.write(f"[{datetime.now(timezone.utc).isoformat()}] {msg}\n")


def notify(title, body):
    try:
        subprocess.run(
            ["osascript", "-e",
             f'display notification "{body}" with title "{title}" sound name "Basso"'],
            check=False, timeout=10,
        )
    except Exception:
        pass


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--check"
    all_rows = check_disks() + check_tm() + check_cpu()
    crits = [r for r in all_rows if r[-1] == "CRIT"]
    warns = [r for r in all_rows if r[-1] == "WARN"]

    lines = []
    for kind, name, val, lvl in all_rows:
        icon = {"OK": "✅", "WARN": "🟡", "CRIT": "🔴"}[lvl]
        lines.append(f"{icon} [{kind}] {name}: {val}")
    report = "\n".join(lines)
    print(report)
    log(f"mode={mode} CRIT={len(crits)} WARN={len(warns)}")

    if mode == "--alert" and crits:
        os.makedirs(os.path.join(PKA_ROOT, "TEAM_Inbox"), exist_ok=True)
        p = os.path.join(PKA_ROOT, "TEAM_Inbox",
                         f"{datetime.now().strftime('%Y-%m-%d')}_dobby_host-watch-alert.md")
        with open(p, "w") as f:
            f.write(f"# 🖥️ Alerte santé hôte — {datetime.now().strftime('%d/%m/%Y')}\n\n")
            for kind, name, val, lvl in crits:
                f.write(f"- **[{kind}] {name}** : {val}\n")
            f.write("\n> À traiter en priorité.\n")
        notify("🖥️ PKA Host-Watch", f"{len(crits)} alerte(s) critique(s)")
        print(f"\n🔔 Alerte écrite : {p}")
        return 1

    if crits:
        print(f"\n🔔 {len(crits)} CRIT (mode --check → pas de notification). Lancez --alert pour notifier.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
