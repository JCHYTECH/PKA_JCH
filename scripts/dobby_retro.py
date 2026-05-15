#!/usr/bin/env python3
"""
dobby_retro.py
Dobby 🦉 — rétrospective quotidienne des sessions Claude Code.
Lit les transcripts du jour, identifie les inefficacités, sauvegarde les insights.
Tourne à 23h après Sybil.
"""

import json
import sqlite3
from datetime import date, datetime, timezone
from pathlib import Path

import anthropic

# ── CONFIG ──────────────────────────────────────────────────────
BASE_DIR      = Path(__file__).resolve().parent
PKA_DIR       = BASE_DIR.parent
DB_PATH       = PKA_DIR / "TEAM" / "team.db"
SESSIONS_DIR  = Path.home() / ".claude/projects/-Users-jchavauxm5"
RETRO_DIR     = PKA_DIR / "wiki" / "Daily"
SECRETS_DIR   = Path.home() / ".config" / "pka-jch"
ANTHROPIC_KEY = (SECRETS_DIR / "anthropic_key.txt").read_text().strip()

MAX_TRANSCRIPT_CHARS = 12000

DOBBY_SYSTEM = """Tu es Dobby 🦉, orchestrateur du système PKA de Jean-Claude Havaux.
Tu analyses les transcripts de sessions de travail entre JCH et toi-même (Claude Code).
Ton objectif : identifier les inefficacités, les mauvaises routes de réflexion, les allers-retours évitables, les oublis de coordination.

Tu produis une rétrospective structurée en markdown avec ces sections :
## Ce qui a bien fonctionné
## Inefficacités détectées
## Causes racines identifiées
## Règles à mémoriser pour les prochaines sessions

Sois direct et précis. Cite des exemples concrets du transcript. Ne te ménage pas — l'objectif est de t'améliorer.
Output : markdown pur, prêt à écrire dans un fichier."""
# ────────────────────────────────────────────────────────────────


def extract_today_transcript():
    """Lire tous les JSONL du jour et extraire les échanges user/assistant."""
    today = date.today().isoformat()
    exchanges = []

    for jsonl_file in sorted(SESSIONS_DIR.glob("*.jsonl"),
                             key=lambda f: f.stat().st_mtime, reverse=True):
        # Ignorer les fichiers non modifiés aujourd'hui
        mtime = datetime.fromtimestamp(jsonl_file.stat().st_mtime).date().isoformat()
        if mtime != today:
            continue

        with open(jsonl_file, encoding="utf-8") as fh:
            for line in fh:
                try:
                    d = json.loads(line)
                except json.JSONDecodeError:
                    continue

                ts = d.get("timestamp", "")
                if ts and not ts.startswith(today):
                    continue

                if d.get("type") not in ("user", "assistant"):
                    continue

                msg = d.get("message", {})
                role = d.get("type")
                content = msg.get("content", "")

                if isinstance(content, list):
                    text = " ".join(
                        c.get("text", "") for c in content
                        if isinstance(c, dict) and c.get("type") == "text"
                    ).strip()
                else:
                    text = str(content).strip()

                if text:
                    exchanges.append((role, text))

    return exchanges


def build_transcript(exchanges):
    """Formater les échanges en texte lisible, tronqué si nécessaire."""
    lines = []
    for role, text in exchanges:
        label = "JCH" if role == "user" else "Claude"
        lines.append(f"[{label}] {text[:500]}")

    full = "\n".join(lines)
    if len(full) > MAX_TRANSCRIPT_CHARS:
        full = full[:MAX_TRANSCRIPT_CHARS] + "\n\n[... transcript tronqué ...]"
    return full


def call_dobby(transcript, today_str):
    client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
    prompt = (
        f"Voici le transcript de la session de travail du {today_str} entre JCH et Claude Code :\n\n"
        f"{transcript}\n\n"
        f"Produis la rétrospective de cette session."
    )
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=2000,
        system=DOBBY_SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


def save_retro_md(today_str, content):
    year  = today_str[:4]
    month = today_str[5:7]
    dest_dir = RETRO_DIR / year / month
    dest_dir.mkdir(parents=True, exist_ok=True)

    filepath = dest_dir / f"{today_str}-dobby-retro.md"
    header = (
        f"---\ndate: {today_str}\ntype: retrospective\nauthor: Dobby\ntags: [retro, meta]\n---\n\n"
        f"# Rétrospective — {today_str}\n\n"
    )
    filepath.write_text(header + content, encoding="utf-8")
    return str(filepath)


def save_retro_db(today_str, content):
    """Stocker les règles extraites dans knowledge pour mémoire persistante."""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("""
            INSERT OR IGNORE INTO knowledge (title, body, type, tags, created_by)
            VALUES (?, ?, 'insight', 'retrospective,meta,dobby', 'Dobby')
        """, (f"Rétro {today_str}", content[:3000]))
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"[retro DB] erreur : {e}")


def main():
    today_str = date.today().isoformat()
    print(f"[Dobby] Rétrospective {today_str}…")

    exchanges = extract_today_transcript()
    if not exchanges:
        print("[Dobby] Aucune session détectée aujourd'hui — rétrospective annulée.")
        return

    print(f"[Dobby] {len(exchanges)} échanges trouvés.")
    transcript = build_transcript(exchanges)

    retro = call_dobby(transcript, today_str)
    filepath = save_retro_md(today_str, retro)
    save_retro_db(today_str, retro)

    print(f"[Dobby] Rétrospective écrite → {filepath}")


if __name__ == "__main__":
    main()
