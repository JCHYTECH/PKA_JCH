#!/usr/bin/env python3
"""Rebuild file_index from the live filesystem."""

from __future__ import annotations

import argparse
import os
import re
import sqlite3
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "TEAM" / "team.db"
DEFAULT_SCAN_ROOTS = ("JCH_Inbox", "TEAM_Inbox", "TEAM", "wiki")
EXCLUDED_DIR_NAMES = {".git", "node_modules", ".venv", "__pycache__"}
EXCLUDED_FILE_NAMES = {".DS_Store"}
EXCLUDED_FILE_PREFIXES = ("~$",)
COMPONENT_RE = re.compile(r"^\d{2}\.\d{2}\b")


def table_exists(conn: sqlite3.Connection, name: str) -> bool:
    row = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name = ?",
        (name,),
    ).fetchone()
    return bool(row)


def next_archive_name(conn: sqlite3.Connection, base_name: str) -> str:
    if not table_exists(conn, base_name):
        return base_name

    index = 1
    while table_exists(conn, f"{base_name}_{index}"):
        index += 1
    return f"{base_name}_{index}"


def archive_existing_table(conn: sqlite3.Connection, archive_suffix: str) -> tuple[str | None, int]:
    if not table_exists(conn, "file_index"):
        return None, 0

    archive_name = next_archive_name(conn, f"file_index_legacy_{archive_suffix}")
    legacy_rows = conn.execute("SELECT COUNT(*) FROM file_index").fetchone()[0]
    conn.execute(f'ALTER TABLE file_index RENAME TO "{archive_name}"')
    return archive_name, legacy_rows


