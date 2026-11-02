#!/usr/bin/env python3
"""
skill_search.py
Forge 🦦 — Recherche les skills pertinents pour une tâche donnée.
Usage : python skill_search.py "requête texte" [--limit 3]
Retourne les skills matchants avec leur procédure complète.
"""

import argparse
import sqlite3
from pathlib import Path

try:
    from scripts.instinct_search import format_instincts, search_instincts
    from scripts.pka_context_profile import infer_project_key
except ModuleNotFoundError:
    from instinct_search import format_instincts, search_instincts
    from pka_context_profile import infer_project_key

DB_PATH = Path(__file__).resolve().parent.parent / "TEAM" / "team.db"


def get_columns(cur: sqlite3.Cursor) -> set[str]:
    rows = cur.execute("PRAGMA table_info(skills)").fetchall()
    return {row[1] for row in rows}


def search_skills(query: str, limit: int = 3, project_key: str | None = None) -> list[dict]:
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    columns = get_columns(cur)
    resolved_project_key = project_key or infer_project_key(query)

    # Tokenise la requête et cherche chaque mot dans trigger_pattern, title, context
    tokens = [t.lower() for t in query.split() if len(t) > 2]
    if not tokens:
        return []

    conditions = " OR ".join(
        ["(LOWER(trigger_pattern) LIKE ? OR LOWER(title) LIKE ? OR LOWER(context) LIKE ?)"]
        * len(tokens)
    )
    params = []
    for token in tokens:
        params += [f"%{token}%", f"%{token}%", f"%{token}%"]

    select_columns = [
        "id", "title", "trigger_pattern", "specialist", "procedure",
        "context", "usage_count"
    ]
    for optional in ("scope", "project_key", "confidence", "source_kind", "model", "updated_at"):
        if optional in columns:
            select_columns.append(optional)

    order_parts = []
    if resolved_project_key and "scope" in columns and "project_key" in columns:
        order_parts.append(
            "CASE "
            "WHEN scope = 'project' AND project_key = ? THEN 0 "
            "WHEN scope = 'global' THEN 1 "
            "ELSE 2 END"
        )
        params.append(resolved_project_key)
    elif "scope" in columns:
        order_parts.append(
            "CASE "
            "WHEN scope = 'global' THEN 0 "
            "WHEN scope = 'project' THEN 1 "
            "ELSE 2 END"
        )
    order_parts.append("usage_count DESC")

    cur.execute(
        f"""SELECT {", ".join(select_columns)}
            FROM skills
            WHERE {conditions}
            ORDER BY {", ".join(order_parts)}
            LIMIT ?""",
        params + [limit],
    )

    rows = [dict(r) for r in cur.fetchall()]
    con.close()

    # Incrémente usage_count pour les skills retournés
    if rows:
        ids = [r["id"] for r in rows]
        con2 = sqlite3.connect(DB_PATH)
        con2.execute(
            f"UPDATE skills SET usage_count = usage_count + 1, last_used = DATE('now') WHERE id IN ({','.join('?' * len(ids))})",
            ids,
        )
        con2.commit()
        con2.close()

    return rows


def format_skills(skills: list[dict]) -> str:
    if not skills:
        return ""
    lines = ["## Skills pertinents chargés depuis la mémoire PKA\n"]
    for s in skills:
        lines.append(f"### {s['title']}")
        if s.get("specialist"):
            lines.append(f"*Spécialiste : {s['specialist']}*")
        if s.get("context"):
            lines.append(f"**Quand l'utiliser :** {s['context']}")
        metadata = []
        if s.get("scope"):
            metadata.append(f"scope={s['scope']}")
        if s.get("project_key"):
            metadata.append(f"project={s['project_key']}")
        if s.get("confidence") is not None:
            metadata.append(f"confidence={s['confidence']}")
        if metadata:
            lines.append(f"**Métadonnées :** {', '.join(metadata)}")
        lines.append(f"\n**Procédure :**\n{s['procedure']}\n")
    return "\n".join(lines)


def format_for_context(skills: list[dict], instincts: list[dict] | None = None) -> str:
    sections = []
    skills_section = format_skills(skills)
    if skills_section:
        sections.append(skills_section)
    instincts_section = format_instincts(instincts or [])
    if instincts_section:
        sections.append(instincts_section)
    return "\n\n".join(section for section in sections if section)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Recherche de skills PKA")
    parser.add_argument("query", help="Requête texte décrivant la tâche")
    parser.add_argument("--limit", type=int, default=3)
    parser.add_argument("--project-key", default=None)
    args = parser.parse_args()

    resolved_project_key = args.project_key or infer_project_key(args.query)
    results = search_skills(args.query, args.limit, project_key=resolved_project_key)
    instincts = search_instincts(args.query, args.limit, project_key=resolved_project_key)
    if not results and not instincts:
        print("Aucun skill trouvé pour cette requête.")
    else:
        print(format_for_context(results, instincts))
