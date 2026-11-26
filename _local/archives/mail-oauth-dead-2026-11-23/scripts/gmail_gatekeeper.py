#!/usr/bin/env python3
"""
gmail_gatekeeper.py

Flux strict pour la boîte Gmail dédiée à Dobby :
- ne lit que les en-têtes lors du scan
- supprime les emails non autorisés sans ouvrir leur corps
- met en file d'attente les emails autorisés
- n'extrait le contenu et les pièces jointes qu'après accord explicite
"""

from __future__ import annotations

import argparse
import base64
import json
import re
import socket
import sys
from datetime import datetime
from email.utils import parseaddr
from pathlib import Path
from typing import Any

from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


BASE_DIR = Path(__file__).resolve().parent
PKA_DIR = BASE_DIR.parent
CONFIG_PATH = PKA_DIR / "JCH_Inbox" / "99_SYSTEM" / "security" / "gmail_gatekeeper.json"
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.modify",
]


def load_config() -> dict[str, Any]:
    if not CONFIG_PATH.exists():
        raise FileNotFoundError(f"Config manquante: {CONFIG_PATH}")
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def resolve_path(value: str) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute():
        path = PKA_DIR / path
    return path


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: Any) -> None:
    ensure_parent(path)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def get_credentials(config: dict[str, Any]) -> Credentials:
    secrets_dir = Path(config["google_secrets_dir"]).expanduser()
    token_file = secrets_dir / config["token_file"]
    creds_file = secrets_dir / config["credentials_file"]

    creds = None
    if token_file.exists():
        creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)

    if not creds or not creds.valid:
        try:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                raise RefreshError("No valid refresh token available.")
        except RefreshError:
            flow = InstalledAppFlow.from_client_secrets_file(str(creds_file), SCOPES)
            with socket.socket() as sock:
                sock.bind(("127.0.0.1", 0))
                port = int(sock.getsockname()[1])
            creds = flow.run_local_server(
                host="localhost",
                port=port,
                open_browser=True,
                browser="open -a 'Google Chrome' %s",
                authorization_prompt_message="Connexion Google ouverte dans Chrome.",
                prompt="consent",
            )
        token_file.write_text(creds.to_json(), encoding="utf-8")

    return creds


def gmail_service(config: dict[str, Any]):
    creds = get_credentials(config)
    return build("gmail", "v1", credentials=creds)


def parse_sender(from_raw: str) -> tuple[str, str]:
    name, email_addr = parseaddr(from_raw)
    return (name.strip() or email_addr.strip(), email_addr.strip().lower())


def load_state(config: dict[str, Any]) -> dict[str, Any]:
    state_path = resolve_path(config["state_file"])
    return load_json(
        state_path,
        {
            "last_scan_at": None,
            "seen_allowed_ids": [],
            "deleted_unauthorized_ids": [],
            "pending": [],
        },
    )


def save_state(config: dict[str, Any], state: dict[str, Any]) -> None:
    state_path = resolve_path(config["state_file"])
    save_json(state_path, state)


def header_for_message(service, msg_id: str) -> dict[str, Any]:
    return service.users().messages().get(
        userId="me",
        id=msg_id,
        format="metadata",
        metadataHeaders=["From", "Subject", "Date"],
    ).execute()


def list_inbox_messages(service) -> list[dict[str, Any]]:
    messages = []
    page_token = None
    while True:
        response = service.users().messages().list(
            userId="me",
            q="in:inbox",
            maxResults=100,
            pageToken=page_token,
        ).execute()
        messages.extend(response.get("messages", []))
        page_token = response.get("nextPageToken")
        if not page_token:
            break
    return messages


def delete_message(service, msg_id: str, deletion_mode: str) -> None:
    if deletion_mode == "delete":
        service.users().messages().delete(userId="me", id=msg_id).execute()
    else:
        service.users().messages().trash(userId="me", id=msg_id).execute()


def scan_mailbox(config: dict[str, Any]) -> dict[str, Any]:
    service = gmail_service(config)
    state = load_state(config)
    allowed = {email.lower() for email in config["allowed_senders"]}
    seen_allowed = set(state.get("seen_allowed_ids", []))
    deleted_unauthorized = set(state.get("deleted_unauthorized_ids", []))
    pending_by_id = {item["id"]: item for item in state.get("pending", [])}

    summary = {
        "allowed_new": [],
        "allowed_existing": 0,
        "deleted_unauthorized": [],
        "errors": [],
    }

    for msg in list_inbox_messages(service):
        msg_id = msg["id"]
        try:
            data = header_for_message(service, msg_id)
            headers = {
                h["name"]: h["value"]
                for h in data.get("payload", {}).get("headers", [])
            }
            sender_name, sender_email = parse_sender(headers.get("From", ""))
            subject = headers.get("Subject", "(sans objet)")
            date_raw = headers.get("Date", "")
            internal_date = int(data.get("internalDate", 0))
        except Exception as exc:
            summary["errors"].append(f"{msg_id}: {exc}")
            continue

        if sender_email not in allowed:
            if msg_id not in deleted_unauthorized:
                try:
                    delete_message(service, msg_id, config.get("deletion_mode", "trash"))
                    deleted_unauthorized.add(msg_id)
                    summary["deleted_unauthorized"].append(
                        {"id": msg_id, "sender": sender_email, "subject": subject}
                    )
                except Exception as exc:
                    summary["errors"].append(f"delete {msg_id}: {exc}")
            continue

        if msg_id in pending_by_id:
            summary["allowed_existing"] += 1
            continue

        record = {
            "id": msg_id,
            "thread_id": data.get("threadId"),
            "sender_name": sender_name,
            "sender_email": sender_email,
            "subject": subject,
            "date": date_raw,
            "internal_date": internal_date,
            "status": "pending_user_instruction",
            "processed": False,
            "saved_to": None,
        }
        pending_by_id[msg_id] = record
        seen_allowed.add(msg_id)
        summary["allowed_new"].append(record)

    state["last_scan_at"] = datetime.now().isoformat(timespec="seconds")
    state["seen_allowed_ids"] = sorted(seen_allowed)
    state["deleted_unauthorized_ids"] = sorted(deleted_unauthorized)
    state["pending"] = sorted(
        pending_by_id.values(),
        key=lambda item: item.get("internal_date", 0),
        reverse=True,
    )
    save_state(config, state)

    return summary


