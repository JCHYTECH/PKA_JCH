#!/usr/bin/env python3
"""
exif_analysis.py — Dobby 🦉 / Argus 🦅
Analyses déterministes à partir de l'EXIF + des pixels (sans appel IA) :
  1. Audit exposition ETTR    — correction d'expo + histogramme
  2. Risque de flou de bougé  — vitesse + focale + IS
  3. Netteté / qualité focus  — Variance de Laplacian (global + zone AF)
  4. Limite de diffraction    — ouverture + capteur APS-C
  5. Profondeur de champ      — ouverture + focale + distance sujet
  6. Bruit / ISO              — ISO + ombres

Usage (CLI)    : python3 exif_analysis.py <image_path> [--json]
Usage (import) : from exif_analysis import analyze, format_report

Dépendances    : numpy, Pillow, exif_raw (module voisin), exiftool (via exif_raw)
"""
import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from exif_raw import extract as extract_exif

# Canon EOS R10 — APS-C 22.3×14.9 mm, crop 1.6, 6000×4000 (24.2 MP, pixel 3.72 µm)
CROP = 1.6
SENSOR_W_MM = 22.3
RAW_W = 6000
RAW_H = 4000
PIXEL_UM = SENSOR_W_MM * 1000 / RAW_W          # ≈ 3.72 µm
COC_MM = 0.019                                  # cercle de confusion APS-C
DIFFRACTION_ONSET_F = 8.0                       # ~f/8 sur APS-C 24 MP (Airy ≈ 2.5 px)
WAVELENGTH_UM = 0.55
SHARP_SCALE = 1024                              # taille de référence pour la netteté


def _load_gray(path, scale=None):
    im = Image.open(path).convert("L")
    if scale:
        ratio = scale / max(im.size)
        if ratio < 1:
            im = im.resize((int(im.width * ratio), int(im.height * ratio)), Image.LANCZOS)
    return np.asarray(im).astype(np.float64)


def _laplacian_var(a):
    lap = np.zeros_like(a)
    lap[1:-1, 1:-1] = (a[:-2, 1:-1] + a[2:, 1:-1] + a[1:-1, :-2] + a[1:-1, 2:] - 4 * a[1:-1, 1:-1])
    return float(lap.var())


def _as_float(v, strip=None):
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v)
    if strip:
        s = s.replace(strip, "")
    s = s.strip().rstrip("m").strip()  # enlève 'm' unité éventuelle
    try:
        return float(s)
    except (ValueError, TypeError):
        return None


def audit_exposure(path, exif):
    a = _load_gray(path)
    lum = float(a.mean())
    p05, p50, p95 = (float(x) for x in np.percentile(a, [5, 50, 95]))
    clip_hi = float((a >= 250).mean() * 100)
    clip_lo = float((a <= 5).mean() * 100)
    headroom = math.log2(255.0 / max(p95, 1.0))
    ec = exif.get("exposure_comp_num")

    if clip_hi > 2:
        verdict = f"hautes lumières clippées ({clip_hi:.1f} %) — risque de perte sur le blanc"
    elif headroom < 0.3:
        verdict = f"proche du bord droit (marge {headroom:.2f} EV) — exposition quasi optimale"
    elif headroom >= 0.7:
        verdict = f"marge de {headroom:.2f} EV — tu aurais pu exposer plus clair sans clipper"
    else:
        verdict = f"exposition correcte, marge {headroom:.2f} EV"
    if ec is not None and ec < 0:
        verdict += f" (sous-expo volontaire EC {ec:.2f} EV — protège les hautes lumières)"

    return {
        "lum_mean": round(lum, 1),
        "p05": round(p05, 1), "p50": round(p50, 1), "p95": round(p95, 1),
        "clip_hi_pct": round(clip_hi, 2), "clip_lo_pct": round(clip_lo, 2),
        "ettr_headroom_ev": round(headroom, 2),
        "verdict": verdict,
    }


