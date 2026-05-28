#!/usr/bin/env python3
"""
email_digest.py
Lit les emails non lus (Gmail API) + agenda du jour (Calendar API)
Envoie une notification ntfy.sh à 9h, 14h, 20h.
"""

import os
import re
import json
import ssl
import time
import base64
import sqlite3
import certifi
import urllib.request
from datetime import datetime, timezone, timedelta
from pathlib import Path

import anthropic
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# ── CONFIGURATION ──────────────────────────────────────────────
NTFY_TOPIC   = "jch-mail-digest"
MAX_DISPLAY  = 5

PRIORITY_SENDERS = ["bosseloir", "noury", "peiwen", "qi"]

PRIORITY_KEYWORDS = [
    "urgent", "important", "deadline", "contrat",
    "vetalyx", "arteon", "jchytech", "signature",
    "relance", "rappel", "meeting", "réunion",
]

# Score négatif — spam / newsletters
SPAM_KEYWORDS = [
    "unsubscribe", "se désabonner", "newsletter", "promo", "promotion",
    "offre exclusive", "offre spéciale", "soldes", "réduction", "discount",
    "no-reply", "noreply", "do-not-reply", "donotreply",
    "marketing", "publicité", "advertisement",
]

SPAM_SENDERS = [
    "temu", "aliexpress", "shein", "wish", "vinted", "leboncoin",
    "newsletters", "info@", "news@", "hello@", "contact@",
]

BASE_DIR       = os.path.dirname(os.path.abspath(__file__))
SECRETS_DIR    = os.path.expanduser("~/.config/pka-jch")
TOKEN_FILE     = os.path.join(SECRETS_DIR, "token.json")
CREDS_FILE     = os.path.join(SECRETS_DIR, "credentials.json")
ANTHROPIC_KEY  = Path(os.path.join(SECRETS_DIR, "anthropic_key.txt")).read_text().strip()
LAST_RUN_FILE  = os.path.join(BASE_DIR, ".last_run")
DB_PATH        = os.path.join(os.path.dirname(BASE_DIR), "TEAM", "team.db")
TEAM_INBOX     = os.path.join(os.path.dirname(BASE_DIR), "TEAM_Inbox")
DIGEST_LOG     = os.path.join(BASE_DIR, "digest_history.md")

DIGEST_TO      = "jc_havaux@yahoo.com"

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/calendar.readonly",
]

PKA_LABELS = ["!PKA/ARTEON", "!PKA/VETALYX", "!PKA/JCHYTECH", "!PKA/PERSO", "!PKA/DIM3", "!PKA/SAC"]
# ───────────────────────────────────────────────────────────────


def get_credentials():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "w") as f:
            f.write(creds.to_json())
    return creds


