#!/usr/bin/env python3
"""Serveur local PKA dashboards.

Expose les dashboards HTML sur 127.0.0.1 et lance Dobby via Terminal
uniquement pour les modeles autorises.
"""

from __future__ import annotations

import argparse
import secrets
import datetime as dt
import json
import mimetypes
import os
import re
import sqlite3
import subprocess
import sys
import tempfile
import uuid
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlencode, urlparse

SCRIPT_DIR = Path(__file__).resolve().parent
PKA_DIR = SCRIPT_DIR.parents[0]
if str(PKA_DIR) not in sys.path:
    sys.path.insert(0, str(PKA_DIR))

from scripts import pka_kanban_schema
from scripts import pka_kanban_service
from scripts import pka_plane_adapter

JCH_INBOX_DIR = PKA_DIR / "JCH_Inbox"
DASHBOARD_DIR = PKA_DIR / "JCH_Inbox" / "01_DASHBOARDS"
TEAM_DB = PKA_DIR / "TEAM" / "team.db"
TEAM_INBOX_DIR = PKA_DIR / "TEAM_Inbox"
WIKI_DIR = PKA_DIR / "wiki"
DASHBOARD_TOKEN_FILE = Path(os.environ.get(
    "PKA_DASHBOARD_TOKEN_FILE",
    str(Path.home() / ".codex" / "memories" / "pka-jch" / "dashboard_token.txt"),
))

REALTIME_MODEL = os.environ.get("PKA_REALTIME_MODEL", "gpt-realtime-2")
REALTIME_VOICES = {
    "alloy",
    "ash",
    "ballad",
    "coral",
    "echo",
    "sage",
    "shimmer",
    "verse",
    "marin",
    "cedar",
}
REALTIME_DEFAULT_VOICE = os.environ.get("PKA_REALTIME_VOICE", "marin")

MODELS = {
    "claude": {
        "label": "Claude Code",
        "command": ["./dobby.sh", "--model", "claude"],
        "bg": "#30200f",
        "fg": "#f8f5f0",
        "cursor": "#c17f3a",
    },
    "codex": {
        "label": "Codex CLI",
        "command": ["./dobby.sh", "--model", "codex"],
        "bg": "#131520",
        "fg": "#f8f5f0",
        "cursor": "#4a5568",
    },
    "gemini": {
        "label": "Gemini CLI",
        "command": ["./dobby.sh", "--model", "gemini"],
        "bg": "#0f1710",
        "fg": "#f8f5f0",
        "cursor": "#3d5a3e",
    },
    "deepseek": {
        "label": "DeepSeek Chat",
        "command": ["./dobby.sh", "--model", "deepseek"],
        "bg": "#30100b",
        "fg": "#f8f5f0",
        "cursor": "#c0392b",
    },
    "deepseek-r1": {
        "label": "DeepSeek R1",
        "command": ["./dobby.sh", "--model", "deepseek-r1"],
        "bg": "#0b0908",
        "fg": "#f8f5f0",
        "cursor": "#2a2420",
    },
    "gemma4": {
        "label": "Gemma 4",
        "command": ["./dobby.sh", "--model", "gemma4"],
        "bg": "#1b1918",
        "fg": "#f8f5f0",
        "cursor": "#6b6560",
    },
    "qwen3": {
        "label": "Qwen 3.6",
        "command": ["./dobby.sh", "--model", "qwen3"],
        "bg": "#3a3937",
        "fg": "#0d0b09",
        "cursor": "#e8e2da",
    },
}


def terminal_command(model: str) -> str:
    data = MODELS[model]
    command = " ".join(MODELS[model]["command"])
    title = f"Dobby - {data['label']}"
    palette = (
        f"printf '\\033]0;{title}\\007'; "
        f"printf '\\033]10;{data['fg']}\\007'; "
        f"printf '\\033]11;{data['bg']}\\007'; "
        f"printf '\\033]12;{data['cursor']}\\007'; "
    )
    return f"{palette}cd {quote_for_shell(PKA_DIR)} && {command}"


def quote_for_shell(path: Path) -> str:
    return "'" + str(path).replace("'", "'\\''") + "'"


def launch_terminal(model: str) -> None:
    script = f"""
tell application "Terminal"
  activate
  do script {json.dumps(terminal_command(model))}
end tell
"""
    subprocess.run(["osascript", "-e", script], check=True)


def launch_save_prompt() -> None:
    command = f"cd {quote_for_shell(PKA_DIR)} && ./scripts/pka_save.py --interactive"
    script = f"""
tell application "Terminal"
  activate
  do script {json.dumps(command)}
end tell
"""
    subprocess.run(["osascript", "-e", script], check=True)


def active_team_count() -> int:
    with sqlite3.connect(TEAM_DB) as conn:
        row = conn.execute("select count(*) from members where status='active'").fetchone()
    return int(row[0])


