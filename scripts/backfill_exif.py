#!/usr/bin/env python3
"""
backfill_exif.py — Met à jour les colonnes EXIF (focal_length, aperture, iso_value,
shutter_speed) pour les analyses existantes dans argus_critique.db.
Usage : python3 backfill_exif.py [--photo-dir DIR]
"""
import sqlite3
import subprocess
import argparse
from pathlib import Path

DB_PATH   = Path(__file__).resolve().parent.parent / "PHOTO" / "argus_critique.db"
PHOTO_DIR = Path("/Users/jchavauxm5/Desktop/LrC To /Dobby select")


def extract_exif(image_path: Path) -> dict:
    try:
        r = subprocess.run(
            ['exiftool', '-FocalLength', '-Aperture', '-ISO', '-ShutterSpeed',
             '-n', '-s3', str(image_path)],
            capture_output=True, text=True, timeout=10
        )
        lines = [l.strip() for l in r.stdout.strip().splitlines() if l.strip()]
        keys  = ['focal_length', 'aperture', 'iso_value', 'shutter_speed']
        result = {}
        for i, val in enumerate(lines):
            if i >= len(keys):
                break
            k = keys[i]
            try:
                if k == 'focal_length':   result[k] = int(float(val))
                elif k == 'aperture':     result[k] = round(float(val), 1)
                elif k == 'iso_value':    result[k] = int(val)
                else:                     result[k] = val
            except (ValueError, TypeError):
                pass
        return result
    except Exception:
        return {}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--photo-dir", default=str(PHOTO_DIR))
    args = parser.parse_args()
    photo_dir = Path(args.photo_dir)

    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT id, filename FROM analyses WHERE focal_length IS NULL"
    ).fetchall()

    updated = skipped = 0
    for row_id, filename in rows:
        img = photo_dir / filename
        if not img.exists():
            skipped += 1
            continue
        exif = extract_exif(img)
        if not exif:
            skipped += 1
            continue
        conn.execute(
            """UPDATE analyses
               SET focal_length=?, aperture=?, iso_value=?, shutter_speed=?
               WHERE id=?""",
            (exif.get('focal_length'), exif.get('aperture'),
             exif.get('iso_value'), exif.get('shutter_speed'), row_id)
        )
        updated += 1

    conn.commit()
    conn.close()
    print(f"✅ EXIF backfill — {updated} mises à jour, {skipped} ignorées")


if __name__ == "__main__":
    main()
