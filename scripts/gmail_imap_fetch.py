#!/usr/bin/env python3
"""
gmail_imap_fetch.py — Lecture Gmail via IMAP + mot de passe d'application.

Lit les mails correspondant à une RECHERCHE Gmail ciblée (par défaut : tous les
mails envoyés à l'alias `jc.havaux+dobby@gmail.com`) et les dépose dans
JCH_Inbox/00_INBOX/email_imports/. Aucune dépendance aux filtres/étiquettes Gmail :
l'adresse de destination EST le déclencheur.

Usage :
  python3 scripts/gmail_imap_fetch.py --list             # liste les mails correspondants
  python3 scripts/gmail_imap_fetch.py --fetch            # télécharge les NOUVEAUX mails
  python3 scripts/gmail_imap_fetch.py --fetch --force    # re-télécharge aussi les déjà vus

Config : JCH_Inbox/99_SYSTEM/security/gmail_imap.json  (champ `search`)
Secret : ~/.config/pka-jch/gmail_app_password.txt  (mot de passe d'application)
État   : _local/gmail_imap_fetch_state.json  (UIDs déjà importés, dédup)
"""

from __future__ import annotations

import argparse
import base64
import email
import imaplib
import json
import os
import re
import sys
from datetime import datetime
from email.header import decode_header, make_header
from email.utils import parsedate_to_datetime
from pathlib import Path

PKA_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = PKA_DIR / "JCH_Inbox" / "99_SYSTEM" / "security" / "gmail_imap.json"
EXTRACT_ROOT = PKA_DIR / "JCH_Inbox" / "00_INBOX" / "email_imports"
STATE_PATH = PKA_DIR / "_local" / "gmail_imap_fetch_state.json"
APP_PASSWORD_FILE = Path("~/.config/pka-jch/gmail_app_password.txt").expanduser()

DEFAULT_CONFIG = {
    "imap_host": "imap.gmail.com",
    "account": "jc.havaux@gmail.com",
    "search": "to:jc.havaux+dobby@gmail.com",
}


def load_config() -> dict:
    cfg = dict(DEFAULT_CONFIG)
    if CONFIG_PATH.exists():
        data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        cfg.update({k: v for k, v in data.items() if v})
    return cfg


def get_app_password() -> str:
    env = os.environ.get("GMAIL_APP_PASSWORD", "").strip()
    if env:
        return env
    if APP_PASSWORD_FILE.exists():
        return APP_PASSWORD_FILE.read_text(encoding="utf-8").strip()
    raise RuntimeError(
        "Mot de passe d'application introuvable. Définissez GMAIL_APP_PASSWORD "
        "ou créez ~/.config/pka-jch/gmail_app_password.txt"
    )


def connect(cfg: dict) -> imaplib.IMAP4_SSL:
    mbox = imaplib.IMAP4_SSL(cfg["imap_host"])
    mbox.login(cfg["account"], get_app_password())
    return mbox


def load_state() -> dict:
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text(encoding="utf-8"))
    return {"seen_uids": [], "last_fetch": None}


