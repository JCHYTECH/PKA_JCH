#!/usr/bin/env python3
"""
pka_fts_index.py — Indexation FTS5 des sessions JSON PKA.
Crée un index full-text dans team.db (session_fts) pour recherche cross-session.

Usage:
    python3 scripts/pka_fts_index.py --all
    python3 scripts/pka_fts_index.py --recent 50
    python3 scripts/pka_fts_index.py --session session_20260619_120000.json

Inspiré de FTS5 session search d'Hermes Agent.
"""

import argparse
import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

PKA_DIR = Path(__file__).resolve().parents[1]
TEAM_DB = PKA_DIR / "TEAM" / "team.db"


def find_session_files() -> list[Path]:
    """Trouve tous les fichiers session_*.json dans PKA_DIR."""
    return sorted(
        PKA_DIR.glob("session_*.json"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )


def extract_session_info(path: Path) -> dict | None:
    """Extrait les infos clés d'un fichier session JSON."""
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, OSError):
        return None

    # Extraire le contenu texte (adapte selon la structure réelle des sessions)
    content_parts = []

    if isinstance(data, dict):
        # Essayer des clés communes
        for key in ("messages", "transcript", "content", "text", "conversation"):
            if key in data:
                val = data[key]
                if isinstance(val, list):
                    for item in val:
                        if isinstance(item, dict):
                            content_parts.append(item.get("content", item.get("text", str(item))))
                        else:
                            content_parts.append(str(item))
                elif isinstance(val, str):
                    content_parts.append(val)

    if not content_parts:
        # Fallback : tout le JSON en texte
        content_parts.append(json.dumps(data, ensure_ascii=False))

    # Aplatir et convertir en str
    flat_parts = []
    for part in content_parts:
        if isinstance(part, str):
            flat_parts.append(part)
        elif isinstance(part, list):
            flat_parts.extend(str(x) for x in part)
        else:
            flat_parts.append(str(part))
    content = " ".join(flat_parts)

    # Métadonnées
    session_id = path.stem
    date = ""
    model = ""
    project = ""

    if isinstance(data, dict):
        meta = data.get("metadata", data.get("meta", {}))
        if isinstance(meta, dict):
            date = meta.get("date", meta.get("timestamp", ""))
            model = meta.get("model", "")
            project = meta.get("project", "")

    # Si pas de date dans metadata, utiliser la date du fichier
    if not date:
        mtime = datetime.fromtimestamp(path.stat().st_mtime)
        date = mtime.strftime("%Y-%m-%d")

    return {
        "session_id": session_id,
        "date": str(date)[:10],
        "model": str(model)[:50],
        "project": str(project)[:50],
        "content": content[:1_000_000],  # max 1M chars par session
        "size_chars": len(content),
    }


def index_sessions(sessions: list[dict], dry_run: bool = False) -> int:
    """Indexe les sessions dans session_fts (team.db)."""
    if dry_run:
        return len(sessions)

    indexed = 0
    try:
        with sqlite3.connect(TEAM_DB) as con:
            for sess in sessions:
                # Vérifier si déjà indexé
                existing = con.execute(
                    "SELECT 1 FROM session_fts WHERE session_id = ?",
                    (sess["session_id"],),
                ).fetchone()
                if existing:
                    continue

                con.execute(
                    """INSERT INTO session_fts
                       (session_id, date, model, project, content)
                       VALUES (?, ?, ?, ?, ?)""",
                    (
                        sess["session_id"],
                        sess["date"],
                        sess["model"],
                        sess["project"],
                        sess["content"],
                    ),
                )
                indexed += 1
    except sqlite3.DatabaseError as e:
        print(f"Erreur DB: {e}", file=sys.stderr)

    return indexed


def search_fts(query: str, limit: int = 10) -> list[dict]:
    """Recherche FTS5 dans les sessions indexées."""
    try:
        with sqlite3.connect(TEAM_DB) as con:
            rows = con.execute(
                """SELECT session_id, date, model, project,
                          snippet(session_fts, 2, '<b>', '</b>', '...', 40) AS snippet
                   FROM session_fts
                   WHERE session_fts MATCH ?
                   ORDER BY rank
                   LIMIT ?""",
                (query, limit),
            ).fetchall()
    except sqlite3.DatabaseError as e:
        print(f"Erreur recherche: {e}", file=sys.stderr)
        return []

    return [
        {
            "session_id": r[0],
            "date": r[1],
            "model": r[2],
            "project": r[3],
            "snippet": r[4],
        }
        for r in rows
    ]


def main():
    parser = argparse.ArgumentParser(
        description="pka_fts_index — Index FTS5 des sessions PKA"
    )
    parser.add_argument("--all", action="store_true", help="Indexer toutes les sessions")
    parser.add_argument("--recent", type=int, help="Indexer les N sessions les plus récentes")
    parser.add_argument("--session", help="Indexer une session spécifique (fichier JSON)")
    parser.add_argument("--search", help="Rechercher dans l'index (mode recherche)")
    parser.add_argument("--dry-run", action="store_true", help="Afficher sans écrire")
    parser.add_argument("--json", action="store_true", help="Sortie JSON")
    args = parser.parse_args()

    # Mode recherche
    if args.search:
        results = search_fts(args.search)
        if args.json:
            print(json.dumps(results, indent=2, ensure_ascii=False))
        else:
            print(f"=== Recherche FTS5 : '{args.search}' ===\n")
            for r in results:
                print(f"[{r['date']}] {r['session_id']}")
                print(f"  modèle: {r['model']} | projet: {r['project']}")
                print(f"  {r['snippet']}\n")
            if not results:
                print("Aucun résultat.")
        return

    # Mode indexation
    sessions = []

    if args.session:
        path = PKA_DIR / args.session
        if not path.exists():
            path = Path(args.session)
        if path.exists():
            info = extract_session_info(path)
            if info:
                sessions.append(info)
    elif args.recent:
        files = find_session_files()[: args.recent]
        for f in files:
            info = extract_session_info(f)
            if info:
                sessions.append(info)
    elif args.all:
        files = find_session_files()
        for f in files:
            info = extract_session_info(f)
            if info:
                sessions.append(info)
    else:
        # Par défaut : 50 plus récentes
        files = find_session_files()[:50]
        for f in files:
            info = extract_session_info(f)
            if info:
                sessions.append(info)

    indexed = index_sessions(sessions, dry_run=args.dry_run)

    output = {
        "status": "ok",
        "sessions_found": len(sessions),
        "sessions_indexed": indexed,
        "dry_run": args.dry_run,
    }

    if args.json:
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(f"=== pka_fts_index v0.1.0 ===")
        print(f"Sessions trouvées : {len(sessions)}")
        if args.dry_run:
            print(f"🔍 Dry run — {indexed} sessions auraient été indexées")
        else:
            print(f"✅ {indexed} sessions indexées dans session_fts")


if __name__ == "__main__":
    main()
