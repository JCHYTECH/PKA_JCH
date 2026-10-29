#!/usr/bin/env python3
"""
pka_llm_trace.py — Tracing des appels LLM par script (P3).

Chaque script PKA qui appelle un LLM peut logger son appel ici. On obtient
une vue « coût par projet / par script / par modèle » que le coût par session
ne donne pas.

Table : team.db → llm_calls

Usage (bibliothèque) :
    from pka_llm_trace import trace_call
    with trace_call(script="pka_memory_review", project="AI_IT_TOOLS",
                    model="deepseek/deepseek-chat") as t:
        resp = call_llm(...)
        t.record(tokens_in=120, tokens_out=45, cost_usd=0.00003)
        # ou t.fail("timeout")

Usage (CLI) :
    python3 scripts/pka_llm_trace.py init           # crée la table
    python3 scripts/pka_llm_trace.py report         # vue synthétique
    python3 scripts/pka_llm_trace.py report --days 30 --json
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
import time
from contextlib import contextmanager
from datetime import datetime, timedelta
from pathlib import Path

PKA_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PKA_ROOT / "TEAM" / "team.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS llm_calls (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    ts          TEXT NOT NULL DEFAULT (datetime('now')),
    script      TEXT NOT NULL,
    project     TEXT,
    model       TEXT NOT NULL,
    tokens_in   INTEGER DEFAULT 0,
    tokens_out  INTEGER DEFAULT 0,
    cost_usd    REAL DEFAULT 0.0,
    latency_ms  INTEGER DEFAULT 0,
    success     INTEGER DEFAULT 1,
    error       TEXT
);
CREATE INDEX IF NOT EXISTS idx_llm_calls_ts ON llm_calls(ts);
CREATE INDEX IF NOT EXISTS idx_llm_calls_script ON llm_calls(script);
CREATE INDEX IF NOT EXISTS idx_llm_calls_project ON llm_calls(project);
"""


def conn() -> sqlite3.Connection:
    c = sqlite3.connect(DB_PATH)
    c.executescript(SCHEMA)
    return c


def ensure_schema() -> None:
    conn().close()


class _Trace:
    def __init__(self, script: str, project: str | None, model: str):
        self.script = script
        self.project = project
        self.model = model
        self.t0 = time.time()
        self.tokens_in = 0
        self.tokens_out = 0
        self.cost_usd = 0.0
        self.success = 1
        self.error: str | None = None

    def record(self, tokens_in: int = 0, tokens_out: int = 0, cost_usd: float = 0.0) -> None:
        self.tokens_in = tokens_in
        self.tokens_out = tokens_out
        self.cost_usd = cost_usd

    def fail(self, error: str) -> None:
        self.success = 0
        self.error = error[:500]

    def flush(self) -> None:
        latency = int((time.time() - self.t0) * 1000)
        try:
            c = conn()
            c.execute(
                "INSERT INTO llm_calls (script, project, model, tokens_in, tokens_out, "
                "cost_usd, latency_ms, success, error) VALUES (?,?,?,?,?,?,?,?,?)",
                (self.script, self.project, self.model, self.tokens_in, self.tokens_out,
                 self.cost_usd, latency, self.success, self.error),
            )
            c.commit()
            c.close()
        except sqlite3.Error:
            pass  # le tracing ne doit jamais casser l'appelant


@contextmanager
def trace_call(script: str, model: str, project: str | None = None):
    t = _Trace(script, project, model)
    try:
        yield t
    except Exception as exc:
        t.fail(f"{type(exc).__name__}: {exc}")
        raise
    finally:
        t.flush()


# ── CLI ────────────────────────────────────────────────────────────────────
def cmd_init() -> int:
    ensure_schema()
    print(f"Table llm_calls prête dans {DB_PATH}")
    return 0


def cmd_report(days: int, as_json: bool) -> int:
    ensure_schema()
    since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    c = conn()
    c.row_factory = sqlite3.Row

    by_project = [dict(r) for r in c.execute(
        "SELECT COALESCE(project,'(non assigné)') AS project, COUNT(*) AS calls, "
        "SUM(tokens_in+tokens_out) AS tokens, ROUND(SUM(cost_usd),4) AS cost_usd, "
        "ROUND(AVG(latency_ms)) AS avg_ms "
        "FROM llm_calls WHERE substr(ts,1,10) >= ? "
        "GROUP BY project ORDER BY cost_usd DESC", (since,))]

    by_model = [dict(r) for r in c.execute(
        "SELECT model, COUNT(*) AS calls, ROUND(SUM(cost_usd),4) AS cost_usd "
        "FROM llm_calls WHERE substr(ts,1,10) >= ? "
        "GROUP BY model ORDER BY cost_usd DESC", (since,))]

    totals = dict(c.execute(
        "SELECT COUNT(*), ROUND(COALESCE(SUM(cost_usd),0),4), "
        "COALESCE(SUM(tokens_in+tokens_out),0) FROM llm_calls "
        "WHERE substr(ts,1,10) >= ?", (since,)).fetchone())
    c.close()

    if as_json:
        print(json.dumps({"since": since, "totals": totals,
                          "by_project": by_project, "by_model": by_model},
                         indent=2, ensure_ascii=False))
        return 0

    print(f"LLM trace — depuis {since}")
    print(f"  total : {totals['COUNT(*)']} appel(s), "
          f"{totals['COALESCE(SUM(tokens_in+tokens_out),0)']:,} tokens, "
          f"${totals['ROUND(COALESCE(SUM(cost_usd),0),4)']}\n")
    print("  Par projet :")
    for r in by_project:
        print(f"    {r['project'][:28]:28} {r['calls']:>5} appels  ${r['cost_usd']:<9} "
              f"{r['tokens'] or 0:>9,} tok  {r['avg_ms'] or 0:>5} ms")
    if by_model:
        print("\n  Par modèle :")
        for r in by_model:
            print(f"    {r['model'][:34]:34} {r['calls']:>5} appels  ${r['cost_usd']}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd")
    sub.add_parser("init", help="Crée la table llm_calls")
    r = sub.add_parser("report", help="Vue synthétique des coûts")
    r.add_argument("--days", type=int, default=30)
    r.add_argument("--json", action="store_true")
    args = p.parse_args()

    if args.cmd == "init":
        return cmd_init()
    if args.cmd == "report":
        return cmd_report(args.days, args.json)
    p.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
