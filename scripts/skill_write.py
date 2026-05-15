#!/usr/bin/env python3
"""
skill_write.py
Forge 🦦 — Enregistre un skill dans team.db après une tâche complexe résolue.
Usage : python skill_write.py --title "..." --trigger "..." --procedure "..." [--specialist "..."] [--context "..."]
"""

import argparse
import sqlite3
from datetime import date
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "TEAM" / "team.db"


def get_columns(cur: sqlite3.Cursor) -> set[str]:
    rows = cur.execute("PRAGMA table_info(skills)").fetchall()
    return {row[1] for row in rows}


def write_skill(title: str, trigger_pattern: str, procedure: str,
                specialist: str = None, context: str = None,
                source_kind: str = "manual", confidence: float = 0.7,
                scope: str = "global", project_key: str = None,
                model: str = None) -> int:
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    columns = get_columns(cur)
    today = date.today().isoformat()

    # Si un skill avec le même trigger existe, on le met à jour
    cur.execute(
        "SELECT id, usage_count FROM skills WHERE trigger_pattern = ? COLLATE NOCASE",
        (trigger_pattern,)
    )
    row = cur.fetchone()

    if row:
        skill_id, count = row
        updates = [
            ("title", title),
            ("procedure", procedure),
            ("specialist", specialist),
            ("context", context),
            ("usage_count", count + 1),
            ("last_used", today),
        ]
        if "source_kind" in columns:
            updates.append(("source_kind", source_kind))
        if "confidence" in columns:
            updates.append(("confidence", confidence))
        if "scope" in columns:
            updates.append(("scope", scope))
        if "project_key" in columns:
            updates.append(("project_key", project_key))
        if "model" in columns and model is not None:
            updates.append(("model", model))
        if "updated_at" in columns:
            updates.append(("updated_at", today))

        assignments = ", ".join(f"{column}=?" for column, _ in updates)
        params = [value for _, value in updates] + [skill_id]
        cur.execute(f"UPDATE skills SET {assignments} WHERE id=?", params)
        print(f"✅ Skill mis à jour (id={skill_id}) : {title}")
    else:
        insert_map = {
            "title": title,
            "trigger_pattern": trigger_pattern,
            "specialist": specialist,
            "procedure": procedure,
            "context": context,
        }
        if "source_kind" in columns:
            insert_map["source_kind"] = source_kind
        if "confidence" in columns:
            insert_map["confidence"] = confidence
        if "scope" in columns:
            insert_map["scope"] = scope
        if "project_key" in columns:
            insert_map["project_key"] = project_key
        if "model" in columns and model is not None:
            insert_map["model"] = model
        if "updated_at" in columns:
            insert_map["updated_at"] = today

        cols = ", ".join(insert_map.keys())
        placeholders = ", ".join("?" for _ in insert_map)
        cur.execute(
            f"INSERT INTO skills ({cols}) VALUES ({placeholders})",
            list(insert_map.values())
        )
        skill_id = cur.lastrowid
        print(f"✅ Nouveau skill créé (id={skill_id}) : {title}")

    con.commit()
    con.close()
    return skill_id


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enregistre un skill PKA")
    parser.add_argument("--title", required=True)
    parser.add_argument("--trigger", required=True, dest="trigger_pattern")
    parser.add_argument("--procedure", required=True)
    parser.add_argument("--specialist", default=None)
    parser.add_argument("--context", default=None)
    parser.add_argument("--source-kind", default="manual")
    parser.add_argument("--confidence", type=float, default=0.7)
    parser.add_argument("--scope", default="global")
    parser.add_argument("--project-key", default=None)
    parser.add_argument("--model", default=None)
    args = parser.parse_args()

    write_skill(
        title=args.title,
        trigger_pattern=args.trigger_pattern,
        procedure=args.procedure,
        specialist=args.specialist,
        context=args.context,
        source_kind=args.source_kind,
        confidence=args.confidence,
        scope=args.scope,
        project_key=args.project_key,
        model=args.model,
    )
