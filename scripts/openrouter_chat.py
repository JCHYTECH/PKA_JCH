#!/usr/bin/env python3
"""openrouter_chat.py — Chat interactif Dobby via OpenRouter (multi-modèles).

Usage :
  python3 scripts/openrouter_chat.py --model openai/gpt-6.1-sol --system-file AGENTS.md
  python3 scripts/openrouter_chat.py --model anthropic/claude-opus-5.5 --system-file AGENTS.md
  python3 scripts/openrouter_chat.py --model moonshotai/kimi-k3.1-pro --system-file AGENTS.md
  python3 scripts/openrouter_chat.py --list   # liste les modèles gpt/claude/kimi

Clé lue depuis ~/.config/pka-jch/openrouter_key.txt.
System prompt (bootstrap Dobby) chargé depuis --system-file (défaut : AGENTS.md).
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

KEY_FILE = os.path.expanduser("~/.config/pka-jch/openrouter_key.txt")
BASE_URL = "https://openrouter.ai/api/v1"
PKA_DIR = Path(__file__).resolve().parents[1]
DEFAULT_SYSTEM_FILE = PKA_DIR / "AGENTS.md"


def get_key() -> str:
    try:
        return Path(KEY_FILE).read_text(encoding="utf-8").strip()
    except OSError:
        sys.stderr.write(f"❌ Clé OpenRouter introuvable : {KEY_FILE}\n")
        sys.exit(1)


def load_system(path: str) -> str:
    p = Path(path)
    if not p.is_absolute():
        p = PKA_DIR / p
    try:
        return p.read_text(encoding="utf-8")
    except OSError as e:
        sys.stderr.write(f"❌ System file illisible : {p} ({e})\n")
        sys.exit(1)


def post_chat(messages: list[dict], model: str, key: str, temperature: float) -> str:
    payload = json.dumps({
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/chat/completions",
        data=payload,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            data = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:600]
        raise RuntimeError(f"HTTP {e.code}: {detail}") from e
    except urllib.error.URLError as e:
        raise RuntimeError(f"Réseau: {e.reason}") from e

    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        raise RuntimeError(f"Réponse inattendue: {json.dumps(data)[:600]}")


def list_models(key: str) -> None:
    req = urllib.request.Request(
        f"{BASE_URL}/models", headers={"Authorization": f"Bearer {key}"}
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.loads(r.read().decode("utf-8"))
    ids = sorted(m["id"] for m in data.get("data", []))
    for m in ids:
        low = m.lower()
        if "gpt" in low or "claude" in low or "kimi" in low:
            print(m)


def main() -> int:
    parser = argparse.ArgumentParser(description="Chat interactif Dobby via OpenRouter")
    parser.add_argument("--model", default="openai/gpt-6.1-sol")
    parser.add_argument("--system-file", default=str(DEFAULT_SYSTEM_FILE))
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--list", action="store_true", help="lister les modèles")
    args = parser.parse_args()

    key = get_key()
    if args.list:
        list_models(key)
        return 0

    system_prompt = load_system(args.system_file)
    messages = [{"role": "system", "content": system_prompt}]

    print("🐶 Dobby — OpenRouter")
    print(f"   Modèle : {args.model}")
    print("Commandes : /bye quitter · /reset vider · /models lister · /model <slug> changer")
    print("")

    while True:
        try:
            user_text = input("JCH> ").strip()
        except EOFError:
            print("")
            return 0
        if not user_text:
            continue
        if user_text in {"/bye", "/exit", "/quit"}:
            return 0
        if user_text == "/reset":
            messages = [{"role": "system", "content": system_prompt}]
            print("Historique réinitialisé.")
            continue
        if user_text == "/models":
            list_models(key)
            continue
        if user_text.startswith("/model"):
            parts = user_text.split()
            if len(parts) >= 2:
                args.model = parts[1]
                print(f"✅ Modèle changé : {args.model}")
            else:
                print("Usage : /model <slug>  (ex: /model anthropic/claude-sonnet-5-5)")
            continue

        messages.append({"role": "user", "content": user_text})
        try:
            assistant = post_chat(messages, args.model, key, args.temperature)
        except RuntimeError as e:
            print(f"❌ Erreur OpenRouter: {e}", file=sys.stderr)
            messages.pop()  # retire le message user raté pour ne pas polluer l'historique
            continue

        assistant = assistant.strip()
        print(f"\nDobby> {assistant}\n")
        messages.append({"role": "assistant", "content": assistant})

    return 0


if __name__ == "__main__":
    raise SystemExit(main())