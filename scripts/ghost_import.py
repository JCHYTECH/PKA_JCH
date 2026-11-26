#!/usr/bin/env python3
"""ghost_import.py — Pousse un article markdown comme brouillon Ghost via l'Admin API.

Usage :
  GHOST_ADMIN_KEY="id:secret" python3 scripts/ghost_import.py <fichier.md> [--tag slug]
La clé Admin API se lit depuis GHOST_ADMIN_KEY (jamais dans le repo).
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from urllib import error, request


def make_jwt(api_key: str) -> str:
    """Génère un JWT HS256 Ghost Admin API depuis `id:secret`."""
    key_id, secret_hex = api_key.split(":", 1)
    secret = bytes.fromhex(secret_hex)
    iat = int(time.time())
    header = {"alg": "HS256", "typ": "JWT", "kid": key_id}
    payload = {"iat": iat, "exp": iat + 300, "aud": "/admin/"}

    def enc(obj: dict) -> str:
        raw = json.dumps(obj, separators=(",", ":")).encode()
        return base64.urlsafe_b64encode(raw).rstrip(b"=").decode()

    msg = f"{enc(header)}.{enc(payload)}"
    sig = hmac.new(secret, msg.encode(), hashlib.sha256).digest()
    return f"{msg}.{base64.urlsafe_b64encode(sig).rstrip(b'=').decode()}"


def extract_title(text: str) -> str:
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("# "):
            return s[2:].strip()
    return "Sans titre"


META_LINE_RE = re.compile(r'^\s*\*\*(Date|Statut|Status|Ton|Tone|Publication)\s*:\*\*.*$')


def md_to_html(md_path: Path, *, strip_title: bool) -> str:
    """Convertit le markdown en HTML (pandoc). Ignore le frontmatter YAML,
    le titre H1 (option) et les lignes de métadonnées éditoriales du corps."""
    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    kept = []
    for ln in lines:
        s = ln.strip()
        if strip_title and s.startswith("# "):
            continue
        if META_LINE_RE.match(ln):
            continue
        kept.append(ln)
    text = "\n".join(kept)
    tmp = md_path.with_suffix(".tmp.html.md")
    tmp.write_text(text, encoding="utf-8")
    try:
        r = subprocess.run(
            ["pandoc", str(tmp), "-f", "markdown+yaml_metadata_block", "-t", "html", "--wrap=none"],
            capture_output=True, text=True,
        )
        if r.returncode != 0:
            raise SystemExit(f"pandoc: {r.stderr[:500]}")
        return r.stdout.strip()
    finally:
        tmp.unlink(missing_ok=True)


def create_post(api_url: str, jwt: str, title: str, html: str, tags: list[str]) -> dict:
    body = json.dumps({"posts": [{"title": title, "html": html, "status": "draft", "tags": tags}]}).encode()
    req = request.Request(
        f"{api_url}/ghost/api/admin/posts/",
        data=body,
        headers={"Authorization": f"Ghost {jwt}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read())
    except error.HTTPError as e:
        raise SystemExit(f"HTTP {e.code}: {e.read().decode()[:600]}")


def main() -> int:
    p = argparse.ArgumentParser(description="Pousse un markdown comme brouillon Ghost")
    p.add_argument("file", help="Fichier markdown à importer")
    p.add_argument("--api-url", default="https://wildlens.ghost.io")
    p.add_argument("--tag", action="append", default=[], help="Slug de tag (répétable)")
    p.add_argument("--keep-title-in-body", action="store_true", help="Garder le H1 dans le corps")
    args = p.parse_args()

    api_key = os.environ.get("GHOST_ADMIN_KEY")
    if not api_key:
        raise SystemExit("Clé absente — définir GHOST_ADMIN_KEY (id:secret)")

    md = Path(args.file)
    title = extract_title(md.read_text(encoding="utf-8"))
    html = md_to_html(md, strip_title=not args.keep_title_in_body)
    jwt = make_jwt(api_key)
    data = create_post(args.api_url, jwt, title, html, args.tag)

    posts = data.get("posts", [])
    if posts:
        po = posts[0]
        print(f"✅ brouillon créé : « {po.get('title')} »")
        print(f"   id={po.get('id')}  slug={po.get('slug')}  status={po.get('status')}")
        print(f"   url={po.get('url')}")
    else:
        print("⚠️ réponse sans post :", json.dumps(data)[:400])
    return 0


if __name__ == "__main__":
    sys.exit(main())
