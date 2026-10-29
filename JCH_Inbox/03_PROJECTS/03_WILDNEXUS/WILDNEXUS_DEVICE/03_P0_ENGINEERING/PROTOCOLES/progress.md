# Protocole Progress — WILDNEXUS P0 M-02

> **Fichier State** — lu par Dobby avant toute affirmation sur l'avancement des protocoles.
> **Règle :** ne jamais déduire l'état d'un protocole d'artefacts (CSV, logs). Ce fichier est la source unique.
> **Dernière mise à jour :** 2026-07-05 — FW-04 ✅ + FW-05 ✅ (audio module + metadata, 11/11 host tests). 37/37 tests au total.

---

## Protocole : M-02 Partiel — Banc ESP32-S3 + PPK2 (Phases A→E)

| Phase | Description | Statut | Date | Résultat | Notes |
|-------|-------------|--------|------|----------|-------|
| A | ESP32 alive check (wn_blink) | ✅ done | 2026-06-16 | OK | DevKit #1 |
| B | Deep sleep 30s vérification | ✅ done | 2026-06-16 | OK | |
| C | Mesure deep sleep PPK2 | ✅ done | 2026-06-18 | Voir CSV | 5 acquisitions PPK2 |
| D | Réveil court 20 cycles | ⏳ pending | — | — | Firmware `wn_wake_short` prêt |
| E | Cycle simulé WildNexus | ⏳ pending | — | — | Firmware `wn_event_simulated` prêt |

## Protocole : SOPs Individuelles — Caméra & Radio

| SOP | Description | Statut | Date | Résultat | Notes |
|-----|-------------|--------|------|----------|-------|
| SOP-01 | ESP32 alive check | ✅ done | 2026-06-16 | OK | |
| SOP-02 | Deep sleep 30s | ✅ done | 2026-06-16 | OK | |
| SOP-03 | PPK2 deep sleep | ✅ done | 2026-06-18 | Voir CSV | |
| SOP-04 | Wake short 20 cycles | ⏳ pending | — | — | = Phase D |
| SOP-05 | Simulation cycle événement | ⏳ pending | — | — | = Phase E |
| SOP-06 | MicroSD | ⏳ pending | — | — | Besoin carte SD 128 GB |
| SOP-07 | LoRa | 🔴 blocked | — | — | Module non commandé (panier Mouser ~279€) |
| SOP-08 | Caméra OV5640 | ⏳ pending | — | — | Hardware ✅, pinout mappé wn_config.h |
| SOP-09 | PIR EKMB | ⏳ pending | — | — | PIR×2 reçus |
| SOP-10 | Batterie AA Buck | ⏳ pending | — | — | Buck×10 reçus |
| SOP-11 | Edge AI Benchmark | 🟡 blocked | — | — | Nécessite SOP-08 d'abord |
| SOP-12 | Micro Provisioning | ⏳ pending | — | — | |

## Protocole : SOPs Audio (ADR-013/016/017)

| SOP | Description | Statut | Date | Résultat | Notes |
|-----|-------------|--------|------|----------|-------|
| SOP-13 | I2S MEMS init + capture stéréo | ⏳ pending | — | — | Hardware ✅, pinout mappé. Code I2S prêt dans wn_audio.c. |
| SOP-14 | FFT 1024 — features spectrales | ✅ done | 2026-07-05 | 1kHz sine ✅, silence ✅, noise ✅ | FFT implémenté + testé sur host. 10 descripteurs validés. |
| SOP-15 | Clip WAV 3s + sidecar JSON | ✅ done | 2026-07-05 | 11/11 tests pass | WAV encode + JSON sidecar (CLIP + FFT) implémentés + testés. |
| SOP-16 | Payload spectral LoRa (type 0x05) | ✅ done | 2026-07-05 | 13/13 tests pass | Codec ADR-014 v2. Encode/decode roundtrip OK. |
| SOP-17 | Coexistence PIR + timer audio | ⏳ pending | — | — | State machine gère le routing, test hardware nécessaire. |
| SOP-18 | Budget énergétique audio (PPK2) | ⏳ pending | — | — | Mesure réelle sur banc. Estimation ~1,4 mAh/jour. |

## Protocole : Caméra

| Test | Description | Statut | Date | Résultat | Notes |
|------|-------------|--------|------|----------|-------|
| CAM-01 | ESP32-CAM OV2640 flash via FT232RL | ⏳ pending | — | — | Hardware ✅ |
| CAM-02 | OV5640 DVP pinout + capture | ⏳ pending | — | — | Hardware ✅, pinout mappé |
| CAM-03 | Test harness MobileNet-SSD | 🟡 blocked | — | — | Dataset 51 images, deadline 15/07, attend CAM-01 |

## Protocole : Firmware intégré (ADR-016)

| Test | Description | Statut | Date | Résultat | Notes |
|------|-------------|--------|------|----------|-------|
| FW-01 | Repo wildnexus-firmware créé | ✅ done | 2026-06-30 | ESP-IDF modulaire | Commit a85f1a9 |
| FW-02 | Codec payload ADR-014 (caméra + spectral) | ✅ done | 2026-07-05 | 13/13 tests | v0.2.0. Commit a85f1a9. |
| FW-03 | Machine d'états double cycle | ✅ done | 2026-07-05 | 13/13 tests host | v0.2.0. Dual-cycle. Commit 131f6fb. |
| FW-04 | Module wn_audio.c (I2S + FFT + WAV) | ✅ done | 2026-07-05 | 11/11 tests host | FFT radix-2 + 10 features + WAV encode + quantization. Commit 8c44793. |
| FW-05 | Module wn_audio_metadata.c (sidecar JSON) | ✅ done | 2026-07-05 | 11/11 tests host | CLIP + FFT sidecar JSON + filename + dirpath. Commit 8c44793. |

## Résumé tests firmware (37/37 host tests ✅)

| Suite | Tests | Statut | Commit |
|-------|-------|--------|--------|
| Codec (ADR-014) | 13/13 | ✅ | a85f1a9 |
| State machine (ADR-016) | 13/13 | ✅ | 131f6fb |
| Audio + metadata (ADR-013/017) | 11/11 | ✅ | 8c44793 |
| **TOTAL** | **37/37** | **✅** | |

## Dépendances critiques

```
SOP-07 (LoRa) ────── bloque ──→ transmission réelle (codec + state machine OK)
                                  
SOP-08 (Caméra) ─── bloque ──→ SOP-11 (Edge AI)
                                  CAM-03 (test harness)
                                  
SOP-13 (I2S init) ── bloque ──→ test réel sur hardware (code prêt)
                                   
Panier Mouser (~279€) ── bloque ──→ SOP-07 (LoRa)
Carte SD 128 GB (~15€) ── bloque ──→ SOP-06 (storage) + SOP-15 (stockage clips réels)
```

## Légende

| Symbole | Signification |
|---------|--------------|
| ✅ done | Phase exécutée et validée |
| ⏳ pending | En attente d'exécution |
| 🔴 blocked | Bloquée — voir notes |
| 🟡 blocked | Bloquée par dépendance |

---

*Mis à jour le 2026-07-05 — 5/5 tests firmware passés sans hardware (37/37). Tous les modules testables sur host sont livrés. Reste : tests hardware (SOP-08 caméra, SOP-13 I2S) + panier Mouser (LoRa). Source : git log, test output.*
