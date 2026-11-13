# Convergence capteurs — Van IOT × Serre IOT

> Croisement des besoins capteurs pour achat groupé
> Date : 2026-06-07 | Rédacteur : [[Dobby]] 🦉
> **Mis à jour 2026-07-08 v4** — Correction SNZB-04P (contact seul, pas de T°). Économie réelle : -1 capteur (-10€, JSN-SR04T → DS300 Tap)

## Capteurs communs — À commander ensemble

| Capteur | Van Qté | Serre Qté | Total | Modèle | Prix/u | Total € | Amazon ? |
|---------|---------|-----------|-------|--------|--------|---------|----------|
| Ouverture porte | 7 | 2-4 | **9-11** | Aqara MCCGQ11LM | 8 € | 72-88 € | ✅ |
| T°/HR Zigbee | 2 | 2 | **4** | Sonoff SNZB-02D | 10 € | 40 € | ✅ |
| Jauge eau ultrason | — | 1 | **1** | JSN-SR04T | 5 € | 5 € | ✅ |
| PIR extérieur | 1 | 1 | **2** | Optex BX-80NR + SNZB-04 | 21 €/lot | 42 € | ✅ |
| Fuite eau Zigbee | 1 | 1 | **2** | Aqara SJCGQ11LM | 12 € | 24 € | ✅ |
| Module relais 12V | 1 | 1 | **2** | SRD-12VDC | 5 € | 10 € | ✅ |
| ESP32-S3 DevKit | 1 | 1 | **2** | ESP32-S3 | 12 € | 24 € | ✅ |
| ZBDongle-E | 1 | 1 | **2** | Sonoff ZBDongle-E | 18 € | 36 € | ✅ |

**Sous-total commun : ~252 € — tout Amazon ✅**

> **Notes v4 (2026-07-08) :**
> - ⚠️ Le SNZB-04P est un capteur d'ouverture uniquement (pas de T°). Il ne remplace PAS le SNZB-02D. C'est une option d'upgrade (tamper alert, pile 5 ans) pour frigo et toit.
> - Van jauge eau 2→0 : remplacé par **DS300 Tap** (lecture directe des sondes CBE dans les cuves)
> - SNZB-02D extérieur : supprimé (→ BME280 en P3, fait T°+HR+pression)

## Plan d'achat groupé — 1 commande Amazon

Lot Amazon FR :
- Aqara MCCGQ11LM ×9 : 72 € *(van ×7 + serre ×2)*
- Sonoff SNZB-02D ×4 : 40 € *(van ×2 + serre ×2)*
- JSN-SR04T ×1 : 5 € *(serre uniquement)*
- Optex BX-80NR ×2 + SNZB-04 ×2 : 42 €
- Aqara SJCGQ11LM ×2 : 24 €
- Module relais SRD-12VDC ×2 : 10 €
- ESP32-S3 DevKit ×2 : 24 €
- ZBDongle-E ×2 : 36 €
- MPU6050 GY-521 ×1 : 4 €
**Total : ~257 € — 27 items** *(v1 : 275€ / 28 items)*

Puis ITEAD : SNZB-04P ×2 (~16 €) optionnels — upgrade tamper alert pour frigo et toit.
Puis AliExpress : INMP441 ×1 (~3 €) pour le dB van.

## Économie vs commandes séparées

| Sans convergence | Avec convergence (v2) |
|-----------------|----------------------|
| Van : ~185 € + Serre : ~200 € + ports | **Amazon : 257 € + ITEAD : 16 € + AliEx : 3 €** |
| **~410 €** | **~276 €** |
| | **Économie : ~134 € + un seul colis** |
| | *(vs commandes séparées)* |

## Historique

| Date | Version | Change |
|------|---------|--------|
| 2026-06-07 | v1 | Version initiale — 28 items, 275€ |
| 2026-07-08 | v4 | Correction SNZB-04P (contact seul). 27 items, 257€. Économie réelle : -1 capteur |