def list_pending(config: dict[str, Any]) -> list[dict[str, Any]]:
    state = load_state(config)
    return [
        item
        for item in state.get("pending", [])
        if not item.get("processed")
    ]


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return slug or "message"


def decode_b64(data: str) -> bytes:
    return base64.urlsafe_b64decode(data.encode("utf-8"))


def extract_plain_text(payload: dict[str, Any]) -> str:
    mime = payload.get("mimeType", "")
    body = payload.get("body", {})
    data = body.get("data")

    if mime == "text/plain" and data:
        return decode_b64(data).decode("utf-8", errors="ignore")

    for part in payload.get("parts", []):
        text = extract_plain_text(part)
        if text:
            return text

    return ""


def walk_parts(payload: dict[str, Any]):
    yield payload
    for part in payload.get("parts", []) or []:
        yield from walk_parts(part)


def save_attachments(service, msg_id: str, payload: dict[str, Any], dest_dir: Path) -> list[str]:
    saved = []
    attachments_dir = dest_dir / "attachments"
    attachments_dir.mkdir(parents=True, exist_ok=True)

    for part in walk_parts(payload):
        filename = part.get("filename")
        body = part.get("body", {})
        attachment_id = body.get("attachmentId")
        inline_data = body.get("data")

        if not filename:
            continue

        content = None
        if attachment_id:
            attachment = service.users().messages().attachments().get(
                userId="me",
                messageId=msg_id,
                id=attachment_id,
            ).execute()
            content = decode_b64(attachment["data"])
        elif inline_data:
            content = decode_b64(inline_data)

        if content is None:
            continue

        target = attachments_dir / filename
        target.write_bytes(content)
        saved.append(str(target.relative_to(PKA_DIR)))

    return saved


def process_message(config: dict[str, Any], msg_id: str) -> dict[str, Any]:
    service = gmail_service(config)
    state = load_state(config)
    pending = state.get("pending", [])
    target = next((item for item in pending if item["id"] == msg_id), None)
    if not target:
        raise ValueError(f"Message inconnu dans la file d'attente: {msg_id}")

    data = service.users().messages().get(userId="me", id=msg_id, format="full").execute()
    payload = data.get("payload", {})
    headers = {
        h["name"]: h["value"]
        for h in payload.get("headers", [])
    }

    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    slug = slugify(target["subject"])[:60]
    dest_dir = resolve_path(config["extract_root"]) / f"{timestamp}_{slug}"
    dest_dir.mkdir(parents=True, exist_ok=True)

    body_text = extract_plain_text(payload).strip()
    attachments = save_attachments(service, msg_id, payload, dest_dir)

    md = [
        "# Email importé",
        "",
        f"- De : {headers.get('From', '')}",
        f"- Objet : {headers.get('Subject', '(sans objet)')}",
        f"- Date : {headers.get('Date', '')}",
        f"- Message ID : {msg_id}",
        "",
        "## Corps",
        "",
        body_text or "(corps texte non disponible)",
        "",
    ]

    if attachments:
        md.extend(["## Pièces jointes", ""])
        for item in attachments:
            md.append(f"- `{item}`")
        md.append("")

    output_file = dest_dir / "email.md"
    output_file.write_text("\n".join(md), encoding="utf-8")

    for item in pending:
        if item["id"] == msg_id:
            item["processed"] = True
            item["status"] = "imported_waiting_instruction"
            item["saved_to"] = str(output_file.relative_to(PKA_DIR))
            item["attachment_count"] = len(attachments)
            break

    state["pending"] = pending
    save_state(config, state)

    return {
        "id": msg_id,
        "saved_to": str(output_file.relative_to(PKA_DIR)),
        "attachments": attachments,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Garde-barrière Gmail PKA")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("scan", help="Scanne la boîte et applique la whitelist stricte")
    sub.add_parser("list", help="Liste les emails autorisés en attente")

    process_cmd = sub.add_parser("process", help="Importe un email autorisé après accord")
    process_cmd.add_argument("--id", required=True, help="ID Gmail du message à importer")

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    config = load_config()

    if args.command == "scan":
        result = scan_mailbox(config)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0

    if args.command == "list":
        print(json.dumps(list_pending(config), indent=2, ensure_ascii=False))
        return 0

    if args.command == "process":
        result = process_message(config, args.id)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
