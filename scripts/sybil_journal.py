#!/usr/bin/env python3
"""
sybil_journal.py
Sybil 🦔 — génère automatiquement l'entrée journal du jour à 22h.
Collecte : digest du jour, agenda, activité team.db, fichiers modifiés.
Écrit dans wiki/Daily/ et insère dans team.db → journal.
"""

import os
import re
from pka_memory_log import log_run
import sqlite3
from datetime import datetime, date, timezone, timedelta
from pathlib import Path

import anthropic
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# ── CONFIG ──────────────────────────────────────────────────────
BASE_DIR     = Path(__file__).resolve().parent
PKA_DIR      = BASE_DIR.parent
DB_PATH      = PKA_DIR / "TEAM" / "team.db"
WIKI_DAILY   = PKA_DIR / "wiki" / "Daily"
DIGEST_LOG   = BASE_DIR / "digest_history.md"
SECRETS_DIR  = Path.home() / ".config" / "pka-jch"
TOKEN_FILE   = SECRETS_DIR / "token.json"
CREDS_FILE   = SECRETS_DIR / "credentials.json"
ANTHROPIC_KEY = (SECRETS_DIR / "anthropic_key.txt").read_text().strip()

SCOPES = [
    "https://www.googleapis.com/auth/calendar.readonly",
]

SYBIL_SYSTEM = """Tu es Sybil 🦔, archiviste personnelle de Jean-Claude Havaux (JCH).
Tu écris l'entrée journal quotidienne automatique à partir des faits observables de la journée.
Ton style : sobre, précis, en français. Pas d'effusion, pas de jugement. Tu rapportes ce qui s'est passé.
Tu utilises la première personne du pluriel ("Voici ce que la journée a produit") ou une voix neutre narrative.
Tu structure en sections thématiques selon ce que tu as reçu comme données.
Ton output est du markdown pur, sans balise de code, prêt à être écrit dans un fichier .md."""
# ────────────────────────────────────────────────────────────────


def get_calendar_service():
    creds = None
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    if not creds or not creds.valid:
        return None
    return build("calendar", "v3", credentials=creds)


def get_today_events():
    try:
        service = get_calendar_service()
        if not service:
            return []
        now = datetime.now(timezone.utc)
        start = now.replace(hour=0, minute=0, second=0).isoformat()
        end   = now.replace(hour=23, minute=59, second=59).isoformat()
        result = service.events().list(
            calendarId="primary",
            timeMin=start, timeMax=end,
            singleEvents=True, orderBy="startTime",
            maxResults=20
        ).execute()
        events = []
        for e in result.get("items", []):
            title = e.get("summary", "(sans titre)")
            start_info = e.get("start", {})
            if "dateTime" in start_info:
                dt = datetime.fromisoformat(start_info["dateTime"])
                events.append(f"{dt.strftime('%H:%M')} — {title}")
            else:
                events.append(f"Journée — {title}")
        return events
    except Exception:
        return []


def get_today_digest():
    """Extraire les entrées du digest d'aujourd'hui depuis digest_history.md."""
    today = date.today().strftime("%Y-%m-%d")
    if not DIGEST_LOG.exists():
        return []
    content = DIGEST_LOG.read_text(encoding="utf-8")
    sections = re.split(r"(?=## \d{4}-\d{2}-\d{2})", content)
    today_sections = [s for s in sections if s.startswith(f"## {today}")]
    return today_sections


def get_today_db_activity():
    """Récupérer l'activité team.db du jour : inbox, interactions, ideas."""
    today = date.today().isoformat()
    results = {}
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # Inbox — tâches routées aujourd'hui
        c.execute("""
            SELECT from_name, to_name, subject FROM inbox
            WHERE date(created_at) = ? OR date(updated_at) = ?
            ORDER BY created_at DESC LIMIT 10
        """, (today, today))
        rows = c.fetchall()
        if rows:
            results["inbox"] = [f"{r[0]} → {r[1]} : {r[2]}" for r in rows]

        # Interactions CRM du jour
        c.execute("""
            SELECT c.first_name, c.last_name, i.type, i.summary
            FROM interactions i
            JOIN contacts c ON c.id = i.contact_id
            WHERE i.date = ?
            ORDER BY i.id DESC LIMIT 10
        """, (today,))
        rows = c.fetchall()
        if rows:
            results["interactions"] = [f"{r[0]} {r[1]} — {r[2]} : {r[3]}" for r in rows]

        # Idées capturées aujourd'hui
        c.execute("""
            SELECT title, status FROM ideas
            WHERE date(created_at) = ?
            ORDER BY id DESC LIMIT 10
        """, (today,))
        rows = c.fetchall()
        if rows:
            results["ideas"] = [f"{r[0]} [{r[1]}]" for r in rows]

        conn.close()
    except Exception:
        pass
    return results


