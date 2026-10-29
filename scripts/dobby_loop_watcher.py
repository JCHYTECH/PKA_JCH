#!/usr/bin/env python3
"""
dobby_loop_watcher.py  🦉  — Détecte les nouveaux commits et déclenche les loops.

Scanne `git log` depuis le dernier check, compare les fichiers modifiés
avec les briefs actifs (auto_review, benchmark_loop, seo_loop, etc.),
et écrit des triggers dans `team.db` pour que Dobby les traite au
prochain démarrage.

Usage :
    python3 scripts/dobby_loop_watcher.py           # check unique
    python3 scripts/dobby_loop_watcher.py --daemon  # boucle infinie (pour cron)
"""

import json
import os
import re
import sqlite3
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


# ── CONFIG ──────────────────────────────────────────────────────────
PKA_DIR = Path(__file__).resolve().parent.parent
DB_PATH = PKA_DIR / "TEAM" / "team.db"
BRIEFS_DIR = PKA_DIR / "TEAM_Inbox"
STATE_FILE = PKA_DIR / "_local" / "loop_watcher_state.json"
CHECK_INTERVAL = 300  # secondes entre chaque scan (mode daemon)

# Mapping : flag dans le brief → loop_type
LOOP_FLAGS = {
    "auto_review": "forge-loop",
    "benchmark_loop": "wildnexus-benchmark-loop",
    "edge_ai_loop": "edge-ai-loop",
    "seo_loop": "seo-loop",
    "sigma_loop": "sigma-loop",
    "bench_loop": "bench-loop",
}


# ── STATE ───────────────────────────────────────────────────────────
def load_state() -> dict:
    if STATE_FILE.is_file():
        try:
            return json.loads(STATE_FILE.read_text())
        except (json.JSONDecodeError, OSError):
            pass
    return {"last_commit": None, "last_check": None}


def save_state(state: dict):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))


# ── GIT ─────────────────────────────────────────────────────────────
def get_new_commits(since_commit: str | None) -> list[dict]:
    """Récupère les commits depuis `since_commit` (exclus) jusqu'à HEAD."""
    if since_commit:
        try:
            output = subprocess.check_output(
                ["git", "log", f"{since_commit}..HEAD", "--format=%H|%an|%s"],
                cwd=PKA_DIR,
                text=True,
            )
        except subprocess.CalledProcessError:
            return []
    else:
        # Premier run : prend juste le dernier commit
        try:
            output = subprocess.check_output(
                ["git", "log", "-1", "--format=%H|%an|%s"],
                cwd=PKA_DIR,
                text=True,
            )
        except subprocess.CalledProcessError:
            return []

    commits = []
    for line in output.strip().split("\n"):
        if not line:
            continue
        parts = line.split("|", 2)
        if len(parts) == 3:
            commits.append({
                "hash": parts[0],
                "author": parts[1],
                "subject": parts[2],
            })
    return commits


def get_changed_files(commit_hash: str) -> list[str]:
    """Retourne la liste des fichiers modifiés par un commit."""
    try:
        output = subprocess.check_output(
            ["git", "diff-tree", "--no-commit-id", "--name-only", "-r", commit_hash],
            cwd=PKA_DIR,
            text=True,
        )
        return [f.strip() for f in output.strip().split("\n") if f.strip()]
    except subprocess.CalledProcessError:
        return []


# ── BRIEFS ───────────────────────────────────────────────────────────
def find_active_loop_briefs() -> list[dict]:
    """Trouve tous les briefs dans TEAM_Inbox/ qui contiennent un flag loop."""
    briefs = []
    if not BRIEFS_DIR.is_dir():
        return briefs

    for fpath in BRIEFS_DIR.glob("*.md"):
        try:
            content = fpath.read_text()
        except OSError:
            continue

        for flag, loop_type in LOOP_FLAGS.items():
            # Cherche le flag dans le brief (ex: "auto_review: true")
            if re.search(rf"{flag}\s*:\s*true", content, re.IGNORECASE):
                # Extrait les livrables / chemins du brief
                livrables = _extract_livrables(content)
                briefs.append({
                    "file": str(fpath.relative_to(PKA_DIR)),
                    "loop_type": loop_type,
                    "flag": flag,
                    "livrables": livrables,
                })
                break  # un seul flag par brief
    return briefs