def audit_motion_blur(exif):
    t = exif.get("exposure_time_num")
    f = exif.get("focal_length_num")
    if not t or not f:
        return {"verdict": "vitesse/focale indisponibles"}
    eff_f = f * CROP
    min_shutter = 1.0 / eff_f
    is_on = bool(exif.get("image_stabilization")) and str(exif.get("image_stabilization")).lower().startswith("on")
    is_stops = 3 if is_on else 0
    min_shutter_is = min_shutter / (2 ** is_stops)
    actual = 1.0 / t if t > 0 else 0

    if actual >= min_shutter * 4:
        verdict = f"vitesse 1/{actual:.0f} largement au-dessus du seuil — aucun risque de bougé, y compris en action"
    elif actual >= min_shutter:
        verdict = f"vitesse 1/{actual:.0f} ≥ seuil 1/{min_shutter:.0f} (sans IS) — OK pour sujet perché"
    elif actual >= min_shutter_is:
        verdict = f"vitesse 1/{actual:.0f} sous le seuil 1/{min_shutter:.0f} mais couverte par l'IS ({is_stops} stops) — OK perché, limite en action"
    else:
        verdict = f"vitesse 1/{actual:.0f} trop lente pour {eff_f:.0f} mm équiv. — risque de bougé"

    return {
        "focal_eff_mm": round(eff_f),
        "min_shutter_recip": f"1/{min_shutter:.0f}",
        "is": f"on (~{is_stops} stops)" if is_on else "off",
        "verdict": verdict,
    }


def audit_sharpness(path, exif):
    a = _load_gray(path, scale=SHARP_SCALE)
    h, w = a.shape
    vl = _laplacian_var(a)

    if vl < 50:
        level = "flou / raté de focus probable"
    elif vl < 150:
        level = "netteté moyenne"
    elif vl < 400:
        level = "bonne netteté"
    else:
        level = "très nette"

    out = {"laplacian_var": round(vl, 1), "verdict": level, "note": "VL sur 1024 px (repère : <50 flou, 50–150 moyen, 150–400 bon, >400 très net)"}

    # Netteté dans la zone AF (si coordonnées disponibles, RAW uniquement)
    ax = exif.get("af_area_x")
    ay = exif.get("af_area_y")
    aw = exif.get("af_area_width")
    ah = exif.get("af_area_height")
    if ax is not None and ay is not None and aw and ah:
        try:
            ax, ay, aw, ah = float(ax), float(ay), float(aw), float(ah)
            # coordonnées AF centrées sur l'image plein format (6000×4000)
            # → on les projette dans l'image chargée (échelle SHARP_SCALE)
            sx = w / RAW_W
            sy = h / RAW_H
            cx = w / 2 + ax * sx
            cy = h / 2 + ay * sy
            rw = aw * sx / 2
            rh = ah * sy / 2
            x0 = max(0, int(cx - rw)); x1 = min(w, int(cx + rw))
            y0 = max(0, int(cy - rh)); y1 = min(h, int(cy + rh))
            region = a[y0:y1, x0:x1]
            if region.size > 100:
                out["af_point_sharpness"] = round(_laplacian_var(region), 1)
                out["af_zone"] = [x0, y0, x1, y1]
        except (ValueError, TypeError):
            pass
    return out


def audit_diffraction(exif):
    f = _as_float(exif.get("f_number"))
    if f is None:
        return {"verdict": "ouverture indisponible"}
    airy = 2.44 * WAVELENGTH_UM * f
    ratio = airy / PIXEL_UM
    if f <= DIFFRACTION_ONSET_F:
        verdict = f"f/{f:.1f} sous le seuil de diffraction (~f/{DIFFRACTION_ONSET_F:.0f}) — netteté optimale"
    else:
        verdict = f"f/{f:.1f} au-delà du seuil (~f/{DIFFRACTION_ONSET_F:.0f}) — légère diffraction (tache d'Airy {airy:.1f} µm ≈ {ratio:.1f} px)"
    return {"airy_um": round(airy, 1), "airy_px": round(ratio, 1), "verdict": verdict}


