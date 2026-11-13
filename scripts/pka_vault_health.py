#!/usr/bin/env python3
"""pka_vault_health.py — Score de santé unifié du vault PKA_JCH (0-100).

Cadre : « un bon vault capitalise, il n'accumule pas » — trois piliers d'audit
(forme / fond / recherche), inspiré de l'audit "second brain" et aligné sur les
outils PKA existants (check_state_freshness, pka_memory_eval).

Usage :
    python3 scripts/pka_vault_health.py                # tout (forme + fond + recherche)
    python3 scripts/pka_vault_health.py --json         # sortie machine
    python3 scripts/pka_vault_health.py --skip-search  # forme + fond (rapide)

Piliers :
    FORME     : liens morts + header/TLDR manquant (couche connaissance compilée)
    FOND      : fraîcheur des fichiers State (règle des 7/14 jours)
    RECHERCHE : banc pka_memory_eval (hit@k, MRR, tokens) — 18 questions fixes
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

PKA_ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("PKA_WORKSPACE", str(PKA_ROOT))

# ── Couche "connaissance compilée" scannée pour la forme ─────────────────────
# (le raw — inbox, projets — est volontairement exclu : il est légitimement
#  non lié tant qu'il n'est pas ingéré. On audite la couche qui doit être propre.)
FORM_SCOPES = [
    "wiki", "docs", "TEAM",
    "MEMORY.md", "SOUL.md", "USER.md",
    "AGENTS.md", "CLAUDE.md", "ADAPTER-PROMPT.md",
    "JCH_Inbox/04_PILOTAGE_STRATEGIQUE",
]
FORM_SKIP_DIRS = {"_archive", "backups", "assets", "node_modules", ".git", "Daily"}
# Fichiers racines/d'index — jamais comptés comme orphelins
ORPHAN_WHITELIST = {
    "index.md", "log.md", "INDEX.md", "ROSTER.md", "readme.md",
}

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:[#|][^\]]*)?\]\]")
MDLINK_RE = re.compile(r"\]\(([^)#\s]+(?:\.md)?)(?:#[^)]*)?\)")
HEADING_RE = re.compile(r"^\s*#{1,6}\s*\S")
BLOCKQUOTE_RE = re.compile(r"^\s*>\s*\S")


def _iter_scope_files() -> list[Path]:
    files: list[Path] = []
    for scope in FORM_SCOPES:
        p = PKA_ROOT / scope
        if p.is_file():
            files.append(p)
        elif p.is_dir():
            for f in sorted(p.rglob("*.md")):
                if any(part in FORM_SKIP_DIRS for part in f.parts):
                    continue
                if f.name.lower() == "readme.md" and f.parent == PKA_ROOT:
                    continue
                files.append(f)
    # dédoublonnage (chemins réels, pas symlinks)
    seen: set[Path] = set()
    out: list[Path] = []
    for f in files:
        rp = f.resolve()
        if rp not in seen:
            seen.add(rp)
            out.append(f)
    return out


def _build_known_index(files: list[Path]) -> tuple[set[str], dict[str, Path]]:
    """Index des noms connus (basename sans ext) et des chemins relatifs."""
    names: set[str] = set()
    relpaths: dict[str, Path] = {}
    for f in files:
        names.add(f.stem.lower())
        names.add(f.name.lower())
        rel = f.relative_to(PKA_ROOT)
        relpaths[str(rel).lower()] = f
        relpaths[str(rel).lower().replace(".md", "")] = f
    # compléter avec tous les .md du vault (même hors scope) pour résoudre les liens
    for f in PKA_ROOT.rglob("*.md"):
        if any(part in FORM_SKIP_DIRS | {"_local", "JCH_PRIVATE"} for part in f.parts):
            continue
        names.add(f.stem.lower())
        rel = f.relative_to(PKA_ROOT)
        relpaths[str(rel).lower()] = f
    return names, relpaths


def audit_forme(files: list[Path]) -> dict:
    names, relpaths = _build_known_index(files)
    # index des références sortantes (pour les orphelins, wiki uniquement)
    referenced: set[str] = set()
    wiki_files = [f for f in files if "wiki" in f.parts]

    dead_link_files: list[str] = []
    missing_header_files: list[str] = []
    n_dead_links = 0

    for f in files:
        try:
            text = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        rel = f.relative_to(PKA_ROOT)

        # 1) header/TLDR : après un éventuel frontmatter YAML, un # ou >
        raw_lines = text.splitlines()
        idx = 0
        if raw_lines and raw_lines[0].strip() == "---":
            idx = 1
            while idx < len(raw_lines) and raw_lines[idx].strip() != "---":
                idx += 1
            idx += 1  # passer le --- de fermeture
        body = [ln for ln in raw_lines[idx:idx + 4] if ln.strip()]
        has_header = any(HEADING_RE.match(ln) or BLOCKQUOTE_RE.match(ln)
                         for ln in body)
        if not has_header:
            missing_header_files.append(str(rel))

        # 2) liens morts — on ignore le code (fences + inline) pour éviter
        #    de matcher des exemples documentaires comme ![[images/...]]
        text_links = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
        text_links = re.sub(r"`[^`\n]+`", "", text_links)
        dead = 0
        for m in WIKILINK_RE.finditer(text_links):
            target = m.group(1).strip().lower()
            base = target.split("/")[-1]
            if target in relpaths or base in names:
                continue
            # lien vers un chemin avec extension explicite
            if target.endswith(".md") or "/" in target:
                dead += 1
        for m in MDLINK_RE.finditer(text_links):
            target = m.group(1).strip()
            if not target or target.startswith(("http", "mailto:", "#")):
                continue
            base = target.split("/")[-1].lower()
            # résoudre relatif au dossier du fichier, puis à la racine
            candidates = [f.parent / target, PKA_ROOT / target]
            if not base.endswith(".md"):
                candidates += [f.parent / (target + ".md"), PKA_ROOT / (target + ".md")]
            if not any(c.exists() for c in candidates):
                # wikilink déjà couvert ; ici lien markdown standard
                if target.endswith(".md") or "/" in target:
                    dead += 1
        if dead:
            dead_link_files.append(str(rel))
            n_dead_links += dead

        # 3) références sortantes (pour orphelins)
        if f in wiki_files:
            for m in WIKILINK_RE.finditer(text_links):
                referenced.add(m.group(1).strip().lower().split("/")[-1])
            for m in MDLINK_RE.finditer(text_links):
                t = m.group(1).strip().split("/")[-1].lower()
                if t:
                    referenced.add(t)

    # orphelins : fichiers wiki non référencés (hors index/log/readme)
    orphans: list[str] = []
    for f in wiki_files:
        if f.name.lower() in ORPHAN_WHITELIST:
            continue
        if any(part in {"Daily", "archives"} for part in f.parts):
            continue  # navigation chronologique, pas des nœuds du graphe
        key = f.stem.lower()
        if key not in referenced and f.name.lower() not in referenced:
            orphans.append(str(f.relative_to(PKA_ROOT)))

    total = len(files)
    bad = len(set(dead_link_files) | set(missing_header_files))
    clean = max(0, total - bad)
    score = round(100 * clean / total, 1) if total else 0.0

    return {
        "score": score,
        "files": total,
        "clean": clean,
        "dead_link_files": sorted(set(dead_link_files)),
        "n_dead_links": n_dead_links,
        "missing_header_files": sorted(set(missing_header_files)),
        "orphans": orphans,  # info uniquement — non compté dans le score
    }


def audit_fond() -> dict:
    import check_state_freshness as csf
    results = csf.check_freshness(json_output=True)

    ok = len(results["ok"])
    warn = len(results["warning"])
    crit = len(results["critical"])
    miss = len(results["missing"])
    total = ok + warn + crit + miss
    if total == 0:
        return {"score": 0.0, "ok": 0, "warning": 0, "critical": 0, "missing": 0,
                "total": 0, "stale": []}
    weighted = ok * 1.0 + warn * 0.5 + crit * 0.0 + miss * 0.0
    score = round(100 * weighted / total, 1)
    stale = [e["file"] for e in results["warning"] + results["critical"]]
    return {
        "score": score, "ok": ok, "warning": warn, "critical": crit,
        "missing": miss, "total": total, "stale": stale,
    }


def audit_recherche(timeout: int = 300) -> dict | None:
    """Lance pka_memory_eval --json et agrège hit@k/MRR en score 0-100."""
    cmd = [sys.executable, str(PKA_ROOT / "scripts" / "pka_memory_eval.py"),
           "--json", "--sources", "retrieve"]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return {"error": f"timeout {timeout}s", "score": None}
    if r.returncode != 0 or not r.stdout.strip():
        return {"error": (r.stderr or "no output").strip()[:200], "score": None}
    try:
        report = json.loads(r.stdout)
    except json.JSONDecodeError as exc:
        return {"error": f"JSON invalide: {exc}", "score": None}

    s = report.get("summary", {})
    hit = s.get("hit@k", 0.0)
    mrr = s.get("mrr", 0.0)
    score = round(0.5 * hit + 0.5 * (mrr * 100), 1)
    return {
        "score": score,
        "questions": s.get("questions", 0),
        "hit@k": hit,
        "mrr": mrr,
        "source_match": s.get("source_match"),
        "avg_tokens": s.get("avg_tokens"),
        "avg_latency_ms": s.get("avg_latency_ms"),
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--json", action="store_true")
    p.add_argument("--skip-search", action="store_true")
    p.add_argument("--search-timeout", type=int, default=300)
    args = p.parse_args()

    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    forme = audit_forme(_iter_scope_files())
    fond = audit_fond()
    recherche = None if args.skip_search else audit_recherche(args.search_timeout)

    pillars = [("forme", forme["score"]), ("fond", fond["score"])]
    if recherche and recherche.get("score") is not None:
        pillars.append(("recherche", recherche["score"]))
    global_score = round(sum(v for _, v in pillars) / len(pillars), 1)

    report = {
        "generated": ts,
        "global": global_score,
        "forme": forme,
        "fond": fond,
        "recherche": recherche if recherche else {"skipped": True},
    }

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0

    print(f"PKA Vault Health — {ts}")
    print("─" * 62)
    print(f"FORME      : {forme['score']:>5}  "
          f"({forme['files']} fichiers, {forme['files'] - forme['clean']} avec erreurs)")
    print(f"  liens morts    : {len(forme['dead_link_files'])} fichiers "
          f"({forme['n_dead_links']} liens)")
    print(f"  header manquant: {len(forme['missing_header_files'])} fichiers")
    if forme["orphans"]:
        print(f"  orphelins (info): {len(forme['orphans'])} fichiers wiki")
    print(f"FOND       : {fond['score']:>5}  "
          f"(OK {fond['ok']} / WARN {fond['warning']} / CRIT {fond['critical']} "
          f"/ MISS {fond['missing']})")
    if fond["stale"]:
        for s in fond["stale"][:5]:
            print(f"  périmé : {s}")
    if args.skip_search:
        print("RECHERCHE  :   —    (skip --skip-search)")
    elif recherche and recherche.get("score") is not None:
        print(f"RECHERCHE  : {recherche['score']:>5}  "
              f"({recherche['questions']} questions, hit@5={recherche['hit@k']}%, "
              f"MRR={recherche['mrr']})")
        print(f"  tokens/req : {recherche['avg_tokens']}  "
              f"latence {recherche['avg_latency_ms']} ms")
    else:
        print(f"RECHERCHE  :   —    erreur: {recherche.get('error') if recherche else '?'}")
    print("─" * 62)
    print(f"GLOBAL     : {global_score:>5} / 100")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
