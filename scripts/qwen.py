#!/usr/bin/env python3
"""Qwen 3.7 Plus/Max via OpenRouter for PKA_JCH."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pka_bootstrap import ROOT_DIR, render_bootstrap_context  # noqa: E402

KEY_FILE = Path("~/.config/pka-jch/openrouter_key.txt").expanduser()
API_URL = "https://openrouter.ai/api/v1/chat/completions"

MODELS = {
    "plus": "qwen/qwen3.7-plus",
    "max": "qwen/qwen3.7-max",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="qwen",
        description="Qwen 3.7 via OpenRouter. Default: Plus. Use `qwen max ...` for Max.",
    )
    parser.add_argument(
        "args",
        nargs="*",
        help='Prompt words, optionally prefixed by "plus" or "max".',
    )
    parser.add_argument(
        "-m",
        "--model",
        choices=sorted(MODELS),
        default=None,
        help="Model alias to use.",
    )
    parser.add_argument(
        "--raw",
        action="store_true",
        help="Do not include the PKA/Qwen system pointer.",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=4096,
        help="Maximum output tokens.",
    )
    return parser.parse_intermixed_args()


def load_key() -> str:
    if not KEY_FILE.exists():
        raise SystemExit(f"OpenRouter key not found: {KEY_FILE}")
    key = KEY_FILE.read_text(encoding="utf-8").strip()
    if not key:
        raise SystemExit(f"OpenRouter key is empty: {KEY_FILE}")
    return key


def load_system_prompt(model: str) -> str:
    bootstrap_context = render_bootstrap_context()
    return f"""You are running inside the local `qwen` CLI wrapper for PKA_JCH.

Important runtime constraint:
- Current OpenRouter model id: `{model}`.
- When an activation confirmation asks for MODEL, use the exact current model id above.
- You are a plain chat-completions model call through OpenRouter.
- You do not have filesystem, shell, browser, or tool access in this runtime.
- The wrapper has already loaded the consolidated bootstrap context (ADAPTER-PROMPT.md,
  SOUL.md, USER.md, TEAM/dobby.md, TEAM/ROSTER.md, State files, TTD.md, MEMORY.md,
  daily notes, project scans, inbox scans) via scripts/pka_bootstrap.py.
- Do not ask JCH to paste any of those files.
- If a task needs live filesystem/tool execution, say briefly that Codex/Dobby with tools should run it.
- Otherwise answer directly as [[Dobby]] using the loaded context.

{bootstrap_context}
"""


def resolve_model_and_prompt(args: argparse.Namespace) -> tuple[str, str]:
    words = list(args.args)
    alias = args.model or "plus"
    if words and words[0].lower() in MODELS:
        alias = words.pop(0).lower()
    return MODELS[alias], " ".join(words).strip()


def request_chat(messages: list[dict[str, str]], key: str, model: str, max_tokens: int) -> str:
    payload = json.dumps(
        {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens,
            "stream": False,
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {body[:1000]}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Network error: {exc.reason}") from exc

    if "error" in data:
        message = data["error"].get("message", data["error"])
        raise RuntimeError(str(message))
    return data["choices"][0]["message"]["content"]


def build_messages(raw: bool, model: str) -> list[dict[str, str]]:
    if raw:
        return []
    return [{"role": "system", "content": load_system_prompt(model)}]


def run_once(prompt: str, key: str, model: str, raw: bool, max_tokens: int) -> None:
    messages = build_messages(raw, model)
    messages.append({"role": "user", "content": prompt})
    print(request_chat(messages, key, model, max_tokens).strip())


def run_interactive(key: str, model: str, raw: bool, max_tokens: int) -> None:
    messages = build_messages(raw, model)
    print(f"Qwen ({model}) | Entrée vide ou /q pour quitter\n")
    while True:
        try:
            prompt = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return
        if not prompt or prompt in {"/q", "/quit", "exit"}:
            return
        messages.append({"role": "user", "content": prompt})
        try:
            reply = request_chat(messages, key, model, max_tokens).strip()
        except RuntimeError as exc:
            messages.pop()
            print(f"Erreur: {exc}", file=sys.stderr)
            continue
        messages.append({"role": "assistant", "content": reply})
        print(f"\n{reply}\n")


def main() -> int:
    args = parse_args()
    key = load_key()
    model, prompt = resolve_model_and_prompt(args)

    try:
        if prompt:
            run_once(prompt, key, model, args.raw, args.max_tokens)
        else:
            run_interactive(key, model, args.raw, args.max_tokens)
    except RuntimeError as exc:
        print(f"Erreur: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
