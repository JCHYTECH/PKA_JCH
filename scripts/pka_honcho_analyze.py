#!/usr/bin/env python3
"""
pka_honcho_analyze.py — User modeling évolutif (pattern Honcho/Hermes).
Analyse les sessions récentes, détecte des patterns utilisateur,
propose des mises à jour de USER.md.

⚠️ Mode principal = SYNCHRONE (Dobby analyse en direct après chaque session).
   Ce script est le fallback batch pour l'analyse rétrospective.

Usage batch (fallback) :
    python3 scripts/pka_honcho_analyze.py --days 7 --dry-run
    python3 scripts/pka_honcho_analyze.py --since 2026-06-12

Design spec : docs/system/honcho-pka-design.md
Règle SOUL.md : section « Honcho PKA — user modeling synchrone post-session »
"""

import argparse
import json
import sqlite3
import sys
from datetime import datetime, timedelta
from pathlib import Path

PKA_DIR = Path(__file__).resolve().parents[1]
TEAM_DB = PKA_DIR / "TEAM" / "team.db"
USER_MD = PKA_DIR / "USER.md"

CATEGORIES = ["preference", "habit", "project_interest", "technical", "communication"]


def load_recent_sessions(days: int = 7) -> list[dict]:
    """Charge les sessions récentes depuis team.db (memory_log)."""
    since = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    try:
        with sqlite3.connect(TEAM_DB) as con:
            rows = con.execute(
                """SELECT memory_name, model, body, project_key, created_at
                   FROM memory_log
                   WHERE created_at >= ?
                   ORDER BY created_at DESC""",
                (since,),
            ).fetchall()
    except sqlite3.DatabaseError:
        return []

    return [
        {
            "name": r[0],
            "model": r[1],
            "body": r[2] or "",
            "project": r[3] or "",
            "date": r[4],
        }
        for r in rows
    ]


def analyze_sessions(sessions: list[dict]) -> list[dict]:
    """
    Analyse heuristique des sessions pour détecter des patterns.
    En production, cette fonction délègue au LLM.
    """
    insights = []
    all_text = " ".join(s["body"] for s in sessions)

    # Heuristiques par catégorie
    project_keywords = {
        "WILDNEXUS": "WildNexus",
        "ARTEON": "ARTEON",
        "VETALYX": "Vetalyx",
        "PHOTO": "PHOTO_NATURE",
        "INSECTNET": "InsectNet",
        "IOT": "IOT",
    }

    # project_interest — fréquence de mention par projet
    for key, label in project_keywords.items():
        count = all_text.lower().count(key.lower())
        if count >= 3:
            insights.append({
                "category": "project_interest",
                "insight": f"Projet {label} mentionné {count} fois sur la période",
                "evidence": f"{count} occurrences dans memory_log",
                "confidence": min(0.5 + count * 0.1, 1.0),
            })

    # communication — détection de ton
    collaborative_markers = ["faisons", "collaborons", "ensemble", "équipe", "let's", "we"]
    direct_markers = ["fais", "exécute", "lance", "do it", "run"]
    collab_count = sum(all_text.lower().count(m) for m in collaborative_markers)
    direct_count = sum(all_text.lower().count(m) for m in direct_markers)
    if collab_count > direct_count * 2:
        insights.append({
            "category": "communication",
            "insight": "Ton collaboratif dominant (faisons/ensemble > fais/exécute)",
            "evidence": f"marqueurs collaboratifs: {collab_count}, directifs: {direct_count}",
            "confidence": 0.7,
        })

    # technical — détection de nouveaux outils mentionnés
    tech_markers = {
        "ollama": "Ollama",
        "docker": "Docker",
        "mlx": "MLX",
        "wokwi": "Wokwi",
        "zigbee": "Zigbee",
        "tailscale": "Tailscale",
    }
    for key, label in tech_markers.items():
        if key in all_text.lower():
            insights.append({
                "category": "technical",
                "insight": f"Technologie {label} activement utilisée",
                "evidence": f"Mentionné dans memory_log",
                "confidence": 0.6,
            })

    return insights


