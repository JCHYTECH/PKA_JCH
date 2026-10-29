#!/usr/bin/env python3
"""Promote mature instincts into reusable skills."""

from __future__ import annotations

import argparse
import json
import sqlite3
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "TEAM" / "team.db"
CONFIG_PATH = ROOT / "JCH_Inbox" / "99_SYSTEM" / "instinct_promotion_config.json"


def promoted_procedure(instinct: sqlite3.Row) -> str:
    return "\n".join([
        f"1. Trigger pattern observed: {instinct['trigger_pattern']}.",
        f"2. Observation: {instinct['observation']}",
        f"3. Recommended action: {instinct['action']}",
        "4. Reuse this as the default path unless a stronger project-specific rule overrides it.",
    ])


def ensure_skill(conn: sqlite3.Connection, instinct: sqlite3.Row) -> None:
    today = date.today().isoformat()
    procedure = promoted_procedure(instinct)
    existing = conn.execute(
        "SELECT id FROM skills WHERE trigger_pattern = ? COLLATE NOCASE",
        (instinct["trigger_pattern"],),
    ).fetchone()
    payload = (
        instinct["summary"],
        "Forge",
        procedure,
        instinct["observation"],
        "promoted-instinct",
        instinct["confidence"],
        instinct["scope"],
        instinct["project_key"],
        instinct["model"],
        today,
    )
    if existing:
        conn.execute(
            """
            UPDATE skills
            SET title=?, specialist=?, procedure=?, context=?, source_kind=?, confidence=?,
                scope=?, project_key=?, model=?, updated_at=?
            WHERE id=?
            """,
            payload + (existing[0],),
        )
        return
    conn.execute(
        """
        INSERT INTO skills
        (title, trigger_pattern, specialist, procedure, context, source_kind, confidence, scope, project_key, model, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            instinct["summary"],
            instinct["trigger_pattern"],
            "Forge",
            procedure,
            instinct["observation"],
            "promoted-instinct",
            instinct["confidence"],
            instinct["scope"],
            instinct["project_key"],
            instinct["model"],
            today,
        ),
    )


def load_config() -> dict:
    if CONFIG_PATH.is_file():
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    return {
        "min_confidence": 0.8,
        "min_observations": 2,
        "allow_scopes": ["global", "project"],
        "allow_source_kinds": ["learned", "system"],
        "report_dir": str(ROOT / "TEAM_Inbox"),
    }


def evaluate_instincts(
    min_confidence: float = 0.8,
    min_observations: int = 2,
    allow_scopes: list[str] | None = None,
    allow_source_kinds: list[str] | None = None,
) -> dict:
    allow_scopes = allow_scopes or ["global", "project"]
    allow_source_kinds = allow_source_kinds or ["learned", "system"]
    promoted: list[str] = []
    skipped: list[dict] = []
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            """
            SELECT *
            FROM instincts
            WHERE status = 'active'
            ORDER BY confidence DESC, observation_count DESC
            """
        ).fetchall()
        today = date.today().isoformat()
        for instinct in rows:
            reasons = []
            if instinct["confidence"] < min_confidence:
                reasons.append("confidence below threshold")
            if instinct["observation_count"] < min_observations:
                reasons.append("observation_count below threshold")
            if instinct["scope"] not in allow_scopes:
                reasons.append("scope not allowed")
            if instinct["source_kind"] not in allow_source_kinds:
                reasons.append("source_kind not allowed")
            if reasons:
                skipped.append({"instinct_key": instinct["instinct_key"], "reasons": reasons})
            else:
                promoted.append(instinct["instinct_key"])
    return {
        "date": today,
        "promoted": promoted,
        "skipped": skipped,
        "min_confidence": min_confidence,
        "min_observations": min_observations,
        "allow_scopes": allow_scopes,
        "allow_source_kinds": allow_source_kinds,
    }


def promote_instincts(
    min_confidence: float = 0.8,
    min_observations: int = 2,
    allow_scopes: list[str] | None = None,
    allow_source_kinds: list[str] | None = None,
) -> dict:
    result = evaluate_instincts(
        min_confidence=min_confidence,
        min_observations=min_observations,
        allow_scopes=allow_scopes,
        allow_source_kinds=allow_source_kinds,
    )

    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(
            f"""
            SELECT *
            FROM instincts
            WHERE status = 'active'
              AND instinct_key IN ({",".join("?" for _ in result["promoted"])})
            ORDER BY confidence DESC, observation_count DESC
            """,
            result["promoted"],
        ).fetchall() if result["promoted"] else []
        today = date.today().isoformat()
        for instinct in rows:
            ensure_skill(conn, instinct)
            conn.execute(
                """
                UPDATE instincts
                SET status='promoted', source_ref=?, updated_at=?
                WHERE id=?
                """,
                (f"skill:{instinct['trigger_pattern']}", today, instinct["id"]),
            )
        conn.commit()
    return result


def markdown_report(result: dict) -> str:
    lines = [
        "# Instinct Promotion Report",
        "",
        f"_Generated: {result['date']}_",
        f"_Thresholds: confidence >= {result['min_confidence']}, observations >= {result['min_observations']}_",
        "",
        "## Promoted Instincts",
        "",
    ]
    if result["promoted"]:
        for instinct_key in result["promoted"]:
            lines.append(f"- {instinct_key}")
    else:
        lines.append("No instincts promoted.")

    lines.extend(["", "## Skipped Instincts", ""])
    if result["skipped"]:
        for item in result["skipped"]:
            lines.append(f"- {item['instinct_key']}: {', '.join(item['reasons'])}")
    else:
        lines.append("No skipped instincts.")
    return "\n".join(lines) + "\n"


def run_promotion_from_config(write_report: bool = False) -> dict:
    config = load_config()
    result = promote_instincts(
        min_confidence=config.get("min_confidence", 0.8),
        min_observations=config.get("min_observations", 2),
        allow_scopes=config.get("allow_scopes", ["global", "project"]),
        allow_source_kinds=config.get("allow_source_kinds", ["learned", "system"]),
    )
    if write_report:
        report_dir = Path(config.get("report_dir", ROOT / "TEAM_Inbox"))
        report_dir.mkdir(parents=True, exist_ok=True)
        report_path = report_dir / f"{result['date']}_instinct_promotion.md"
        report_path.write_text(markdown_report(result), encoding="utf-8")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Promote mature instincts into skills")
    parser.add_argument("--min-confidence", type=float, default=0.8)
    parser.add_argument("--min-observations", type=int, default=2)
    parser.add_argument("--write-report", action="store_true")
    parser.add_argument("--use-config", action="store_true")
    args = parser.parse_args()

    if args.use_config:
        result = run_promotion_from_config(write_report=args.write_report)
    else:
        result = promote_instincts(args.min_confidence, args.min_observations)

    if result["promoted"]:
        print("Promoted instincts:")
        for instinct_key in result["promoted"]:
            print(f"- {instinct_key}")
    else:
        print("No instincts met promotion thresholds.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
