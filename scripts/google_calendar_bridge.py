#!/usr/bin/env python3
"""Small Google Calendar bridge for PKA_JCH.

Uses a dedicated OAuth desktop credential and guarded PKA calendar scopes.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import socket
from pathlib import Path

from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


ROOT = Path(__file__).resolve().parents[1]
SYSTEM_DIR = ROOT / "JCH_Inbox" / "99_SYSTEM"
CREDENTIALS_FILE = SYSTEM_DIR / "google_calendar_credentials.json"
TOKEN_FILE = SYSTEM_DIR / "google_calendar_token.json"
COLORS_FILE = SYSTEM_DIR / "google_calendar_colors.json"
PKA_CALENDAR_PREFIX = "PKA — "
SCOPES = [
    "https://www.googleapis.com/auth/calendar.events",
    "https://www.googleapis.com/auth/calendar.calendars",
    "https://www.googleapis.com/auth/calendar.calendarlist",
]


def get_free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def has_required_saved_scopes(saved_scopes: list[str] | None, required_scopes: list[str]) -> bool:
    return set(saved_scopes or []) >= set(required_scopes)


def read_saved_token_scopes(token_file: Path = TOKEN_FILE) -> list[str] | None:
    if not token_file.exists():
        return None
    try:
        data = json.loads(token_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    return data.get("scopes")


def load_credentials() -> Credentials:
    creds = None
    saved_scopes = read_saved_token_scopes(TOKEN_FILE)
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE))

    if creds and creds.valid and has_required_saved_scopes(saved_scopes, SCOPES):
        return creds

    if creds and creds.expired and creds.refresh_token and has_required_saved_scopes(saved_scopes, SCOPES):
        try:
            creds.refresh(Request())
        except RefreshError:
            creds = None

    if not creds or not has_required_saved_scopes(saved_scopes, SCOPES):
        if not CREDENTIALS_FILE.exists():
            raise FileNotFoundError(f"Missing OAuth credentials: {CREDENTIALS_FILE}")
        flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
        creds = flow.run_local_server(
            host="localhost",
            port=get_free_port(),
            open_browser=True,
            authorization_prompt_message="Connexion Google Calendar ouverte dans le navigateur.",
            prompt="consent",
        )

    TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")
    os.chmod(TOKEN_FILE, 0o600)
    return creds


def service():
    return build("calendar", "v3", credentials=load_credentials())


def list_calendars() -> None:
    result = service().calendarList().list().execute()
    for cal in result.get("items", []):
        primary = " primary" if cal.get("primary") else ""
        access_role = cal.get("accessRole", "")
        print(f"{cal.get('id')}\t{cal.get('summary')}\t{access_role}{primary}")


def load_color_map() -> dict:
    if not COLORS_FILE.exists():
        return {}
    return json.loads(COLORS_FILE.read_text(encoding="utf-8"))


def pka_calendar_name(category: str, color_map: dict | None = None) -> str:
    colors = color_map if color_map is not None else load_color_map()
    normalized = category.upper()
    if normalized not in colors:
        known = ", ".join(sorted(colors)) or "none configured"
        raise ValueError(f"Unknown calendar category: {category}. Known: {known}")
    return f"{PKA_CALENDAR_PREFIX}{colors[normalized]['label']}"


def require_pka_calendar_name(calendar_name: str) -> None:
    if not calendar_name.startswith(PKA_CALENDAR_PREFIX):
        raise ValueError(f"Refusing to manage non-PKA calendar: {calendar_name}")


def build_event(
    *,
    summary: str,
    description: str,
    location: str,
    start: str,
    end: str,
    timezone: str,
    category: str = "",
) -> dict:
    start_dt = dt.datetime.fromisoformat(start)
    end_dt = dt.datetime.fromisoformat(end)
    event = {
        "summary": summary,
        "description": description,
        "start": {"dateTime": start_dt.isoformat(), "timeZone": timezone},
        "end": {"dateTime": end_dt.isoformat(), "timeZone": timezone},
    }
    if location:
        event["location"] = location
    if category:
        color_map = load_color_map()
        normalized = category.upper()
        if normalized not in color_map:
            known = ", ".join(sorted(color_map)) or "none configured"
            raise ValueError(f"Unknown calendar category: {category}. Known: {known}")
        event["colorId"] = str(color_map[normalized]["colorId"])
    return event


def add_event(args: argparse.Namespace) -> None:
    calendar_id = args.calendar_id
    if args.use_pka_calendar:
        if not args.category:
            raise ValueError("--use-pka-calendar requires --category")
        calendar_id = ensure_pka_calendar(args.category)
    event = build_event(
        summary=args.summary,
        description=args.description,
        location=args.location,
        start=args.start,
        end=args.end,
        timezone=args.timezone,
        category="" if args.use_pka_calendar else args.category,
    )

    created = service().events().insert(calendarId=calendar_id, body=event).execute()
    print(created.get("htmlLink", created.get("id", "created")))


def update_event_color(args: argparse.Namespace) -> None:
    color_map = load_color_map()
    normalized = args.category.upper()
    if normalized not in color_map:
        known = ", ".join(sorted(color_map)) or "none configured"
        raise ValueError(f"Unknown calendar category: {args.category}. Known: {known}")
    patched = (
        service()
        .events()
        .patch(
            calendarId=args.calendar_id,
            eventId=args.event_id,
            body={"colorId": str(color_map[normalized]["colorId"])},
        )
        .execute()
    )
    print(patched.get("htmlLink", patched.get("id", "updated")))


def calendar_color_body(color_info: dict) -> dict:
    if "background" in color_info and "foreground" in color_info:
        return {
            "backgroundColor": color_info["background"],
            "foregroundColor": color_info["foreground"],
        }
    return {}


def find_calendar_by_summary(summary: str) -> dict | None:
    page_token = None
    calendar_service = service()
    while True:
        result = calendar_service.calendarList().list(pageToken=page_token).execute()
        for calendar in result.get("items", []):
            if calendar.get("summary") == summary:
                return calendar
        page_token = result.get("nextPageToken")
        if not page_token:
            return None


def ensure_pka_calendar(category: str) -> str:
    colors = load_color_map()
    normalized = category.upper()
    calendar_name = pka_calendar_name(normalized, colors)
    require_pka_calendar_name(calendar_name)

    calendar_service = service()
    existing = find_calendar_by_summary(calendar_name)
    if existing:
        calendar_id = existing["id"]
    else:
        created = (
            calendar_service.calendars()
            .insert(body={"summary": calendar_name, "timeZone": "Europe/Brussels"})
            .execute()
        )
        calendar_id = created["id"]

    color_body = calendar_color_body(colors[normalized])
    if color_body:
        color_body["selected"] = True
        calendar_service.calendarList().update(
            calendarId=calendar_id,
            colorRgbFormat=True,
            body=color_body,
        ).execute()
    return calendar_id


def sync_pka_calendars() -> None:
    for category in sorted(load_color_map()):
        calendar_id = ensure_pka_calendar(category)
        print(f"{category}\t{calendar_id}\t{pka_calendar_name(category)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="PKA_JCH Google Calendar bridge")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("auth", help="Authorize and save the local token")
    subparsers.add_parser("list-calendars", help="List visible Google calendars")
    subparsers.add_parser("sync-pka-calendars", help="Create/update guarded PKA calendars")

    add = subparsers.add_parser("add-event", help="Create an event")
    add.add_argument("--calendar-id", default="primary")
    add.add_argument("--summary", required=True)
    add.add_argument("--description", default="")
    add.add_argument("--location", default="")
    add.add_argument("--start", required=True, help="ISO local datetime, e.g. 2026-06-04T14:00:00")
    add.add_argument("--end", required=True, help="ISO local datetime, e.g. 2026-06-04T15:00:00")
    add.add_argument("--timezone", default="Europe/Brussels")
    add.add_argument("--category", default="", help="Category key from google_calendar_colors.json")
    add.add_argument(
        "--use-pka-calendar",
        action="store_true",
        help="Route event to the guarded PKA calendar for --category",
    )

    update_color = subparsers.add_parser("update-color", help="Set an event color by category")
    update_color.add_argument("--calendar-id", default="primary")
    update_color.add_argument("--event-id", required=True)
    update_color.add_argument("--category", required=True)

    args = parser.parse_args()
    if args.command == "auth":
        load_credentials()
        print(f"Token saved: {TOKEN_FILE}")
    elif args.command == "list-calendars":
        list_calendars()
    elif args.command == "sync-pka-calendars":
        sync_pka_calendars()
    elif args.command == "add-event":
        add_event(args)
    elif args.command == "update-color":
        update_event_color(args)


if __name__ == "__main__":
    main()