def directory_items(path: Path, limit: int | None = None) -> list[dict]:
    if not path.exists():
        return []
    items = sorted(path.iterdir(), key=lambda item: item.stat().st_mtime, reverse=True)
    if limit is not None:
        items = items[:limit]
    return [
        {
            "name": item.name,
            "path": str(item.relative_to(JCH_INBOX_DIR)) if item.is_relative_to(JCH_INBOX_DIR) else str(item),
            "type": "directory" if item.is_dir() else "file",
            "modified": item.stat().st_mtime,
        }
        for item in items
        if item.name != ".DS_Store"
    ]


def latest_daily_note() -> str | None:
    daily = PKA_DIR / "wiki" / "Daily"
    notes = [item for item in daily.rglob("*.md") if item.is_file()]
    if not notes:
        return None
    return max(notes, key=lambda item: item.stat().st_mtime).name


def kanban_snapshot() -> dict:
    schema = pka_kanban_schema.load_schema()
    empty_summary = {
        "totals": {status: 0 for status in schema["statuses"]},
        "blocked": 0,
        "awaiting_jch": 0,
        "by_project": {},
    }

    try:
        config = pka_plane_adapter.load_config()
        cards = []
        for project_key in sorted(config["projects"]):
            cards.extend(pka_plane_adapter.fetch_project_issues(project_key))
        return pka_kanban_service.build_summary(cards)
    except Exception as exc:
        empty_summary["error"] = str(exc)
        return empty_summary


def dashboard_health() -> dict:
    inbox = [item for item in (JCH_INBOX_DIR / "00_INBOX").iterdir() if item.name != ".DS_Store"] if (JCH_INBOX_DIR / "00_INBOX").exists() else []
    projects = [item for item in (JCH_INBOX_DIR / "03_PROJECTS").iterdir() if item.is_dir()] if (JCH_INBOX_DIR / "03_PROJECTS").exists() else []
    latest = directory_items(PKA_DIR / "TEAM_Inbox", limit=1)
    kanban = kanban_snapshot()
    return {
        "ok": True,
        "teamActive": active_team_count(),
        "inboxPending": len(inbox),
        "projectsActive": len(projects),
        "latestDaily": latest_daily_note(),
        "latestDeliverable": latest[0]["name"] if latest else None,
        "kanban": {
            "blocked": kanban["blocked"],
            "awaitingJch": kanban["awaiting_jch"],
            "totals": kanban["totals"],
        },
    }


def slugify(value: str, fallback: str = "dobby-live") -> str:
    slug = re.sub(r"[^a-zA-Z0-9_-]+", "-", value.lower()).strip("-")
    return slug[:80] or fallback


def dashboard_token() -> str:
    env_token = os.environ.get("PKA_DASHBOARD_TOKEN")
    if env_token:
        return env_token.strip()
    DASHBOARD_TOKEN_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not DASHBOARD_TOKEN_FILE.exists():
        DASHBOARD_TOKEN_FILE.write_text(secrets.token_urlsafe(24), encoding="utf-8")
        DASHBOARD_TOKEN_FILE.chmod(0o600)
    return DASHBOARD_TOKEN_FILE.read_text(encoding="utf-8").strip()


def is_loopback_address(address: str) -> bool:
    return address in {"127.0.0.1", "::1", "localhost"} or address.startswith("127.")


def token_from_cookie(cookie_header: str | None) -> str | None:
    if not cookie_header:
        return None
    for part in cookie_header.split(";"):
        name, _, value = part.strip().partition("=")
        if name == "pka_token":
            return value
    return None


def read_openai_api_key() -> str | None:
    env_key = os.environ.get("OPENAI_API_KEY")
    if env_key:
        return env_key.strip()

    for candidate in (
        Path.home() / ".config" / "pka-jch" / "openai_key.txt",
        Path(__file__).resolve().parent / "telegram-bot" / ".env",
    ):
        if not candidate.is_file():
            continue
        if candidate.name == ".env":
            for line in candidate.read_text(encoding="utf-8").splitlines():
                if line.startswith("OPENAI_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")
        else:
            return candidate.read_text(encoding="utf-8").strip()
    return None


def read_env_file_value(path: Path, key: str) -> str | None:
    if not path.is_file():
        return None
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        clean = line.strip()
        if not clean or clean.startswith("#") or "=" not in clean:
            continue
        name, value = clean.split("=", 1)
        if name.strip() == key:
            return value.strip().strip('"').strip("'")
    return None


def read_secret_value(env_name: str, file_candidates: tuple[Path, ...] = ()) -> str | None:
    env_value = os.environ.get(env_name)
    if env_value:
        return env_value.strip()

    for candidate in file_candidates:
        if candidate.is_file():
            if candidate.name == ".env":
                value = read_env_file_value(candidate, env_name)
                if value:
                    return value
            else:
                return candidate.read_text(encoding="utf-8", errors="replace").strip()
    return None


