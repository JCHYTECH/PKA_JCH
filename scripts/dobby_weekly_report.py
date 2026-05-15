#!/usr/bin/env python3
"""
dobby_weekly_report.py
Dobby 🦉 — rapport hebdomadaire pour JCH.
Analyse les sessions de la semaine, identifie les patterns de collaboration,
envoie le rapport par email à jc_havaux@yahoo.com.
Tourne tous les dimanches à 19h.
"""

import base64
import email.mime.text
import json
import sqlite3
from datetime import date, datetime, timedelta
from pathlib import Path

import anthropic
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# ── CONFIG ──────────────────────────────────────────────────────
BASE_DIR      = Path(__file__).resolve().parent
PKA_DIR       = BASE_DIR.parent
DB_PATH       = PKA_DIR / "TEAM" / "team.db"
SESSIONS_DIR  = Path.home() / ".claude/projects/-Users-jchavauxm5"
WIKI_DAILY    = PKA_DIR / "wiki" / "Daily"
SECRETS_DIR   = Path.home() / ".config" / "pka-jch"
TOKEN_FILE    = SECRETS_DIR / "token.json"
CREDS_FILE    = SECRETS_DIR / "credentials.json"
ANTHROPIC_KEY = (SECRETS_DIR / "anthropic_key.txt").read_text().strip()
DIGEST_TO     = "jc_havaux@yahoo.com"
MAX_CHARS     = 14000

SCOPES = [
    "https://www.googleapis.com/auth/gmail.send",
]

DOBBY_SYSTEM = """Tu es Dobby 🦉, orchestrateur PKA de Jean-Claude Havaux.
Tu analyses les sessions de travail de la semaine pour identifier comment JCH pourrait améliorer
sa façon de collaborer avec toi (Claude Code) et avec son équipe PKA.
Tu écris un rapport bienveillant mais direct, adressé à JCH à la deuxième personne (tu).
Tu identifies : ses patterns de communication, ce qui ralentit les sessions, ce qu'il pourrait faire différemment.
Tu proposes des habitudes concrètes et actionnables, avec un défi de la semaine.
Ton ton : franc, respectueux, constructif. Pas de flatterie.
Output : markdown structuré, lisible par email."""
# ────────────────────────────────────────────────────────────────


def get_week_transcripts():
    """Extraire les échanges des 7 derniers jours."""
    today = date.today()
    week_ago = today - timedelta(days=7)
    exchanges_by_day = {}

    for jsonl_file in sorted(SESSIONS_DIR.glob("*.jsonl"),
                             key=lambda f: f.stat().st_mtime, reverse=True):
        mtime_date = datetime.fromtimestamp(jsonl_file.stat().st_mtime).date()
        if mtime_date < week_ago or mtime_date > today:
            continue

        day_str = mtime_date.isoformat()
        if day_str not in exchanges_by_day:
            exchanges_by_day[day_str] = []

        with open(jsonl_file, encoding="utf-8") as fh:
            for line in fh:
                try:
                    d = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if d.get("type") not in ("user", "assistant"):
                    continue
                msg = d.get("message", {})
                content = msg.get("content", "")
                if isinstance(content, list):
                    text = " ".join(
                        c.get("text", "") for c in content
                        if isinstance(c, dict) and c.get("type") == "text"
                    ).strip()
                else:
                    text = str(content).strip()
                if text:
                    exchanges_by_day[day_str].append((d.get("type"), text[:350]))

    return exchanges_by_day


def build_week_context(exchanges_by_day):
    parts = []
    for day, exchanges in sorted(exchanges_by_day.items()):
        section = f"### {day} ({len(exchanges)} échanges)\n"
        lines = []
        for role, text in exchanges:
            label = "JCH" if role == "user" else "Claude"
            lines.append(f"[{label}] {text}")
        section += "\n".join(lines)
        parts.append(section)

    full = "\n\n".join(parts)
    if len(full) > MAX_CHARS:
        full = full[:MAX_CHARS] + "\n\n[... tronqué ...]"
    return full


def get_week_retros():
    """Lire les rétrospectives Dobby de la semaine pour enrichir l'analyse."""
    today = date.today()
    retros = []
    for i in range(7):
        d = today - timedelta(days=i)
        year, month = d.strftime("%Y"), d.strftime("%m")
        retro_file = WIKI_DAILY / year / month / f"{d.isoformat()}-dobby-retro.md"
        if retro_file.exists():
            retros.append(retro_file.read_text(encoding="utf-8")[:1000])
    return retros


def call_dobby(context, retros, week_str):
    client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)

    retro_section = ""
    if retros:
        retro_section = "\n\nRétrospectives Dobby de la semaine (extraits) :\n" + "\n---\n".join(retros[:3])

    prompt = (
        f"Voici les transcripts de sessions de travail de la semaine du {week_str} :\n\n"
        f"{context}"
        f"{retro_section}\n\n"
        f"Génère le rapport hebdomadaire 'Comment mieux collaborer avec ton équipe PKA' pour JCH.\n"
        f"Sections :\n"
        f"## Ce que tu fais bien\n"
        f"## Patterns qui ralentissent nos sessions\n"
        f"## Habitudes concrètes à adopter\n"
        f"## Défi de la semaine"
    )

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        system=DOBBY_SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def save_report_md(today_str, content):
    year, month = today_str[:4], today_str[5:7]
    dest_dir = WIKI_DAILY / year / month
    dest_dir.mkdir(parents=True, exist_ok=True)
    filepath = dest_dir / f"{today_str}-dobby-jch-rapport-hebdo.md"
    header = (
        f"---\ndate: {today_str}\ntype: rapport-hebdo\nauthor: Dobby\ntags: [rapport, jch, collaboration, meta]\n---\n\n"
    )
    filepath.write_text(header + content, encoding="utf-8")
    return str(filepath)


def send_email(content, week_str):
    try:
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
        service = build("gmail", "v1", credentials=creds)

        subject = f"🦉 Dobby — Rapport hebdo PKA · Semaine du {week_str}"
        body = f"Bonjour JCH,\n\nVoici ta rétrospective hebdomadaire PKA.\n\n{content}\n\n— Dobby 🦉"

        msg = email.mime.text.MIMEText(body, "plain", "utf-8")
        msg["To"]      = DIGEST_TO
        msg["From"]    = "me"
        msg["Subject"] = subject

        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")
        service.users().messages().send(userId="me", body={"raw": raw}).execute()
        print(f"[Dobby] Email envoyé à {DIGEST_TO}")
    except Exception as e:
        print(f"[Dobby] Erreur envoi email : {e}")


def main():
    today_str = date.today().isoformat()
    week_ago  = (date.today() - timedelta(days=7)).isoformat()
    week_str  = f"{week_ago} → {today_str}"
    print(f"[Dobby] Rapport hebdo {week_str}…")

    exchanges_by_day = get_week_transcripts()
    if not exchanges_by_day:
        print("[Dobby] Aucune session cette semaine.")
        return

    total = sum(len(v) for v in exchanges_by_day.values())
    print(f"[Dobby] {len(exchanges_by_day)} jours de session, {total} échanges.")

    context = build_week_context(exchanges_by_day)
    retros  = get_week_retros()
    report  = call_dobby(context, retros, week_str)

    filepath = save_report_md(today_str, report)
    send_email(report, week_str)
    print(f"[Dobby] Rapport écrit → {filepath}")


if __name__ == "__main__":
    main()
