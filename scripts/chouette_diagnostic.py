#!/usr/bin/env python3
"""
chouette_diagnostic.py
Chouette 🦉 — Diagnostic matériel : corrèle les scores Argus avec les données EXIF
pour distinguer problème technique (photographe) vs problème matériel (équipement).

Usage :
  python3 chouette_diagnostic.py [--client CLIENT_ID] [--min-photos 5]
"""

import argparse
import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH    = Path(__file__).resolve().parent.parent / "PHOTO" / "argus_critique.db"
TEAM_INBOX = Path(__file__).resolve().parent.parent / "TEAM_Inbox" / "ARTEON_Phase0"

# Seuils de diagnostic
SCORE_WEAK   = 14.0   # axe faible si moyenne < ce seuil /20
SCORE_STRONG = 16.0   # axe fort si moyenne > ce seuil


def get_photos(client_id: str) -> list[dict]:
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    rows = con.execute(
        """SELECT filename, species, focal_length, aperture, iso_value, shutter_speed,
                  score_composition, score_exposition, score_nettete,
                  score_technique, score_impact, score_total, tier
           FROM analyses
           WHERE client_id = ? AND focal_length IS NOT NULL
           ORDER BY id ASC""",
        (client_id,)
    ).fetchall()
    con.close()
    return [dict(r) for r in rows]


def segment(photos: list[dict], key: str, threshold) -> tuple[list, list]:
    """Sépare les photos en deux groupes selon un seuil sur une colonne EXIF."""
    above = [p for p in photos if p.get(key) and p[key] >= threshold]
    below = [p for p in photos if p.get(key) and p[key] < threshold]
    return above, below


def avg(photos: list[dict], col: str) -> float | None:
    vals = [p[col] for p in photos if p.get(col) is not None]
    return round(sum(vals) / len(vals), 2) if vals else None


def diagnose(photos: list[dict]) -> list[dict]:
    """
    Produit une liste de diagnostics détectés.
    Chaque diagnostic : {type, finding, recommendation, evidence}
    """
    diagnostics = []

    if not photos:
        return diagnostics

    # ── Diagnostic 1 : Netteté vs Focale ─────────────────────────────────────
    long, short = segment(photos, "focal_length", 400)
    if len(long) >= 3 and len(short) >= 3:
        net_long  = avg(long,  "score_nettete")
        net_short = avg(short, "score_nettete")
        if net_long and net_short and (net_short - net_long) >= 1.5:
            diagnostics.append({
                "type":   "MATÉRIEL",
                "axe":    "Netteté",
                "finding": f"Netteté {net_long}/20 au-delà de 400mm vs {net_short}/20 en dessous",
                "cause":   "Limite optique du zoom en bout de focale — chute de résolution et de contraste normale sur les télézooms",
                "recommendation": (
                    "Fermer d'1 à 2 stops au-delà de 400mm (f/8 minimum). "
                    "Tester avec l'Extender EF 1.4x sur le RF 200-800mm pour "
                    "les longues distances — meilleure constance optique que le Tamron en bout."
                ),
            })

    # ── Diagnostic 2 : Netteté vs ISO ────────────────────────────────────────
    hi_iso, lo_iso = segment(photos, "iso_value", 3200)
    if len(hi_iso) >= 3 and len(lo_iso) >= 3:
        net_hi = avg(hi_iso, "score_nettete")
        net_lo = avg(lo_iso, "score_nettete")
        if net_hi and net_lo and (net_lo - net_hi) >= 1.5:
            diagnostics.append({
                "type":   "MATÉRIEL + TECHNIQUE",
                "axe":    "Netteté / Technique",
                "finding": f"Netteté {net_hi}/20 au-dessus de ISO 3200 vs {net_lo}/20 en dessous",
                "cause":   "Bruit de luminance à ISO élevé — impact sur la perception de netteté par le jury",
                "recommendation": (
                    "Passer les fichiers ISO 3200+ dans DxO PureRaw avant Lightroom — "
                    "réduction de bruit la plus efficace sur capteurs Canon. "
                    "Sur le 90D : plafonner à ISO 1600 si possible (capteur plus bruité que le R10)."
                ),
            })

    # ── Diagnostic 3 : Exposition vs Ouverture ───────────────────────────────
    wide, closed = segment(photos, "aperture", 6.3)  # f/6.3 = ouverture large pour ce matos
    if len(wide) >= 3 and len(closed) >= 3:
        exp_wide   = avg(wide,   "score_exposition")
        exp_closed = avg(closed, "score_exposition")
        if exp_wide and exp_closed and (exp_closed - exp_wide) >= 1.2:
            diagnostics.append({
                "type":   "TECHNIQUE",
                "axe":    "Exposition",
                "finding": f"Exposition {exp_wide}/20 à grande ouverture vs {exp_closed}/20 fermé",
                "cause":   "Grande ouverture + longue focale = profondeur de champ très faible — le boîtier a plus de mal à mesurer correctement l'exposition",
                "recommendation": (
                    "En mode Av à grande ouverture : activer la mesure Spot sur l'œil du sujet "
                    "plutôt que la mesure évaluative. Corriger +0,7 EV sur fond sombre."
                ),
            })

    # ── Diagnostic 4 : Technique globale — photographe ou matériel ? ─────────
    mean_tech = avg(photos, "score_technique")
    mean_net  = avg(photos, "score_nettete")
    mean_exp  = avg(photos, "score_exposition")
    mean_comp = avg(photos, "score_composition")
    mean_imp  = avg(photos, "score_impact")

    if mean_tech and mean_comp and mean_imp:
        creative_avg  = round((mean_comp + mean_imp) / 2, 2)
        technical_avg = round((mean_tech + mean_net + mean_exp) / 3, 2) if mean_net and mean_exp else None
        if technical_avg and (creative_avg - technical_avg) >= 1.5:
            diagnostics.append({
                "type":   "PROFIL",
                "axe":    "Créatif vs Technique",
                "finding": f"Axes créatifs (composition + impact) : {creative_avg}/20 · Axes techniques : {technical_avg}/20",
                "cause":   "L'œil est en avance sur la maîtrise technique — profil courant chez les photographes autodidactes talentueux",
                "recommendation": (
                    "Travailler en priorité l'exposition et la netteté — les gains seront "
                    "immédiats car la vision créative est déjà là. "
                    "Activer les profils C1/C2/C3 recommandés par Chouette pour automatiser "
                    "les réglages dans les situations récurrentes."
                ),
            })

    return diagnostics