def save_state(state: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def decode_header_value(value: str) -> str:
    try:
        return str(make_header(decode_header(value)))
    except Exception:
        return value or ""


def slugify(text: str, max_len: int = 60) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return slug[:max_len] or "sans-objet"


def iter_parts(msg):
    """Itère sur toutes les parts, en incluant les sous-messages (forwards)."""
    yield msg
    if msg.is_multipart():
        for part in msg.walk():
            yield part
            # les forwards Outlook contiennent un message imbriqué avec leurs PJ
            if part.is_multipart() or part.get_content_maintype() == "message":
                for sub in part.walk():
                    yield sub


def parse_message(raw: bytes) -> dict:
    """Extrait sujet, expéditeur, date, corps et pièces jointes (nom + bytes)."""
    msg = email.message_from_bytes(raw)
    subject = decode_header_value(msg.get("Subject", "(sans objet)"))
    sender = decode_header_value(msg.get("From", ""))
    date_raw = msg.get("Date", "")
    try:
        dt = parsedate_to_datetime(date_raw)
    except Exception:
        dt = datetime.now()

    body_plain = ""
    body_html = ""
    attachments = []  # list[(filename, bytes)]

    seen_attachment_names = set()
    for part in iter_parts(msg):
        ctype = part.get_content_type()
        cdispo = str(part.get("Content-Disposition", "")).lower()
        fname = part.get_filename()

        # pièce jointe (Content-Disposition: attachment) ou PDF/image avec un nom
        is_attachment = "attachment" in cdispo or (fname and ctype not in ("text/plain", "text/html"))
        if fname and is_attachment:
            fname = decode_header_value(fname)
            payload = part.get_payload(decode=True)
            if payload and fname not in seen_attachment_names:
                attachments.append((fname, payload))
                seen_attachment_names.add(fname)
            continue

        if ctype == "text/plain" and not body_plain and not fname:
            try:
                body_plain = part.get_payload(decode=True).decode(
                    part.get_content_charset() or "utf-8", errors="replace"
                )
            except Exception:
                body_plain = ""
        elif ctype == "text/html" and not body_html and not fname:
            try:
                body_html = part.get_payload(decode=True).decode(
                    part.get_content_charset() or "utf-8", errors="replace"
                )
            except Exception:
                body_html = ""

    body = body_plain.strip() or body_html.strip() or "(corps vide)"
    return {
        "subject": subject,
        "sender": sender,
        "date": dt,
        "body": body,
        "attachments": attachments,
    }


def search_uids(mbox: imaplib.IMAP4_SSL, cfg: dict) -> list[str]:
    mbox.select("INBOX", readonly=True)
    query = cfg["search"]
    typ, data = mbox.uid("search", None, "X-GM-RAW", f'"{query}"')
    if typ != "OK":
        raise RuntimeError(f"Recherche échouée: {query}")
    return [u.decode() for u in data[0].split()] if data and data[0] else []


def fetch_raw(mbox: imaplib.IMAP4_SSL, uid: str) -> bytes | None:
    typ, data = mbox.uid("fetch", uid, "(RFC822)")
    if typ != "OK":
        return None
    for item in data:
        if isinstance(item, tuple) and isinstance(item[1], (bytes, bytearray)):
            return bytes(item[1])
    return None


def save_message(raw: bytes, meta: dict, uid: str) -> list[str]:
    EXTRACT_ROOT.mkdir(parents=True, exist_ok=True)
    dt = meta["date"]
    base = f"{dt:%Y-%m-%d_%H%M%S}_{slugify(meta['subject'])}"
    written = []

    md = f"# {meta['subject']}\n\n"
    md += f"- **De :** {meta['sender']}\n"
    md += f"- **Date :** {dt.isoformat(timespec='seconds')}\n"
    md += f"- **UID :** {uid}\n"
    if meta["attachments"]:
        md += f"- **Pièces jointes :** {', '.join(fn for fn, _ in meta['attachments'])}\n"
    md += "\n---\n\n" + meta["body"] + "\n"
    (EXTRACT_ROOT / f"{base}.md").write_text(md, encoding="utf-8")
    written.append(f"{base}.md")

    (EXTRACT_ROOT / f"{base}.eml").write_bytes(raw)
    written.append(f"{base}.eml")

    # sauvegarde des pièces jointes
    for fname, payload in meta["attachments"]:
        safe = slugify(Path(fname).stem) + Path(fname).suffix
        out = EXTRACT_ROOT / f"{base}_PJ_{safe}"
        out.write_bytes(payload)
        written.append(out.name)

    return written


def main() -> int:
    parser = argparse.ArgumentParser(description="Lecture Gmail via IMAP (sans OAuth, par recherche).")
    parser.add_argument("--list", action="store_true", help="Liste les mails correspondants.")
    parser.add_argument("--fetch", action="store_true", help="Télécharge les nouveaux mails.")
    parser.add_argument("--force", action="store_true", help="Avec --fetch : re-télécharge aussi les déjà vus.")
    args = parser.parse_args()

    if not args.list and not args.fetch:
        parser.print_help()
        return 1

    cfg = load_config()
    mbox = connect(cfg)
    try:
        uids = search_uids(mbox, cfg)
    finally:
        mbox.logout()

    print(f"🔍 Recherche '{cfg['search']}' -> {len(uids)} mail(s).")

    if args.list:
        mbox = connect(cfg)
        mbox.select("INBOX", readonly=True)
        try:
            for uid in uids:
                raw = fetch_raw(mbox, uid)
                if not raw:
                    continue
                meta = parse_message(raw)
                print(f"  - [{uid}] {meta['subject'][:60]}  |  {meta['sender']}")
        finally:
            mbox.logout()
        return 0

    # --fetch
    state = load_state()
    seen = set(state.get("seen_uids", []))
    to_fetch = uids if args.force else [u for u in uids if u not in seen]

    print(f"📬 {len(to_fetch)} nouveau(x) mail(s) à importer.")
    mbox = connect(cfg)
    mbox.select("INBOX")
    count = 0
    try:
        for uid in to_fetch:
            raw = fetch_raw(mbox, uid)
            if not raw:
                print(f"   ⚠️  UID {uid}: fetch vide, ignoré.")
                continue
            meta = parse_message(raw)
            files = save_message(raw, meta, uid)
            print(f"   ✅ [{uid}] {meta['subject'][:55]}  ({meta['sender']})")
            for f in files:
                print(f"        ↳ {f}")
            seen.add(uid)
            count += 1
    finally:
        mbox.logout()

    state["seen_uids"] = sorted(seen)
    state["last_fetch"] = datetime.now().isoformat(timespec="seconds")
    save_state(state)

    print(f"\nTerminé — {count} mail(s) importé(s) dans {EXTRACT_ROOT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
