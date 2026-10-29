#!/usr/bin/env python3
"""Estimer la consommation de tokens d'une session.

Usage:
    python scripts/pka_token_tracker.py --input-chars 45000 --output-chars 8000 --model deepseek-v4

Ou après une session :
    echo "input_tokens=45000 output_tokens=8000" | python scripts/pka_token_tracker.py --parse
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# Approximate char-to-token ratios per model family
RATIOS = {
    "claude": 3.5,      # ~3.5 chars per token (Claude)
    "deepseek": 4.0,    # ~4 chars per token (DeepSeek)
    "gemini": 4.0,      # ~4 chars per token (Gemini)
    "gpt": 4.0,         # ~4 chars per token (GPT)
    "qwen": 4.0,        # ~4 chars per token (Qwen)
}

# Approximate cost per 1M input tokens (USD)
COST_PER_M_IN = {
    "claude-sonnet-4": 3.0,
    "claude-opus-4": 15.0,
    "deepseek-v4": 2.0,
    "deepseek-r1": 7.0,
    "gemini-2.5-pro": 1.25,
    "gpt-5": 10.0,
    "qwen3.7-plus": 1.0,
    "qwen3.7-max": 4.0,
}

COST_PER_M_OUT = {
    "claude-sonnet-4": 15.0,
    "claude-opus-4": 75.0,
    "deepseek-v4": 8.0,
    "deepseek-r1": 28.0,
    "gemini-2.5-pro": 10.0,
    "gpt-5": 40.0,
    "qwen3.7-plus": 4.0,
    "qwen3.7-max": 16.0,
}


def detect_model(text: str) -> str:
    text = text.lower()
    if "deepseek" in text:
        if "r1" in text:
            return "deepseek-r1"
        return "deepseek-v4"
    if "gemini" in text:
        return "gemini-2.5-pro"
    if "gpt" in text or "chatgpt" in text:
        return "gpt-5"
    if "qwen" in text:
        if "max" in text:
            return "qwen3.7-max"
        return "qwen3.7-plus"
    if "opus" in text:
        return "claude-opus-4"
    return "claude-sonnet-4"


def estimate(input_chars: int = 0, output_chars: int = 0,
             model: str | None = None, summary: bool = True) -> dict:
    ratio = RATIOS.get("deepseek", 4.0)
    model_key = detect_model(model) if model else "deepseek-v4"

    input_tokens = int(input_chars / ratio)
    output_tokens = int(output_chars / ratio)
    total_tokens = input_tokens + output_tokens

    cost_in = (input_tokens / 1_000_000) * COST_PER_M_IN.get(model_key, 2.0)
    cost_out = (output_tokens / 1_000_000) * COST_PER_M_OUT.get(model_key, 8.0)
    total_cost = cost_in + cost_out

    result = {
        "model": model_key,
        "ratio_chars_per_token": ratio,
        "input_chars": input_chars,
        "output_chars": output_chars,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "cost_input_usd": round(cost_in, 6),
        "cost_output_usd": round(cost_out, 6),
        "total_cost_usd": round(total_cost, 6),
    }

    if summary:
        print(f"[{model_key}] {input_tokens:,} in + {output_tokens:,} out = {total_tokens:,} tokens")
        print(f"  Cost: ${total_cost:.4f} ({cost_in:.4f} in + {cost_out:.4f} out)")

    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Estimer consommation tokens d'une session")
    parser.add_argument("--input-chars", type=int, default=0, help="Caractères en input")
    parser.add_argument("--output-chars", type=int, default=0, help="Caractères en output")
    parser.add_argument("--model", type=str, default=None, help="Modèle (deepseek-v4, claude-sonnet-4, ...)")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--parse", action="store_true", help="Parse input_tokens=N output_tokens=N from stdin")
    args = parser.parse_args()

    if args.parse:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            parts = {}
            for pair in line.split():
                if "=" in pair:
                    k, v = pair.split("=", 1)
                    parts[k] = v
            ic = int(parts.get("input_tokens", parts.get("input_chars", "0")))
            oc = int(parts.get("output_tokens", parts.get("output_chars", "0")))
            model = parts.get("model", args.model)
            result = estimate(ic, oc, model, summary=not args.json)
            if args.json:
                print(json.dumps(result, indent=2))
    else:
        result = estimate(args.input_chars, args.output_chars, args.model, summary=not args.json)
        if args.json:
            print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
