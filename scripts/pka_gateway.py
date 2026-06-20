#!/usr/bin/env python3
"""
pka_gateway.py 🦉 — Gateway unifiée multi-canal PKA

Point d'entrée unique pour tous les messages externes vers Dobby.
Remplace les connecteurs fragmentés (Telegram bot, Dropbox watch,
Apple Notes, loop watcher, Gmail gatekeeper) par un processus unique.

Canaux supportés :
  - local_inbox   → JCH_Inbox/00_INBOX/ (fichiers + dossiers)
  - dropbox_inbox → ~/Dropbox/00_INBOX/ (si configuré)
  - apple_notes   → Export Apple Notes → inbox
  - telegram      → Bot Telegram — lit conversation.db
  - git_commits   → Nouveaux commits → triggers loops

Usage :
  python3 scripts/pka_gateway.py                          # scan unique + résumé
  python3 scripts/pka_gateway.py --watch                  # polling continu
  python3 scripts/pka_gateway.py --once --verbose         # scan détaillé
  python3 scripts/pka_gateway.py --status                 # état des canaux

Output :
  - Messages normalisés → team.db (table gateway_messages)
  - Fichiers inbox détectés → file_index (team.db)
  - Commits → loop_triggers (team.db)
  - Résumé → stdout + TEAM_Inbox/YYYY-MM-DD_gateway_scan.md
"""

import argparse
import json
import os
import sqlite3
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# ── CONFIG ──────────────────────────────────────────────────────────
PKA_DIR = Path(__file__).resolve().parents[1]
DB_PATH = PKA_DIR / "TEAM" / "team.db"
LOCAL_INBOX = PKA_DIR / "JCH_Inbox" / "00_INBOX"
PROCESSED_DIR = LOCAL_INBOX / ".processed"
DROPBOX_INBOX = Path.home() / "Dropbox" / "00_INBOX"
TEAM_INBOX = PKA_DIR / "TEAM_Inbox"
STATE_FILE = PKA_DIR / "_local" / "gateway_state.json"

POLL_INTERVAL = 60  # secondes (mode --watch)
MAX_MESSAGES_PER_SCAN = 50

# ── SCHEMA ──────────────────────────────────────────────────────────

