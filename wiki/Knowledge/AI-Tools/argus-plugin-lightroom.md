---
date: 2026-05-02
tags: [plugin, lightroom, [[Argus]], photo, claude-api, workflow]
type: knowledge
domain: AI-Tools
status: stable
---

# [[Argus]] — Plugin Lightroom Classic

Plugin d'analyse photographique IA intégré directement dans Lightroom Classic. Un clic droit → rapport PDF professionnel + preset XMP appliqué automatiquement en Develop.

---

## Architecture

```
ArgusAnalysis.lua          ← Plugin LR (Lua 5.1, SDK LR 6.0)
    └── io.popen →
        run_analysis.py    ← Orchestrateur Python
            ├── dng_extract.py      ← Extraction preview RAW (exiftool)
            ├── color_analysis.py   ← Couleur moyenne + complémentaire
            ├── pdf_report.py       ← Rapport PDF (reportlab)
            └── generate_xmp.py    ← Preset XMP Lightroom
```

**Modèle IA :** `claude-opus-4-7` (vision)  
**Clé API :** `~/.config/pka-jch/anthropic_key.txt`

---

## Workflow utilisateur

1. Sélectionner une photo dans LR (JPEG, RAW, CR3, NEF, ARW…)
2. `Cmd+'` — créer la copie virtuelle manuellement
3. **Extras → Analyser avec [[Argus]]**
4. Valider le dialog de rappel
5. ~20-25 sec → réglages Develop appliqués + dialog résultat

---

## Outputs

| Fichier | Destination |
|---------|-------------|
| Rapport PDF | `PKA_JCH/PHOTO/analyses/<stem>_analyse.pdf` |
| Preset XMP | `PKA_JCH/PHOTO/presets/<stem>.xmp` |

### Contenu du PDF
- Photo miniature + fiche technique (boîtier, objectif, ISO, vitesse, focale)
- Scores jury sur 5 axes (composition, exposition, netteté, technique, impact)
- Analyse chromatique (couleur moyenne + complémentaire)
- Critique détaillée par axe
- Corrections Lightroom recommandées avec justifications
- Indicateur température : `XXXX K → YYYY K  ▲/▼ N/5`
- Pistes de retouche locale

---

## Formats RAW supportés

| Extension | Marque |
|-----------|--------|
| `.cr2` `.cr3` | Canon |
| `.nef` | Nikon |
| `.arw` | Sony |
| `.orf` | Olympus / OM System |
| `.rw2` | Panasonic |
| `.raf` | Fujifilm |
| `.pef` | Pentax |
| `.raw` | Leica / générique |
| `.dng` | Adobe (universel) |
| `.3fr` | Hasselblad |
| `.iiq` | Phase One |

Extraction via `exiftool` (cascade : `-JpgFromRaw` → `-PreviewImage` → `-OtherImage`).

---

## Réglages Develop appliqués

Le plugin applique via `LrDevelopController.setValue` les paramètres suivants :

| XMP | LR SDK | Note |
|-----|--------|------|
| `ColorTemperature` | `Temperature` | **Ignoré sur JPEG** (échelle Kelvin ≠ -100/+100) |
| `Tint` | `Tint` | |
| `Exposure2012` | `Exposure` | |
| `Contrast2012` | `Contrast` | |
| `Highlights2012` | `Highlights` | |
| `Shadows2012` | `Shadows` | |
| `Whites2012` | `Whites` | |
| `Blacks2012` | `Blacks` | |
| `Clarity2012` | `Clarity` | |
| `Dehaze` | `Dehaze` | |
| `Vibrance` | `Vibrance` | |
| `Saturation` | `Saturation` | |

---

## Limitations connues

| Limitation | Cause | Workaround |
|------------|-------|------------|
| Copie virtuelle non automatique | `LrCatalog:createVirtualCopies` retourne nil — bug SDK LR | `Cmd+'` manuel avant analyse |
| Temperature ignorée sur JPEG | LR Develop JPEG : échelle -100/+100, pas Kelvin | Appliquer le XMP manuellement ou travailler en RAW |
| Preview RAW = qualité réduite | Miniature JPEG embarquée (~2-8 MP) | Utiliser DNG ou JPEG export haute résolution pour meilleure analyse |

---

## Dépendances

```bash
# Python (installées dans /usr/local/bin/python3)
pip install anthropic pillow numpy reportlab

# Système
brew install exiftool   # extraction preview RAW
```

---

## Fichiers clés

```
PKA_JCH/PHOTO/plugin/argus.lrplugin/
    Info.lua
    ArgusAnalysis.lua

~/.claude/skills/photo-analyse-wildlife/scripts/
    run_analysis.py
    dng_extract.py
    color_analysis.py
    pdf_report.py
    generate_xmp.py
```

---

## Historique

| Date | Version | Changement |
|------|---------|------------|
| 2026-05-01 | v0.1 | Prototype — CLI [[Python]] seul |
| 2026-05-01 | v0.5 | Plugin LR intégré, premier test Bernache du Canada (76/100) |
| 2026-05-02 | v1.0 | XMP corrigé (WhiteBalance=Custom), use_defaults=False, workflow Cmd+' stabilisé |
| 2026-05-02 | v1.1 | Support CR3 (exiftool), temp_level -5/+5, JPEG Temperature fix, tous formats RAW |
