#!/usr/bin/env python3
"""
crop_advisor.py — Dobby 🦉 / Argus 🦅
Recadrage précis assisté par composition + crop guide overlays.

Entrées :
  - image (JPEG/PNG)
  - sujet : {"bbox": [x,y,w,h] normalisé 0-1, "focal": [x,y] normalisé,
             "gaze": "left"|"right"|"center"}
  - ratio cible (largeur/hauteur), ex: 1.5 (3:2), 0.8 (4:5), 1.0 (1:1)
  - guides : "thirds", "phi" (basés sur des points d'ancrage)

Sorties :
  - recadrages candidats (coordonnées PLEINE résolution + normalisées)
  - overlay JPEG : grille (tiers + phi) + bbox sujet + point focal + recadrages

Usage : python3 crop_advisor.py <image> --bbox x,y,w,h --focal x,y --gaze right
                                [--ratio 1.5] [--out overlay.jpg]
"""
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw

import math

# A4 = 1:√2 ≈ 1.4142 (ratio largeur/hauteur, paysage)
A4_RATIO = math.sqrt(2)              # A4 paysage (largeur/hauteur)
A4_PORTRAIT_RATIO = 1 / math.sqrt(2)  # A4 portrait

GUIDES = {
    "thirds": {"ax": [1/3, 2/3], "ay": [1/3, 2/3]},
    "phi":    {"ax": [0.382, 0.618], "ay": [0.382, 0.618]},
}
COLORS = {"thirds": (255, 255, 0, 230), "phi": (0, 255, 255, 230)}


def _anchor_for_gaze(guide, gaze):
    g = GUIDES[guide]
    if gaze == "right":
        ax = g["ax"][0]      # point focal à gauche → air à droite
    elif gaze == "left":
        ax = g["ax"][1]      # point focal à droite → air à gauche
    else:
        ax = 0.5
    ay = g["ay"][0]          # œil dans le tiers supérieur
    return ax, ay


def compute_crop(W, H, bbox, focal, gaze, ratio, guide="thirds", margin_pct=0.15):
    """Recadrage robuste : contient le sujet (avec marge) au ratio cible, et place
    le point focal sur le guide quand c'est possible (ancre souple — dégrade sinon).
    Retourne toujours un dict tant que le sujet tient dans l'image."""
    ax, ay = _anchor_for_gaze(guide, gaze)
    sbx, sby, sbw, sbh = bbox[0] * W, bbox[1] * H, bbox[2] * W, bbox[3] * H
    fpx, fpy = focal[0] * W, focal[1] * H
    m = margin_pct * max(sbw, sbh)

    # sujet padé
    px0, py0 = sbx - m, sby - m
    px1, py1 = sbx + sbw + m, sby + sbh + m
    # clamp au cadre : sujet proche du bord → la marge déborderait
    px0 = max(0.0, px0)
    py0 = max(0.0, py0)
    px1 = min(float(W), px1)
    py1 = min(float(H), py1)
    sw, sh = px1 - px0, py1 - py0

    # taille minimale du crop au ratio cible (contient le sujet padé)
    cw = max(sw, sh * ratio)
    ch = cw / ratio
    if cw > W:
        cw = W
        ch = cw / ratio
    if ch > H:
        ch = H
        cw = ch * ratio

    # position idéale : point focal ancré sur (ax, ay)
    cx_ideal = fpx - ax * cw
    cy_ideal = fpy - ay * ch

    # plage faisable : contient le sujet padé ET reste dans l'image
    lo_x = max(0.0, px1 - cw)
    hi_x = min(W - cw, px0)
    lo_y = max(0.0, py1 - ch)
    hi_y = min(H - ch, py0)

    # clamp : on s'approche de l'idéal dans les limites faisables
    cx = lo_x if cx_ideal < lo_x else (hi_x if cx_ideal > hi_x else cx_ideal)
    cy = lo_y if cy_ideal < lo_y else (hi_y if cy_ideal > hi_y else cy_ideal)

    return {
        "guide": guide,
        "gaze": gaze,
        "ratio": ratio,
        "x": round(cx), "y": round(cy), "w": round(cw), "h": round(ch),
        "anchor": (round(ax, 3), round(ay, 3)),
        # coordonnées normalisées (pour Lightroom / affichage)
        "nx": round(cx / W, 4), "ny": round(cy / H, 4),
        "nw": round(cw / W, 4), "nh": round(ch / H, 4),
    }


