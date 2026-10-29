# Brief — Analyse caméra WildNexus : ESP32-Cam + OV2640

**De :** [[Dobby]] 🦉  
**Pour :** [[Araignée]] #30 (IoT), [[Fourmi]] #31 (Bench), [[Chouette]] #25 (Terrain)  
**Date :** 2026-06-12  
**Priorité :** Moyenne  
**Projet :** 03_WILDNEXUS  

---

## Contexte

JCH a déposé deux documents techniques dans l'[[inbox]] :

1. **ESP32-Cam M12 Lens Hack** (Instructables) — Modification hardware pour remplacer la lentille OV2640 par une M12
2. **OV2640DS.pdf** — Datasheet du capteur OV2640 (2MP)

Fichiers déplacés → `03_PROJECTS/03_WILDNEXUS/`

## Mission

### [[Araignée]] #30 — IoT
- Évaluer le M12 lens hack pour le use-case caméra-piège
- Comparer OV2640 vs alternatives (OV5640, GC2053)
- Vérifier compatibilité stack LoRa/ESP32

### [[Fourmi]] #31 — Bench
- Extraire specs critiques du datasheet (conso, voltages, timings)
- Évaluer faisabilité lens hack (outils, risques)

### [[Chouette]] #25 — Terrain
- Impact qualité image en conditions faune/faible lumière
- Comparer avec caméras-pièges actuelles
- Proposer protocole test si pertinent

## Livrable

`TEAM_Inbox/2026-06-XX_araignee-fourmi-chouette_analyse-camera-wildnexus.md`

## Deadline

2026-06-19
