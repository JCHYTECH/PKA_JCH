#!/usr/bin/env python3
"""
or_image.py — Génération d'image via OpenRouter (Gemini nano-banana par défaut).

Usage :
  python3 scripts/or_image.py "ton prompt" -o sortie.jpg
  python3 scripts/or_image.py -m google/gemini-3-pro-image "…" -o out.png
  echo "prompt" | python3 scripts/or_image.py -o out.png

Clé lue depuis ~/.config/pka-jch/openrouter_key.txt.
L'image générée est écrite dans le fichier de sortie (défaut : tmp/or_image.png).
"""
import os
import re
import sys
import json
import base64
import urllib.request
import urllib.error

KEY_FILE = os.path.expanduser("~/.config/pka-jch/openrouter_key.txt")
BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "google/gemini-nano-banana-2.1"
DEFAULT_OUT = os.path.expanduser("~/PKA_JCH/tmp/or_image.png")


def get_key():
    try:
        with open(KEY_FILE) as f:
            return f.read().strip()
    except OSError:
        sys.stderr.write(f"❌ Clé OpenRouter introuvable : {KEY_FILE}\n")
        sys.exit(1)


def data_uri_decode(uri):
    """'data:image/jpeg;base64,xxx' -> (bytes, 'jpg')"""
    m = re.match(r"data:image/(png|jpeg|jpg|webp);base64,(.+)", uri, re.DOTALL)
    if not m:
        return None, None
    ext = m.group(1)
    if ext == "jpeg":
        ext = "jpg"
    try:
        return base64.b64decode(m.group(2)), ext
    except Exception:
        return None, None


def fetch_bytes(url):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def extract_image(data):
    """Retourne (bytes, ext) ou (None, None)."""
    m = data["choices"][0]["message"]
    # 1) champ images (Gemini nano-banana / gpt-image)
    for im in (m.get("images") or []):
        u = im.get("image_url", {}).get("url", "") if isinstance(im, dict) else ""
        if u.startswith("data:"):
            return data_uri_decode(u)
        if u.startswith("http"):
            b = fetch_bytes(u)
            ext = "jpg" if "jpeg" in u else ("png" if "png" in u else "webp" if "webp" in u else "jpg")
            return b, ext
    # 2) contenu (markdown image / data URI / URL)
    content = m.get("content") or ""
    mm = re.search(r"data:image/[^;]+;base64,([A-Za-z0-9+/=\s]+)", content)
    if mm:
        return data_uri_decode("data:image/jpeg;base64," + mm.group(1).strip())
    mu = re.search(r"https?://[^\s\)\"']+\.(?:png|jpe?g|webp)", content)
    if mu:
        u = mu.group(0)
        b = fetch_bytes(u)
        ext = "jpg" if "jpeg" in u else ("png" if "png" in u else "webp")
        return b, ext
    return None, None


def main():
    args = sys.argv[1:]
    model = DEFAULT_MODEL
    out = DEFAULT_OUT
    prompt_parts = []
    i = 0
    while i < len(args):
        a = args[i]
        if a in ("-m", "--model"):
            model = args[i + 1]; i += 2; continue
        if a in ("-o", "--output"):
            out = args[i + 1]; i += 2; continue
        prompt_parts.append(a); i += 1
    prompt = " ".join(prompt_parts).strip() or sys.stdin.read().strip()
    if not prompt:
        sys.stderr.write("❌ Prompt vide.\n")
        sys.exit(1)

    key = get_key()
    payload = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}/chat/completions",
        data=payload,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    sys.stderr.write(f"🎨 {model} — génération en cours…\n")
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            data = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        sys.stderr.write(f"❌ Erreur OpenRouter {e.code} : {e.read().decode('utf-8', 'replace')[:400]}\n")
        sys.exit(1)
    except urllib.error.URLError as e:
        sys.stderr.write(f"❌ Erreur réseau : {e.reason}\n")
        sys.exit(1)

    if "choices" not in data or not data["choices"]:
        sys.stderr.write(f"❌ Réponse inattendue : {json.dumps(data)[:400]}\n")
        sys.exit(1)

    b, ext = extract_image(data)
    if not b:
        sys.stderr.write(f"❌ Pas d'image trouvée dans la réponse : {json.dumps(data)[:400]}\n")
        sys.exit(1)

    # ajuste l'extension du fichier si le prompt ne l'a pas précisée
    if not out.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
        out += "." + (ext or "jpg")
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "wb") as f:
        f.write(b)
    usage = data.get("usage", {})
    cost = usage.get("cost", "?")
    sys.stderr.write(f"✅ Image écrite : {out} ({len(b)} octets · coût ~${cost})\n")
    print(out)


if __name__ == "__main__":
    main()
