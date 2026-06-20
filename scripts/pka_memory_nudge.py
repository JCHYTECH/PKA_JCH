#!/usr/bin/env python3
"""
pka_memory_nudge.py — Extraction de mémoire post-réponse (pattern Hermes).
Analyse les derniers échanges et extrait : faits sur JC, décisions, patterns.

⚠️ Mode principal = SYNCHRONE (Dobby analyse en direct après ~10 réponses).
   Ce script est le fallback batch pour l'analyse rétrospective.

Usage batch (fallback) :
    python3 scripts/pka_memory_nudge.py --transcript <fichier> [--dry-run]
    python3 scripts/pka_memory_nudge.py --stdin [--dry-run]

Règle SOUL.md : section « Memory Nudge — extraction mémoire synchrone »
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path


def extract_from_transcript(text: str, dry_run: bool = False) -> dict:
    """
    Analyse heuristique d'un transcript pour extraction de mémoire.
    En production, cette fonction délègue au LLM.
    Pour le prototype, elle utilise des patterns de détection.
    """
    lines = text.strip().split("\n")
    user_facts = []
    decisions = []
    patterns = []

    # Heuristiques de détection
    decision_keywords = [
        "décidé", "décision", "adopté", "validé", "choisi", "on va", "je vais",
        "decided", "decision", "adopted", "validated", "chosen", "we'll", "i'll",
        "OK pour", "OK pour", "faisons", "go for", "let's"
    ]
    fact_keywords = [
        "JC a", "JCH a", "le setup", "l'IP", "le mot de passe", "la config",
        "j'utilise", "j'ai installé", "mon", "ma", "mes",
        "jc uses", "jch uses", "setup is", "configured"
    ]
    pattern_keywords = [
        "toujours", "chaque fois", "systématiquement", "pattern", "récurrent",
        "always", "every time", "systematically", "recurring", "habit"
    ]

    for i, line in enumerate(lines):
        line_lower = line.lower()
        context = "\n".join(lines[max(0, i - 2):min(len(lines), i + 3)])

        for kw in decision_keywords:
            if kw.lower() in line_lower:
                decisions.append({
                    "line": i + 1,
                    "keyword": kw,
                    "context": context.strip()[:300],
                    "timestamp": datetime.now().isoformat()
                })
                break

        for kw in fact_keywords:
            if kw.lower() in line_lower:
                user_facts.append({
                    "line": i + 1,
                    "keyword": kw,
                    "context": context.strip()[:300],
                    "timestamp": datetime.now().isoformat()
                })
                break

        for kw in pattern_keywords:
            if kw.lower() in line_lower:
                patterns.append({
                    "line": i + 1,
                    "keyword": kw,
                    "context": context.strip()[:300],
                    "timestamp": datetime.now().isoformat()
                })
                break

    result = {
        "metadata": {
            "extractor": "pka_memory_nudge.py",
            "version": "0.1.0",
            "timestamp": datetime.now().isoformat(),
            "dry_run": dry_run,
            "total_lines": len(lines),
            "method": "heuristic (prototype — LLM delegation à venir)"
        },
        "user_facts": user_facts[:10],   # max 10
        "decisions": decisions[:10],
        "patterns": patterns[:5],
        "counts": {
            "user_facts": len(user_facts),
            "decisions": len(decisions),
            "patterns": len(patterns)
        }
    }

    return result


def apply_to_user_md(facts: list, dry_run: bool = False) -> list:
    """Propose des ajouts à USER.md."""
    suggestions = []
    for fact in facts:
        suggestion = f"[MEMORY NUDGE] {fact['context'][:200]}"
        suggestions.append(suggestion)
    return suggestions


def apply_to_memory_md(decisions: list, dry_run: bool = False) -> list:
    """Propose des entrées pour MEMORY.md."""
    suggestions = []
    for decision in decisions:
        suggestion = (
            f"- [{datetime.now().strftime('%Y-%m-%d')}] "
            f"[Memory Nudge] : {decision['context'][:250]}"
        )
        suggestions.append(suggestion)
    return suggestions


def apply_to_team_db(patterns: list, dry_run: bool = False) -> list:
    """Propose des entrées pour team.db (dobby_feedback)."""
    suggestions = []
    for pattern in patterns:
        suggestions.append({
            "table": "dobby_feedback",
            "type": "pattern_emerging",
            "content": pattern['context'][:300],
            "confidence": "low"  # prototype
        })
    return suggestions


def main():
    parser = argparse.ArgumentParser(
        description="pka_memory_nudge — Extraction mémoire post-réponse (Hermes pattern)"
    )
    parser.add_argument(
        "--transcript", "-t",
        help="Chemin vers le fichier transcript à analyser"
    )
    parser.add_argument(
        "--stdin", action="store_true",
        help="Lire le transcript depuis stdin"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Ne pas écrire, seulement afficher ce qui serait fait"
    )
    parser.add_argument(
        "--apply", action="store_true",
        help="Appliquer les suggestions (USER.md, MEMORY.md, team.db)"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Sortie JSON uniquement"
    )
    args = parser.parse_args()

    # Lire le transcript
    if args.stdin:
        text = sys.stdin.read()
    elif args.transcript:
        transcript_path = Path(args.transcript)
        if not transcript_path.exists():
            print(json.dumps({"error": f"Fichier introuvable: {args.transcript}"}))
            sys.exit(1)
        text = transcript_path.read_text(encoding="utf-8")
    else:
        print(json.dumps({"error": "Spécifier --transcript ou --stdin"}))
        sys.exit(1)

    if not text.strip():
        print(json.dumps({"error": "Transcript vide"}))
        sys.exit(1)

    # Extraire
    result = extract_from_transcript(text, dry_run=args.dry_run)

    # Suggestions
    user_suggestions = apply_to_user_md(result["user_facts"], args.dry_run)
    memory_suggestions = apply_to_memory_md(result["decisions"], args.dry_run)
    db_suggestions = apply_to_team_db(result["patterns"], args.dry_run)

    output = {
        **result,
        "suggestions": {
            "user_md": user_suggestions,
            "memory_md": memory_suggestions,
            "team_db": db_suggestions
        }
    }

    if args.json:
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(f"=== pka_memory_nudge v0.1.0 ===\n")
        print(f"Lignes analysées : {result['metadata']['total_lines']}")
        print(f"Faits utilisateur : {result['counts']['user_facts']}")
        print(f"Décisions        : {result['counts']['decisions']}")
        print(f"Patterns         : {result['counts']['patterns']}")
        print(f"\n--- Suggestions USER.md ---")
        for s in user_suggestions:
            print(f"  {s[:120]}...")
        print(f"\n--- Suggestions MEMORY.md ---")
        for s in memory_suggestions:
            print(f"  {s[:120]}...")
        print(f"\n--- Suggestions team.db ---")
        for s in db_suggestions:
            print(f"  table={s['table']} type={s['type']}")

    if args.apply and not args.dry_run:
        # En production : persister via team.db
        print("\n⚠️  --apply : persistance non implémentée (prototype).")
        print("    En production, Dobby appelle ce script puis décide quoi écrire.")


if __name__ == "__main__":
    main()
