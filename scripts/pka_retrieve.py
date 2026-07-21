#!/usr/bin/env python3
"""
PKA Unified Retrieval — recherche unifiée multi-sources pour PKA.

Traduit une question en langage naturel en requêtes sur :
  - team.db (knowledge, journal, ideas, retro_patterns)
  - graphify (knowledge graph traversal)
  - file_index (recherche par nom de fichier)
  - MEMORY.md + wiki/ (grep textuel)
  - Ollama embeddings (recherche sémantique via M1)

Usage:
    python3 scripts/pka_retrieve.py "qu'est-ce qu'on a décidé pour le deep sleep ESP32 ?"
    python3 scripts/pka_retrieve.py --project WILDNEXUS "état du BOM"
    python3 scripts/pka_retrieve.py --fts "budget WildNexus mars 2026"
    python3 scripts/pka_retrieve.py --json "bme688 capteur"
    python3 scripts/pka_retrieve.py --embed "qu'est-ce qu'on a décidé pour le deep sleep ?"

Part of PKA Memory Layer — docs/system/pka-memory-layer.md
"""

import json
import os
import re
import sqlite3
import urllib.request
import urllib.error
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

# Ollama embedding config (M1)
OLLAMA_M1_URL = "http://100.73.212.110:11434"
OLLAMA_EMBED_MODEL = "nomic-embed-text"  # Fast, lightweight, 768-dim
# Fallback: gemma3:12b if nomic-embed-text not available
OLLAMA_EMBED_FALLBACK = "gemma3:12b-it-qat"


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


# ─── Semantic Search (Embedding-based) ─────────────────────────────

def get_embedding(text: str, model: str = None) -> list | None:
    """
    Get embedding vector from Ollama on M1.
    Returns list of floats or None if unavailable.
    """
    if model is None:
        model = OLLAMA_EMBED_MODEL

    try:
        payload = json.dumps({
            "model": model,
            "prompt": text[:512]  # Truncate to avoid OOM
        }).encode("utf-8")

        req = urllib.request.Request(
            f"{OLLAMA_M1_URL}/api/embeddings",
            data=payload,
            headers={"Content-Type": "application/json"}
        )
        resp = urllib.request.urlopen(req, timeout=15)
        body = json.loads(resp.read().decode("utf-8"))
        return body.get("embedding")
    except urllib.error.HTTPError as e:
        # Model might not support /api/embeddings — try fallback
        if e.code == 404 and model != OLLAMA_EMBED_FALLBACK:
            return get_embedding(text, OLLAMA_EMBED_FALLBACK)
        return None
    except Exception:
        return None


def cosine_similarity(a: list, b: list) -> float:
    """Compute cosine similarity between two vectors."""
    if not a or not b or len(a) != len(b):
        return 0.0

    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5

    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def search_embedding(query: str, limit: int = MAX_RESULTS) -> list[dict]:
    """
    Semantic search using Ollama embeddings.
    Computes cosine similarity between query embedding and all facts
    in memory_capture + knowledge.
    Falls back to empty list if Ollama unavailable.
    """
    # Get query embedding
    query_embedding = get_embedding(query)
    if query_embedding is None:
        return []

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    results = []

    # Search memory_capture
    try:
        rows = conn.execute(
            "SELECT id, fact, category, importance, created_at, trust "
            "FROM memory_capture WHERE status='active'"
        ).fetchall()
    except sqlite3.OperationalError:
        rows = conn.execute(
            "SELECT id, fact, category, importance, created_at "
            "FROM memory_capture WHERE status='active'"
        ).fetchall()

    for row in rows:
        fact_text = row["fact"]
        fact_embedding = get_embedding(fact_text)
        if fact_embedding:
            sim = cosine_similarity(query_embedding, fact_embedding)
            if sim > 0.5:  # Threshold
                trust_str = ""
                try:
                    t = row["trust"]
                    if t and t != "internal":
                        trust_str = f" [{t}]"
                except (KeyError, IndexError):
                    pass
                results.append({
                    "source": "memory_capture/embed",
                    "title": f"#{row['id']} [{row['category']}] P{row['importance']}{trust_str}",
                    "body": fact_text[:300],
                    "type": "semantic_match",
                    "date": row["created_at"] or "",
                    "relevance": "high" if sim > 0.75 else "medium",
                    "similarity": round(sim, 3)
                })

    # Search knowledge
    kb_rows = conn.execute(
        "SELECT id, title, body, type, created_at FROM knowledge WHERE status='active'"
    ).fetchall()

    for row in kb_rows:
        kb_text = (row["title"] or "") + " " + (row["body"] or "")
        if len(kb_text) < 10:
            continue
        kb_embedding = get_embedding(kb_text[:512])
        if kb_embedding:
            sim = cosine_similarity(query_embedding, kb_embedding)
            if sim > 0.5:
                results.append({
                    "source": "knowledge/embed",
                    "title": row["title"] or f"Knowledge #{row['id']}",
                    "body": (row["body"] or "")[:300],
                    "type": row["type"] or "note",
                    "date": row["created_at"] or "",
                    "relevance": "high" if sim > 0.75 else "medium",
                    "similarity": round(sim, 3)
                })

    conn.close()

    # Sort by similarity descending
    results.sort(key=lambda r: r.get("similarity", 0), reverse=True)

    # Tag first result as best_match
    if results and results[0].get("similarity", 0) > 0.8:
        results[0]["relevance"] = "best_match"

    return results[:limit]


def check_semantic_available() -> bool:
    """Check if Ollama embeddings are available on M1."""
    try:
        req = urllib.request.Request(f"{OLLAMA_M1_URL}/api/tags", method="GET")
        urllib.request.urlopen(req, timeout=5)
        return True
    except Exception:
        return False


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
        return json.dumps(results, indent=2, ensure_ascii=False, default=str)

    if not results:
        return "Aucun résultat trouvé."

    lines = [f"📊 {len(results)} résultats :"]
    if results and "similarity" in results[0]:
        lines.append(f"   (recherche sémantique — embedding Ollama M1)\n")
    else:
        lines.append("")
    for i, r in enumerate(results, 1):
        source_icon = {
            "team.db/knowledge": "🧠",
            "knowledge/embed": "🧠💫",
            "memory_capture/embed": "📌💫",
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
        if "similarity" in r:
            lines.append(f"   🎯 similarité: {r['similarity']}")
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
    parser.add_argument("--embed", action="store_true",
                        help="Activer la recherche sémantique par embedding (Ollama M1)")
    parser.add_argument("--semantic", action="store_true",
                        help="Alias pour --embed")

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

    # Semantic search via embeddings
    semantic_results = []
    if args.embed or args.semantic:
        if check_semantic_available():
            semantic_results = search_embedding(args.query, args.limit)
            if not semantic_results:
                print("⚠️  Embedding search returned no results (threshold > 0.5)", file=sys.stderr)
        else:
            print("⚠️  Ollama M1 indisponible — recherche sémantique désactivée", file=sys.stderr)

    results = retrieve(args.query, args.project, args.limit)

    # Merge: semantic results first (higher relevance), then keyword results
    if semantic_results:
        results = semantic_results + results

    if args.fts:
        results = fts_results + results
    print(format_results(results, args.json))
