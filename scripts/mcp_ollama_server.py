#!/usr/bin/env python3
"""MCP server — Ollama PKA. Expose les modèles locaux du M1 (ou local)."""

import json
import os
from urllib import request, error

from mcp.server.fastmcp import FastMCP

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://100.73.212.110:11434")
BASE = f"{OLLAMA_HOST}/api"

mcp = FastMCP("pka-ollama")


def _get(path: str) -> dict:
    url = f"{BASE}{path}"
    req = request.Request(url)
    try:
        with request.urlopen(req, timeout=10) as r:
            return json.loads(r.read())
    except error.URLError as e:
        return {"error": str(e)}


@mcp.tool()
def list_models() -> str:
    """Liste tous les modèles Ollama disponibles (nom, taille, modifié)."""
    data = _get("/tags")
    if "error" in data:
        return f"Erreur: {data['error']}"
    models = data.get("models", [])
    if not models:
        return "Aucun modèle trouvé."
    lines = []
    for m in models:
        size_gb = m.get("size", 0) / 1e9
        lines.append(f"{m['name']} — {size_gb:.1f} Go — modifié {m.get('modified_at','?')}")
    return "\n".join(lines)


@mcp.tool()
def model_info(model: str) -> str:
    """Affiche les détails d'un modèle Ollama (paramètres, famille, template)."""
    data = _get("/show")
    if "error" in data:
        return f"Erreur: {data['error']}"
    # Pour show, il faut POST avec le nom du modèle
    import urllib.request as ur
    body = json.dumps({"name": model}).encode()
    req = ur.Request(f"{BASE}/show", data=body, headers={"Content-Type": "application/json"})
    try:
        with ur.urlopen(req, timeout=10) as r:
            info = json.loads(r.read())
    except error.URLError as e:
        return f"Erreur: {e}"
    lines = []
    for k in ["modelfile", "parameters", "template"]:
        if k in info:
            lines.append(f"--- {k} ---\n{info[k]}")
    return "\n".join(lines) if lines else str(info)


@mcp.tool()
def running_models() -> str:
    """Liste les modèles actuellement chargés en mémoire sur le serveur Ollama."""
    data = _get("/ps")
    if "error" in data:
        return f"Erreur: {data['error']}"
    models = data.get("models", [])
    if not models:
        return "Aucun modèle chargé."
    lines = []
    for m in models:
        size_gb = m.get("size", 0) / 1e9
        lines.append(f"{m['name']} — {size_gb:.1f} Go — {m.get('details',{}).get('family','?')}")
    return "\n".join(lines)


@mcp.tool()
def pull_model(model: str) -> str:
    """Télécharge un modèle Ollama (ex: 'gemma3:12b'). Préviens si le modèle existe déjà."""
    import urllib.request as ur
    body = json.dumps({"name": model}).encode()
    req = ur.Request(f"{BASE}/pull", data=body, headers={"Content-Type": "application/json"})
    try:
        with ur.urlopen(req, timeout=120) as r:
            # Streaming response — on lit la dernière ligne
            last = ""
            for line in r:
                last = line.decode()
            return last
    except error.URLError as e:
        return f"Erreur: {e}"


if __name__ == "__main__":
    mcp.run()
