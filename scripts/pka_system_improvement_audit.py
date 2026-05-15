#!/usr/bin/env python3
"""Operational improvement audit for PKA_JCH."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sqlite3
from pathlib import Path

try:
    from scripts import generate_tool_pointers
except ModuleNotFoundError:
    import generate_tool_pointers


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "TEAM_Inbox"


def severity_rank(value: str) -> int:
    return {"critical": 4, "high": 3, "medium": 2, "low": 1}.get(value, 0)


def status_from_findings(findings: list[dict]) -> str:
    worst = max((severity_rank(item["severity"]) for item in findings), default=0)
    if worst >= 3:
        return "red"
    if worst >= 1:
        return "orange"
    return "green"


def active_count(db_path: Path) -> int | None:
    if not db_path.is_file():
        return None
    with sqlite3.connect(db_path) as conn:
        row = conn.execute("SELECT count(*) FROM members WHERE status='active'").fetchone()
    return int(row[0])


def check_instruction_surface() -> list[dict]:
    findings = []
    db_path = ROOT / "TEAM" / "team.db"
    count = active_count(db_path)
    if count is None:
        findings.append({
            "severity": "high",
            "check": "instruction-surface",
            "path": str(db_path.relative_to(ROOT)),
            "detail": "TEAM/team.db missing; cannot validate overlays against roster source of truth",
            "mitigation": "restore TEAM/team.db before relying on overlay audits",
            "quick_win": False,
        })
        return findings

    expected_markers = [
        f"{count} membres actifs",
        f"{count} members active",
        f"{count} spécialistes",
        f"{count - 1} spécialistes + Dobby",
        f"{count - 1} specialists + Dobby",
    ]
    for name in ("CLAUDE.md", "AGENTS.md", "GEMINI.md", "DEEPSEEK.md", "ADAPTER-PROMPT.md"):
        path = ROOT / name
        if not path.is_file():
            findings.append({
                "severity": "medium",
                "check": "instruction-surface",
                "path": name,
                "detail": "overlay file missing",
                "mitigation": "create or sync the missing tool overlay from the canonical PKA instructions",
                "quick_win": True,
            })
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        if not any(marker in text for marker in expected_markers):
            findings.append({
                "severity": "medium",
                "check": "instruction-surface",
                "path": name,
                "detail": f"overlay does not mention active roster count {count}",
                "mitigation": "sync overlay wording with TEAM/team.db roster count",
                "quick_win": True,
            })
    return findings


def check_pointer_generation_drift() -> list[dict]:
    findings = []
    originals = {
        "ROOT": generate_tool_pointers.ROOT,
        "DB_PATH": generate_tool_pointers.DB_PATH,
        "CONFIG_PATH": generate_tool_pointers.CONFIG_PATH,
        "PROJECTS_DIR": generate_tool_pointers.PROJECTS_DIR,
        "INBOX_DIR": generate_tool_pointers.INBOX_DIR,
        "CLAUDE_PATH": generate_tool_pointers.CLAUDE_PATH,
    }
    try:
        generate_tool_pointers.ROOT = ROOT
        generate_tool_pointers.DB_PATH = ROOT / "TEAM" / "team.db"
        generate_tool_pointers.CONFIG_PATH = ROOT / "JCH_Inbox" / "99_SYSTEM" / "tool_pointer_config.json"
        generate_tool_pointers.PROJECTS_DIR = ROOT / "JCH_Inbox" / "03_PROJECTS"
        generate_tool_pointers.INBOX_DIR = ROOT / "JCH_Inbox" / "00_INBOX"
        generate_tool_pointers.CLAUDE_PATH = ROOT / "CLAUDE.md"
        rc = generate_tool_pointers.generate(check=True)
    finally:
        for key, value in originals.items():
            setattr(generate_tool_pointers, key, value)

    if rc != 0:
        findings.append({
            "severity": "medium",
            "check": "pointer-generation",
            "path": "CLAUDE.md / AGENTS.md / GEMINI.md / DEEPSEEK.md",
            "detail": "generated pointer surfaces are drifting from the canonical config",
            "mitigation": "run `python3 scripts/generate_tool_pointers.py` to resync the managed surfaces",
            "quick_win": True,
        })
    return findings


def check_script_surface() -> list[dict]:
    findings = []
    required = {
        "scripts/skill_search.py": "skill retrieval layer",
        "scripts/skill_write.py": "skill persistence layer",
        "scripts/pka_security_audit.py": "security audit baseline",
        "scripts/pka_vigilance.py": "daily vigilance baseline",
    }
    for relative, purpose in required.items():
        path = ROOT / relative
        if not path.is_file():
            findings.append({
                "severity": "high",
                "check": "script-surface",
                "path": relative,
                "detail": f"missing required script for {purpose}",
                "mitigation": "restore or recreate the missing orchestration script",
                "quick_win": False,
            })
    return findings


def check_hook_surface() -> list[dict]:
    findings = []
    settings = ROOT / ".claude" / "settings.local.json"
    if not settings.is_file():
        findings.append({
            "severity": "medium",
            "check": "hook-surface",
            "path": ".claude/settings.local.json",
            "detail": "Claude local settings missing; session-start/session-stop automation cannot be reviewed",
            "mitigation": "restore settings.local.json or document why this harness runs without it",
            "quick_win": False,
        })
        return findings

    try:
        data = json.loads(settings.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        findings.append({
            "severity": "high",
            "check": "hook-surface",
            "path": ".claude/settings.local.json",
            "detail": f"invalid JSON: {exc}",
            "mitigation": "repair the local Claude settings JSON before relying on hooks",
            "quick_win": True,
        })
        return findings

    hooks = data.get("hooks", {})
    for required_hook in ("SessionStart", "Stop"):
        if required_hook not in hooks:
            findings.append({
                "severity": "medium",
                "check": "hook-surface",
                "path": ".claude/settings.local.json",
                "detail": f"{required_hook} hook missing",
                "mitigation": f"restore a {required_hook} automation entry for Dobby lifecycle reminders or loaders",
                "quick_win": True,
            })
    if "PreToolUse" not in hooks:
        findings.append({
            "severity": "low",
            "check": "hook-surface",
            "path": ".claude/settings.local.json",
            "detail": "no PreToolUse automation present for strategic checks or compaction prompts",
            "mitigation": "consider adding lightweight PreToolUse hooks for context and efficiency guidance",
            "quick_win": False,
        })
    return findings


def check_skills_surface() -> list[dict]:
    findings = []
    db_path = ROOT / "TEAM" / "team.db"
    if not db_path.is_file():
        return findings

    with sqlite3.connect(db_path) as conn:
        columns = {row[1] for row in conn.execute("PRAGMA table_info(skills)")}
        required = {"source_kind", "confidence", "scope", "project_key", "updated_at"}
        missing = sorted(required - columns)
        if missing:
            findings.append({
                "severity": "medium",
                "check": "skills-surface",
                "path": "TEAM/team.db::skills",
                "detail": f"missing metadata columns: {', '.join(missing)}",
                "mitigation": "run the skills metadata migration before depending on scoped/system skill analysis",
                "quick_win": True,
            })

        row = conn.execute("SELECT COUNT(*) FROM skills").fetchone()
        total = int(row[0]) if row else 0
        if total == 0:
            findings.append({
                "severity": "medium",
                "check": "skills-surface",
                "path": "TEAM/team.db::skills",
                "detail": "no reusable skills registered",
                "mitigation": "seed the database with at least the core operating procedures Dobby should reuse",
                "quick_win": False,
            })

        if "source_kind" in columns:
            learned = conn.execute(
                "SELECT COUNT(*) FROM skills WHERE source_kind = 'system'"
            ).fetchone()
            system_count = int(learned[0]) if learned else 0
            if system_count == 0:
                findings.append({
                    "severity": "low",
                    "check": "skills-surface",
                    "path": "TEAM/team.db::skills",
                    "detail": "no system-tagged skills registered yet",
                    "mitigation": "register at least the core system-improvement skill for future requests",
                    "quick_win": True,
                })
    return findings


def run_audit() -> dict:
    findings = []
    findings.extend(check_instruction_surface())
    findings.extend(check_pointer_generation_drift())
    findings.extend(check_script_surface())
    findings.extend(check_hook_surface())
    findings.extend(check_skills_surface())
    findings = sorted(findings, key=lambda item: severity_rank(item["severity"]), reverse=True)
    return {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "status": status_from_findings(findings),
        "findings": findings,
    }


def markdown_report(result: dict) -> str:
    lines = [
        "# PKA System Improvement Audit",
        "",
        f"_Generated: {result['generated_at']}_",
        f"_Status: {result['status'].upper()}_",
        "",
    ]
    if not result["findings"]:
        lines.append("No findings.")
        return "\n".join(lines) + "\n"

    lines.extend(["## Findings", "", "| Severity | Check | Path | Detail | Mitigation |", "|---|---|---|---|---|"])
    for item in result["findings"]:
        lines.append(
            f"| {item['severity']} | {item['check']} | `{item['path']}` | "
            f"{item['detail']} | {item['mitigation']} |"
        )

    quick_wins = [item for item in result["findings"] if item.get("quick_win")]
    lines.extend(["", "## Quick Wins", ""])
    if not quick_wins:
        lines.append("No quick wins identified.")
    else:
        for item in quick_wins:
            lines.append(f"- `{item['path']}`: {item['mitigation']}")

    lines.extend(["", "## Recommended Next Steps", ""])
    if result["status"] == "red":
        lines.append("- Resolve the highest-severity structural issues before adding more automation.")
    else:
        lines.append("- Stabilize overlay and hooks drift before broadening the system surface.")
        lines.append("- Use the skills metadata layer to separate reusable system procedures from ad hoc task memory.")

    lines.extend(["", "## Future Architecture Notes", ""])
    lines.append("- A later instinct layer can sit beneath `skills` once the metadata model is stable.")
    lines.append("- Generated multi-tool overlays remain a future target after current drift becomes measurable.")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Operational improvement audit for PKA_JCH")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of Markdown")
    parser.add_argument("--write-report", action="store_true", help="Write the markdown report to TEAM_Inbox")
    args = parser.parse_args()

    result = run_audit()
    if args.write_report:
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        report_path = REPORT_DIR / f"{dt.date.today().isoformat()}_dobby_system_improvement_audit.md"
        report_path.write_text(markdown_report(result), encoding="utf-8")

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(markdown_report(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
