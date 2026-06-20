#!/usr/bin/env python3
"""
PKA Unified Retrieval — recherche unifiée multi-sources pour PKA.

Traduit une question en langage naturel en requêtes sur :
  - team.db (knowledge, journal, ideas, retro_patterns)
  - graphify (knowledge graph traversal)
  - file_index (recherche par nom de fichier)
  - MEMORY.md + wiki/ (grep textuel)

Usage:
    python3 scripts/pka_retrieve.py "qu'est-ce qu'on a décidé pour le deep sleep ESP32 ?"
    python3 scripts/pka_retrieve.py --project WILDNEXUS "état du BOM"
    python3 scripts/pka_retrieve.py --fts "budget WildNexus mars 2026"
    python3 scripts/pka_retrieve.py --json "bme688 capteur"

Part of PKA Memory Layer — docs/system/pka-memory-layer.md
"""

import json
import os
import re
import sqlite3
import subprocess
import sys
from pathlib import Path

# ─── Configuration ───────────────────────────────────────────────

PKA_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(PKA_ROOT, "TEAM", "team.db")
GRAPHIFY_BIN = os.path.expanduser("~/.local/bin/graphify")
GRAPH_PATH = os.path.join(PKA_ROOT, "graphify-out", "graph.json")
MEMORY_PATH = os.path.join(PKA_ROOT, "MEMORY.md")
WIKI_PATH = os.path.join(PKA_ROOT, "wiki")
MAX_RESULTS = 10


# ─── Sources ──────────────────────────────────────────────────────

def search_db(query, project=None, limit=MAX_RESULTS):
    """Recherche dans team.db — table knowledge."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    sql = """SELECT title, body, type, source, created_at, tags
             FROM knowledge
             WHERE status = 'active'
               AND (title LIKE ? OR body LIKE ? OR tags LIKE ?)"""
    params = [f"%{query}%", f"%{query}%", f"%{query}%"]

    if project:
        sql += " AND (tags LIKE ? OR source LIKE ?)"
        params.extend([f"%{project}%", f"%{project}%"])

    sql += " ORDER BY created_at DESC LIMIT ?"
    params.append(limit)

    rows = conn.execute(sql, params).fetchall()
    conn.close()

    return [{
        "source": "team.db/knowledge",
        "title": r["title"],
        "body": r["body"][:300] if r["body"] else "",
        "type": r["type"],
        "date": r["created_at"],
        "relevance": "high" if query.lower() in (r["title"] + (r["body"] or "")).lower() else "medium"
    } for r in rows]


def search_graphify(query, limit=MAX_RESULTS):
    """Recherche via graphify si disponible."""
    if not os.path.exists(GRAPHIFY_BIN) or not os.path.exists(GRAPH_PATH):
        return []

    try:
        result = subprocess.run(
            [GRAPHIFY_BIN, "query", query, "--graph", GRAPH_PATH],
            capture_output=True, text=True, timeout=10, cwd=PKA_ROOT
        )
        if result.returncode == 0 and result.stdout.strip():
            lines = result.stdout.strip().split("\n")[:limit]
            return [{
                "source": "graphify",
                "title": f"Graph: {line[:80]}",
                "body": line[:300],
                "type": "graph_edge",
                "date": "",
                "relevance": "medium"
            } for line in lines if line.strip()]
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass
    return []


def search_file_index(query, limit=MAX_RESULTS):
    """Recherche dans l'index de fichiers team.db."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    try:
        rows = conn.execute(
            """SELECT file_path, file_name, description, project_key, updated_at
               FROM file_index
               WHERE file_name LIKE ? OR description LIKE ?
               ORDER BY updated_at DESC LIMIT ?""",
            (f"%{query}%", f"%{query}%", limit)
        ).fetchall()
    except sqlite3.OperationalError:
        conn.close()
        return []

    conn.close()
    return [{
        "source": "file_index",
        "title": r["file_name"] or r["file_path"],
        "body": r["description"] or "",
        "type": "file",
        "date": r["updated_at"] or "",
        "relevance": "medium"
    } for r in rows]


def search_memory_md(query, limit=MAX_RESULTS):
    """Recherche dans MEMORY.md."""
    if not os.path.exists(MEMORY_PATH):
        return []
    with open(MEMORY_PATH) as f:
        lines = f.readlines()

    results = []
    for i, line in enumerate(lines):
        if query.lower() in line.lower():
            # Prend le contexte (2 lignes avant, 2 après)
            start = max(0, i - 2)
            end = min(len(lines), i + 3)
            context = "".join(lines[start:end]).strip()
            results.append({
                "source": "MEMORY.md",
                "title": f"Ligne {i+1}",
                "body": context[:300],
                "type": "memory_entry",
                "date": "",
                "relevance": "high" if query.lower() in line.lower() else "medium"
            })
            if len(results) >= limit:
                break
    return results