def store_insights(insights: list[dict], dry_run: bool = False) -> int:
    """Stocke les insights dans team.db (user_model)."""
    if dry_run:
        return len(insights)

    stored = 0
    try:
        with sqlite3.connect(TEAM_DB) as con:
            for ins in insights:
                con.execute(
                    """INSERT INTO user_model
                       (category, insight, evidence, confidence, status, created_at)
                       VALUES (?, ?, ?, ?, 'proposed', datetime('now'))""",
                    (
                        ins["category"],
                        ins["insight"],
                        ins.get("evidence", ""),
                        ins.get("confidence", 0.5),
                    ),
                )
                stored += 1
    except sqlite3.DatabaseError as e:
        print(f"Erreur DB: {e}", file=sys.stderr)

    return stored


def propose_user_md_diff(insights: list[dict]) -> list[str]:
    """Génère des propositions de modification de USER.md."""
    diffs = []
    for ins in insights:
        if ins["category"] == "project_interest":
            diffs.append(f"+ Focus prioritaire : {ins['insight']}")
        elif ins["category"] == "technical":
            diffs.append(f"+ Technologie active : {ins['insight']}")
        elif ins["category"] == "communication":
            diffs.append(f"+ Préférence : {ins['insight']}")
        elif ins["category"] == "preference":
            diffs.append(f"+ Préférence : {ins['insight']}")
    return diffs


def main():
    parser = argparse.ArgumentParser(
        description="pka_honcho_analyze — User modeling évolutif (Honcho pattern)"
    )
    parser.add_argument("--days", type=int, default=7, help="Jours à analyser (défaut: 7)")
    parser.add_argument("--since", help="Date de début (YYYY-MM-DD)")
    parser.add_argument("--dry-run", action="store_true", help="Afficher sans écrire")
    parser.add_argument("--apply", action="store_true", help="Appliquer les insights (DB + proposer diff USER.md)")
    parser.add_argument("--json", action="store_true", help="Sortie JSON")
    args = parser.parse_args()

    if args.since:
        try:
            days = (datetime.now() - datetime.strptime(args.since, "%Y-%m-%d")).days
        except ValueError:
            print("Format date invalide. Utiliser YYYY-MM-DD.", file=sys.stderr)
            sys.exit(1)
    else:
        days = args.days

    sessions = load_recent_sessions(days)
    if not sessions:
        print(json.dumps({"status": "empty", "message": f"Aucune session sur les {days} derniers jours"}))
        return

    insights = analyze_sessions(sessions)
    stored = store_insights(insights, dry_run=args.dry_run)
    diffs = propose_user_md_diff(insights)

    output = {
        "status": "ok",
        "period_days": days,
        "sessions_analyzed": len(sessions),
        "insights_found": len(insights),
        "insights_stored": stored,
        "insights": [
            {
                "category": i["category"],
                "insight": i["insight"],
                "confidence": i["confidence"],
            }
            for i in insights
        ],
        "user_md_diff": diffs,
    }

    if args.json:
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(f"=== pka_honcho_analyze v0.1.0 ===\n")
        print(f"Période : {days} jours")
        print(f"Sessions analysées : {len(sessions)}")
        print(f"Insights trouvés : {len(insights)}")
        for ins in insights:
            print(f"  [{ins['category']}] {ins['insight']} (confiance: {ins['confidence']:.1f})")
        if diffs:
            print(f"\n--- USER.md diff proposé ---")
            for d in diffs:
                print(f"  {d}")
        if not args.dry_run and stored:
            print(f"\n✅ {stored} insights stockés dans team.db (user_model)")
        elif args.dry_run:
            print(f"\n🔍 Dry run — {len(insights)} insights auraient été stockés")


if __name__ == "__main__":
    main()
