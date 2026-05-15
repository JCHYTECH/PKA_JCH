#!/usr/bin/env python3
"""Non-destructive security audit for PKA_JCH."""

from __future__ import annotations

import argparse
import datetime as dt
import fnmatch
import json
import os
import sqlite3
import stat
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SECURITY_DIR = ROOT / "JCH_Inbox" / "99_SYSTEM" / "security"
ALLOWLIST = SECURITY_DIR / "allowlist.json"
REPORT_DIR = ROOT / "TEAM_Inbox"


DEFAULT_SENSITIVE_GLOBS = [
    "*.db",
    "*.sqlite",
    "*.sqlite3",
    "*.log",
    ".env",
    ".env.*",
    "*token*",
    "*secret*",
    "*credentials*",
    "*.key",
    "*.pem",
]

DEFAULT_IGNORED_PATHS = {
    ".git",
    "__pycache__",
    "scripts/telegram-bot/venv",
}


def load_allowlist() -> dict:
    if ALLOWLIST.is_file():
        return json.loads(ALLOWLIST.read_text(encoding="utf-8"))
    return {}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def is_ignored(path: Path, ignored: set[str]) -> bool:
    relative = rel(path)
    parts = set(path.relative_to(ROOT).parts)
    return any(relative == item or relative.startswith(f"{item}/") or item in parts for item in ignored)


def is_sensitive(path: Path, patterns: list[str]) -> bool:
    name = path.name
    if name == ".env.example":
        return False
    relative = rel(path)
    return any(fnmatch.fnmatch(name, pattern) or fnmatch.fnmatch(relative, pattern) for pattern in patterns)


def file_mode(path: Path) -> int:
    return stat.S_IMODE(path.stat().st_mode)


def check_permissions(patterns: list[str], ignored: set[str]) -> list[dict]:
    findings = []
    for path in ROOT.rglob("*"):
        if not path.is_file() or is_ignored(path, ignored):
            continue
        if not is_sensitive(path, patterns):
            continue
        mode = file_mode(path)
        if mode & 0o077:
            findings.append({
                "severity": "high",
                "check": "permissions",
                "path": rel(path),
                "detail": f"mode {mode:04o}, expected 0600 or stricter",
                "mitigation": f"chmod 600 {rel(path)}",
            })
    return findings


def active_count(db_path: Path) -> int | None:
    if not db_path.is_file():
        return None
    with sqlite3.connect(db_path) as conn:
        row = conn.execute("select count(*) from members where status='active'").fetchone()
    return int(row[0])


def semantic_db_signature(db_path: Path) -> list[str]:
    with sqlite3.connect(db_path) as conn:
        return [line for line in conn.iterdump() if not line.startswith("BEGIN TRANSACTION") and not line.startswith("COMMIT")]


def check_roster_drift() -> list[dict]:
    findings = []
    authoritative = ROOT / "TEAM" / "team.db"
    count = active_count(authoritative)
    if count is None:
        return [{
            "severity": "critical",
            "check": "database",
            "path": rel(authoritative),
            "detail": "authoritative database missing",
            "mitigation": "restore TEAM/team.db from latest backup",
        }]

    mirrors = [
        ROOT / "AGENTS.md",
        ROOT / "GEMINI.md",
        ROOT / "ADAPTER-PROMPT.md",
        ROOT / "TEAM" / "ROSTER.md",
    ]
    expected_markers = {
        f"{count} spécialistes",
        f"{count} specialists",
        f"{count} membres actifs",
        f"{count} members active",
        f"{count - 1} spécialistes + Dobby",
        f"{count - 1} specialists + Dobby",
    }
    for mirror in mirrors:
        if not mirror.is_file():
            continue
        text = mirror.read_text(encoding="utf-8", errors="replace")
        if not any(marker in text for marker in expected_markers):
            findings.append({
                "severity": "medium",
                "check": "roster-drift",
                "path": rel(mirror),
                "detail": f"does not mention current active count {count}",
                "mitigation": "sync markdown mirror from TEAM/team.db",
            })

    root_db = ROOT / "team.db"
    if root_db.is_file() and semantic_db_signature(root_db) != semantic_db_signature(authoritative):
        findings.append({
            "severity": "high",
            "check": "db-drift",
            "path": rel(root_db),
            "detail": "root team.db differs semantically from TEAM/team.db",
            "mitigation": "sync the compatibility mirror or update scripts to stop using it",
        })
    return findings


