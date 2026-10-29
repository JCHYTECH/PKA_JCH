#!/usr/bin/env python3
"""MCP server — Plane PKA. Expose 5 outils pour gérer issues et cycles."""

import json
import os
from pathlib import Path
from urllib import request, error

from mcp.server.fastmcp import FastMCP

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "JCH_Inbox" / "99_SYSTEM" / "pka_plane_config.json"

mcp = FastMCP("pka-plane")


def _cfg() -> dict:
    return json.loads(CONFIG_PATH.read_text())


def _token() -> str:
    tok = os.environ.get("PKA_PLANE_API_TOKEN", "")
    if not tok:
        raise RuntimeError("PKA_PLANE_API_TOKEN non défini")
    return tok


def _get(url: str) -> dict:
    req = request.Request(url, headers={"X-API-Key": _token()})
    with request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())


def _post(url: str, data: dict) -> dict:
    body = json.dumps(data).encode()
    req = request.Request(url, data=body, headers={
        "X-API-Key": _token(), "Content-Type": "application/json"
    }, method="POST")
    with request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())


def _patch(url: str, data: dict) -> dict:
    body = json.dumps(data).encode()
    req = request.Request(url, data=body, headers={
        "X-API-Key": _token(), "Content-Type": "application/json"
    }, method="PATCH")
    with request.urlopen(req, timeout=10) as r:
        return json.loads(r.read())


@mcp.tool()
def list_projects() -> str:
    """Liste tous les projets PKA avec leur slug et ID Plane."""
    cfg = _cfg()
    lines = []
    for key, val in cfg["projects"].items():
        lines.append(f"{key}: {val['plane_project_id']}")
    return "\n".join(lines)


@mcp.tool()
def list_issues(project_key: str, state: str = "") -> str:
    """Liste les issues d'un projet. project_key ex: 03_WILDNEXUS. state optionnel: backlog/unstarted/started/completed/cancelled."""
    cfg = _cfg()
    pid = cfg["projects"][project_key]["plane_project_id"]
    ws = cfg["workspace_slug"]
    base = cfg["api_base"]
    url = f"{base}/workspaces/{ws}/projects/{pid}/issues/?per_page=50"
    if state:
        url += f"&state_type={state}"
    data = _get(url)
    results = data.get("results", data) if isinstance(data, dict) else data
    if not results:
        return "Aucune issue."
    lines = []
    for i in results[:30]:
        lines.append(f"[{i.get('sequence_id','?')}] {i.get('name','')} — {i.get('state_detail',{}).get('name','?')}")
    return "\n".join(lines)


@mcp.tool()
def create_issue(project_key: str, title: str, description: str = "", priority: str = "none") -> str:
    """Crée une issue dans un projet Plane. priority: urgent/high/medium/low/none."""
    cfg = _cfg()
    pid = cfg["projects"][project_key]["plane_project_id"]
    ws = cfg["workspace_slug"]
    base = cfg["api_base"]
    url = f"{base}/workspaces/{ws}/projects/{pid}/issues/"
    payload = {"name": title, "description_html": f"<p>{description}</p>", "priority": priority}
    result = _post(url, payload)
    return f"Issue créée : [{result.get('sequence_id','?')}] {result.get('name','')} (id: {result.get('id','')})"


@mcp.tool()
def update_issue_status(project_key: str, issue_id: str, state_name: str) -> str:
    """Met à jour le statut d'une issue. state_name: nom exact de l'état dans Plane (ex: 'In Progress')."""
    cfg = _cfg()
    pid = cfg["projects"][project_key]["plane_project_id"]
    ws = cfg["workspace_slug"]
    base = cfg["api_base"]
    # Récupérer les états disponibles
    states = _get(f"{base}/workspaces/{ws}/projects/{pid}/states/")
    state_list = states.get("results", states) if isinstance(states, dict) else states
    state_id = next((s["id"] for s in state_list if s["name"].lower() == state_name.lower()), None)
    if not state_id:
        names = [s["name"] for s in state_list]
        return f"État '{state_name}' non trouvé. Disponibles : {names}"
    result = _patch(f"{base}/workspaces/{ws}/projects/{pid}/issues/{issue_id}/", {"state": state_id})
    return f"Issue {issue_id} → {state_name}"


@mcp.tool()
def list_cycles(project_key: str) -> str:
    """Liste les cycles d'un projet Plane."""
    cfg = _cfg()
    pid = cfg["projects"][project_key]["plane_project_id"]
    ws = cfg["workspace_slug"]
    base = cfg["api_base"]
    data = _get(f"{base}/workspaces/{ws}/projects/{pid}/cycles/")
    results = data.get("results", data) if isinstance(data, dict) else data
    if not results:
        return "Aucun cycle."
    lines = []
    for c in results:
        lines.append(f"{c.get('name','')} | status: {c.get('status','')} | {c.get('start_date','')} → {c.get('end_date','')} | id: {c.get('id','')}")
    return "\n".join(lines)


if __name__ == "__main__":
    mcp.run()
