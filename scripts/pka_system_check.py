#!/usr/bin/env python3
"""Run the main PKA system checks in one command."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path

try:
    from scripts import generate_tool_pointers
    from scripts import instinct_promote
    from scripts import pka_security_audit
    from scripts import pka_system_improvement_audit
except ModuleNotFoundError:
    import generate_tool_pointers
    import instinct_promote
    import pka_security_audit
    import pka_system_improvement_audit


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "TEAM_Inbox"


def combine_results(security: dict, improvement: dict, pointers: dict, promotion: dict) -> dict:
    statuses = [security["status"], improvement["status"], pointers["status"], promotion["status"]]
    if "red" in statuses:
        status = "red"
    elif "orange" in statuses:
        status = "orange"
    else:
        status = "green"
    return {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "status": status,
        "security": security,
        "improvement": improvement,
        "pointers": pointers,
        "promotion": promotion,
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
    if result["promotion"].get("details"):
        lines.append("## Instinct Promotion")
        lines.append("")
        for item in result["promotion"]["details"]:
            lines.append(f"- {item}")
        lines.append("")
    if result["status"] == "green":
        lines.append("No findings.")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the main PKA system checks")
    parser.add_argument("--json", action="store_true", help="Print JSON instead of Markdown")
    parser.add_argument("--write-report", action="store_true", help="Write report to TEAM_Inbox")
    args = parser.parse_args()

    security = pka_security_audit.run_audit()
    improvement = pka_system_improvement_audit.run_audit()
    pointers = pointer_status()
    promotion = promotion_status()
    result = combine_results(security, improvement, pointers, promotion)

    if args.write_report:
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        report_path = REPORT_DIR / f"{dt.date.today().isoformat()}_dobby_system_check.md"
        report_path.write_text(markdown_report(result), encoding="utf-8")

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(markdown_report(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
