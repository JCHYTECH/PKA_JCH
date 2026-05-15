#!/usr/bin/env python3
"""
argus_progression.py
Forge 🦦 — Calcule l'indice de progression Argus par client et par palier.
Paliers : 20 · 50 · 100 photos

Usage :
  python3 argus_progression.py [--client CLIENT_ID] [--output rapport.md]
  python3 argus_progression.py --check   # vérifie si un palier est atteint (exit 0 = nouveau palier)
"""

import argparse
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH    = Path(__file__).resolve().parent.parent / "PHOTO" / "argus_critique.db"
TEAM_INBOX = Path(__file__).resolve().parent.parent / "TEAM_Inbox" / "ARTEON_Phase0"
PALIERS    = [20, 50, 100]

AXES = [
    ("score_composition", "Composition"),
    ("score_exposition",  "Exposition"),
    ("score_nettete",     "Netteté"),
    ("score_technique",   "Technique"),
    ("score_impact",      "Impact visuel"),
]


def get_photos(client_id: str) -> list[dict]:
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    rows = con.execute(
        """SELECT id, created_at, filename, species,
                  score_composition, score_exposition, score_nettete,
                  score_technique, score_impact, score_total, tier
           FROM analyses
           WHERE client_id = ?
           ORDER BY id ASC""",
        (client_id,)
    ).fetchall()
    con.close()
    return [dict(r) for r in rows]


def assign_palier(rank: int) -> int | None:
    """Retourne le palier (20/50/100) auquel appartient cette photo, ou None."""
    for p in PALIERS:
        if rank <= p:
            return p
    return None


def compute_windows(photos: list[dict]) -> dict:
    """
    Découpe les photos en fenêtres cumulatives aux paliers.
    Retourne {palier: {axe: moyenne, 'total': moyenne, 'count': n}}
    """
    windows = {}
    for palier in PALIERS:
        subset = photos[:palier]
        if not subset:
            continue
        n = len(subset)
        entry = {"count": n}
        for col, label in AXES:
            entry[label] = round(sum(p[col] for p in subset) / n, 2)
        entry["Total"] = round(sum(p["score_total"] for p in subset) / n, 1)
        windows[palier] = entry
    return windows


def compute_deltas(windows: dict) -> dict:
    """
    Calcule les deltas entre paliers consécutifs.
    Retourne {(p1, p2): {axe: delta}}
    """
    deltas = {}
    paliers_available = sorted(windows.keys())
    for i in range(1, len(paliers_available)):
        p_prev = paliers_available[i - 1]
        p_curr = paliers_available[i]
        d = {}
        for _, label in AXES + [("score_total", "Total")]:
            prev_val = windows[p_prev].get(label, 0)
            curr_val = windows[p_curr].get(label, 0)
            delta = round(curr_val - prev_val, 2)
            pct   = round((delta / prev_val * 100), 1) if prev_val else 0
            d[label] = {"delta": delta, "pct": pct}
        deltas[(p_prev, p_curr)] = d
    return deltas


def trend_icon(delta: float) -> str:
    if delta > 0.3:   return "↑ ✅"
    if delta < -0.3:  return "↓ ⚠️"
    return "→"


