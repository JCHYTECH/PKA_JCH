#!/usr/bin/env python3
"""P1-4 — ajouter la 3ᵉ roue (midtones) + Luminance + varier Blending/Balance aux XMP.

Constat : les 12 looks Naturaliste partagent le même grading (ombres 220°, hautes 38°,
blending 50, balance -20 partout) — ils ne diffèrent que par TSL/courbe.
Ce script rend chaque look distinct par sa roue « tons moyens », ses sliders Luminance,
et son Blending/Balance, tout en respectant la convention de force existante :
  - Doux  = saturation × 0.4, Fort = saturation × 2.0  (teinte + blending + balance constants)
  - le midtone et les Luminance suivent la même règle de scaling.

Réversible via git. Idempotent (re-exécution sans doublon).
Valeurs de départ (base) : mid_hue, mid_sat, shadow_lum, midtone_lum, highlight_lum, blending, balance
"""
import os
import glob
import sys

DIR = "JCH_Inbox/03_PROJECTS/02_ARTEON/presets-naturaliste"

DESIGN = {
    "Signature Fin Art Cinematique": (40, 3, 0, 0, 0, 50, -20),   # référence universelle
    "Plumage sombre":                (30, 6, -8, 0, 0, 65, -10),  # réchauffe, noirs veloutés
    "Plumage clair":                 (200, 2, 0, 0, 0, 40, 10),   # protège hautes lumières
    "Golden hour":                   (40, 8, 0, 0, 5, 75, 25),    # lumière chaude, halo doré
    "Plumage colore":                (210, 5, 0, 0, 0, 50, 0),    # rehausse les bleus
    "Mammiferes":                    (25, 6, -5, 0, 0, 60, -10),  # fourrure fauve
    "Nocturne":                      (215, 5, -6, 0, 0, 55, -5),  # compense lumière artificielle
    "Macro":                         (0, 2, 0, 0, 0, 45, 0),      # détail d'abord, neutre
    "Action vol":                    (210, 3, 0, 0, 0, 35, 0),    # sec, ne mord pas le bruit
    "Paysage":                       (45, 4, 0, 0, 0, 55, 10),    # profondeur chaude
    "Noir et blanc":                 (0, 0, 0, 0, 0, 50, -20),    # monochrome (aucune teinte)
    "Contre-jour brume":             (195, 4, 0, 0, 0, 85, 15),   # doux, atmosphérique
}

FORCE = {" - Doux": 0.4, "": 1.0, " - Fort": 2.0}

NEW_KEYS = (
    "ColorGradeMidtoneHue", "ColorGradeMidtoneSat",
    "ColorGradeShadowLum", "ColorGradeMidtoneLum", "ColorGradeHighlightLum",
    "ColorGradeBalance",
)


def process(path, mid_hue, mid_sat, sh_lum, md_lum, hi_lum, blend, bal, force):
    mid_sat = int(round(mid_sat * force))
    sh_lum = int(round(sh_lum * force))
    md_lum = int(round(md_lum * force))
    hi_lum = int(round(hi_lum * force))

    with open(path, encoding="utf-8") as fh:
        lines = fh.readlines()

    new_lines = [
        f'    crs:ColorGradeMidtoneHue="{mid_hue}"\n',
        f'    crs:ColorGradeMidtoneSat="{mid_sat}"\n',
        f'    crs:ColorGradeShadowLum="{sh_lum}"\n',
        f'    crs:ColorGradeMidtoneLum="{md_lum}"\n',
        f'    crs:ColorGradeHighlightLum="{hi_lum}"\n',
        f'    crs:ColorGradeBalance="{bal}"\n',
    ]

    out = []
    inserted = False
    for ln in lines:
        s = ln.strip()
        # idempotence : retire les clés qu'on va (ré)ajouter
        if any(s.startswith(k + "=") for k in NEW_KEYS):
            continue
        if s.startswith("crs:ColorGradeBlending="):
            ln = f'    crs:ColorGradeBlending="{blend}"\n'
        elif s.startswith("crs:SplitToningBalance="):
            ln = f'    crs:SplitToningBalance="{bal}"\n'
        out.append(ln)
        if not inserted and s.startswith("crs:ColorGradeHighlightSat="):
            out.extend(new_lines)
            inserted = True

    if not inserted:  # repli : avant ColorGradeBlending
        for i, ln in enumerate(out):
            if ln.strip().startswith("crs:ColorGradeBlending="):
                out[i:i] = new_lines
                inserted = True
                break

    with open(path, "w", encoding="utf-8") as fh:
        fh.writelines(out)

    return mid_sat, sh_lum, md_lum, hi_lum


def main() -> int:
    files = sorted(glob.glob(os.path.join(DIR, "*.xmp")))
    done = 0
    for f in files:
        base = os.path.basename(f)[:-4]
        if base.endswith(" - Doux"):
            look, force = base[: -len(" - Doux")], FORCE[" - Doux"]
        elif base.endswith(" - Fort"):
            look, force = base[: -len(" - Fort")], FORCE[" - Fort"]
        else:
            look, force = base, FORCE[""]
        if look not in DESIGN:
            print(f"SKIP look inconnu : {base}")
            continue
        mh, ms, sl, ml, hl, blend, bal = DESIGN[look]
        ms2, sl2, ml2, hl2 = process(f, mh, ms, sl, ml, hl, blend, bal, force)
        done += 1
        print(f"{base:45s} mid={mh}/{ms2:+d} lum={sl2:+d}/{ml2:+d}/{hl2:+d} blend={blend} bal={bal:+d}")

    print(f"\n{done} fichiers traités.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