def advise(image_path, subject, ratios=(A4_RATIO, A4_PORTRAIT_RATIO), guides=("thirds", "phi"), margin_pct=0.15):
    """Calcule les recadrages candidats pour chaque couple (ratio, guide)."""
    im = Image.open(image_path)
    W, H = im.size
    crops = []
    for ratio in ratios:
        for guide in guides:
            c = compute_crop(W, H, subject["bbox"], subject["focal"],
                             subject.get("gaze", "center"), ratio, guide, margin_pct)
            if c:
                crops.append(c)
    return {"width": W, "height": H, "crops": crops}


def crop_to_xmp_attrs(crop):
    """Convertit un crop (nx/ny/nw/nh normalisés) en attributs XMP Lightroom (crop).

    Lightroom stocke la POSITION des bords du crop (0-1), pas la fraction rognée :
    plein cadre = CropTop 0, CropLeft 0, CropBottom 1, CropRight 1."""
    top = crop["ny"]
    left = crop["nx"]
    bottom = crop["ny"] + crop["nh"]
    right = crop["nx"] + crop["nw"]
    return {
        "HasCrop": "True",
        "CropTop": f"{min(1.0, max(0.0, top)):.4f}",
        "CropLeft": f"{min(1.0, max(0.0, left)):.4f}",
        "CropBottom": f"{min(1.0, max(0.0, bottom)):.4f}",
        "CropRight": f"{min(1.0, max(0.0, right)):.4f}",
        "CropAngle": "0",
        "CropConstrainToWarp": "0",
        "CropConstrainToUnitSquare": "1",
    }


def render_overlay(image_path, subject, crops, out_path, scale=1600):
    """Dessine grille + bbox + focal + recadrages sur une copie réduite."""
    im = Image.open(image_path).convert("RGB")
    W_full, H_full = im.size
    k = scale / max(im.size)
    if k < 1:
        im = im.resize((int(W_full * k), int(H_full * k)), Image.LANCZOS)
    W, H = im.size
    d = ImageDraw.Draw(im, "RGBA")

    # grille tiers (blanc)
    for i in (1, 2):
        x = int(W * i / 3); y = int(H * i / 3)
        d.line([(x, 0), (x, H)], fill=(255, 255, 255, 80), width=1)
        d.line([(0, y), (W, y)], fill=(255, 255, 255, 80), width=1)
    # grille phi / nombre d'or (doré)
    for f in (0.382, 0.618):
        x = int(W * f); y = int(H * f)
        d.line([(x, 0), (x, H)], fill=(255, 200, 0, 90), width=1)
        d.line([(0, y), (W, y)], fill=(255, 200, 0, 90), width=1)

    # bbox sujet (vert) + point focal (rouge)
    bx, by, bw, bh = subject["bbox"]
    d.rectangle([bx * W, by * H, (bx + bw) * W, (by + bh) * H], outline=(0, 255, 0, 210), width=2)
    fx, fy = subject["focal"]
    r = 6
    d.ellipse([fx * W - r, fy * H - r, fx * W + r, fy * H + r], fill=(255, 0, 0, 255))

    # recadrages candidats (couleur par guide)
    for c in crops:
        col = COLORS.get(c["guide"], (255, 255, 255, 220))
        x0 = c["x"] * k; y0 = c["y"] * k; x1 = (c["x"] + c["w"]) * k; y1 = (c["y"] + c["h"]) * k
        d.rectangle([x0, y0, x1, y1], outline=col, width=3)
        d.text((x0 + 4, y0 + 4), f"{c['guide']} {c['ratio']:.2f}", fill=col)

    im.save(out_path, quality=90)
    return out_path


def main():
    import argparse
    ap = argparse.ArgumentParser(description="Recadrage assisté par composition + overlay")
    ap.add_argument("image")
    ap.add_argument("--bbox", required=True, help="x,y,w,h normalisé (ex: 0.35,0.40,0.35,0.45)")
    ap.add_argument("--focal", required=True, help="x,y normalisé (ex: 0.44,0.585)")
    ap.add_argument("--gaze", default="center", choices=["left", "right", "center"])
    ap.add_argument("--ratio", default="1.4142,0.7071", help="ratio(s) l/h, séparés par virgule (A4 paysage ≈ 1.4142, portrait ≈ 0.7071)")
    ap.add_argument("--out", default=None, help="chemin overlay JPEG")
    args = ap.parse_args()

    bbox = [float(v) for v in args.bbox.split(",")]
    focal = [float(v) for v in args.focal.split(",")]
    ratios = tuple(float(v) for v in args.ratio.split(","))
    subject = {"bbox": bbox, "focal": focal, "gaze": args.gaze}

    result = advise(args.image, subject, ratios=ratios)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    if args.out:
        overlay = render_overlay(args.image, subject, result["crops"], args.out)
        print(f"OVERLAY: {overlay}", file=sys.stderr)


if __name__ == "__main__":
    main()