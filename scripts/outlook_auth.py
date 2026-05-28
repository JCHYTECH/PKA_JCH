#!/usr/bin/env python3
"""
outlook_auth.py — A executer UNE SEULE FOIS dans le terminal.
Ouvre le navigateur pour l'authentification Microsoft, puis stocke le token.
"""

import json
from pathlib import Path
import msal

SECRETS_DIR = Path.home() / ".config" / "pka-jch"
MS_CONFIG = SECRETS_DIR / "outlook_config.json"
TOKEN_CACHE = SECRETS_DIR / "outlook_token.json"

if not MS_CONFIG.exists():
    MS_CONFIG = Path.home() / "PKA_JCH" / "docs" / "system" / "outlook_config.json"

SCOPES = ["https://graph.microsoft.com/Mail.ReadWrite"]

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
        print("Token deja valide. Rien a faire.")
        TOKEN_CACHE.write_text(cache.serialize())
        exit(0)

print("Ouverture du navigateur pour Outlook...")
result = app.acquire_token_interactive(
    scopes=SCOPES,
    prompt="select_account",
)

if "access_token" in result:
    TOKEN_CACHE.write_text(cache.serialize())
    print("OK. Token stocke.")
else:
    print(f"Echec: {result.get('error_description', result)}")
