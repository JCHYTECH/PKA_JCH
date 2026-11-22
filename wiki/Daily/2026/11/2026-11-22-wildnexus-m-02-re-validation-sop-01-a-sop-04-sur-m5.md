---
date: 2026-11-22
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-11-22 — WildNexus M-02 re-validation SOP-01 à SOP-04 sur M5

## Session — 22:09 — WildNexus M-02 re-validation SOP-01 à SOP-04 sur M5

### Contexte
- Modèle : deepseek-v4-pro
- Projet : WILDNEXUS

### Résumé
Re-validation des phases A→D du prototype M-02 WildNexus sur le M5, avec la nouvelle chaîne d'outillage (Arduino IDE 2.3.10 + esp32 core 3.3.10, arduino-cli 1.6.0, PPK2 piloté en CLI via ppk2-api 0.9.2). Carte identifiée : ESP32-S3 QFN56 rev v0.2, MAC 58:e6:c5:74:7d:2c, flash 8MB quad (Micron), PSRAM 8MB OPI. Alive check, deep sleep 30 s, mesure PPK2 (deep sleep ~1061 µA, overhead DevKit) et réveil court 20 cycles tous validés, cohérents avec juin 2026.

### Actions
Flash et moniteur série de wn_blink (alive 1×/s) — SOP-01.
Flash et vérification deep sleep 30 s (rst:0x5 DSLEEP, intervalle 31 s) — SOP-02.
Mesure PPK2 deep sleep (Source Meter 5 V, ppk2-api) : 1061 µA médiane, pic 158 mA — SOP-03.
20/20 cycles wn_wake_short (intervalle 17,5 s) + 6/6 mesurés PPK2 — SOP-04.
Ajout note CDC On Boot dans SOP-01.
Carte identifiée via esptool flash_id.

### Décisions
Règle durable : CDC On Boot = OFF quand on flashe via le port CP2102/UART (sinon Serial part sur l'USB natif).
Règle durable : tout changement PSRAM/FlashSize/CDC exige arduino-cli compile --clean (sinon sdkconfig périmé réutilisé).
PPK2 piloté en CLI via ppk2-api (mesure sans la GUI Power Profiler).

### Prochaines étapes
SOP-05 Phase E — simulation cycle événement (PIR + action + sommeil).
Re-mesurer le deep sleep sur PCB nu pour confirmer <20 µA (sans l'overhead DevKit ~1 mA).
Gate 1 : inventaire matériel au banc (checklist INVENTAIRE 2026-11-12).
