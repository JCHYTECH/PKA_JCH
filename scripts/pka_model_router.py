#!/usr/bin/env python3
"""
pka_model_router.py — Routeur de modèles PKA (interrogeable)

Lit `docs/system/models-routing.json` et répond à « quel modèle pour quelle tâche ».

Usage :
  python3 scripts/pka_model_router.py "rédiger un article photo nature"
  python3 scripts/pka_model_router.py --task redaction-editoriale
  python3 scripts/pka_model_router.py --model claude-sonnet
  python3 scripts/pka_model_router.py --list          # tous les modèles
  python3 scripts/pka_model_router.py --tasks         # toutes les règles de routage

Le modèle est interchangeable : ce routeur ne choisit que la *référence* (modèle +
provider + fallback). Il n'appelle aucune API — c'est la couche de décision du harnais.
"""
import argparse
import json
import os
import sys
import unicodedata


SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROUTING_PATH = os.path.join(SCRIPT_DIR, "..", "docs", "system", "models-routing.json")


def load():
    with open(ROUTING_PATH, encoding="utf-8") as f:
        return json.load(f)


def normalize(s: str) -> str:
    """Minuscules, sans accents, pour un matching tolérant."""
    s = s.lower()
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return s


def find_model(data, model_id):
    for m in data["models"]:
        if m["id"] == model_id:
            return m
    return None


def describe(data, model_id):
    m = find_model(data, model_id)
    if not m:
        return None
    p = data["providers"].get(m["provider"], {})
    loc = "local" if p.get("kind") == "local" else "cloud"
    host = p.get("host", "")
    return {
        "id": m["id"],
        "provider": m["provider"],
        "location": loc,
        "host": host,
        "role": m["role"],
        "ctx": m["ctx"],
        "usage": m["usage"],
    }


def route(data, text):
    """Score chaque règle par mots-clés présents, retourne le meilleur match."""
    t = normalize(text)
    best = None
    best_score = 0
    for rule in data["routing"]:
        score = 0
        matched = []
        for kw in rule["keywords"]:
            if normalize(kw) in t:
                score += 1
                matched.append(kw)
        if score > best_score:
            best_score = score
            best = (rule, matched)
    if not best:
        return None, [], data["routing_default"]
    rule, matched = best
    return rule, matched, None


def main():
    ap = argparse.ArgumentParser(description="Routeur de modèles PKA")
    ap.add_argument("query", nargs="?", help="Description libre de la tâche")
    ap.add_argument("--task", help="Identifiant de règle (ex: redaction-editoriale)")
    ap.add_argument("--model", help="Détail d'un modèle (id)")
    ap.add_argument("--list", action="store_true", help="Lister tous les modèles")
    ap.add_argument("--tasks", action="store_true", help="Lister les règles de routage")
    args = ap.parse_args()

    data = load()

    if args.list:
        print("=== Modèles PKA ===")
        for m in data["models"]:
            loc = "local" if data["providers"][m["provider"]]["kind"] == "local" else "cloud"
            print(f"  {m['id']:<24} [{loc:5}] {m['usage']}")
        return

    if args.tasks:
        print("=== Règles de routage ===")
        for r in data["routing"]:
            fb = ", ".join(r["fallback"]) if r["fallback"] else "—"
            print(f"  {r['task']:<24} → {r['primary']}  (fallback: {fb})")
        return

    if args.model:
        d = describe(data, args.model)
        if not d:
            print(f"❌ Modèle inconnu : {args.model}")
            sys.exit(1)
        print(f"=== {d['id']} ===")
        host_suffix = f", {d['host']}" if d["host"] else ""
        print(f"  Provider : {d['provider']} ({d['location']}{host_suffix})")
        print(f"  Rôle     : {d['role']}")
        print(f"  Contexte : {d['ctx']}")
        print(f"  Usage    : {d['usage']}")
        return

    if args.task:
        rule = next((r for r in data["routing"] if r["task"] == args.task), None)
        if not rule:
            print(f"❌ Règle inconnue : {args.task}")
            print("Règles dispo : " + ", ".join(r["task"] for r in data["routing"]))
            sys.exit(1)
        primary = describe(data, rule["primary"])
        fbs = [describe(data, x) for x in rule["fallback"]]
        print(f"=== Routage — {rule['task']} ===")
        print(f"  Note     : {rule['note']}")
        print(f"  Primaire : {rule['primary']}  ({primary['provider']}, {primary['location']})")
        for f in fbs:
            print(f"  Fallback : {f['id']}  ({f['provider']}, {f['location']})")
        return

    if not args.query:
        ap.print_help()
        return

    rule, matched, default = route(data, args.query)
    if rule:
        primary = describe(data, rule["primary"])
        fbs = [describe(data, x) for x in rule["fallback"]]
        print(f"=== Routage — « {args.query} » ===")
        print(f"  Règle    : {rule['task']}  (mots-clés: {', '.join(matched)})")
        print(f"  Note     : {rule['note']}")
        print(f"  Primaire : {rule['primary']}  ({primary['provider']}, {primary['location']})")
        for f in fbs:
            print(f"  Fallback : {f['id']}  ({f['provider']}, {f['location']})")
    else:
        primary = describe(data, default["primary"])
        print(f"=== Routage — « {args.query} » ===")
        print("  Aucune règle correspondante → défaut")
        print(f"  Primaire : {default['primary']}  ({primary['provider']}, {primary['location']})")
        for f in default["fallback"]:
            d = describe(data, f)
            print(f"  Fallback : {f}  ({d['provider']}, {d['location']})")


if __name__ == "__main__":
    main()