def json_request(url: str, headers: dict[str, str], timeout: int = 12) -> tuple[int, dict | None, str | None]:
    command = [
        "curl",
        "--silent",
        "--show-error",
        "--write-out",
        "\n%{http_code}",
        url,
    ]
    for name, value in headers.items():
        command.extend(["-H", f"{name}: {value}"])
    try:
        result = subprocess.run(command, check=False, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return 0, None, "timeout"

    if result.returncode != 0:
        return 0, None, result.stderr.strip()[:240] or "curl failed"

    body, _, status_text = result.stdout.rpartition("\n")
    try:
        status = int(status_text)
    except ValueError:
        return 0, None, "invalid HTTP response"

    if 200 <= status < 300:
        try:
            return status, json.loads(body) if body else {}, None
        except json.JSONDecodeError as exc:
            return status, None, f"invalid JSON: {exc}"

    try:
        payload = json.loads(body)
        raw_error = payload.get("error") if isinstance(payload, dict) else None
        if isinstance(raw_error, dict):
            message = raw_error.get("message") or payload.get("message") or body
        elif isinstance(raw_error, str):
            message = raw_error
        elif isinstance(payload, dict):
            message = payload.get("message") or body
        else:
            message = body
    except json.JSONDecodeError:
        message = body
    return status, None, (message or f"HTTP {status}")[:240]


def month_window_unix() -> tuple[int, int]:
    now = dt.datetime.now(dt.timezone.utc)
    start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    return int(start.timestamp()), int(now.timestamp())


def sum_openai_costs(payload: dict) -> tuple[float, str]:
    total = 0.0
    currency = "usd"
    for bucket in payload.get("data", []):
        for item in bucket.get("results", []):
            amount = item.get("amount") or {}
            if isinstance(amount, dict):
                value = amount.get("value")
                currency = amount.get("currency", currency)
                try:
                    total += float(value or 0)
                except (TypeError, ValueError):
                    pass
    return total, currency.upper()


def sum_anthropic_costs(payload: dict) -> tuple[float | None, str]:
    total = 0.0
    found = False
    currency = "USD"

    def walk(value: object) -> None:
        nonlocal total, found, currency
        if isinstance(value, dict):
            if isinstance(value.get("currency"), str):
                currency = value["currency"].upper()
            for key in ("amount", "cost", "cost_usd", "total_cost"):
                raw = value.get(key)
                if isinstance(raw, (int, float, str)):
                    try:
                        total += float(raw)
                        found = True
                    except ValueError:
                        pass
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(payload)
    return (total if found else None), currency


def provider_balance_status() -> dict:
    env_path = Path(__file__).resolve().parent / "telegram-bot" / ".env"
    config_dir = Path.home() / ".config" / "pka-jch"
    start_time, end_time = month_window_unix()
    today = dt.datetime.now(dt.timezone.utc).date()
    month_start = today.replace(day=1).isoformat()
    tomorrow = (today + dt.timedelta(days=1)).isoformat()

    providers: list[dict] = []

    deepseek_key = read_secret_value("DEEPSEEK_API_KEY", (env_path,))
    deepseek = {
        "id": "deepseek",
        "label": "DeepSeek",
        "kind": "Solde disponible",
        "configured": bool(deepseek_key),
        "status": "missing",
        "value": "clé absente",
        "detail": "DEEPSEEK_API_KEY non configurée",
        "console_url": "https://platform.deepseek.com/usage",
        "topup_url": "https://platform.deepseek.com/top_up",
    }
    if deepseek_key:
        status, payload, message = json_request(
            "https://api.deepseek.com/user/balance",
            {"Authorization": f"Bearer {deepseek_key}", "Accept": "application/json"},
        )
        if status == 200 and payload:
            infos = payload.get("balance_infos") or []
            amounts = [
                f"{info.get('total_balance')} {info.get('currency')}"
                for info in infos
                if info.get("total_balance") is not None and info.get("currency")
            ]
            deepseek.update({
                "status": "ok" if payload.get("is_available", True) else "warning",
                "value": " · ".join(amounts) or "solde lu",
                "detail": "appel API possible" if payload.get("is_available", True) else "solde insuffisant pour appels API",
            })
        else:
            deepseek.update({"status": "error", "value": "erreur", "detail": message or f"HTTP {status}"})
    providers.append(deepseek)

    openai_key = read_openai_api_key()
    openai = {
        "id": "openai",
        "label": "OpenAI",
        "kind": "Dépense mois",
        "configured": bool(openai_key),
        "status": "missing",
        "value": "clé absente",
        "detail": "OPENAI_API_KEY non configurée",
        "console_url": "https://platform.openai.com/usage",
        "topup_url": "https://platform.openai.com/settings/organization/billing/overview",
    }
    if openai_key:
        query = urlencode({"start_time": start_time, "end_time": end_time, "limit": 31})
        status, payload, message = json_request(
            f"https://api.openai.com/v1/organization/costs?{query}",
            {"Authorization": f"Bearer {openai_key}", "Accept": "application/json"},
        )
        if status == 200 and payload:
            total, currency = sum_openai_costs(payload)
            openai.update({
                "status": "ok",
                "value": f"{total:.2f} {currency}",
                "detail": "coût API depuis le début du mois; pas un solde disponible",
            })
        elif status in {401, 403}:
            openai.update({
                "status": "manual",
                "value": "voir console",
                "detail": "Clé sans droits admin — solde réel disponible sur la console",
            })
        else:
            openai.update({
                "status": "manual",
                "value": "voir console",
                "detail": message or f"HTTP {status} — contrôle manuel requis",
            })
    providers.append(openai)

    anthropic_key = read_secret_value(
        "ANTHROPIC_ADMIN_KEY",
        (config_dir / "anthropic_admin_key.txt", env_path),
    )
    if not anthropic_key:
        anthropic_key = read_secret_value(
            "ANTHROPIC_API_KEY",
            (config_dir / "anthropic_key.txt", env_path),
        )
    anthropic = {
        "id": "anthropic",
        "label": "Anthropic",
        "kind": "Coût mois",
        "configured": bool(anthropic_key),
        "status": "missing",
        "value": "clé absente",
        "detail": "clé Anthropic non configurée",
        "console_url": "https://console.anthropic.com/settings/billing",
        "topup_url": "https://console.anthropic.com/settings/plans",
    }
    if anthropic_key:
        query = urlencode({"starting_at": month_start, "ending_at": tomorrow})
        status, payload, message = json_request(
            f"https://api.anthropic.com/v1/organizations/cost_report?{query}",
            {
                "x-api-key": anthropic_key,
                "anthropic-version": "2023-06-01",
                "Accept": "application/json",
            },
        )
        if status == 200 and payload:
            total, currency = sum_anthropic_costs(payload)
            anthropic.update({
                "status": "ok",
                "value": f"{total:.2f} {currency}" if total is not None else "coût lu",
                "detail": "API Admin Usage/Cost; solde exact → voir console",
            })
        elif status in {401, 403, 404}:
            anthropic.update({
                "status": "manual",
                "value": "voir console",
                "detail": "Pas d'API de solde individuel — contrôle manuel requis",
            })
        else:
            anthropic.update({
                "status": "manual",
                "value": "voir console",
                "detail": message or f"HTTP {status} — contrôle manuel requis",
            })
    providers.append(anthropic)

    google_key = read_secret_value("GOOGLE_API_KEY", (config_dir / "google_key.txt", env_path))
    providers.append({
        "id": "google",
        "label": "Google Gemini",
        "kind": "Facturation Cloud",
        "configured": bool(google_key),
        "status": "manual" if google_key else "missing",
        "value": "voir console" if google_key else "clé absente",
        "detail": "Pas d'API de solde — contrôle manuel via Google Cloud Billing",
        "console_url": "https://console.cloud.google.com/billing",
        "topup_url": "https://console.cloud.google.com/billing",
    })

    providers.append({
        "id": "ollama",
        "label": "Ollama local",
        "kind": "Local",
        "configured": True,
        "status": "local",
        "value": "0 EUR",
        "detail": "pas de fournisseur payant; coût machine/énergie seulement",
    })

    return {
        "ok": True,
        "generatedAt": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "providers": providers,
        "sources": {
            "deepseek": "https://api-docs.deepseek.com/api/get-user-balance/",
            "openai": "https://platform.openai.com/docs/api-reference/usage/costs",
            "anthropic": "https://docs.anthropic.com/en/api/usage-cost-api",
        },
    }


def realtime_tools() -> list[dict]:
    return [
        {
            "type": "function",
            "name": "pka_status",
            "description": "Retourne l'etat du systeme PKA: equipe, inbox, projets, derniere note et dernier livrable.",
            "parameters": {"type": "object", "properties": {}, "additionalProperties": False},
        },
        {
            "type": "function",
            "name": "read_inbox",
            "description": "Liste les fichiers en attente dans JCH_Inbox/00_INBOX.",
            "parameters": {"type": "object", "properties": {}, "additionalProperties": False},
        },
        {
            "type": "function",
            "name": "search_wiki",
            "description": "Cherche un terme dans les fichiers Markdown du wiki PKA.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Terme a chercher."},
                    "limit": {"type": "integer", "minimum": 1, "maximum": 8, "default": 5},
                },
                "required": ["query"],
                "additionalProperties": False,
            },
        },
        {
            "type": "function",
            "name": "create_daily_note",
            "description": "Ajoute une note dans la daily note du jour. Non destructif: ajoute a la fin du fichier.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Titre court de la note."},
                    "content": {"type": "string", "description": "Contenu a sauvegarder."},
                },
                "required": ["title", "content"],
                "additionalProperties": False,
            },
        },
        {
            "type": "function",
            "name": "save_team_inbox",
            "description": "Sauve un livrable Markdown dans TEAM_Inbox.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "Titre du livrable."},
                    "content": {"type": "string", "description": "Contenu Markdown du livrable."},
                },
                "required": ["title", "content"],
                "additionalProperties": False,
            },
        },
        {
            "type": "function",
            "name": "prepare_model_brief",
            "description": "Prepare un brief Markdown pour un modele cible externe comme Claude, Gemini ou Codex. Ne lance pas le modele.",
            "parameters": {
                "type": "object",
                "properties": {
                    "target": {"type": "string", "description": "Modele ou outil cible: Claude, Gemini, Codex, OpenAI, Auto."},
                    "task": {"type": "string", "description": "Tache a confier."},
                    "context": {"type": "string", "description": "Contexte utile pour le modele cible."},
                },
                "required": ["target", "task"],
                "additionalProperties": False,
            },
        },
    ]


