#!/usr/bin/env python3
"""
argus_batch.py
Forge 🦦 — Lance le pipeline Argus sur un dossier de photos.
Usage : python3 argus_batch.py [--source DOSSIER] [--pause SECONDES]
Résultats : PHOTO/analyses/ + PHOTO/presets/ + TEAM_Inbox/ARTEON_Phase0/rapport_batch.md
"""

import argparse
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path

SOURCE_DEFAULT = Path("/Users/jchavauxm5/Desktop/LrC To /Dobby select")
RUN_ANALYSIS   = Path.home() / ".claude/skills/photo-analyse-wildlife/scripts/run_analysis.py"
TEAM_INBOX     = Path("/Users/jchavauxm5/PKA_JCH/TEAM_Inbox/ARTEON_Phase0")
EXTENSIONS     = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".dng", ".cr2", ".cr3", ".nef"}

BANNER = """
🦅 Argus — Batch ARTEON Phase 0
================================"""


def run_one(image_path: Path, pause: float, bypass_ethics: bool = False) -> dict:
    start = time.time()
    cmd = [sys.executable, str(RUN_ANALYSIS), str(image_path)]
    if bypass_ethics:
        cmd.append("--bypass-ethics")
    result = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = round(time.time() - start, 1)

    if result.returncode == 0:
        lines = result.stdout.strip().splitlines()
        parsed = {}
        for line in lines:
            if ": " in line:
                k, v = line.split(": ", 1)
                parsed[k.strip()] = v.strip()
        return {
            "status": "ok",
            "file": image_path.name,
            "pdf": parsed.get("PDF", "—"),
            "xmp": parsed.get("XMP", "—"),
            "score": parsed.get("SCORE", "—"),
            "espece": parsed.get("ESPECE", "—"),
            "elapsed": elapsed,
        }
    elif result.returncode == 2:
        return {"status": "rejected", "file": image_path.name, "reason": result.stderr.strip(), "elapsed": elapsed}
    elif result.returncode == 3:
        return {"status": "moderation", "file": image_path.name, "reason": result.stderr.strip(), "elapsed": elapsed}
    else:
        return {"status": "error", "file": image_path.name, "reason": result.stderr.strip()[:200], "elapsed": elapsed}


def write_report(results: list, source: Path):
    TEAM_INBOX.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M")
    report_path = TEAM_INBOX / f"{ts}_argus_batch_rapport.md"

    ok       = [r for r in results if r["status"] == "ok"]
    errors   = [r for r in results if r["status"] == "error"]
    rejected = [r for r in results if r["status"] in ("rejected", "moderation")]

    lines = [
        f"# Argus — Rapport Batch ARTEON Phase 0",
        f"",
        f"**Date :** {datetime.now().strftime('%Y-%m-%d %H:%M')}  ",
        f"**Source :** `{source}`  ",
        f"**Total :** {len(results)} photos — ✅ {len(ok)} ok · ❌ {len(errors)} erreurs · 🚫 {len(rejected)} rejetées",
        f"",
        f"---",
        f"",
        f"## ✅ Analyses réussies ({len(ok)})",
        f"",
        f"| Fichier | Espèce | Score | PDF | XMP | Durée |",
        f"|---------|--------|-------|-----|-----|-------|",
    ]
    for r in ok:
        pdf_name = Path(r["pdf"]).name if r["pdf"] != "—" else "—"
        xmp_name = Path(r["xmp"]).name if r["xmp"] != "—" else "—"
        lines.append(f"| {r['file']} | {r['espece']} | {r['score']} | {pdf_name} | {xmp_name} | {r['elapsed']}s |")

    if errors:
        lines += ["", f"## ❌ Erreurs ({len(errors)})", ""]
        for r in errors:
            lines.append(f"- **{r['file']}** — {r.get('reason', '?')}")

    if rejected:
        lines += ["", f"## 🚫 Rejetées ({len(rejected)})", ""]
        for r in rejected:
            lines.append(f"- **{r['file']}** — {r.get('reason', '?')}")

    lines += [
        "",
        "---",
        "",
        f"*Généré par Argus 🦅 via argus_batch.py — PKA ARTEON Phase 0*",
    ]

    report_path.write_text("\n".join(lines))
    return report_path


def main():
    parser = argparse.ArgumentParser(description="Batch Argus — ARTEON Phase 0")
    parser.add_argument("--source", default=str(SOURCE_DEFAULT), help="Dossier source")
    parser.add_argument("--pause", type=float, default=3.0, help="Pause entre photos (s)")
    parser.add_argument("--limit", type=int, default=0, help="Limiter à N photos (0 = toutes)")
    parser.add_argument("--bypass-ethics", action="store_true", help="Sauter le filtre éthique (usage interne JCH uniquement)")
    args = parser.parse_args()

    source = Path(args.source)
    if not source.exists():
        print(f"❌ Dossier introuvable : {source}")
        sys.exit(1)

    images = sorted([f for f in source.iterdir() if f.suffix.lower() in EXTENSIONS])
    if not images:
        print(f"❌ Aucune image trouvée dans {source}")
        sys.exit(1)

    if args.limit > 0:
        images = images[:args.limit]

    print(BANNER)
    print(f"📂 Source  : {source}")
    print(f"📸 Photos  : {len(images)}")
    print(f"⏸  Pause   : {args.pause}s entre chaque")
    print(f"")

    results = []
    for i, img in enumerate(images, 1):
        print(f"[{i:02d}/{len(images)}] {img.name} ...", end=" ", flush=True)
        r = run_one(img, args.pause, bypass_ethics=args.bypass_ethics)
        if r["status"] == "ok":
            print(f"✅ {r['score']} ({r['espece']}) — {r['elapsed']}s")
        elif r["status"] in ("rejected", "moderation"):
            print(f"🚫 {r['status'].upper()}")
        else:
            print(f"❌ ERREUR — {r.get('reason', '')[:80]}")
        results.append(r)
        if i < len(images):
            time.sleep(args.pause)

    report_path = write_report(results, source)

    ok = sum(1 for r in results if r["status"] == "ok")
    print(f"\n{'='*40}")
    print(f"✅ {ok}/{len(results)} photos analysées")
    print(f"📄 Rapport : {report_path}")
    print(f"🖼  PDFs    : /Users/jchavauxm5/PKA_JCH/PHOTO/analyses/")
    print(f"🎨 XMPs    : /Users/jchavauxm5/PKA_JCH/PHOTO/presets/")


if __name__ == "__main__":
    main()
