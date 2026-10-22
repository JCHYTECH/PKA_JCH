#!/usr/bin/env python3
"""
pka_memory_eval.py — Banc d'essai de la mémoire PKA (P1).

Mesure ce que le coût par session ne dit pas : est-ce que le retriever trouve
la bonne information, et à quel prix en tokens ?

Métriques produites par question :
  - hit@k      : la réponse attendue apparaît-elle dans les k résultats ?
  - rang       : position du premier résultat pertinent
  - tokens     : tokens consommés par le contexte retourné
  - latence    : ms

Usage :
  python3 scripts/pka_memory_eval.py                 # run complet, mode graphique
  python3 scripts/pka_memory_eval.py --k 5
  python3 scripts/pka_memory_eval.py --json          # sortie machine
  python3 scripts/pka_memory_eval.py --save          # écrit le rapport dans memory-eval/

Le banc ne dépend pas de pka_retrieve : il interroge les sources directement,
ce qui permet de comparer FTS / graphify / MEMORY.md séparément.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

PKA_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PKA_ROOT / "TEAM" / "team.db"
MEMORY_PATH = PKA_ROOT / "MEMORY.md"
WIKI_PATH = PKA_ROOT / "wiki"
GRAPH_PATH = PKA_ROOT / "graphify-out" / "graph.json"
EVAL_DIR = PKA_ROOT / "JCH_Inbox" / "03_PROJECTS" / "01_AI_IT_TOOLS" / "memory-eval"
QUESTIONS_PATH = EVAL_DIR / "questions.json"


def approx_tokens(text: str) -> int:
    """Estimation ~4 chars/token (suffisant pour comparer des configurations)."""
    return max(1, len(text) // 4)


# ── Sources ────────────────────────────────────────────────────────────────
def src_fts(query: str, k: int) -> list[dict]:
    """FTS5 sur les sessions + knowledge."""
    out = []
    try:
        c = sqlite3.connect(DB_PATH)
        # Requête FTS : termes OR-és pour éviter les échecs sur stopwords
        terms = [t for t in re.findall(r"\w+", query) if len(t) > 2][:6]
        if not terms:
            return []
        match = " OR ".join(terms)
        for row in c.execute(
            "SELECT session_id, date, snippet(session_fts, 4, '', '', '…', 20) AS s "
            "FROM session_fts WHERE session_fts MATCH ? LIMIT ?", (match, k)):
            out.append({"source": "fts-sessions", "title": row[0], "date": row[1],
                        "body": row[2] or ""})
        for row in c.execute(
            "SELECT title, body FROM knowledge WHERE (title LIKE ? OR body LIKE ?) "
            "AND status='active' LIMIT ?",
            (f"%{terms[0]}%", f"%{terms[0]}%", k)):
            out.append({"source": "fts-knowledge", "title": row[0], "body": row[1] or ""})
        c.close()
    except sqlite3.Error:
        pass
    return out


def src_memory(query: str, k: int) -> list[dict]:
    """MEMORY.md — entrées contenant un des termes."""
    out = []
    if not MEMORY_PATH.exists():
        return []
    terms = [t.lower() for t in re.findall(r"\w+", query) if len(t) > 3]
    try:
        for i, line in enumerate(MEMORY_PATH.read_text(encoding="utf-8").splitlines()):
            low = line.lower()
            if line.strip().startswith("-") and any(t in low for t in terms):
                out.append({"source": "memoire", "title": f"MEMORY.md:{i+1}",
                            "body": line.strip()[:400]})
                if len(out) >= k:
                    break
    except OSError:
        pass
    return out


def src_graphify(query: str, k: int) -> list[dict]:
    out = []
    try:
        r = subprocess.run(["graphify", "query", query], capture_output=True,
                           text=True, timeout=45)
        if r.returncode == 0 and r.stdout.strip():
            for line in r.stdout.strip().splitlines()[:k]:
                out.append({"source": "graphify", "title": line[:90], "body": line})
    except (subprocess.SubprocessError, FileNotFoundError, OSError):
        pass
    return out


SOURCES = {"fts": src_fts, "memoire": src_memory, "graphify": src_graphify}


# ── Évaluation ─────────────────────────────────────────────────────────────
def evaluate(questions: list[dict], k: int, sources: list[str]) -> list[dict]:
    results = []
    for q in questions:
        hits = []
        t0 = time.time()
        for name in sources:
            try:
                hits.extend(SOURCES[name](q["question"], k))
            except Exception as exc:  # une source qui casse ne stoppe pas le banc
                hits.append({"source": name, "title": f"[ERREUR] {exc}", "body": ""})
        latency = int((time.time() - t0) * 1000)

        expect = [e.lower() for e in q.get("expect_any", [])]
        rank = None
        matched_in = None
        for pos, h in enumerate(hits, 1):
            blob = f"{h.get('title','')} {h.get('body','')}".lower()
            if any(e in blob for e in expect):
                rank = pos
                matched_in = h["source"]
                break

        tokens = sum(approx_tokens(f"{h.get('title','')} {h.get('body','')}")
                     for h in hits[:k])
        results.append({
            "id": q["id"],
            "category": q.get("category", "?"),
            "hit": rank is not None,
            "rank": rank,
            "found_in": matched_in,
            "expected_source": q.get("expect_source"),
            "source_ok": (matched_in == q.get("expect_source")) if matched_in else False,
            "n_results": len(hits),
            "tokens": tokens,
            "latency_ms": latency,
        })
    return results


def summarize(results: list[dict]) -> dict:
    n = len(results) or 1
    hits = [r for r in results if r["hit"]]
    ranks = [r["rank"] for r in hits]
    return {
        "questions": len(results),
        "hit@k": round(len(hits) / n * 100, 1),
        "hit_rate": round(len(hits) / n, 3),
        "mrr": round(sum(1 / r for r in ranks) / n, 3) if ranks else 0.0,
        "avg_rank": round(sum(ranks) / len(ranks), 2) if ranks else None,
        "avg_tokens": round(sum(r["tokens"] for r in results) / n),
        "avg_latency_ms": round(sum(r["latency_ms"] for r in results) / n),
        "source_match": round(sum(1 for r in hits if r["source_ok"]) / n * 100, 1),
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--k", type=int, default=5)
    p.add_argument("--json", action="store_true")
    p.add_argument("--save", action="store_true")
    p.add_argument("--sources", default="fts,memoire,graphify")
    p.add_argument("--questions", default=str(QUESTIONS_PATH))
    args = p.parse_args()

    qpath = Path(args.questions)
    if not qpath.exists():
        print(f"Questions introuvables : {qpath}", file=sys.stderr)
        return 1
    questions = json.loads(qpath.read_text(encoding="utf-8"))["questions"]
    sources = [s.strip() for s in args.sources.split(",") if s.strip() in SOURCES]

    results = evaluate(questions, args.k, sources)
    summary = summarize(results)

    report = {
        "generated": datetime.now().isoformat(timespec="seconds"),
        "k": args.k,
        "sources": sources,
        "summary": summary,
        "results": results,
    }

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"Memory eval — {summary['questions']} questions, k={args.k}, "
              f"sources={','.join(sources)}")
        print(f"  hit@k        : {summary['hit@k']}%")
        print(f"  MRR          : {summary['mrr']}")
        print(f"  source match : {summary['source_match']}%")
        print(f"  tokens/req   : {summary['avg_tokens']}")
        print(f"  latence      : {summary['avg_latency_ms']} ms\n")
        print("  Détail par catégorie :")
        cats: dict[str, list] = {}
        for r in results:
            cats.setdefault(r["category"], []).append(r)
        for cat, rs in sorted(cats.items()):
            h = sum(1 for r in rs if r["hit"])
            print(f"    {cat:16} {h}/{len(rs)} hit")
        misses = [r["id"] for r in results if not r["hit"]]
        if misses:
            print(f"\n  Manquées : {', '.join(misses)}")

    if args.save:
        EVAL_DIR.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        out = EVAL_DIR / f"run-{ts}.json"
        out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nRapport : {out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