def get_last_run():
    try:
        with open(LAST_RUN_FILE) as f:
            return float(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 0.0


def save_last_run():
    with open(LAST_RUN_FILE, "w") as f:
        f.write(str(time.time()))


def load_known_emails():
    """Load all emails from contacts table into a set for fast lookup."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT LOWER(email) FROM contacts WHERE email IS NOT NULL")
        known = {row[0].strip() for row in cur.fetchall()}
        conn.close()
        return known
    except Exception:
        return set()


def load_sender_rules():
    """Load whitelist and blacklist from email_senders table."""
    whitelist_emails, whitelist_patterns, blacklist_patterns = set(), [], []
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("SELECT match_pattern, status FROM email_senders WHERE match_pattern IS NOT NULL")
        for pattern, status in cur.fetchall():
            p = pattern.lower().strip()
            if not p:
                continue
            if status == "whitelist":
                if "@" in p:
                    whitelist_emails.add(p)
                else:
                    whitelist_patterns.append(p)
            elif status == "blacklist":
                blacklist_patterns.append(p)
        conn.close()
    except Exception:
        pass
    return whitelist_emails, whitelist_patterns, blacklist_patterns


KNOWN_EMAILS = load_known_emails()
WHITELIST_EMAILS, WHITELIST_PATTERNS, BLACKLIST_PATTERNS = load_sender_rules()

# Préfixes d'adresse typiques des expéditeurs automatisés
_BOT_PREFIXES = (
    "noreply", "no-reply", "no_reply", "donotreply", "do-not-reply",
    "hello", "info", "news", "newsletter", "newsletters", "updates",
    "notifications", "notification", "alert", "alerts", "support",
    "mailer", "reply", "postmaster", "admin", "contact", "mail",
    "billing", "invoice", "order", "orders", "receipt", "receipts",
    "tracking", "shipment", "delivery", "confirm", "confirmation",
    "automated", "bounce", "system", "marketing", "promo",
)
# Sous-domaines typiques des plateformes d'envoi en masse
_BOT_SUBDOMAINS = ("em.", "email.", "mail.", "e.", "list.", "send.", "mg.",
                   "news.", "bulk.", "mkto.", "mkt.", "drip.", "engage.")


def _is_human_sender(sender_email: str) -> bool:
    """Retourne True seulement si l'adresse ressemble à un humain, pas un bot."""
    e = sender_email.lower().strip()
    local = e.split("@")[0] if "@" in e else e
    domain = e.split("@")[1] if "@" in e else ""

    if local in _BOT_PREFIXES or any(local.startswith(p) for p in _BOT_PREFIXES):
        return False
    if any(domain.startswith(sub) for sub in _BOT_SUBDOMAINS):
        return False
    # Domaines de plateformes d'envoi connus
    for bot_domain in ("temuemail.com", "aliexpress.com", "sendgrid.net",
                       "amazonses.com", "mailchimp.com", "klaviyo.com",
                       "exacttarget.com", "salesforce.com", "hubspot.com"):
        if domain.endswith(bot_domain):
            return False
    return True



def score_email(sender_email, subject, sender_name=""):
    s = 0
    email_lower   = sender_email.lower()
    name_lower    = sender_name.lower()
    subject_lower = subject.lower()

    # Blacklist — filtre immédiat, score -20, inutile d'aller plus loin
    for p in BLACKLIST_PATTERNS:
        if p in email_lower or p in name_lower:
            return -20

    # Whitelist email exact → +10
    if email_lower in WHITELIST_EMAILS:
        s += 10
    else:
        # Whitelist pattern (nom expéditeur connu) → +5
        for p in WHITELIST_PATTERNS:
            if p in email_lower or p in name_lower:
                s += 5
                break

    # Contact CRM connu (en plus de la whitelist) → +3
    if email_lower in KNOWN_EMAILS:
        s += 3

    # Expéditeurs prioritaires nommément → +5
    for p in PRIORITY_SENDERS:
        if p in email_lower:
            s += 5

    # Mots-clés prioritaires dans l'objet → +2 chacun
    for kw in PRIORITY_KEYWORDS:
        if kw in subject_lower:
            s += 2

    # Signaux spam résiduels → -5 chacun
    for kw in SPAM_KEYWORDS:
        if kw in subject_lower or kw in email_lower:
            s -= 5

    return s


def get_emails(service, last_run):
    result = service.users().messages().list(
        userId="me", q="is:unread in:inbox", maxResults=100
    ).execute()

    messages  = result.get("messages", [])
    emails    = []
    new_count = 0

    for msg in messages:
        data = service.users().messages().get(
            userId="me", id=msg["id"],
            format="metadata",
            metadataHeaders=["From", "Subject", "Date"]
        ).execute()

        headers = {h["name"]: h["value"] for h in data.get("payload", {}).get("headers", [])}
        subject      = headers.get("Subject", "(sans objet)")
        from_raw     = headers.get("From", "")
        internal_date = int(data.get("internalDate", 0)) / 1000  # ms → s

        # Parse sender name and email
        if "<" in from_raw:
            sender_name  = from_raw.split("<")[0].strip().strip('"')
            sender_email = from_raw.split("<")[1].rstrip(">").strip()
        else:
            sender_name  = from_raw
            sender_email = from_raw

        if internal_date > last_run:
            new_count += 1

        emails.append({
            "subject":      subject,
            "sender_name":  sender_name or sender_email,
            "sender_email": sender_email.lower(),
            "received":     internal_date,
            "score":        score_email(sender_email, subject, sender_name),
            "msg_id":       msg["id"],
        })

    # Whitelist-first : seuls les scores >= 0 passent (blacklist → -20, inconnus → 0)
    emails = [e for e in emails if e["score"] >= 0]
    emails.sort(key=lambda e: e["score"], reverse=True)
    return emails, new_count


# ── ROUTING RULES ──────────────────────────────────────────────
RENARD_KEYWORDS = [
    "contrat", "contract", "pacte", "actionnaire", "nda", "confidentialité",
    "signature", "clause", "avocat", "notaire", "juridique", "tribunal",
    "litige", "mise en demeure", "résiliation", "accord", "convention",
    "statuts", "cession", "acquisition", "due diligence", "term sheet", "compliance"
]
VASCO_KEYWORDS = [
    "vetalyx", "vitalyx", "vétérinaire", "veterinaire", "allergie",
    "diagnostic", "ivd", "clinique vétérinaire", "médicament", "prescription",
    "panel allergène", "test sérologique", "dermatite", "atopie",
    "respiratory", "food allergy", "nutraceutique", "supplément", "probiotique"
]
BRUNO_KEYWORDS = [
    "investissement", "financement", "valorisation", "levée de fonds",
    "dividende", "bilan", "fiscal", "impôt", "capital", "parts sociales",
    "budget", "trésorerie", "term sheet", "portefeuille", "rendement",
    "placement", "patrimoine", "private equity", "obligations", "etf"
]
MEETING_KEYWORDS = [
    "rendez-vous", "meeting", "réunion", "call", "disponible",
    "agenda", "planifier", "slot", "visio", "zoom", "teams"
]
# ───────────────────────────────────────────────────────────────


def _matches(text, keywords):
    t = text.lower()
    return any(kw in t for kw in keywords)


def _push_alert(topic, title, message, priority=3):
    """Send a separate targeted push notification."""
    try:
        payload = json.dumps({
            "topic":    topic,
            "title":    title,
            "message":  message,
            "priority": priority,
            "tags":     ["email"],
        }).encode("utf-8")
        req = urllib.request.Request(
            "https://ntfy.sh",
            data=payload,
            headers={"Content-Type": "application/json"},
        )
        ctx = ssl.create_default_context(cafile=certifi.where())
        urllib.request.urlopen(req, timeout=10, context=ctx)
    except Exception:
        pass


def route_email(subject, sender_email, sender_name, email_date):
    """Analyse an email and trigger routing actions in team.db + push alerts."""
    combined = f"{subject}"
    routed_to = []

    try:
        conn = sqlite3.connect(DB_PATH)
        cur  = conn.cursor()
        today = datetime.now().strftime("%Y-%m-%d")
        email_lower = sender_email.lower()

        # ── Renard — Legal ──
        if _matches(combined, RENARD_KEYWORDS):
            try:
                cur.execute("""
                    INSERT INTO inbox (direction, from_name, to_name, subject, body, status)
                    VALUES ('JCH→TEAM', 'JCH', 'Renard', ?, ?, 'pending')
                """, (f"[EMAIL] {subject}", f"De: {sender_name} <{sender_email}>"))
                routed_to.append("Renard")
                _push_alert(NTFY_TOPIC, "🦊 Renard — email légal",
                            f"{sender_name}: {subject}", priority=5)
            except Exception:
                pass

        # ── Vasco — Vetalyx ──
        if _matches(combined, VASCO_KEYWORDS):
            try:
                cur.execute("""
                    INSERT INTO inbox (direction, from_name, to_name, subject, body, status)
                    VALUES ('JCH→TEAM', 'JCH', 'Vasco', ?, ?, 'pending')
                """, (f"[EMAIL] {subject}", f"De: {sender_name} <{sender_email}>"))
                routed_to.append("Vasco")
                _push_alert(NTFY_TOPIC, "🐺 Vasco — email Vetalyx",
                            f"{sender_name}: {subject}", priority=4)
            except Exception:
                pass

        # ── Bruno — Finance ──
        if _matches(combined, BRUNO_KEYWORDS):
            try:
                cur.execute("""
                    INSERT INTO inbox (direction, from_name, to_name, subject, body, status)
                    VALUES ('JCH→TEAM', 'JCH', 'Bruno', ?, ?, 'pending')
                """, (f"[EMAIL] {subject}", f"De: {sender_name} <{sender_email}>"))
                routed_to.append("Bruno")
                _push_alert(NTFY_TOPIC, "🐻 Bruno — email financier",
                            f"{sender_name}: {subject}", priority=4)
            except Exception:
                pass

        # ── Delphi — CRM ──
        cur.execute("SELECT id FROM contacts WHERE LOWER(email) = ?", (email_lower,))
        contact = cur.fetchone()

        if contact:
            # Known contact → log interaction silently
            try:
                cur.execute("""
                    INSERT INTO interactions (contact_id, date, type, summary)
                    VALUES (?, ?, 'email', ?)
                """, (contact[0], today, subject[:200]))
                cur.execute("""
                    UPDATE contacts SET last_contact = ? WHERE id = ?
                """, (today, contact[0]))
            except Exception:
                pass
        elif _is_human_sender(sender_email) and score_email(sender_email, subject) >= 5:
            # Unknown human sender with significant score → flag for Delphi
            cur.execute("""
                INSERT INTO inbox (direction, from_name, to_name, subject, body, status)
                VALUES ('JCH→TEAM', 'JCH', 'Delphi', 'Nouveau contact potentiel', ?, 'pending')
            """, (f"{sender_name} <{sender_email}> — {subject}",))
            routed_to.append("Delphi?")

        # ── Meeting request → follow_up ──
        if _matches(combined, MEETING_KEYWORDS):
            contact_id = contact[0] if contact else None
            try:
                tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
                cur.execute("""
                    INSERT INTO follow_ups (contact_id, due_date, subject, notes)
                    VALUES (?, ?, ?, ?)
                """, (contact_id, tomorrow,
                      f"Répondre : {subject[:100]}",
                      f"Demande de RDV de {sender_name}"))
                routed_to.append("follow_up↗")
            except Exception:
                pass

        conn.commit()
        conn.close()

    except Exception:
        pass

    return routed_to


# ── SPECIALIST PERSONAS ────────────────────────────────────────
SPECIALISTS = {
    "Pie": {
        "emoji": "🐦‍⬛",
        "system": (
            "Tu es Pie, analyste de contenu mails pour JCH (Jean-Claude Havaux, entrepreneur belge). "
            "Tu analyses chaque email pour en extraire l'intention, l'urgence et l'action requise. "
            "Tu travailles nativement en FR et EN. Si tu détectes une autre langue, tu le signales. "
            "Projets connus : ARTEON (plateforme photo/critique), VETALYX (diagnostics vétérinaires), "
            "JCHYTECH (entité légale/admin/comptabilité), DIM3 (liquidation société), "
            "SAC (service client), PERSO (personnel hors projets). "
            "Réponds UNIQUEMENT en JSON valide, sans markdown, sans texte autour :\n"
            '{"intention": "demande|information|relance|offre|SAC|autre", '
            '"urgence": 1, '
            '"sentiment": "positif|neutre|negatif", '
            '"langue": "FR|EN|ZH|autre", '
            '"action": "repondre|lire|archiver|router", '
            '"projet": "ARTEON|VETALYX|JCHYTECH|DIM3|SAC|PERSO", '
            '"resume": "Une phrase max."}'
        ),
    },
    "Renard": {
        "emoji": "🦊",
        "system": (
            "Tu es Renard, conseiller juridique de JCH (Jean-Claude Havaux, entrepreneur belge). "
            "Tu analyses les emails à implications légales ou contractuelles. "
            "Tu réponds en français, de manière concise et structurée. "
            "Format : 1) Nature juridique de l'email 2) Points d'attention 3) Action recommandée."
        ),
    },
    "Vasco": {
        "emoji": "🐺",
        "system": (
            "Tu es Vasco, vétérinaire spécialiste en médecine interne (chats & chiens) "
            "et expert produit pour Vetalyx (diagnostics IVD + nutraceutiques). "
            "Tu analyses les emails liés à Vetalyx, aux partenaires vétérinaires ou aux produits. "
            "Tu réponds en français. "
            "Format : 1) Sujet clinique ou produit 2) Pertinence pour Vetalyx 3) Action recommandée."
        ),
    },
    "Bruno": {
        "emoji": "🐻",
        "system": (
            "Tu es Bruno, analyste financier et conseiller en investissement de JCH. "
            "Tu analyses les emails à implications financières, d'investissement ou de financement. "
            "Tu réponds en français. "
            "Format : 1) Nature financière 2) Opportunité ou risque identifié 3) Action recommandée."
        ),
    },
}
# ───────────────────────────────────────────────────────────────


def get_email_body(service, msg_id):
    """Fetch and decode the plain text body of an email."""
    try:
        data = service.users().messages().get(
            userId="me", id=msg_id, format="full"
        ).execute()

        def extract_text(payload):
            mime = payload.get("mimeType", "")
            if mime == "text/plain":
                body_data = payload.get("body", {}).get("data", "")
                if body_data:
                    return base64.urlsafe_b64decode(body_data).decode("utf-8", errors="ignore")
            for part in payload.get("parts", []):
                result = extract_text(part)
                if result:
                    return result
            return ""

        return extract_text(data.get("payload", {}))[:3000]
    except Exception:
        return ""


def analyze_email(specialist_name, sender_name, sender_email, subject, body):
    """Call Claude API as the given specialist and return the analysis."""
    spec = SPECIALISTS.get(specialist_name)
    if not spec:
        return None

    user_msg = (
        f"Email reçu par JCH :\n\n"
        f"De : {sender_name} <{sender_email}>\n"
        f"Objet : {subject}\n\n"
        f"Corps :\n{body or '(corps non disponible)'}\n\n"
        f"Analyse cet email."
    )

    try:
        client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=600,
            system=spec["system"],
            messages=[{"role": "user", "content": user_msg}],
        )
        return response.content[0].text
    except Exception as e:
        return f"Erreur analyse : {e}"


