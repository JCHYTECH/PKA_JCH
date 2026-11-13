# Notes Camera WildNexus — Synthèse TKA_JCH

> Extraites d'Apple Notes le 2026-06-14. Sources : notes OV540, OV5640, INFOS CAMERA POUR ESP32.

---

## Lentille recommandée pour wildlife (3-12m)

**M12 6mm ou 8mm** — FOV 40-50°, full glass (4G-6G), f/2.0 minimum.

- Focus fixe réglé à ~8m → profondeur de champ de 3m à l'infini
- Filetage M12 + lock ring ou colle pour geler le focus
- Filtre IR-Cut (650nm) pour usage jour, NoIR pour nuit avec LED 850nm
- Pour grand angle (90-120°) : 2.1mm ou 2.8mm
- Pour reconnaissance (65-75°) : 3.6mm

---

## Gestion batterie — PIR + Deep Sleep

- MOSFET power-gating obligatoire : couper VCC/DOVDD du OV5640 (le standby logiciel laisse une consommation résiduelle)
- PIR externe sur GPIO RTC → wake ESP32-S3 → power cam → snapshot SD → sleep
- Consommation en deep sleep : microampères

---

## Contraintes OV5640 + ESP32-S3

- **PSRAM obligatoire** : 4-8 Mo pour buffer 5MP
- **FPS limité** : ~5 FPS en 2592×1944, 25-30 FPS seulement en SVGA/VGA
- **Dissipation thermique** : le OV5640 chauffe, prévoir aération/dissipateur dans le boîtier
- **Wi-Fi lent** : une JPEG 5MP prend du temps à transmettre → privilégier stockage SD local
- Module Arducam pré-équipé M12 recommandé (plug-and-play) vs adaptateur 3D imprimé

---

## Références

- Arducam M12 modules : https://blog.arducam.com/esp32-machine-vision-learning-guide/
- ESP32-CAM objectif M12 : https://www.instructables.com, https://www.reddit.com
- OV5640 datasheet : cf. `datasheets/`
