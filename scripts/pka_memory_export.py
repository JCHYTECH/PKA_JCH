#!/usr/bin/env python3
"""
pka_memory_export.py — Export portable de la mémoire PKA (P4).

Inspiration HyperMemory (2026) : la mémoire comme fichiers JSON atomiques,
échangeables entre agents et runtimes. Chez nous, team.db est la source ;
ce script produit un artefact portable, versionnable et inspectable.

Chaque fait devient un enregistrement atomique :
  {"id", "kind", "content", "provenance", "confidence", "observed_at"}

Usage :
  python3 scripts/pka_memory_export.py                 # export complet
  python3 scripts/pka_memory_export.py --out /tmp/mem.json
  python3 scripts/pka_memory_export.py --kind knowledge --dry-run
  python3 scripts/pka_memory_export.py --stats

Sortie par défaut : _local/persist/pka-memory-export.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

PKA_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PKA_ROOT / "TEAM" / "team.db"
MEMORY_PATH = PKA_ROOT / "MEMORY.md"
DEFAULT_OUT = PKA_ROOT / "_local" / "persist" / "pka-memory-export.json"

SCHEMA_VERSION = 1


def _id(kind: str, content: str) -> str:
    """Identifiant stable : même contenu = même id, donc dédoublonnable."""
    return hashlib.sha256(f"{kind}|{content}".encode()).hexdigest()[:16]


def _rec(kind: str, content: str, provenance: str, confidence: float,
         observed_at: str | None, **extra) -> dict:
    rec = {
        "id": _id(kind, content),
        "kind": kind,
        "content": content.strip()[:2000],
        "provenance": provenance,
        "confidence": round(confidence, 2),
        "observed_at": observed_at or "",
        "schema_version": SCHEMA_VERSION,
    }
    rec.update({k: v for k, v in extra.items() if v})
    return rec


def export_knowledge() -> list[dict]:
    out = []
    try:
        c = sqlite3.connect(DB_PATH)
        c.row_factory = sqlite3.Row
        for r in c.execute(
                "SELECT title, body, type, source, tags, created_at FROM knowledge "
                "WHERE status='active'"):
            out.append(_rec("knowledge",
                            f"{r['title']}\n{r['body'] or ''}",
                            f"team.db:knowledge/{r['source'] or '—'}",
                            0.8, r["created_at"],
                            knowledge_type=r["type"], tags=r["tags"]))
        c.close()
    except sqlite3.Error as exc:
        print(f"[warn] knowledge : {exc}", file=sys.stderr)
    return out


def export_memory_md() -> list[dict]:
    """Chaque entrée datée de MEMORY.md → un fait atomique."""
    out = []
    if not MEMORY_PATH.exists():
        return out
    for line in MEMORY_PATH.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^- \[(\d{4}-\d{2}-\d{2})\]\s*(?:\[([^\]]+)\])?\s*:?\s*(.+)$", line.strip())
        if not m:
            continue
        date, tag, body = m.groups()
        out.append(_rec("memory_entry", body, "MEMORY.md", 0.9, date, tag=tag))
    return out


def export_skills() -> list[dict]:
    out = []
    for f in sorted((PKA_ROOT / "skills").glob("*/SKILL.md")):
        try:
            text = f.read_text(encoding="utf-8")
        except OSError:
            continue
        name = re.search(r"^name:\s*(.+)$", text, re.M)
        desc = re.search(r"^description:\s*(.+)$", text, re.M)
        out.append(_rec("skill_procedure",
                        f"{name.group(1).strip() if name else f.parent.name}: "
                        f"{desc.group(1).strip() if desc else ''}",
                        f"skills/{f.parent.name}/SKILL.md", 0.85, None))
    return out


def export_llm_calls() -> list[dict]:
    """Agrégats de coûts — pas les appels individuels (trop verbeux)."""
    out = []
    try:
        c = sqlite3.connect(DB_PATH)
        for r in c.execute(
                "SELECT COALESCE(project,'—') AS p, model, COUNT(*), "
                "ROUND(SUM(cost_usd),4), COALESCE(SUM(tokens_in+tokens_out),0) "
                "FROM llm_calls GROUP BY p, model"):
            out.append(_rec(
                "llm_cost_aggregate",
                f"{r[0]} / {r[1]} : {r[2]} appels, {r[4]} tokens, ${r[3]}",
                "team.db:llm_calls", 1.0, None))
        c.close()
    except sqlite3.Error:
        pass
    return out


EXPORTERS = {
    "knowledge": export_knowledge,
    "memory": export_memory_md,
    "skills": export_skills,
    "llm": export_llm_calls,
}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--out", default=str(DEFAULT_OUT))
    p.add_argument("--kind", choices=sorted(EXPORTERS), help="Exporter un seul type")
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--stats", action="store_true")
    args = p.parse_args()

    kinds = [args.kind] if args.kind else list(EXPORTERS)
    records: list[dict] = []
    for k in kinds:
        try:
            recs = EXPORTERS[k]()
        except Exception as exc:
            print(f"[warn] {k} : {exc}", file=sys.stderr)
            recs = []
        print(f"  {k:10} {len(recs):>4} fait(s)", file=sys.stderr)
        records.extend(recs)

    # Dédoublonnage par id
    uniq = {r["id"]: r for r in records}

    if args.stats:
        from collections import Counter
        print(f"\nTotal : {len(uniq)} fait(s) uniques (sur {len(records)} bruts)")
        for kind, n in Counter(r["kind"] for r in uniq.values()).most_common():
            print(f"  {kind:22} {n}")
        return 0

    payload = {
        "schema": "pka-memory-portable",
        "schema_version": SCHEMA_VERSION,
        "exported_at": datetime.now().isoformat(timespec="seconds"),
        "source": "TEAM/team.db + MEMORY.md + skills/",
        "count": len(uniq),
        "facts": sorted(uniq.values(), key=lambda r: (r["kind"], r["id"])),
    }

    if args.dry_run:
        print(json.dumps({"count": len(uniq),
                          "kinds": sorted({r['kind'] for r in uniq.values()})},
                         indent=2, ensure_ascii=False))
        return 0

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    size_kb = out.stat().st_size / 1024
    print(f"Export : {len(uniq)} fait(s) → {out} ({size_kb:.0f} Ko)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
