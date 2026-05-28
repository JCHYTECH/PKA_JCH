#!/usr/bin/env python3
"""
outlook_gatekeeper.py
Lit les mails non lus Outlook/Office365 via Microsoft Graph API.
Meme pipeline que email_digest.py : score → Pie (Claude) → classement → archive.
"""

import json
import os
import re
import sys
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import msal
import requests
import anthropic

# ── CONFIG ───────────────────────────────────────────────────────
BASE_DIR       = Path(__file__).resolve().parent
PKA_DIR        = BASE_DIR.parent
SECRETS_DIR    = Path.home() / ".config" / "pka-jch"
# Fallback: also check PKA workspace if .config is not writable
MS_CONFIG      = SECRETS_DIR / "outlook_config.json"
if not MS_CONFIG.exists():
    MS_CONFIG = PKA_DIR / "docs" / "system" / "outlook_config.json"
TOKEN_CACHE    = SECRETS_DIR / "outlook_token.json"
DB_PATH        = PKA_DIR / "TEAM" / "team.db"
TEAM_INBOX     = PKA_DIR / "TEAM_Inbox"
ANTHROPIC_KEY  = (SECRETS_DIR / "anthropic_key.txt").read_text().strip()
LOG_FILE       = PKA_DIR / "tmp" / "outlook-gatekeeper.log"

GRAPH_BASE = "https://graph.microsoft.com/v1.0"
SCOPES = ["https://graph.microsoft.com/Mail.ReadWrite"]

# ── Scoring (same as email_digest) ──────────────────────────────
PRIORITY_SENDERS   = ["bosseloir", "noury", "peiwen", "qi"]
PRIORITY_KEYWORDS  = ["urgent", "important", "deadline", "contrat",
                      "vetalyx", "arteon", "jchytech", "signature",
                      "relance", "rappel", "meeting", "reunion"]
SPAM_KEYWORDS      = ["unsubscribe", "newsletter", "promo", "promotion",
                      "offre exclusive", "soldes", "reduction", "discount",
                      "no-reply", "noreply", "marketing", "publicite"]
PKA_FOLDERS = ["ARTEON", "VETALYX", "JCHYTECH", "DIM3", "SAC", "PERSO"]

# ── Pie system prompt (same as email_digest) ────────────────────
PIE_SYSTEM = (
    "Tu es Pie, analyste de contenu mails pour JCH (Jean-Claude Havaux). "
    "Tu analyses chaque email pour en extraire l'intention, l'urgence et l'action. "
    "Projets connus : ARTEON, VETALYX, JCHYTECH, DIM3, SAC, PERSO. "
    "Reponds UNIQUEMENT en JSON valide, sans markdown :\n"
    '{"intention": "demande|information|relance|offre|SAC|autre", '
    '"urgence": 1, '
    '"sentiment": "positif|neutre|negatif", '
    '"langue": "FR|EN|ZH|autre", '
    '"action": "repondre|lire|archiver|router", '
    '"projet": "ARTEON|VETALYX|JCHYTECH|DIM3|SAC|PERSO", '
    '"resume": "Une phrase max."}'
)
# ─────────────────────────────────────────────────────────────────

def log(msg: str):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{now}] {msg}\n")

def load_config() -> dict:
    if not MS_CONFIG.exists():
        log("Config manquante : outlook_config.json")
        sys.exit(1)
    return json.loads(MS_CONFIG.read_text())

def get_token(config: dict) -> str:
    cache = msal.SerializableTokenCache()
    if TOKEN_CACHE.exists():
        cache.deserialize(TOKEN_CACHE.read_text())

    app = msal.PublicClientApplication(
        config["client_id"],
        authority=f"https://login.microsoftonline.com/{config['tenant_id']}",
        token_cache=cache,
    )

    accounts = app.get_accounts()
    result = None
    if accounts:
        result = app.acquire_token_silent(SCOPES, account=accounts[0])

    if not result:
        log("Token expire — lancer outlook_auth.py dans le terminal")
        sys.exit(1)

    if "access_token" not in result:
        raise RuntimeError(f"Auth failed: {result.get('error_description', result)}")

    TOKEN_CACHE.write_text(cache.serialize())
    return result["access_token"]

def get_unread_messages(token: str) -> list[dict]:
    headers = {"Authorization": f"Bearer {token}"}
    url = (f"{GRAPH_BASE}/me/messages"
           f"?$filter=isRead eq false"
           f"&$top=50"
           f"&$select=id,subject,from,receivedDateTime,bodyPreview")
    messages = []
    while url:
        r = requests.get(url, headers=headers, timeout=30)
        if r.status_code != 200:
            log(f"Graph error {r.status_code}: {r.text[:200]}")
            break
        data = r.json()
        messages.extend(data.get("value", []))
        url = data.get("@odata.nextLink")
    return messages