def realtime_instructions(model_target: str) -> str:
    return f"""Tu es Dobby, orchestrateur PKA de JCH. Reponds en francais par defaut, de facon courte et naturelle a l'oral.
Tu es l'interface vocale transversale du systeme. Modele cible demande par JCH: {model_target}.
Si une demande exige une action PKA, utilise les tools disponibles. Les tools sont limites a des actions non destructives.
Pour Claude, Gemini, Codex ou un autre moteur: explique que tu peux preparer et sauvegarder le brief; ne pretends pas avoir lance le modele sauf si un tool le confirme.
Demande confirmation avant toute action sensible. Resume les actions sauvegardees avec le chemin du fichier quand le tool le retourne."""


def build_realtime_session(voice: str, model_target: str) -> dict:
    selected_voice = voice if voice in REALTIME_VOICES else REALTIME_DEFAULT_VOICE
    if selected_voice not in REALTIME_VOICES:
        selected_voice = "marin"
    return {
        "type": "realtime",
        "model": REALTIME_MODEL,
        "instructions": realtime_instructions(model_target),
        "audio": {
            "input": {
                "turn_detection": {
                    "type": "server_vad",
                    "create_response": True,
                    "interrupt_response": True,
                }
            },
            "output": {"voice": selected_voice},
        },
        "tools": realtime_tools(),
        "tool_choice": "auto",
    }