def save_analysis(specialist_name, sender_name, subject, analysis):
    """Write analysis to TEAM_Inbox as a markdown file."""
    today     = datetime.now().strftime("%Y-%m-%d")
    slug      = re.sub(r"[^\w]", "-", subject[:40].lower()).strip("-")
    filename  = f"{today}_{specialist_name.lower()}_email-{slug}.md"
    filepath  = os.path.join(TEAM_INBOX, filename)
    spec      = SPECIALISTS[specialist_name]

    content = (
        f"# {spec['emoji']} {specialist_name} — Analyse email\n\n"
        f"**Date :** {today}  \n"
        f"**De :** {sender_name}  \n"
        f"**Objet :** {subject}  \n\n"
        f"---\n\n"
        f"{analysis}\n"
    )

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return filename


def get_today_events(service):
    now   = datetime.now(timezone.utc)
    start = now.replace(hour=0, minute=0, second=0).isoformat()
    end   = now.replace(hour=23, minute=59, second=59).isoformat()

    result = service.events().list(
        calendarId="primary",
        timeMin=start, timeMax=end,
        singleEvents=True, orderBy="startTime",
        maxResults=10
    ).execute()

    events = []
    for e in result.get("items", []):
        title = e.get("summary", "(sans titre)")
        start_info = e.get("start", {})
        if "dateTime" in start_info:
            dt = datetime.fromisoformat(start_info["dateTime"])
            time_str = dt.strftime("%H:%M")
        else:
            time_str = "Journée"
        events.append(f"{time_str} {title}")

    return events


