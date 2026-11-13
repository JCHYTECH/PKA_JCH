#!/usr/bin/env python3
"""
check_balances.py — Solde DeepSeek + OpenRouter en une commande.

Usage :
  python3 scripts/check_balances.py

Lit :
  - DEEPSEEK_API_KEY depuis ~/.config/pka-jch/api_keys
  - Clé OpenRouter depuis ~/.config/pka-jch/openrouter_key.txt
Interroge les endpoints de solde en temps réel.
"""
import os
import re
import json
import urllib.request
import urllib.error

DEEPSEEK_BALANCE_URL = "https://api.deepseek.com/user/balance"
OPENROUTER_CREDITS_URL = "https://openrouter.ai/api/v1/credits"


def read_api_keys():
    """Extrait les clés de ~/.config/pka-jch/api_keys (format shell)."""
    path = os.path.expanduser("~/.config/pka-jch/api_keys")
    keys = {}
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                m = re.match(r'(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*["\']?([^"\'#\s]+)', line)
                if m:
                    keys[m.group(1)] = m.group(2)
    except OSError:
        pass
    return keys


def get(url, key):
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {key}"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))


def main():
    keys = read_api_keys()
    ds_key = keys.get("DEEPSEEK_API_KEY") or os.environ.get("DEEPSEEK_API_KEY")
    or_key = None
    try:
        with open(os.path.expanduser("~/.config/pka-jch/openrouter_key.txt")) as f:
            or_key = f.read().strip()
    except OSError:
        pass

    print("💳 Soldes LLM")
    print("=" * 44)

    # --- DeepSeek (API directe) ---
    if ds_key:
        try:
            d = get(DEEPSEEK_BALANCE_URL, ds_key)
            if d.get("is_available"):
                for bi in d.get("balance_infos", []):
                    cur = bi.get("currency", "?")
                    total = bi.get("total_balance", "?")
                    granted = bi.get("granted_balance", "?")
                    topped = bi.get("topped_up_balance", "?")
                    print(f"DeepSeek  ({cur}) : {total} dispo  (recharge {topped} · promo {granted})")
            else:
                print("DeepSeek  : solde indisponible")
        except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError) as e:
            print(f"DeepSeek  : erreur ({e})")
    else:
        print("DeepSeek  : clé absente")

    # --- OpenRouter (voie alternative) ---
    if or_key:
        try:
            d = get(OPENROUTER_CREDITS_URL, or_key)
            data = d.get("data", {})
            total = float(data.get("total_credits", 0) or 0)
            used = float(data.get("total_usage", 0) or 0)
            remaining = total - used
            print(f"OpenRouter : {total:.2f} crédits · utilisés {used:.2f} · restants {remaining:.2f}")
        except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError) as e:
            print(f"OpenRouter : erreur ({e})")
    else:
        print("OpenRouter : clé absente")


if __name__ == "__main__":
    main()
