#!/usr/bin/env python3
"""
dobby_codex_bridge.py  🦉  — Pont mémoire Dobby ↔ Codex CLI

Bidirectionnel :
  ⬆ Dobby → Codex : écrit les patterns rétro dans la mémoire Codex
  ⬇ Codex → Dobby : importe les goals Codex dans le système de rétro

Usage :
    python3 scripts/dobby_codex_bridge.py                    # sync bidirectionnel
    python3 scripts/dobby_codex_bridge.py --to-codex         # Dobby → Codex seulement
    python3 scripts/dobby_codex_bridge.py --from-codex       # Codex → Dobby seulement
    python3 scripts/dobby_codex_bridge.py --status            # voir ce qu'il y a des deux côtés
"""

import json
import os
import sqlite3
import sys
import time
from datetime import date, datetime
from pathlib import Path

# ── CHEMINS ──────────────────────────────────────────────────────────
PKA_DIR = Path(__file__).resolve().parent.parent
DB_PATH = PKA_DIR / "TEAM" / "team.db"
CODEX_DIR = Path.home() / ".codex"
CODEX_MEMORIES = CODEX_DIR / "memories_1.sqlite"
CODEX_GOALS = CODEX_DIR / "goals_1.sqlite"
CODEX_HISTORY = CODEX_DIR / "history.jsonl"


# ── DOBBY → CODEX ─────────────────────────────────────────────────────

def push_patterns_to_codex():
    """Écrit les patterns rétro Dobby dans la mémoire Codex CLI."""
    if not DB_PATH.exists():
        print("[bridge] team.db introuvable")
        return 0

    if not CODEX_MEMORIES.exists():
        print("[bridge] Codex memories DB introuvable")
        return 0

    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        c.execute("SELECT name FROM sqlite_master WHERE name='retro_patterns'")
        if not c.fetchone():
            print("[bridge] Table retro_patterns absente")
            conn.close()
            return 0

        c.execute("""
            SELECT pattern_type, content, date, id FROM retro_patterns
            ORDER BY id DESC LIMIT 30
        """)
        patterns = c.fetchall()
        conn.close()

        if not patterns:
            print("[bridge] Aucun pattern à écrire")
            return 0

        codex_conn = sqlite3.connect(CODEX_MEMORIES)
        codex_c = codex_conn.cursor()

        now_ts = int(time.time())
        written = 0
        for ptype, content, pdate, pid in patterns:
            raw = json.dumps({
                "source": "dobby_retro",
                "type": ptype,
                "date": pdate,
                "content": content,
                "pka_id": pid,
            }, ensure_ascii=False)

            codex_c.execute(
                "SELECT thread_id FROM stage1_outputs WHERE raw_memory = ? LIMIT 1",
                (raw,),
            )
            if codex_c.fetchone():
                continue

            codex_c.execute("""
                INSERT INTO stage1_outputs
                (thread_id, source_updated_at, raw_memory, rollout_summary,
                 rollout_slug, generated_at, usage_count, last_usage,
                 selected_for_phase2)
                VALUES (?, ?, ?, ?, ?, ?, 0, 0, 1)
            """, (
                f"pka_dobby_{pid}",
                0,
                raw,
                f"[PKA] {ptype}: {content[:120]}",
                f"pka_dobby_{ptype}",
                now_ts,
            ))
            written += 1

        codex_conn.commit()
        codex_conn.close()
        print(f"[bridge] ✅ {written} patterns écrits dans Codex memories")
        return written

    except (OSError, sqlite3.DatabaseError) as e:
        print(f"[bridge] Erreur écriture Codex: {e}")
        return 0


# ── CODEX → DOBBY ─────────────────────────────────────────────────────

