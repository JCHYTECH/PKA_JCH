#!/usr/bin/env python3
"""
or_route.py — Routeur de modèles OpenRouter (choix auto selon la tâche).

Usage :
  python3 scripts/or_route.py "ta question"          # route auto
  python3 scripts/or_route.py -m <model> "…"          # forcer un modèle
  echo "…" | python3 scripts/or_route.py

Affiche sur stderr : → <catégorie> : <modèle> (<raison>)
Réponse sur stdout. Réutilise claude_openrouter.call().
"""
import sys
from claude_openrouter import call, DEFAULT_MODEL

# (catégorie, mots-clés [minuscules], modèle OpenRouter, raison)
ROUTES = [
    ("image", [
        "génère", "générer", "dessine", "dessiner", "illustre", "illustrer",
        "render", "affiche une image", "image de", "image du", "schéma",
        "dessin", "visuel", "pictogramme", "logo", "affiche",
    ], "google/gemini-nano-banana-2.1", "génération d'image (⚠️ sortie image, pas texte)"),
    ("vision", [
        "regarde cette image", "analyse l'image", "ocr", "décris l'image",
        "que vois-tu", "photo ci-", "capture d'écran", "extrait le texte de",
    ], "openai/gpt-4o", "vision (entrée image)"),
    ("code", [
        "code", "refactor", "bug", "debug", "fonction", "script", "python",
        "sql", "regex", " git ", "api", "html", "css", "test", "compil",
        "déploie", "patch", "commit",
    ], "anthropic/claude-sonnet-4.5", "code / refactoring"),
    ("raisonnement", [
        "math", "logique", "raisonn", "calcule", "algorithme", "prouve",
        "théorème", "énigme", "déduis", "équation", "probabilité",
    ], "deepseek/deepseek-v4-pro", "raisonnement profond"),
    ("chinois", [
        "chinois", "chinese", "中文", "traduis", "traduction", "mandarin",
        "中国", " zh", "cn", "diah", "dixun",
    ], "moonshotai/kimi-k3", "chinois / traduction CN"),
    ("rédaction", [
        "rédig", "redig", "copy", "article", "blog", "écris", "écri",
        "story", "narrat", "marketing", "newsletter", "landing", "titre",
    ], "anthropic/claude-sonnet-4.5", "rédaction longue"),
    ("bulk", [
        "résum", "resum", "extrais", "classif", "liste", "synthè", "bullet",
        "tableau", "organise", "tri", "catalogue", "étiquet", "etiket",
    ], "deepseek/deepseek-v4-flash", "bulk à bas coût"),
]


def route(prompt: str):
    p = prompt.lower()
    for name, kws, model, reason in ROUTES:
        if any(k in p for k in kws):
            return model, name, reason
    return DEFAULT_MODEL, "default", "généraliste pas cher"


def main():
    args = sys.argv[1:]
    model_override = None
    system = None
    while args and args[0].startswith("-"):
        if args[0] in ("-m", "--model"):
            if len(args) < 2:
                sys.stderr.write("❌ --model attend un argument\n")
                sys.exit(1)
            model_override = args[1]
            args = args[2:]
        elif args[0] in ("--system",):
            if len(args) < 2:
                sys.stderr.write("❌ --system attend un argument\n")
                sys.exit(1)
            system = args[1]
            args = args[2:]
        else:
            sys.stderr.write(f"❌ Option inconnue : {args[0]}\n")
            sys.exit(1)

    prompt = " ".join(args) if args else sys.stdin.read()
    if not prompt.strip():
        sys.stderr.write("❌ Prompt vide.\n")
        sys.exit(1)

    if model_override:
        model, name, reason = model_override, "manuel", "forcé par -m"
    else:
        model, name, reason = route(prompt)

    sys.stderr.write(f"→ {name} : {model} ({reason})\n")
    call(model, prompt, system)


if __name__ == "__main__":
    main()