def send_ntfy(emails, total_unread, new_count, today_events, routing_summary=None):
    hour = datetime.now().hour
    session = "Matin" if hour < 12 else ("Après-midi" if hour < 17 else "Soir")
    priority_count = sum(1 for e in emails if e["score"] > 0)

    title = (
        f"📬 {session} — "
        f"{total_unread} non lu{'s' if total_unread != 1 else ''} · "
        f"{new_count} nouveau{'x' if new_count > 1 else ''} · "
        f"{priority_count} prioritaire{'s' if priority_count > 1 else ''}"
    )

    lines = []

    if emails:
        for i, e in enumerate(emails[:MAX_DISPLAY], 1):
            subj    = e["subject"][:40] + ("…" if len(e["subject"]) > 40 else "")
            known   = "✓" if e["sender_email"] in KNOWN_EMAILS else "?"
            lines.append(f"{i}. [{known}] {e['sender_name']}: {subj}")
        if len(emails) > MAX_DISPLAY:
            lines.append(f"+ {len(emails) - MAX_DISPLAY} autre(s) filtrés")
    else:
        lines.append("Aucun email pertinent.")

    if routing_summary:
        lines.append("")
        lines.append("🔀 Routés :")
        for r in routing_summary[:3]:
            lines.append(f"  · {r}")

    if today_events:
        lines.append("")
        lines.append("📅 Aujourd'hui :")
        for ev in today_events[:3]:
            lines.append(f"  · {ev}")

    payload = json.dumps({
        "topic":    NTFY_TOPIC,
        "title":    title,
        "message":  "\n".join(lines),
        "priority": 3,
        "tags":     ["email", "calendar"],
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://ntfy.sh",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    ctx = ssl.create_default_context(cafile=certifi.where())
    urllib.request.urlopen(req, timeout=10, context=ctx)


def send_digest_email(service, emails, new_count, today_events, routing_summary, analyses_saved, labels_applied=None):
    """Send the digest as an email to DIGEST_TO via Gmail API."""
    import email.mime.text
    import email.mime.multipart

    hour = datetime.now().hour
    session = "Matin" if hour < 12 else ("Après-midi" if hour < 17 else "Soir")
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    priority_count = sum(1 for e in emails if e["score"] > 0)

    subject = (
        f"📬 PKA Digest — {session} {now_str} · "
        f"{len(emails)} email(s) · {new_count} nouveau(x)"
    )

    # ── Plain text body ──
    lines = [f"PKA DIGEST — {session} {now_str}", "=" * 40, ""]

    lines.append(f"Boîte de réception : {len(emails)} email(s) filtrés · {new_count} nouveaux · {priority_count} prioritaires")
    lines.append("")

    if emails:
        lines.append("TOP EMAILS")
        lines.append("-" * 30)
        for i, e in enumerate(emails[:MAX_DISPLAY], 1):
            known = "✓ connu" if e["sender_email"] in KNOWN_EMAILS else "? inconnu"
            subj  = e["subject"][:60] + ("…" if len(e["subject"]) > 60 else "")
            lines.append(f"{i}. [{known}] {e['sender_name']}")
            lines.append(f"   {subj}")
            lines.append(f"   Score : {e['score']}")
            lines.append("")
        if len(emails) > MAX_DISPLAY:
            lines.append(f"+ {len(emails) - MAX_DISPLAY} autre(s) filtrés")
            lines.append("")
    else:
        lines.append("Aucun email pertinent.")
        lines.append("")

    if routing_summary:
        lines.append("ROUTING ÉQUIPE")
        lines.append("-" * 30)
        for r in routing_summary:
            lines.append(f"  → {r}")
        lines.append("")

    if labels_applied:
        lines.append("LABELS APPLIQUÉS")
        lines.append("-" * 30)
        for sender, label in labels_applied:
            lines.append(f"  · {label}  ←  {sender}")
        lines.append("")

    if analyses_saved:
        lines.append("ANALYSES DISPONIBLES")
        lines.append("-" * 30)
        for a in analyses_saved:
            lines.append(f"  · TEAM_Inbox/{a}")
        lines.append("")

    if today_events:
        lines.append("AGENDA DU JOUR")
        lines.append("-" * 30)
        for ev in today_events:
            lines.append(f"  · {ev}")
        lines.append("")

    lines.append("—")
    lines.append("PKA — Personal Knowledge Assistant")

    body_text = "\n".join(lines)

    msg = email.mime.text.MIMEText(body_text, "plain", "utf-8")
    msg["To"]      = DIGEST_TO
    msg["From"]    = "me"
    msg["Subject"] = subject

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")
    try:
        service.users().messages().send(
            userId="me", body={"raw": raw}
        ).execute()
    except Exception as e:
        print(f"[send_digest_email] erreur : {e}")


def save_digest_log(emails, new_count, routing_summary, analyses_saved):
    """Append a digest run entry to the local digest history log."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    hour = datetime.now().hour
    session = "Matin" if hour < 12 else ("Après-midi" if hour < 17 else "Soir")

    lines = [f"## {now} — {session}\n"]
    lines.append(f"- **Non lus filtrés :** {len(emails)}  |  **Nouveaux :** {new_count}\n")

    if emails:
        lines.append("\n**Top emails :**\n")
        for e in emails[:MAX_DISPLAY]:
            known = "✓" if e["sender_email"] in KNOWN_EMAILS else "?"
            subj  = e["subject"][:60] + ("…" if len(e["subject"]) > 60 else "")
            lines.append(f"- [{known}] **{e['sender_name']}** — {subj} (score {e['score']})\n")

    if routing_summary:
        lines.append("\n**Routing :**\n")
        for r in routing_summary:
            lines.append(f"- {r}\n")

    if analyses_saved:
        lines.append("\n**Analyses sauvegardées :**\n")
        for a in analyses_saved:
            lines.append(f"- `{a}`\n")

    lines.append("\n---\n\n")
    entry = "".join(lines)

    # Create file with header if new
    if not os.path.exists(DIGEST_LOG):
        entry = "# Digest History\n\n" + entry

    with open(DIGEST_LOG, "a", encoding="utf-8") as f:
        f.write(entry)


def get_or_create_labels(service):
    """Return a dict {label_name: label_id} — creates missing PKA labels."""
    existing = {l["name"]: l["id"] for l in
                service.users().labels().list(userId="me").execute().get("labels", [])}
    result = {}
    for name in PKA_LABELS:
        if name in existing:
            result[name] = existing[name]
        else:
            try:
                created = service.users().labels().create(
                    userId="me",
                    body={"name": name, "labelListVisibility": "labelShow",
                          "messageListVisibility": "show"}
                ).execute()
                result[name] = created["id"]
            except Exception:
                pass
    return result


def apply_label(service, msg_id, label_id):
    """Apply a label to a Gmail message."""
    try:
        service.users().messages().modify(
            userId="me", id=msg_id,
            body={"addLabelIds": [label_id]}
        ).execute()
    except Exception:
        pass


def archive_from_inbox(service, msg_id):
    """Remove the INBOX label — archives the message out of the inbox."""
    try:
        service.users().messages().modify(
            userId="me", id=msg_id,
            body={"removeLabelIds": ["INBOX"]}
        ).execute()
    except Exception:
        pass


def main():
    last_run = get_last_run()
    creds    = get_credentials()

    gmail_service    = build("gmail",    "v1",   credentials=creds)
    calendar_service = build("calendar", "v3",   credentials=creds)
    pka_labels       = get_or_create_labels(gmail_service)

    emails, new_count  = get_emails(gmail_service, last_run)
    today_events       = get_today_events(calendar_service)

    # Route + analyze new emails (received after last run, score >= 0)
    routing_summary = []
    analyses_saved  = []
    labels_applied  = []
    for e in emails:
        if e["received"] > last_run and e["score"] >= 0:
            routed = route_email(
                e["subject"], e["sender_email"],
                e["sender_name"], e["received"]
            )
            if routed:
                routing_summary.append(f"{e['sender_name']} → {', '.join(routed)}")

            body = get_email_body(gmail_service, e["msg_id"]) if e.get("msg_id") else ""

            # Pie analyse tous les emails nouveaux
            pie_result = analyze_email(
                "Pie", e["sender_name"], e["sender_email"], e["subject"], body
            )
            if pie_result:
                try:
                    pie_data = json.loads(pie_result)
                    e["pie"] = pie_data
                    # Appliquer label Gmail projet
                    projet = pie_data.get("projet", "")
                    label_key = f"!PKA/{projet}" if projet else None
                    if label_key and label_key in pka_labels and e.get("msg_id"):
                        apply_label(gmail_service, e["msg_id"], pka_labels[label_key])
                        archive_from_inbox(gmail_service, e["msg_id"])
                        labels_applied.append((e["sender_name"], label_key))
                    # Route vers Jade si langue non FR/EN
                    if pie_data.get("langue", "FR") not in ("FR", "EN"):
                        conn = sqlite3.connect(DB_PATH)
                        conn.execute(
                            "INSERT INTO inbox (direction, from_name, to_name, subject, body, status) "
                            "VALUES ('JCH→TEAM', 'JCH', 'Jade', ?, ?, 'pending')",
                            (f"[EMAIL {pie_data['langue']}] {e['subject']}",
                             f"De: {e['sender_name']} <{e['sender_email']}>")
                        )
                        conn.commit()
                        conn.close()
                        routed.append(f"Jade ({pie_data['langue']})")
                except (json.JSONDecodeError, Exception):
                    pass
                fname = save_analysis("Pie", e["sender_name"], e["subject"], pie_result)
                analyses_saved.append(fname)

            # Analyze with specialist if score high enough
            if e["score"] >= 2:
                for specialist in ["Renard", "Vasco", "Bruno"]:
                    if specialist in routed:
                        analysis = analyze_email(
                            specialist,
                            e["sender_name"], e["sender_email"],
                            e["subject"], body
                        )
                        if analysis:
                            fname = save_analysis(
                                specialist, e["sender_name"],
                                e["subject"], analysis
                            )
                            analyses_saved.append(fname)
                            spec = SPECIALISTS[specialist]
                            _push_alert(
                                NTFY_TOPIC,
                                f"{spec['emoji']} {specialist} — analyse prête",
                                f"{e['sender_name']}: {e['subject'][:50]}\n→ {fname}",
                                priority=4
                            )

    send_ntfy(emails, len(emails), new_count, today_events, routing_summary)
    send_digest_email(gmail_service, emails, new_count, today_events, routing_summary, analyses_saved, labels_applied)
    save_digest_log(emails, new_count, routing_summary, analyses_saved)
    save_last_run()


if __name__ == "__main__":
    main()
