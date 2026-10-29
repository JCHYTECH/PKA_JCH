#!/usr/bin/env python3
"""
Pont Argus → Lightroom Classic via MCP (lightroom-mcp)

Usage:
  # Préparer les réglages pour une analyse
  python3 mcp_apply_lr.py prepare <analysis_id>
  python3 mcp_apply_lr.py prepare <analysis_id> --photo-id "LrC to-48"

  # Lister les clés SDK supportées
  python3 mcp_apply_lr.py sdk-keys

  # Mapper des clés humaines → SDK
  python3 mcp_apply_lr.py map '{"ColorTemperature": 5400, "Exposure": 0.5}'

Workflow complet :
  1. Argus analyse → stocke lr_params dans argus_critique.db
  2. mcp_apply_lr.py prepare <id> → JSON compatible lightroom-mcp
  3. Dobby appelle set_develop_settings(photo_id, settings) via MCP
  4. Lightroom Classic applique les réglages automatiquement
"""

import json
import sqlite3
import sys
from pathlib import Path
from typing import Optional

DB_PATH = Path(__file__).parent / "argus_critique.db"

# Mapping : clé humaine (Argus) → clé SDK Lightroom
# Les clés SDK sont restreintes à la allowlist du plugin lightroom-mcp
HUMAN_TO_SDK: dict[str, str] = {
    # White Balance
    "ColorTemperature": "Temperature",
    "WhiteBalance": "WhiteBalance",
    "Tint": "Tint",

    # Tone (Process 2012)
    "Exposure": "Exposure2012",
    "Contrast": "Contrast2012",
    "Highlights": "Highlights2012",
    "Shadows": "Shadows2012",
    "Whites": "Whites2012",
    "Blacks": "Blacks2012",

    # Presence
    "Texture": "Texture",
    "Clarity": "Clarity2012",
    "Dehaze": "Dehaze",
    "Vibrance": "Vibrance",
    "Saturation": "Saturation",

    # Detail
    "Sharpness": "Sharpness",
    "SharpenRadius": "SharpenRadius",
    "SharpenDetail": "SharpenDetail",
    "SharpenEdgeMasking": "SharpenEdgeMasking",
    "LuminanceNoise": "LuminanceSmoothing",
    "LuminanceNoiseDetail": "LuminanceNoiseReductionDetail",
    "LuminanceNoiseContrast": "LuminanceNoiseReductionContrast",
    "ColorNoise": "ColorNoiseReduction",
    "ColorNoiseDetail": "ColorNoiseReductionDetail",
    "ColorNoiseSmoothness": "ColorNoiseReductionSmoothness",

    # Lens
    "LensProfile": "LensProfileEnable",
    "LensDistortion": "LensManualDistortionAmount",

    # Transform
    "PerspectiveVertical": "PerspectiveVertical",
    "PerspectiveHorizontal": "PerspectiveHorizontal",
    "PerspectiveRotate": "PerspectiveRotate",
    "PerspectiveScale": "PerspectiveScale",
    "PerspectiveAspect": "PerspectiveAspect",
    "Upright": "PerspectiveUpright",

    # Effects
    "VignetteAmount": "PostCropVignetteAmount",
    "VignetteMidpoint": "PostCropVignetteMidpoint",
    "VignetteRoundness": "PostCropVignetteRoundness",
    "VignetteFeather": "PostCropVignetteFeather",
    "VignetteStyle": "PostCropVignetteStyle",
    "GrainAmount": "GrainAmount",
    "GrainSize": "GrainSize",
    "GrainFrequency": "GrainFrequency",

    # Tone Curve
    "ToneCurve": "ToneCurveName2012",
    "Grayscale": "ConvertToGrayscale",

    # Parametric
    "ParametricShadows": "ParametricShadows",
    "ParametricDarks": "ParametricDarks",
    "ParametricLights": "ParametricLights",
    "ParametricHighlights": "ParametricHighlights",

    # Crop
    "CropTop": "CropTop",
    "CropLeft": "CropLeft",
    "CropBottom": "CropBottom",
    "CropRight": "CropRight",
    "CropAngle": "CropAngle",
}

# Reverse mapping (SDK → human)
SDK_TO_HUMAN: dict[str, str] = {v: k for k, v in HUMAN_TO_SDK.items()}

# Valeurs spéciales : clés qui doivent être converties (ex: température Kelvin → float relatif)
# Pour l'instant, on passe les valeurs telles quelles — le plugin Lua fera la validation