def post_realtime_call(sdp: str, voice: str, model_target: str) -> tuple[int, str, str]:
    api_key = read_openai_api_key()
    if not api_key:
        return 500, "text/plain; charset=utf-8", "OPENAI_API_KEY introuvable cote serveur."

    session = json.dumps(build_realtime_session(voice, model_target), ensure_ascii=False)

    try:
        with tempfile.TemporaryDirectory(prefix="pka-realtime-") as tmpdir:
            sdp_path = Path(tmpdir) / "offer.sdp"
            session_path = Path(tmpdir) / "session.json"
            sdp_path.write_text(sdp, encoding="utf-8")
            session_path.write_text(session, encoding="utf-8")
            command = [
                "curl",
                "--silent",
                "--show-error",
                "--write-out",
                "\n%{http_code}\n%{content_type}",
                "https://api.openai.com/v1/realtime/calls",
                "-H",
                f"Authorization: Bearer {api_key}",
                "-F",
                f"sdp=<{sdp_path};type=application/sdp",
                "-F",
                f"session=<{session_path};type=application/json",
            ]
            result = subprocess.run(
                command,
                check=False,
                capture_output=True,
                text=True,
                timeout=45,
            )
    except subprocess.TimeoutExpired:
        return 504, "text/plain; charset=utf-8", "Timeout OpenAI Realtime."

    if result.returncode != 0:
        return 502, "text/plain; charset=utf-8", f"Connexion OpenAI impossible: {result.stderr.strip()}"

    body_and_meta = result.stdout.rsplit("\n", 2)
    if len(body_and_meta) != 3:
        return 502, "text/plain; charset=utf-8", result.stdout or "Reponse OpenAI illisible."

    response_body, status_text, content_type = body_and_meta
    try:
        status = int(status_text)
    except ValueError:
        status = 502

    return status, content_type or "application/sdp", response_body


def search_wiki(query: str, limit: int = 5) -> dict:
    cleaned_query = query.strip().lower()
    if not cleaned_query:
        return {"ok": False, "error": "query manquant"}
    limit = max(1, min(int(limit or 5), 8))
    results = []
    for path in sorted(WIKI_DIR.rglob("*.md")):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        lowered = text.lower()
        index = lowered.find(cleaned_query)
        if index < 0:
            continue
        start = max(0, index - 140)
        end = min(len(text), index + len(cleaned_query) + 220)
        results.append({
            "path": str(path.relative_to(PKA_DIR)),
            "excerpt": " ".join(text[start:end].split()),
        })
        if len(results) >= limit:
            break
    return {"ok": True, "query": query, "results": results}


def append_daily_note(title: str, content: str) -> dict:
    today = dt.date.today()
    directory = WIKI_DIR / "Daily" / f"{today:%Y}" / f"{today:%m}"
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / f"{today:%Y-%m-%d}-dobby-live.md"
    timestamp = dt.datetime.now().strftime("%H:%M")
    if not path.exists():
        path.write_text(f"# {today:%Y-%m-%d} — Dobby Live\n\n", encoding="utf-8")
    with path.open("a", encoding="utf-8") as handle:
        handle.write(f"## {timestamp} — {title.strip() or 'Note'}\n\n{content.strip()}\n\n")
    return {"ok": True, "path": str(path.relative_to(PKA_DIR))}


