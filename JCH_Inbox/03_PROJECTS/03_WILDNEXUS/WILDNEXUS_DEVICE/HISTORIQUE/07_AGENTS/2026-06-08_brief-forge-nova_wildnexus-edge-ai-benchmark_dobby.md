# Brief — Benchmark Edge AI sur ESP32-S3 (MobileNet-SSD)

**De :** [[Dobby]] 🦉
**Pour :** [[Forge]] 🦦 + [[Nova]] 🦋
**Date :** 2026-06-08
**Priorité :** M-02 — bloque acceptation ADR-010
**ADR lié :** ADR-010 — point de réserve R4

## Contexte

L'ADR-010 exige un filtre de détection humaine embarqué sur ESP32-S3 (MobileNet-SSD quantifié INT8, résolution VGA 640×480).

Les critères théoriques :
- > 90 % recall humain à 5 m (jour)
- > 80 % recall humain à 5 m (nuit IR)
- < 5 % faux positifs sur faune
- Latence < 2s par frame

Ces chiffres n'ont **jamais été testés sur le matériel cible**. La réserve R4 exige un benchmark réel avant fermeture M-02. Si l'ESP32-S3 échoue → trigger migration MCU vers RV1106/STM32N6 (ADR-001).

## Mission

1. **[[Forge]]** : sélectionner et quantifier un modèle MobileNet-SSD (ou équivalent) compatible ESP32-S3 PSRAM (≥ 8 MB). Mesurer la latence d'inférence sur VGA 640×480. Si > 2s, tester aussi en 320×240 et rapporter.

2. **[[Nova]]** : constituer un jeu de test minimal (20-30 images) couvrant : humain jour (5 m, 10 m), humain nuit IR, faune (cerf, sanglier, [[renard]]), faux positifs potentiels (tronc, rocher). Annoter et mesurer recall/précision.

3. Livrable commun : **rapport de benchmark** — tableau recall/précision × condition, latence mesurée, consommation RAM, conclusion GO/NO-GO pour ESP32-S3.

## Format livrable

`YYYY-MM-DD_forge_nova_wildnexus-edge-ai-benchmark.md` dans `TEAM_Inbox/`

## Deadline

Avant fermeture M-02.

## Voir aussi

- `ADR-010` — critères de succès §1, trigger migration MCU
- `ADR-001` — fallback RV1106/STM32N6
- `ADR-005` — budget énergétique à croiser avec conso inférence
