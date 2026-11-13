# scripts/procurement/digikey_client.py
"""
Crée une MyList DigiKey avec les composants validés.
JCH ouvre la liste sur digikey.be et l'ajoute au panier manuellement.

⚠️  Requiert OAuth2 3-legged (Authorization Code Flow).
    Première utilisation : un navigateur s'ouvre pour autoriser l'accès.
    Le refresh token est mis en cache dans ~/.procurement_digikey_token.json
    (valide 90 jours — renouvellement automatique).

Config .procurement.env :
    DIGIKEY_CLIENT_ID=xxx
    DIGIKEY_CLIENT_SECRET=xxx
    DIGIKEY_REDIRECT_URI=https://localhost   # doit correspondre à l'app DK
    DIGIKEY_SANDBOX=false                    # true pour tests
"""
import json
import time
import threading
import webbrowser
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from typing import Optional

import requests

from .models import ProcurementResult
from . import config as cfg

# ── URLs DigiKey ────────────────────────────────────────────────────────────
_BASE = "https://sandbox-api.digikey.com" if cfg.DIGIKEY_SANDBOX else "https://api.digikey.com"
_AUTH_URL = f"{_BASE}/v1/oauth2/authorize"
_TOKEN_URL = f"{_BASE}/v1/oauth2/token"
_MYLISTS_URL = f"{_BASE}/mylists/v1/lists"
_SITE_URL = "https://www.digikey.be/en/mylists"


# ── Token cache ──────────────────────────────────────────────────────────────

def _load_token() -> dict:
    if cfg.DIGIKEY_TOKEN_CACHE.exists():
        try:
            return json.loads(cfg.DIGIKEY_TOKEN_CACHE.read_text())
        except Exception:
            pass
    return {}


def _save_token(data: dict) -> None:
    cfg.DIGIKEY_TOKEN_CACHE.write_text(json.dumps(data, indent=2))
    cfg.DIGIKEY_TOKEN_CACHE.chmod(0o600)


def _token_expired(token: dict) -> bool:
    return time.time() >= token.get("expires_at", 0) - 60


# ── OAuth helpers ─────────────────────────────────────────────────────────────

def _refresh_access_token(refresh_token: str) -> dict:
    resp = requests.post(
        _TOKEN_URL,
        data={
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": cfg.DIGIKEY_CLIENT_ID,
            "client_secret": cfg.DIGIKEY_CLIENT_SECRET,
        },
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    data["expires_at"] = time.time() + data.get("expires_in", 1800)
    return data


def _exchange_code(code: str) -> dict:
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
    resp.raise_for_status()
    data = resp.json()
    data["expires_at"] = time.time() + data.get("expires_in", 1800)
    return data


def _browser_auth_flow() -> str:
    """
    Lance le navigateur et intercepte le code OAuth sur localhost:8080.
    Retourne le code d'autorisation.
    Si le redirect_uri configuré n'est pas localhost, demande à l'utilisateur
    de coller l'URL de redirection manuellement.
    """
    params = {
        "response_type": "code",
        "client_id": cfg.DIGIKEY_CLIENT_ID,
        "redirect_uri": cfg.DIGIKEY_REDIRECT_URI,
    }
    auth_url = f"{_AUTH_URL}?{urllib.parse.urlencode(params)}"

    parsed_redirect = urllib.parse.urlparse(cfg.DIGIKEY_REDIRECT_URI)
    redirect = cfg.DIGIKEY_REDIRECT_URI.lower()
    # Serveur local uniquement pour http://localhost:<port> explicite
    use_local_server = (
        parsed_redirect.scheme == "http"
        and ("localhost" in redirect or "127.0.0.1" in redirect)
        and parsed_redirect.port is not None
    )

    if use_local_server:
        parsed = parsed_redirect
        port = parsed.port
        code_holder: dict = {}

        class _Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                qs = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
                code_holder["code"] = qs.get("code", [""])[0]
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"<h2>DigiKey auth OK. Vous pouvez fermer cet onglet.</h2>")
                threading.Thread(target=self.server.shutdown, daemon=True).start()

            def log_message(self, *_):
                pass  # silencieux

        server = HTTPServer(("", port), _Handler)
        print(f"\n🔐 DigiKey OAuth — ouverture navigateur…")
        print(f"   (serveur local sur port {port})\n")
        webbrowser.open(auth_url)
        server.serve_forever()
        code = code_holder.get("code", "")
        if not code:
            raise RuntimeError("Aucun code OAuth reçu depuis DigiKey.")
        return code
    else:
        # Redirect non-localhost : flow manuel
        print(f"\n🔐 DigiKey OAuth — ouvre cette URL dans ton navigateur :")
        print(f"\n   {auth_url}\n")
        print("   Après autorisation, DigiKey te redirige vers une URL du type :")
        print(f"   {cfg.DIGIKEY_REDIRECT_URI}?code=XXXXX")
        print("\n   Colle l'URL complète de redirection ici :")
        raw = input("   → ").strip()
        qs = urllib.parse.parse_qs(urllib.parse.urlparse(raw).query)
        code = qs.get("code", [""])[0]
        if not code:
            raise RuntimeError("Code OAuth non trouvé dans l'URL collée.")
        return code