def get_message_body(token: str, msg_id: str) -> str:
    headers = {"Authorization": f"Bearer {token}"}
    url = f"{GRAPH_BASE}/me/messages/{msg_id}?$select=body"
    r = requests.get(url, headers=headers, timeout=30)
    if r.status_code == 200:
        return r.json().get("body", {}).get("content", "")[:3000]
    return ""

def score_email(sender_email: str, subject: str, sender_name: str = "") -> int:
    s = 0
    e = sender_email.lower()
    subj = subject.lower()
    for p in PRIORITY_SENDERS:
        if p in e:
            s += 5
    for kw in PRIORITY_KEYWORDS:
        if kw in subj:
            s += 2
    for kw in SPAM_KEYWORDS:
        if kw in subj or kw in e:
            s -= 5
    return s

def analyze_with_pie(sender_name: str, sender_email: str, subject: str, body: str) -> dict | None:
    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
        user_msg = (
            f"Email recu par JCH :\n\n"
            f"De : {sender_name} <{sender_email}>\n"
            f"Objet : {subject}\n\n"
            f"Corps :\n{body or '(corps non disponible)'}\n\n"
            f"Analyse cet email."
        )
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=600,
            system=PIE_SYSTEM,
            messages=[{"role": "user", "content": user_msg}],
        )
        return json.loads(response.content[0].text)
    except Exception as e:
        log(f"Pie error: {e}")
        return None

def get_or_create_folder(token: str, folder_name: str) -> str | None:
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(
        f"{GRAPH_BASE}/me/mailFolders/inbox/childFolders",
        headers=headers, timeout=30
    )
    if r.status_code == 200:
        for f in r.json().get("value", []):
            if f["displayName"] == folder_name:
                return f["id"]
    r2 = requests.post(
        f"{GRAPH_BASE}/me/mailFolders/inbox/childFolders",
        headers=headers,
        json={"displayName": folder_name},
        timeout=30
    )
    if r2.status_code == 201:
        return r2.json()["id"]
    return None

def move_to_folder(token: str, msg_id: str, folder_id: str):
    headers = {"Authorization": f"Bearer {token}"}
    requests.post(
        f"{GRAPH_BASE}/me/messages/{msg_id}/move",
        headers=headers,
        json={"destinationId": folder_id},
        timeout=30
    )

def save_pie_analysis(sender_name: str, subject: str, analysis: dict):
    today = datetime.now().strftime("%Y-%m-%d")
    slug = re.sub(r"[^\w]", "-", subject[:40].lower()).strip("-")
    filename = f"{today}_outlook_pie_{slug}.md"
    filepath = TEAM_INBOX / filename
    TEAM_INBOX.mkdir(parents=True, exist_ok=True)
    content = (
        f"# Pie — Analyse email Outlook\n\n"
        f"**Date :** {today}\n"
        f"**De :** {sender_name}\n"
        f"**Objet :** {subject}\n\n"
        f"---\n\n"
        f"- **Intention :** {analysis.get('intention')}\n"
        f"- **Urgence :** {analysis.get('urgence')}/5\n"
        f"- **Sentiment :** {analysis.get('sentiment')}\n"
        f"- **Projet :** {analysis.get('projet')}\n"
        f"- **Action :** {analysis.get('action')}\n"
        f"- **Resume :** {analysis.get('resume')}\n"
    )
    filepath.write_text(content, encoding="utf-8")
    return filename

def main():
    TEAM_INBOX.mkdir(parents=True, exist_ok=True)
    config = load_config()
    token = get_token(config)

    folders = {}
    for proj in PKA_FOLDERS:
        fid = get_or_create_folder(token, f"PKA/{proj}")
        if fid:
            folders[proj] = fid

    messages = get_unread_messages(token)
    log(f"Scan: {len(messages)} unread messages")

    processed = 0
    for msg in messages:
        msg_id = msg["id"]
        subject = msg.get("subject", "(sans objet)")
        from_data = msg.get("from", {}).get("emailAddress", {})
        sender_email = from_data.get("address", "").lower()
        sender_name = from_data.get("name", sender_email)
        body_preview = msg.get("bodyPreview", "")

        score = score_email(sender_email, subject, sender_name)
        if score < 0:
            log(f"SPAM: {sender_name} — {subject[:50]}")
            continue

        body = get_message_body(token, msg_id) if score >= 2 else body_preview

        pie = analyze_with_pie(sender_name, sender_email, subject, body)
        if not pie:
            continue

        projet = pie.get("projet", "")
        if projet in folders:
            move_to_folder(token, msg_id, folders[projet])
            log(f"[{projet}] {sender_name}: {subject[:60]}")

        save_pie_analysis(sender_name, subject, pie)
        processed += 1

    log(f"Done: {processed}/{len(messages)} processed")

if __name__ == "__main__":
    main()
