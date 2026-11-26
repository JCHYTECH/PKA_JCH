#!/usr/bin/env python3
"""
outlook_auth.py — À exécuter UNE SEULE FOIS dans le terminal.
Authentification Microsoft (device code) → stocke le token.
Lecture seule : Mail.Read, Calendars.Read, Contacts.Read (consentement Orban45, 24/11).
Aucun envoi, aucune écriture.
"""

import json
from pathlib import Path
import msal

SECRETS_DIR = Path.home() / ".config" / "pka-jch"
MS_CONFIG = SECRETS_DIR / "outlook_config.json"
TOKEN_CACHE = SECRETS_DIR / "outlook_token.json"

if not MS_CONFIG.exists():
    MS_CONFIG = Path.home() / "PKA_JCH" / "docs" / "system" / "outlook_config.json"

# Lecture seule — conforme au consentement accordé par Orban45 (24/11).
SCOPES = [
    "https://graph.microsoft.com/Mail.Read",
    "https://graph.microsoft.com/Calendars.Read",
    "https://graph.microsoft.com/Contacts.Read",
]

config = json.loads(MS_CONFIG.read_text())

cache = msal.SerializableTokenCache()
if TOKEN_CACHE.exists():
    cache.deserialize(TOKEN_CACHE.read_text())

app = msal.PublicClientApplication(
    config["client_id"],
    authority=f"https://login.microsoftonline.com/{config['tenant_id']}",
    token_cache=cache,
)

accounts = app.get_accounts()
result = None
if accounts:
    result = app.acquire_token_silent(SCOPES, account=accounts[0])
    if result:
        print("Token déjà valide. Rien à faire.")
        TOKEN_CACHE.write_text(cache.serialize())
        exit(0)

print("Authentification device code...")
flow = app.initiate_device_flow(scopes=SCOPES)
if "user_code" not in flow:
    print(f"Échec: {flow.get('error_description', flow)}")
    exit(1)
print(flow["message"])
result = app.acquire_token_by_device_flow(flow)

if "access_token" in result:
    TOKEN_CACHE.write_text(cache.serialize())
    print("OK. Token stocké.")
else:
    print(f"Échec: {result.get('error_description', result)}")