def get_analysis(analysis_id: int) -> Optional[dict]:
    """Récupère une analyse depuis argus_critique.db."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        "SELECT * FROM analyses WHERE id = ?", (analysis_id,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def map_lr_params(lr_params: dict) -> dict:
    """Convertit les clés humaines en clés SDK Lightroom.

    Args:
        lr_params: dict avec clés humaines (ex: {"Exposure": 0.5, "ColorTemperature": 5400})

    Returns:
        dict avec clés SDK (ex: {"Exposure2012": 0.5, "Temperature": 5400})
    """
    mapped = {}
    skipped = []
    for key, value in lr_params.items():
        sdk_key = HUMAN_TO_SDK.get(key)
        if sdk_key:
            mapped[sdk_key] = value
        else:
            skipped.append(key)
    if skipped:
        print(f"⚠️  Clés non mappées (ignorées) : {', '.join(skipped)}", file=sys.stderr)
    return mapped


def prepare_mcp_call(analysis_id: int, photo_id: Optional[str] = None) -> dict:
    """Prépare l'appel MCP set_develop_settings pour une analyse.

    Returns:
        dict avec 'photo_id' et 'settings' prêts pour l'outil MCP.
    """
    analysis = get_analysis(analysis_id)
    if not analysis:
        print(f"❌ Analyse #{analysis_id} introuvable", file=sys.stderr)
        sys.exit(1)

    lr_params_raw = analysis.get("lr_params")
    if not lr_params_raw:
        print(f"❌ Analyse #{analysis_id} n'a pas de lr_params", file=sys.stderr)
        sys.exit(1)

    lr_params = json.loads(lr_params_raw) if isinstance(lr_params_raw, str) else lr_params_raw
    mapped = map_lr_params(lr_params)

    pid = photo_id or analysis.get("filename", f"analysis_{analysis_id}")
    return {
        "photo_id": pid,
        "settings": mapped,
    }


def cmd_prepare(args: list[str]):
    """Commande prepare : prépare l'appel MCP pour une analyse."""
    if not args:
        print("Usage: mcp_apply_lr.py prepare <analysis_id> [--photo-id <id>]", file=sys.stderr)
        sys.exit(1)

    analysis_id = int(args[0])
    photo_id = None
    if len(args) >= 3 and args[1] == "--photo-id":
        photo_id = args[2]

    result = prepare_mcp_call(analysis_id, photo_id)
    print(json.dumps(result, indent=2))

    # Afficher un rappel pour l'utilisateur
    sdk_keys = list(result["settings"].keys())
    print(f"\n📋 Pour appliquer dans Lightroom, utilise l'outil MCP 'set_develop_settings' :", file=sys.stderr)
    print(f"   photo_id: {result['photo_id']}", file=sys.stderr)
    print(f"   settings: {len(sdk_keys)} paramètres → {', '.join(sdk_keys[:8])}{'...' if len(sdk_keys) > 8 else ''}", file=sys.stderr)


def cmd_sdk_keys(_args: list[str]):
    """Liste toutes les clés SDK supportées."""
    sdk_keys = sorted(set(HUMAN_TO_SDK.values()))
    print(f"Clés SDK Lightroom supportées ({len(sdk_keys)}) :\n")
    for key in sdk_keys:
        human = SDK_TO_HUMAN.get(key, "—")
        print(f"  {key:<35} ← {human}")


def cmd_map(args: list[str]):
    """Mappe des clés humaines → SDK depuis un JSON fourni."""
    if not args:
        print("Usage: mcp_apply_lr.py map '<json>'", file=sys.stderr)
        sys.exit(1)

    lr_params = json.loads(args[0])
    mapped = map_lr_params(lr_params)
    print(json.dumps(mapped, indent=2))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: mcp_apply_lr.py <prepare|sdk-keys|map> [args...]", file=sys.stderr)
        sys.exit(1)

    cmd = sys.argv[1]
    rest = sys.argv[2:]

    if cmd == "prepare":
        cmd_prepare(rest)
    elif cmd == "sdk-keys":
        cmd_sdk_keys(rest)
    elif cmd == "map":
        cmd_map(rest)
    else:
        print(f"Commande inconnue : {cmd}", file=sys.stderr)
        print("Commandes : prepare, sdk-keys, map", file=sys.stderr)
        sys.exit(1)