def _get_access_token() -> str:
    """Retourne un access token valide — refresh ou nouveau flow si nécessaire."""
    if not cfg.DIGIKEY_CLIENT_ID or not cfg.DIGIKEY_CLIENT_SECRET:
        raise RuntimeError(
            "❌ DIGIKEY_CLIENT_ID / DIGIKEY_CLIENT_SECRET manquants dans .procurement.env"
        )

    token = _load_token()

    # Token valide en cache
    if token.get("access_token") and not _token_expired(token):
        return token["access_token"]

    # Refresh token disponible
    if token.get("refresh_token"):
        try:
            token = _refresh_access_token(token["refresh_token"])
            _save_token(token)
            return token["access_token"]
        except Exception:
            pass  # refresh échoué → re-auth complète

    # Nouveau flow navigateur
    code = _browser_auth_flow()
    token = _exchange_code(code)
    _save_token(token)
    return token["access_token"]


# ── MyLists API ───────────────────────────────────────────────────────────────

def _auth_headers(access_token: str) -> dict:
    return {
        "Authorization": f"Bearer {access_token}",
        "X-DIGIKEY-Client-Id": cfg.DIGIKEY_CLIENT_ID,
        "X-DIGIKEY-Locale-Site": "BE",
        "X-DIGIKEY-Locale-Language": "en",
        "X-DIGIKEY-Locale-Currency": "EUR",
        "Content-Type": "application/json",
    }


def _create_list(access_token: str, list_name: str) -> str:
    """Crée une MyList DigiKey et retourne son ID."""
    resp = requests.post(
        _MYLISTS_URL,
        headers=_auth_headers(access_token),
        json={"ListName": list_name},
        timeout=15,
    )
    if not resp.ok:
        raise RuntimeError(f"{resp.status_code} {resp.reason} — {resp.text[:300]}")
    data = resp.json()
    if isinstance(data, str):
        return data  # DigiKey retourne l'ID directement comme string JSON
    return data.get("listId") or data.get("id") or data.get("ListId") or str(data)


def _add_parts(access_token: str, list_id: str, items: list) -> None:
    """Ajoute des composants à une MyList existante."""
    url = f"{_MYLISTS_URL}/{list_id}/parts"
    resp = requests.post(
        url,
        headers=_auth_headers(access_token),
        json=items,  # DigiKey attend un tableau JSON direct
        timeout=15,
    )
    resp.raise_for_status()


# ── Point d'entrée public ─────────────────────────────────────────────────────

def push_digikey_list(result: ProcurementResult, list_name: str = "PKA_Procurement") -> str:
    """
    Crée une MyList DigiKey avec les composants validés du ProcurementResult.
    Retourne une string décrivant le résultat (URL liste ou message d'erreur).
    Jamais de commande automatique — JCH valide et commande manuellement.
    """
    if not cfg.DIGIKEY_CLIENT_ID or not cfg.DIGIKEY_CLIENT_SECRET:
        return (
            "⚠️ Mode simulation DigiKey — liste non créée. "
            "Ajouter DIGIKEY_CLIENT_ID + DIGIKEY_CLIENT_SECRET dans .procurement.env pour activer."
        )

    # Construire la liste des items éligibles
    items = []
    for e in result.enriched:
        mpn = e.found_mpn or e.component.mpn
        if not mpn or e.flag == "⚠️ MANUEL":
            continue
        items.append({
            "requestedPartNumber": mpn,
            "quantities": [{"quantity": e.component.qty}],
            "customerReference": e.component.ref,
            "notes": e.component.description[:100] if e.component.description else "",
        })

    if not items:
        return "⚠️ Aucun composant éligible pour la liste DigiKey (MPN manquants ou tous MANUEL)."

    try:
        access_token = _get_access_token()
        list_id = _create_list(access_token, list_name)
        _add_parts(access_token, list_id, items)
        list_url = f"{_SITE_URL}?listId={list_id}"
        return f"✅ MyList DigiKey créée ({len(items)} composants) : {list_url}"

    except Exception as exc:
        return f"❌ Erreur MyList DigiKey : {exc}"
