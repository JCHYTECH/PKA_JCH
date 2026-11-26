#!/usr/bin/env python3
"""
exif_raw.py — Dobby 🦉 / Argus 🦅
Extraction EXIF enrichie (JPEG export + CR3 RAW) : exposition, focus, WB, optique.

Comble la limite historique de `read_exif_fields` (4 champs : focale, ouverture,
ISO, vitesse) en capturant la télémétrie complète disponible dans le fichier :
  - exposition  : temps, ouverture, ISO, correction d'expo, mode, mesure, flash,
                  WB, température couleur, LightValue (EV)
  - focus       : focale, objectif, mode AF, distance de mise au point (bornes),
                  zone AF, position du collimateur actif, rafale, IS
  - WB brute    : température mesurée/réglée, coefficients RGGB as-shot (RAW)
  - boîtier     : marque, modèle, date, résolution native (RAW)

Usage (CLI)    : python3 exif_raw.py <image_path>
Usage (import) : from exif_raw import extract; data = extract(path)

Dépendance     : exiftool (https://exiftool.org — brew install exiftool)
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

# exiftool : chemin absolu, repli sur le PATH
_EXIFTOOL = "/opt/homebrew/bin/exiftool"
if not Path(_EXIFTOOL).exists():
    _EXIFTOOL = shutil.which("exiftool") or "exiftool"

# clé normalisée -> [candidats exiftool groupés (famille 0), par priorité décroissante]
FIELDS = {
    # --- boîtier / prise ---
    "make":                 ["EXIF:Make", "Make"],
    "model":                ["EXIF:Model", "Model"],
    "datetime_original":    ["EXIF:DateTimeOriginal", "DateTimeOriginal"],
    "raw_width":            ["MakerNotes:CanonImageWidth", "EXIF:CanonImageWidth", "CanonImageWidth"],
    "raw_height":           ["MakerNotes:CanonImageHeight", "EXIF:CanonImageHeight", "CanonImageHeight"],
    # --- exposition ---
    "exposure_time":        ["EXIF:ExposureTime", "ExposureTime"],
    "f_number":             ["EXIF:FNumber", "FNumber"],
    "iso":                  ["EXIF:ISO", "ISO"],
    "exposure_comp":        ["EXIF:ExposureCompensation", "MakerNotes:ExposureCompensation", "ExposureCompensation"],
    "exposure_program":     ["EXIF:ExposureProgram", "ExposureProgram"],
    "metering_mode":        ["EXIF:MeteringMode", "MakerNotes:MeteringMode", "MeteringMode"],
    "flash":                ["EXIF:Flash", "Flash"],
    "white_balance":        ["EXIF:WhiteBalance", "WhiteBalance"],
    "wb_preset":            ["MakerNotes:WhiteBalance"],  # preset Canon réel (ex: Cloudy)
    "color_temperature":    ["EXIF:ColorTemperature", "XMP:ColorTemperature", "MakerNotes:ColorTempKelvin", "ColorTemperature"],
    "light_value":          ["Composite:LightValue", "LightValue"],
    # --- optique / focus ---
    "focal_length":         ["EXIF:FocalLength", "FocalLength"],
    "focal_length_35efl":   ["Composite:FocalLength35efl", "FocalLength35efl"],
    "lens_model":           ["EXIF:LensModel", "XMP:LensModel", "LensModel"],
    "rf_lens_type":         ["MakerNotes:RFLensType", "RFLensType"],
    "focus_mode":           ["MakerNotes:FocusMode", "FocusMode"],
    "focus_distance_upper": ["EXIF:FocusDistanceUpper", "MakerNotes:FocusDistanceUpper", "FocusDistanceUpper"],
    "focus_distance_lower": ["EXIF:FocusDistanceLower", "MakerNotes:FocusDistanceLower", "FocusDistanceLower"],
    "subject_distance":     ["EXIF:SubjectDistance", "Composite:SubjectDistance", "SubjectDistance"],
    "af_area_mode":         ["MakerNotes:AFAreaMode", "AFAreaMode"],
    "af_area_x":            ["MakerNotes:AFAreaXPositions", "AFAreaXPositions"],
    "af_area_y":            ["MakerNotes:AFAreaYPositions", "AFAreaYPositions"],
    "af_area_width":        ["MakerNotes:AFAreaWidths", "AFAreaWidths"],
    "af_area_height":       ["MakerNotes:AFAreaHeights", "AFAreaHeights"],
    "af_points_in_focus":   ["MakerNotes:AFPointsInFocus", "AFPointsInFocus"],
    "num_af_points":        ["MakerNotes:NumAFPoints", "NumAFPoints"],
    "valid_af_points":      ["MakerNotes:ValidAFPoints", "ValidAFPoints"],
    "drive_mode":           ["Composite:DriveMode", "DriveMode"],
    "continuous_drive":     ["MakerNotes:ContinuousDrive", "ContinuousDrive"],
    "image_stabilization":  ["MakerNotes:ImageStabilization", "ImageStabilization"],
    # --- WB brute (RAW) ---
    "color_temp_kelvin":    ["MakerNotes:ColorTempKelvin", "ColorTempKelvin"],
    "color_temp_measured":  ["MakerNotes:ColorTempMeasured", "ColorTempMeasured"],
    "wb_rggb_as_shot":      ["MakerNotes:WB_RGGBLevelsAsShot", "WB_RGGBLevelsAsShot"],
}

# champs numériques utiles pour l'audit quantitatif (seconde passe `-n`)
NUMERIC = {
    "exposure_comp_num": ["EXIF:ExposureCompensation", "MakerNotes:ExposureCompensation", "ExposureCompensation"],
    "light_value_num":   ["Composite:LightValue", "LightValue"],
    "iso_num":           ["EXIF:ISO", "ISO"],
    "exposure_time_num": ["EXIF:ExposureTime", "ExposureTime"],
    "focus_upper_m":     ["EXIF:FocusDistanceUpper", "MakerNotes:FocusDistanceUpper", "FocusDistanceUpper"],
    "focus_lower_m":     ["EXIF:FocusDistanceLower", "MakerNotes:FocusDistanceLower", "FocusDistanceLower"],
    "focal_length_num":  ["EXIF:FocalLength", "FocalLength"],
}

# champs « liste » (exiftool renvoie N valeurs séparées par espaces) → 1er élément non nul
LIST_FIELDS = {"af_area_x", "af_area_y", "af_area_width", "af_area_height"}


def _run(args, timeout=30):
    """Exécute exiftool en JSON (groupes famille 0) et renvoie le 1er dict, ou {}."""
    try:
        r = subprocess.run(
            [_EXIFTOOL, *args], capture_output=True, text=True, timeout=timeout
        )
    except (OSError, subprocess.TimeoutExpired):
        return {}
    if r.returncode != 0:
        return {}
    try:
        data = json.loads(r.stdout)
    except json.JSONDecodeError:
        return {}
    return data[0] if data else {}


def _get(meta, candidates):
    """Renvoie la première valeur présente parmi les candidats groupés."""
    for c in candidates:
        if c in meta:
            return meta[c]
    return None


def _first_nonzero(value):
    """Pour un champ liste : renvoie le 1er élément non nul (sinon le 1er)."""
    items = value if isinstance(value, list) else str(value).split()
    for it in items:
        s = str(it).strip()
        if s not in ("", "0", "0.0", "n/a"):
            return it
    return items[0] if items else None


def extract(image_path):
    """Extrait la télémétrie EXIF enrichie d'une image (JPEG/CR3/DNG...).

    Retourne un dict plat. Les champs absents du fichier sont simplement omis
    (un JPEG exporté n'a pas le focus/AF ; un CR3 n'a pas le WB édité par LrC).
    """
    path = str(Path(image_path).expanduser())
    human = _run(["-json", "-G", path])
    num = _run(["-json", "-G", "-n", path])

    out = {
        "path": path,
        "file_type": Path(path).suffix.lower().lstrip(".") or None,
    }
    for key, candidates in FIELDS.items():
        v = _get(human, candidates)
        if v is None:
            continue
        out[key] = _first_nonzero(v) if key in LIST_FIELDS else v
    for key, candidates in NUMERIC.items():
        v = _get(num, candidates)
        if v is not None:
            out[key] = v
    return out


def main():
    if len(sys.argv) < 2:
        print(
            json.dumps(
                {"error": "usage: exif_raw.py <image_path>"},
                ensure_ascii=False, indent=2,
            )
        )
        sys.exit(1)
    print(json.dumps(extract(sys.argv[1]), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