def pull_goals_from_codex():
    """Importe les goals Codex CLI dans team.db retro_patterns."""
    if not CODEX_GOALS.exists():
        print("[bridge] Codex goals DB introuvable")
        return 0

    if not DB_PATH.exists():
        print("[bridge] team.db introuvable")
        return 0

    try:
        codex_conn = sqlite3.connect(CODEX_GOALS)
        c = codex_conn.cursor()

        c.execute("SELECT name FROM sqlite_master WHERE name='thread_goals'")
        if not c.fetchone():
            codex_conn.close()
            return 0

        c.execute("""
            SELECT thread_id, objective, status, created_at_ms, updated_at_ms
            FROM thread_goals WHERE status = 'active'
            ORDER BY updated_at_ms DESC LIMIT 20
        """)
        goals = c.fetchall()
        codex_conn.close()

        if not goals:
            print("[bridge] Aucun goal Codex actif")
            return 0

        today = date.today().isoformat()

        conn = sqlite3.connect(DB_PATH)
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS retro_patterns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                pattern_type TEXT NOT NULL,
                content TEXT NOT NULL,
                source TEXT,
                session_count INTEGER DEFAULT 1,
                created_at TEXT DEFAULT (datetime('now'))
            );
        """)

        c = conn.cursor()
        imported = 0
        for thread_id, objective, status, created_ms, updated_ms in goals:
            created_dt = datetime.fromtimestamp(created_ms / 1000).isoformat()[:10] if created_ms else today
            c.execute(
                "INSERT INTO retro_patterns (date, pattern_type, content, source) VALUES (?, 'codex_goal', ?, 'codex_bridge')",
                (created_dt, objective[:500]),
            )
            imported += 1

        conn.commit()
        conn.close()
        print(f"[bridge] ✅ {imported} goals Codex importés dans retro_patterns")
        return imported

    except (OSError, sqlite3.DatabaseError) as e:
        print(f"[bridge] Erreur import goals: {e}")
        return 0


# ── STATUS ────────────────────────────────────────────────────────────

def show_status():
    """Affiche l'état des deux systèmes."""
    print("=== Dobby → Codex bridge status ===\n")

    if DB_PATH.exists():
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            c.execute("SELECT name FROM sqlite_master WHERE name='retro_patterns'")
            if c.fetchone():
                c.execute("SELECT COUNT(*), pattern_type FROM retro_patterns GROUP BY pattern_type")
                rows = c.fetchall()
                print(f"Dobby retro_patterns: {sum(r[0] for r in rows)} total")
                for r in rows:
                    print(f"  {r[1]}: {r[0]}")
            else:
                print("Dobby retro_patterns: table absente")
            conn.close()
        except Exception as e:
            print(f"Dobby: {e}")
    else:
        print("Dobby team.db: introuvable")

    if CODEX_MEMORIES.exists():
        try:
            conn = sqlite3.connect(CODEX_MEMORIES)
            c = conn.cursor()
            c.execute("SELECT name FROM sqlite_master WHERE name='stage1_outputs'")
            if c.fetchone():
                c.execute("SELECT COUNT(*) FROM stage1_outputs")
                count = c.fetchone()[0]
                c.execute("SELECT COUNT(*) FROM stage1_outputs WHERE rollout_slug LIKE 'pka_dobby_%'")
                pka_count = c.fetchone()[0]
                print(f"\nCodex memories: {count} total ({pka_count} venant de Dobby)")
                c.execute("SELECT DISTINCT rollout_slug FROM stage1_outputs")
                slugs = [r[0] for r in c.fetchall() if r[0]]
                print(f"  Catégories: {slugs[:10]}")
            else:
                print(f"\nCodex memories: table stage1_outputs absente")
            conn.close()
        except Exception as e:
            print(f"\nCodex: {e}")
    else:
        print("\nCodex memories DB: introuvable")

    if CODEX_GOALS.exists():
        try:
            conn = sqlite3.connect(CODEX_GOALS)
            c = conn.cursor()
            c.execute("SELECT name FROM sqlite_master WHERE name='thread_goals'")
            if c.fetchone():
                c.execute("SELECT COUNT(*), status FROM thread_goals GROUP BY status")
                rows = c.fetchall()
                print(f"\nCodex goals: {sum(r[0] for r in rows)} total")
                for r in rows:
                    print(f"  {r[1]}: {r[0]}")
            conn.close()
        except Exception as e:
            print(f"\nCodex goals error: {e}")


# ── CLI ───────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    to_codex = "--to-codex" in args
    from_codex = "--from-codex" in args
    show = "--status" in args

    if show or not (to_codex or from_codex):
        show_status()
        print()

    if to_codex or not (to_codex or from_codex or show):
        push_patterns_to_codex()
        print()

    if from_codex or not (to_codex or from_codex or show):
        pull_goals_from_codex()
        print()

    if not (to_codex or from_codex or show):
        print("---")
        print("Bridge bidirectionnel terminé. Pour actions spécifiques :")
        print("  --to-codex    Dobby → Codex (écrire patterns)")
        print("  --from-codex  Codex → Dobby (importer goals)")
        print("  --status      État des deux systèmes")


if __name__ == "__main__":
    main()
