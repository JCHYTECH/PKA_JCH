#!/usr/bin/env python3
"""pka_agent_usage.py — Compteur d'utilisation des sous-agents par Dobby.

Mesure la part de réponses où Dobby délègue à un sous-agent (agent_open),
pour répondre à : « quel % de tes réponses utilisent des agents ? ».

Usage :
    python3 scripts/pka_agent_usage.py --turn      # enregistrer une réponse (début de tour)
    python3 scripts/pka_agent_usage.py --agent     # enregistrer une activation d'agent
    python3 scripts/pka_agent_usage.py --report    # afficher les stats
    python3 scripts/pka_agent_usage.py --reset     # remise à zéro

Métriques :
    turns               : nombre total de réponses
    agent_activations   : nombre total d'appels agent_open
    turns_with_agents   : nombre de réponses avec ≥1 agent
    % tours avec agents : turns_with_agents / turns
    agents / tour       : agent_activations / turns
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

PKA_ROOT = Path(__file__).resolve().parents[1]
STATE_PATH = PKA_ROOT / "_local" / "state" / "agent-usage.json"

DEFAULTS = {
    "turns": 0,
    "agent_activations": 0,
    "turns_with_agents": 0,
    "agent_this_turn": False,
    "started": None,
    "updated": None,
}


def _load() -> dict:
    if STATE_PATH.exists():
        try:
            data = json.loads(STATE_PATH.read_text(encoding="utf-8"))
            for k, v in DEFAULTS.items():
                data.setdefault(k, v)
            return data
        except (json.JSONDecodeError, OSError):
            pass
    return dict(DEFAULTS)


def _save(data: dict) -> None:
    STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    data["updated"] = datetime.now().isoformat(timespec="seconds")
    STATE_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False),
                          encoding="utf-8")


def record_turn() -> None:
    data = _load()
    if data["started"] is None:
        data["started"] = datetime.now().isoformat(timespec="seconds")
    data["turns"] += 1
    data["agent_this_turn"] = False
    _save(data)


def record_agent() -> None:
    data = _load()
    if data["started"] is None:
        data["started"] = datetime.now().isoformat(timespec="seconds")
    if data["turns"] == 0:
        # bootstrap : un agent sans --turn préalable compte pour un tour implicite
        data["turns"] = 1
    data["agent_activations"] += 1
    if not data["agent_this_turn"]:
        data["turns_with_agents"] += 1
        data["agent_this_turn"] = True
    _save(data)


def report() -> dict:
    data = _load()
    turns = data["turns"]
    agents = data["agent_activations"]
    twa = data["turns_with_agents"]
    pct = round(100 * twa / turns, 1) if turns else 0.0
    ratio = round(agents / turns, 2) if turns else 0.0
    return {
        "started": data["started"],
        "updated": data["updated"],
        "turns": turns,
        "agent_activations": agents,
        "turns_with_agents": twa,
        "pct_turns_with_agents": pct,
        "agents_per_turn": ratio,
    }


def reset() -> None:
    _save(dict(DEFAULTS))


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--turn", action="store_true", help="enregistrer une réponse")
    g.add_argument("--agent", action="store_true", help="enregistrer une activation d'agent")
    g.add_argument("--report", action="store_true", help="afficher les stats")
    g.add_argument("--json", action="store_true", help="stats en JSON")
    g.add_argument("--reset", action="store_true", help="remise à zéro")
    args = p.parse_args()

    if args.turn:
        record_turn()
        print(f"turn enregistré — total {_load()['turns']}")
    elif args.agent:
        record_agent()
        print(f"agent enregistré — total {_load()['agent_activations']}")
    elif args.reset:
        reset()
        print("compteur remis à zéro")
    else:
        r = report()
        if args.json:
            print(json.dumps(r, indent=2, ensure_ascii=False))
        else:
            print("Utilisation des sous-agents "
                  f"(depuis {r['started'] or '—'})")
            print("─" * 44)
            print(f"Réponses (tours)        : {r['turns']}")
            print(f"Activations d'agents    : {r['agent_activations']}")
            print(f"Tours avec ≥1 agent     : {r['turns_with_agents']}")
            print(f"% tours avec agents     : {r['pct_turns_with_agents']} %")
            print(f"Agents / tour (moyenne) : {r['agents_per_turn']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
