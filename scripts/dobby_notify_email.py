#!/usr/bin/env python3
"""
dobby_notify_email.py — Envoi d'un mail à JC via Gmail SMTP (mot de passe d'application).

Réutilise le même mot de passe d'application que gmail_imap_fetch.py :
    ~/.config/pka-jch/gmail_app_password.txt  (compte jc.havaux@gmail.com)

Usage :
    python3 scripts/dobby_notify_email.py --subject "..." --body "corps"
    echo "corps" | python3 scripts/dobby_notify_email.py --subject "..." --body -
    python3 scripts/dobby_notify_email.py --subject "..." --body "..." --dry-run
    python3 scripts/dobby_notify_email.py --subject "..." --body "..." --to jc_havaux@yahoo.com

Config : JCH_Inbox/99_SYSTEM/security/gmail_imap.json  (champ account)
Secret : ~/.config/pka-jch/gmail_app_password.txt  (jamais commité)
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import smtplib
import sys
from datetime import datetime, timezone
from email.message import EmailMessage
from email.utils import format_datetime, make_msgid
from pathlib import Path

PKA_DIR = Path(__file__).resolve().parent.parent
CONFIG_PATH = PKA_DIR / "JCH_Inbox" / "99_SYSTEM" / "security" / "gmail_imap.json"
APP_PASSWORD_FILE = Path("~/.config/pka-jch/gmail_app_password.txt").expanduser()

DEFAULT_TO = "jc.havaux@gmail.com"
SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587


def load_account() -> str:
    """Compte Gmail émetteur (défaut : jc.havaux@gmail.com)."""
    if CONFIG_PATH.exists():
        try:
            data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
            acc = data.get("account", "").strip()
            if acc:
                return acc
        except Exception:
            pass
    return "jc.havaux@gmail.com"


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


def send_email(subject: str, body: str, to: str | None = None, dry_run: bool = False,
               attachments: list[str] | None = None) -> bool:
    """Envoie un mail, avec pièces jointes optionnelles. Retourne True si envoyé (ou dry-run OK)."""
    account = load_account()
    recipient = to or DEFAULT_TO
    password = get_app_password()

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = f"Dobby <{account}>"
    msg["To"] = recipient
    msg["Date"] = format_datetime(datetime.now(timezone.utc))
    msg["Message-ID"] = make_msgid(domain="gmail.com")
    msg.set_content(body)

    for path in attachments or []:
        p = Path(path)
        if not p.is_file():
            raise FileNotFoundError(f"Pièce jointe introuvable : {path}")
        ctype, _ = mimetypes.guess_type(p.name)
        maintype, subtype = (ctype or "application/octet-stream").split("/", 1)
        msg.add_attachment(p.read_bytes(), maintype=maintype, subtype=subtype, filename=p.name)

    server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=30)
    try:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(account, password)
        if dry_run:
            return True
        server.send_message(msg)
        return True
    finally:
        try:
            server.quit()
        except Exception:
            pass


def main() -> int:
    parser = argparse.ArgumentParser(description="Dobby — notification email (Gmail SMTP)")
    parser.add_argument("--subject", required=True, help="Sujet du mail")
    parser.add_argument("--body", default="", help="Corps du mail ('-' pour lire stdin)")
    parser.add_argument("--to", default=DEFAULT_TO, help=f"Destinataire (défaut : {DEFAULT_TO})")
    parser.add_argument("--dry-run", action="store_true", help="Connexion SMTP + login, sans envoi")
    parser.add_argument("--attach", action="append", default=None, metavar="FILE", help="Pièce jointe (répétable)")
    args = parser.parse_args()

    body = args.body
    if body == "-":
        body = sys.stdin.read()

    try:
        send_email(args.subject, body, to=args.to, dry_run=args.dry_run, attachments=args.attach)
    except Exception as e:
        print(f"❌ Envoi échoué : {e}", file=sys.stderr)
        return 1

    if args.dry_run:
        print(f"✅ SMTP OK (dry-run, aucun mail envoyé) — {SMTP_HOST}:{SMTP_PORT} — login {load_account()}")
    else:
        print(f"✅ Mail envoyé → {args.to}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())