def audit_dof(exif):
    f = exif.get("focal_length_num")
    N = _as_float(exif.get("f_number"))
    s = exif.get("focus_lower_m") or exif.get("subject_distance")
    s = _as_float(s, strip="m")
    if not f or not N or not s:
        return {"verdict": "DOF indisponible (focale/ouverture/distance manquantes)"}
    f = float(f); s = s * 1000  # mm
    c = COC_MM
    H = f * f / (N * c) + f
    if H > s:
        near = H * s / (H + (s - f))
        far = H * s / (H - (s - f))
        dof_m = (far - near) / 1000
    else:
        near = s
        far = float("inf")
        dof_m = float("inf")
    verdict = (
        f"DOF ≈ {dof_m:.2f} m autour du point (distance {s/1000:.0f} m)"
        if dof_m != float("inf") else
        f"DOF infinie (sujet au-delà de l'hyperfocale {H/1000:.0f} m)"
    )
    return {
        "hyperfocal_m": round(H / 1000, 1),
        "dof_m": round(dof_m, 2) if dof_m != float("inf") else "infini",
        "near_m": round(near / 1000, 2),
        "far_m": round(far / 1000, 2) if far != float("inf") else "infini",
        "verdict": verdict,
    }


def audit_noise(exif):
    iso = exif.get("iso_num")
    if not iso:
        return {"verdict": "ISO indisponible"}
    iso = int(iso)
    if iso <= 800:
        v = f"ISO {iso} — bruit négligeable"
    elif iso <= 1600:
        v = f"ISO {iso} — bruit léger, détail préservé"
    elif iso <= 3200:
        v = f"ISO {iso} — bruit visible, à traiter (denoise)"
    else:
        v = f"ISO {iso} — bruit fort, risque de perte de détail dans les ombres"
    return {"iso": iso, "verdict": v}


def analyze(image_path, exif=None):
    """Retourne un dict structuré des 6 audits (exposition, bougé, netteté,
    diffraction, DOF, bruit) pour l'image donnée.

    `exif` optionnel : dict pré-extrait (ex: RAW) à utiliser pour les audits
    EXIF, pendant que `image_path` fournit les pixels (ex: preview JPEG)."""
    path = str(Path(image_path).expanduser())
    if exif is None:
        exif = extract_exif(path)
    return {
        "path": path,
        "exposure": audit_exposure(path, exif),
        "motion_blur": audit_motion_blur(exif),
        "sharpness": audit_sharpness(path, exif),
        "diffraction": audit_diffraction(exif),
        "dof": audit_dof(exif),
        "noise": audit_noise(exif),
    }


def format_report(analysis, include_path=True):
    """Rendu compact lisible (une ligne par audit) — réutilisable en prompt."""
    lines = []
    if include_path:
        lines.append(f"EXIF + pixels — {Path(analysis['path']).name}")
    lines.append("Exposition : " + analysis["exposure"].get("verdict", "?"))
    lines.append("Bougé       : " + analysis["motion_blur"].get("verdict", "?"))
    lines.append("Netteté     : " + analysis["sharpness"].get("verdict", "?") +
                 f" (Laplacian var {analysis['sharpness'].get('laplacian_var','?')})")
    lines.append("Diffraction : " + analysis["diffraction"].get("verdict", "?"))
    lines.append("DOF         : " + analysis["dof"].get("verdict", "?"))
    lines.append("Bruit       : " + analysis["noise"].get("verdict", "?"))
    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print("usage: exif_analysis.py <image_path> [--json]", file=sys.stderr)
        sys.exit(1)
    a = analyze(sys.argv[1])
    if "--json" in sys.argv:
        print(json.dumps(a, ensure_ascii=False, indent=2))
    else:
        print(format_report(a))


if __name__ == "__main__":
    main()
