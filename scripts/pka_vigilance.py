#!/usr/bin/env python3
"""Daily vigilance report for PKA_JCH.
 pass pozible
   script is non-destructive. It aggregates security and local hardware
signals into a simple GREEN/ORANGE/RED status.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import subprocess
from pathlib import Path

import pka_security_audit


ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "TEAM_Inbox"
SECURITY_DIR = ROOT / "JCH_Inbox" / "99_SYSTEM" / "security"


def run(command: list[str], timeout: int = 20) -> tuple[int, str, str]:
    try:
        result = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired as exc:
        return 124, exc.stdout or "", "timeout"


def severity_rank(value: str) -> int:
    return {"critical": 4, "high": 3, "medium": 2, "low": 1}.get(value, 0)


def status_from_findings(findings: list[dict]) -> str:
    worst = max((severity_rank(item["severity"]) for item in findings), default=0)
    if worst >= 3:
        return "red"
    if worst >= 1:
        return "orange"
    return "green"


def disk_findings() -> list[dict]:
    findings = []
    total, used, free = shutil.disk_usage("/System/Volumes/Data")
    used_ratio = used / total if total else 0
    if used_ratio >= 0.95:
        findings.append({
            "severity": "medium",
            "check": "disk-space",
            "path": "/System/Volumes/Data",
            "detail": f"Data volume is {used_ratio:.0%} full",
            "mitigation": "free space; target below 85% for comfortable backups and operations",
        })
    elif used_ratio >= 0.90:
        findings.append({
            "severity": "low",
            "check": "disk-space",
            "path": "/System/Volumes/Data",
            "detail": f"Data volume is {used_ratio:.0%} full",
            "mitigation": "plan cleanup before it reaches 95%",
        })
    return findings


def time_machine_findings() -> list[dict]:
    findings = []
    code, out, err = run(["tmutil", "destinationinfo"])
    if "No destinations configured" in out or "No destinations configured" in err:
        findings.append({
            "severity": "high",
            "check": "time-machine",
            "path": "Time Machine",
            "detail": "no destination configured",
            "mitigation": "configure encrypted Time Machine destination",
        })
        return findings
    if code != 0:
        findings.append({
            "severity": "medium",
            "check": "time-machine",
            "path": "Time Machine",
            "detail": err or out or f"tmutil destinationinfo exited {code}",
            "mitigation": "verify Time Machine settings manually",
        })
    return findings


def external_volume_findings() -> list[dict]:
    findings = []
    volumes = Path("/Volumes")
    if not volumes.is_dir():
        return findings
    for volume in volumes.iterdir():
        if volume.name in {"Macintosh HD", "PKA_TimeMachine"}:
            continue
        code, out, _ = run(["diskutil", "info", str(volume)])
        if code != 0:
            continue
        if "File System Personality:   ExFAT" in out or "File System Personality:   NTFS" in out:
            findings.append({
                "severity": "medium",
                "check": "external-volume",
                "path": str(volume),
                "detail": "external volume uses ExFAT/NTFS, not a macOS encrypted format",
                "mitigation": "do not store PKA secrets, DBs, or logs there unless wrapped in encrypted container",
            })
    return findings


def network_findings() -> list[dict]:
    findings = []
    code, out, err = run(["lsof", "-iTCP", "-sTCP:LISTEN", "-n", "-P"])
    if code != 0:
        findings.append({
            "severity": "low",
            "check": "network",
            "path": "lsof",
            "detail": err or "could not inspect listening sockets",
            "mitigation": "rerun manually if network exposure changes",
        })
        return findings

    broad = []
    for line in out.splitlines()[1:]:
        if " TCP *:" in line:
            parts = line.split()
            command = parts[0] if parts else "unknown"
            port = line.rsplit(":", 1)[-1].split()[0]
            broad.append(f"{command}:{port}")

    interesting = [item for item in broad if not item.startswith(("ControlCe:", "rapportd:"))]
    if interesting:
        findings.append({
            "severity": "medium",
            "check": "network",
            "path": "listening sockets",
            "detail": "LAN-listening services: " + ", ".join(sorted(set(interesting))),
            "mitigation": "disable unnecessary services; Epson Event Manager is already in P1 TODO",
        })
    return findings


def cloud_sync_findings() -> list[dict]:
    findings = []
    cloud_paths = [
        Path.home() / "Library" / "CloudStorage" / "Dropbox",
        Path.home() / "Library" / "CloudStorage" / "OneDrive",
        Path.home() / "Library" / "Dropbox",
    ]
    present = [str(path) for path in cloud_paths if path.exists()]
    if present:
        findings.append({
            "severity": "low",
            "check": "cloud-sync",
            "path": ", ".join(present),
            "detail": "cloud sync clients/directories detected",
            "mitigation": "verify PKA_JCH, .env, DBs and logs are excluded or encrypted before sync",
        })
    return findings


def run_vigilance() -> dict:
    security = pka_security_audit.run_audit()
    findings = list(security["findings"])
    findings.extend(disk_findings())
    findings.extend(time_machine_findings())
    findings.extend(external_volume_findings())
    findings.extend(network_findings())
    findings.extend(cloud_sync_findings())
    findings = sorted(findings, key=lambda item: severity_rank(item["severity"]), reverse=True)
    return {
        "generated_at": dt.datetime.now().isoformat(timespec="seconds"),
        "status": status_from_findings(findings),
        "findings": findings,
    }


def markdown_report(result: dict) -> str:
    lines = [
        "# PKA Vigilance Report",
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
            f"{item['detail']} | {item['mitigation']} |"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Rapport de vigilance PKA_JCH")
    parser.add_argument("--json", action="store_true", help="print JSON instead of Markdown")
    parser.add_argument("--write-report", action="store_true", help="write report to TEAM_Inbox")
    args = parser.parse_args()

    result = run_vigilance()
    if args.write_report:
        REPORT_DIR.mkdir(parents=True, exist_ok=True)
        today = dt.date.today().isoformat()
        path = REPORT_DIR / f"{today}_dobby_vigilance.md"
        path.write_text(markdown_report(result), encoding="utf-8")

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(markdown_report(result))
    return 1 if result["status"] == "red" else 0


if __name__ == "__main__":
    raise SystemExit(main())