def save_team_inbox(title: str, content: str) -> dict:
    TEAM_INBOX_DIR.mkdir(parents=True, exist_ok=True)
    today = dt.date.today().strftime("%Y-%m-%d")
    path = TEAM_INBOX_DIR / f"{today}_dobby_live_{slugify(title)}.md"
    header = f"# {title.strip() or 'Dobby Live'}\n\n_Source : Dobby Live / Realtime 2_\n\n"
    path.write_text(header + content.strip() + "\n", encoding="utf-8")
    return {"ok": True, "path": str(path.relative_to(PKA_DIR))}


def prepare_model_brief(target: str, task: str, context: str = "") -> dict:
    title = f"Brief {target.strip() or 'Auto'} — {task.strip()[:60] or 'Tache'}"
    content = (
        f"**Modele cible :** {target.strip() or 'Auto'}\n\n"
        f"**Tache :** {task.strip()}\n\n"
        f"**Contexte :**\n\n{context.strip() or 'A completer depuis la session Dobby Live.'}\n\n"
        "**Statut :** prepare par Dobby Live, execution externe non lancee.\n"
    )
    return save_team_inbox(title, content)


def run_live_tool(name: str, arguments: dict) -> dict:
    if name == "pka_status":
        return {"ok": True, "status": dashboard_health()}
    if name == "read_inbox":
        return {"ok": True, "items": directory_items(JCH_INBOX_DIR / "00_INBOX")}
    if name == "search_wiki":
        return search_wiki(str(arguments.get("query", "")), int(arguments.get("limit", 5)))
    if name == "create_daily_note":
        return append_daily_note(str(arguments.get("title", "Note Dobby Live")), str(arguments.get("content", "")))
    if name == "save_team_inbox":
        return save_team_inbox(str(arguments.get("title", "Dobby Live")), str(arguments.get("content", "")))
    if name == "prepare_model_brief":
        return prepare_model_brief(
            str(arguments.get("target", "Auto")),
            str(arguments.get("task", "")),
            str(arguments.get("context", "")),
        )
    return {"ok": False, "error": f"Tool non autorise: {name}"}