def create_file_index_table(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        DROP INDEX IF EXISTS idx_file_index_inbox_dir;
        DROP INDEX IF EXISTS idx_file_index_project_key;
        DROP INDEX IF EXISTS idx_file_index_component;
        DROP INDEX IF EXISTS idx_file_index_status;
        DROP TABLE IF EXISTS file_index;
        CREATE TABLE file_index (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            filename        TEXT NOT NULL,
            file_path       TEXT NOT NULL UNIQUE,
            file_type       TEXT,
            size_bytes      INTEGER,
            description     TEXT,
            tags            TEXT,
            owner           TEXT,
            linked_member   TEXT,
            inbox_direction TEXT CHECK(inbox_direction IN ('JCH_Inbox', 'TEAM_Inbox', NULL)),
            indexed_on      TEXT NOT NULL DEFAULT (datetime('now')),
            last_modified   TEXT,
            category        TEXT,
            project_key     TEXT,
            component       TEXT,
            exists_on_disk  INTEGER NOT NULL DEFAULT 1 CHECK(exists_on_disk IN (0, 1)),
            status          TEXT NOT NULL DEFAULT 'active' CHECK(status IN ('active', 'archived', 'reference', 'temporary'))
        );
        CREATE INDEX idx_file_index_inbox_dir ON file_index(inbox_direction);
        CREATE INDEX idx_file_index_project_key ON file_index(project_key);
        CREATE INDEX idx_file_index_component ON file_index(component);
        CREATE INDEX idx_file_index_status ON file_index(status);
        """
    )


def should_skip_dir(dirname: str) -> bool:
    return dirname in EXCLUDED_DIR_NAMES


def should_skip_file(name: str) -> bool:
    if name in EXCLUDED_FILE_NAMES:
        return True
    return any(name.startswith(prefix) for prefix in EXCLUDED_FILE_PREFIXES)


def derive_inbox_direction(rel_path: str) -> str | None:
    if rel_path.startswith("JCH_Inbox/"):
        return "JCH_Inbox"
    if rel_path.startswith("TEAM_Inbox/"):
        return "TEAM_Inbox"
    return None


def derive_project_key(parts: tuple[str, ...]) -> str | None:
    if not parts:
        return None
    if parts[0] in {"TEAM", "TEAM_Inbox", "wiki"}:
        return "PKA"
    if len(parts) >= 2 and parts[0] == "JCH_Inbox" and parts[1] in {"01_DASHBOARDS", "99_SYSTEM"}:
        return "PKA"
    if len(parts) >= 3 and parts[0] == "JCH_Inbox" and parts[1] == "03_PROJECTS":
        return parts[2]
    return None


def derive_component(parts: tuple[str, ...]) -> str | None:
    if not parts:
        return None
    if parts[0] in {"TEAM", "TEAM_Inbox", "wiki"}:
        return parts[0]
    if len(parts) >= 2 and parts[0] == "JCH_Inbox" and parts[1] in {"01_DASHBOARDS", "99_SYSTEM"}:
        return parts[1]
    if len(parts) < 4 or parts[0] != "JCH_Inbox" or parts[1] != "03_PROJECTS":
        return None
    candidate = parts[3]
    if COMPONENT_RE.match(candidate):
        return candidate
    return None


def derive_category(rel_path: str, file_type: str, project_key: str | None, component: str | None) -> str:
    parts = tuple(Path(rel_path).parts)
    if rel_path.startswith("scripts/"):
        return "script"
    if rel_path.startswith("TEAM_Inbox/"):
        return "team_deliverable"
    if rel_path.startswith("TEAM/"):
        return "team_system"
    if rel_path.startswith("wiki/"):
        return "wiki"
    if rel_path.startswith("docs/"):
        return "doc"
    if project_key:
        if component and "APP" in component and file_type in {"html", "js", "css", "json"}:
            return "app_source"
        if file_type in {"png", "jpg", "jpeg", "svg", "webp"}:
            return "asset"
        return "project_doc"
    if parts and parts[0] == "JCH_Inbox":
        return "inbox_doc"
    return "reference"


def derive_status(rel_path: str) -> str:
    parts = set(Path(rel_path).parts)
    if "archive" in parts or "archives" in parts:
        return "archived"
    return "active"


def iter_scan_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for scan_root in DEFAULT_SCAN_ROOTS:
        start = root / scan_root
        if not start.exists():
            continue
        for current_root, dirnames, filenames in os.walk(start):
            dirnames[:] = [name for name in dirnames if not should_skip_dir(name)]
            current = Path(current_root)
            for filename in filenames:
                if should_skip_file(filename):
                    continue
                files.append(current / filename)
    return files


def collect_rows(root: Path) -> list[tuple]:
    rows = []
    for path in iter_scan_files(root):
        rel_path = path.relative_to(root).as_posix()
        parts = tuple(path.relative_to(root).parts)
        file_type = path.suffix.lstrip(".").lower()
        project_key = derive_project_key(parts)
        component = derive_component(parts)
        rows.append(
            (
                path.name,
                rel_path,
                file_type,
                path.stat().st_size,
                None,
                None,
                None,
                None,
                derive_inbox_direction(rel_path),
                datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
                derive_category(rel_path, file_type, project_key, component),
                project_key,
                component,
                1,
                derive_status(rel_path),
            )
        )
    return rows


def build_row(root: Path, path: Path) -> tuple:
    rel_path = path.relative_to(root).as_posix()
    parts = tuple(path.relative_to(root).parts)
    file_type = path.suffix.lstrip(".").lower()
    project_key = derive_project_key(parts)
    component = derive_component(parts)
    return (
        path.name,
        rel_path,
        file_type,
        path.stat().st_size,
        None,
        None,
        None,
        None,
        derive_inbox_direction(rel_path),
        datetime.fromtimestamp(path.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
        derive_category(rel_path, file_type, project_key, component),
        project_key,
        component,
        1,
        derive_status(rel_path),
    )


def insert_rows(conn: sqlite3.Connection, rows: list[tuple]) -> None:
    conn.executemany(
        """
        INSERT INTO file_index (
            filename, file_path, file_type, size_bytes, description, tags, owner, linked_member,
            inbox_direction, last_modified, category, project_key, component, exists_on_disk, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        rows,
    )


def upsert_rows(conn: sqlite3.Connection, rows: list[tuple]) -> int:
    conn.executemany(
        """
        INSERT INTO file_index (
            filename, file_path, file_type, size_bytes, description, tags, owner, linked_member,
            inbox_direction, last_modified, category, project_key, component, exists_on_disk, status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(file_path) DO UPDATE SET
            filename=excluded.filename,
            file_type=excluded.file_type,
            size_bytes=excluded.size_bytes,
            inbox_direction=excluded.inbox_direction,
            last_modified=excluded.last_modified,
            category=excluded.category,
            project_key=excluded.project_key,
            component=excluded.component,
            exists_on_disk=excluded.exists_on_disk,
            status=excluded.status
        """,
        rows,
    )
    return len(rows)


def rebuild_index(root: Path = ROOT, db_path: Path = DB_PATH, archive_suffix: str | None = None) -> dict:
    if archive_suffix is None:
        archive_suffix = datetime.now().strftime("%Y_%m_%d")

    rows = collect_rows(root)
    with sqlite3.connect(db_path) as conn:
        archived_table, legacy_rows = archive_existing_table(conn, archive_suffix)
        create_file_index_table(conn)
        insert_rows(conn, rows)
        conn.commit()

    return {
        "archived_table": archived_table,
        "legacy_rows": legacy_rows,
        "indexed_rows": len(rows),
        "scan_roots": list(DEFAULT_SCAN_ROOTS),
    }


def rescan_index(root: Path = ROOT, db_path: Path = DB_PATH) -> dict:
    scanned_paths: set[str] = set()
    inserted = 0
    updated = 0

    with sqlite3.connect(db_path) as conn:
        if not table_exists(conn, "file_index"):
            create_file_index_table(conn)

        existing_paths = {
            row[0]
            for row in conn.execute("SELECT file_path FROM file_index")
        }

        for path in iter_scan_files(root):
            row = build_row(root, path)
            rel_path = row[1]
            scanned_paths.add(rel_path)
            if rel_path in existing_paths:
                updated += 1
            else:
                inserted += 1
            upsert_rows(conn, [row])

        marked_missing = 0
        for (file_path,) in conn.execute("SELECT file_path FROM file_index WHERE exists_on_disk = 1"):
            if file_path not in scanned_paths:
                conn.execute(
                    "UPDATE file_index SET exists_on_disk = 0, status = 'reference' WHERE file_path = ?",
                    (file_path,),
                )
                marked_missing += 1

        conn.commit()

    return {
        "inserted": inserted,
        "updated": updated,
        "marked_missing": marked_missing,
        "scanned": len(scanned_paths),
    }


def search_index(
    db_path: Path,
    query: str,
    project_key: str | None = None,
    component: str | None = None,
    limit: int = 20,
) -> list[dict]:
    escaped_query = query.lower().replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
    needle = f"%{escaped_query}%"
    sql = """
        SELECT
            filename,
            file_path,
            category,
            project_key,
            component,
            CASE
                WHEN lower(filename) = ? THEN 300
                WHEN lower(filename) LIKE ? THEN 200
                WHEN lower(file_path) LIKE ? THEN 100
                ELSE 0
            END AS rank
        FROM file_index
        WHERE exists_on_disk = 1
          AND status != 'archived'
          AND (
            lower(filename) LIKE ? ESCAPE '\\'
            OR lower(file_path) LIKE ? ESCAPE '\\'
            OR lower(COALESCE(tags, '')) LIKE ? ESCAPE '\\'
          )
    """
    params: list[object] = [query.lower(), needle, needle, needle, needle, needle]
    if project_key:
        sql += " AND project_key = ?"
        params.append(project_key)
    if component:
        sql += " AND component = ?"
        params.append(component)
    sql += " ORDER BY rank DESC, filename ASC LIMIT ?"
    params.append(limit)

    with sqlite3.connect(db_path) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(sql, params).fetchall()
    return [dict(row) for row in rows]


def available_filters(db_path: Path) -> dict:
    with sqlite3.connect(db_path) as conn:
        projects = [
            row[0]
            for row in conn.execute(
                """
                SELECT DISTINCT project_key
                FROM file_index
                WHERE exists_on_disk = 1
                  AND status != 'archived'
                  AND project_key IS NOT NULL
                ORDER BY project_key
                """
            )
        ]
        components: dict[str, list[str]] = {}
        for project_key in projects:
            components[project_key] = [
                row[0]
                for row in conn.execute(
                    """
                    SELECT DISTINCT component
                    FROM file_index
                    WHERE exists_on_disk = 1
                      AND status != 'archived'
                      AND project_key = ?
                      AND component IS NOT NULL
                    ORDER BY component
                    """,
                    (project_key,),
                )
            ]
    return {"projects": projects, "components": components}


def main() -> int:
    parser = argparse.ArgumentParser(description="Rebuild file_index from live filesystem")
    subparsers = parser.add_subparsers(dest="command", required=False)

    rebuild_parser = subparsers.add_parser("rebuild")
    rebuild_parser.add_argument("--root", type=Path, default=ROOT)
    rebuild_parser.add_argument("--db", type=Path, default=DB_PATH)
    rebuild_parser.add_argument("--archive-suffix", default=None)

    rescan_parser = subparsers.add_parser("rescan")
    rescan_parser.add_argument("--root", type=Path, default=ROOT)
    rescan_parser.add_argument("--db", type=Path, default=DB_PATH)

    search_parser = subparsers.add_parser("search")
    search_parser.add_argument("query")
    search_parser.add_argument("--db", type=Path, default=DB_PATH)
    search_parser.add_argument("--project-key", default=None)
    search_parser.add_argument("--component", default=None)
    search_parser.add_argument("--limit", type=int, default=20)

    args = parser.parse_args()

    if args.command in (None, "rebuild"):
        root = getattr(args, "root", ROOT)
        db = getattr(args, "db", DB_PATH)
        archive_suffix = getattr(args, "archive_suffix", None)
        result = rebuild_index(root, db, archive_suffix)
        print(
            f"Rebuilt file_index: {result['indexed_rows']} rows"
            + (f" (archived {result['legacy_rows']} rows to {result['archived_table']})" if result["archived_table"] else "")
        )
        return 0

    if args.command == "rescan":
        result = rescan_index(args.root, args.db)
        print(
            f"Rescanned file_index: {result['scanned']} scanned, {result['inserted']} inserted, "
            f"{result['updated']} updated, {result['marked_missing']} marked missing"
        )
        return 0

    if args.command == "search":
        for row in search_index(
            args.db,
            args.query,
            project_key=args.project_key,
            component=args.component,
            limit=args.limit,
        ):
            print(f"{row['project_key'] or '-'} | {row['component'] or '-'} | {row['filename']} | {row['file_path']}")
        return 0

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