def build_report(client_id: str, photos: list[dict],
                 windows: dict, deltas: dict) -> str:
    n = len(photos)
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    lines = [
        f"# Argus — Indice de Progression · {client_id}",
        f"",
        f"**Client :** {client_id}  ",
        f"**Date :** {now}  ",
        f"**Photos analysées :** {n}",
        f"",
        f"---",
        f"",
        f"## Scores moyens par palier",
        f"",
        f"| Axe | " + " | ".join(f"≤{p} photos (n={windows[p]['count']})"
                                  for p in sorted(windows)) + " |",
        f"|-----|" + "|".join("---" for _ in windows) + "|",
    ]

    for _, label in AXES:
        row = f"| **{label}** |"
        for p in sorted(windows):
            val = windows[p].get(label, "—")
            row += f" {val}/20 |"
        lines.append(row)

    # Total
    row = f"| **TOTAL** |"
    for p in sorted(windows):
        val = windows[p].get("Total", "—")
        row += f" **{val}/100** |"
    lines.append(row)

    # Deltas
    if deltas:
        lines += ["", "---", "", "## Indice de progression (Δ entre paliers)", ""]
        for (p_prev, p_curr), d in sorted(deltas.items()):
            lines.append(f"### Palier {p_prev} → {p_curr} photos")
            lines.append("")
            lines.append(f"| Axe | Δ | % | Tendance |")
            lines.append(f"|-----|---|---|----------|")
            for _, label in AXES:
                info = d.get(label, {})
                delta = info.get("delta", 0)
                pct   = info.get("pct", 0)
                icon  = trend_icon(delta)
                sign  = "+" if delta >= 0 else ""
                lines.append(f"| {label} | {sign}{delta} | {sign}{pct}% | {icon} |")
            total_d = d.get("Total", {})
            td = total_d.get("delta", 0)
            tp = total_d.get("pct", 0)
            sign = "+" if td >= 0 else ""
            lines.append(f"| **TOTAL** | **{sign}{td}** | **{sign}{tp}%** | {trend_icon(td)} |")
            lines.append("")

    # Synthèse
    if len(windows) >= 2:
        last_p  = max(windows)
        first_p = min(windows)
        best_axis  = max(AXES, key=lambda x: windows[last_p].get(x[1], 0))[1]
        worst_axis = min(AXES, key=lambda x: windows[last_p].get(x[1], 0))[1]
        total_delta = round(windows[last_p]["Total"] - windows[first_p]["Total"], 1)
        sign = "+" if total_delta >= 0 else ""

        lines += [
            "---", "",
            "## Synthèse",
            "",
            f"- **Point fort constant :** {best_axis} — score le plus élevé au dernier palier",
            f"- **Axe de progression prioritaire :** {worst_axis} — score le plus faible",
            f"- **Progression globale :** {sign}{total_delta} pts entre palier {first_p} et {last_p}",
        ]

        # Note pédagogique sur le biais de sélection
        if total_delta < 0:
            lines += [
                "",
                "> **Note :** Une baisse entre le premier et le dernier palier est normale et "
                "ne reflète pas un recul de vos compétences. Les photographes soumettent "
                "naturellement leurs meilleures images en premier — c'est un biais de sélection "
                "bien connu. Au fil des paliers, vous prenez confiance et soumettez des photos "
                "plus variées, parfois plus risquées. C'est précisément là que la progression "
                "réelle devient mesurable.",
            ]

    # Invitation coaching
    lines += [
        "",
        "---",
        "",
        "## Envie d'aller plus loin ?",
        "",
        f"Votre axe le plus faible est **{worst_axis}**. Nos experts peuvent vous aider à "
        f"corriger ça — non pas en post-traitement, mais **avant de déclencher**.",
        "",
        "Notre équipe de conseillers techniques peut vous proposer :",
        "",
        f"- **Fiches setup terrain** adaptées à votre matériel et vos sujets de prédilection",
        f"- **Profils boîtier** préconfigurés pour vos 3 situations les plus fréquentes",
        f"- **Brief pré-sortie** personnalisé selon vos conditions de lumière habituelles",
        "",
        "📩 Répondez simplement **OUI** à cet email pour recevoir vos recommandations "
        "personnalisées sous 48h.",
        "",
        "---",
        "",
        "*Rapport généré par Argus 🦅 — Service ARTEON · L'Instant Lu*",
    ]
    return "\n".join(lines)


def check_new_palier(client_id: str) -> int | None:
    """Retourne le palier nouvellement atteint, ou None."""
    photos = get_photos(client_id)
    n = len(photos)
    for p in PALIERS:
        if n == p:
            return p
    return None


def main():
    parser = argparse.ArgumentParser(description="Indice de progression Argus")
    parser.add_argument("--client", default="JCH", help="Client ID")
    parser.add_argument("--output", default=None, help="Fichier de sortie (.md)")
    parser.add_argument("--check", action="store_true",
                        help="Vérifie si un palier vient d'être atteint (exit 1 si non)")
    args = parser.parse_args()

    if args.check:
        palier = check_new_palier(args.client)
        if palier:
            print(f"PALIER_ATTEINT: {palier}")
            exit(0)
        else:
            exit(1)

    photos  = get_photos(args.client)
    n       = len(photos)

    if n < PALIERS[0]:
        print(f"⚠️  {n} photos — minimum {PALIERS[0]} requis pour l'analyse de progression.")
        exit(0)

    windows = compute_windows(photos)
    deltas  = compute_deltas(windows)
    report  = build_report(args.client, photos, windows, deltas)

    if args.output:
        out = Path(args.output)
    else:
        TEAM_INBOX.mkdir(parents=True, exist_ok=True)
        ts  = datetime.now().strftime("%Y-%m-%d_%H-%M")
        out = TEAM_INBOX / f"{ts}_argus_progression_{args.client}.md"

    out.write_text(report)
    print(f"✅ Rapport de progression → {out}")

    # Affiche synthèse console
    last_p = max(windows)
    print(f"\n📊 {n} photos analysées — score moyen : {windows[last_p]['Total']}/100")
    for _, label in AXES:
        val = windows[last_p].get(label, "—")
        print(f"   {label:<20} {val}/20")


if __name__ == "__main__":
    main()
