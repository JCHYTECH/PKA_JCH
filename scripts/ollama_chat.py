#!/usr/bin/env python3
"""Chat interactif minimal pour Ollama avec system prompt.

Remplace l'usage fragile de `ollama run --system`, non supporte par toutes
les versions du CLI Ollama. Utilise directement l'API locale.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path


OLLAMA_URL = "http://127.0.0.1:11434/api/chat"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Chat interactif Ollama local")
    parser.add_argument("--model", required=True)
    parser.add_argument("--system-file", required=True)
    parser.add_argument("--num-ctx", type=int, default=4096)
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--verbose", action="store_true")
    return parser.parse_args()


def load_text(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def post_chat(payload: dict) -> dict:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        OLLAMA_URL,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=600) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Ollama indisponible: {exc}") from exc


def fmt_ns(value: int | None) -> str:
    if not value:
        return "0 ms"
    ms = value / 1_000_000
    if ms < 1000:
        return f"{ms:.0f} ms"
    return f"{ms / 1000:.2f} s"


def main() -> int:
    args = parse_args()
    system_prompt = load_text(args.system_file)
    messages = [{"role": "system", "content": system_prompt}]

    print("Chat Ollama local")
    print(f"Modele : {args.model}")
    print("Commandes : /bye pour quitter, /reset pour vider l'historique")
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
            print("Historique reinitialise.")
            continue

        messages.append({"role": "user", "content": user_text})
        payload = {
            "model": args.model,
            "messages": messages,
            "stream": False,
            "options": {
                "num_ctx": args.num_ctx,
                "temperature": args.temperature,
            },
        }

        try:
            response = post_chat(payload)
        except RuntimeError as exc:
            print(f"Erreur Ollama: {exc}", file=sys.stderr)
            return 1

        assistant = (response.get("message") or {}).get("content", "").strip()
        if assistant:
            print(f"\nDobby> {assistant}\n")
        else:
            print("\nDobby> [reponse vide]\n")
        messages.append({"role": "assistant", "content": assistant})

        if args.verbose:
            print(
                "timings:"
                f" load={fmt_ns(response.get('load_duration'))}"
                f" prompt={fmt_ns(response.get('prompt_eval_duration'))}"
                f" eval={fmt_ns(response.get('eval_duration'))}"
                f" total={fmt_ns(response.get('total_duration'))}"
            )
            print(
                "tokens:"
                f" prompt={response.get('prompt_eval_count', 0)}"
                f" eval={response.get('eval_count', 0)}"
            )
            print("")


if __name__ == "__main__":
    raise SystemExit(main())