def get_modified_files():
    """Fichiers PKA modifiés aujourd'hui (hors scripts et cache)."""
    today = date.today()
    modified = []
    skip = {".git", "scripts", "__pycache__", ".DS_Store", "backups"}
    for f in PKA_DIR.rglob("*"):
        if f.is_file() and not any(s in f.parts for s in skip):
            mtime = datetime.fromtimestamp(f.stat().st_mtime).date()
            if mtime == today:
                rel = str(f.relative_to(PKA_DIR))
                modified.append(rel)
    return modified[:30]


def build_context(events, digest_sections, db_activity, modified_files):
    parts = [f"DATE : {date.today().isoformat()}\n"]

    if events:
        parts.append("## Agenda du jour\n" + "\n".join(f"- {e}" for e in events))

    if digest_sections:
        parts.append("## Digest email (extraits)\n" + "\n".join(digest_sections[:3]))

    if db_activity.get("inbox"):
        parts.append("## Activité équipe (inbox)\n" + "\n".join(f"- {r}" for r in db_activity["inbox"]))

    if db_activity.get("interactions"):
        parts.append("## Interactions CRM\n" + "\n".join(f"- {r}" for r in db_activity["interactions"]))

    if db_activity.get("ideas"):
        parts.append("## Idées capturées\n" + "\n".join(f"- {r}" for r in db_activity["ideas"]))

    if modified_files:
        parts.append("## Fichiers modifiés\n" + "\n".join(f"- {f}" for f in modified_files))

    return "\n\n".join(parts)


def call_sybil(context):
    client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
    prompt = (
        f"Voici les données observables de la journée de JCH :\n\n{context}\n\n"
        f"Écris l'entrée journal du jour. Structure-la en sections thématiques pertinentes. "
        f"Commence directement par le frontmatter YAML puis le contenu markdown. "
        f"Pas de section 'Humeur' ou 'Énergie' — ce sont des données que JCH renseignera lui-même."
    )
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1500,
        system=SYBIL_SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def save_journal_md(today_str, content):
    year  = today_str[:4]
    month = today_str[5:7]
    dest_dir = WIKI_DAILY / year / month
    dest_dir.mkdir(parents=True, exist_ok=True)

    filepath = dest_dir / f"{today_str}-sybil-auto.md"
    if filepath.exists():
        # Ajouter une section au fichier existant
        existing = filepath.read_text(encoding="utf-8")
        filepath.write_text(existing + f"\n\n---\n\n## Mise à jour automatique 22h\n\n{content}", encoding="utf-8")
    else:
        filepath.write_text(content, encoding="utf-8")
    return str(filepath)


def save_journal_db(today_str, content):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        title = f"Journal automatique — {today_str}"
        c.execute("""
            INSERT OR IGNORE INTO journal (date, title, body)
            VALUES (?, ?, ?)
        """, (today_str, title, content[:5000]))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[journal DB] erreur : {e}")


def main():
    today_str = date.today().isoformat()
    print(f"[Sybil] Génération journal {today_str}…")

    events         = get_today_events()
    digest_secs    = get_today_digest()
    db_activity    = get_today_db_activity()
    modified_files = get_modified_files()

    context = build_context(events, digest_secs, db_activity, modified_files)

    if not context.strip():
        print("[Sybil] Aucune donnée collectée — journal non généré.")
        return

    journal_text = call_sybil(context)
    filepath     = save_journal_md(today_str, journal_text)
    save_journal_db(today_str, journal_text)

    print(f"[Sybil] Journal écrit → {filepath}")
    log_run("sybil_journal", "ok", f"Journal {today_str} écrit → {filepath}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        log_run("sybil_journal", "error", str(exc))
        raise