def ensure_schema():
    """Crée la table gateway_messages si elle n'existe pas."""
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""
            CREATE TABLE IF NOT EXISTS gateway_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                channel TEXT NOT NULL,
                source_path TEXT,
                message_type TEXT NOT NULL,
                subject TEXT,
                body TEXT,
                priority TEXT DEFAULT 'normal',
                status TEXT DEFAULT 'unread',
                created_at TEXT DEFAULT (datetime('now')),
                processed_at TEXT,
                routed_to TEXT
            )
        """)


# ── CHANNEL SCANNERS ────────────────────────────────────────────────

def scan_local_inbox(state: dict) -> list[dict]:
    """Scanne JCH_Inbox/00_INBOX/ pour les nouveaux fichiers."""
    messages = []
    if not LOCAL_INBOX.is_dir():
        return messages

    seen = set(state.get("local_inbox_seen", []))
    new_seen = []

    for entry in sorted(LOCAL_INBOX.iterdir()):
        if entry.name.startswith("."):
            continue
        if entry.is_dir() and entry.name == ".processed":
            continue

        entry_id = f"{entry.name}:{entry.stat().st_mtime}"
        new_seen.append(entry_id)

        if entry_id in seen:
            continue

        msg_type = "directory" if entry.is_dir() else "file"
        messages.append({
            "channel": "local_inbox",
            "source_path": str(entry.relative_to(PKA_DIR)),
            "message_type": msg_type,
            "subject": entry.name,
            "body": f"Nouveau {msg_type} dans 00_INBOX: {entry.name}",
            "priority": "normal",
        })

    state["local_inbox_seen"] = list(set(new_seen))[-200:]  # max 200
    return messages


def scan_dropbox_inbox(state: dict) -> list[dict]:
    """Scanne ~/Dropbox/00_INBOX/ si configuré."""
    messages = []
    if not DROPBOX_INBOX.is_dir():
        return messages

    seen = set(state.get("dropbox_inbox_seen", []))
    new_seen = []

    for entry in sorted(DROPBOX_INBOX.iterdir()):
        if entry.name.startswith("."):
            continue

        entry_id = f"{entry.name}:{entry.stat().st_mtime}"
        new_seen.append(entry_id)

        if entry_id in seen:
            continue

        messages.append({
            "channel": "dropbox_inbox",
            "source_path": str(entry),
            "message_type": "file" if entry.is_file() else "directory",
            "subject": entry.name,
            "body": f"Dropbox inbox: {entry.name}",
            "priority": "high" if entry.suffix in (".pdf", ".docx", ".md") else "normal",
        })

    state["dropbox_inbox_seen"] = list(set(new_seen))[-200:]
    return messages


def scan_apple_notes(state: dict) -> list[dict]:
    """Vérifie les nouveaux exports Apple Notes."""
    messages = []
    notes_dir = LOCAL_INBOX / "notes_apple"
    if not notes_dir.is_dir():
        return messages

    seen = set(state.get("apple_notes_seen", []))
    new_seen = []

    for entry in sorted(notes_dir.iterdir()):
        if entry.name.startswith("."):
            continue

        entry_id = f"{entry.name}:{entry.stat().st_mtime}"
        new_seen.append(entry_id)

        if entry_id in seen:
            continue

        messages.append({
            "channel": "apple_notes",
            "source_path": str(entry.relative_to(PKA_DIR)),
            "message_type": "note",
            "subject": entry.stem,
            "body": f"Note Apple: {entry.stem}",
            "priority": "low",
        })

    state["apple_notes_seen"] = list(set(new_seen))[-200:]
    return messages


def scan_telegram(state: dict) -> list[dict]:
    """Surveille la base conversation.db du bot Telegram pour les nouveaux messages."""
    messages = []
    conv_db = PKA_DIR / "scripts" / "telegram-bot" / "conversation.db"
    if not conv_db.is_file():
        return messages

    last_id = state.get("telegram_last_id", 0)
    try:
        conn = sqlite3.connect(conv_db)
        rows = conn.execute(
            "SELECT id, role, content, created FROM history WHERE id > ? ORDER BY id",
            (last_id,)
        ).fetchall()
        conn.close()

        for row in rows:
            msg_id, role, content, created = row
            messages.append({
                "channel": "telegram",
                "source_path": f"telegram:{msg_id}",
                "message_type": "text" if role == "user" else "response",
                "subject": f"Telegram {role}",
                "body": content[:500] if content else "",
                "priority": "high" if role == "user" else "normal",
            })
            last_id = max(last_id, msg_id)

        state["telegram_last_id"] = last_id
    except sqlite3.DatabaseError:
        pass

    return messages


def scan_git_commits(state: dict) -> list[dict]:
    """Détecte les nouveaux commits depuis le dernier scan."""
    messages = []
    try:
        import subprocess
        last_sha = state.get("git_last_sha", "")
        cmd = ["git", "-C", str(PKA_DIR), "log", "--oneline", "-20"]
        if last_sha:
            cmd = ["git", "-C", str(PKA_DIR), "log", "--oneline", f"{last_sha}..HEAD"]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            return messages

        lines = result.stdout.strip().split("\n")
        for line in lines:
            if not line.strip():
                continue
            sha = line.split()[0]
            msg = " ".join(line.split()[1:])
            messages.append({
                "channel": "git_commits",
                "source_path": sha,
                "message_type": "commit",
                "subject": f"Commit {sha[:7]}",
                "body": msg,
                "priority": "normal",
            })

        # Mettre à jour le dernier SHA
        all_log = subprocess.run(
            ["git", "-C", str(PKA_DIR), "log", "--oneline", "-1"],
            capture_output=True, text=True, timeout=10
        )
        if all_log.stdout.strip():
            state["git_last_sha"] = all_log.stdout.split()[0]

    except (subprocess.SubprocessError, FileNotFoundError):
        pass

    return messages


# ── STORE ────────────────────────────────────────────────────────────

def store_messages(messages: list[dict], dry_run: bool = False) -> int:
    """Stocke les messages dans team.db (gateway_messages)."""
    if dry_run:
        return len(messages)

    stored = 0
    with sqlite3.connect(DB_PATH) as con:
        for msg in messages[:MAX_MESSAGES_PER_SCAN]:
            con.execute(
                """INSERT INTO gateway_messages
                   (channel, source_path, message_type, subject, body, priority)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (msg["channel"], msg.get("source_path", ""),
                 msg["message_type"], msg.get("subject", ""),
                 msg.get("body", ""), msg.get("priority", "normal")),
            )
            stored += 1
    return stored


# ── REPORT ───────────────────────────────────────────────────────────

def generate_report(messages: list[dict], state: dict) -> str:
    """Génère un résumé humain du scan."""
    now = datetime.now()
    lines = [
        f"# Gateway Scan — {now.strftime('%Y-%m-%d %H:%M')}",
        "",
        f"Messages détectés : **{len(messages)}**",
        "",
    ]

    by_channel: dict[str, list] = {}
    for msg in messages:
        by_channel.setdefault(msg["channel"], []).append(msg)

    lines.append("| Canal | Messages |")
    lines.append("|-------|----------|")
    for channel, items in sorted(by_channel.items()):
        lines.append(f"| {channel} | {len(items)} |")
    lines.append("")

    for channel, items in sorted(by_channel.items()):
        lines.append(f"## {channel}")
        for msg in items[:5]:
            lines.append(f"- [{msg['priority']}] {msg['subject']}")
        if len(items) > 5:
            lines.append(f"- ... et {len(items) - 5} autres")
        lines.append("")

    return "\n".join(lines)


def write_report(report: str):
    """Écrit le rapport dans TEAM_Inbox/."""
    today = datetime.now().strftime("%Y-%m-%d")
    ts = datetime.now().strftime("%H%M")
    path = TEAM_INBOX / f"{today}_gateway_scan_{ts}.md"
    path.write_text(report, encoding="utf-8")
    return path