def _extract_livrables(content: str) -> list[str]:
    """Extrait les chemins de livrables depuis un brief."""
    paths = []
    # Pattern : `chemin/` ou `fichier.ext`
    for match in re.finditer(r'`([^`]+/(?:[^`]+\.(?:py|js|ino|cpp|yml|yaml|md|sh|json|html|css))?)`', content):
        paths.append(match.group(1))
    return paths


# ── MATCHING ─────────────────────────────────────────────────────────
def match_commits_to_briefs(
    commits: list[dict], briefs: list[dict]
) -> list[dict]:
    """Pour chaque commit, vérifie si les fichiers modifiés correspondent à un brief actif."""
    triggers = []

    for commit in commits:
        changed = get_changed_files(commit["hash"])
        if not changed:
            continue

        for brief in briefs:
            matched = _files_match_brief(changed, brief)
            if matched:
                triggers.append({
                    "brief_file": brief["file"],
                    "loop_type": brief["loop_type"],
                    "matched_files": ",".join(matched),
                    "commit_hash": commit["hash"],
                    "commit_author": commit["author"],
                })

    return triggers


def _files_match_brief(changed: list[str], brief: dict) -> list[str]:
    """Vérifie si les fichiers modifiés correspondent aux livrables du brief."""
    matched = []
    livrables = brief.get("livrables", [])

    # Si le brief liste des livrables spécifiques
    for livrable in livrables:
        for f in changed:
            if livrable in f or f.endswith(livrable.split("/")[-1]):
                matched.append(f)
                break

    # Si pas de livrables spécifiques, matcher sur le dossier du projet
    if not matched:
        # Essaie de matcher sur le chemin du brief lui-même
        brief_path = brief["file"]
        for f in changed:
            # Même dossier ou sous-dossier que le brief
            if brief_path.split("/")[0] in f:
                matched.append(f)

    return matched


# ── DB ───────────────────────────────────────────────────────────────
def store_triggers(triggers: list[dict], conn: sqlite3.Connection):
    """Écrit les triggers dans team.db."""
    for t in triggers:
        conn.execute(
            """INSERT INTO loop_triggers
               (brief_file, loop_type, matched_files, commit_hash, commit_author)
               VALUES (?, ?, ?, ?, ?)""",
            (t["brief_file"], t["loop_type"], t["matched_files"],
             t["commit_hash"], t["commit_author"]),
        )
    conn.commit()


# ── MAIN ─────────────────────────────────────────────────────────────
def run_once():
    """Une passe de scan."""
    state = load_state()
    last_commit = state.get("last_commit")

    commits = get_new_commits(last_commit)
    if not commits:
        return 0

    briefs = find_active_loop_briefs()
    if not briefs:
        # Même sans trigger, on met à jour le curseur
        state["last_commit"] = commits[-1]["hash"]
        state["last_check"] = datetime.now().isoformat()
        save_state(state)
        return 0

    triggers = match_commits_to_briefs(commits, briefs)

    if triggers:
        conn = sqlite3.connect(str(DB_PATH))
        store_triggers(triggers, conn)
        conn.close()
        print(f"[Loop Watcher] {len(triggers)} trigger(s) créé(s) :")
        for t in triggers:
            print(f"  → {t['loop_type']} sur {t['brief_file']} (commit {t['commit_hash'][:8]})")

    # Met à jour le curseur
    state["last_commit"] = commits[-1]["hash"]
    state["last_check"] = datetime.now().isoformat()
    save_state(state)

    return len(triggers)


def main():
    if "--daemon" in sys.argv:
        print(f"[Loop Watcher] Démarrage daemon (intervalle: {CHECK_INTERVAL}s)")
        while True:
            try:
                n = run_once()
                if n:
                    print(f"[Loop Watcher] {n} trigger(s). Prochain check dans {CHECK_INTERVAL}s.")
            except Exception as exc:
                print(f"[Loop Watcher] Erreur: {exc}", file=sys.stderr)
            time.sleep(CHECK_INTERVAL)
    else:
        run_once()


if __name__ == "__main__":
    main()
