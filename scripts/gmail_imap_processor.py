#!/usr/bin/env python3
"""gmail_imap_processor.py — Tri + routage automatique des mails Gmail (lecture seule).

Lit les non-lus de la boîte Gmail (consolidation de toutes les adresses), classe
chaque mail par projet PKA via `JCH_Inbox/99_SYSTEM/email_routing.json`, dépose
les nouveaux dans `00_INBOX/email_triage/<projet>/` (`.eml` + `.md`), et notifie
via ntfy.

Lecture seule stricte : ne marque rien comme lu, n'archive pas, n'envoie rien.
Déduplication locale : `_local/gmail_imap_processor_state.json`.

Usage :
  python3 scripts/gmail_imap_processor.py --dry-run   # trie sans écrire ni notifier
  python3 scripts/gmail_imap_processor.py --no-push   # écrit mais ne notifie pas
  python3 scripts/gmail_imap_processor.py             # run complet
"""

from __future__ import annotations

import argparse
import email
import imaplib
import json
import os
import re
import ssl
import urllib.request
from datetime import datetime
from email.header import decode_header, make_header
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
try:
    import unsubscribe as unsub_mod
except ImportError:  # pragma: no cover
    unsub_mod = None

PKA_DIR = Path(__file__).resolve().parent.parent
APP_PASSWORD_FILE = Path("~/.config/pka-jch/gmail_app_password.txt").expanduser()
ROUTING_PATH = PKA_DIR / "JCH_Inbox" / "99_SYSTEM" / "email_routing.json"
OUTPUT_ROOT = PKA_DIR / "JCH_Inbox" / "00_INBOX" / "email_triage"
STATE_PATH = PKA_DIR / "_local" / "gmail_imap_processor_state.json"

IMAP_HOST = "imap.gmail.com"
ACCOUNT = "jc.havaux@gmail.com"
SEARCH = "is:unread in:inbox"
MAX_SCAN = 60
NTFY_TOPIC = "jch-mail-digest-cnfbzcvqi9lg"
NOTIFY_START_HOUR = 8
NOTIFY_END_HOUR = 22


def get_app_password() -> str:
    env = os.environ.get("GMAIL_APP_PASSWORD", "").strip()
    if env:
        return env
    if APP_PASSWORD_FILE.exists():
        return APP_PASSWORD_FILE.read_text(encoding="utf-8").strip()
    raise RuntimeError("Mot de passe d'application introuvable : ~/.config/pka-jch/gmail_app_password.txt")


def decode_header_value(value: str) -> str:
    try:
        return str(make_header(decode_header(value)))
    except Exception:
        return value or ""


def parse_from(from_raw: str) -> tuple[str, str]:
    from_raw = decode_header_value(from_raw or "")
    if "<" in from_raw and ">" in from_raw:
        name = from_raw.split("<")[0].strip().strip('"').strip()
        addr = from_raw.split("<")[1].split(">")[0].strip()
        return name or addr, addr
    return from_raw, from_raw


def load_state() -> set[str]:
    if STATE_PATH.exists():
        try:
            return set(json.loads(STATE_PATH.read_text(encoding="utf-8")).get("seen_uids", []))
        except Exception:
            pass
    return set()


