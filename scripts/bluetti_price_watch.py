#!/usr/bin/env python3
"""
bluetti_price_watch.py — Surveille les prix Bluetti EU (Elite 100 V2 + Charger 2)
Dobby 🦉 — 2026-10-03

Fetch l'API Shopify publique de bluettipower.eu, compare au prix de référence
(prix constaté le 03/10/2026) et alerte si le prix descend sous le seuil —
dans l'optique de déclencher un achat avant le Black Friday.

Usage :
  python3 scripts/bluetti_price_watch.py --check    (défaut) affiche l'état
  python3 scripts/bluetti_price_watch.py --alert    alerte si baisse (fichier + notification)
  python3 scripts/bluetti_price_watch.py --reset    réinitialise les prix de référence

Dépendances : stdlib uniquement (urllib), python3.
"""

import json
import os
import subprocess
import sys
import urllib.request
from datetime import datetime, timezone

PKA_ROOT = os.path.expanduser("~/PKA_JCH")
STATE_DIR = os.path.join(PKA_ROOT, "_local", "state")
LOG_DIR = os.path.join(PKA_ROOT, "_local", "logs")
STATE_FILE = os.path.join(STATE_DIR, "bluetti_price_watch.json")
LOG_FILE = os.path.join(LOG_DIR, "bluetti_price_watch.log")

BASE = "https://www.bluettipower.eu"

# Prix de référence au 2026-10-03 (constatés via l'API Shopify EU).
# baseline = prix actuel ; on alerte dès que le prix passe EN DESSOUS.
PRODUCTS = [
    {
        "name": "Elite 100 V2",
        "handle": "elite-100-v2-portable-power-station",
        "sku_prefix": "EL100V2-EU-GY",   # variante de base (prise EU), €499
        "baseline": 499.00,
    },
    {
        "name": "Charger 2",
        "handle": "bluetti-charger-2-alternator-solar-charger",
        "sku_prefix": "CG-DC-UN",        # variante de base "Charger 2 (Included DC Cable)", €399
        "baseline": 399.00,
    },
]

USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) PKA-Price-Watch/1.0"


def fetch_product(handle):
    url = f"{BASE}/products/{handle}.json"
    req = urllib.request.Request(
        url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def extract_price(prod, data):
    variants = data.get("product", {}).get("variants", [])
    for v in variants:
        if v.get("sku", "").startswith(prod["sku_prefix"]):
            compare = v.get("compare_at_price")
            return {
                "price": float(v.get("price", "0")),
                "compare_at": float(compare) if compare else None,
                "sku": v.get("sku"),
                "variant": v.get("title"),
            }
    return None


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            return json.load(f)
    return {"reference": {}, "last_seen": {}, "last_alerted": {}}


def save_state(state):
    os.makedirs(STATE_DIR, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def log(msg):
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.now(timezone.utc).isoformat()}] {msg}\n")


def notify(title, body):
    try:
        subprocess.run(
            ["osascript", "-e",
             f'display notification "{body}" with title "{title}" sound name "Basso"'],
            check=False, timeout=10,
        )
    except Exception:
        pass


def collect():
    results = []
    for prod in PRODUCTS:
        try:
            info = extract_price(prod, fetch_product(prod["handle"]))
            err = None if info else f"variante {prod['sku_prefix']} introuvable"
        except Exception as e:
            info, err = None, f"erreur fetch: {e}"
        results.append((prod, info, err))
    return results


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--check"
    state = load_state()

    if mode == "--reset":
        for prod, info, err in collect():
            if info:
                state["reference"][prod["name"]] = info["price"]
        save_state(state)
        print("✅ Références réinitialisées aux prix actuels :")
        for k, v in state["reference"].items():
            print(f"  {k}: {v:.2f} €")
        return 0

    results = collect()
    drops = []
    lines = []

    for prod, info, err in results:
        if err:
            lines.append(f"⚠️  {prod['name']}: {err}")
            continue

        ref = state["reference"].get(prod["name"], prod["baseline"])
        price = info["price"]
        delta = price - ref
        marker = "🟢" if price < ref else ("🔴" if price > ref else "⚪")
        compare = f"{info['compare_at']:.2f}" if info["compare_at"] else "—"
        lines.append(
            f"{marker} {prod['name']}: {price:.2f} € (réf {ref:.2f} €, "
            f"{'+' if delta > 0 else ''}{delta:.2f}) | barré {compare}"
        )

        state["last_seen"][prod["name"]] = price

        # Alerte si prix < référence ET nouveau plus-bas non encore signalé.
        if price < ref and state["last_alerted"].get(prod["name"]) != price:
            drops.append((prod, info, ref, delta))
        elif price >= ref:
            # le prix est remonté → réarme l'alerte pour une future baisse.
            state["last_alerted"].pop(prod["name"], None)

    save_state(state)

    report = "\n".join(lines)
    print(report)
    log(f"mode={mode} | " + " | ".join(lines))

    if drops and mode == "--alert":
        os.makedirs(os.path.join(PKA_ROOT, "TEAM_Inbox"), exist_ok=True)
        stamp = datetime.now().strftime("%Y-%m-%d")
        alert_path = os.path.join(
            PKA_ROOT, "TEAM_Inbox", f"{stamp}_dobby_bluetti-price-alert.md"
        )
        with open(alert_path, "w") as f:
            f.write(f"# 🛒 Baisse de prix Bluetti détectée — {stamp}\n\n")
            for prod, info, ref, delta in drops:
                f.write(f"- **{prod['name']}** : {info['price']:.2f} € "
                        f"(réf {ref:.2f} €, {delta:.2f} €)\n")
                f.write(f"  - Variante : {info['variant']} ({info['sku']})\n")
                f.write(f"  - URL : {BASE}/products/{prod['handle']}\n")
            f.write("\n> À arbitrer avant le Black Friday : acheter ou attendre.\n")

        for prod, info, ref, delta in drops:
            state["last_alerted"][prod["name"]] = info["price"]
        save_state(state)

        notify("🛒 Bluetti baisse de prix",
               f"{len(drops)} produit(s) sous le seuil de référence")
        print(f"\n🔔 Alerte écrite : {alert_path}")
        return 1

    if drops:
        print(f"\n🔔 {len(drops)} baisse(s) détectée(s) "
              f"(mode --check → pas de notification). Lancez --alert pour notifier.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