class DashboardHandler(BaseHTTPRequestHandler):
    server_version = "PKADashboard/1.0"

    def log_message(self, fmt: str, *args: object) -> None:
        print(f"{self.address_string()} - {fmt % args}")

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path

        query_token = parse_qs(parsed.query).get("token", [""])[0]
        if query_token and secrets.compare_digest(query_token, dashboard_token()):
            clean_location = path or "/hub.html"
            self.send_response(HTTPStatus.FOUND)
            self.send_header("Location", clean_location)
            self.send_header("Set-Cookie", f"pka_token={query_token}; Path=/; HttpOnly; SameSite=Lax; Max-Age=2592000")
            self.end_headers()
            return

        if path == "/unlock":
            self.send_unlock_page()
            return

        if path == "/api/auth":
            self.send_json({"ok": self.is_authorized_request(), "local": self.is_local_request()})
            return

        if not self.is_authorized_request():
            self.redirect("/unlock")
            return

        if path == "/":
            self.redirect("/hub.html")
            return

        if path == "/modeles":
            self.redirect("/modeles.html")
            return

        if path == "/organigramme":
            self.redirect("/organigramme.html")
            return

        if path == "/api/models":
            self.send_json({
                name: {
                    "label": data["label"],
                    "command": " ".join(data["command"]),
                    "bg": data["bg"],
                    "fg": data["fg"],
                    "cursor": data["cursor"],
                }
                for name, data in MODELS.items()
            })
            return

        if path == "/api/health":
            self.send_json(dashboard_health())
            return

        if path == "/api/kanban/summary":
            self.send_json(kanban_snapshot())
            return

        if path == "/api/provider-balances":
            self.send_json(provider_balance_status())
            return

        if path == "/api/projects":
            self.send_json({"items": directory_items(JCH_INBOX_DIR / "03_PROJECTS")})
            return

        if path == "/api/inbox":
            self.send_json({"items": directory_items(JCH_INBOX_DIR / "00_INBOX")})
            return

        if path == "/api/latest":
            self.send_json({"items": directory_items(PKA_DIR / "TEAM_Inbox", limit=8)})
            return

        if path == "/api/live/config":
            self.send_json({
                "ok": True,
                "model": REALTIME_MODEL,
                "voices": sorted(REALTIME_VOICES),
                "defaultVoice": REALTIME_DEFAULT_VOICE if REALTIME_DEFAULT_VOICE in REALTIME_VOICES else "marin",
                "tools": [tool["name"] for tool in realtime_tools()],
            })
            return

        self.serve_static(path)

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        parts = [part for part in parsed.path.split("/") if part]

        if parsed.path == "/unlock":
            body = self.read_request_body().decode("utf-8", errors="replace")
            params = parse_qs(body)
            token = params.get("token", [""])[0].strip()
            if secrets.compare_digest(token, dashboard_token()):
                self.send_response(HTTPStatus.FOUND)
                self.send_header("Location", "/dobby-live.html")
                self.send_header("Set-Cookie", f"pka_token={token}; Path=/; HttpOnly; SameSite=Lax; Max-Age=2592000")
                self.end_headers()
            else:
                self.send_unlock_page("Token invalide.")
            return

        if not self.is_authorized_request():
            self.send_json({"ok": False, "error": "Acces PKA verrouille"}, HTTPStatus.UNAUTHORIZED)
            return

        if parsed.path == "/api/realtime/call":
            query = parse_qs(parsed.query)
            voice = query.get("voice", [REALTIME_DEFAULT_VOICE])[0]
            model_target = query.get("target", ["Auto"])[0][:40]
            sdp = self.read_request_body().decode("utf-8", errors="replace")
            status, content_type, response_body = post_realtime_call(sdp, voice, model_target)
            self.send_bytes(response_body.encode("utf-8"), HTTPStatus(status), content_type)
            return

        if parsed.path == "/api/live/tool":
            if self.headers.get("X-PKA-Dashboard") != "1":
                self.send_json({"ok": False, "error": "Requete dashboard invalide"}, HTTPStatus.FORBIDDEN)
                return
            try:
                payload = json.loads(self.read_request_body().decode("utf-8"))
            except json.JSONDecodeError:
                self.send_json({"ok": False, "error": "JSON invalide"}, HTTPStatus.BAD_REQUEST)
                return
            result = run_live_tool(str(payload.get("name", "")), payload.get("arguments") or {})
            self.send_json(result)
            return

        if len(parts) == 2 and parts[0] == "launch":
            if self.headers.get("X-PKA-Dashboard") != "1":
                self.send_json({"ok": False, "error": "Requete dashboard invalide"}, HTTPStatus.FORBIDDEN)
                return

            model = parts[1]
            if model not in MODELS:
                self.send_json({"ok": False, "error": "Modele non autorise"}, HTTPStatus.BAD_REQUEST)
                return

            try:
                launch_terminal(model)
            except subprocess.CalledProcessError as exc:
                self.send_json(
                    {"ok": False, "error": f"Terminal non lance: {exc}"},
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                )
                return

            self.send_json({"ok": True, "model": model, "label": MODELS[model]["label"]})
            return

        if len(parts) == 1 and parts[0] == "save":
            if self.headers.get("X-PKA-Dashboard") != "1":
                self.send_json({"ok": False, "error": "Requete dashboard invalide"}, HTTPStatus.FORBIDDEN)
                return
            try:
                launch_save_prompt()
            except subprocess.CalledProcessError as exc:
                self.send_json(
                    {"ok": False, "error": f"Sauvegarde non lancee: {exc}"},
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                )
                return
            self.send_json({"ok": True})
            return

        self.send_json({"ok": False, "error": "Route inconnue"}, HTTPStatus.NOT_FOUND)

    def is_local_request(self) -> bool:
        host = self.client_address[0] if self.client_address else ""
        return is_loopback_address(host)

    def is_authorized_request(self) -> bool:
        if self.is_local_request():
            return True
        parsed = urlparse(self.path)
        query_token = parse_qs(parsed.query).get("token", [""])[0]
        cookie_token = token_from_cookie(self.headers.get("Cookie")) or ""
        expected = dashboard_token()
        return secrets.compare_digest(query_token, expected) or secrets.compare_digest(cookie_token, expected)

    def send_unlock_page(self, error: str = "") -> None:
        error_html = f"<div class='error'>{error}</div>" if error else ""
        html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PKA · Acces</title>
