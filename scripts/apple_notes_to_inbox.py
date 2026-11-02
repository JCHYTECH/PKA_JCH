#!/usr/bin/env python3
"""Export Apple Notes to PKA inbox as Markdown files.

Reads the local Apple Notes SQLite database and exports recent notes
(not password-protected, not deleted) as individual .md files.

Usage:
    python scripts/apple_notes_to_inbox.py              # export last 30 days
    python scripts/apple_notes_to_inbox.py --all         # export all notes
    python scripts/apple_notes_to_inbox.py --days 90     # export last 90 days
    python scripts/apple_notes_to_inbox.py --note "Photo setup"  # export one note
"""

from __future__ import annotations

import argparse
import gzip
import os
import re
import sqlite3
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES_DB = Path.home() / "Library" / "Group Containers" / "group.com.apple.notes" / "NoteStore.sqlite"
OUT_DIR = ROOT / "JCH_Inbox" / "00_INBOX" / "notes_apple"

# Apple Core Data uses an epoch of 2001-01-01
APPLE_EPOCH = 978307200


def slugify(title: str) -> str:
    """Sanitize a note title for use as a filename."""
    s = re.sub(r"[^\w\s-]", "", title)
    s = re.sub(r"\s+", "_", s.strip())
    return s[:80] or "untitled"


def extract_plain_text(zdata_blob: bytes | None) -> str:
    """Extract readable text from Apple Notes compressed blob (gzip or raw)."""
    if not zdata_blob:
        return ""
    try:
        decompressed = gzip.decompress(zdata_blob)
    except (gzip.BadGzipFile, OSError):
        decompressed = zdata_blob

    text = decompressed.decode("utf-8", errors="replace")

    # Strip NSAttributedString/HTML wrapper, keep plain text
    # Apple Notes stores as either raw text or HTML/RTF blob
    # Try to extract readable content
    if text.startswith("\x1f\x8b"):
        return "[binary gzip — could not decode]"

    # Remove null bytes and control chars
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)

    # If it's HTML, try to extract body text
    if "<html" in text.lower() or "<body" in text.lower():
        # Simple HTML tag stripping
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"&nbsp;", " ", text)
        text = re.sub(r"&amp;", "&", text)
        text = re.sub(r"&lt;", "<", text)
        text = re.sub(r"&gt;", ">", text)
        text = re.sub(r"\s+", " ", text).strip()

    return text[:5000]  # cap at reasonable size


def get_folder_id(folder_name: str) -> int | None:
    """Resolve an Apple Notes folder name to its internal Z_PK id."""
    if not NOTES_DB.exists():
        return None
    db = sqlite3.connect(str(NOTES_DB))
    row = db.execute(
        "SELECT Z_PK FROM ZICCLOUDSYNCINGOBJECT WHERE ZTITLE2 = ? AND ZFOLDERTYPE = 0 AND ZMARKEDFORDELETION = 0",
        (folder_name,)
    ).fetchone()
    db.close()
    return row[0] if row else None


def get_notes(days: int | None = 30, title_filter: str | None = None, folder_id: int | None = None) -> list[dict]:
    """Query Apple Notes database and return matching notes."""
    if not NOTES_DB.exists():
        print(f"❌ Apple Notes database not found: {NOTES_DB}", file=sys.stderr)
        return []

    db = sqlite3.connect(str(NOTES_DB))
    db.row_factory = sqlite3.Row

    where_clauses = [
        "o.ZTITLE1 IS NOT NULL",
        "o.ZTITLE1 != ''",
        "o.ZMARKEDFORDELETION = 0",
        "o.ZISPASSWORDPROTECTED = 0",
    ]

    params: list = []

    if days is not None:
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        cutoff_apple = cutoff.timestamp() - APPLE_EPOCH
        where_clauses.append("o.ZMODIFICATIONDATE1 >= ?")
        params.append(cutoff_apple)

    if title_filter:
        where_clauses.append("o.ZTITLE1 LIKE ?")
        params.append(f"%{title_filter}%")

    if folder_id is not None:
        where_clauses.append("o.ZFOLDER = ?")
        params.append(folder_id)

    where = " AND ".join(where_clauses)

    query = f"""
        SELECT o.Z_PK as pk,
               o.ZTITLE1 as title,
               o.ZSNIPPET as snippet,
               o.ZCREATIONDATE1 as created_ts,
               o.ZMODIFICATIONDATE1 as modified_ts,
               d.ZDATA as data_blob
        FROM ZICCLOUDSYNCINGOBJECT o
        LEFT JOIN ZICNOTEDATA d ON d.ZNOTE = o.Z_PK
        WHERE {where}
        ORDER BY o.ZMODIFICATIONDATE1 DESC
    """

    rows = db.execute(query, params).fetchall()
    db.close()

    notes = []
    for r in rows:
        created = datetime.fromtimestamp(r["created_ts"] + APPLE_EPOCH, tz=timezone.utc) if r["created_ts"] else None
        modified = datetime.fromtimestamp(r["modified_ts"] + APPLE_EPOCH, tz=timezone.utc) if r["modified_ts"] else None

        notes.append({
            "pk": r["pk"],
            "title": (r["title"] or "Sans titre").strip(),
            "snippet": (r["snippet"] or "").strip(),
            "created": created,
            "modified": modified,
            "body": extract_plain_text(r["data_blob"]),
        })

    return notes


def export_note(note: dict) -> Path | None:
    """Write a single note as a Markdown file. Returns the output path."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    date_str = note["modified"].strftime("%Y-%m-%d") if note["modified"] else "unknown"
    fname = f"{date_str}_{slugify(note['title'])}.md"
    out_path = OUT_DIR / fname

    created_str = note["created"].strftime("%Y-%m-%d %H:%M") if note["created"] else "?"
    modified_str = note["modified"].strftime("%Y-%m-%d %H:%M") if note["modified"] else "?"

    content = f"""# {note['title']}

> Exporté depuis Apple Notes — créé le {created_str}, modifié le {modified_str}

{note['body'] or note['snippet'] or '_Note vide_'}
"""

    # Skip if unchanged
    if out_path.exists() and out_path.read_text(encoding="utf-8") == content:
        return None

    out_path.write_text(content, encoding="utf-8")
    return out_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Export Apple Notes to PKA inbox")
    parser.add_argument("--all", action="store_true", help="Export all notes (not just recent)")
    parser.add_argument("--days", type=int, default=30, help="Export notes modified in last N days (default: 30)")
    parser.add_argument("--note", type=str, help="Export a specific note by title (substring match)")
    parser.add_argument("--folder", type=str, default="TKA_JCH", help="Apple Notes folder to export (default: TKA_JCH)")
    args = parser.parse_args()

    days = None if args.all else args.days

    folder_id = None
    if args.folder:
        folder_id = get_folder_id(args.folder)
        if folder_id is None:
            print(f"❌ Folder not found: '{args.folder}'", file=sys.stderr)
            return 1
        print(f"📁 Folder: {args.folder} (id={folder_id})")

    print(f"📝 Reading Apple Notes...")
    notes = get_notes(days=days, title_filter=args.note, folder_id=folder_id)
    print(f"   Found {len(notes)} note(s)")

    exported = 0
    skipped = 0
    for note in notes:
        path = export_note(note)
        if path:
            print(f"   ✅ {path.name}")
            exported += 1
        else:
            skipped += 1

    print(f"\n📦 {exported} exported, {skipped} skipped (unchanged)")
    print(f"   → {OUT_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