def build_report(client_id: str, photos: list[dict], diagnostics: list[dict]) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    n   = len(photos)

    lines = [
        f"# Chouette — Diagnostic Matériel · {client_id}",
        f"",
        f"**Client :** {client_id}  ",
        f"**Date :** {now}  ",
        f"**Photos avec données EXIF :** {n}",
        f"",
        f"---",
        f"",
    ]

    if not diagnostics:
        lines += [
            "## ✅ Aucun problème matériel détecté",
            "",
            "Les scores techniques sont homogènes quelle que soit la focale, "
            "l'ouverture ou l'ISO. Les axes faibles identifiés par Argus relèvent "
            "de la technique photographique, pas du matériel.",
        ]
    else:
        lines += [f"## {len(diagnostics)} diagnostic(s) identifié(s)", ""]
        for i, d in enumerate(diagnostics, 1):
            badge = "🔧" if d["type"] == "MATÉRIEL" else ("📐" if d["type"] == "TECHNIQUE" else "🔍")
            lines += [
                f"### {badge} Diagnostic {i} — {d['type']} · {d['axe']}",
                f"",
                f"**Constat :** {d['finding']}  ",
                f"**Cause :** {d['cause']}  ",
                f"**Recommandation :** {d['recommendation']}",
                f"",
            ]

    lines += [
        "---",
        "",
        "*Rapport généré par Chouette 🦉 — Service ARTEON · L'Instant Lu*",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Chouette — Diagnostic matériel")
    parser.add_argument("--client",     default="JCH")
    parser.add_argument("--min-photos", type=int, default=5,
                        help="Nombre minimum de photos EXIF pour analyser")
    parser.add_argument("--output",     default=None)
    args = parser.parse_args()

    photos = get_photos(args.client)

    if len(photos) < args.min_photos:
        print(f"⚠️  Seulement {len(photos)} photos avec EXIF — minimum {args.min_photos} requis.")
        return

    diagnostics = diagnose(photos)
    report      = build_report(args.client, photos, diagnostics)

    if args.output:
        out = Path(args.output)
    else:
        TEAM_INBOX.mkdir(parents=True, exist_ok=True)
        ts  = datetime.now().strftime("%Y-%m-%d_%H-%M")
        out = TEAM_INBOX / f"{ts}_chouette_diagnostic_{args.client}.md"

    out.write_text(report)
    print(f"✅ Diagnostic → {out}")
    print(f"   {len(diagnostics)} diagnostic(s) détecté(s) sur {len(photos)} photos EXIF")


if __name__ == "__main__":
    main()