# ── STATE ────────────────────────────────────────────────────────────

def load_state() -> dict:
    if STATE_FILE.is_file():
        try:
            return json.loads(STATE_FILE.read_text())
        except json.JSONDecodeError:
            pass
    return {
        "local_inbox_seen": [],
        "dropbox_inbox_seen": [],
        "apple_notes_seen": [],
        "git_last_sha": "",
        "last_scan": None,
    }


def save_state(state: dict):
    state["last_scan"] = datetime.now().isoformat()
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2, ensure_ascii=False))


# ── STATUS ───────────────────────────────────────────────────────────

def show_status():
    """Affiche l'état de tous les canaux."""
    state = load_state()
    print("🦉 pka_gateway — État des canaux\n")

    telegram_ok = (PKA_DIR / "scripts" / "telegram-bot" / "conversation.db").is_file()
    telegram_running = False
    try:
        import subprocess
        result = subprocess.run(["pgrep", "-f", "telegram-bot/bot.py"], capture_output=True, text=True)
        telegram_running = bool(result.stdout.strip())
    except Exception:
        pass

    channels = [
        ("local_inbox", LOCAL_INBOX.is_dir(), "JCH_Inbox/00_INBOX/"),
        ("dropbox_inbox", DROPBOX_INBOX.is_dir(), "~/Dropbox/00_INBOX/"),
        ("apple_notes", (LOCAL_INBOX / "notes_apple").is_dir(), "Apple Notes → inbox"),
        ("telegram", telegram_running, f"Telegram bot {'🟢 actif' if telegram_running else '🔴 arrêté'}"),
        ("git_commits", True, "Git log scanner"),
    ]

    for name, active, desc in channels:
        icon = "🟢" if active else "🔴"
        print(f"  {icon} {name:20s} {desc}")

    if state.get("last_scan"):
        print(f"\n  Dernier scan : {state['last_scan']}")

    # Compteurs DB
    try:
        with sqlite3.connect(DB_PATH) as con:
            total = con.execute("SELECT COUNT(*) FROM gateway_messages").fetchone()[0]
            unread = con.execute(
                "SELECT COUNT(*) FROM gateway_messages WHERE status='unread'"
            ).fetchone()[0]
            print(f"  Messages en file : {unread} non lus / {total} total")
    except sqlite3.DatabaseError:
        print("  Messages en file : table non initialisée")


# ── MAIN ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="pka_gateway.py — Gateway unifiée multi-canal PKA"
    )
    parser.add_argument("--watch", action="store_true",
                        help="Polling continu (intervalle: 60s)")
    parser.add_argument("--once", action="store_true",
                        help="Scan unique (défaut)")
    parser.add_argument("--status", action="store_true",
                        help="Afficher l'état des canaux")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Affichage détaillé")
    parser.add_argument("--dry-run", action="store_true",
                        help="Scan sans écriture DB")
    parser.add_argument("--report", action="store_true",
                        help="Générer un rapport dans TEAM_Inbox/")
    args = parser.parse_args()

    if args.status:
        show_status()
        return

    ensure_schema()

    if args.watch:
        print("🦉 pka_gateway — Mode watch (Ctrl+C pour arrêter)\n")
        try:
            while True:
                _run_scan(dry_run=args.dry_run,
                          verbose=args.verbose,
                          report=args.report)
                time.sleep(POLL_INTERVAL)
        except KeyboardInterrupt:
            print("\n👋 Gateway arrêtée.")
    else:
        _run_scan(dry_run=args.dry_run,
                  verbose=args.verbose,
                  report=args.report)


def _run_scan(dry_run: bool = False, verbose: bool = False,
              report: bool = False):
    """Exécute un scan complet de tous les canaux."""
    state = load_state()
    all_messages = []

    # Scanner chaque canal
    scanners = [
        ("local_inbox", scan_local_inbox),
        ("dropbox_inbox", scan_dropbox_inbox),
        ("apple_notes", scan_apple_notes),
        ("telegram", scan_telegram),
        ("git_commits", scan_git_commits),
    ]

    for channel_name, scanner in scanners:
        try:
            msgs = scanner(state)
            all_messages.extend(msgs)
            if verbose and msgs:
                print(f"  [{channel_name}] {len(msgs)} nouveaux messages")
        except Exception as exc:
            if verbose:
                print(f"  [{channel_name}] Erreur: {exc}")

    # Stocker
    if all_messages:
        stored = store_messages(all_messages, dry_run=dry_run)
        tag = "[DRY-RUN]" if dry_run else ""
        print(f"🦉 Gateway : {stored} message(s) {tag}")
        if verbose:
            for msg in all_messages[:10]:
                print(f"  [{msg['channel']}] {msg['subject']}")

        if report and not dry_run:
            rep = generate_report(all_messages, state)
            rpath = write_report(rep)
            print(f"📊 Rapport : {rpath.name}")

    save_state(state)


if __name__ == "__main__":
    main()
