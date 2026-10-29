#!/usr/bin/env python3
"""Run the main PKA system checks in one command — with auto-heal and differential reporting."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path

try:
    from scripts import generate_tool_pointers
    from scripts import instinct_promote
    from scripts import pka_security_audit
    from scripts import pka_system_improvement_audit
    from scripts import pka_structure_check
except ModuleNotFoundError:
    import generate_tool_pointers
    import instinct_promote
    import pka_security_audit
    import pka_system_improvement_audit
    import pka_structure_check


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "TEAM_Inbox"
STATE_FILE = ROOT / "_local" / "system_check_state.json"


def combine_results(security: dict, improvement: dict,
                    pointers: dict, promotion: dict,
                    structure: dict | None = None) -> dict:
    checks = {
        "security": security, "improvement": improvement,
        "pointers": pointers, "promotion": promotion,
    }
    if structure:
        checks["structure"] = structure
    statuses = [c["status"] for c in checks.values()]
    if "red" in statuses:
        status = "red"
    elif "orange" in statuses:
        status = "orange"
    else:
        status = "green"
    return {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "status": status,
        **checks,
    }


def pointer_status() -> dict:
    rc = generate_tool_pointers.generate(check=True)
    return {
        "status": "green" if rc == 0 else "orange",
        "details": [] if rc == 0 else ["canonical pointer surfaces are drifting"],
    }


def promotion_status() -> dict:
    config = instinct_promote.load_config()
    result = instinct_promote.evaluate_instincts(
        min_confidence=config.get("min_confidence", 0.8),
        min_observations=config.get("min_observations", 2),
        allow_scopes=config.get("allow_scopes", ["global", "project"]),
        allow_source_kinds=config.get("allow_source_kinds", ["learned", "system"]),
    )
    if result["promoted"]:
        return {
            "status": "orange",
            "details": [f"{len(result['promoted'])} instincts ready for promotion review"],
            "promoted": result["promoted"],
        }
    return {"status": "green", "details": [], "promoted": []}


def markdown_report(result: dict) -> str:
    lines = [
        "# PKA System Check",
        "",
        f"_Generated: {result['generated_at']}_",
        f"_Status: {result['status'].upper()}_",
        "",
        "## Components",
        "",
        f"- Security audit: `{result['security']['status'].upper()}`",
        f"- System improvement audit: `{result['improvement']['status'].upper()}`",
        f"- Pointer generation drift: `{result['pointers']['status'].upper()}`",
        f"- File placement drift: `{result.get('structure', {}).get('status', 'skipped').upper()}`",
        f"- Instinct promotion: `{result['promotion']['status'].upper()}`",
        "",
    ]
    if result["security"].get("findings"):
        lines.append("## Security Findings")
        lines.append("")
        for item in result["security"]["findings"]:
            lines.append(f"- `{item['severity']}` `{item['check']}` {item['path']}: {item['detail']}")
        lines.append("")
    if result["improvement"].get("findings"):
        lines.append("## Improvement Findings")
        lines.append("")
        for item in result["improvement"]["findings"]:
            lines.append(f"- `{item['severity']}` `{item['check']}` {item['path']}: {item['detail']}")
        lines.append("")
    if result["pointers"].get("details"):
        lines.append("## Pointer Drift")
        lines.append("")
        for item in result["pointers"]["details"]:
            lines.append(f"- {item}")
        lines.append("")
    if result.get("structure") and result["structure"].get("findings"):
        lines.append("## Structure Drift")
        lines.append("")
        for item in result["structure"]["findings"]:
            lines.append(f"- `{item['severity']}` `{item['check']}` {item['path']}: {item['detail']}")
        lines.append("")
    if result["promotion"].get("details"):
        lines.append("## Instinct Promotion")
        lines.append("")
        for item in result["promotion"]["details"]:
            lines.append(f"- {item}")
        lines.append("")
    if result["status"] == "green":
        lines.append("No findings.")
    return "\n".join(lines) + "\n"


def result_hash(result: dict) -> str:
    """Deterministic hash of check statuses — ignore timestamps."""
    key = {
        "security": result["security"]["status"],
        "improvement": result["improvement"]["status"],
        "pointers": result["pointers"]["status"],
        "promotion": result["promotion"]["status"],
        "structure": result.get("structure", {}).get("status", "skipped"),
    }
    return hashlib.sha256(json.dumps(key, sort_keys=True).encode()).hexdigest()[:16]


def load_last_state() -> str | None:
    if STATE_FILE.is_file():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8")).get("hash")
        except (json.JSONDecodeError, KeyError):
            return None
    return None


def save_state(state_hash: str) -> None:
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps({
        "hash": state_hash,
        "updated_at": dt.datetime.now().isoformat(timespec="seconds"),
    }), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the main PKA system checks")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of Markdown")
    parser.add_argument("--write-report", action="store_true", help="Write report to TEAM_Inbox")
    parser.add_argument("--auto-heal", action="store_true", help="Auto-fix permissions via security audit")
    parser.add_argument("--force", action="store_true", help="Write report even if state unchanged")
    args = parser.parse_args()

    security = pka_security_audit.run_audit(auto_heal=args.auto_heal)
    improvement = pka_system_improvement_audit.run_audit()
    pointers = pointer_status()
    promotion = promotion_status()
    structure = pka_structure_check.run_structure_check()
    result = combine_results(security, improvement, pointers, promotion, structure)

    if args.write_report:
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        current_hash = result_hash(result)
        last_hash = load_last_state()

        if args.force or current_hash != last_hash:
            report_path = REPORT_DIR / f"{dt.date.today().isoformat()}_dobby_system_check.md"
            report_path.write_text(markdown_report(result), encoding="utf-8")
            save_state(current_hash)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(markdown_report(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
