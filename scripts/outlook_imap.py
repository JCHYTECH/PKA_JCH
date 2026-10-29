#!/usr/bin/env python3
"""
outlook_imap.py
Lit les mails non lus Outlook/Hotmail via IMAP.
Simple, zero OAuth, zero Azure. App password recommande si 2FA active.
"""

import email
import imaplib
import json
import re
import sys
from datetime import datetime
from email.header import decode_header
from pathlib import Path

import anthropic

BASE_DIR       = Path(__file__).resolve().parent
PKA_DIR        = BASE_DIR.parent
SECRETS_DIR    = Path.home() / ".config" / "pka-jch"
IMAP_CONFIG    = PKA_DIR / "docs" / "system" / "outlook_imap.json"
TEAM_INBOX     = PKA_DIR / "TEAM_Inbox"
ANTHROPIC_KEY  = (SECRETS_DIR / "anthropic_key.txt").read_text().strip()
LOG_FILE       = PKA_DIR / "tmp" / "outlook-imap.log"

PIE_SYSTEM = (
    "Tu es Pie, analyste de contenu mails pour JCH. "
    "Reponds UNIQUEMENT en JSON valide, sans markdown :\n"
    '{"intention": "demande|information|relance|offre|SAC|autre", '
    '"urgence": 1, '
    '"projet": "ARTEON|VETALYX|JCHYTECH|DIM3|SAC|PERSO", '
    '"action": "repondre|lire|archiver", '
    '"resume": "Une phrase max."}'
)

def log(msg: str):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{now}] {msg}\n")

def load_config() -> dict:
    if not IMAP_CONFIG.exists():
        log("Config manquante : outlook_imap.json")
        sys.exit(1)
    return json.loads(IMAP_CONFIG.read_text())

def decode_str(s):
    if s is None:
        return ""
    parts = decode_header(s)
    result = []
    for data, charset in parts:
        if isinstance(data, bytes):
            result.append(data.decode(charset or "utf-8", errors="ignore"))
        else:
            result.append(str(data))
    return " ".join(result)

def analyze_with_pie(subject: str, sender: str, body: str) -> dict | None:
    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
        user_msg = (
            f"Email recu par JCH :\n\n"
            f"De : {sender}\n"
            f"Objet : {subject}\n\n"
            f"Corps :\n{body[:2000]}\n\n"
            f"Analyse cet email."
        )
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=400,
            system=PIE_SYSTEM,
            messages=[{"role": "user", "content": user_msg}],
        )
        return json.loads(response.content[0].text)
    except Exception as e:
        log(f"Pie error: {e}")
        return None

def main():
    config = load_config()
    TEAM_INBOX.mkdir(parents=True, exist_ok=True)

    mail = imaplib.IMAP4_SSL("outlook.office365.com", 993)
    mail.login(config["email"], config["password"])
    mail.select("inbox")

    _, ids = mail.search(None, "UNSEEN")
    msg_ids = ids[0].split()
    log(f"Scan: {len(msg_ids)} unread")

    processed = 0
    for num in msg_ids[-20:]:
        _, data = mail.fetch(num, "(RFC822)")
        raw = data[0][1]
        msg = email.message_from_bytes(raw)

        subject = decode_str(msg["Subject"])
        sender = decode_str(msg["From"])
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    b = part.get_payload(decode=True)
                    if b:
                        body = b.decode("utf-8", errors="ignore")
                        break
        else:
            b = msg.get_payload(decode=True)
            if b:
                body = b.decode("utf-8", errors="ignore")

        pie = analyze_with_pie(subject, sender, body)
        if not pie:
            continue

        projet = pie.get("projet", "PERSO")
        log(f"[{projet}] {sender[:40]}: {subject[:60]}")

        today = datetime.now().strftime("%Y-%m-%d")
        slug = re.sub(r"[^\w]", "-", subject[:40].lower()).strip("-")
        fname = f"{today}_outlook_{slug}.md"
        filepath = TEAM_INBOX / fname
        filepath.write_text(
            f"# Pie — Outlook\n\n"
            f"**De :** {sender}\n"
            f"**Objet :** {subject}\n"
            f"**Projet :** {projet}\n"
            f"**Action :** {pie.get('action')}\n\n"
            f"**Resume :** {pie.get('resume')}\n",
            encoding="utf-8"
        )

        mail.store(num, "+FLAGS", "\\Seen")
        processed += 1

    mail.logout()
    log(f"Done: {processed}")

if __name__ == "__main__":
    main()
