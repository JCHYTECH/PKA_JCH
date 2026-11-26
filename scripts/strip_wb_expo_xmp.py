#!/usr/bin/env python3
"""P0-1 — découpler WB/tint/expo des XMP de look (pack Naturaliste).

Rend chaque preset « As Shot » sur la balance des blancs et l'exposition,
conformément au mode d'emploi (« le preset donne la direction, pas la valeur »).
Retire 4 clés : crs:WhiteBalance, crs:ColorTemperature, crs:Tint, crs:Exposure2012.

Réversible via git (fichiers trackés) : git checkout -- <fichier>.
"""
import os
import glob
import sys

DIR = "JCH_Inbox/03_PROJECTS/02_ARTEON/presets-naturaliste"
KEYS = ("crs:WhiteBalance=", "crs:ColorTemperature=", "crs:Tint=", "crs:Exposure2012=")


def main() -> int:
    files = sorted(glob.glob(os.path.join(DIR, "*.xmp")))
    if not files:
        print("Aucun .xmp trouvé dans", DIR, file=sys.stderr)
        return 1

    total_removed = 0
    touched = 0
    for f in files:
        with open(f, encoding="utf-8") as fh:
            lines = fh.readlines()
        kept, removed = [], []
        for ln in lines:
            s = ln.strip()
            if any(s.startswith(k) for k in KEYS):
                removed.append(s)
            else:
                kept.append(ln)
        if removed:
            with open(f, "w", encoding="utf-8") as fh:
                fh.writelines(kept)
            touched += 1
            total_removed += len(removed)
            print(f"{os.path.basename(f):45s} -{len(removed)}  {', '.join(removed)}")
        else:
            print(f"{os.path.basename(f):45s}  rien à retirer")

    print(f"\nTOTAL : {total_removed} clés retirées sur {touched}/{len(files)} fichiers.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
