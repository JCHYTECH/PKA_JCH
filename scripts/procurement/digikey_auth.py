#!/usr/bin/env python3
"""
Authentification OAuth2 DigiKey — à lancer UNE SEULE FOIS dans un terminal interactif.
Le token est mis en cache dans ~/.procurement_digikey_token.json (valide 90 jours).

Usage :
    python3 -m scripts.procurement.digikey_auth
"""
import json
import time
import urllib.parse
import webbrowser
import requests
from pathlib import Path

# Charger config sans importer le module entier (évite les dépendances)
from . import config as cfg

_BASE = "https://sandbox-api.digikey.com" if cfg.DIGIKEY_SANDBOX else "https://api.digikey.com"
_AUTH_URL = f"{_BASE}/v1/oauth2/authorize"
_TOKEN_URL = f"{_BASE}/v1/oauth2/token"


def main():
    if not cfg.DIGIKEY_CLIENT_ID or not cfg.DIGIKEY_CLIENT_SECRET:
        print("❌ DIGIKEY_CLIENT_ID / DIGIKEY_CLIENT_SECRET manquants dans ~/.procurement.env")
        return

    # Vérifier si un token valide existe déjà
    if cfg.DIGIKEY_TOKEN_CACHE.exists():
        try:
            token = json.loads(cfg.DIGIKEY_TOKEN_CACHE.read_text())
            if time.time() < token.get("expires_at", 0) - 60:
                print("✅ Token DigiKey valide en cache — aucune action requise.")
                print(f"   Expire dans {int((token['expires_at'] - time.time()) / 60)} min")
                return
        except Exception:
            pass

    params = {
        "response_type": "code",
        "client_id": cfg.DIGIKEY_CLIENT_ID,
        "redirect_uri": cfg.DIGIKEY_REDIRECT_URI,
    }
    auth_url = f"{_AUTH_URL}?{urllib.parse.urlencode(params)}"

    print("\n🔐 DigiKey OAuth2 — Autorisation initiale")
    print("=" * 55)
    print("\n1. Ouvre cette URL dans ton navigateur :")
    print(f"\n   {auth_url}\n")
    print("2. Connecte-toi à DigiKey et autorise l'app PKA_JCH")
    print("3. Le navigateur redirige vers une page d'erreur — c'est normal")
    print("4. Copie l'URL complète depuis la barre d'adresse\n")
    print("   Elle ressemble à : https://localhost?code=XXXXXXXX\n")

    try:
        webbrowser.open(auth_url)
    except Exception:
        pass

    raw = input("Colle l'URL de redirection ici : ").strip()

    qs = urllib.parse.parse_qs(urllib.parse.urlparse(raw).query)
    code = qs.get("code", [""])[0]
    if not code:
        print("❌ Code OAuth non trouvé dans l'URL. Réessaie.")
        return

    print("\n⏳ Échange du code contre un token...")
    resp = requests.post(
        _TOKEN_URL,
        data={
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": cfg.DIGIKEY_REDIRECT_URI,
            "client_id": cfg.DIGIKEY_CLIENT_ID,
            "client_secret": cfg.DIGIKEY_CLIENT_SECRET,
        },
        timeout=15,
    )

    if resp.status_code != 200:
        print(f"❌ Erreur token : {resp.status_code} — {resp.text}")
        return

    data = resp.json()
    data["expires_at"] = time.time() + data.get("expires_in", 1800)
    cfg.DIGIKEY_TOKEN_CACHE.write_text(json.dumps(data, indent=2))
    cfg.DIGIKEY_TOKEN_CACHE.chmod(0o600)

    print(f"✅ Token mis en cache : {cfg.DIGIKEY_TOKEN_CACHE}")
    print(f"   Access token valide {data.get('expires_in', 1800) // 60} min")
    print(f"   Refresh token valide 90 jours — renouvellement automatique")
    print("\n   Tu peux maintenant lancer --push-digikey sans interaction.")


if __name__ == "__main__":
    main()
