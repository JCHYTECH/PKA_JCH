#!/usr/bin/env python3
"""
claude_openrouter.py — Appel LLM one-shot via OpenRouter (Claude par défaut).

Usage :
  python3 scripts/claude_openrouter.py "ta question"                 # Claude Sonnet (défaut)
  python3 scripts/claude_openrouter.py -m anthropic/claude-opus-4.5 "…"   # modèle précis
  echo "ta question" | python3 scripts/claude_openrouter.py -m deepseek/deepseek-v4-flash

  --system "texte"   : system prompt optionnel
  --list             : liste les modèles anthropic/* disponibles

Clé lue depuis ~/.config/pka-jch/openrouter_key.txt (crédits OpenRouter).
Sortie : la réponse sur stdout ; code retour 0 = OK, 1 = erreur.
"""
import os
import sys
import json
import urllib.request
import urllib.error

KEY_FILE = os.path.expanduser("~/.config/pka-jch/openrouter_key.txt")
BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "anthropic/claude-sonnet-4.5"


def get_key():
    try:
        with open(KEY_FILE) as f:
            return f.read().strip()
    except OSError:
        sys.stderr.write(f"❌ Clé OpenRouter introuvable : {KEY_FILE}\n")
        sys.exit(1)


def call(model, prompt, system=None):
    key = get_key()
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    payload = json.dumps({
        "model": model,
        "messages": messages,
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
        with urllib.request.urlopen(req, timeout=120) as r:
            data = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        sys.stderr.write(f"❌ Erreur OpenRouter {e.code} : {e.read().decode('utf-8', 'replace')[:500]}\n")
        sys.exit(1)
    except urllib.error.URLError as e:
        sys.stderr.write(f"❌ Erreur réseau : {e.reason}\n")
        sys.exit(1)

    try:
        content = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        sys.stderr.write(f"❌ Réponse inattendue : {json.dumps(data)[:500]}\n")
        sys.exit(1)

    print(content)
    # usage éventuel sur stderr (sans polluer stdout)
    usage = data.get("usage")
    if usage and os.environ.get("OR_SHOW_USAGE"):
        sys.stderr.write(f"[usage: {usage.get('total_tokens', '?')} tokens]\n")
    return content


def list_claude_models():
    key = get_key()
    req = urllib.request.Request(
        f"{BASE_URL}/models",
        headers={"Authorization": f"Bearer {key}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read().decode("utf-8"))
    except urllib.error.URLError as e:
        sys.stderr.write(f"❌ Erreur réseau : {e.reason}\n")
        sys.exit(1)
    ids = sorted(m["id"] for m in data.get("data", []))
    for m in ids:
        if "claude" in m or "anthropic" in m:
            print(m)


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        sys.exit(0)
    if args[0] == "--list":
        list_claude_models()
        sys.exit(0)

    model = DEFAULT_MODEL
    system = None
    while args and args[0].startswith("-"):
        if args[0] in ("-m", "--model"):
            if len(args) < 2:
                sys.stderr.write("❌ --model attend un argument\n")
                sys.exit(1)
            model = args[1]
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

    if args:
        prompt = " ".join(args)
    else:
        prompt = sys.stdin.read()

    if not prompt.strip():
        sys.stderr.write("❌ Prompt vide (passe-le en argument ou via stdin).\n")
        sys.exit(1)

    call(model, prompt, system)


if __name__ == "__main__":
    main()
