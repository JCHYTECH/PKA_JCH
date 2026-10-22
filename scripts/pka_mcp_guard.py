#!/usr/bin/env python3
"""
pka_mcp_guard.py — Gouvernance des serveurs MCP PKA (P2).

Répond au risque 2026 « tool poisoning » (OWASP Agentic ASI01) : la description
d'un outil MCP est du texte lu par l'agent mais rarement inspecté par l'humain.

Deux fonctions :
  1. REGISTRE — liste versionnée des serveurs approuvés (nom, commande, hash du
     schéma d'outils). Serveur inconnu ou schéma modifié => alerte.
  2. SCAN — analyse des descriptions d'outils pour détecter des instructions
     cachées (injection indirecte dans le manifeste MCP).

Usage :
  python3 scripts/pka_mcp_guard.py audit              # audit config + registre
  python3 scripts/pka_mcp_guard.py scan-tools <json>  # scanne une liste d'outils
  python3 scripts/pka_mcp_guard.py freeze             # enregistre les hashes actuels
  python3 scripts/pka_mcp_guard.py --help

Format de l'entrée scan-tools (sortie de tools/list) :
  {"tools": [{"name": "...", "description": "..."}, ...]}
  ou directement [{"name": ..., "description": ...}, ...]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path

PKA_ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = PKA_ROOT / "JCH_Inbox" / "99_SYSTEM" / "mcp_registry.json"
DEEPSEEK_CFG = Path("~/.deepseek/config.toml").expanduser()

# ── Signatures d'injection dans les descriptions d'outils ────────────────────
INJECTION_PATTERNS = [
    (r"ignore\s+(all\s+)?(previous|prior|above)\s+instructions", 40),
    (r"(before|after)\s+using\s+this\s+tool[^.]{0,80}(read|send|upload|delete|exfiltrat)", 35),
    (r"(do\s+not|don't)\s+(tell|inform|mention\s+to)\s+the\s+user", 35),
    (r"(secretly|silently|without\s+(the\s+)?user'?s?\s+(knowledge|consent))", 35),
    (r"(send|post|upload|email)\s+(the\s+)?(contents?|data|keys?|tokens?)\s+to", 40),
    (r"(read|access)\s+(~/\.ssh|\.env|credentials|api[_-]?key)", 40),
    (r"(system\s*prompt|your\s+instructions|hidden\s+prompt)", 25),
    (r"<\s*important\s*>|<\s*admin\s*>|\[system\]", 20),
    (r"(execute|run)\s+(shell|bash|cmd|powershell)\s+command", 30),
    (r"(curl|wget|invoke-webrequest)\s+https?://", 30),
]

INVISIBLE_RE = re.compile(r"[\u200b-\u200f\u202a-\u202e\u2060-\u2064\ufeff]")
BASE64_LONG = re.compile(r"[A-Za-z0-9+/]{120,}={0,2}")


def score_description(text: str) -> tuple[int, list[str]]:
    """Retourne (score 0-100, raisons)."""
    score = 0
    reasons: list[str] = []
    low = text.lower()

    for pattern, weight in INJECTION_PATTERNS:
        if re.search(pattern, low):
            score += weight
            reasons.append(f"pattern: {pattern[:48]}")

    if INVISIBLE_RE.search(text):
        score += 30
        reasons.append("caractères invisibles (zero-width / bidi)")

    if BASE64_LONG.search(text):
        score += 25
        reasons.append("blob base64 suspect (>120 chars)")

    if len(text) > 2000:
        score += 10
        reasons.append(f"description anormalement longue ({len(text)} chars)")

    return min(score, 100), reasons


def load_registry() -> dict:
    if REGISTRY_PATH.exists():
        return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    return {"version": 1, "created": None, "servers": {}}


def save_registry(reg: dict) -> None:
    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY_PATH.write_text(json.dumps(reg, indent=2, ensure_ascii=False), encoding="utf-8")


def parse_deepseek_servers() -> list[dict]:
    """Parse minimal des [[mcp_servers]] de config.toml (sans dépendance TOML)."""
    if not DEEPSEEK_CFG.exists():
        return []
    text = DEEPSEEK_CFG.read_text(encoding="utf-8")
    servers = []
    for block in re.split(r"\[\[mcp_servers\]\]", text)[1:]:
        block = block.split("[[")[0]
        name = re.search(r'name\s*=\s*"([^"]+)"', block)
        cmd = re.search(r'command\s*=\s*"([^"]+)"', block)
        args = re.findall(r'"([^"]*)"', block.split("args")[1]) if "args" in block else []
        servers.append({
            "name": name.group(1) if name else "?",
            "command": cmd.group(1) if cmd else "?",
            "args": args,
        })
    return servers


def fingerprint(server: dict) -> str:
    payload = f"{server['name']}|{server['command']}|{' '.join(server.get('args', []))}"
    return hashlib.sha256(payload.encode()).hexdigest()[:16]


def cmd_audit() -> int:
    reg = load_registry()
    servers = parse_deepseek_servers()
    print(f"Registre : {REGISTRY_PATH} ({len(reg['servers'])} serveur(s) approuvé(s))")
    print(f"Config   : {DEEPSEEK_CFG} ({len(servers)} serveur(s) déclaré(s))\n")

    problems = 0
    for s in servers:
        fp = fingerprint(s)
        known = reg["servers"].get(s["name"])
        if not known:
            print(f"  ⚠️  NON APPROUVÉ : {s['name']} ({s['command']}) — hash {fp}")
            problems += 1
        elif known.get("fingerprint") != fp:
            print(f"  ⚠️  MODIFIÉ : {s['name']} — hash {known.get('fingerprint')} → {fp}")
            problems += 1
        else:
            print(f"  ✅ {s['name']} — approuvé (hash {fp})")

    orphans = set(reg["servers"]) - {s["name"] for s in servers}
    for o in orphans:
        print(f"  ℹ️  {o} : au registre mais plus déclaré")

    print(f"\nRésultat : {problems} anomalie(s).")
    return 1 if problems else 0


def cmd_freeze() -> int:
    reg = load_registry()
    servers = parse_deepseek_servers()
    for s in servers:
        fp = fingerprint(s)
        entry = reg["servers"].get(s["name"], {})
        entry.update({
            "command": s["command"],
            "args": s.get("args", []),
            "fingerprint": fp,
            "approved_on": entry.get("approved_on") or datetime.now().date().isoformat(),
        })
        reg["servers"][s["name"]] = entry
    reg["created"] = reg.get("created") or datetime.now().isoformat(timespec="seconds")
    save_registry(reg)
    print(f"Registre mis à jour : {len(servers)} serveur(s) approuvé(s) → {REGISTRY_PATH}")
    return 0


def cmd_scan_tools(path: str) -> int:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    tools = data.get("tools", data) if isinstance(data, dict) else data
    flagged = 0
    print(f"Scan de {len(tools)} description(s) d'outils\n")
    for t in tools:
        name = t.get("name", "?")
        desc = t.get("description", "") or ""
        score, reasons = score_description(desc)
        verdict = "QUARANTAINE" if score > 50 else ("ATTENTION" if score >= 20 else "ok")
        mark = {"ok": "✅", "ATTENTION": "⚠️ ", "QUARANTAINE": "🔴"}[verdict]
        print(f"  {mark} {name:32} score={score:3d}  {verdict}")
        for r in reasons:
            print(f"       · {r}")
        if score >= 20:
            flagged += 1
    print(f"\n{flagged} outil(s) à examiner.")
    return 1 if flagged else 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd")
    sub.add_parser("audit", help="Comparer config et registre")
    sub.add_parser("freeze", help="Approuver/enregistrer les hashes actuels")
    st = sub.add_parser("scan-tools", help="Scanner les descriptions d'outils MCP")
    st.add_argument("path", help="Fichier JSON (sortie de tools/list)")
    args = p.parse_args()

    if args.cmd == "audit":
        return cmd_audit()
    if args.cmd == "freeze":
        return cmd_freeze()
    if args.cmd == "scan-tools":
        return cmd_scan_tools(args.path)
    p.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
