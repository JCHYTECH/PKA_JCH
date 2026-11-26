#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Future Invest — Commodity Watch (météo + géopolitique, continu)

Surveille en continu les signaux qui touchent les matières premières :
  - Géopolitique : GDELT DOC 2.0 (embargos, restrictions, sécheresses)
  - Météo : US Drought Monitor (sécheresse US — proxy blé/maïs/soja)
Écrit un journal quotidien + un état JSON. --dry-run par défaut (règle PKA).

Usage :
  python3 scripts/futureinvest_commodity_watch.py          # dry-run (affiche, n'écrit pas)
  python3 scripts/futureinvest_commodity_watch.py --apply  # écrit journal + état
"""
import json
import os
import sys
import datetime
import urllib.parse
import urllib.request
import time

BASE = "/Users/jchavauxm5/PKA_JCH"
PROJ = os.path.join(BASE, "JCH_Inbox/03_PROJECTS/10_FUTURE_INVEST")
LOG_DIR = os.path.join(PROJ, "logs", "watch")
STATE_FILE = os.path.join(BASE, "_local", "futureinvest_watch_state.json")

# --- Géopolitique : requêtes GDELT (commodités/pays clés) ---
GEO_QUERIES = [
    ("export ban grain", "grain-export-ban"),
    ("export restriction rice", "rice-export-restriction"),
    ("india rice export", "india-rice"),
    ("wheat export russia ukraine", "wheat-black-sea"),
    ("drought", "drought"),
    ("sanction fertilizer", "fertilizer-sanction"),
]

# --- Météo ---
DROUGHT_URL = "https://droughtmonitor.unl.edu/DmData/JSON.aspx"
ALERT_THRESHOLD = 100  # articles GDELT / 30 j


def fetch(url, timeout=25, retries=2):
    last = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "futureinvest-watch/1.0"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode("utf-8", "replace")
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2 * (attempt + 1))  # backoff
    raise last


def gdelt_count(query):
    """Nombre d'articles GDELT sur 30 jours pour une requête."""
    url = (
        "https://api.gdeltproject.org/api/v2/doc/doc"
        f"?query={urllib.parse.quote(query)}"
        "&mode=artcount&timespan=30d&format=json"
    )
    data = json.loads(fetch(url))
    return int(data.get("articles", data.get("totalresults", 0)))


def drought_avg_d1_d4():
    """% moyen de superficie en sécheresse D1-D4 (proxy, non pondéré par surface)."""
    data = json.loads(fetch(DROUGHT_URL))
    if not isinstance(data, list) or not data:
        return None
    total = 0.0
    n = 0
    for row in data:
        try:
            total += sum(float(row.get(k, 0)) for k in ("D1", "D2", "D3", "D4"))
            n += 1
        except (TypeError, ValueError):
            continue
    return round(total / n, 2) if n else None


def main():
    dry = "--apply" not in sys.argv
    stamp = datetime.datetime.now().strftime("%Y-%m-%d")

    report = {"date": stamp, "dry_run": dry, "geopolitical": {}, "weather": {}}
    for query, key in GEO_QUERIES:
        try:
            report["geopolitical"][key] = gdelt_count(query)
            time.sleep(1.5)  # GDELT rate limit (429) — espace les requêtes
        except Exception as e:  # noqa: BLE001
            report["geopolitical"][key] = f"ERR {e}"
    try:
        report["weather"]["us_drought_d1_d4_avg_pct"] = drought_avg_d1_d4()
    except Exception as e:  # noqa: BLE001
        report["weather"]["us_drought"] = f"ERR {e}"

    if dry:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        print("[dry-run] n'écrit rien. Relancer avec --apply pour journaliser.")
        return

    os.makedirs(LOG_DIR, exist_ok=True)
    log_path = os.path.join(LOG_DIR, f"{stamp}.md")

    prev = {}
    if os.path.exists(STATE_FILE):
        try:
            prev = json.load(open(STATE_FILE, encoding="utf-8"))
        except Exception:
            prev = {}

    alerts = []
    for k, v in report["geopolitical"].items():
        if isinstance(v, int) and v >= ALERT_THRESHOLD:
            alerts.append(f"geopolitical:{k} ({v} articles/30j)")
    cur_drought = report["weather"].get("us_drought_d1_d4_avg_pct")
    prev_drought = prev.get("weather", {}).get("us_drought_d1_d4_avg_pct")
    if isinstance(cur_drought, (int, float)) and isinstance(prev_drought, (int, float)):
        if cur_drought > prev_drought + 2.0:
            alerts.append(f"sécheresse US en hausse {prev_drought}% → {cur_drought}%")

    lines = [f"# Commodity Watch — {stamp}", ""]
    lines.append("## Géopolitique (GDELT, 30 j)")
    for k, v in report["geopolitical"].items():
        lines.append(f"- {k}: {v}")
    lines.append("")
    lines.append("## Météo")
    lines.append(f"- sécheresse US (moy D1-D4): {cur_drought}%")
    lines.append("")
    lines.append("## Alertes")
    lines.extend(("- " + a for a in alerts) if alerts else ["- rien de notable"])

    with open(log_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    print(f"Écrit {log_path} — {len(alerts)} alerte(s)")


if __name__ == "__main__":
    main()