def check_backups() -> list[dict]:
    backup_dir = ROOT / "TEAM" / "backups"
    backups = sorted(backup_dir.glob("team_*.db")) if backup_dir.is_dir() else []
    if not backups:
        return [{
            "severity": "critical",
            "check": "backups",
            "path": rel(backup_dir),
            "detail": "no team.db backups found",
            "mitigation": "run scripts/backup_team_db.py",
        }]
    latest = max(backups, key=lambda item: item.stat().st_mtime)
    age_hours = (dt.datetime.now().timestamp() - latest.stat().st_mtime) / 3600
    if age_hours > 36:
        return [{
            "severity": "high",
            "check": "backups",
            "path": rel(latest),
            "detail": f"latest backup is {age_hours:.1f} hours old",
            "mitigation": "run scripts/backup_team_db.py and verify scheduler",
        }]
    return []


def check_gitignore() -> list[dict]:
    path = ROOT / ".gitignore"
    if not path.is_file():
        return [{
            "severity": "high",
            "check": "gitignore",
            "path": ".gitignore",
            "detail": "missing security exclusions",
            "mitigation": "create .gitignore before initializing or publishing a repo",
        }]
    text = path.read_text(encoding="utf-8", errors="replace")
    required = [".env", "*.db", "*.log", "venv/"]
    missing = [item for item in required if item not in text]
    if missing:
        return [{
            "severity": "medium",
            "check": "gitignore",
            "path": ".gitignore",
            "detail": f"missing patterns: {', '.join(missing)}",
            "mitigation": "add missing sensitive patterns",
        }]
    return []


def run_audit() -> dict:
    allowlist = load_allowlist()
    patterns = allowlist.get("sensitive_globs", DEFAULT_SENSITIVE_GLOBS)
    ignored = set(allowlist.get("ignored_paths", [])) | DEFAULT_IGNORED_PATHS
    findings = []
    findings.extend(check_permissions(patterns, ignored))
    findings.extend(check_roster_drift())
    findings.extend(check_backups())
    findings.extend(check_gitignore())

    severity_order = {"critical": 4, "high": 3, "medium": 2, "low": 1}
    worst = max((severity_order.get(item["severity"], 0) for item in findings), default=0)
    status = "green" if worst == 0 else "orange" if worst <= 2 else "red"
    return {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "status": status,
        "findings": sorted(findings, key=lambda item: severity_order.get(item["severity"], 0), reverse=True),
    }


def markdown_report(result: dict) -> str:
    lines = [
        "# PKA Security Audit",
        "",
        f"_Generated: {result['generated_at']}_",
        f"_Status: {result['status'].upper()}_",
        "",
    ]
    if not result["findings"]:
        lines.append("No findings.")
        return "\n".join(lines) + "\n"

    lines.extend(["| Severity | Check | Path | Detail | Mitigation |", "|---|---|---|---|---|"])
    for item in result["findings"]:
        lines.append(
            f"| {item['severity']} | {item['check']} | `{item['path']}` | "
            f"{item['detail']} | `{item['mitigation']}` |"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit local securite PKA_JCH")
    parser.add_argument("--json", action="store_true", help="print JSON instead of Markdown")
    parser.add_argument("--write-report", action="store_true", help="write Markdown report to TEAM_Inbox")
    args = parser.parse_args()

    result = run_audit()
    if args.write_report:
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        today = dt.date.today().isoformat()
        path = REPORT_DIR / f"{today}_dobby_security-audit.md"
        path.write_text(markdown_report(result), encoding="utf-8")

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(markdown_report(result))
    return 1 if result["status"] == "red" else 0


if __name__ == "__main__":
    raise SystemExit(main())
