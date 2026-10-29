#!/usr/bin/env python3
"""
provider_balance.py  🦉  — Solde des comptes API LLM

Vérifie les crédits restants chez les fournisseurs qui exposent
une API de solde : OpenRouter, DeepSeek, NVIDIA.
(OpenAI, Anthropic, Gemini sont post-payés — pas de solde à checker.)

Usage :
    python3 scripts/provider_balance.py
    python3 scripts/provider_balance.py --json
    python3 scripts/provider_balance.py --warn-only
    python3 scripts/provider_balance.py --threshold 5
"""

import json, os, sys, urllib.request
from pathlib import Path

SECRETS_DIR = Path.home() / ".config" / "pka-jch"
WARN_THRESHOLD_USD = 10.0


def _read_key_file(filename: str) -> str | None:
    p = SECRETS_DIR / filename
    return p.read_text().strip() if p.is_file() else None


def _read_org_id() -> str | None:
    org = os.environ.get("OPENAI_ORG_ID")
    if org:
        return org
    api_file = SECRETS_DIR / "api_keys"
    if api_file.is_file():
        for line in api_file.read_text().splitlines():
            line = line.strip()
            if line.startswith("export "):
                line = line[7:]
            if line.startswith("OPENAI_ORG_ID="):
                return line.split("=", 1)[1].strip().strip('"').strip("'").strip()
    return None


def _read_key(env_var: str, filename: str | None = None) -> str | None:
    key = os.environ.get(env_var)
    if not key and filename:
        key = _read_key_file(filename)
    if not key:
        # Fallback: parse api_keys file (supports `KEY=val` and `export KEY=val`)
        api_file = SECRETS_DIR / "api_keys"
        if api_file.is_file():
            for line in api_file.read_text().splitlines():
                line = line.strip()
                if line.startswith("export "):
                    line = line[7:]
                if line.startswith(env_var + "="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'").strip()
    return key


def _api_get(url: str, key: str) -> dict:
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {key}"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())


def check_openrouter() -> dict:
    key = _read_key("OPENROUTER_API_KEY", "openrouter_key.txt")
    if not key:
        return {"provider": "OpenRouter", "status": "no_key", "balance": None}
    try:
        data = _api_get("https://openrouter.ai/api/v1/auth/key", key)
        d = data.get("data", {})
        # OpenRouter: limit_remaining = crédits restants, credits = solde pré-payé
        balance = float(d.get("limit_remaining", d.get("credits", 0)))
        usage_m = float(d.get("usage_monthly", 0))
        return {"provider": "OpenRouter", "status": "ok", "balance": round(balance, 2), "currency": "USD", "usage_monthly": round(usage_m, 2)}
    except Exception as e:
        return {"provider": "OpenRouter", "status": "error", "balance": None, "error": str(e)[:60]}


def check_deepseek() -> dict:
    key = _read_key("DEEPSEEK_API_KEY")
    if not key:
        return {"provider": "DeepSeek", "status": "no_key", "balance": None}
    try:
        data = _api_get("https://api.deepseek.com/user/balance", key)
        b = float(data.get("balance_io", 0))  # non-expiring credits
        return {"provider": "DeepSeek", "status": "ok", "balance": round(b, 4), "currency": data.get("currency", "CNY")}
    except Exception as e:
        return {"provider": "DeepSeek", "status": "error", "balance": None, "error": str(e)[:60]}


def check_openai_usage() -> dict:
    """Consommation OpenAI du mois en cours. Priorité OPENAI_BILLING_KEY (org-level)."""
    key = _read_key("OPENAI_BILLING_KEY") or _read_key("OPENAI_API_KEY")
    if not key:
        return {"provider": "OpenAI", "status": "no_key", "usage_month": None}
    from datetime import date
    today = date.today()
    start = today.replace(day=1).isoformat()
    end = today.isoformat()
    url = f"https://api.openai.com/v1/dashboard/billing/usage?start_date={start}&end_date={end}"
    org_id = _read_org_id()
    try:
        req = urllib.request.Request(url, headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        })
        if org_id:
            req.add_header("OpenAI-Organization", org_id)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        total = float(data.get("total_usage", 0)) / 100  # OpenAI returns in cents
        return {"provider": "OpenAI", "status": "ok", "usage_month": round(total, 2), "currency": "USD", "period": f"{start}..{end}"}
    except Exception as e:
        error_str = str(e)[:80]
        if "403" in error_str:
            error_str = "403 Forbidden — clé sans scope billing ou org ID manquant"
        return {"provider": "OpenAI", "status": "error", "usage_month": None, "error": error_str}


