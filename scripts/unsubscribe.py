#!/usr/bin/env python3
"""unsubscribe.py — Désabonnements mail (validation par lot, mode B).

Flux : JC déplace les mails indésirables dans `00_INBOX/email_triage/_UNSUBSCRIBE/`.
Dobby (scan, toutes les 30 min) extrait le header `List-Unsubscribe`, prépare une
liste en attente (`pending-unsubscribe.json`) et notifie. Après « go » de JC, Dobby
exécute les désabonnements (URL https one-click), ajoute expéditeur + domaine à la
liste noire (`email_blacklist.json`), journalise et déplace les mails traités.

Usage :
  python3 scripts/unsubscribe.py --scan      # détecte + prépare la liste pending
  python3 scripts/unsubscribe.py --list      # affiche la liste pending
  python3 scripts/unsubscribe.py --execute   # exécute les désabonnements validés
"""

from __future__ import annotations

import argparse
import email
import json
import re
import ssl
import urllib.request
from datetime import datetime
from email.header import decode_header, make_header
from pathlib import Path

PKA_DIR = Path(__file__).resolve().parent.parent
TRIAGE = PKA_DIR / "JCH_Inbox" / "00_INBOX" / "email_triage"
UNSUB_DIR = TRIAGE / "_UNSUBSCRIBE"
DONE_DIR = UNSUB_DIR / "_done"
IGNORED_DIR = TRIAGE / "_Ignorés"
PENDING_PATH = PKA_DIR / "_local" / "pending-unsubscribe.json"
BLACKLIST_PATH = PKA_DIR / "JCH_Inbox" / "99_SYSTEM" / "email_blacklist.json"
JOURNAL_PATH = UNSUB_DIR / "journal.md"


def decode_header_value(value: str) -> str:
    try:
        return str(make_header(decode_header(value)))
    except Exception:
        return value or ""


def extract_unsubscribe(eml_path: Path) -> list[str]:
    """Extrait les valeurs List-Unsubscribe (mailto: / https://) d'un .eml."""
    try:
        msg = email.message_from_bytes(eml_path.read_bytes())
        values = msg.get_all("List-Unsubscribe", []) or []
    except Exception:
        return []
    out: list[str] = []
    for v in values:
        v = decode_header_value(v)
        for url in re.findall(r"<(https?://[^>]+|mailto:[^>]+)>", v):
            if url not in out:
                out.append(url.strip())
    return out


def load_pending() -> list[dict]:
    if PENDING_PATH.exists():
        try:
            return json.loads(PENDING_PATH.read_text(encoding="utf-8"))
        except Exception:
            pass
    return []


