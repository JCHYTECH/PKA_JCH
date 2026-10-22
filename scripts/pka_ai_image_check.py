#!/usr/bin/env python3
"""
pka_ai_image_check.py — Détection d'images générées par IA (3 niveaux).

Répond à la question « cette photo est-elle (en tout ou partie) générée par IA ? »
par un FAISCEAU D'INDICES, jamais par une certitude. Le niveau de confiance de
chaque signal est explicite dans le rapport.

Niveau 1 — PROVENANCE (déterministe)
    C2PA / Content Credentials + EXIF (Software, Make, Model, XMP).
    Fiable à 100 % quand un manifeste signé est présent.
    Absence de manifeste ≠ image réelle (ni Midjourney ni un screenshot n'en ont).

Niveau 2 — GLOBAL (statistique)
    Classifieur ViT (capcheck/ai-image-detection) → probabilité Real/Fake.

Niveau 3 — LOCAL (localisation)
    Découpage en patchs + score individuel → met en évidence les zones
    synthétiques (inpainting, extension, objet ajouté).

Usage :
    python3 scripts/pka_ai_image_check.py photo.jpg
    python3 scripts/pka_ai_image_check.py photo.jpg --json
    python3 scripts/pka_ai_image_check.py dossier/ --report rapport.md
    python3 scripts/pka_ai_image_check.py photo.jpg --no-local     # plus rapide

Avertissement : aucun détecteur n'est parfait. Les générateurs évoluent plus vite
que les détecteurs. Un score élevé est un signal, pas une preuve.

⚠️ RAPPEL (décision JCH 2026-10-22) : usage niveau 1 uniquement. Dès que cet
outil est utilisé en conditions réelles, rappeler à JCH qu'on doit creuser la
piste « entraîner un détecteur sur SES propres photos » — c'est la seule voie
qui répondra à la question de la détection PARTIELLE, les modèles publics
étant mesurés inutilisables (12/12 vraies photos classées IA).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime
from pathlib import Path

PKA_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REPORT_DIR = PKA_ROOT / "JCH_Inbox" / "03_PROJECTS" / "05_PHOTO_AI_JURY" / "ai-checks"

MODEL_NAME = "capcheck/ai-image-detection"
EXTS = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff", ".bmp"}

# Marqueurs FORTS : génération d'image par IA (verdict « IA probable »).
AI_GENERATION_MARKERS = [
    "dall-e", "dalle", "midjourney", "stable diffusion", "stablediffusion",
    "firefly", "generative fill", "inpainting", "img2img", "outpainting",
    "comfyui", "automatic1111", "imagen 3", "flux.1", "sdxl",
    "nano banana", "synthid", "trainedalgorithmicmedia",
]

# Marqueurs FAIBLES : outils de retouche (peuvent contenir de l'IA, souvent pas).
# « photoshop » seul ne prouve RIEN — une photo de terrain passe par Camera Raw.
EDIT_MARKERS = ["photoshop", "affinity photo", "gimp", "lightroom", "dxo", "capture one"]

_pipeline = None


def get_pipeline():
    """Charge le modèle une seule fois (lent au premier appel)."""
    global _pipeline
    if _pipeline is None:
        from transformers import pipeline
        _pipeline = pipeline("image-classification", model=MODEL_NAME)
    return _pipeline


# ── Niveau 1 : provenance ────────────────────────────────────────────────────
def check_provenance(path: Path) -> dict:
    """EXIF + XMP + C2PA. Retourne un dict de signaux."""
    out = {"signals": [], "ai_markers": [], "c2pa": None, "summary": ""}

    # C2PA (optionnel — dépend de c2pa-python)
    try:
        import c2pa  # type: ignore
        try:
            with open(path, "rb") as fh:
                reader = c2pa.Reader(fh, format=path.suffix.lstrip("."))
                manifest = json.loads(reader.json())
            out["c2pa"] = manifest
            out["signals"].append("C2PA : manifeste de provenance présent")
            blob = json.dumps(manifest).lower()
            if any(m in blob for m in ("trainedalgorithmicmedia", "generative", "ai")):
                out["ai_markers"].append("C2PA : action « trained algorithmique » détectée")
        except Exception as exc:  # manifeste absent ou invalide
            out["signals"].append(f"C2PA : pas de manifeste lisible ({type(exc).__name__})")
    except ImportError:
        out["signals"].append("C2PA : module `c2pa` non installé (pip install c2pa-python)")

    # EXIF / XMP
    try:
        from PIL import Image
        from PIL.ExifTags import TAGS
        with Image.open(path) as img:
            exif = img.getexif()
            fields = {}
            for tag_id, value in exif.items():
                name = TAGS.get(tag_id, str(tag_id))
                if isinstance(value, (str, int, float)):
                    fields[name] = str(value)[:200]
            out["exif"] = {k: fields[k] for k in
                           ("Make", "Model", "Software", "Artist", "DateTime")
                           if k in fields}

            # XMP peut vivre dans les info dict
            xmp = img.info.get("xmp") or img.info.get("XML:com.adobe.xmp") or b""
            if isinstance(xmp, bytes):
                xmp = xmp.decode("utf-8", errors="ignore")
            haystack = (json.dumps(out["exif"]) + " " + str(xmp)).lower()

            for marker in AI_GENERATION_MARKERS:
                if marker in haystack:
                    out["ai_markers"].append(f"génération IA déclarée : « {marker} »")
            for marker in EDIT_MARKERS:
                if marker in haystack:
                    out.setdefault("edit_markers", []).append(marker)

            # Cohérence appareil photo
            if out["exif"].get("Make") or out["exif"].get("Model"):
                out["signals"].append(
                    f"EXIF appareil : {out['exif'].get('Make','?')} {out['exif'].get('Model','')}".strip())
            else:
                out["signals"].append("EXIF : aucun appareil photo déclaré")
    except Exception as exc:
        out["signals"].append(f"EXIF illisible : {type(exc).__name__}")

    if out["ai_markers"]:
        out["summary"] = f"{len(out['ai_markers'])} marqueur(s) de génération IA"
    elif out.get("edit_markers"):
        out["summary"] = f"retouche : {', '.join(out['edit_markers'][:3])} (ne prouve pas de génération)"
    elif out["c2pa"]:
        out["summary"] = "manifeste C2PA présent — voir détail"
    else:
        out["summary"] = "aucun signal de provenance IA (absence de preuve ≠ preuve)"
    return out


# ── Niveau 2 : score global ──────────────────────────────────────────────────
def score_global(path: Path) -> dict:
    from PIL import Image
    clf = get_pipeline()
    with Image.open(path) as img:
        img = img.convert("RGB")
        results = clf(img)
    by_label = {r["label"].upper(): r["score"] for r in results}
    fake = by_label.get("FAKE", by_label.get("AI", 0.0))
    real = by_label.get("REAL", by_label.get("HUMAN", 0.0))
    verdict = "suspecte" if fake >= 0.5 else "cohérente avec une photo"
    return {"fake_score": round(fake, 4), "real_score": round(real, 4),
            "verdict": verdict, "labels": {k: round(v, 4) for k, v in by_label.items()}}


# ── Niveau 3 : localisation ─────────────────────────────────────────────────
def score_local(path: Path, grid: int = 3, overlap: float = 0.15) -> dict:
    """Découpe en grid×grid patchs (+ chevauchement) et score chacun."""
    from PIL import Image
    clf = get_pipeline()
    with Image.open(path) as img:
        img = img.convert("RGB")
        w, h = img.size
        # Réduire les très grandes images pour rester rapide
        max_side = 1600
        if max(w, h) > max_side:
            ratio = max_side / max(w, h)
            img = img.resize((int(w * ratio), int(h * ratio)))
            w, h = img.size

        pw, ph = w // grid, h // grid
        if pw < 64 or ph < 64:
            return {"patches": [], "note": "image trop petite pour la localisation"}

        patches = []
        for gy in range(grid):
            for gx in range(grid):
                x0 = max(0, int(gx * pw - pw * overlap))
                y0 = max(0, int(gy * ph - ph * overlap))
                x1 = min(w, int((gx + 1) * pw + pw * overlap))
                y1 = min(h, int((gy + 1) * ph + ph * overlap))
                crop = img.crop((x0, y0, x1, y1))
                res = clf(crop)
                fake = next((r["score"] for r in res
                             if r["label"].upper() in ("FAKE", "AI")), 0.0)
                patches.append({
                    "cell": f"{gx},{gy}",
                    "box": [x0, y0, x1, y1],
                    "fake_score": round(fake, 4),
                })

    patches.sort(key=lambda p: -p["fake_score"])
    flagged = [p for p in patches if p["fake_score"] >= 0.5]
    return {
        "grid": grid,
        "patches": patches,
        "flagged_count": len(flagged),
        "flagged": flagged[:5],
        "top": patches[0] if patches else None,
        "spread": round(sum(p["fake_score"] for p in patches) / max(len(patches), 1), 4),
    }


# ── Agrégation ──────────────────────────────────────────────────────────────
def analyze(path: Path, do_local: bool = True, grid: int = 3,
            use_model: bool = False) -> dict:
    prov = check_provenance(path)

    glob_ = {"skipped": "classifieur désactivé (fiabilité insuffisante, cf. README)"}
    if use_model:
        try:
            glob_ = score_global(path)
        except Exception as exc:
            glob_ = {"error": f"{type(exc).__name__}: {exc}"}

    local = None
    if do_local and use_model:
        try:
            local = score_local(path, grid=grid)
        except Exception as exc:
            local = {"error": f"{type(exc).__name__}: {exc}"}

    # Synthèse : on combine les signaux, sans jamais prétendre à la certitude
    reasons = []
    verdict, confidence = "indéterminée", "faible"

    if prov.get("ai_markers"):
        verdict, confidence = "IA probable", "forte"
        reasons.extend(prov["ai_markers"][:3])
    if isinstance(glob_, dict) and "fake_score" in glob_:
        if glob_["fake_score"] >= 0.85:
            reasons.append(f"classifieur global : {glob_['fake_score']:.0%} IA")
            if verdict == "indéterminée":
                verdict, confidence = "IA probable", "moyenne"
            elif confidence == "forte":
                confidence = "très forte"
        elif glob_["fake_score"] <= 0.15:
            reasons.append(f"classifieur global : {glob_['real_score']:.0%} réel")
            if verdict == "indéterminée":
                verdict = "cohérente avec une photo"
    if local and local.get("flagged_count"):
        reasons.append(
            f"{local['flagged_count']} région(s) sur {len(local['patches'])} "
            f"avec score IA ≥ 50 % (synthèse locale possible)")
        if verdict == "cohérente avec une photo":
            verdict = "partiellement suspecte"
        elif verdict == "indéterminée":
            verdict, confidence = "partiellement suspecte", "moyenne"

    return {
        "file": str(path),
        "name": path.name,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest()[:16],
        "checked_at": datetime.now().isoformat(timespec="seconds"),
        "verdict": verdict,
        "confidence": confidence,
        "reasons": reasons,
        "provenance": prov,
        "global": glob_,
        "local": local,
    }


def render_md(report: dict, out: Path) -> None:
    """Écrit un rapport markdown lisible."""
    lines = [
        f"# AI Image Check — {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "> **Avertissement** : faisceau d'indices, jamais une preuve. "
        "Les détecteurs sont en course contre les générateurs.",
        "",
    ]
    for r in report["results"]:
        if "error" in r:
            lines.append(f"## {r['name']} — ERREUR\n\n{r['error']}\n")
            continue
        lines.append(f"## {r['name']} — **{r['verdict']}** (confiance {r['confidence']})")
        lines.append(f"- SHA-256 : `{r['sha256']}` · {r['checked_at']}")
        if r["reasons"]:
            lines.append("- Signaux :")
            for reason in r["reasons"]:
                lines.append(f"  - {reason}")
        if r["provenance"].get("exif"):
            ex = ", ".join(f"{k}={v}" for k, v in r["provenance"]["exif"].items())
            lines.append(f"- EXIF : {ex}")
        g = r.get("global") or {}
        if "fake_score" in g:
            lines.append(f"- Global : IA {g['fake_score']:.1%} / réel {g['real_score']:.1%}")
        loc = r.get("local") or {}
        if loc.get("patches"):
            lines.append(f"- Local ({loc['grid']}×{loc['grid']}) : "
                         f"{loc['flagged_count']} région(s) ≥ 50 %")
            for p in loc.get("flagged", [])[:3]:
                lines.append(f"  - cellule {p['cell']} → {p['fake_score']:.0%} "
                             f"(box {p['box']})")
        lines.append("")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("target", help="Image ou dossier")
    p.add_argument("--json", action="store_true")
    p.add_argument("--no-local", action="store_true", help="Sauter la localisation (rapide)")
    p.add_argument("--with-model", action="store_true",
                   help="Activer le classifieur ViT (DÉCONSEILLÉ — voir le README)")
    p.add_argument("--benchmark", action="store_true",
                   help="Comparer les modèles sur un jeu de référence")
    p.add_argument("--grid", type=int, default=3, help="Découpage NxN (défaut 3)")
    p.add_argument("--report", help="Écrire un rapport markdown à ce chemin")
    args = p.parse_args()

    target = Path(args.target)
    if not target.exists():
        print(f"Introuvable : {target}", file=sys.stderr)
        return 1

    files = ([target] if target.is_file()
             else sorted(f for f in target.rglob("*") if f.suffix.lower() in EXTS))
    if not files:
        print("Aucune image trouvée.", file=sys.stderr)
        return 1

    # Le classifieur ViT est DÉSACTIVÉ par défaut : validation du 2026-10-22
    # sur 12 photos réelles (dashcam/smartphone) → 12/12 classées « IA ».
    # Les modèles publics sont surajustés aux distributions 2024-2025 et
    # confondent le traitement smartphone (HDR, débruitage) avec de la synthèse.
    # → n'utiliser que la provenance (niveau 1), qui est déterministe.
    use_model = args.with_model
    results = []
    for f in files:
        try:
            results.append(analyze(f, do_local=use_model and not args.no_local,
                                   grid=args.grid, use_model=use_model))
        except Exception as exc:
            results.append({"name": f.name, "error": f"{type(exc).__name__}: {exc}"})
        r = results[-1]
        if not args.json:
            print(f"{r['name']}: {r.get('verdict','ERREUR')} "
                  f"(confiance {r.get('confidence','—')})")

    # ── Hook de rappel (décision JC 2026-10-22) ──────────────────
    # Trace l'usage et affiche le rappel sur stderr (jamais sur stdout,
    # pour ne pas casser --json). Ne doit jamais faire échouer l'outil.
    try:
        import sys as _sys
        _sys.path.insert(0, str(PKA_ROOT / "scripts"))
        from ai_image_check_hook import record_and_remind
        record_and_remind(invocation="pka_ai_image_check", n_files=len(files))
    except Exception:
        pass

    report = {"generated": datetime.now().isoformat(timespec="seconds"),
              "model": MODEL_NAME, "results": results}

    if args.report:
        render_md(report, Path(args.report))
        print(f"\nRapport : {args.report}", file=sys.stderr)

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