def save_state(seen: set[str]) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(
        json.dumps({"seen_uids": sorted(seen)}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def load_routing() -> dict:
    if ROUTING_PATH.exists():
        try:
            return json.loads(ROUTING_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"projects": {}, "default": "Autres"}


def slugify(text: str, maxlen: int = 40) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "-", text.lower()).strip("-")
    return s[:maxlen] or "mail"


def route_project(sender_email: str, sender_name: str, subject: str, routing: dict) -> str:
    text = f"{sender_email} {sender_name} {subject}".lower()
    for project, rules in routing.get("projects", {}).items():
        for s in rules.get("senders", []):
            if s.lower() in text:
                return project
        for kw in rules.get("keywords", []):
            if kw.lower() in text:
                return project
    return routing.get("default", "Autres")


def connect() -> imaplib.IMAP4_SSL:
    mbox = imaplib.IMAP4_SSL(IMAP_HOST)
    mbox.login(ACCOUNT, get_app_password())
    return mbox


def fetch_unread(mbox: imaplib.IMAP4_SSL) -> list[dict]:
    mbox.select("INBOX", readonly=True)
    typ, data = mbox.uid("search", None, "X-GM-RAW", f'"{SEARCH}"')
    if typ != "OK":
        raise RuntimeError(f"Recherche échouée : {SEARCH}")
    uids = [u.decode() for u in data[0].split()] if data and data[0] else []
    uids = uids[-MAX_SCAN:]

    emails: list[dict] = []
    for uid in uids:
        typ, d = mbox.uid("fetch", uid, "(BODY.PEEK[HEADER.FIELDS (FROM SUBJECT DATE)])")
        if typ != "OK":
            continue
        raw = b""
        for item in d:
            if isinstance(item, tuple) and isinstance(item[1], (bytes, bytearray)):
                raw = bytes(item[1])
                break
        if not raw:
            continue
        msg = email.message_from_bytes(raw)
        emails.append({
            "uid": uid,
            "subject": decode_header_value(msg.get("Subject", "(sans objet)")),
            "sender_name": parse_from(msg.get("From", ""))[0],
            "sender_email": parse_from(msg.get("From", ""))[1],
            "date": msg.get("Date", ""),
        })
    return emails


def fetch_body(mbox: imaplib.IMAP4_SSL, uid: str) -> bytes | None:
    try:
        typ, d = mbox.uid("fetch", uid, "(BODY.PEEK[])")
        if typ != "OK":
            return None
        for item in d:
            if isinstance(item, tuple) and isinstance(item[1], (bytes, bytearray)):
                return bytes(item[1])
    except Exception:
        return None
    return None


def push_ntfy(title: str, message: str) -> bool:
    try:
        payload = json.dumps({
            "topic": NTFY_TOPIC, "title": title, "message": message,
            "priority": 3, "tags": ["email"],
        }).encode("utf-8")
        req = urllib.request.Request(
            "https://ntfy.sh", data=payload,
            headers={"Content-Type": "application/json"},
        )
        urllib.request.urlopen(req, timeout=10, context=ssl.create_default_context())
        return True
    except Exception:
        return False


def write_mail(project: str, m: dict, body: bytes) -> Path:
    d = OUTPUT_ROOT / project
    d.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    stem = f"{ts}_{slugify(m['sender_email'].split('@')[0])}"
    eml_path = d / f"{stem}.eml"
    md_path = d / f"{stem}.md"
    if body:
        eml_path.write_bytes(body)
    md_path.write_text(
        f"# {m['subject']}\n\n"
        f"- **De :** {m['sender_name']} <{m['sender_email']}>\n"
        f"- **Date :** {m['date']}\n"
        f"- **Projet :** {project}\n\n"
        f"---\n"
        f"*(mail complet : {eml_path.name})*\n",
        encoding="utf-8",
    )
    return md_path


def main() -> None:
    ap = argparse.ArgumentParser(description="Tri + routage automatique des mails (lecture seule)")
    ap.add_argument("--dry-run", action="store_true", help="Trie sans écrire ni notifier")
    ap.add_argument("--no-push", action="store_true", help="Écrit mais ne notifie pas")
    args = ap.parse_args()

    seen = load_state()
    mbox = connect()
    try:
        emails = fetch_unread(mbox)
        new = [e for e in emails if e["uid"] not in seen]
        for e in new:
            e["body"] = fetch_body(mbox, e["uid"])
    finally:
        try:
            mbox.logout()
        except Exception:
            pass

    routing = load_routing()
    for e in emails:
        if unsub_mod is not None and unsub_mod.is_blacklisted(e["sender_email"]):
            e["project"] = "_Ignorés"
        else:
            e["project"] = route_project(e["sender_email"], e["sender_name"], e["subject"], routing)

    by_project: dict[str, int] = {}
    for e in new:
        by_project[e["project"]] = by_project.get(e["project"], 0) + 1

    if args.dry_run:
        print(f"{len(emails)} non-lus ({len(new)} nouveaux)")
        for p, n in sorted(by_project.items(), key=lambda x: -x[1]):
            print(f"  {p}: {n}")
        return

    for e in new:
        write_mail(e["project"], e, e.get("body") or b"")

    if new and not args.no_push:
        hour = datetime.now().hour
        if NOTIFY_START_HOUR <= hour < NOTIFY_END_HOUR:
            title = f"📬 {len(new)} nouveau(x) mail(s)"
            body = "\n".join(f"• [{e['project']}] {e['sender_name']} — {e['subject'][:50]}" for e in new[:8])
            push_ntfy(title, body)

    save_state({e["uid"] for e in emails})

    print(f"{len(emails)} non-lus → {len(new)} nouveaux routés")
    for p, n in sorted(by_project.items(), key=lambda x: -x[1]):
        print(f"  {p}: {n}")
    if new:
        print(f"Déposés dans {OUTPUT_ROOT.relative_to(PKA_DIR)}")

    # Détecter les mails déposés dans _UNSUBSCRIBE/ → désabonnements en attente de validation JC
    if unsub_mod is not None:
        pending = unsub_mod.scan()
        active = [p for p in pending if p.get("status") == "pending"]
        if active and not args.no_push:
            hour = datetime.now().hour
            if NOTIFY_START_HOUR <= hour < NOTIFY_END_HOUR:
                push_ntfy(
                    f"🔕 {len(active)} désabonnement(s) en attente",
                    "Validation JC requise → python3 scripts/unsubscribe.py --execute",
                )


if __name__ == "__main__":
    main()