<style>
:root {{ --pka-ivoire: #f8f5f0; --pka-text: #0d0b09; --pka-muted: #6b6560; --pka-line: #e7ded3; --pka-shadow: 0 8px 28px rgba(42, 36, 32, 0.06); --pka-ocre: #c17f3a; --pka-brun: #2a2420; --pka-rouge: #c0392b; }}
body {{ margin: 0; min-height: 100vh; display: grid; place-items: center; font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: var(--pka-ivoire); color: var(--pka-text); }}
main {{ width: min(420px, calc(100vw - 44px)); background: white; border: 1px solid var(--pka-line); box-shadow: var(--pka-shadow); padding: 24px; border-left: 4px solid var(--pka-ocre); }}
h1 {{ margin: 0 0 8px; font-size: 24px; }}
p {{ margin: 0 0 18px; color: var(--pka-muted); font-size: 13px; line-height: 1.5; }}
label {{ display: block; color: var(--pka-muted); font-size: 10px; letter-spacing: 0.1em; text-transform: uppercase; margin-bottom: 7px; }}
input {{ width: 100%; min-height: 42px; border: 1px solid var(--pka-line); padding: 0 12px; font: inherit; }}
button {{ width: 100%; min-height: 42px; margin-top: 12px; border: 0; border-radius: 6px; background: var(--pka-brun); color: white; font: inherit; font-weight: 700; }}
.error {{ border-left: 3px solid var(--pka-rouge); background: #fbfaf8; color: var(--pka-rouge); padding: 10px 12px; margin-bottom: 14px; font-size: 13px; }}
</style>
</head>
<body>
<main>
<h1>Dobby Live</h1>
<p>Acces mobile protege. Entre le token du dashboard PKA pour deverrouiller cette session.</p>
{error_html}
<form method="POST" action="/unlock">
<label for="token">Token</label>
<input id="token" name="token" type="password" autocomplete="current-password" autofocus>
<button type="submit">Deverrouiller</button>
</form>
</main>
</body>
</html>"""
        self.send_bytes(html.encode("utf-8"), HTTPStatus.OK, "text/html; charset=utf-8")

    def serve_static(self, request_path: str) -> None:
        relative = unquote(request_path.lstrip("/"))
        if not relative:
            relative = "01_DASHBOARDS/hub.html"

        if relative.startswith("assets/"):
            relative = f"01_DASHBOARDS/{relative}"
        elif "/" not in relative and (JCH_INBOX_DIR / relative).is_file():
            relative = relative
        elif "/" not in relative:
            relative = f"01_DASHBOARDS/{relative}"

        candidate = (JCH_INBOX_DIR / relative).resolve()
        try:
            candidate.relative_to(JCH_INBOX_DIR.resolve())
        except ValueError:
            self.send_error(HTTPStatus.FORBIDDEN)
            return

        if candidate.is_dir():
            self.send_directory_index(candidate)
            return

        if not candidate.is_file():
            self.send_error(HTTPStatus.NOT_FOUND)
            return

        content_type = mimetypes.guess_type(candidate.name)[0] or "application/octet-stream"
        data = candidate.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def send_directory_index(self, directory: Path) -> None:
        entries = [item for item in sorted(directory.iterdir(), key=lambda item: (not item.is_dir(), item.name.lower())) if item.name != ".DS_Store"]
        relative = directory.relative_to(JCH_INBOX_DIR)
        rows = []
        for item in entries:
            href = "/" + str(item.relative_to(JCH_INBOX_DIR))
            if item.is_dir():
                href += "/"
            rows.append(
                "<a class='row' href='{}'><span>{}</span><small>{}</small></a>".format(
                    href.replace("'", "%27"),
                    item.name,
                    "dossier" if item.is_dir() else "fichier",
                )
            )
        body = "\n".join(rows) or "<div class='empty'>Aucun fichier.</div>"
        html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PKA · {relative}</title>
<link rel="stylesheet" href="/01_DASHBOARDS/assets/pka-theme.css">
<style>
body {{ font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; margin: 0; }}
main {{ max-width: 980px; margin: 0 auto; padding: 42px 48px 80px; }}
h1 {{ font-size: 24px; margin: 0 0 8px; }}
.path {{ color: var(--pka-muted); font-size: 13px; margin-bottom: 26px; }}
.row {{ display: flex; justify-content: space-between; gap: 20px; padding: 14px 16px; background: white; border: 1px solid var(--pka-line); border-left: 4px solid var(--pka-sable); color: var(--pka-text); text-decoration: none; margin-bottom: 8px; }}
.row:hover {{ border-left-color: var(--pka-ocre); }}
small {{ color: var(--pka-muted); text-transform: uppercase; letter-spacing: 0.08em; font-size: 10px; }}
.empty {{ background: white; border: 1px solid var(--pka-line); padding: 18px; color: var(--pka-muted); }}
.back {{ display: inline-block; margin-bottom: 24px; color: var(--pka-muted); text-decoration: none; }}
</style>
</head>
<body>
<main>
<a class="back" href="/hub.html">Retour au hub</a>
<h1>Index dossier</h1>
<div class="path">{relative}</div>
{body}
</main>
</body>
</html>"""
        data = html.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def redirect(self, location: str) -> None:
        self.send_response(HTTPStatus.FOUND)
        self.send_header("Location", location)
        self.end_headers()

    def send_json(self, payload: dict, status: HTTPStatus = HTTPStatus.OK) -> None:
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_bytes(data, status, "application/json; charset=utf-8")

    def read_request_body(self) -> bytes:
        length = int(self.headers.get("Content-Length", "0"))
        return self.rfile.read(length) if length else b""

    def send_bytes(self, data: bytes, status: HTTPStatus = HTTPStatus.OK, content_type: str = "application/octet-stream") -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)


def main() -> None:
    parser = argparse.ArgumentParser(description="Serveur local dashboards PKA")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=int(os.environ.get("PKA_DASHBOARD_PORT", "8787")))
    args = parser.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), DashboardHandler)
    print(f"PKA dashboards: http://{args.host}:{args.port}")
    print("Ctrl+C pour arreter.")
    server.serve_forever()


if __name__ == "__main__":
    main()
