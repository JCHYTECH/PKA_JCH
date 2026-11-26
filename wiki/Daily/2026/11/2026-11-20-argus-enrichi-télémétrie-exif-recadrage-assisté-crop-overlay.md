---
date: 2026-11-20
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-11-20 — Argus enrichi — télémétrie EXIF + recadrage assisté (crop overlays)

## Session — 20:57 — Argus enrichi — télémétrie EXIF + recadrage assisté (crop overlays)

### Contexte
- Modèle : deepseek-v4-pro
- Projet : PHOTO_AI_JURY

### Résumé
Session PHOTO_AI_JURY : enrichissement du pipeline Argus. Analyse de 2 CR3 (fous de Bassan, 76-79/100). Nouveaux modules : exif_raw.py (EXIF enrichie), exif_analysis.py (6 audits déterministes : ETTR, bougé, netteté, diffraction, DOF, bruit), crop_advisor.py (recadrage tiers/nombre d'or, gaze-aware, overlays A4 paysage+portrait). Injection télémétrie+audit dans le prompt Opus. Gravure du crop dans le XMP preset — BLOQUÉ : LrC n'applique pas le crop (sémantique corrigée + CropConstrainToUnitSquare + version 18.7/15.4, toujours KO).

### Actions
Créé scripts/exif_raw.py, exif_analysis.py, crop_advisor.py. Patché run_analysis.py (télémétrie + crop + sidecar) et generate_xmp.py (version 18.7/15.4). Analysé untitled-2643.CR3 et untitled-2648.CR3. Préréglages LrC 'in work - untitled-2643/2648' (racine + préfixe, sous-dossiers ignorés par LrC).

### Décisions
Ratio de base A4 (1:√2) paysage + portrait. Guide recadrage retenu = nombre d'or (phi). Marge 0,15. LrC ne lit QUE la racine de CameraRaw/Settings. Crop XMP = position des bords (0-1), pas fraction rognée.

### Prochaines étapes
Résoudre l'application du crop dans LrC (piste : sidecar .xmp à côté du CR3 au lieu du preset). Repasser untitled-2643 pour lui donner son crop. Différé : guide diagonale, détection d'habitudes, score NIMA.
