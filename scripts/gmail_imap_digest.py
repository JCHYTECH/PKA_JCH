#!/usr/bin/env python3
"""gmail_imap_digest.py — Digest mails non lus via IMAP (sans OAuth, lecture seule).

Méthode retenue (décision 2026-11-21) : IMAP + mot de passe d'application, car
l'OAuth Gmail (projet Google Cloud orphelin + écran de consentement « Testing »)
est instable (tokens expirant en ~7 j). Ce script ne marque RIEN comme lu,
n'archive pas, n'envoie rien : lecture seule, conforme au garde-fou decision-gate.

Déduplication locale : un fichier d'état (`_local/gmail_imap_digest_state.json`)
mémorise les UIDs déjà signalés, pour ne re-pousser que les NOUVEAUX non-lus.
La boîte n'est jamais modifiée.

Usage :
  python3 scripts/gmail_imap_digest.py --list       # affiche les non-lus (stdout)
  python3 scripts/gmail_imap_digest.py              # digest → fichier + ntfy
  python3 scripts/gmail_imap_digest.py --no-push    # fichier seul, sans ntfy
  python3 scripts/gmail_imap_digest.py --limit 10

Secret : ~/.config/pka-jch/gmail_app_password.txt (ou env GMAIL_APP_PASSWORD)
Sortie : JCH_Inbox/00_INBOX/email_digest/YYYY-MM-DD.md
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

PKA_DIR = Path(__file__).resolve().parent.parent
APP_PASSWORD_FILE = Path("~/.config/pka-jch/gmail_app_password.txt").expanduser()
OUTPUT_DIR = PKA_DIR / "JCH_Inbox" / "00_INBOX" / "email_digest"
STATE_PATH = PKA_DIR / "_local" / "gmail_imap_digest_state.json"

IMAP_HOST = "imap.gmail.com"
ACCOUNT = "jc.havaux@gmail.com"
SEARCH = "is:unread in:inbox"
MAX_SCAN = 50  # on ne regarde que les 50 non-lus les plus récents (défensif)
NTFY_TOPIC = "jch-mail-digest-cnfbzcvqi9lg"
MAX_DISPLAY = 8

PRIORITY_SENDERS = ["bosseloir", "noury", "peiwen", "qi"]
PRIORITY_KEYWORDS = [
    "urgent", "important", "deadline", "contrat", "vetalyx", "arteon",
    "jchytech", "signature", "relance", "rappel", "meeting", "réunion",
]
SPAM_KEYWORDS = [
    "unsubscribe", "se désabonner", "newsletter", "promo", "promotion",
    "offre exclusive", "offre spéciale", "soldes", "réduction", "discount",
    "no-reply", "noreply", "do-not-reply", "donotreply", "marketing",
    "publicité", "advertisement",
]
SPAM_SENDERS = [
    "temu", "aliexpress", "shein", "wish", "vinted", "leboncoin",
    "newsletters", "info@", "news@", "hello@", "contact@",
]

_BOT_PREFIXES = (
    "noreply", "no-reply", "no_reply", "donotreply", "do-not-reply",
    "hello", "info", "news", "newsletter", "newsletters", "updates",
    "notifications", "notification", "alert", "alerts", "support",
    "mailer", "reply", "postmaster", "admin", "contact", "mail",
    "billing", "invoice", "order", "orders", "receipt", "receipts",
    "tracking", "shipment", "delivery", "confirm", "confirmation",
    "automated", "bounce", "system", "marketing", "promo",
)
_BOT_SUBDOMAINS = ("em.", "email.", "mail.", "e.", "list.", "send.", "mg.",
                   "news.", "bulk.", "mkto.", "mkt.", "drip.", "engage.")


def get_app_password() -> str:
    env = os.environ.get("GMAIL_APP_PASSWORD", "").strip()
    if env:
        return env
    if APP_PASSWORD_FILE.exists():
        return APP_PASSWORD_FILE.read_text(encoding="utf-8").strip()
    raise RuntimeError(
        "Mot de passe d'application introuvable : ~/.config/pka-jch/gmail_app_password.txt"
    )


def connect() -> imaplib.IMAP4_SSL:
    mbox = imaplib.IMAP4_SSL(IMAP_HOST)
    mbox.login(ACCOUNT, get_app_password())
    return mbox


def load_seen() -> set[str]:
    if STATE_PATH.exists():
        try:
            data = json.loads(STATE_PATH.read_text(encoding="utf-8"))
            return set(data.get("seen_uids", []))
        except Exception:
            pass
    return set()


def save_seen(uids: set[str]) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    STATE_PATH.write_text(
        json.dumps({"seen_uids": sorted(uids)}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


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


def _is_human_sender(sender_email: str) -> bool:
    e = sender_email.lower().strip()
    local = e.split("@")[0] if "@" in e else e
    domain = e.split("@")[1] if "@" in e else ""
    if local in _BOT_PREFIXES or any(local.startswith(p) for p in _BOT_PREFIXES):
        return False
    if any(domain.startswith(s) for s in _BOT_SUBDOMAINS):
        return False
    for bot in ("temuemail.com", "aliexpress.com", "sendgrid.net", "amazonses.com",
                "mailchimp.com", "klaviyo.com", "exacttarget.com", "salesforce.com",
                "hubspot.com"):
        if domain.endswith(bot):
            return False
    return True


def score_email(sender_email: str, subject: str, sender_name: str = "") -> int:
    s = 0
    el = sender_email.lower()
    nl = sender_name.lower()
    sl = subject.lower()

    for p in SPAM_SENDERS:
        if p in el or p in nl:
            return -20
    if not _is_human_sender(el):
        s -= 3

    for p in PRIORITY_SENDERS:
        if p in el:
            s += 5
    for kw in PRIORITY_KEYWORDS:
        if kw in sl:
            s += 2
    for kw in SPAM_KEYWORDS:
        if kw in sl or kw in el:
            s -= 5
    return s


def list_unread(mbox: imaplib.IMAP4_SSL) -> list[dict]:
    mbox.select("INBOX", readonly=True)
    typ, data = mbox.uid("search", None, "X-GM-RAW", f'"{SEARCH}"')
    if typ != "OK":
        raise RuntimeError(f"Recherche échouée : {SEARCH}")
    uids = [u.decode() for u in data[0].split()] if data and data[0] else []
    uids = uids[-MAX_SCAN:]  # les plus récents seulement (défensif)

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
        subject = decode_header_value(msg.get("Subject", "(sans objet)"))
        sender_name, sender_email = parse_from(msg.get("From", ""))
        emails.append({
            "uid": uid,
            "subject": subject,
            "sender_name": sender_name,
            "sender_email": sender_email,
            "score": score_email(sender_email, subject, sender_name),
        })

    emails = [e for e in emails if e["score"] >= 0]
    emails.sort(key=lambda e: e["score"], reverse=True)
    return emails


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


def render(emails: list[dict], limit: int, seen: set[str] | None = None) -> str:
    now = datetime.now()
    seen = seen or set()
    lines = [f"# 📬 Digest mails — {now:%Y-%m-%d %H:%M}", ""]
    lines.append(f"**Non lus retenus :** {len(emails)} (score ≥ 0)\n")
    for e in emails[:limit]:
        marker = "🆕 " if e["uid"] not in seen else ""
        subj = e["subject"][:70] + ("…" if len(e["subject"]) > 70 else "")
        lines.append(f"- {marker}**{e['sender_name']}** — {subj}  *(score {e['score']})*")
    if not emails:
        lines.append("Rien de prioritaire.")
    lines.append("")
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(description="Digest mails non lus via IMAP (lecture seule)")
    ap.add_argument("--list", action="store_true", help="Afficher sans écrire ni pousser")
    ap.add_argument("--limit", type=int, default=MAX_DISPLAY)
    ap.add_argument("--no-push", action="store_true", help="Ne pas pousser ntfy")
    args = ap.parse_args()

    mbox = connect()
    try:
        emails = list_unread(mbox)
    finally:
        try:
            mbox.logout()
        except Exception:
            pass

    seen = load_seen()
    current_uids = {e["uid"] for e in emails}
    new_emails = [e for e in emails if e["uid"] not in seen]

    text = render(emails, args.limit, seen)

    if args.list:
        print(text)
        print(f"\n🆕 nouveaux depuis le dernier run : {len(new_emails)}")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUTPUT_DIR / f"{datetime.now():%Y-%m-%d}.md"
    out.write_text(text + "\n", encoding="utf-8")

    pushed = False
    if not args.no_push and new_emails:
        title = f"📬 Digest mails — {datetime.now():%H:%M}"
        body = "\n".join(
            f"• {e['sender_name']} — {e['subject'][:50]}"
            for e in new_emails[:args.limit]
        )
        pushed = push_ntfy(title, body)

    save_seen(current_uids)

    print(f"{len(emails)} non-lus retenus ({len(new_emails)} nouveaux) → {out}")
    print(f"ntfy: {'envoyé' if pushed else 'non envoyé (rien de nouveau ou non configuré)'}")


if __name__ == "__main__":
    main()