def search_wiki(query, limit=MAX_RESULTS):
    """Recherche dans le vault wiki/."""
    if not os.path.isdir(WIKI_PATH):
        return []
    results = []
    for root, dirs, files in os.walk(WIKI_PATH):
        for f in files:
            if f.endswith(".md"):
                fpath = os.path.join(root, f)
                try:
                    with open(fpath) as fh:
                        content = fh.read()
                    if query.lower() in content.lower():
                        # Extrait un extrait contextuel
                        idx = content.lower().find(query.lower())
                        start = max(0, idx - 100)
                        end = min(len(content), idx + 200)
                        snippet = content[start:end].replace("\n", " ")
                        results.append({
                            "source": f"wiki/{os.path.relpath(fpath, WIKI_PATH)}",
                            "title": f.replace(".md", ""),
                            "body": snippet[:300],
                            "type": "wiki",
                            "date": "",
                            "relevance": "high"
                        })
                except (IOError, UnicodeDecodeError):
                    pass
                if len(results) >= limit:
                    return results
    return results


def search_retro(query, project=None, limit=MAX_RESULTS):
    """Recherche dans retro_patterns."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    sql = """SELECT pattern_type, content, source, created_at
             FROM retro_patterns
             WHERE content LIKE ?"""
    params = [f"%{query}%"]

    if project:
        sql += " AND (source LIKE ? OR content LIKE ?)"
        params.extend([f"%{project}%", f"%{project}%"])

    sql += " ORDER BY created_at DESC LIMIT ?"
    params.append(limit)

    try:
        rows = conn.execute(sql, params).fetchall()
    except sqlite3.OperationalError:
        conn.close()
        return []

    conn.close()
    return [{
        "source": "team.db/retro_patterns",
        "title": f"Pattern: {r['pattern_type']}",
        "body": r["content"][:300],
        "type": "retro_pattern",
        "date": r["created_at"],
        "relevance": "medium"
    } for r in rows]


# ─── Consolidation ────────────────────────────────────────────────

def retrieve(query, project=None, limit=MAX_RESULTS):
    """Point d'entrée unifié — interroge toutes les sources."""
    all_results = []

    # Parallélisable — exécution séquentielle pour simplicité
    all_results.extend(search_db(query, project, limit))
    all_results.extend(search_retro(query, project, limit))
    all_results.extend(search_memory_md(query, limit))
    all_results.extend(search_file_index(query, limit))
    all_results.extend(search_wiki(query, limit))
    all_results.extend(search_graphify(query, limit))

    # Tri par pertinence (high > medium) puis par source
    all_results.sort(key=lambda r: (
        0 if r["relevance"] == "high" else 1,
        r["source"]
    ))

    return all_results[:limit * 2]  # un peu plus large car consolidation


def format_results(results, json_output=False):
    """Formate les résultats pour affichage."""
    if json_output:
        return json.dumps(results, indent=2, ensure_ascii=False)

    if not results:
        return "Aucun résultat trouvé."

    lines = [f"📊 {len(results)} résultats :\n"]
    for i, r in enumerate(results, 1):
        source_icon = {
            "team.db/knowledge": "🧠",
            "team.db/retro_patterns": "🔄",
            "MEMORY.md": "📋",
            "file_index": "📁",
            "graphify": "🕸️",
        }.get(r["source"], "📄")

        lines.append(f"{i}. {source_icon} [{r['source']}] {r['title']}")
        if r["body"]:
            lines.append(f"   {r['body'][:200]}")
        if r["date"]:
            lines.append(f"   📅 {r['date']}")
        lines.append("")

    return "\n".join(lines)


# ─── Main ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="PKA Unified Retrieval")
    parser.add_argument("query", nargs="?", help="Requête en langage naturel")
    parser.add_argument("--project", "-p", help="Filtrer par projet (ex: WILDNEXUS)")
    parser.add_argument("--json", "-j", action="store_true", help="Sortie JSON")
    parser.add_argument("--limit", "-n", type=int, default=MAX_RESULTS,
                        help=f"Nombre max de résultats par source (défaut: {MAX_RESULTS})")
    parser.add_argument("--fts", action="store_true",
                        help="Activer la recherche FTS5 dans les sessions indexées")

    args = parser.parse_args()

    if not args.query:
        parser.print_help()
        sys.exit(1)

    if args.fts:
        # Recherche FTS5 + sources existantes
        try:
            with sqlite3.connect(DB_PATH) as con:
                fts_rows = con.execute(
                    """SELECT session_id, date, model, project,
                              snippet(session_fts, 2, '<b>', '</b>', '...', 40) AS snippet
                       FROM session_fts
                       WHERE session_fts MATCH ?
                       ORDER BY rank
                       LIMIT ?""",
                    (args.query, args.limit),
                ).fetchall()

            fts_results = [
                {
                    "source": "session_fts",
                    "title": f"Session {r[0]} [{r[1]}]",
                    "body": f"Modèle: {r[2]} | Projet: {r[3]}\n{r[4]}",
                    "date": r[1],
                }
                for r in fts_rows
            ]
        except sqlite3.DatabaseError:
            fts_results = []

    results = retrieve(args.query, args.project, args.limit)
    if args.fts:
        results = fts_results + results
    print(format_results(results, args.json))