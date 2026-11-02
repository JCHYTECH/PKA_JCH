#!/usr/bin/env python3
"""
google_auth.py
Authentification OAuth2 Google — à exécuter une seule fois.
Génère token.json utilisé ensuite par email_digest.py.
"""

import os
import socket
from google.auth.exceptions import RefreshError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.modify",
    "https://www.googleapis.com/auth/gmail.send",
    "https://www.googleapis.com/auth/calendar.readonly",
]

BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
SECRETS_DIR = os.path.expanduser("~/.config/pka-jch")
CREDS_FILE  = os.path.join(SECRETS_DIR, "credentials.json")
TOKEN_FILE  = os.path.join(SECRETS_DIR, "token.json")

def get_free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])

creds = None
if os.path.exists(TOKEN_FILE):
    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

if not creds or not creds.valid:
    try:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            raise RefreshError("No valid refresh token available.")
    except RefreshError:
        flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
        port = get_free_port()
        creds = flow.run_local_server(
            host="localhost",
            port=port,
            open_browser=True,
            browser="open -a 'Google Chrome' %s",
            authorization_prompt_message="Connexion Google ouverte dans Chrome.",
            prompt="consent",
        )
    with open(TOKEN_FILE, "w") as f:
        f.write(creds.to_json())

print("Authentification réussie. token.json généré.")
