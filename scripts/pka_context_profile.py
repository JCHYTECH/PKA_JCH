#!/usr/bin/env python3
"""Project context profile selection for PKA_JCH."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "JCH_Inbox" / "99_SYSTEM" / "context_profiles.json"


def load_profiles() -> list[dict]:
    data = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    return data.get("profiles", [])


def infer_project_key(query: str) -> str | None:
    query_lc = query.lower()
    for profile in load_profiles():
        if any(term.lower() in query_lc for term in profile.get("trigger_terms", [])):
            return profile["project_key"]
    return None


def select_profile(query: str | None = None, project_key: str | None = None) -> dict | None:
    resolved_key = project_key or (infer_project_key(query or "") if query else None)
    if resolved_key is None:
        return None
    for profile in load_profiles():
        if profile["project_key"] == resolved_key:
            return profile
    return None


def markdown_profile(profile: dict | None) -> str:
    if profile is None:
        return "No matching context profile.\n"
    lines = [
        f"# {profile['label']} Context Profile",
        "",
        f"- `project_key`: `{profile['project_key']}`",
        f"- `specialist_hint`: `{profile.get('specialist_hint', '')}`",
        f"- `roots`: {', '.join(f'`{root}`' for root in profile.get('roots', []))}",
        f"- `paired_skills`: {', '.join(f'`{item}`' for item in profile.get('paired_skills', [])) or 'none'}",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Select a PKA context profile")
    parser.add_argument("--query", default=None)
    parser.add_argument("--project-key", default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    profile = select_profile(query=args.query, project_key=args.project_key)
    if args.json:
        print(json.dumps(profile, ensure_ascii=False, indent=2))
    else:
        print(markdown_profile(profile))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