def get_balances(with_openai: bool = True) -> dict:
    """Exportable — retourne tous les soldes et usages. Utilisable par dobby_retro."""
    results = [check_openrouter(), check_deepseek(), check_nvidia()]
    if with_openai:
        results.append(check_openai_usage())
    total_balance = sum(r["balance"] for r in results if r.get("balance") is not None and r.get("currency") == "USD")
    warnings = [r for r in results if r["status"] in ("error",) or (
        r.get("balance") is not None and r["balance"] < WARN_THRESHOLD_USD
    )]
    return {
        "results": results,
        "total_balance_usd": round(total_balance, 2),
        "warnings": len(warnings) > 0,
        "warning_count": len(warnings),
        "threshold_usd": WARN_THRESHOLD_USD,
    }


def check_nvidia() -> dict:
    key = _read_key("NVIDIA_API_KEY", "nvidia_key.txt")
    if not key:
        return {"provider": "NVIDIA", "status": "no_key", "balance": None}
    try:
        data = _api_get("https://api.build.nvidia.com/v1/credits", key)
        r = float(data.get("remaining_credits", 0))
        return {"provider": "NVIDIA", "status": "ok", "balance": round(r, 2), "currency": "USD"}
    except Exception as e:
        return {"provider": "NVIDIA", "status": "error", "balance": None, "error": str(e)[:60]}


POST_PAID = [
    ("Anthropic", "api.anthropic.com", "Console → Usage"),
    ("Gemini", "generativelanguage.googleapis.com", "Google Cloud Billing"),
    ("Kimi", "(API inconnue)", "Dashboard partenaire"),
]


def format_report(results: list[dict], threshold: float, warn_only: bool) -> str:
    lines = []
    any_warn = False
    for r in results:
        s = r["status"]
        if s == "no_key":
            if not warn_only:
                lines.append(f"  {r['provider']:12s} ⚪ pas de clé")
            continue
        if s == "error":
            lines.append(f"  {r['provider']:12s} 🔴 {r.get('error','?')}")
            any_warn = True
            continue
        b = r["balance"]
        cur = r.get("currency", "USD")
        low = b is not None and b < threshold
        if low:
            lines.append(f"  {r['provider']:12s} {'🔴' if b < threshold/2 else '🟡'} ${b} {cur} (bas)")
            any_warn = True
        elif not warn_only:
            lines.append(f"  {r['provider']:12s} 🟢 ${b} {cur}")
    if any_warn:
        lines.append("\n  ⚠️ Comptes bas ou erreurs détectés.")
    return "\n".join(lines)


def main():
    threshold = WARN_THRESHOLD_USD
    as_json = "--json" in sys.argv
    warn_only = "--warn-only" in sys.argv
    for i, a in enumerate(sys.argv[1:]):
        if a == "--threshold" and i + 1 < len(sys.argv[1:]):
            threshold = float(sys.argv[1:][i + 1])

    data = get_balances(with_openai=True)
    results = data["results"]

    if as_json:
        print(json.dumps({"providers": results, "total_balance_usd": data["total_balance_usd"], "threshold_usd": threshold}, indent=2, ensure_ascii=False))
        return

    print("─── Provider API Balances ───\n")
    print(format_report(results, threshold, warn_only))

    # Show OpenAI consumption separately (it's usage, not balance)
    openai = next((r for r in results if r["provider"] == "OpenAI"), None)
    if openai and openai["status"] == "ok":
        print(f"  OpenAI      📊 ${openai['usage_month']} consommé ce mois-ci")
    elif openai and openai["status"] == "error":
        print(f"  OpenAI      🔴 {openai.get('error','?')}")

    print("\nPost-payés (dashboard uniquement) :")
    for name, url, note in POST_PAID:
        print(f"  {name:12s} → {url} ({note})")

    if data["total_balance_usd"]:
        print(f"\nTotal disponible (USD) : ${data['total_balance_usd']:.2f}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrompu.")
