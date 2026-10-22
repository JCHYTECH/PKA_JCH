#!/usr/bin/env python3
"""
ai_image_check_hook.py — Hook de rappel sur usage de pka_ai_image_check.

Décision JCH 2026-10-22 : on reste au niveau 1 (provenance). Dès que l'outil
est utilisé en conditions réelles, rappeler qu'il faut creuser la piste
« entraîner un détecteur sur les propres photos de JCH ».

Ce module s'importe en tête de pka_ai_image_check.py. À chaque exécution il :
  1. écrit une ligne d'audit dans team.db → table ai_image_checks
  2. affiche le rappel sur stderr (jamais sur stdout, pour ne pas casser --json)

Usage direct (test) :
    python3 scripts/ai_image_check_hook.py --test
    python3 scripts/ai_image_check_hook.py --status
"""
from __future__ import annotations

import argparse
import sqlite3
import sys
from datetime import datetime, date
from pathlib import Path

PKA_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PKA_ROOT / "TEAM" / "team.db"
MEMORY_PATH = PKA_ROOT / "MEMORY.md"

REMINDER = (
    "\n" + "─" * 68 + "\n"
    "⚠️  RAPPEL (décision JC 2026-10-22) — outil de détection IA utilisé.\n"
    "    On est restés au niveau 1 (provenance C2PA/EXIF).\n"
    "    → Il faut creuser la piste : ENTRAÎNER UN DÉTECTEUR SUR LES PHOTOS DE JCH.\n"
    "    C'est la seule voie pour détecter une image PARTIELLEMENT générée\n"
    "    (les classifieurs publics sont mesurés inutilisables : 12/12 faux positifs).\n"
    "    Réf. : 05_PHOTO_AI_JURY/ai-image-detection.md § Pistes\n"
    + "─" * 68 + "\n"
)

SCHEMA = """
CREATE TABLE IF NOT EXISTS ai_image_checks (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    ts        TEXT NOT NULL DEFAULT (datetime('now')),
    run_date  TEXT NOT NULL,
    invocation TEXT,
    n_files   INTEGER DEFAULT 0,
    source    TEXT DEFAULT 'cli'
);
CREATE INDEX IF NOT EXISTS idx_ai_checks_date ON ai_image_checks(run_date);
"""


def _conn() -> sqlite3.Connection:
    c = sqlite3.connect(DB_PATH)
    c.executescript(SCHEMA)
    return c


def record_and_remind(invocation: str = "", n_files: int = 0,
                      quiet: bool = False) -> None:
    """Appelé par pka_ai_image_check.main(). Ne doit jamais lever d'exception."""
    today = date.today().isoformat()
    try:
        c = _conn()
        c.execute(
            "INSERT INTO ai_image_checks (run_date, invocation, n_files) "
            "VALUES (?,?,?)", (today, invocation[:300], n_files))
        # Combien de fois aujourd'hui ?
        n_today = c.execute(
            "SELECT COUNT(*) FROM ai_image_checks WHERE run_date=?",
            (today,)).fetchone()[0]
        c.commit()
        c.close()
    except sqlite3.Error:
        n_today = 0

    if quiet:
        return
    msg = REMINDER
    if n_today > 1:
        msg += f"    ({n_today}ᵉ utilisation aujourd'hui)\n"
    print(msg, file=sys.stderr, flush=True)


def write_memory_note(note: str) -> bool:
    """Ajoute une entrée datée en tête de MEMORY.md (idempotent par jour)."""
    today = date.today().isoformat()
    entry = f"- [{today}] [RAPPEL — Détection IA] : {note}"
    try:
        text = MEMORY_PATH.read_text(encoding="utf-8")
    except OSError:
        return False
    if entry in text:
        return True  # déjà présent aujourd'hui
    anchor = "> Dernière mise à jour"
    idx = text.find("\n", text.find(anchor))
    if idx == -1:
        return False
    new = text[:idx + 1] + "\n" + entry + "\n" + text[idx + 1:]
    MEMORY_PATH.write_text(new, encoding="utf-8")
    return True


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--test", action="store_true", help="Déclencher le rappel")
    p.add_argument("--status", action="store_true", help="Historique d'utilisation")
    p.add_argument("--to-memory", action="store_true",
                   help="Écrire le rappel dans MEMORY.md")
    args = p.parse_args()

    if args.status:
        try:
            c = _conn()
            rows = c.execute(
                "SELECT run_date, COUNT(*), MAX(ts) FROM ai_image_checks "
                "GROUP BY run_date ORDER BY run_date DESC LIMIT 10").fetchall()
            c.close()
        except sqlite3.Error as exc:
            print(f"Erreur DB : {exc}", file=sys.stderr)
            return 1
        if not rows:
            print("Aucune utilisation enregistrée.")
            return 0
        print("Utilisations de pka_ai_image_check :")
        for d, n, last in rows:
            print(f"  {d}  {n:>3} exécution(s)  (dernière : {last})")
        return 0

    if args.to_memory:
        ok = write_memory_note(
            "outil `pka_ai_image_check` utilisé → creuser l'entraînement d'un "
            "détecteur sur les photos JCH (niveau 1 seulement en attendant).")
        print("MEMORY.md mis à jour." if ok else "Échec (déjà présent ou fichier introuvable).")
        return 0

    # --test ou défaut
    record_and_remind(invocation="--test", n_files=0)
    return 0


if __name__ == "__main__":
    sys.exit(main())
