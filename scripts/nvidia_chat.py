#!/usr/bin/env python3
"""Chat interactif terminal — Nvidia via OpenRouter, initialisé avec le contexte PKA."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from model_client import get_client, get_model


def _load_system_prompt() -> str:
    parts = []
    for fname in ("ADAPTER-PROMPT.md", "MEMORY.md"):
        f = ROOT / fname
        if f.exists():
            parts.append(f"# {fname}\n\n{f.read_text(encoding='utf-8')}")
    return "\n\n---\n\n".join(parts)


MODEL = get_model("nvidia")
client = get_client("nvidia")
SYSTEM = _load_system_prompt()
messages = [{"role": "system", "content": SYSTEM}]

print(f"Nvidia Chat — {MODEL}")
print(f"Contexte chargé : ADAPTER-PROMPT.md + MEMORY.md ({len(SYSTEM)} chars)")
print("Commandes : /bye pour quitter, /reset pour vider l'historique\n")

while True:
    try:
        user_text = input("JCH> ").strip()
    except (EOFError, KeyboardInterrupt):
        print("")
        break

    if not user_text:
        continue
    if user_text in {"/bye", "/exit", "/quit"}:
        break
    if user_text == "/reset":
        messages = [{"role": "system", "content": SYSTEM}]
        print("Historique réinitialisé.\n")
        continue

    messages.append({"role": "user", "content": user_text})

    try:
        resp = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            max_tokens=4096,
        )
        answer = resp.choices[0].message.content.strip()
    except Exception as exc:
        print(f"Erreur : {exc}\n", file=sys.stderr)
        messages.pop()
        continue

    print(f"\nNvidia> {answer}\n")
    messages.append({"role": "assistant", "content": answer})
