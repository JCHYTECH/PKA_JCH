#!/usr/bin/env python3
"""box_monitor.py — Surveillance ping de la box Proximus (LAN + WAN).

Usage :
    python3 scripts/box_monitor.py --duration 900            # 15 min
    python3 scripts/box_monitor.py --duration 30 --interval 1  # test court

Sortie : résumé JSON sur stdout + copie dans --json-out.
Code de sortie : 0 = aucune coupure · 1 = coupures détectées.
"""
from __future__ import annotations

import argparse
import datetime
import json
import re
import subprocess
import threading
import time

TARGETS = {"lan": "192.168.128.1", "wan": "8.8.8.8"}


def ping_once(host: str, timeout_ms: int = 1000):
    """Un ping. Retourne (ok, latence_ms|None)."""
    try:
        p = subprocess.run(
            ["ping", "-c", "1", "-W", str(timeout_ms), host],
            capture_output=True, text=True, timeout=3,
        )
        m = re.search(r"time[=<]([\d.]+)\s*ms", p.stdout + p.stderr)
        ok = p.returncode == 0 and m is not None
        return ok, (float(m.group(1)) if m else None)
    except Exception:
        return False, None


def monitor(key, host, duration, interval, results, lock):
    log = open(f"/tmp/box-monitor-{key}.log", "a")
    r = {"sent": 0, "ok": 0, "fail": 0, "latencies": [], "outages": []}
    end = time.time() + duration
    outage_start = None
    while time.time() < end:
        t = datetime.datetime.now()
        ok, lat = ping_once(host)
        with lock:
            r["sent"] += 1
            line = f"{t.isoformat(timespec='seconds')} {'OK' if ok else 'FAIL'}"
            if lat is not None:
                line += f" {lat:.1f}ms"
            log.write(line + "\n")
            log.flush()
            if ok:
                r["ok"] += 1
                r["latencies"].append(lat)
                if outage_start is not None:
                    r["outages"].append({
                        "start": outage_start.isoformat(timespec="seconds"),
                        "end": t.isoformat(timespec="seconds"),
                        "duration_s": round((t - outage_start).total_seconds(), 1),
                    })
                    outage_start = None
            else:
                r["fail"] += 1
                if outage_start is None:
                    outage_start = t
        time.sleep(interval)
    if outage_start is not None:
        now = datetime.datetime.now()
        r["outages"].append({
            "start": outage_start.isoformat(timespec="seconds"),
            "end": now.isoformat(timespec="seconds"),
            "duration_s": round((now - outage_start).total_seconds(), 1),
        })
    log.close()
    with lock:
        results[key] = r


def summarize(key, r, host):
    lat = r["latencies"]
    return {
        "host": host,
        "sent": r["sent"],
        "ok": r["ok"],
        "fail": r["fail"],
        "loss_pct": round(100.0 * r["fail"] / r["sent"], 1) if r["sent"] else 0,
        "lat_min": round(min(lat), 1) if lat else None,
        "lat_avg": round(sum(lat) / len(lat), 1) if lat else None,
        "lat_max": round(max(lat), 1) if lat else None,
        "outage_count": len(r["outages"]),
        "outages": r["outages"],
    }


def main():
    ap = argparse.ArgumentParser(description="Surveillance ping box Proximus")
    ap.add_argument("--duration", type=int, default=900, help="Durée en secondes (défaut 900 = 15 min)")
    ap.add_argument("--interval", type=float, default=2.0, help="Intervalle entre pings (s)")
    ap.add_argument("--json-out", default="/tmp/box-monitor-summary.json", help="Chemin du résumé JSON")
    args = ap.parse_args()

    start = datetime.datetime.now()
    results = {}
    lock = threading.Lock()
    threads = [
        threading.Thread(target=monitor, args=(k, v, args.duration, args.interval, results, lock))
        for k, v in TARGETS.items()
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    summary = {
        "start": start.isoformat(timespec="seconds"),
        "end": datetime.datetime.now().isoformat(timespec="seconds"),
    }
    for k, v in TARGETS.items():
        summary[k] = summarize(k, results[k], v)

    with open(args.json_out, "w") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))

    total_outages = sum(summary[k]["outage_count"] for k in TARGETS)
    raise SystemExit(1 if total_outages > 0 else 0)


if __name__ == "__main__":
    main()