def save_pending(items: list[dict]) -> None:
    PENDING_PATH.parent.mkdir(parents=True, exist_ok=True)
    PENDING_PATH.write_text(json.dumps(items, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def load_blacklist() -> set[str]:
    if BLACKLIST_PATH.exists():
        try:
            return set(json.loads(BLACKLIST_PATH.read_text(encoding="utf-8")).get("blacklist", []))
        except Exception:
            pass
    return set()


def save_blacklist(entries: set[str]) -> None:
    BLACKLIST_PATH.parent.mkdir(parents=True, exist_ok=True)
    BLACKLIST_PATH.write_text(
        json.dumps({"blacklist": sorted(entries)}, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def is_blacklisted(sender_email: str) -> bool:
    e = sender_email.lower().strip()
    domain = e.split("@")[-1] if "@" in e else ""
    bl = load_blacklist()
    return e in bl or domain in bl


def scan() -> list[dict]:
    """Détecte les nouveaux .eml dans _UNSUBSCRIBE/ et prépare la liste pending."""
    if not UNSUB_DIR.exists():
        return []
    pending = load_pending()
    known = {p["file"] for p in pending}
    changed = False
    for eml in sorted(UNSUB_DIR.glob("*.eml")):
        if eml.name in known:
            continue
        try:
            msg = email.message_from_bytes(eml.read_bytes())
            sender = decode_header_value(msg.get("From", ""))
            subject = decode_header_value(msg.get("Subject", "(sans objet)"))
        except Exception:
            sender, subject = "(illisible)", "(illisible)"
        unsub = extract_unsubscribe(eml)
        pending.append({
            "file": eml.name,
            "sender": sender,
            "subject": subject,
            "unsubscribe": unsub or ["(aucun List-Unsubscribe — à traiter manuellement)"],
            "status": "pending",
        })
        changed = True
    if changed:
        save_pending(pending)
    return pending


def _http_unsubscribe(url: str) -> str:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        urllib.request.urlopen(req, timeout=15, context=ssl.create_default_context())
        return "OK"
    except Exception as exc:
        return f"ÉCHEC ({exc.__class__.__name__})"


def _blacklist_sender(sender: str) -> None:
    m = re.search(r"<([^>]+)>", sender)
    addr = (m.group(1) if m else sender.strip()).lower()
    if "@" not in addr:
        return
    domain = addr.split("@")[-1]
    bl = load_blacklist()
    bl.add(addr)
    bl.add(domain)
    save_blacklist(bl)


def _journal(item: dict) -> None:
    UNSUB_DIR.mkdir(parents=True, exist_ok=True)
    lines = [f"\n## {datetime.now():%Y-%m-%d %H:%M} — {item['sender']}"]
    lines.append(f"- Sujet : {item['subject']}")
    for r in item.get("result", []):
        lines.append(f"- {r['url']} → {r['ok']}")
    with JOURNAL_PATH.open("a", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def execute() -> dict:
    """Exécute les désabonnements pending (après validation JC)."""
    pending = load_pending()
    todo = [p for p in pending if p.get("status") == "pending"]
    done = 0
    DONE_DIR.mkdir(parents=True, exist_ok=True)
    for item in todo:
        result = []
        for u in item["unsubscribe"]:
            if u.startswith("https://"):
                result.append({"url": u, "ok": _http_unsubscribe(u)})
            elif u.startswith("mailto:"):
                result.append({"url": u, "ok": "mailto — envoi non configuré (à faire manuellement)"})
            else:
                result.append({"url": u, "ok": "non traité (pas une URL)"})
        item["status"] = "done"
        item["result"] = result
        item["executed_at"] = datetime.now().isoformat()
        _blacklist_sender(item["sender"])
        _journal(item)
        done += 1
        # déplacer les fichiers traités
        stem = Path(item["file"]).stem
        for f in UNSUB_DIR.glob(f"{stem}.*"):
            try:
                f.rename(DONE_DIR / f.name)
            except OSError:
                pass
    save_pending(pending)
    return {"executed": done, "pending_remaining": len([p for p in pending if p.get("status") == "pending"])}


def main() -> None:
    ap = argparse.ArgumentParser(description="Désabonnements mail (validation par lot)")
    ap.add_argument("--scan", action="store_true", help="Détecte + prépare la liste pending")
    ap.add_argument("--list", action="store_true", help="Affiche la liste pending")
    ap.add_argument("--execute", action="store_true", help="Exécute les désabonnements validés")
    args = ap.parse_args()

    if args.execute:
        r = execute()
        print(f"Exécutés : {r['executed']} · restants : {r['pending_remaining']}")
        return

    if args.scan:
        scan()

    pending = load_pending()
    active = [p for p in pending if p.get("status") == "pending"]
    if args.list or args.scan or not any([args.scan, args.list, args.execute]):
        print(f"{len(active)} désabonnement(s) en attente :")
        for p in active:
            print(f"  • {p['sender']} — {p['subject'][:50]}")
            for u in p["unsubscribe"]:
                print(f"      {u}")
    if active:
        print("\n→ validation JC requise, puis : python3 scripts/unsubscribe.py --execute")


if __name__ == "__main__":
    main()
