#!/usr/bin/env python3
"""Consolidation migration v4. Castor.

Adds CHECK constraints, indexes, schema_version table, tables_owned column,
typed journal links, knowledge_links self-loop check, created_by columns,
bookmarks url uniqueness. Idempotent — safe to re-run.
"""

import sqlite3
from pathlib import Path

DB = Path(__file__).resolve().parent.parent / "TEAM" / "team.db"

VALID_STATUS = {
    "members":         ['active', 'inactive', 'archived'],
    "hiring_pipeline": ['open', 'in_research', 'in_design', 'closed', 'cancelled'],
    "goals":           ['active', 'achieved', 'paused', 'dropped'],
    "ideas":           ['raw', 'developing', 'validated', 'shelved', 'archived'],
    "follow_ups":      ['open', 'done', 'cancelled'],
    "bookmarks_read":  ['unread', 'reading', 'done'],
    "knowledge":       ['active', 'archived'],
    "inbox":           ['pending', 'in_progress', 'done', 'cancelled'],
}

def quoted(values: list[str]) -> str:
    return ", ".join(f"'{v}'" for v in values)

def col_exists(cur, table: str, col: str) -> bool:
    return col in [r[1] for r in cur.execute(f"PRAGMA table_info({table})")]

def main() -> None:
    con = sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys = OFF")
    cur = con.cursor()

    # ── 1. schema_version table ─────────────────────────────────────
    cur.execute("""
    CREATE TABLE IF NOT EXISTS schema_version (
        version     INTEGER PRIMARY KEY,
        applied_on  TEXT NOT NULL DEFAULT (datetime('now')),
        description TEXT NOT NULL,
        applied_by  TEXT
    )
    """)
    cur.executemany(
        "INSERT OR IGNORE INTO schema_version (version, description, applied_by) VALUES (?,?,?)",
        [
            (1, "Initial schema: members, responsibilities, hiring_pipeline, inbox", "Dobby"),
            (2, "Added journal, contacts, file_index", "Dobby"),
            (3, "Added knowledge, knowledge_links, ideas, bookmarks, goals, interactions, follow_ups; enhanced journal+contacts", "Dobby"),
            (4, "Consolidation: CHECK constraints, indexes, tables_owned, typed journal link, created_by, url unique", "Castor"),
        ],
    )

    # ── 2. members.tables_owned ─────────────────────────────────────
    if not col_exists(cur, "members", "tables_owned"):
        cur.execute("ALTER TABLE members ADD COLUMN tables_owned TEXT")
        cur.executemany(
            "UPDATE members SET tables_owned = ? WHERE name = ?",
            [
                ("members,responsibilities,hiring_pipeline,inbox,file_index,journal,goals,ideas,bookmarks", "Dobby"),
                ("members,responsibilities", "Bouvier"),
                ("knowledge", "Furet"),
                ("members,responsibilities,hiring_pipeline,inbox,journal,contacts,interactions,follow_ups,knowledge,knowledge_links,ideas,bookmarks,goals,file_index,schema_version", "Castor"),
                ("knowledge,knowledge_links,ideas,bookmarks", "Corbeau"),
                ("contacts,interactions,follow_ups", "Delphi"),
            ],
        )
        print("  ✓ members.tables_owned")

    # ── 3. created_by columns where attribution matters ─────────────
    for tbl in ("journal", "knowledge", "ideas", "bookmarks", "goals"):
        if not col_exists(cur, tbl, "created_by"):
            cur.execute(f"ALTER TABLE {tbl} ADD COLUMN created_by TEXT")
            print(f"  ✓ {tbl}.created_by")

    # ── 4. typed journal link: linked_type + linked_id ──────────────
    #    Also fold all status CHECKs and self-loop check via table-recreation pattern.
    #    Note: ALTER TABLE statements auto-commit, so no explicit BEGIN/COMMIT here.

    # 4a. journal — replace linked_to with linked_type + linked_id
    cur.executescript(f"""
    CREATE TABLE IF NOT EXISTS journal_new (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        date        TEXT NOT NULL,
        author      TEXT NOT NULL DEFAULT 'JCH',
        title       TEXT NOT NULL,
        body        TEXT,
        mood        TEXT,
        tags        TEXT,
        linked_type TEXT CHECK(linked_type IN ('knowledge','contact','goal','idea','journal') OR linked_type IS NULL),
        linked_id   INTEGER,
        gratitude   TEXT,
        intentions  TEXT,
        reflections TEXT,
        highlight   TEXT,
        energy      INTEGER CHECK(energy IS NULL OR energy BETWEEN 1 AND 5),
        weather     TEXT,
        created_by  TEXT,
        created_at  TEXT NOT NULL DEFAULT (datetime('now')),
        updated_at  TEXT
    );
    INSERT INTO journal_new (id, date, author, title, body, mood, tags, gratitude, intentions, reflections, highlight, energy, weather, created_by, created_at, updated_at)
        SELECT id, date, author, title, body, mood, tags, gratitude, intentions, reflections, highlight, energy, weather, created_by, created_at, updated_at FROM journal;
    DROP TABLE journal;
    ALTER TABLE journal_new RENAME TO journal;
    """)

    # 4b. members — add status CHECK (preserve all data + tables_owned)
    cur.executescript(f"""
    CREATE TABLE members_new (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        name         TEXT NOT NULL UNIQUE,
        animal       TEXT NOT NULL,
        role         TEXT NOT NULL,
        status       TEXT NOT NULL DEFAULT 'active' CHECK(status IN ({quoted(VALID_STATUS["members"])})),
        persona      TEXT,
        tables_owned TEXT,
        hired_on     TEXT NOT NULL,
        hired_by     TEXT
    );
    INSERT INTO members_new SELECT id, name, animal, role, status, persona, tables_owned, hired_on, hired_by FROM members;
    DROP TABLE members;
    ALTER TABLE members_new RENAME TO members;
    """)

    # 4c. hiring_pipeline — status CHECK
    cur.executescript(f"""
    CREATE TABLE hp_new (
        id             INTEGER PRIMARY KEY AUTOINCREMENT,
        requested_by   TEXT NOT NULL,
        capability_gap TEXT NOT NULL,
        furet_brief    TEXT,
        bouvier_design TEXT,
        status         TEXT NOT NULL DEFAULT 'open' CHECK(status IN ({quoted(VALID_STATUS["hiring_pipeline"])})),
        created_at     TEXT NOT NULL,
        closed_at      TEXT
    );
    INSERT INTO hp_new SELECT id, requested_by, capability_gap, furet_brief, bouvier_design, status, created_at, closed_at FROM hiring_pipeline;
    DROP TABLE hiring_pipeline;
    ALTER TABLE hp_new RENAME TO hiring_pipeline;
    """)

    # 4d. goals — status CHECK + horizon CHECK
    cur.executescript(f"""
    CREATE TABLE goals_new (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        title       TEXT NOT NULL,
        description TEXT,
        horizon     TEXT CHECK(horizon IS NULL OR horizon IN ('daily','weekly','monthly','quarterly','yearly','life')),
        status      TEXT NOT NULL DEFAULT 'active' CHECK(status IN ({quoted(VALID_STATUS["goals"])})),
        target_date TEXT,
        tags        TEXT,
        created_by  TEXT,
        created_at  TEXT NOT NULL DEFAULT (datetime('now')),
        updated_at  TEXT
    );
    INSERT INTO goals_new (id, title, description, horizon, status, target_date, tags, created_by, created_at, updated_at)
        SELECT id, title, description, horizon, status, target_date, tags, created_by, created_at, updated_at FROM goals;
    DROP TABLE goals;
    ALTER TABLE goals_new RENAME TO goals;
    """)

    # 4e. ideas — status CHECK
    cur.executescript(f"""
    CREATE TABLE ideas_new (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        title       TEXT NOT NULL,
        body        TEXT,
        status      TEXT NOT NULL DEFAULT 'raw' CHECK(status IN ({quoted(VALID_STATUS["ideas"])})),
        tags        TEXT,
        created_by  TEXT,
        created_at  TEXT NOT NULL DEFAULT (datetime('now')),
        updated_at  TEXT
    );
    INSERT INTO ideas_new (id, title, body, status, tags, created_by, created_at, updated_at)
        SELECT id, title, body, status, tags, created_by, created_at, updated_at FROM ideas;
    DROP TABLE ideas;
    ALTER TABLE ideas_new RENAME TO ideas;
    """)

    # 4f. bookmarks — read_status CHECK + url UNIQUE
    cur.executescript(f"""
    CREATE TABLE bookmarks_new (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        title       TEXT NOT NULL,
        url         TEXT UNIQUE,
        description TEXT,
        type        TEXT CHECK(type IS NULL OR type IN ('article','video','tool','book','podcast','paper','other')),
        tags        TEXT,
        read_status TEXT NOT NULL DEFAULT 'unread' CHECK(read_status IN ({quoted(VALID_STATUS["bookmarks_read"])})),
        created_by  TEXT,
        added_on    TEXT NOT NULL DEFAULT (date('now'))
    );
    INSERT INTO bookmarks_new (id, title, url, description, type, tags, read_status, created_by, added_on)
        SELECT id, title, url, description, type, tags, read_status, created_by, added_on FROM bookmarks;
    DROP TABLE bookmarks;
    ALTER TABLE bookmarks_new RENAME TO bookmarks;
    """)

    # 4g. follow_ups — status CHECK
    cur.executescript(f"""
    CREATE TABLE fu_new (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        contact_id  INTEGER REFERENCES contacts(id),
        due_date    TEXT NOT NULL,
        subject     TEXT NOT NULL,
        notes       TEXT,
        status      TEXT NOT NULL DEFAULT 'open' CHECK(status IN ({quoted(VALID_STATUS["follow_ups"])})),
        created_at  TEXT NOT NULL DEFAULT (datetime('now'))
    );
    INSERT INTO fu_new SELECT id, contact_id, due_date, subject, notes, status, created_at FROM follow_ups;
    DROP TABLE follow_ups;
    ALTER TABLE fu_new RENAME TO follow_ups;
    """)

    # 4h. knowledge — status CHECK + type CHECK
    cur.executescript(f"""
    CREATE TABLE knowledge_new (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        title      TEXT NOT NULL,
        body       TEXT,
        type       TEXT CHECK(type IS NULL OR type IN ('note','insight','concept','quote','fact','procedure','framework')),
        source     TEXT,
        source_url TEXT,
        status     TEXT NOT NULL DEFAULT 'active' CHECK(status IN ({quoted(VALID_STATUS["knowledge"])})),
        tags       TEXT,
        created_by TEXT,
        created_at TEXT NOT NULL DEFAULT (datetime('now')),
        updated_at TEXT
    );
    INSERT INTO knowledge_new (id, title, body, type, source, source_url, status, tags, created_by, created_at, updated_at)
        SELECT id, title, body, type, source, source_url, status, tags, created_by, created_at, updated_at FROM knowledge;
    DROP TABLE knowledge;
    ALTER TABLE knowledge_new RENAME TO knowledge;
    """)

    # 4i. knowledge_links — self-loop CHECK + relationship CHECK
    cur.executescript("""
    CREATE TABLE kl_new (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        from_id      INTEGER NOT NULL REFERENCES knowledge(id),
        to_id        INTEGER NOT NULL REFERENCES knowledge(id),
        relationship TEXT CHECK(relationship IS NULL OR relationship IN ('supports','contradicts','related','extends','example_of')),
        CHECK(from_id <> to_id)
    );
    INSERT INTO kl_new SELECT id, from_id, to_id, relationship FROM knowledge_links;
    DROP TABLE knowledge_links;
    ALTER TABLE kl_new RENAME TO knowledge_links;
    """)

    # 4j. inbox — direction + status CHECK (direction was already CHECKed; reinforce status)
    cur.executescript(f"""
    CREATE TABLE inbox_new (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        direction  TEXT NOT NULL CHECK(direction IN ('JCH→TEAM', 'TEAM→JCH')),
        from_name  TEXT NOT NULL,
        to_name    TEXT NOT NULL,
        subject    TEXT NOT NULL,
        body       TEXT,
        status     TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ({quoted(VALID_STATUS["inbox"])})),
        created_at TEXT NOT NULL DEFAULT (datetime('now')),
        closed_at  TEXT,
        file_path  TEXT
    );
    INSERT INTO inbox_new SELECT id, direction, from_name, to_name, subject, body, status, created_at, closed_at, file_path FROM inbox;
    DROP TABLE inbox;
    ALTER TABLE inbox_new RENAME TO inbox;
    """)

    print("  ✓ Table recreations with CHECK constraints applied")

    # ── 5. Indexes ──────────────────────────────────────────────────
    indexes = [
        ("idx_responsibilities_member",    "responsibilities(member_id)"),
        ("idx_interactions_contact",       "interactions(contact_id)"),
        ("idx_interactions_date",          "interactions(date)"),
        ("idx_followups_due_status",       "follow_ups(due_date, status)"),
        ("idx_followups_contact",          "follow_ups(contact_id)"),
        ("idx_journal_date",               "journal(date)"),
        ("idx_journal_link",               "journal(linked_type, linked_id)"),
        ("idx_klinks_from",                "knowledge_links(from_id)"),
        ("idx_klinks_to",                  "knowledge_links(to_id)"),
        ("idx_inbox_direction_status",     "inbox(direction, status)"),
        ("idx_contacts_next_followup",     "contacts(next_followup)"),
        ("idx_contacts_last_contact",      "contacts(last_contact)"),
        ("idx_goals_status_horizon",       "goals(status, horizon)"),
        ("idx_ideas_status",               "ideas(status)"),
        ("idx_bookmarks_read",             "bookmarks(read_status)"),
        ("idx_file_index_inbox_dir",       "file_index(inbox_direction)"),
    ]
    for name, target in indexes:
        cur.execute(f"CREATE INDEX IF NOT EXISTS {name} ON {target}")
    print(f"  ✓ {len(indexes)} indexes ensured")

    con.execute("PRAGMA foreign_keys = ON")
    con.commit()

    # ── REPORT ──────────────────────────────────────────────────────
    print("\n=== schema_version ===")
    for row in cur.execute("SELECT version, description, applied_by, applied_on FROM schema_version ORDER BY version"):
        print(f"  v{row[0]:>2}  {row[2]:<8}  {row[1]}")

    print("\n=== members + tables_owned ===")
    for row in cur.execute("SELECT name, animal, role, tables_owned FROM members ORDER BY id"):
        print(f"  {row[1]} {row[0]:<10} {row[2][:38]:<38} → {row[3]}")

    print("\n=== Indexes ===")
    for row in cur.execute("SELECT name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_%' ORDER BY name"):
        print(f"  {row[0]}")

    con.close()
    print("\nMigration v4 complete.")

if __name__ == "__main__":
    main()
